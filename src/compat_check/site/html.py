"""Generate static HTML site from results."""

import re
from collections import defaultdict
from pathlib import Path

import yaml
from jinja2 import Environment, PackageLoader

from compat_check.tentpoles import (
    Tentpole, evaluate, load_tentpoles, roll_up,
)


_PASSING = {"supported", "unreported", "macro_only_yes"}

_RECIPE_SUFFIX = "+recipe"
_POLYFILL_LABEL = "+polyfill"


def _resolve_meta(slug: str, platform_meta: dict):
    """Resolve meta for a slug that may have the '+recipe' suffix.

    Returns (base_slug, meta_or_None, display_suffix). For a recipe slug,
    meta is looked up under the base slug and display_suffix is ' +polyfill'.
    """
    if slug.endswith(_RECIPE_SUFFIX):
        base = slug[:-len(_RECIPE_SUFFIX)]
        return base, platform_meta.get(base), f" {_POLYFILL_LABEL}"
    return slug, platform_meta.get(slug), ""


def _support_pct(statuses: list[str]) -> int:
    """Calculate % of features that compile successfully."""
    if not statuses:
        return 0
    pass_count = sum(1 for s in statuses if s in _PASSING)
    return round(100 * pass_count / len(statuses))


def _support_level(statuses: list[str]) -> str:
    if not statuses:
        return "\u2014"
    pass_count = sum(1 for s in statuses if s in _PASSING)
    if pass_count == len(statuses):
        return "full"
    if pass_count == 0:
        return "none"
    return "partial"


def _build_macro_links(catalog_path: Path) -> dict[str, str]:
    """Build macro name → cppreference URL from catalog descriptions."""
    if not catalog_path.exists():
        return {}
    data = yaml.safe_load(catalog_path.read_text())
    # Well-known macros without wiki links in the catalog
    _KNOWN = {
        "__cpp_concepts": "language/constraints",
        "__cpp_fold_expressions": "language/fold",
        "__cpp_deduction_guides": "language/class_template_argument_deduction",
        "__cpp_exceptions": "language/exceptions",
        "__cpp_rtti": "language/typeid",
        "__cpp_impl_three_way_comparison": "language/operator_comparison#Three-way_comparison",
        "__cpp_impl_reflection": "language/reflection",
        "__cpp_pp_embed": "preprocessor/embed",
        "__cpp_contracts": "language/attributes/contract",
        "__cpp_constexpr_dynamic_alloc": "language/constexpr",
        "__has_cpp_attribute(nodiscard)": "language/attributes/nodiscard",
        "__has_cpp_attribute(deprecated)": "language/attributes/deprecated",
        "__has_cpp_attribute(fallthrough)": "language/attributes/fallthrough",
        "__has_cpp_attribute(maybe_unused)": "language/attributes/maybe_unused",
        "__has_cpp_attribute(likely)": "language/attributes/likely",
        "__has_cpp_attribute(unlikely)": "language/attributes/likely",
        "__has_cpp_attribute(no_unique_address)": "language/attributes/no_unique_address",
        "__has_cpp_attribute(noreturn)": "language/attributes/noreturn",
        "__has_cpp_attribute(carries_dependency)": "language/attributes/carries_dependency",
        "__has_cpp_attribute(assume)": "language/attributes/assume",
        "__has_cpp_attribute(indeterminate)": "language/attributes/indeterminate",
    }
    links: dict[str, str] = {}
    base = "https://en.cppreference.com/w/cpp/"
    links.update({k: base + v for k, v in _KNOWN.items()})
    for section in ["language", "library", "attributes"]:
        for entry in data.get(section, []):
            name = entry["name"]
            if section == "attributes":
                name = f"__has_cpp_attribute({name})"
            rows = entry.get("rows", [])
            desc = rows[0].get("cppreference-description", "") if rows else ""
            # [[cpp/path|text]] wiki links — best quality
            m = re.search(r"\[\[cpp/([^\]|]+)", desc)
            if m:
                links[name] = base + m.group(1).replace(" ", "_")
                continue
            # {{ltt|cpp/path/name|text}} template links with explicit path
            m = re.search(r"\{\{ltt?\|cpp/([^|}]+)", desc)
            if m:
                links[name] = base + m.group(1).replace(" ", "_")
                continue
            # Fallback for library features: link to the header reference page
            headers = entry.get("header_list", "").split()
            if headers and section == "library":
                links[name] = base + "header/" + headers[0]
    return links


