from unittest.mock import patch, MagicMock
from pathlib import Path

from compat_check.build.runner import run_build, run_build_verbose, BuildResult


def test_build_result_pass():
    r = BuildResult(success=True, compile_time_ms=1234, output="", error="")
    assert r.success
    assert r.compile_time_ms == 1234


def test_build_result_fail():
    r = BuildResult(success=False, compile_time_ms=500, output="", error="error: ...")
    assert not r.success


def test_run_build_calls_platformio(tmp_path):
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    (project_dir / "platformio.ini").write_text("[env:test]\n")

    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "SUCCESS"
    mock_result.stderr = ""

    with patch("subprocess.run", return_value=mock_result) as mock_run:
        result = run_build(project_dir, core_dir=tmp_path / "core")

    assert result.success
    cmd = mock_run.call_args[0][0]
    assert "pio" in cmd[0]


def test_run_build_sets_core_dir_env(tmp_path):
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    (project_dir / "platformio.ini").write_text("[env:test]\n")

    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = ""
    mock_result.stderr = ""

    with patch("subprocess.run", return_value=mock_result) as mock_run:
        run_build(project_dir, core_dir=tmp_path / "core")

    env = mock_run.call_args[1].get("env", {})
    assert env.get("PLATFORMIO_CORE_DIR") == str(tmp_path / "core")


def test_run_build_verbose_passes_v_flag(tmp_path):
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    (project_dir / "platformio.ini").write_text("[env:test]\n")

    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "VERBOSE OUTPUT"
    mock_result.stderr = ""

    with patch("subprocess.run", return_value=mock_result) as mock_run:
        build_result, verbose = run_build_verbose(project_dir)

    cmd = mock_run.call_args[0][0]
    assert "-v" in cmd
    assert verbose == "VERBOSE OUTPUT"
    assert build_result.success


def test_run_build_verbose_returns_output_on_failure(tmp_path):
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    (project_dir / "platformio.ini").write_text("[env:test]\n")

    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stdout = "VERBOSE FAIL"
    mock_result.stderr = "error details"

    with patch("subprocess.run", return_value=mock_result):
        build_result, verbose = run_build_verbose(project_dir)

    assert not build_result.success
    assert verbose == "VERBOSE FAIL"
