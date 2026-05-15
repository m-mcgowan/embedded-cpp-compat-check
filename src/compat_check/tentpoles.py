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

_STD_ORDER = ("c++11", "c++14", "c++17", "c++20", "c++23", "c++26")


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
    """Evaluate tentpoles against per-feature results (one platform, one std).

    Results list elements should have 'macro' and 'status' keys. A macro
    absent from results is treated as failing.
    """
    by_macro = {r.get("macro"): r.get("status") for r in results if r.get("macro")}
    statuses: list[TentpoleStatus] = []
    for tp in tentpoles:
        required_pass = sum(1 for m in tp.required if by_macro.get(m) in _PASSING)
        optional_pass = sum(1 for m in tp.optional if by_macro.get(m) in _PASSING)
        required_total = len(tp.required)
        optional_total = len(tp.optional)
        failed_required = tuple(
            m for m in tp.required if by_macro.get(m) not in _PASSING
        )

        if required_pass < required_total:
            level: Level = "unsupported"
        elif optional_total == 0 or optional_pass == optional_total:
            level = "complete"
        elif optional_pass / optional_total >= 0.75:
            level = "good"
        else:
            level = "partial"

        statuses.append(TentpoleStatus(
            id=tp.id,
            name=tp.name,
            level=level,
            required_pass=required_pass,
            required_total=required_total,
            optional_pass=optional_pass,
            optional_total=optional_total,
            failed_required=failed_required,
        ))
    return statuses


def roll_up(statuses: list[TentpoleStatus]) -> dict[Level, int]:
    """Count statuses by level. Always includes all four keys with zeros."""
    counts: dict[Level, int] = {
        "complete": 0, "good": 0, "partial": 0, "unsupported": 0,
    }
    for s in statuses:
        counts[s.level] += 1
    return counts


def headline_std(rollups: dict[str, dict[Level, int]]) -> str | None:
    """Pick the std with the most 'complete' tentpoles. Ties → higher std.

    Secondary criterion (used when no std has any complete tentpoles):
    pick the std with the most non-unsupported tentpoles (complete + good
    + partial). Higher std still wins on a final tie.
    """
    if not rollups:
        return None

    def _key(std: str) -> tuple[int, int, int]:
        r = rollups[std]
        complete = r["complete"]
        non_unsupp = r["complete"] + r["good"] + r["partial"]
        std_idx = _STD_ORDER.index(std) if std in _STD_ORDER else 99
        return (complete, non_unsupp, std_idx)

    return max(rollups.keys(), key=_key)
