# Industrial Sandbox V_02

Agentic Observability Layer, OTel-first.

V_02 is not a refactor of V_01. It is a new controlled-quality step built around:

- Spec-Driven Development.
- Contract-Driven Development.
- OpenTelemetry as the central operational nervous system.
- Classical ML for detection.
- Agentic reasoning for interpretation, explanation, confidence, and recommendation.
- Auditability and governance as first-class outputs.

## Phase 0 Scope

This bootstrap phase establishes the repository frame before runtime implementation:

- system specs under `docs/specs/`
- versioned JSON contracts under `contracts/`
- contract tests under `tests/contracts/`
- UV-first Python project configuration
- placeholder Docker Compose entry point

## UV-first Policy

Python dependency management is UV-first. Use `pyproject.toml` as the project source of truth and keep work encapsulated in `.venv`.

Recommended commands:

```bash
uv sync
uv run python -m unittest discover -s tests/contracts
```

`pip` and `requirements.txt` should only be introduced when there is a concrete compatibility reason.

## Phase 0 Closure

Phase 0 is closed when all contract tests pass.

## Phase 1 Architectural Baseline

Phase 1 expands the original "OTel services" idea into two coordinated modes:

- `pre_hoc/`: offline synthetic telemetry generation for training data.
- `ad_hoc/`: online runtime simulation and inference.

Both modes are governed by shared scenario definitions:

- `configs/scenarios/`
- `scenario_library/`

Redis Streams is the V_02 online inference path. Kafka, Flink, Prometheus, and Kubernetes are represented as V_03 readiness placeholders only.
