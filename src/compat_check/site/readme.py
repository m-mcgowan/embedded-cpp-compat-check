"""Generate README summary table from results."""

from collections import defaultdict
from datetime import date


_PASSING = {"supported", "unreported", "macro_only_yes"}

_STD_ORDER = ["c++11", "c++14", "c++17", "c++20", "c++23", "c++26"]


def _effective_pct(statuses: list[str]) -> int:
    """Calculate % of features that compile successfully."""
    if not statuses:
        return 0
    pass_count = sum(1 for s in statuses if s in _PASSING)
    return round(100 * pass_count / len(statuses))


def generate_summary_table(results: list[dict], platform_meta=None,
                           site_url: str = "") -> str:
    """Generate a markdown summary table from result dicts.

    Args:
        results: list of result dicts from the sweep
        platform_meta: dict mapping slug → Platform for names/board info
        site_url: base URL for platform report links (e.g. "https://example.github.io/repo")
    """
    platform_meta = platform_meta or {}

    # Group by platform → standard → statuses
    grouped: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    for r in results:
        grouped[r["platform"]][r["standard"]].append(r["status"])

    # Compute per-platform stats
    rows = []
    all_stds = set()
    total_features = 0
    total_passing = 0

    for slug, stds in grouped.items():
        meta = platform_meta.get(slug)
        name = meta.name if meta else slug
        board = meta.board_family if meta else ""

        std_list = sorted(stds.keys(), key=lambda s: _STD_ORDER.index(s) if s in _STD_ORDER else 99)
        all_stds.update(std_list)
        if len(std_list) == 1:
            std_range = std_list[0]
        else:
            lo = std_list[0].replace("c++", "")
            hi = std_list[-1].replace("c++", "")
            std_range = f"c++{lo}\u2013c++{hi}"

        best_pct = max(_effective_pct(stds[s]) for s in stds)
        plat_total = sum(len(stds[s]) for s in stds)
        plat_pass = sum(
            sum(1 for st in stds[s] if st in _PASSING)
            for s in stds
        )
        total_features += plat_total
        total_passing += plat_pass

        # Link platform name to its report page
        if site_url:
            linked_name = f"[{name}]({site_url}/{slug}/index.html)"
        else:
            linked_name = name

        rows.append((best_pct, linked_name, board, std_range, f"**{best_pct}%**", slug))

    rows.sort(key=lambda r: -r[0])

    # Aggregates
    num_platforms = len(grouped)
    best_pcts = [r[0] for r in rows]
    pct_range = f"{min(best_pcts)}%\u2013{max(best_pcts)}%" if best_pcts else "N/A"

    # Highest standard tested on ALL platforms
    std_platform_count = defaultdict(int)
    for slug, stds in grouped.items():
        for s in stds:
            std_platform_count[s] += 1
    universal_stds = [s for s in _STD_ORDER if std_platform_count.get(s, 0) == num_platforms]
    highest_universal = universal_stds[-1] if universal_stds else "N/A"

    # Round min effective support down to nearest 10 for a clean threshold
    min_effective = min(best_pcts) if best_pcts else 0
    threshold = (min_effective // 10) * 10

    # Build output
    lines = []
    lines.append(f"*{num_platforms} platforms, all support {highest_universal} "
                 f"above {threshold}% compatibility. "
                 f"Effective support: {pct_range}. "
                 f"Updated {date.today().isoformat()}.*")
    if site_url:
        lines.append(f"[Full report]({site_url}/index.html) with per-feature details.")
    lines.append("")

    header = "| Platform | Board | Standards | Effective Support |"
    sep = "|----------|-------|-----------|-------------------|"
    lines.extend([header, sep])
    for _, name, board, std_range, pct, slug in rows:
        lines.append(f"| {name} | {board} | {std_range} | {pct} |")

    return "\n".join(lines) + "\n"
