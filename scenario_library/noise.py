"""Noise profile primitives shared by PRE-HOC and AD-HOC."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class JitterRange:
    """Seconds of causal jitter to apply around a scenario event."""

    minimum: float
    maximum: float


@dataclass(frozen=True)
class RecoveryProfile:
    """Ordered recovery phases inherited from V_01 scenario design."""

    phases: tuple[int, ...]
