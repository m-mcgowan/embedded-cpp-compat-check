from compat_check.catalog.models import Feature, FeatureKind
from compat_check.probe.generator import generate_probe_source


def _make_features():
    return [
        Feature(name="__cpp_structured_bindings", kind=FeatureKind.LANGUAGE, standard="cpp17", description="Structured bindings", values=[201606]),
        Feature(name="__cpp_lib_optional", kind=FeatureKind.LIBRARY, standard="cpp17", description="std::optional", values=[201606], headers=["optional"]),
    ]


def test_generate_probe_includes_version_header():
    source = generate_probe_source(_make_features())
    assert "#if __has_include(<version>)" in source
    assert "#include <version>" in source


def test_generate_probe_checks_language_macro():
    source = generate_probe_source(_make_features())
    assert "#ifdef __cpp_structured_bindings" in source
    assert '"__cpp_structured_bindings="' in source


def test_generate_probe_checks_library_macro():
    source = generate_probe_source(_make_features())
    assert "#ifdef __cpp_lib_optional" in source
    assert '"__cpp_lib_optional="' in source


def test_generate_probe_has_sentinel():
    source = generate_probe_source(_make_features())
    assert "__SENTINEL__=-1" in source


def test_generate_probe_references_array():
    """Probe must reference the array to prevent linker stripping."""
    source = generate_probe_source(_make_features())
    assert "probe_results" in source
    assert "probe_sink" in source
