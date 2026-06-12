"""AD-HOC streaming anomaly detector scaffold."""

from __future__ import annotations


RAW_STREAM = "otel.telemetry.raw.v0_1"
FEATURE_STREAM = "otel.features.online.v0_1"
DECISION_STREAM = "ml.cluster_decisions.v0_1"


def main() -> None:
    print("Streaming detector scaffold.")
    print(f"Input streams: {RAW_STREAM}, {FEATURE_STREAM}")
    print(f"Output stream: {DECISION_STREAM}")


if __name__ == "__main__":
    main()
