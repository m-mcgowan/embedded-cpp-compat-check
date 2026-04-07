"""Acceptance test: compat-check run against a real platform.

Requires PlatformIO installed and STM32 toolchain available.
Run with: pytest pytests/acceptance/ -v --timeout=300
"""

import json
from pathlib import Path

import pytest

from compat_check.catalog.parser import parse_catalog
from compat_check.orchestrator.engine import Orchestrator
from compat_check.platform.loader import load_platforms

CATALOG = Path(__file__).parent.parent.parent / "catalog" / "data.yaml"
TESTS_DIR = Path(__file__).parent.parent.parent / "tests"
PLATFORMS_DIR = Path(__file__).parent.parent.parent / "platforms"


@pytest.fixture
def platforms():
    return load_platforms(PLATFORMS_DIR)


@pytest.fixture
def stm32(platforms):
    from dataclasses import replace
    matches = [p for p in platforms if p.slug == "stm32-nucleo-f411re"]
    if not matches:
        pytest.skip("stm32-nucleo-f411re platform not found")
    # Only test c++17 to keep it fast
    return replace(matches[0], standards=["c++17"])


class TestFeatureCheck:
    """Acceptance tests that run real PIO probe + batch builds."""

    def test_single_platform_produces_results(self, stm32, tmp_path):
        """Run a real sweep on STM32 at c++17 and verify results structure."""
        features = parse_catalog(CATALOG)

        orch = Orchestrator(
            platforms=[stm32],
            features=features,
            test_dir=TESTS_DIR,
            results_dir=tmp_path / "results",
            work_dir=tmp_path / "work",
        )
        results = orch.run()

        # Should have results for all cpp17 tests
        assert len(results) > 50

        # Check result structure
        r = results[0]
        assert "platform" in r
        assert "standard" in r
        assert "feature" in r
        assert "status" in r
        assert "compiles" in r
        assert "macro_value" in r
        assert r["platform"] == "stm32-nucleo-f411re"
        assert r["standard"] == "c++17"

    def test_results_have_valid_statuses(self, stm32, tmp_path):
        """All results have one of the 4 expected status values."""
        features = parse_catalog(CATALOG)

        orch = Orchestrator(
            platforms=[stm32],
            features=features,
            test_dir=TESTS_DIR,
            results_dir=tmp_path / "results",
            work_dir=tmp_path / "work",
        )
        results = orch.run()

        valid = {"supported", "unsupported", "macro_lies", "unreported"}
        for r in results:
            assert r["status"] in valid, f"{r['feature']}: unexpected status {r['status']}"

    def test_results_written_to_disk(self, stm32, tmp_path):
        """Results are persisted as JSON files."""
        features = parse_catalog(CATALOG)

        orch = Orchestrator(
            platforms=[stm32],
            features=features,
            test_dir=TESTS_DIR,
            results_dir=tmp_path / "results",
            work_dir=tmp_path / "work",
        )
        orch.run()

        result_file = tmp_path / "results" / "stm32-nucleo-f411re" / stm32.version / "cpp17.json"
        assert result_file.exists()
        data = json.loads(result_file.read_text())
        assert len(data) > 50

    def test_manifest_tracks_builds(self, stm32, tmp_path):
        """Manifest is created and tracks the build."""
        features = parse_catalog(CATALOG)

        orch = Orchestrator(
            platforms=[stm32],
            features=features,
            test_dir=TESTS_DIR,
            results_dir=tmp_path / "results",
            work_dir=tmp_path / "work",
        )
        orch.run()

        manifest = json.loads((tmp_path / "results" / "manifest.json").read_text())
        assert "stm32-nucleo-f411re" in manifest["builds"]


class TestSiteGeneration:
    """Test that generate produces valid output from real results."""

    def test_generate_site_from_results(self, stm32, tmp_path):
        features = parse_catalog(CATALOG)

        orch = Orchestrator(
            platforms=[stm32],
            features=features,
            test_dir=TESTS_DIR,
            results_dir=tmp_path / "results",
            work_dir=tmp_path / "work",
        )
        orch.run()

        from compat_check.site.html import generate_site
        from compat_check.site.readme import generate_summary_table

        # Load results back from disk
        import glob as glob_mod
        all_results = []
        for f in glob_mod.glob(f"{tmp_path / 'results'}/**/*.json", recursive=True):
            if "manifest" in f:
                continue
            with open(f) as fh:
                all_results.extend(json.load(fh))

        platform_meta = {stm32.slug: stm32}
        site_dir = tmp_path / "site"
        generate_site(all_results, site_dir, platform_meta)

        assert (site_dir / "index.html").exists()
        assert (site_dir / "stm32-nucleo-f411re" / "index.html").exists()

        index_html = (site_dir / "index.html").read_text()
        assert "stm32-nucleo-f411re" in index_html
        assert "c++17" in index_html

        table = generate_summary_table(all_results, platform_meta)
        assert "STM32" in table
        assert "97%" in table or "%" in table  # some percentage shown
