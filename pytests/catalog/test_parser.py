from pathlib import Path
from compat_check.catalog.models import FeatureKind
from compat_check.catalog.parser import parse_catalog

FIXTURES = Path(__file__).parent / "fixtures"

def test_parse_catalog_language_features():
    features = parse_catalog(FIXTURES / "small_catalog.yaml")
    lang = [f for f in features if f.kind == FeatureKind.LANGUAGE]
    assert len(lang) == 1
    assert lang[0].name == "__cpp_structured_bindings"
    assert lang[0].standard == "cpp17"
    assert 201606 in lang[0].values

def test_parse_catalog_library_features():
    features = parse_catalog(FIXTURES / "small_catalog.yaml")
    lib = [f for f in features if f.kind == FeatureKind.LIBRARY]
    assert len(lib) == 1
    assert lib[0].name == "__cpp_lib_optional"
    assert lib[0].headers == ["optional"]
    assert 201606 in lib[0].values
    assert 202110 in lib[0].values

def test_parse_catalog_attributes():
    features = parse_catalog(FIXTURES / "small_catalog.yaml")
    attrs = [f for f in features if f.kind == FeatureKind.ATTRIBUTE]
    assert len(attrs) == 1
    assert attrs[0].name == "__has_cpp_attribute(nodiscard)"

def test_parse_catalog_infers_standard_from_support():
    features = parse_catalog(FIXTURES / "small_catalog.yaml")
    by_name = {f.name: f for f in features}
    assert by_name["__cpp_lib_optional"].standard == "cpp17"
