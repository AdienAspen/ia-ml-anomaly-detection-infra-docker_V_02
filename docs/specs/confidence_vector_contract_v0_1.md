# Confidence Vector Contract V0.1

Defines how the agentic layer explains confidence.

Confidence is decomposed into named dimensions, not a single opaque score:

- `data_quality`
- `trace_completeness`
- `ml_signal_strength`
- `context_coverage`
- `recommendation_confidence`

Every confidence vector must remain linked to a `trace_id` and an `agent_decision_id`.
