"""Load scenario YAML definitions."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


SCENARIOS_ROOT = Path(__file__).resolve().parents[1] / "configs" / "scenarios"


def scenario_path(scenario_name: str) -> Path:
    """Return the path for a versioned scenario configuration."""

    return SCENARIOS_ROOT / scenario_name


def load_scenario(path: str | Path) -> dict[str, Any]:
    """Load a scenario YAML file from an explicit path or scenario filename."""

    candidate = Path(path)
    if not candidate.exists():
        candidate = SCENARIOS_ROOT / str(path)
    with candidate.open(encoding="utf-8") as handle:
        payload = yaml.safe_load(handle) or {}
    validate_scenario_config(payload)
    return payload


def load_scenarios(paths: list[str | Path]) -> list[dict[str, Any]]:
    """Load multiple scenario configs in order."""

    return [load_scenario(path) for path in paths]


def validate_scenario_config(payload: dict[str, Any]) -> None:
    """Validate the minimum scenario shape required by PRE-HOC and AD-HOC."""

    required = {
        "schema_version",
        "scenario_id",
        "mode_support",
        "services",
        "noise",
        "propagation",
        "labels",
        "telemetry",
        "metric_baselines",
    }
    missing = sorted(required.difference(payload))
    if missing:
        raise ValueError(f"scenario config missing required fields: {', '.join(missing)}")
    if payload["schema_version"] != "scenario_config_v0_1":
        raise ValueError("unsupported scenario schema_version")
    if not payload["mode_support"].get("pre_hoc"):
        raise ValueError("scenario does not support PRE-HOC mode")
    if not payload["services"]:
        raise ValueError("scenario must define at least one service")
