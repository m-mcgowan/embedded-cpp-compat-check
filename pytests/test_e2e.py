"""End-to-end smoke test with mocked PlatformIO builds."""

import json
from pathlib import Path
from unittest.mock import patch

from compat_check.build.runner import BuildResult
from compat_check.catalog.parser import parse_catalog
from compat_check.orchestrator.engine import Orchestrator
from compat_check.platform.loader import load_platform


FIXTURES = Path(__file__).parent / "catalog" / "fixtures"


def test_e2e_pipeline(tmp_path):
    """Full pipeline: catalog -> probe -> compile -> results -> summary."""
    features = parse_catalog(FIXTURES / "small_catalog.yaml")

    platform_yaml = tmp_path / "platform.yaml"
    platform_yaml.write_text(
        "name: Test Board\n"
        "slug: test-board\n"
        "version: '1.0.0'\n"
        "architecture: test\n"
        "mcu: test\n"
        "build_system: platformio\n"
        "framework: arduino\n"
        "platformio:\n"
        "  platform: test\n"
        "  board: test\n"
        "  framework: arduino\n"
        "standards: [c++17]\n"
    )
    platform = load_platform(platform_yaml)

    # Create a test file
    test_dir = tmp_path / "tests" / "cpp17"
    test_dir.mkdir(parents=True)
    (test_dir / "structured_bindings.cpp").write_text(
        "// feature: structured_bindings\n"
        "// macro: __cpp_structured_bindings\n"
        "// standard: cpp17\n"
        "// category: language\n"
        "// description: test\n"
        "auto main() -> int { return 0; }\n"
    )

    orch = Orchestrator(
        platforms=[platform],
        features=features,
        test_dir=tmp_path / "tests",
        results_dir=tmp_path / "results",
        work_dir=tmp_path / "work",
        max_parallel=1,
    )

    mock_build = BuildResult(success=True, compile_time_ms=50, output="", error="")
    probe_strings = "__cpp_structured_bindings=201606\n__SENTINEL__=-1\n"

    with patch("compat_check.orchestrator.engine.run_build", return_value=mock_build), \
         patch("compat_check.orchestrator.engine.extract_probe_strings", return_value=probe_strings):
        results = orch.run()

    # Verify results
    assert len(results) >= 1
    structured = [r for r in results if "structured_bindings" in r["feature"]]
    assert len(structured) == 1
    assert structured[0]["status"] == "supported"
    assert structured[0]["macro_value"] == 201606

    # Verify manifest was written
    manifest_path = tmp_path / "results" / "manifest.json"
    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text())
    assert "test-board" in manifest["builds"]

    # Verify summary table can be generated
    from compat_check.site.readme import generate_summary_table
    table = generate_summary_table(results)
    assert "test-board" in table
