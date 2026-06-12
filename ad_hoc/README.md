# AD-HOC

Online runtime path for simulated services and streaming inference.

Initial flow:

```text
scenario YAML
-> services with OTel SDK
-> OTel Collector gRPC
-> Redis Streams
-> anomaly-detector
-> Context Engine
-> Agentic Reasoning
-> Audit
```

Redis Streams is the V_02 low-latency inference queue.
