# Audit Event Contract V0.1

Defines the minimum audit event emitted by each critical V_02 component.

Audit events must capture:

- `event_id`
- `trace_id`
- `component`
- `action`
- `timestamp`
- `outcome`
- `provenance`

The audit layer must make a decision reconstructible from `trace_id`.
