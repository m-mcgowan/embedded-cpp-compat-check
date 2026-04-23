"""Generate compatibility reports from library build results."""
from collections import defaultdict
from datetime import datetime

_STD_ORDER = ["c++11", "c++14", "c++17", "c++20", "c++23", "c++26"]


def _extract_error_reason(error: str) -> str:
    """Extract a short human-readable reason from a compiler error."""
    if not error:
        return ""
    # Find the first error: line
    for line in error.splitlines():
        if "error:" in line.lower():
            # Extract just the error message after "error:"
            parts = line.split("error:", 1)
            if len(parts) > 1:
                msg = parts[1].strip()
                # Clean up common patterns
                if "No such file or directory" in msg:
                    # Extract the missing header
                    header = msg.split(":")[0].strip()
                    return f"missing header: {header}"
                if "is not a member of" in msg:
                    return msg[:80]
                if "has not been declared" in msg:
                    return msg[:80]
                if "was not declared" in msg:
                    return msg[:80]
                return msg[:80]
    return error.splitlines()[0][:80] if error.strip() else ""


def _classify_platform_failure(plat_results: list[dict]) -> str:
    """Summarize why a platform fails from its error outputs."""
    errors = [r.get("error", "") for r in plat_results if not r["pass"] and r.get("error")]
    if not errors:
        return ""

    # Check for common patterns across all failures
    reasons = [_extract_error_reason(e) for e in errors]
    # If all failures have the same reason, report it once
    unique = set(r for r in reasons if r)
    if len(unique) == 1:
        return unique.pop()
    # If most failures are missing headers, summarize
    missing_headers = [r for r in reasons if r.startswith("missing header:")]
    if len(missing_headers) == len(reasons):
        headers = sorted(set(r.replace("missing header: ", "") for r in missing_headers))
        if len(headers) <= 3:
            return f"missing headers: {', '.join(headers)}"
        return f"missing {len(headers)} standard library headers"
    # Otherwise return the first reason
    return reasons[0] if reasons else ""


def generate_markdown_report(library: dict, results: list[dict], pretty: bool = False) -> str:
    pass_cell = "✅" if pretty else "PASS"
    fail_cell = "❌" if pretty else "FAIL"
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
    lines.append("| Platform | Min Standard | Examples | Notes |")
    lines.append("|----------|-------------|----------|-------|")
    for plat in platforms:
        s = summary[plat]
        min_std = s["min_standard"] or "\u2014"
        notes = s.get("failure_reason", "")
        if s["passing"] == s["total"]:
            notes = ""  # All passing, no notes needed
        lines.append(f"| {plat} | {min_std} | {s['passing']}/{s['total']} | {notes} |")
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
            cells.append(pass_cell if r and r["pass"] else fail_cell)
        lines.append(f"| {ex} | " + " | ".join(cells) + " |")
    lines.append("")

    # Failures with context
    failures = [r for r in results if not r["pass"] and r.get("error")]
    if failures:
        lines.append("## Failure Details")
        lines.append("")
        for r in failures:
            reason = _extract_error_reason(r["error"])
            lines.append(f"**{r['platform']} {r['standard']}: {r['example']}** — {reason}")
            lines.append("")
            lines.append("```")
            error = r["error"]
            error_lines = [l for l in error.splitlines() if "error:" in l.lower()]
            if error_lines:
                for el in error_lines[:3]:  # Show up to 3 error lines
                    lines.append(el.strip())
            else:
                lines.append(error.strip()[:300])
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

        # Determine failure reason for platforms that don't fully pass
        failure_reason = ""
        if best_passing < total:
            failure_reason = _classify_platform_failure(plat_results)

        summary[plat] = {
            "min_standard": min_standard,
            "passing": best_passing,
            "total": total,
            "failure_reason": failure_reason,
        }
    return summary
