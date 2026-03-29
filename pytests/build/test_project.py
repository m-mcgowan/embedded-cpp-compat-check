from pathlib import Path

from compat_check.build.project import generate_pio_project, wrap_for_arduino
from compat_check.platform.models import Platform


def _test_platform():
    return Platform(
        name="Test Board", slug="test-board", version="1.0.0",
        architecture="xtensa", mcu="esp32s3", build_system="platformio",
        standards=["c++17"], framework="arduino",
        platformio={"platform": "espressif32", "board": "esp32-s3-devkitm-1", "framework": "arduino"},
    )


def test_generate_pio_project_creates_ini(tmp_path):
    src = tmp_path / "test.cpp"
    src.write_text("int main() { return 0; }")
    project_dir = tmp_path / "project"
    generate_pio_project(output_dir=project_dir, platform=_test_platform(), standard="c++17", source_file=src)
    ini = project_dir / "platformio.ini"
    assert ini.exists()
    content = ini.read_text()
    assert "esp32-s3-devkitm-1" in content
    assert "-std=gnu++17" in content


def test_generate_pio_project_unflags_default_std(tmp_path):
    src = tmp_path / "test.cpp"
    src.write_text("int main() { return 0; }")
    project_dir = tmp_path / "project"
    generate_pio_project(output_dir=project_dir, platform=_test_platform(), standard="c++17", source_file=src)
    content = (project_dir / "platformio.ini").read_text()
    assert "build_unflags" in content


def test_generate_pio_project_copies_source(tmp_path):
    src = tmp_path / "original.cpp"
    src.write_text("int main() { return 0; }")
    project_dir = tmp_path / "project"
    generate_pio_project(output_dir=project_dir, platform=_test_platform(), standard="c++17", source_file=src)
    main_cpp = project_dir / "src" / "main.cpp"
    assert main_cpp.exists()
    assert "int main()" in main_cpp.read_text()


def test_wrap_for_arduino_adds_header():
    source = 'int main() { return 0; }'
    wrapped = wrap_for_arduino(source)
    assert '#include <Arduino.h>' in wrapped


def test_wrap_for_arduino_replaces_main_with_setup():
    source = 'int main() { return 0; }'
    wrapped = wrap_for_arduino(source)
    assert 'void setup()' in wrapped
    assert 'int main()' not in wrapped


def test_wrap_for_arduino_adds_loop():
    source = 'int main() { return 0; }'
    wrapped = wrap_for_arduino(source)
    assert 'void loop()' in wrapped


def test_wrap_for_arduino_handles_trailing_return():
    source = 'auto main() -> int {\n    return 42;\n}'
    wrapped = wrap_for_arduino(source)
    assert 'void setup()' in wrapped
    assert 'return 42' not in wrapped
