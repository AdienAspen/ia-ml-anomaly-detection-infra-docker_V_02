"""Generate PRE-HOC raw OTel telemetry from YAML scenarios.

This is a scaffold entry point. The first implementation target is exporting
raw OTel JSON through the Collector file/debug path.
"""

from __future__ import annotations

from pathlib import Path


DEFAULT_OUTPUT = Path("artifacts/telemetry/pre_hoc/raw/otel_pre_hoc_raw_traces_v0_1.jsonl")


def main() -> None:
    print(f"PRE-HOC generator scaffold. Target artifact: {DEFAULT_OUTPUT}")


if __name__ == "__main__":
    main()
