"""Run PlatformIO CI builds for library examples."""
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

_STD_UNFLAGS = (
    "-std=gnu++11 -std=gnu++14 -std=gnu++17 -std=gnu++20 -std=gnu++23 "
    "-std=c++11 -std=c++14 -std=c++17 -std=c++20 -std=c++23"
)

@dataclass
class BuildResult:
    success: bool
    compile_time_ms: int
    output: str
    error: str

def run_library_build(
    library_path: Path, example_path: Path,
    board: str, standard: str, timeout: int = 600,
) -> BuildResult:
    std_num = standard.replace("c++", "")
    std_flag = f"-std=gnu++{std_num}"
    cmd = [
        "pio", "ci",
        f"--lib={library_path}",
        f"--board={board}",
        "-O", f"build_unflags={_STD_UNFLAGS}",
        "-O", f"build_flags={std_flag}",
        str(example_path),
    ]
    start = time.monotonic()
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    elapsed_ms = int((time.monotonic() - start) * 1000)
    return BuildResult(
        success=result.returncode == 0,
        compile_time_ms=elapsed_ms,
        output=result.stdout, error=result.stderr,
    )
