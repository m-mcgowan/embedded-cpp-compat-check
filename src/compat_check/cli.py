"""CLI entry point for the compatibility checker."""

import click
from pathlib import Path


@click.group()
def main():
    """Embedded C++ Compatibility Checker."""
    pass


def _get_command_help(command_name: str) -> str:
    """Get the --help output for a subcommand."""
    cmd = main.commands.get(command_name)
    if not cmd:
        return ""
    ctx = click.Context(cmd, info_name=f"compat-check {command_name}")
    return cmd.get_help(ctx)


@main.command()
@click.option("--catalog", default="catalog/data.yaml", type=click.Path(exists=True),
              help="SD-6 feature catalog YAML", show_default=True)
@click.option("--platforms-dir", default="platforms", type=click.Path(exists=True),
              help="Directory containing platform YAML definitions", show_default=True)
@click.option("--tests-dir", default="tests", type=click.Path(exists=True),
              help="Directory containing C++ test files", show_default=True)
@click.option("--results-dir", default="results", type=click.Path(),
              help="Output directory for JSON results", show_default=True)
@click.option("--work-dir", default=".work", type=click.Path(),
              help="Build cache directory", show_default=True)
@click.option("--platform", "platform_filter", default=None,
              help="Run only this platform (slug from platforms/*.yaml)")
@click.option("--test", "test_filter", default=None,
              help="Run only this test (filename without .cpp)")
@click.option("--parallel", default=4, type=int,
              help="Max parallel builds (1=serial)", show_default=True)
@click.option("--dry-run", is_flag=True, help="Show what would be built without building")
@click.option("--recipe", is_flag=True,
              help="Apply platform recipes (test with polyfill libraries like nonstd-lite-bundle)")
def run(catalog, platforms_dir, tests_dir, results_dir, work_dir,
        platform_filter, test_filter, parallel, dry_run, recipe):
    """Test C++ feature compatibility across embedded platforms.

    Runs 394 SD-6 feature tests against each platform at every supported
    C++ standard. Results are saved as JSON and can be rendered as an
    HTML site with 'compat-check generate'.

    The first run downloads PlatformIO toolchains (~200MB per platform).
    Subsequent runs are incremental — only changed tests are rebuilt.
    """
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
@click.option("--target", default="catalog/data.yaml", type=click.Path(),
              help="Output path for the catalog YAML", show_default=True)
def sync(target):
    """Sync the SD-6 feature catalog from upstream.

    Downloads the latest feature-test macro database from
    github.com/cpplearner/feature-test-macro and saves it locally.
    """
    from compat_check.catalog.sync import sync_catalog

    click.echo("Syncing catalog from upstream...")
    sync_catalog(Path(target))
    click.echo(f"Catalog saved to {target}")


@main.command()
@click.option("--results-dir", default="results", type=click.Path(exists=True),
              help="Directory containing JSON results from 'compat-check run'", show_default=True)
@click.option("--output-dir", default="site", type=click.Path(),
              help="Output directory for the HTML site", show_default=True)
@click.option("--platforms-dir", default="platforms", type=click.Path(exists=True),
              help="Directory containing platform YAML definitions", show_default=True)
@click.option("--site-url", default="",
              help="Base URL for platform links in README (e.g. https://user.github.io/repo)")
def generate(results_dir, output_dir, platforms_dir, site_url):
    """Generate a browsable HTML site and update the README compatibility matrix.

    Reads JSON results from a previous 'compat-check run' and produces:
    - An HTML site with per-platform feature tables
    - An updated compatibility matrix in README.md (between marker comments)
    """
    import json
    import glob as glob_mod
    from compat_check.platform.loader import load_platforms
    from compat_check.site.html import generate_site
    from compat_check.site.readme import generate_summary_table

    platforms = load_platforms(Path(platforms_dir))
    platform_meta = {p.slug: p for p in platforms}

    all_results = []
    for f in glob_mod.glob(f"{results_dir}/**/*.json", recursive=True):
        if "manifest" in f:
            continue
        with open(f) as fh:
            all_results.extend(json.load(fh))

    generate_site(all_results, Path(output_dir), platform_meta,
                  catalog_path=Path("catalog/data.yaml"))
    click.echo(f"Site generated at {output_dir}/")

    table = generate_summary_table(all_results, platform_meta, site_url=site_url)

    # Update the matrix table in README.md between markers, or append
    readme_path = Path("README.md")
    start_marker = "<!-- compat-matrix-start -->"
    end_marker = "<!-- compat-matrix-end -->"
    matrix_block = f"{start_marker}\n{table}{end_marker}"

    if readme_path.exists():
        content = readme_path.read_text()
        if start_marker in content and end_marker in content:
            import re
            # Require markers at start of line (block-level HTML comments),
            # so inline examples like `<!-- compat-matrix-start -->` in docs
            # are left untouched.
            content = re.sub(
                f"^{re.escape(start_marker)}.*?^{re.escape(end_marker)}",
                matrix_block,
                content,
                flags=re.DOTALL | re.MULTILINE,
            )
            # Inject CLI help output for each command
            help_sections = {
                "cli-library-help": ("compat-check library --help", _get_command_help("library")),
                "cli-run-help": ("compat-check run --help", _get_command_help("run")),
                "cli-generate-help": ("compat-check generate --help", _get_command_help("generate")),
                "cli-sync-help": ("compat-check sync --help", _get_command_help("sync")),
            }
            for name, (cmd, help_text) in help_sections.items():
                start = f"<!-- {name}-start -->"
                end = f"<!-- {name}-end -->"
                if start in content and end in content:
                    block = f"{start}\n```\n$ {cmd}\n\n{help_text}\n```\n{end}"
                    content = re.sub(
                        f"{re.escape(start)}.*?{re.escape(end)}",
                        block, content, flags=re.DOTALL,
                    )

            readme_path.write_text(content)
            click.echo("README.md updated")
        else:
            click.echo("README.md: no compat-matrix markers found, skipping update")
    else:
        readme_path.write_text(f"# Embedded C++ Compatibility Matrix\n\n{matrix_block}\n")
        click.echo("README.md created")


