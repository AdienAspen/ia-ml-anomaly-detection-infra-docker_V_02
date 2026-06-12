# Scenario Library

Shared scenario execution layer for PRE-HOC and AD-HOC.

The library loads YAML scenario definitions from `configs/scenarios/` and exposes reusable parameters for:

- synthetic noise
- propagation order
- recovery phases
- labels
- runtime mode support

This preserves V_01 scenario knowledge while switching the emission medium to OTel.