def generate_site(results: list[dict], output_dir: Path, platform_meta=None,
                  catalog_path: Path | None = None,
                  tiers_path: Path | None = None) -> None:
    """Generate a static HTML site from result dicts."""
    platform_meta = platform_meta or {}
    macro_links = _build_macro_links(catalog_path) if catalog_path else {}
    tentpoles_by_std: dict[str, list[Tentpole]] = {}
    if tiers_path is not None:
        tentpoles_by_std = load_tentpoles(tiers_path)
    env = Environment(loader=PackageLoader("compat_check.site", "templates"))

    # Group results
    by_platform = defaultdict(list)
    by_platform_std = defaultdict(lambda: defaultdict(list))
    by_platform_std_results: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for r in results:
        by_platform[r["platform"]].append(r)
        by_platform_std[r["platform"]][r["standard"]].append(r["status"])
        by_platform_std_results[r["platform"]][r["standard"]].append(r)

    all_standards = sorted(
        {r["standard"] for r in results},
        key=lambda s: int(s.replace("c++", ""))
    )

    # Build matrix with percentages
    matrix = {}
    for plat, stds in by_platform_std.items():
        matrix[plat] = {}
        for std in all_standards:
            statuses_list = stds.get(std, [])
            cell = {
                "level": _support_level(statuses_list),
                "pct": _support_pct(statuses_list),
                "total": len(statuses_list),
                "pass": sum(1 for s in statuses_list if s in _PASSING),
            }
            tps = tentpoles_by_std.get(std, [])
            if tps and statuses_list:
                plat_std_results = by_platform_std_results[plat].get(std, [])
                tp_statuses = evaluate(plat_std_results, tps)
                counts = roll_up(tp_statuses)
                cell["tentpoles_pass"] = counts["complete"] + counts["good"]
                cell["tentpoles_total"] = len(tp_statuses)
            else:
                cell["tentpoles_pass"] = None
                cell["tentpoles_total"] = None
            matrix[plat][std] = cell

    # Effective support: best % across all standards
    effective = {}
    for plat in matrix:
        pcts = [v["pct"] for v in matrix[plat].values() if v["total"] > 0]
        effective[plat] = max(pcts) if pcts else 0

    platforms = []
    for slug in sorted(by_platform.keys(), key=lambda s: -effective.get(s, 0)):
        _, meta, suffix = _resolve_meta(slug, platform_meta)
        base_name = meta.name if meta else slug.replace(_RECIPE_SUFFIX, "")
        platforms.append({
            "slug": slug,
            "name": f"{base_name}{suffix}",
            "board_family": meta.board_family if meta else "",
            "architecture": meta.architecture if meta else "",
            "effective_pct": effective.get(slug, 0),
        })

    # Index page
    output_dir.mkdir(parents=True, exist_ok=True)
    index_tmpl = env.get_template("index.html")
    (output_dir / "index.html").write_text(
        index_tmpl.render(standards=all_standards, platforms=platforms, matrix=matrix)
    )

    # Per-platform per-std tentpole statuses for platform pages
    platform_tentpole_statuses: dict[str, dict[str, list]] = {}
    for slug, items in by_platform.items():
        platform_tentpole_statuses[slug] = {}
        for std in all_standards:
            tps = tentpoles_by_std.get(std, [])
            if not tps:
                continue
            plat_std_results = by_platform_std_results[slug].get(std, [])
            if plat_std_results:
                platform_tentpole_statuses[slug][std] = evaluate(plat_std_results, tps)

    # Platform pages
    platform_tmpl = env.get_template("platform.html")
    for slug, items in by_platform.items():
        plat_dir = output_dir / slug
        plat_dir.mkdir(exist_ok=True)

        by_std = defaultdict(lambda: defaultdict(list))
        for r in items:
            cat = r.get("category", "unknown")
            by_std[r["standard"]][cat].append(type("R", (), r))

        _, meta, suffix = _resolve_meta(slug, platform_meta)
        version = items[0].get("platform_version", "") if items else ""
        stds_sorted = sorted(
            by_std.keys(), key=lambda s: int(s.replace("c++", ""))
        )

        # Per-standard stats
        std_stats = {}
        for std in stds_sorted:
            all_in_std = by_platform_std[slug].get(std, [])
            std_stats[std] = {
                "pct": _support_pct(all_in_std),
                "pass": sum(1 for s in all_in_std if s in _PASSING),
                "total": len(all_in_std),
            }

        base_name = meta.name if meta else slug.replace(_RECIPE_SUFFIX, "")
        (plat_dir / "index.html").write_text(
            platform_tmpl.render(
                platform_name=f"{base_name}{suffix}",
                platform_slug=slug,
                platform_version=version,
                board_family=meta.board_family if meta else "",
                architecture=meta.architecture if meta else "",
                standards=stds_sorted,
                by_standard={std: dict(sorted(by_std[std].items())) for std in stds_sorted},
                std_stats=std_stats,
                macro_links=macro_links,
                tentpole_statuses=platform_tentpole_statuses.get(slug, {}),
            )
        )
