"""Generate temporary PlatformIO projects for compilation tests."""

import json
import re
from pathlib import Path

from compat_check.platform.models import Platform, Recipe

# Libraries that need a library.json injected because they don't ship one.
_LIBRARY_JSON_FIXUPS = {
    "avr-libstdcpp": {
        "name": "avr-libstdcpp",
        "version": "1.0.0",
        "description": "Subset of GCC libstdc++ for AVR",
        "platforms": ["atmelavr", "atmelmegaavr"],
        "frameworks": "*",
        "build": {"includeDir": "include", "srcDir": "src"},
    },
}

_COMMON_DEFAULTS = [
    "-std=gnu++11", "-std=gnu++14", "-std=gnu++17",
    "-std=gnu++20", "-std=gnu++23",
    "-std=c++11", "-std=c++14", "-std=c++17",
    "-std=c++20", "-std=c++23",
]

_ARDUINO_HEADER = '#include <Arduino.h>\n'
_ARDUINO_LOOP = '\nvoid loop() {}\n'


def _std_flag(standard: str) -> str:
    """Convert 'c++17' to '-std=gnu++17'."""
    num = standard.replace("c++", "")
    return f"-std=gnu++{num}"


def wrap_for_arduino(source: str) -> str:
    """Convert main()-based test to Arduino setup()/loop() format.

    Renames main() to _test_main() and calls it from setup().
    This preserves all return statements in helper functions and lambdas.
    """
    source = _ARDUINO_HEADER + source
    # Rename main to _test_main, keeping the return type
    source = re.sub(
        r'(auto\s+)main(\s*\(\s*\)\s*->\s*int)',
        r'\1_test_main\2',
        source,
    )
    source = re.sub(
        r'(int\s+)main(\s*\(\s*\))',
        r'\1_test_main\2',
        source,
    )
    source += '\nvoid setup() { _test_main(); }\n'
    source += _ARDUINO_LOOP
    return source


def generate_pio_project(
    output_dir: Path,
    platform: Platform,
    standard: str,
    source_file: Path,
    recipe: Recipe | None = None,
) -> None:
    """Generate a minimal PlatformIO project for a single compilation test.

    If recipe is provided, its lib_deps and build flags are added to the
    project configuration (used for "with-recipe" test runs).
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    src_dir = output_dir / "src"
    src_dir.mkdir(exist_ok=True)

    source_content = source_file.read_text()
    if platform.framework == "arduino":
        source_content = wrap_for_arduino(source_content)
    (src_dir / "main.cpp").write_text(source_content)

    # Clear compiled src objects so PlatformIO rebuilds with the new source,
    # but keep framework/library caches intact for fast incremental builds.
    for build_env in (output_dir / ".pio" / "build").glob("*/src"):
        for obj in build_env.glob("*"):
            obj.unlink(missing_ok=True)

    pio = platform.platformio

    ini_content = (
        f"[env:test]\n"
        f"platform = {pio['platform']}\n"
        f"board = {pio['board']}\n"
    )
    if pio.get("framework"):
        ini_content += f"framework = {pio['framework']}\n"

    # Collect build flags and unflags from standard override + recipe
    unflags = []
    flags = []

    if not platform.fixed_standard:
        unflags.extend(_COMMON_DEFAULTS)
        flags.append(_std_flag(standard))

    if recipe:
        if recipe.build_unflags:
            unflags.extend(recipe.build_unflags.split())
        if recipe.build_flags:
            flags.extend(recipe.build_flags.split())
        if recipe.lib_deps:
            ini_content += "lib_deps =\n"
            for dep in recipe.lib_deps:
                ini_content += f"    {dep}\n"

    if unflags:
        ini_content += f"build_unflags = {' '.join(unflags)}\n"
    if flags:
        ini_content += f"build_flags = {' '.join(flags)}\n"

    (output_dir / "platformio.ini").write_text(ini_content)


def inject_library_json_fixups(project_dir: Path) -> None:
    """Write library.json into downloaded libs that don't ship one.

    Call this AFTER the first pio build, which downloads lib_deps.
    """
    libdeps_dir = project_dir / ".pio" / "libdeps"
    if not libdeps_dir.exists():
        return
    for env_dir in libdeps_dir.iterdir():
        for lib_name, lib_json in _LIBRARY_JSON_FIXUPS.items():
            lib_dir = env_dir / lib_name
            json_path = lib_dir / "library.json"
            if lib_dir.is_dir() and not json_path.exists():
                json_path.write_text(json.dumps(lib_json, indent=2) + "\n")
