"""Generate README summary table from results."""

from collections import defaultdict
from datetime import date
from pathlib import Path

from compat_check.tentpoles import (
    Tentpole, evaluate, headline_std, load_tentpoles, roll_up,
)


_PASSING = {"supported", "unreported", "macro_only_yes"}

_STD_ORDER = ["c++11", "c++14", "c++17", "c++20", "c++23", "c++26"]

_RECIPE_SUFFIX = "+recipe"
_POLYFILL_LABEL = "+polyfill"


def _effective_pct(statuses: list[str]) -> int:
    """Calculate % of features that compile successfully."""
    if not statuses:
        return 0
    pass_count = sum(1 for s in statuses if s in _PASSING)
    return round(100 * pass_count / len(statuses))


def _std_label(std: str) -> str:
    return std.replace("c++", "C++")


def _pct_emoji(pct: int) -> str:
    """Color-code a percentage with the same thresholds as the HTML site."""
    if pct >= 90:
        return "🟢"
    if pct >= 50:
        return "🟡"
    return "🔴"


def _peak(stds: dict[str, list[str]]) -> tuple[str, int]:
    """Return (peak_standard, peak_pct). On ties, prefer the highest standard."""
    ordered = sorted(stds.keys(), key=lambda s: _STD_ORDER.index(s) if s in _STD_ORDER else 99)
    best_std, best_pct = ordered[0], _effective_pct(stds[ordered[0]])
    for s in ordered[1:]:
        pct = _effective_pct(stds[s])
        if pct >= best_pct:
            best_std, best_pct = s, pct
    return best_std, best_pct


def _format_tentpole_rollup(std: str, counts: dict[str, int],
                            link_base: str = "") -> str:
    """Format like 'C++17: 4✅ 1🟡 3❌' — omits zero-count buckets.

    Collapses complete+good into ✅ so README cells stay skimmable.
    When link_base is given, the std label is wrapped in a markdown link
    pointing at '{link_base}#{std}' so readers can jump to that std's
    tentpole detail on the platform page.
    """
    parts = []
    passing = counts["complete"] + counts["good"]
    if passing:
        parts.append(f"{passing}✅")
    if counts["partial"]:
        parts.append(f"{counts['partial']}🟡")
    if counts["unsupported"]:
        parts.append(f"{counts['unsupported']}❌")
    body = " ".join(parts) if parts else "—"
    label = _std_label(std)
    if link_base:
        label = f"[{label}]({link_base}#{std})"
    return f"{label}: {body}"


def _usable_cell(platform_results: list[dict],
                 tentpoles_by_std: dict[str, list[Tentpole]],
                 slug: str = "",
                 site_url: str = "") -> str:
    """Build the 'Usable C++' cell for one platform.

    Returns 'Headline (bold) · NextStd (preview)' or '—' if no tentpoles apply.
    When both site_url and slug are given, each std prefix links to that
    std's section on the platform page.
    """
    by_std: dict[str, list[dict]] = defaultdict(list)
    for r in platform_results:
        by_std[r["standard"]].append(r)

    rollups: dict[str, dict[str, int]] = {}
    for std, tentpoles in tentpoles_by_std.items():
        if not tentpoles or std not in by_std:
            continue
        statuses = evaluate(by_std[std], tentpoles)
        rollups[std] = roll_up(statuses)

    if not rollups:
        return "—"

    link_base = f"{site_url}/{slug}/index.html" if site_url and slug else ""

    head = headline_std(rollups)
    parts = [f"**{_format_tentpole_rollup(head, rollups[head], link_base)}**"]
    ordered = sorted(
        rollups.keys(),
        key=lambda s: _STD_ORDER.index(s) if s in _STD_ORDER else 99,
    )
    head_idx = ordered.index(head)
    if head_idx + 1 < len(ordered):
        nxt = ordered[head_idx + 1]
        parts.append(_format_tentpole_rollup(nxt, rollups[nxt], link_base))
    return " · ".join(parts)


def _std_range(std_list: list[str]) -> str:
    if len(std_list) == 1:
        return _std_label(std_list[0])
    return f"{_std_label(std_list[0])}–{_std_label(std_list[-1])}"


