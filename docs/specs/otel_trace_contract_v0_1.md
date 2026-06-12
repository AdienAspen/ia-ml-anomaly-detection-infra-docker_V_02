# OTel Trace Event Contract V0.1

Defines the minimal normalized trace event consumed by downstream V_02 components.

Required identifiers:

- `schema_version`
- `trace_id`
- `span_id`
- `service_name`
- `operation_name`
- `timestamp`

Required operational fields:

- `duration_ms`
- `status_code`
- `attributes`

The contract intentionally keeps OTel-native identifiers visible so all downstream outputs remain reconstructible by `trace_id`.
