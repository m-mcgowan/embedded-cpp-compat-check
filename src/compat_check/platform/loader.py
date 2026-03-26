"""Load platform definitions from YAML files."""
from pathlib import Path
import yaml
from .models import Platform


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
        platformio=data.get("platformio", {}),
        release_monitor=data.get("release_monitor", {}),
    )


def load_platforms(directory: Path) -> list[Platform]:
    """Load all platform definitions from a directory."""
    platforms = []
    for path in sorted(directory.glob("*.yaml")):
        platforms.append(load_platform(path))
    return platforms
