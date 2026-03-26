"""Platform definition data model."""
from dataclasses import dataclass, field


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
    platformio: dict = field(default_factory=dict)
    release_monitor: dict = field(default_factory=dict)
