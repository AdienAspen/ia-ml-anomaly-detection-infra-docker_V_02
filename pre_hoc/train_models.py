"""Train iForest and HDBSCAN models from derived OTel feature datasets."""

from __future__ import annotations

from pathlib import Path


IFOREST_MODEL = Path("artifacts/models/v_02/iforest_otel_model_v0_1.joblib")
HDBSCAN_MODEL = Path("artifacts/models/v_02/hdbscan_otel_model_v0_1.joblib")
POST_FILTER_POLICY = Path("artifacts/models/v_02/post_filter_policy_v0_1.json")


def main() -> None:
    print(f"Training scaffold. iForest artifact: {IFOREST_MODEL}")
    print(f"HDBSCAN artifact: {HDBSCAN_MODEL}")
    print(f"Post-filter policy: {POST_FILTER_POLICY}")


if __name__ == "__main__":
    main()
