"""CLI entry point for the compatibility checker."""

import click
from pathlib import Path


@click.group()
def main():
    """Embedded C++ Compatibility Checker."""
    pass


@main.command()
@click.option("--catalog", default="catalog/data.yaml", type=click.Path(exists=True))
@click.option("--platforms-dir", default="platforms", type=click.Path(exists=True))
@click.option("--tests-dir", default="tests", type=click.Path(exists=True))
@click.option("--results-dir", default="results", type=click.Path())
@click.option("--work-dir", default=".work", type=click.Path())
@click.option("--platform", "platform_filter", default=None, help="Run only this platform")
@click.option("--test", "test_filter", default=None, help="Run only this test")
@click.option("--parallel", default=4, type=int, help="Max parallel builds (1=serial)")
@click.option("--dry-run", is_flag=True, help="Show what would be built")
@click.option("--recipe", is_flag=True, help="Apply platform recipes (test with polyfill libraries)")
def run(catalog, platforms_dir, tests_dir, results_dir, work_dir,
        platform_filter, test_filter, parallel, dry_run, recipe):
    """Run compatibility checks."""
    from compat_check.catalog.parser import parse_catalog
    from compat_check.platform.loader import load_platforms
    from compat_check.orchestrator.engine import Orchestrator

    features = parse_catalog(Path(catalog))
    platforms = load_platforms(Path(platforms_dir))

    if platform_filter:
        platforms = [p for p in platforms if p.slug == platform_filter]
        if not platforms:
            click.echo(f"Error: platform '{platform_filter}' not found", err=True)
            raise SystemExit(1)

    if recipe:
        with_recipe = [p for p in platforms if p.recipe]
        click.echo(f"Platforms with recipes: {[p.slug for p in with_recipe]}")
        if not with_recipe:
            click.echo("No platforms have recipes defined.", err=True)
            raise SystemExit(1)
        platforms = with_recipe

    click.echo(f"Platforms: {[p.slug for p in platforms]}")
    click.echo(f"Features: {len(features)} from catalog")
    click.echo(f"Parallel: {parallel}")
    if recipe:
        click.echo("Mode: with-recipe")

    orch = Orchestrator(
        platforms=platforms,
        features=features,
        test_dir=Path(tests_dir),
        results_dir=Path(results_dir),
        work_dir=Path(work_dir),
        max_parallel=parallel,
        apply_recipe=recipe,
    )

    results = orch.run(dry_run=dry_run)
    click.echo(f"Completed: {len(results)} results")


@main.command()
@click.option("--target", default="catalog/data.yaml", type=click.Path())
def sync(target):
    """Sync the feature catalog from upstream."""
    from compat_check.catalog.sync import sync_catalog

    click.echo("Syncing catalog from upstream...")
    sync_catalog(Path(target))
    click.echo(f"Catalog saved to {target}")


@main.command()
@click.option("--results-dir", default="results", type=click.Path(exists=True))
@click.option("--output-dir", default="site", type=click.Path())
@click.option("--platforms-dir", default="platforms", type=click.Path(exists=True))
def generate(results_dir, output_dir, platforms_dir):
    """Generate static site and README from results."""
    import json
    import glob as glob_mod
    from compat_check.platform.loader import load_platforms
    from compat_check.site.html import generate_site
    from compat_check.site.readme import generate_summary_table

    platforms = load_platforms(Path(platforms_dir))
    platform_meta = {p.slug: p for p in platforms}

    all_results = []
    for f in glob_mod.glob(f"{results_dir}/**/*.json", recursive=True):
        if "manifest" in f or "+recipe" in f:
            continue
        with open(f) as fh:
            all_results.extend(json.load(fh))

    generate_site(all_results, Path(output_dir), platform_meta)
    click.echo(f"Site generated at {output_dir}/")

    table = generate_summary_table(all_results, platform_meta)

    # Update the matrix table in README.md between markers, or append
    readme_path = Path("README.md")
    start_marker = "<!-- compat-matrix-start -->"
    end_marker = "<!-- compat-matrix-end -->"
    matrix_block = f"{start_marker}\n{table}{end_marker}"

    if readme_path.exists():
        content = readme_path.read_text()
        if start_marker in content and end_marker in content:
            import re
            content = re.sub(
                f"{re.escape(start_marker)}.*?{re.escape(end_marker)}",
                matrix_block,
                content,
                flags=re.DOTALL,
            )
            readme_path.write_text(content)
            click.echo("README.md matrix updated")
        else:
            click.echo("README.md: no compat-matrix markers found, skipping update")
    else:
        readme_path.write_text(f"# Embedded C++ Compatibility Matrix\n\n{matrix_block}\n")
        click.echo("README.md created")


