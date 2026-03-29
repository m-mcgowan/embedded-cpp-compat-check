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
