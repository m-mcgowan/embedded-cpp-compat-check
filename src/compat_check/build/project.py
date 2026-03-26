"""Generate temporary PlatformIO projects for compilation tests."""

import shutil
from pathlib import Path

from compat_check.platform.models import Platform

_COMMON_DEFAULTS = [
    "-std=gnu++11", "-std=gnu++14", "-std=gnu++17",
    "-std=gnu++20", "-std=gnu++23",
    "-std=c++11", "-std=c++14", "-std=c++17",
    "-std=c++20", "-std=c++23",
]


def _std_flag(standard: str) -> str:
    """Convert 'c++17' to '-std=gnu++17'."""
    num = standard.replace("c++", "")
    return f"-std=gnu++{num}"


def generate_pio_project(
    output_dir: Path,
    platform: Platform,
    standard: str,
    source_file: Path,
) -> None:
    """Generate a minimal PlatformIO project for a single compilation test."""
    output_dir.mkdir(parents=True, exist_ok=True)
    src_dir = output_dir / "src"
    src_dir.mkdir(exist_ok=True)

    shutil.copy2(source_file, src_dir / "main.cpp")

    pio = platform.platformio
    std_flag = _std_flag(standard)
    unflag_line = " ".join(_COMMON_DEFAULTS)

    ini_content = (
        f"[env:test]\n"
        f"platform = {pio['platform']}\n"
        f"board = {pio['board']}\n"
    )
    if pio.get("framework"):
        ini_content += f"framework = {pio['framework']}\n"
    ini_content += (
        f"build_unflags = {unflag_line}\n"
        f"build_flags = {std_flag}\n"
    )

    (output_dir / "platformio.ini").write_text(ini_content)
