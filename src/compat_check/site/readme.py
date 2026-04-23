"""Generate README summary table from results."""

from collections import defaultdict
from datetime import date


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


def _peak(stds: dict[str, list[str]]) -> tuple[str, int]:
    """Return (peak_standard, peak_pct). On ties, prefer the highest standard."""
    ordered = sorted(stds.keys(), key=lambda s: _STD_ORDER.index(s) if s in _STD_ORDER else 99)
    best_std, best_pct = ordered[0], _effective_pct(stds[ordered[0]])
    for s in ordered[1:]:
        pct = _effective_pct(stds[s])
        if pct >= best_pct:
            best_std, best_pct = s, pct
    return best_std, best_pct


def _std_range(std_list: list[str]) -> str:
    if len(std_list) == 1:
        return _std_label(std_list[0])
    return f"{_std_label(std_list[0])}–{_std_label(std_list[-1])}"


def generate_summary_table(results: list[dict], platform_meta=None,
                           site_url: str = "") -> str:
    """Generate a markdown summary table from result dicts.

    Args:
        results: list of result dicts from the sweep
        platform_meta: dict mapping slug → Platform for names/board info
        site_url: base URL for platform report links (e.g. "https://example.github.io/repo")

    Platforms with a recipe applied are stored under slug "{base}+recipe" and
    render as a second row labeled "{name} +polyfill", grouped immediately after
    the baseline row for the same platform.
    """
    platform_meta = platform_meta or {}

    grouped: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    for r in results:
        grouped[r["platform"]][r["standard"]].append(r["status"])

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

        pct_cell = f"**{_std_label(peak_std)} / {peak_pct}%**"

        rows.append({
            "base_slug": base_slug,
            "is_recipe": is_recipe,
            "peak_pct": peak_pct,
            "name": linked_name,
            "board": board,
            "std_range": std_range,
            "pct_cell": pct_cell,
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

    header = "| Platform | Board | Standards | Effective Support |"
    sep = "|----------|-------|-----------|-------------------|"
    lines.extend([header, sep])
    for row in rows:
        lines.append(f"| {row['name']} | {row['board']} | {row['std_range']} | {row['pct_cell']} |")

    return "\n".join(lines) + "\n"
