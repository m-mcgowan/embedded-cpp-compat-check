"""Acceptance test: compat-check library against a vendored test library.

Requires PlatformIO installed and STM32 toolchain available.
Run with: pytest pytests/acceptance/ -v --timeout=300
"""

import json
from pathlib import Path

import pytest

from compat_check.library.metadata import parse_metadata, discover_examples
from compat_check.library.builder import run_library_build
from compat_check.library.report import generate_markdown_report, generate_json_report
from compat_check.library.resolver import resolve_platforms
from compat_check.platform.loader import load_platforms

TEST_LIBRARY = Path(__file__).parent.parent / "fixtures" / "test-library"
PLATFORMS_DIR = Path(__file__).parent.parent.parent / "platforms"


@pytest.fixture
def platforms():
    return load_platforms(PLATFORMS_DIR)


@pytest.fixture
def stm32(platforms):
    matches = [p for p in platforms if p.slug == "stm32-nucleo-f411re"]
    if not matches:
        pytest.skip("stm32-nucleo-f411re platform not found")
    return matches[0]


class TestLibraryMetadata:
    def test_discovers_library(self):
        meta = parse_metadata(TEST_LIBRARY)
        assert meta.name == "test-library"
        assert meta.version == "1.0.0"

    def test_discovers_examples(self):
        examples = discover_examples(TEST_LIBRARY)
        names = [e.name for e in examples]
        assert "blink" in names
        assert "types_demo" in names

    def test_resolves_star_platforms(self, platforms):
        meta = parse_metadata(TEST_LIBRARY)
        resolved = resolve_platforms(meta.platforms, platforms)
        assert len(resolved) == len(platforms)


class TestLibraryBuild:
    """Acceptance tests that run real PIO builds."""

    def test_build_passes_at_cpp17(self, stm32, tmp_path):
        """Test library builds successfully at c++17 on STM32."""
        examples = discover_examples(TEST_LIBRARY)
        blink = [e for e in examples if e.name == "blink"][0]

        result = run_library_build(
            library_path=TEST_LIBRARY,
            example_path=blink.path,
            board=stm32.platformio["board"],
            standard="c++17",
            build_dir=tmp_path / "build",
        )
        assert result.success, f"Build failed: {result.error[:200]}"

    def test_build_passes_at_cpp11(self, stm32, tmp_path):
        """Test library builds at c++11 — verifies cross-standard testing."""
        examples = discover_examples(TEST_LIBRARY)
        blink = [e for e in examples if e.name == "blink"][0]

        result = run_library_build(
            library_path=TEST_LIBRARY,
            example_path=blink.path,
            board=stm32.platformio["board"],
            standard="c++11",
            build_dir=tmp_path / "build",
        )
        assert result.success, f"Build failed: {result.error[:200]}"


class TestLibraryReport:
    """Test report generation from real build results."""

    def test_markdown_report(self, stm32, tmp_path):
        examples = discover_examples(TEST_LIBRARY)
        meta = parse_metadata(TEST_LIBRARY)
        results = []

        for example in examples:
            result = run_library_build(
                library_path=TEST_LIBRARY,
                example_path=example.path,
                board=stm32.platformio["board"],
                standard="c++17",
                build_dir=tmp_path / "build",
            )
            results.append({
                "platform": stm32.slug,
                "standard": "c++17",
                "example": example.name,
                "pass": result.success,
                "error": result.error if not result.success else None,
                "skipped": False,
            })

        report = generate_markdown_report(
            {"name": meta.name, "version": meta.version}, results
        )
        assert "test-library" in report
        assert "stm32-nucleo-f411re" in report
        assert "PASS" in report
        assert "blink" in report
        assert "types_demo" in report

    def test_json_report(self, stm32, tmp_path):
        meta = parse_metadata(TEST_LIBRARY)
        results = [{
            "platform": stm32.slug,
            "standard": "c++17",
            "example": "blink",
            "pass": True,
            "error": None,
            "skipped": False,
        }]
        report = generate_json_report(
            {"name": meta.name, "version": meta.version}, results
        )
        assert report["library"]["name"] == "test-library"
        assert len(report["results"]) == 1
        assert report["summary"]["stm32-nucleo-f411re"]["passing"] == 1
