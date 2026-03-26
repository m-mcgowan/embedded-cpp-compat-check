"""Data models for the SD-6 feature catalog."""
from dataclasses import dataclass, field
from enum import Enum

class FeatureKind(Enum):
    LANGUAGE = "language"
    LIBRARY = "library"
    ATTRIBUTE = "attribute"

@dataclass(frozen=True)
class Feature:
    """A single SD-6 feature-test macro."""
    name: str
    kind: FeatureKind
    standard: str
    description: str
    values: list[int]
    headers: list[str] = field(default_factory=list)

    @property
    def is_language(self) -> bool:
        return self.kind == FeatureKind.LANGUAGE

    @property
    def is_library(self) -> bool:
        return self.kind == FeatureKind.LIBRARY
