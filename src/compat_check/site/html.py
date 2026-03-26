"""Generate static HTML site from results."""

from collections import defaultdict
from pathlib import Path

from jinja2 import Environment, PackageLoader


def _support_level(statuses: list[str]) -> str:
    passing = {"supported", "unreported", "macro_only_yes"}
    pass_count = sum(1 for s in statuses if s in passing)
    if not statuses:
        return "\u2014"
    if pass_count == len(statuses):
        return "full"
    if pass_count == 0:
        return "none"
    return "partial"


def generate_site(results: list[dict], output_dir: Path) -> None:
    """Generate a static HTML site from result dicts."""
    env = Environment(loader=PackageLoader("compat_check.site", "templates"))

    # Group results
    by_platform = defaultdict(list)
    by_platform_std = defaultdict(lambda: defaultdict(list))
    for r in results:
        by_platform[r["platform"]].append(r)
        by_platform_std[r["platform"]][r["standard"]].append(r["status"])

    all_standards = sorted(
        {r["standard"] for r in results},
        key=lambda s: int(s.replace("c++", ""))
    )

    # Build matrix
    matrix = {}
    for plat, stds in by_platform_std.items():
        matrix[plat] = {}
        for std in all_standards:
            matrix[plat][std] = _support_level(stds.get(std, []))

    platforms = [
        {"slug": slug, "name": slug}
        for slug in sorted(by_platform.keys())
    ]

    # Index page
    output_dir.mkdir(parents=True, exist_ok=True)
    index_tmpl = env.get_template("index.html")
    (output_dir / "index.html").write_text(
        index_tmpl.render(standards=all_standards, platforms=platforms, matrix=matrix)
    )

    # Platform pages
    platform_tmpl = env.get_template("platform.html")
    for slug, items in by_platform.items():
        plat_dir = output_dir / slug
        plat_dir.mkdir(exist_ok=True)

        by_std = defaultdict(list)
        for r in items:
            by_std[r["standard"]].append(type("R", (), r))

        version = items[0].get("platform_version", "") if items else ""
        (plat_dir / "index.html").write_text(
            platform_tmpl.render(
                platform_name=slug,
                platform_version=version,
                by_standard=dict(sorted(by_std.items())),
            )
        )
