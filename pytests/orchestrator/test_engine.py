from pathlib import Path
from unittest.mock import patch

from compat_check.orchestrator.engine import Orchestrator
from compat_check.platform.models import Platform
from compat_check.catalog.models import Feature, FeatureKind
from compat_check.build.runner import BuildResult


def _platform():
    return Platform(
        name="Test", slug="test-board", version="1.0.0",
        architecture="test",
        mcu="test", build_system="platformio", standards=["c++17"],
        framework="arduino",
        platformio={"platform": "test", "board": "test", "framework": "arduino"},
    )


def _features():
    return [
        Feature(
            name="__cpp_structured_bindings",
            kind=FeatureKind.LANGUAGE, standard="cpp17",
            description="Structured bindings", values=[201606],
        ),
    ]


def test_orchestrator_runs_probe_and_tests(tmp_path):
    orch = Orchestrator(
        platforms=[_platform()],
        features=_features(),
        test_dir=tmp_path / "tests",
        results_dir=tmp_path / "results",
        work_dir=tmp_path / "work",
        max_parallel=1,
    )

    # Create a test file
    cpp17_dir = tmp_path / "tests" / "cpp17"
    cpp17_dir.mkdir(parents=True)
    (cpp17_dir / "structured_bindings.cpp").write_text(
        "// feature: structured_bindings\n"
        "// macro: __cpp_structured_bindings\n"
        "// standard: cpp17\n"
        "// category: language\n"
        "// description: test\n"
        "auto main() -> int { auto [a, b] = (int[]){1,2}; return 0; }\n"
    )

    mock_probe_build = BuildResult(success=True, compile_time_ms=100, output="", error="")
    probe_output = "__cpp_structured_bindings=201606\n__SENTINEL__=-1\n"
    mock_verbose = ""

    # Mock batch build: the test compiled successfully
    mock_batch_results = {
        "cpp17/structured_bindings": BuildResult(
            success=True, compile_time_ms=50, output="", error="",
        ),
    }

    with patch("compat_check.orchestrator.engine.run_build_verbose",
               return_value=(mock_probe_build, mock_verbose)), \
         patch("compat_check.orchestrator.engine.run_batch_build",
               return_value=mock_batch_results), \
         patch("compat_check.orchestrator.engine.extract_probe_strings",
               return_value=probe_output), \
         patch("compat_check.orchestrator.engine.generate_batch_project",
               return_value={"cpp17/structured_bindings": "cpp17__structured_bindings"}):
        results = orch.run()

    assert len(results) > 0
    assert results[0]["status"] == "supported"
    assert results[0]["platform_version"] == "1.0.0"
