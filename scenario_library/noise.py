"""Noise profile primitives shared by PRE-HOC and AD-HOC."""

from __future__ import annotations

from dataclasses import dataclass
from random import Random


@dataclass(frozen=True)
class JitterRange:
    """Seconds of causal jitter to apply around a scenario event."""

    minimum: float
    maximum: float


@dataclass(frozen=True)
class RecoveryProfile:
    """Ordered recovery phases inherited from V_01 scenario design."""

    phases: tuple[int, ...]


def bounded_jitter_seconds(rng: Random, config: dict) -> int:
    """Return integer jitter using the V_01 min/max control style."""

    jitter = config.get("jitter_seconds", {})
    return rng.randint(int(jitter.get("min", 0)), int(jitter.get("max", 0)))


def intensity_scale(rng: Random, config: dict) -> float:
    """Return scenario intensity using V_01 ranges plus V_02 distributions."""

    intensity = config.get("intensity", {})
    distribution = intensity.get("distribution", "constant")
    if distribution == "constant":
        return float(intensity.get("value", 1.0))
    if distribution == "lognormal":
        return max(rng.lognormvariate(float(intensity.get("mean", 1.0)), float(intensity.get("sigma", 0.35))), 0.01)
    if distribution == "uniform":
        return rng.uniform(float(intensity.get("min", 0.6)), float(intensity.get("max", 1.4)))
    raise ValueError(f"unsupported intensity distribution: {distribution}")
