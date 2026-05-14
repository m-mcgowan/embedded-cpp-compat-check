"""Curated tentpole features for per-standard usability scoring.

A tentpole is a high-impact, developer-recognizable feature (e.g. Ranges,
Format, Coroutines) that may map to one or more SD-6 feature-test macros.
Each tentpole's macros are split into `required` (must all pass for the
feature to work at all) and `optional` (extensions/variants).

Status derivation per tentpole:
- complete:    all required pass AND all optional pass (or no optional defined)
- good:        all required pass AND >=75% of optional pass
- partial:     all required pass AND <75% of optional pass
- unsupported: any required macro fails
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import yaml

Level = Literal["complete", "good", "partial", "unsupported"]

_PASSING = frozenset({"supported", "unreported", "macro_only_yes"})


@dataclass(frozen=True)
class Tentpole:
    """A curated tentpole feature."""
    id: str
    name: str
    required: tuple[str, ...]
    optional: tuple[str, ...]


@dataclass(frozen=True)
class TentpoleStatus:
    """Evaluation result for a tentpole on a single (platform, std)."""
    id: str
    name: str
    level: Level
    required_pass: int
    required_total: int
    optional_pass: int
    optional_total: int
    failed_required: tuple[str, ...]


def load_tentpoles(path: Path) -> dict[str, list[Tentpole]]:
    """Load catalog/tiers.yaml. Returns {std: [Tentpole, ...]}.

    YAML top-level keys like 'cpp17' are normalized to 'c++17' to match
    the standard format used elsewhere in results.
    """
    data = yaml.safe_load(path.read_text()) or {}
    result: dict[str, list[Tentpole]] = {}
    for std_key, std_data in data.items():
        normalized = std_key.replace("cpp", "c++")
        tentpoles: list[Tentpole] = []
        for entry in (std_data or {}).get("tentpoles", []):
            tentpoles.append(Tentpole(
                id=entry["id"],
                name=entry["name"],
                required=tuple(entry.get("required", [])),
                optional=tuple(entry.get("optional", [])),
            ))
        result[normalized] = tentpoles
    return result


def evaluate(results: list[dict], tentpoles: list[Tentpole]) -> list[TentpoleStatus]:
    """Evaluate tentpoles against per-feature results (one platform, one std)."""
    raise NotImplementedError  # Task 2


def roll_up(statuses: list[TentpoleStatus]) -> dict[Level, int]:
    """Count statuses by level."""
    raise NotImplementedError  # Task 3


def headline_std(rollups: dict[str, dict[Level, int]]) -> str | None:
    """Pick the std with the most 'complete' tentpoles. Ties → highest std."""
    raise NotImplementedError  # Task 3