@main.command()
@click.argument("library_ref")
@click.option("--platforms-dir", default=None, type=click.Path(exists=True),
              help="Directory containing platform YAML definitions (default: bundled)")
@click.option("--platform", "platform_filter", multiple=True,
              help="Test only these platforms (repeatable). Defaults to platforms from library.json.")
@click.option("--example", "example_filter", multiple=True,
              help="Test only these examples (repeatable). Defaults to all examples.")
@click.option("--report", "report_path", default=None, type=click.Path(),
              help="Write report to file (default: stdout)")
@click.option("--report-format", "report_fmt", default=None, type=click.Choice(["md", "json"]),
              help="Report format. Auto-detected from --report extension if omitted.")
@click.option("--lib-deps", multiple=True,
              help="Additional library dependencies for the build (repeatable). "
                   "Accepts PIO library names, URLs, or local paths.")
@click.option("--recipe", is_flag=True,
              help="Include platform recipes (e.g. avr-libstdcpp for AVR). "
                   "Adds each platform's recipe lib_deps to the build.")
@click.option("--pretty", is_flag=True,
              help="Use ✅/❌ emoji instead of PASS/FAIL in the markdown report.")
@click.option("--work-dir", default=".work", type=click.Path(),
              help="Build cache directory", show_default=True)
def library(library_ref, platforms_dir, platform_filter, example_filter,
            report_path, report_fmt, lib_deps, recipe, pretty, work_dir):
    """Test a PlatformIO library across embedded platforms and C++ standards.

    LIBRARY_REF is either a local directory path or a PlatformIO registry
    package name (with optional @version). If the argument exists as a
    directory, it's treated as a local path. Otherwise it's installed
    from the registry.

    \b
    Examples:
      compat-check library ~/my-library          # local directory
      compat-check library ArduinoJson            # registry, latest
      compat-check library ArduinoJson@6.21.0     # registry, pinned

    For each platform, tests the highest C++ standard first and works
    downward to find the minimum working standard. Generates a compatibility
    report showing which platforms and standards your library supports.
    """
    import json as json_mod
    import subprocess
    import tempfile

    # Auto-detect report format from file extension
    if report_fmt is None and report_path:
        if report_path.endswith(".json"):
            report_fmt = "json"
        else:
            report_fmt = "md"
    elif report_fmt is None:
        report_fmt = "md"
    from compat_check.library.metadata import parse_metadata, discover_examples
    from compat_check.library.resolver import resolve_platforms
    from compat_check.library.builder import run_library_build
    from compat_check.library.report import generate_markdown_report, generate_json_report
    from compat_check.platform.loader import load_platforms, bundled_platforms_dir

    # Use bundled platform definitions when --platforms-dir is not specified
    if platforms_dir is None:
        platforms_dir = str(bundled_platforms_dir())

    # Resolve library reference: local path or PIO registry package
    library_dir = Path(library_ref)
    if not library_dir.is_dir():
        # Not a local directory — install from PIO registry into work dir
        pkg_name = library_ref.split("@")[0].strip()
        pkg_dir = Path(work_dir) / "registry" / pkg_name
        pkg_dir.mkdir(parents=True, exist_ok=True)
        click.echo(f"Installing {library_ref} from PlatformIO registry...")
        result = subprocess.run(
            ["pio", "pkg", "install",
             "--storage-dir", str(pkg_dir),
             "--library", library_ref],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            click.echo(f"Failed to install {library_ref}: {result.stderr.strip()}", err=True)
            raise SystemExit(1)
        # Find the installed library directory
        library_dir = pkg_dir
        for candidate in pkg_dir.iterdir():
            if candidate.is_dir() and (candidate / "library.json").exists():
                library_dir = candidate
                break
            if candidate.is_dir() and (candidate / "library.properties").exists():
                library_dir = candidate
                break
        if not (library_dir / "library.json").exists() and not (library_dir / "library.properties").exists():
            click.echo(f"Could not find installed library {library_ref} in {pkg_dir}", err=True)
            raise SystemExit(1)
        click.echo(f"Using {library_dir}")

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
                # Combine explicit --lib-deps with platform recipe deps
                all_deps = list(lib_deps) if lib_deps else []
                if recipe and platform.recipe and platform.recipe.lib_deps:
                    all_deps.extend(platform.recipe.lib_deps)

                result = run_library_build(
                    library_path=library_dir,
                    example_path=example.path,
                    board=board,
                    standard=standard,
                    build_dir=build_dir,
                    fixed_standard=platform.fixed_standard,
                    lib_deps=all_deps or None,
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
        output = generate_markdown_report(lib_info, results, pretty=pretty)

    # Always print summary to stderr
    from compat_check.library.report import _build_summary
    summary = _build_summary(results)
    click.echo("")
    for plat in sorted(summary):
        s = summary[plat]
        min_std = s["min_standard"] or "\u2014"
        reason = s.get("failure_reason", "")
        line = f"  {plat}: {s['passing']}/{s['total']} examples, min standard: {min_std}"
        if reason and s["passing"] < s["total"]:
            line += f"  ({reason})"
        click.echo(line)

    if report_path:
        Path(report_path).write_text(output + "\n")
        click.echo(f"\nReport written to {report_path}")
    else:
        click.echo("")
        click.echo(output)


if __name__ == "__main__":
    main()
