"""Platform definition data model."""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Recipe:
    """Steps to achieve full modern C++ support on a platform."""
    lib_deps: list[str] = field(default_factory=list)
    build_flags: str = ""
    build_unflags: str = ""
    description: str = ""


@dataclass(frozen=True)
class Platform:
    name: str
    slug: str
    version: str
    architecture: str
    mcu: str
    build_system: str
    standards: list[str]
    framework: str = ""
    fixed_standard: bool = False
    recipe: Recipe | None = None
    platformio: dict = field(default_factory=dict)
    release_monitor: dict = field(default_factory=dict)
