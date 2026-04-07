"""Run PlatformIO builds and capture results."""

import os
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path


@dataclass
class BuildResult:
    success: bool
    compile_time_ms: int
    output: str
    error: str


def run_build(
    project_dir: Path,
    core_dir: Path | None = None,
    timeout: int = 600,
) -> BuildResult:
    """Run 'pio run' in the given project directory."""
    env = os.environ.copy()
    if core_dir:
        env["PLATFORMIO_CORE_DIR"] = str(core_dir)

    start = time.monotonic()
    result = subprocess.run(
        ["pio", "run", "-d", str(project_dir)],
        capture_output=True,
        text=True,
        timeout=timeout,
        env=env,
    )
    elapsed_ms = int((time.monotonic() - start) * 1000)

    return BuildResult(
        success=result.returncode == 0,
        compile_time_ms=elapsed_ms,
        output=result.stdout,
        error=result.stderr,
    )


def run_build_verbose(
    project_dir: Path,
    core_dir: Path | None = None,
    timeout: int = 600,
) -> tuple[BuildResult, str]:
    """Run 'pio run -v' and return both the build result and verbose output."""
    env = os.environ.copy()
    if core_dir:
        env["PLATFORMIO_CORE_DIR"] = str(core_dir)

    start = time.monotonic()
    result = subprocess.run(
        ["pio", "run", "-v", "-d", str(project_dir)],
        capture_output=True,
        text=True,
        timeout=timeout,
        env=env,
    )
    elapsed_ms = int((time.monotonic() - start) * 1000)

    build_result = BuildResult(
        success=result.returncode == 0,
        compile_time_ms=elapsed_ms,
        output=result.stdout,
        error=result.stderr,
    )
    return build_result, result.stdout


def run_batch_build(
    project_dir: Path,
    feature_to_stem: dict[str, str],
    timeout: int = 600,
) -> dict[str, BuildResult]:
    """Run PIO build with keep-going and return per-feature results.

    Uses SCONSFLAGS="-k" so PIO continues past individual file errors.
    Determines pass/fail by checking which .o files were produced.
    Captures error output per feature from the build log.
    """
    env = os.environ.copy()
    env["SCONSFLAGS"] = env.get("SCONSFLAGS", "") + " -k"

    start = time.monotonic()
    result = subprocess.run(
        ["pio", "run", "-d", str(project_dir)],
        capture_output=True,
        text=True,
        timeout=timeout,
        env=env,
    )
    total_ms = int((time.monotonic() - start) * 1000)

    # Find compiled .o files
    obj_dir = None
    for candidate in (project_dir / ".pio" / "build").glob("*/src"):
        obj_dir = candidate
        break

    compiled_stems = set()
    if obj_dir:
        for obj in obj_dir.glob("*.cpp.o"):
            # "cpp17__optional.cpp.o" → "cpp17__optional"
            compiled_stems.add(obj.name.replace(".cpp.o", ""))

    # Parse errors per file from build output
    all_output = result.stdout + "\n" + result.stderr
    file_errors = _parse_per_file_errors(all_output, feature_to_stem)

    # Build per-feature results
    results: dict[str, BuildResult] = {}
    per_file_ms = total_ms // max(len(feature_to_stem), 1)
    for feature_key, stem in feature_to_stem.items():
        success = stem in compiled_stems
        error = file_errors.get(stem, "")
        results[feature_key] = BuildResult(
            success=success,
            compile_time_ms=per_file_ms,
            output="",
            error=error if not success else "",
        )

    return results


def _parse_per_file_errors(output: str, feature_to_stem: dict[str, str]) -> dict[str, str]:
    """Extract per-file error output from PIO build log.

    Groups error lines by the source file they reference.
    """
    stem_set = set(feature_to_stem.values())
    errors: dict[str, list[str]] = {s: [] for s in stem_set}
    current_stem = None

    for line in output.split("\n"):
        # Match lines referencing a test source file
        # e.g. "src/cpp17__optional.cpp:8:10: error: ..."
        for stem in stem_set:
            if f"{stem}.cpp" in line:
                current_stem = stem
                break

        if current_stem and (
            "error:" in line or "warning:" in line
            or "In file included from" in line
            or line.startswith(" ")  # continuation of previous error
        ):
            errors[current_stem].append(line)
        elif line.strip() and not any(f"{s}.cpp" in line for s in stem_set):
            # Line not related to any test file — reset context
            if current_stem and not line.startswith(" "):
                current_stem = None

    return {
        stem: "\n".join(lines)[:500]
        for stem, lines in errors.items()
        if lines
    }
