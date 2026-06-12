# Context Slice Contract V0.1

Defines the minimal evidence bundle consumed by the agentic reasoning layer.

A context slice must link:

- the original `trace_id`
- the service or operation under analysis
- the ML cluster or anomaly decision
- evidence summaries
- operational timeline

The context slice is read-only evidence. It must not contain secrets or mutation capabilities.
