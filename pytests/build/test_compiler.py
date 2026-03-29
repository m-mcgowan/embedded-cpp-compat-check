from pathlib import Path
from unittest.mock import patch, MagicMock

from compat_check.build.compiler import (
    CompilerConfig, LinkerConfig,
    extract_compiler_config, extract_linker_config,
    compile_test, link_test,
)


# Real verbose output snippet from AVR build
AVR_VERBOSE = (
    'avr-g++ -o .pio/build/test/src/main.cpp.o -c '
    '-fno-exceptions -fno-threadsafe-statics -fpermissive '
    '-mmcu=atmega328p -Os -Wall -ffunction-sections -fdata-sections -flto '
    '-DPLATFORMIO=60118 -DARDUINO_AVR_UNO -DF_CPU=16000000L '
    '-DARDUINO_ARCH_AVR -DARDUINO=10808 '
    '-Isrc '
    '-I/Users/mat/.platformio/packages/framework-arduino-avr/cores/arduino '
    '-I/Users/mat/.platformio/packages/framework-arduino-avr/variants/standard '
    'src/main.cpp\n'
    'avr-g++ -o .pio/build/test/FrameworkArduino/CDC.cpp.o -c '
    '-fno-exceptions src/CDC.cpp\n'
)


def test_extract_compiler_config_finds_compiler():
    config = extract_compiler_config(AVR_VERBOSE)
    assert config.compiler == 'avr-g++'


def test_extract_compiler_config_extracts_flags():
    config = extract_compiler_config(AVR_VERBOSE)
    assert '-fno-exceptions' in config.flags
    assert '-mmcu=atmega328p' in config.flags
    assert '-DARDUINO_AVR_UNO' in config.flags


def test_extract_compiler_config_extracts_includes():
    config = extract_compiler_config(AVR_VERBOSE)
    assert any('cores/arduino' in inc for inc in config.includes)
    assert any('variants/standard' in inc for inc in config.includes)


def test_extract_compiler_config_excludes_output_and_source():
    config = extract_compiler_config(AVR_VERBOSE)
    assert '-o' not in config.flags
    assert 'main.cpp.o' not in ' '.join(config.flags)
    assert '-c' not in config.flags
    assert 'src/main.cpp' not in config.flags


def test_extract_compiler_config_excludes_isrc():
    config = extract_compiler_config(AVR_VERBOSE)
    assert '-Isrc' not in config.includes
    assert 'src' not in config.includes


# --- Task 4: Linker config ---

AVR_LINK_VERBOSE = (
    'avr-g++ -o .pio/build/test/firmware.elf '
    '-Os -mmcu=atmega328p -Wl,--gc-sections -flto '
    '.pio/build/test/src/main.cpp.o '
    '.pio/build/test/FrameworkArduino/CDC.cpp.o '
    '.pio/build/test/FrameworkArduino/HardwareSerial.cpp.o '
    '-L.pio/build/test '
    '-Wl,--start-group -lm -Wl,--end-group\n'
)


def test_extract_linker_config_finds_linker():
    config = extract_linker_config(AVR_LINK_VERBOSE)
    assert config.linker == 'avr-g++'


def test_extract_linker_config_finds_probe_main_obj():
    config = extract_linker_config(AVR_LINK_VERBOSE)
    assert config.probe_main_obj == '.pio/build/test/src/main.cpp.o'


def test_extract_linker_config_collects_framework_objects():
    config = extract_linker_config(AVR_LINK_VERBOSE)
    assert any('CDC.cpp.o' in obj for obj in config.objects)
    assert any('HardwareSerial.cpp.o' in obj for obj in config.objects)


def test_extract_linker_config_collects_flags():
    config = extract_linker_config(AVR_LINK_VERBOSE)
    assert '-mmcu=atmega328p' in config.flags


def test_extract_linker_config_excludes_output():
    config = extract_linker_config(AVR_LINK_VERBOSE)
    assert 'firmware.elf' not in ' '.join(config.flags)
    assert 'firmware.elf' not in ' '.join(config.objects)


# --- Task 5: compile_test and link_test ---

def test_compile_test_invokes_compiler():
    config = CompilerConfig(
        compiler='/usr/bin/avr-g++',
        flags=['-mmcu=atmega328p', '-Os'],
        includes=['/path/to/arduino/cores'],
    )
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stderr = ''
    with patch('subprocess.run', return_value=mock_result) as mock_run:
        success, error = compile_test(config, Path('/tmp/test.cpp'), Path('/tmp/test.o'))
    assert success
    assert error == ''
    cmd = mock_run.call_args[0][0]
    assert cmd[0] == '/usr/bin/avr-g++'
    assert '-c' in cmd
    assert '-mmcu=atmega328p' in cmd
    assert '-I/path/to/arduino/cores' in cmd
    assert '/tmp/test.cpp' in cmd
    assert '-o' in cmd


def test_compile_test_returns_false_on_failure():
    config = CompilerConfig(compiler='/usr/bin/avr-g++', flags=[], includes=[])
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stderr = 'error: missing header'
    with patch('subprocess.run', return_value=mock_result):
        success, error = compile_test(config, Path('/tmp/test.cpp'), Path('/tmp/test.o'))
    assert not success
    assert 'missing header' in error


def test_link_test_substitutes_obj():
    config = LinkerConfig(
        linker='/usr/bin/avr-g++',
        flags=['-mmcu=atmega328p'],
        objects=['/path/to/CDC.o', '/path/to/Serial.o'],
        scripts=[],
        probe_main_obj='/path/to/src/main.cpp.o',
    )
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stderr = ''
    with patch('subprocess.run', return_value=mock_result) as mock_run:
        success, error = link_test(config, Path('/tmp/test.o'))
    assert success
    cmd = mock_run.call_args[0][0]
    assert '/tmp/test.o' in cmd
    assert '/path/to/src/main.cpp.o' not in cmd
    assert '/path/to/CDC.o' in cmd


def test_link_test_returns_false_on_failure():
    config = LinkerConfig(
        linker='/usr/bin/avr-g++', flags=[], objects=[],
        scripts=[], probe_main_obj='',
    )
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stderr = 'undefined reference to `foo`'
    with patch('subprocess.run', return_value=mock_result):
        success, error = link_test(config, Path('/tmp/test.o'))
    assert not success
    assert 'undefined reference' in error
