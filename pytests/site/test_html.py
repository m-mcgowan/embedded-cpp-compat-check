import textwrap
from pathlib import Path

import pytest

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


@pytest.fixture
def tiers_yaml(tmp_path):
    p = tmp_path / "tiers.yaml"
    p.write_text(textwrap.dedent("""
        cpp17:
          tentpoles:
            - id: optional
              name: std::optional
              required: [__cpp_lib_optional]
        """))
    return p


def test_matrix_cell_includes_tentpole_count(tmp_path, tiers_yaml):
    results = [
        {"platform": "esp32", "standard": "c++17",
         "feature": "cpp17/optional", "category": "library",
         "macro": "__cpp_lib_optional", "status": "supported", "compiles": True},
    ]
    out = tmp_path / "site"
    generate_site(results, out, tiers_path=tiers_yaml)
    index = (out / "index.html").read_text()
    # Cell should include "1/1 tentpoles" beside the raw %
    assert "1/1 tentpoles" in index


def test_matrix_cell_omits_tentpole_line_when_none_defined(tmp_path, tiers_yaml):
    """For C++20 where no tentpoles are defined in this tiers fixture, no sub-line."""
    results = [
        {"platform": "esp32", "standard": "c++20",
         "feature": "cpp20/concepts", "category": "language",
         "macro": "__cpp_concepts", "status": "supported", "compiles": True},
    ]
    out = tmp_path / "site"
    generate_site(results, out, tiers_path=tiers_yaml)
    index = (out / "index.html").read_text()
    assert "tentpoles" not in index
