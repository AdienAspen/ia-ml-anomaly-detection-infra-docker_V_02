"""Build derived feature and label datasets from raw PRE-HOC OTel JSON."""

from __future__ import annotations

from pathlib import Path


DEFAULT_RAW_INPUT = Path("artifacts/telemetry/pre_hoc/raw/otel_pre_hoc_raw_traces_v0_1.jsonl")
DEFAULT_FEATURES_OUTPUT = Path("artifacts/datasets/pre_hoc/otel_pre_hoc_feature_dataset_v0_1.parquet")
DEFAULT_LABELS_OUTPUT = Path("artifacts/datasets/pre_hoc/otel_pre_hoc_labels_v0_1.parquet")


def main() -> None:
    print(f"Dataset builder scaffold. Raw input: {DEFAULT_RAW_INPUT}")
    print(f"Feature output: {DEFAULT_FEATURES_OUTPUT}")
    print(f"Labels output: {DEFAULT_LABELS_OUTPUT}")


if __name__ == "__main__":
    main()
