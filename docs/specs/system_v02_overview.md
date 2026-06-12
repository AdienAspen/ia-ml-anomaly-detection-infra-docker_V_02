# System V_02 Overview

V_02 is an OTel-first, long-lived, auditable observability system.

The end-to-end flow is:

```text
instrumented service
-> OTel trace/span/log/metric
-> telemetry backend
-> dataset builder
-> ML detection pipeline
-> context engine
-> agentic reasoning
-> tool call or recommendation
-> audit event
```

Development order is mandatory:

1. Define specs and contracts.
2. Validate contracts with tests.
3. Implement minimal services.
4. Integrate OpenTelemetry.
5. Build datasets from telemetry.
6. Run classical ML detection.
7. Build context.
8. Run agentic reasoning.
9. Audit every decision.
10. Run in shadow mode.

Core rule: classical ML detects; the agentic layer interprets, reasons, explains, estimates confidence, and recommends.
