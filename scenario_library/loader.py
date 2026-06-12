"""Load scenario YAML definitions.

Implementation note: YAML parsing will use the project-approved dependency once
runtime dependencies are introduced. This module exists now as the stable import
surface for PRE-HOC and AD-HOC code.
"""

from __future__ import annotations

from pathlib import Path


SCENARIOS_ROOT = Path(__file__).resolve().parents[1] / "configs" / "scenarios"


def scenario_path(scenario_name: str) -> Path:
    """Return the path for a versioned scenario configuration."""

    return SCENARIOS_ROOT / scenario_name
