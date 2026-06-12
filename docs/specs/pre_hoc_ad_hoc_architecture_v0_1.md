# PRE-HOC / AD-HOC Architecture V0.1

V_02 separates OpenTelemetry usage into two coordinated modes.

## PRE-HOC

PRE-HOC is the offline path for synthetic telemetry generation, dataset construction, model training, and validation.

The first PRE-HOC artifact is raw OTel JSON exported by the Collector in file or debug mode. Tabular datasets are derived later.

```text
scenario YAML
-> scenario_library
-> OTel SDK
-> OTel Collector file/debug exporter
-> raw telemetry JSON
-> feature extraction
-> tabular dataset
-> iForest + HDBSCAN training
-> model artifacts
```

## AD-HOC

AD-HOC is the runtime path for long-lived simulated services and streaming inference.

```text
scenario YAML
-> scenario_library
-> simulated services
-> OTel SDK
-> OTel Collector gRPC
-> Redis Streams
-> anomaly-detector
-> Context Engine
-> Agentic Reasoning
-> Audit
```

## Shared Rule

The services may differ between PRE-HOC and AD-HOC, but scenario semantics must not. YAML scenarios are the source of truth for jitter, intensity, recovery phases, propagation order, labels, and expected operational intent.
