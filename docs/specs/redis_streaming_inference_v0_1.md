# Redis Streaming Inference V0.1

Redis Streams is the V_02 online inference path.

Rationale:

- low-latency operational queue
- simple runtime dependency for Project 1
- suitable bridge between OTel-derived telemetry and the anomaly detector
- avoids coupling online inference to analytical backends

Prometheus, Kafka, Flink, and historical telemetry stores are not the V_02 critical path for online inference. They remain relevant for observability, historical analysis, PRE-HOC, and V_03 readiness.

Initial stream names:

```text
otel.telemetry.raw.v0_1
otel.features.online.v0_1
ml.cluster_decisions.v0_1
agent.context_requests.v0_1
audit.events.v0_1
```