def generate_summary_table(results: list[dict], platform_meta=None,
                           site_url: str = "",
                           tiers_path: Path | None = None) -> str:
    """Generate a markdown summary table from result dicts.

    Args:
        results: list of result dicts from the sweep
        platform_meta: dict mapping slug → Platform for names/board info
        site_url: base URL for platform report links (e.g. "https://example.github.io/repo")
        tiers_path: optional path to catalog/tiers.yaml. When provided, adds a
            'Usable C++' column with per-std tentpole rollups.

    Platforms with a recipe applied are stored under slug "{base}+recipe" and
    render as a second row labeled "{name} +polyfill", grouped immediately after
    the baseline row for the same platform.
    """
    platform_meta = platform_meta or {}

    tentpoles_by_std: dict[str, list[Tentpole]] = {}
    if tiers_path is not None:
        tentpoles_by_std = load_tentpoles(tiers_path)

    grouped: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    results_by_platform: dict[str, list[dict]] = defaultdict(list)
    for r in results:
        grouped[r["platform"]][r["standard"]].append(r["status"])
        results_by_platform[r["platform"]].append(r)

    rows = []
    baseline_peak_by_base: dict[str, int] = {}

    for slug, stds in grouped.items():
        is_recipe = slug.endswith(_RECIPE_SUFFIX)
        base_slug = slug[:-len(_RECIPE_SUFFIX)] if is_recipe else slug
        meta = platform_meta.get(base_slug)
        name = meta.name if meta else base_slug
        board = meta.board_family if meta else ""

        std_list = sorted(stds.keys(), key=lambda s: _STD_ORDER.index(s) if s in _STD_ORDER else 99)
        std_range = _std_range(std_list)

        peak_std, peak_pct = _peak(stds)

        display_name = f"{name} {_POLYFILL_LABEL}" if is_recipe else name
        if site_url:
            linked_name = f"[{display_name}]({site_url}/{slug}/index.html)"
        else:
            linked_name = display_name

        pct_cell = f"{_pct_emoji(peak_pct)} **{_std_label(peak_std)} / {peak_pct}%**"

        usable = _usable_cell(
            results_by_platform.get(slug, []),
            tentpoles_by_std,
            slug=slug,
            site_url=site_url,
        ) if tentpoles_by_std else ""

        rows.append({
            "base_slug": base_slug,
            "is_recipe": is_recipe,
            "peak_pct": peak_pct,
            "name": linked_name,
            "board": board,
            "std_range": std_range,
            "pct_cell": pct_cell,
            "usable": usable,
        })
        if not is_recipe:
            baseline_peak_by_base[base_slug] = peak_pct

    # Sort: group each platform's rows together (baseline above recipe),
    # ordering platforms by baseline peak pct desc. Recipe-only platforms
    # sort by their own peak.
    def _sort_key(row):
        group_pct = baseline_peak_by_base.get(row["base_slug"], row["peak_pct"])
        return (-group_pct, row["base_slug"], row["is_recipe"])

    rows.sort(key=_sort_key)

    # Aggregates — baseline rows only (recipes are opt-in)
    baseline_rows = [r for r in rows if not r["is_recipe"]]
    num_platforms = len(baseline_rows)
    best_pcts = [r["peak_pct"] for r in baseline_rows]
    pct_range = f"{min(best_pcts)}%–{max(best_pcts)}%" if best_pcts else "N/A"

    # Highest standard tested on ALL baseline platforms
    std_platform_count = defaultdict(int)
    for slug, stds in grouped.items():
        if slug.endswith(_RECIPE_SUFFIX):
            continue
        for s in stds:
            std_platform_count[s] += 1
    universal_stds = [s for s in _STD_ORDER if std_platform_count.get(s, 0) == num_platforms]
    highest_universal = universal_stds[-1] if universal_stds else "N/A"

    min_effective = min(best_pcts) if best_pcts else 0
    threshold = (min_effective // 10) * 10

    lines = []
    highest_universal_label = _std_label(highest_universal) if highest_universal != "N/A" else "N/A"
    lines.append(f"*{num_platforms} platforms, all support {highest_universal_label} "
                 f"above {threshold}% compatibility. "
                 f"Effective support: {pct_range}. "
                 f"Updated {date.today().isoformat()}.*")
    if site_url:
        lines.append(f"[Full report]({site_url}/index.html) with per-feature details.")
    lines.append("")

    header_cells = ["Platform", "Board", "Standards", "Effective Support"]
    sep_cells = ["----------", "-------", "-----------", "-------------------"]
    if tentpoles_by_std:
        header_cells.append("Usable C++")
        sep_cells.append("-----------")
    lines.append("| " + " | ".join(header_cells) + " |")
    lines.append("|" + "|".join(sep_cells) + "|")

    for row in rows:
        cells = [row["name"], row["board"], row["std_range"], row["pct_cell"]]
        if tentpoles_by_std:
            cells.append(row["usable"])
        lines.append("| " + " | ".join(cells) + " |")

    return "\n".join(lines) + "\n"
