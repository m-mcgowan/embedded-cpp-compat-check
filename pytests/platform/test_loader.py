from pathlib import Path
from compat_check.platform.loader import load_platform, load_platforms
from compat_check.platform.models import Platform

FIXTURES = Path(__file__).parent / "fixtures"

def test_load_platform():
    p = load_platform(FIXTURES / "esp32s3-test.yaml")
    assert isinstance(p, Platform)
    assert p.slug == "esp32s3-test"
    assert p.build_system == "platformio"
    assert "c++17" in p.standards
    assert p.platformio["board"] == "esp32-s3-devkitm-1"

def test_load_platforms_from_directory():
    platforms = load_platforms(FIXTURES)
    assert len(platforms) >= 1
    slugs = [p.slug for p in platforms]
    assert "esp32s3-test" in slugs
