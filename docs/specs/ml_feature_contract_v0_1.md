# ML Feature Vector Contract V0.1

Defines the feature vector produced from OTel traces and consumed by the ML detection pipeline.

Required linkage fields:

- `schema_version`
- `trace_id`
- `service_name`
- `window_start`
- `window_end`

Required feature payload:

- `features`

Feature keys are explicit numeric measurements derived from traces, metrics, or logs.
