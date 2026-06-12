"""Generate PRE-HOC raw OTel telemetry from YAML scenarios.

The implementation preserves the V_01 scenario-engine lessons:

- stochastic jitter
- intensity scaling
- propagation sequence
- partial recovery labels
- negative/noise scenarios

The output is raw OTel-shaped JSONL. A later Collector file/debug exporter can
replace the local writer without changing scenario semantics.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from datetime import datetime, timedelta, timezone
from random import Random
from typing import Any
import uuid
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from opentelemetry.sdk.trace import ReadableSpan, TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, SpanExporter, SpanExportResult
from opentelemetry.sdk.resources import Resource

from scenario_library.loader import load_scenarios
from scenario_library.noise import bounded_jitter_seconds, intensity_scale


DEFAULT_OUTPUT = Path("artifacts/telemetry/pre_hoc/raw/otel_pre_hoc_raw_traces_v0_1.jsonl")
DEFAULT_SCENARIOS = [
    "baseline_nominal_v0_1.yaml",
    "latency_propagation_jitter_v0_1.yaml",
]

SERVICE_OPERATIONS = {
    "payments-api": "process_payment",
    "redis-broker": "publish_payment_event",
    "checkout-api": "update_checkout_state",
    "orders-api": "confirm_order",
}

NOISE_RATIO = {
    "latency_ms": 0.06,
    "error_rate": 0.22,
    "throughput": 0.08,
    "queue_depth": 0.20,
}


class JsonlSpanExporter(SpanExporter):
    """Write ended spans as JSONL records preserving trace hierarchy."""

    def __init__(self, output_path: Path) -> None:
        self.output_path = output_path
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self._handle = self.output_path.open("w", encoding="utf-8")

    def export(self, spans: tuple[ReadableSpan, ...] | list[ReadableSpan]) -> SpanExportResult:
        for span in spans:
            self._handle.write(json.dumps(_span_to_otel_json(span), sort_keys=True) + "\n")
        self._handle.flush()
        return SpanExportResult.SUCCESS

    def shutdown(self) -> None:
        self._handle.close()


def generate_training_data(
    *,
    scenario_paths: list[str],
    output_path: Path = DEFAULT_OUTPUT,
    seed: int = 7,
    steps: int | None = None,
    start_at: datetime | None = None,
) -> dict[str, Any]:
    """Generate raw OTel JSONL for one or more versioned scenarios."""

    scenarios = load_scenarios(scenario_paths)
    provider = TracerProvider(resource=Resource.create({"service.namespace": "industrial-sandbox-v02", "deployment.environment": "pre_hoc"}))
    exporter = JsonlSpanExporter(output_path)
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    tracer = provider.get_tracer("industrial_sandbox_v02.pre_hoc")

    try:
        total_spans = 0
        scenario_summaries = []
        for scenario_index, scenario in enumerate(scenarios):
            rng = Random(seed + scenario_index)
            summary = _emit_scenario(tracer, scenario, rng=rng, seed=seed + scenario_index, steps_override=steps, start_at=start_at)
            scenario_summaries.append(summary)
            total_spans += summary["spans_generated"]
    finally:
        provider.force_flush()
        provider.shutdown()

    return {
        "schema_version": "otel_pre_hoc_generation_summary_v0_1",
        "output_path": str(output_path),
        "scenarios": scenario_summaries,
        "spans_generated": total_spans,
    }


def main() -> None:
    args = _parse_args()
    summary = generate_training_data(
        scenario_paths=args.scenario,
        output_path=Path(args.output),
        seed=args.seed,
        steps=args.steps,
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate PRE-HOC raw OTel telemetry JSONL.")
    parser.add_argument("--scenario", action="append", default=None, help="Scenario YAML filename or path. Repeatable.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Output JSONL artifact path.")
    parser.add_argument("--seed", type=int, default=7, help="Deterministic random seed.")
    parser.add_argument("--steps", type=int, default=None, help="Override scenario telemetry steps.")
    args = parser.parse_args()
    args.scenario = args.scenario or DEFAULT_SCENARIOS
    return args


def _emit_scenario(
    tracer: Any,
    scenario: dict[str, Any],
    *,
    rng: Random,
    seed: int,
    steps_override: int | None,
    start_at: datetime | None,
) -> dict[str, Any]:
    scenario_id = scenario["scenario_id"]
    telemetry = scenario["telemetry"]
    steps = steps_override or int(telemetry.get("steps", 6))
    interval_seconds = int(telemetry.get("interval_seconds", 30))
    services = list(scenario["services"])
    propagation_sequence = list(scenario["propagation"].get("sequence", []))
    activation_steps = _build_activation_steps(services, propagation_sequence)
    base_start = start_at or datetime(2026, 6, 12, 12, 0, tzinfo=timezone.utc)
    scenario_intensity = intensity_scale(rng, scenario["noise"])
    spans_generated = 0

    for step in range(steps):
        step_time = base_start + timedelta(seconds=step * interval_seconds)
        root_name = f"{scenario_id}.step_{step:04d}"
        with tracer.start_as_current_span(
            root_name,
            attributes={
                "scenario.id": scenario_id,
                "scenario.class_name": scenario["labels"]["class_name"],
                "scenario.anomaly": scenario["labels"]["anomaly"],
                "scenario.seed": seed,
                "scenario.step": step,
                "pre_hoc.raw_artifact": True,
            },
        ) as root_span:
            root_span.set_attribute("operation.name", telemetry.get("root_operation", "scenario_step"))
            spans_generated += 1
            for service_name in services:
                state = _service_state(
                    scenario=scenario,
                    service_name=service_name,
                    step=step,
                    steps=steps,
                    activation_steps=activation_steps,
                    intensity=scenario_intensity,
                    rng=rng,
                )
                metrics = _service_metrics(scenario, service_name, state=state, rng=rng)
                jitter = bounded_jitter_seconds(rng, scenario["noise"])
                operation_name = SERVICE_OPERATIONS.get(service_name, f"{service_name}.operation")
                with tracer.start_as_current_span(
                    operation_name,
                    attributes={
                        "service.name": service_name,
                        "operation.name": operation_name,
                        "scenario.id": scenario_id,
                        "scenario.class_name": scenario["labels"]["class_name"],
                        "scenario.anomaly": scenario["labels"]["anomaly"],
                        "scenario.phase": state["phase"],
                        "scenario.expected_propagation": bool(propagation_sequence),
                        "scenario.activation_step": activation_steps.get(service_name, -1)
                        if activation_steps.get(service_name) is not None
                        else -1,
                        "scenario.jitter_seconds": jitter,
                        "scenario.service_intensity": state["intensity"],
                        "event.timestamp": (step_time + timedelta(seconds=jitter)).isoformat(),
                        "http.status_code": 500 if metrics.get("error_rate", 0.0) >= 0.05 else 200,
                        "duration_ms": metrics["latency_ms"],
                        **{f"metric.{key}": value for key, value in metrics.items()},
                    },
                ):
                    spans_generated += 1

    return {
        "scenario_id": scenario_id,
        "steps": steps,
        "spans_generated": spans_generated,
        "services": services,
    }


def _build_activation_steps(services: list[str], propagation_sequence: list[str]) -> dict[str, int | None]:
    activation = {service_name: None for service_name in services}
    root_start = 2
    current_step = root_start
    for index, service_name in enumerate(propagation_sequence):
        activation[service_name] = current_step
        if index < len(propagation_sequence) - 1:
            current_step += 1
    return activation


def _service_state(
    *,
    scenario: dict[str, Any],
    service_name: str,
    step: int,
    steps: int,
    activation_steps: dict[str, int | None],
    intensity: float,
    rng: Random,
) -> dict[str, Any]:
    labels = scenario["labels"]
    activation_step = activation_steps.get(service_name)
    is_active = activation_step is not None and step >= activation_step
    service_intensity = 1.0
    phase = "baseline"

    if labels["class_name"] == "latency_propagation" and is_active:
        service_intensity = 1.0 + 0.40 * intensity + 0.05 * rng.random()
        phase = "partial_recovery" if step >= max(steps - 1, 0) and scenario["noise"].get("recovery_phases") else "propagating"
    elif labels["class_name"] == "nominal":
        service_intensity = 1.0 + rng.uniform(-0.03, 0.03)

    return {"intensity": max(service_intensity, 0.01), "phase": phase}


def _service_metrics(scenario: dict[str, Any], service_name: str, *, state: dict[str, Any], rng: Random) -> dict[str, float]:
    baselines = scenario["metric_baselines"][service_name]
    metrics: dict[str, float] = {}
    for metric_name, baseline in baselines.items():
        noise = 1.0 + rng.uniform(-NOISE_RATIO.get(metric_name, 0.10), NOISE_RATIO.get(metric_name, 0.10))
        if metric_name == "throughput":
            value = float(baseline) * max(0.35, 2.0 - state["intensity"]) * noise
        else:
            value = float(baseline) * state["intensity"] * noise
        metrics[metric_name] = round(max(value, 0.0), 6)
    metrics.setdefault("latency_ms", round(10.0 * state["intensity"], 6))
    return metrics


def _span_to_otel_json(span: ReadableSpan) -> dict[str, Any]:
    context = span.get_span_context()
    parent = span.parent
    attributes = dict(span.attributes or {})
    service_name = attributes.get("service.name", "scenario-controller")
    status_code = attributes.get("http.status_code", 200)
    duration_ms = attributes.get("duration_ms")
    if duration_ms is None and span.end_time and span.start_time:
        duration_ms = (span.end_time - span.start_time) / 1_000_000

    return {
        "resource": {
            "attributes": {
                "service.name": service_name,
                "service.namespace": "industrial-sandbox-v02",
                "deployment.environment": "pre_hoc",
            }
        },
        "scope": {"name": "industrial_sandbox_v02.pre_hoc"},
        "span": {
            "name": span.name,
            "trace_id": format(context.trace_id, "032x"),
            "span_id": format(context.span_id, "016x"),
            "parent_span_id": format(parent.span_id, "016x") if parent else None,
            "start_time_unix_nano": span.start_time,
            "end_time_unix_nano": span.end_time,
            "attributes": attributes,
            "status_code": "ERROR" if int(status_code) >= 500 else "OK",
            "duration_ms": duration_ms,
        },
    }


if __name__ == "__main__":
    main()
