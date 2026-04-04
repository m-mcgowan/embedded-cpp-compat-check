"""Generate README summary table from results."""

from collections import defaultdict


_PASSING = {"supported", "unreported", "macro_only_yes"}


def _effective_pct(statuses: list[str]) -> int:
    """Calculate % of features that compile successfully."""
    if not statuses:
        return 0
    pass_count = sum(1 for s in statuses if s in _PASSING)
    return round(100 * pass_count / len(statuses))


def generate_summary_table(results: list[dict], platform_meta=None) -> str:
    """Generate a markdown summary table from result dicts.

    Table shows platform name, board family, supported standards, and effective
    support % (best across all standards).
    """
    platform_meta = platform_meta or {}

    # Group by platform → standard → statuses
    grouped: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    for r in results:
        grouped[r["platform"]][r["standard"]].append(r["status"])

    # Build rows: (effective_pct, name, board, standards_range, pct_str)
    rows = []
    for slug, stds in grouped.items():
        meta = platform_meta.get(slug)
        name = meta.name if meta else slug
        board = meta.board_family if meta else ""

        std_list = sorted(stds.keys(), key=lambda s: int(s.replace("c++", "")))
        if len(std_list) == 1:
            std_range = std_list[0].replace("c++", "c++")
        else:
            lo = std_list[0].replace("c++", "")
            hi = std_list[-1].replace("c++", "")
            std_range = f"c++{lo}\u2013c++{hi}"

        # Best % across standards
        best_pct = max(_effective_pct(stds[s]) for s in stds)

        rows.append((best_pct, name, board, std_range, f"**{best_pct}%**"))

    # Sort by effective support descending
    rows.sort(key=lambda r: -r[0])

    header = "| Platform | Board | Standards | Effective Support |"
    sep = "|----------|-------|-----------|-------------------|"

    lines = [header, sep]
    for _, name, board, std_range, pct in rows:
        lines.append(f"| {name} | {board} | {std_range} | {pct} |")

    return "\n".join(lines) + "\n"
