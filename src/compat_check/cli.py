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
def run(catalog, platforms_dir, tests_dir, results_dir, work_dir,
        platform_filter, test_filter, parallel, dry_run):
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

    click.echo(f"Platforms: {[p.slug for p in platforms]}")
    click.echo(f"Features: {len(features)} from catalog")
    click.echo(f"Parallel: {parallel}")

    orch = Orchestrator(
        platforms=platforms,
        features=features,
        test_dir=Path(tests_dir),
        results_dir=Path(results_dir),
        work_dir=Path(work_dir),
        max_parallel=parallel,
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
def generate(results_dir, output_dir):
    """Generate static site and README from results."""
    import json
    import glob as glob_mod
    from compat_check.site.html import generate_site
    from compat_check.site.readme import generate_summary_table

    all_results = []
    for f in glob_mod.glob(f"{results_dir}/**/*.json", recursive=True):
        if "manifest" in f:
            continue
        with open(f) as fh:
            all_results.extend(json.load(fh))

    generate_site(all_results, Path(output_dir))
    click.echo(f"Site generated at {output_dir}/")

    table = generate_summary_table(all_results)
    readme = f"# Embedded C++ Compatibility Matrix\n\n{table}\n"
    Path("README.md").write_text(readme)
    click.echo("README.md updated")


if __name__ == "__main__":
    main()