@main.command()
@click.argument("library_path", type=click.Path(exists=True))
@click.option("--platforms-dir", default="platforms", type=click.Path(exists=True))
@click.option("--platform", "platform_filter", multiple=True, help="Test only these platforms")
@click.option("--example", "example_filter", multiple=True, help="Test only these examples")
@click.option("--report", "report_path", default=None, type=click.Path(), help="Write report to file")
@click.option("--report-format", "report_fmt", default="md", type=click.Choice(["md", "json"]))
@click.option("--work-dir", default=".work", type=click.Path())
def library(library_path, platforms_dir, platform_filter, example_filter,
            report_path, report_fmt, work_dir):
    """Check library compatibility across platforms."""
    import json as json_mod
    from compat_check.library.metadata import parse_metadata, discover_examples
    from compat_check.library.resolver import resolve_platforms
    from compat_check.library.builder import run_library_build
    from compat_check.library.report import generate_markdown_report, generate_json_report
    from compat_check.platform.loader import load_platforms

    library_dir = Path(library_path)
    meta = parse_metadata(library_dir)
    click.echo(f"Library: {meta.name} v{meta.version}")

    # Resolve platforms
    all_platforms = load_platforms(Path(platforms_dir))
    platforms = resolve_platforms(meta.platforms, all_platforms)
    if platform_filter:
        platforms = [p for p in platforms if p.slug in platform_filter]
    if not platforms:
        click.echo("No matching platforms found.", err=True)
        raise SystemExit(1)
    click.echo(f"Platforms: {[p.slug for p in platforms]}")

    # Discover examples
    examples = discover_examples(library_dir)
    if example_filter:
        examples = [e for e in examples if e.name in example_filter]
    if not examples:
        click.echo("No examples found.", err=True)
        raise SystemExit(1)
    click.echo(f"Examples: {[e.name for e in examples]}")

    # Build matrix
    # Test highest standard first per (platform, example). If the highest
    # fails, lower standards will too — skip them. If it passes, test
    # descending to find the minimum working standard.
    results = []
    total = sum(len(p.standards) for p in platforms) * len(examples)
    done = 0
    skipped = 0
    work = Path(work_dir)

    for platform in platforms:
        board = platform.platformio["board"]
        build_dir = work / "library" / platform.slug
        standards_desc = list(reversed(platform.standards))

        for example in examples:
            found_pass = False
            found_fail_descending = False

            for standard in standards_desc:
                done += 1

                # If highest standard failed, skip all lower standards
                if found_fail_descending:
                    skipped += 1
                    click.echo(
                        f"  [{done}/{total}] {platform.slug} {standard} {example.name}..."
                        f" SKIP"
                    )
                    results.append({
                        "platform": platform.slug,
                        "standard": standard,
                        "example": example.name,
                        "pass": False,
                        "error": None,
                        "skipped": True,
                    })
                    continue

                # If we already found a failing standard below a passing one,
                # all lower standards also fail — skip them
                if found_pass and found_fail_descending:
                    skipped += 1
                    click.echo(
                        f"  [{done}/{total}] {platform.slug} {standard} {example.name}..."
                        f" SKIP"
                    )
                    results.append({
                        "platform": platform.slug,
                        "standard": standard,
                        "example": example.name,
                        "pass": False,
                        "error": None,
                        "skipped": True,
                    })
                    continue

                click.echo(
                    f"  [{done}/{total}] {platform.slug} {standard} {example.name}...",
                    nl=False,
                )
                result = run_library_build(
                    library_path=library_dir,
                    example_path=example.path,
                    board=board,
                    standard=standard,
                    build_dir=build_dir,
                    fixed_standard=platform.fixed_standard,
                )
                status = "PASS" if result.success else "FAIL"
                click.echo(f" {status} ({result.compile_time_ms}ms)")

                if result.success:
                    found_pass = True
                else:
                    if not found_pass:
                        # Highest standard failed — everything below fails too
                        found_fail_descending = True

                results.append({
                    "platform": platform.slug,
                    "standard": standard,
                    "example": example.name,
                    "pass": result.success,
                    "error": result.error if not result.success else None,
                })

    if skipped:
        click.echo(f"  ({skipped} builds skipped)")

    # Generate report
    lib_info = {"name": meta.name, "version": meta.version}
    if report_fmt == "json":
        report_data = generate_json_report(lib_info, results)
        output = json_mod.dumps(report_data, indent=2)
    else:
        output = generate_markdown_report(lib_info, results)

    if report_path:
        Path(report_path).write_text(output + "\n")
        click.echo(f"Report written to {report_path}")
    else:
        click.echo("")
        click.echo(output)


if __name__ == "__main__":
    main()
