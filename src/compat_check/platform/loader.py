"""Load platform definitions from YAML files."""
from pathlib import Path
import yaml
from .models import Platform, Recipe


def _load_recipe(data: dict | None) -> Recipe | None:
    if not data:
        return None
    return Recipe(
        lib_deps=data.get("lib_deps", []),
        build_flags=data.get("build_flags", ""),
        build_unflags=data.get("build_unflags", ""),
        description=data.get("description", ""),
    )


def load_platform(path: Path) -> Platform:
    """Load a single platform definition from a YAML file."""
    with open(path) as f:
        data = yaml.safe_load(f)
    return Platform(
        name=data["name"],
        slug=data["slug"],
        version=data.get("version", "unknown"),
        architecture=data["architecture"],
        mcu=data["mcu"],
        build_system=data["build_system"],
        standards=data["standards"],
        framework=data.get("framework", ""),
        board_family=data.get("board_family", ""),
        fixed_standard=data.get("fixed_standard", False),
        min_framework_standard=data.get("min_framework_standard", ""),
        recipe=_load_recipe(data.get("recipe")),
        platformio=data.get("platformio", {}),
        release_monitor=data.get("release_monitor", {}),
    )


def load_platforms(directory: Path) -> list[Platform]:
    """Load all platform definitions from a directory."""
    platforms = []
    for path in sorted(directory.glob("*.yaml")):
        platforms.append(load_platform(path))
    return platforms
