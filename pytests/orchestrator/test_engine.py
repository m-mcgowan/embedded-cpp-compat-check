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

    mock_build = BuildResult(success=True, compile_time_ms=100, output="", error="")
    probe_output = "__cpp_structured_bindings=201606\n__SENTINEL__=-1\n"

    # Verbose output that won't parse -> triggers PIO fallback
    mock_verbose = ""

    with patch("compat_check.orchestrator.engine.run_build_verbose",
               return_value=(mock_build, mock_verbose)), \
         patch("compat_check.orchestrator.engine.run_build",
               return_value=mock_build), \
         patch("compat_check.orchestrator.engine.extract_probe_strings",
               return_value=probe_output):
        results = orch.run()

    assert len(results) > 0
    assert results[0]["status"] == "supported"
    assert results[0]["platform_version"] == "1.0.0"
