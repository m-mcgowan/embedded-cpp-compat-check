from pathlib import Path

from compat_check.site.html import generate_site


def test_generate_site_creates_index(tmp_path):
    results = [
        {
            "platform": "esp32",
            "platform_version": "1.0",
            "standard": "c++17",
            "feature": "cpp17/optional",
            "macro": "__cpp_lib_optional",
            "category": "library",
            "status": "supported",
            "macro_value": 201606,
            "compiles": True,
            "compile_time_ms": 100,
        },
    ]
    generate_site(results, tmp_path)
    index = tmp_path / "index.html"
    assert index.exists()
    content = index.read_text()
    assert "esp32" in content
    assert "c++17" in content


def test_generate_site_creates_platform_page(tmp_path):
    results = [
        {
            "platform": "esp32",
            "platform_version": "1.0",
            "standard": "c++17",
            "feature": "cpp17/optional",
            "macro": "__cpp_lib_optional",
            "category": "library",
            "status": "supported",
            "macro_value": 201606,
            "compiles": True,
            "compile_time_ms": 100,
        },
    ]
    generate_site(results, tmp_path)
    platform_page = tmp_path / "esp32" / "index.html"
    assert platform_page.exists()
    content = platform_page.read_text()
    assert "optional" in content
