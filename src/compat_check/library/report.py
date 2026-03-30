"""Generate compatibility reports from library build results."""
from collections import defaultdict
from datetime import datetime

_STD_ORDER = ["c++11", "c++14", "c++17", "c++20", "c++23", "c++26"]

def generate_markdown_report(library: dict, results: list[dict]) -> str:
    name = library["name"]
    version = library["version"]
    lines = [
        f"# Library Compatibility Report: {name} v{version}",
        "", f"Generated: {datetime.now().strftime('%Y-%m-%d')}", "",
    ]
    summary = _build_summary(results)
    platforms = sorted(summary.keys())
    examples = sorted({r["example"] for r in results})

    # Summary table
    lines.append("## Summary")
    lines.append("")
    lines.append("| Platform | Min Standard | Examples |")
    lines.append("|----------|-------------|----------|")
    for plat in platforms:
        s = summary[plat]
        min_std = s["min_standard"] or "\u2014"
        lines.append(f"| {plat} | {min_std} | {s['passing']}/{s['total']} |")
    lines.append("")

    # Detail table
    plat_stds = []
    for plat in platforms:
        stds = sorted(
            {r["standard"] for r in results if r["platform"] == plat},
            key=lambda s: _STD_ORDER.index(s) if s in _STD_ORDER else 99,
        )
        for std in stds:
            plat_stds.append((plat, std))

    lines.append("## Detail")
    lines.append("")
    header = "| Example | " + " | ".join(f"{p} {s}" for p, s in plat_stds) + " |"
    sep = "|---------|" + "|".join("-" * (len(f"{p} {s}") + 2) for p, s in plat_stds) + "|"
    lines.append(header)
    lines.append(sep)

    by_key = {(r["platform"], r["standard"], r["example"]): r for r in results}
    for ex in examples:
        cells = []
        for plat, std in plat_stds:
            r = by_key.get((plat, std, ex))
            cells.append("PASS" if r and r["pass"] else "FAIL")
        lines.append(f"| {ex} | " + " | ".join(cells) + " |")
    lines.append("")

    # Failures
    failures = [r for r in results if not r["pass"] and r.get("error")]
    if failures:
        lines.append("## Failures")
        lines.append("")
        for r in failures:
            lines.append(f"### {r['platform']} {r['standard']}: {r['example']}")
            lines.append("```")
            error = r["error"]
            error_lines = [l for l in error.splitlines() if "error:" in l.lower()]
            if error_lines:
                lines.append(error_lines[0].strip())
            else:
                lines.append(error.strip()[:200])
            lines.append("```")
            lines.append("")
    return "\n".join(lines)

def generate_json_report(library: dict, results: list[dict]) -> dict:
    summary = _build_summary(results)
    return {
        "library": library,
        "generated": datetime.now().isoformat(),
        "platforms": sorted({r["platform"] for r in results}),
        "examples": sorted({r["example"] for r in results}),
        "results": results,
        "summary": summary,
    }

def _build_summary(results: list[dict]) -> dict:
    by_platform = defaultdict(list)
    for r in results:
        by_platform[r["platform"]].append(r)
    summary = {}
    for plat, plat_results in by_platform.items():
        examples = {r["example"] for r in plat_results}
        total = len(examples)
        stds = sorted(
            {r["standard"] for r in plat_results},
            key=lambda s: _STD_ORDER.index(s) if s in _STD_ORDER else 99,
        )
        min_standard = None
        best_passing = 0
        for std in stds:
            std_results = [r for r in plat_results if r["standard"] == std]
            passing = sum(1 for r in std_results if r["pass"])
            if passing > best_passing:
                best_passing = passing
            if passing == total and min_standard is None:
                min_standard = std
        summary[plat] = {
            "min_standard": min_standard,
            "passing": best_passing,
            "total": total,
        }
    return summary
