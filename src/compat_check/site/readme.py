"""Generate README summary table from results."""

from collections import defaultdict


def _support_level(statuses: list[str]) -> str:
    """Classify overall support for a platform/standard combo."""
    if not statuses:
        return "\u2014"
    passing = {"supported", "unreported", "macro_only_yes"}
    pass_count = sum(1 for s in statuses if s in passing)
    if pass_count == len(statuses):
        return "full"
    if pass_count == 0:
        return "\u2014"
    return "partial"


def generate_summary_table(results: list[dict]) -> str:
    """Generate a markdown summary table from result dicts."""
    grouped: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    for r in results:
        grouped[r["platform"]][r["standard"]].append(r["status"])

    all_standards = sorted(
        {r["standard"] for r in results},
        key=lambda s: int(s.replace("c++", ""))
    )
    all_platforms = sorted(grouped.keys())

    header = "| Platform | " + " | ".join(all_standards) + " |"
    sep = "|---|" + "|".join(["---"] * len(all_standards)) + "|"

    rows = []
    for platform in all_platforms:
        cells = []
        for std in all_standards:
            statuses = grouped[platform].get(std, [])
            cells.append(_support_level(statuses))
        rows.append(f"| {platform} | " + " | ".join(cells) + " |")

    return "\n".join([header, sep] + rows) + "\n"
