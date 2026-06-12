# Scenario Library Contract V0.1

The scenario library preserves V_01 synthetic-noise knowledge while changing the emission medium to OpenTelemetry.

Reusable scenario dimensions:

- jitter
- intensity distribution
- recovery phases
- propagation sequence
- hidden dependency hints
- intermittent failure behavior
- maintenance windows
- labels for training and validation

The YAML definitions under `configs/scenarios/` are the source of truth. Python code must load and execute those definitions; it must not hard-code scenario semantics.
