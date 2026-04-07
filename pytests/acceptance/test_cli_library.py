"""Acceptance test: compat-check library CLI end-to-end.

Tests the full CLI path including registry resolution, report generation,
and summary output. Requires PlatformIO installed.

Run with: pytest pytests/acceptance/test_cli_library.py -v --timeout=600
"""

import subprocess
from pathlib import Path

import pytest

TEST_LIBRARY = Path(__file__).parent.parent / "fixtures" / "test-library"


def _run_cli(*args, timeout=300):
    """Run compat-check library and return (returncode, stdout, stderr)."""
    cmd = ["compat-check", "library", *args]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return result.returncode, result.stdout, result.stderr


class TestCLILocalLibrary:
    """Test the CLI with a local library directory."""

    def test_local_library_produces_report(self, tmp_path):
        report = tmp_path / "report.md"
        rc, stdout, stderr = _run_cli(
            str(TEST_LIBRARY),
            "--platform", "stm32-nucleo-f411re",
            "--report", str(report),
        )
        assert rc == 0, f"CLI failed: {stdout}"
        assert report.exists()
        content = report.read_text()
        assert "test-library" in content
        assert "stm32-nucleo-f411re" in content
        assert "PASS" in content

    def test_local_library_json_report(self, tmp_path):
        report = tmp_path / "report.json"
        rc, stdout, stderr = _run_cli(
            str(TEST_LIBRARY),
            "--platform", "stm32-nucleo-f411re",
            "--report", str(report),
        )
        assert rc == 0, f"CLI failed: {stdout}"
        import json
        data = json.loads(report.read_text())
        assert data["library"]["name"] == "test-library"

    def test_local_library_shows_summary(self):
        rc, stdout, stderr = _run_cli(
            str(TEST_LIBRARY),
            "--platform", "stm32-nucleo-f411re",
        )
        assert rc == 0, f"CLI failed: {stdout}"
        assert "min standard:" in stdout


class TestCLIRegistryLibrary:
    """Test the CLI with a PlatformIO registry library."""

    def test_registry_library_installs_and_tests(self, tmp_path):
        report = tmp_path / "report.md"
        rc, stdout, stderr = _run_cli(
            "ArduinoJson",
            "--platform", "stm32-nucleo-f411re",
            "--example", "JsonParserExample",
            "--report", str(report),
        )
        assert rc == 0, f"CLI failed: {stdout}"
        assert report.exists()
        content = report.read_text()
        assert "ArduinoJson" in content
        assert "PASS" in content

    def test_registry_not_found(self):
        rc, stdout, stderr = _run_cli(
            "NonExistentLibrary12345",
            "--platform", "stm32-nucleo-f411re",
        )
        assert rc != 0
