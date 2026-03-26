from compat_check.catalog.models import Feature, FeatureKind

def test_feature_creation():
    f = Feature(name="__cpp_structured_bindings", kind=FeatureKind.LANGUAGE, standard="cpp17", description="Structured bindings declaration", values=[201606], headers=[])
    assert f.name == "__cpp_structured_bindings"
    assert f.kind == FeatureKind.LANGUAGE
    assert f.is_language

def test_library_feature_has_headers():
    f = Feature(name="__cpp_lib_optional", kind=FeatureKind.LIBRARY, standard="cpp17", description="std::optional", values=[201606, 202110], headers=["optional"])
    assert f.is_library
    assert "optional" in f.headers
