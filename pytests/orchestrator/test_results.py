from compat_check.orchestrator.results import classify_feature, FeatureStatus


def test_supported():
    assert classify_feature(macro_value=201606, compiles=True) == FeatureStatus.SUPPORTED

def test_macro_lies():
    assert classify_feature(macro_value=201606, compiles=False) == FeatureStatus.MACRO_LIES

def test_unreported():
    assert classify_feature(macro_value=0, compiles=True) == FeatureStatus.UNREPORTED

def test_unsupported():
    assert classify_feature(macro_value=0, compiles=False) == FeatureStatus.UNSUPPORTED

def test_macro_only_yes():
    assert classify_feature(macro_value=201606, compiles=None) == FeatureStatus.MACRO_ONLY_YES

def test_macro_only_no():
    assert classify_feature(macro_value=0, compiles=None) == FeatureStatus.MACRO_ONLY_NO
