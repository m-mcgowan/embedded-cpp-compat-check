"""Cross-reference Stage 1 and Stage 2 results."""

from enum import Enum


class FeatureStatus(str, Enum):
    SUPPORTED = "supported"
    MACRO_LIES = "macro_lies"
    UNREPORTED = "unreported"
    UNSUPPORTED = "unsupported"
    MACRO_ONLY_YES = "macro_only_yes"
    MACRO_ONLY_NO = "macro_only_no"


def classify_feature(
    macro_value: int,
    compiles: bool | None,
) -> FeatureStatus:
    """Classify a feature based on macro probe and compile test results."""
    macro_defined = macro_value > 0

    if compiles is None:
        return FeatureStatus.MACRO_ONLY_YES if macro_defined else FeatureStatus.MACRO_ONLY_NO

    if macro_defined and compiles:
        return FeatureStatus.SUPPORTED
    if macro_defined and not compiles:
        return FeatureStatus.MACRO_LIES
    if not macro_defined and compiles:
        return FeatureStatus.UNREPORTED
    return FeatureStatus.UNSUPPORTED
