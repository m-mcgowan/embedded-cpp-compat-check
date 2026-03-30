from pathlib import Path
from unittest.mock import patch, MagicMock
from compat_check.library.builder import BuildResult, run_library_build

def test_run_library_build_constructs_pio_ci_command():
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "SUCCESS"
    mock_result.stderr = ""
    with patch("subprocess.run", return_value=mock_result) as mock_run:
        result = run_library_build(
            library_path=Path("/libs/mylib"),
            example_path=Path("/libs/mylib/examples/basic.cpp"),
            board="uno", standard="c++17",
        )
    assert result.success
    cmd = mock_run.call_args[0][0]
    assert "pio" in cmd[0]
    assert "ci" in cmd
    assert "--board=uno" in cmd
    assert any("mylib" in str(c) for c in cmd)
    assert any("std=gnu++17" in str(c) for c in cmd)

def test_run_library_build_captures_failure():
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stdout = "BUILD OUTPUT"
    mock_result.stderr = "error: something broke"
    with patch("subprocess.run", return_value=mock_result):
        result = run_library_build(
            library_path=Path("/libs/mylib"),
            example_path=Path("/libs/mylib/examples/basic.cpp"),
            board="uno", standard="c++17",
        )
    assert not result.success
    assert "something broke" in result.error

def test_run_library_build_example_directory():
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = ""
    mock_result.stderr = ""
    with patch("subprocess.run", return_value=mock_result) as mock_run:
        run_library_build(
            library_path=Path("/libs/mylib"),
            example_path=Path("/libs/mylib/examples/blink"),
            board="uno", standard="c++17",
        )
    cmd = mock_run.call_args[0][0]
    assert any("blink" in str(c) for c in cmd)
