import json
from pathlib import Path
from compat_check.library.metadata import LibraryMetadata, parse_metadata, discover_examples

def test_parse_library_json(tmp_path):
    (tmp_path / "library.json").write_text(json.dumps({
        "name": "my-lib", "version": "1.2.3",
        "platforms": ["atmelavr", "espressif32"], "frameworks": ["arduino"],
    }))
    meta = parse_metadata(tmp_path)
    assert meta.name == "my-lib"
    assert meta.version == "1.2.3"
    assert meta.platforms == ["atmelavr", "espressif32"]

def test_parse_library_json_star_platforms(tmp_path):
    (tmp_path / "library.json").write_text(json.dumps({
        "name": "my-lib", "version": "1.0.0", "platforms": "*",
    }))
    meta = parse_metadata(tmp_path)
    assert meta.platforms == ["*"]

def test_parse_library_properties(tmp_path):
    (tmp_path / "library.properties").write_text(
        "name=my-lib\nversion=2.0.0\narchitectures=avr,esp32,stm32\n"
    )
    meta = parse_metadata(tmp_path)
    assert meta.name == "my-lib"
    assert meta.version == "2.0.0"
    assert meta.platforms == ["avr", "esp32", "stm32"]

def test_parse_library_properties_star(tmp_path):
    (tmp_path / "library.properties").write_text(
        "name=my-lib\nversion=1.0.0\narchitectures=*\n"
    )
    meta = parse_metadata(tmp_path)
    assert meta.platforms == ["*"]

def test_parse_prefers_library_json(tmp_path):
    (tmp_path / "library.json").write_text(json.dumps({
        "name": "from-json", "version": "1.0.0", "platforms": "*",
    }))
    (tmp_path / "library.properties").write_text("name=from-props\nversion=2.0.0\n")
    meta = parse_metadata(tmp_path)
    assert meta.name == "from-json"

def test_discover_examples_cpp_files(tmp_path):
    ex = tmp_path / "examples"
    ex.mkdir()
    (ex / "basic.cpp").write_text("int main() {}")
    (ex / "advanced.cpp").write_text("int main() {}")
    examples = discover_examples(tmp_path)
    names = {e.name for e in examples}
    assert names == {"basic", "advanced"}

def test_discover_examples_ino_in_subdirs(tmp_path):
    ex = tmp_path / "examples" / "blink"
    ex.mkdir(parents=True)
    (ex / "blink.ino").write_text("void setup() {} void loop() {}")
    examples = discover_examples(tmp_path)
    assert len(examples) == 1
    assert examples[0].name == "blink"

def test_discover_examples_nested_dirs(tmp_path):
    ex = tmp_path / "examples" / "arduino" / "i2c_basic"
    ex.mkdir(parents=True)
    (ex / "i2c_basic.ino").write_text("void setup() {}")
    examples = discover_examples(tmp_path)
    assert len(examples) == 1
    assert examples[0].name == "arduino/i2c_basic"

def test_discover_examples_empty(tmp_path):
    examples = discover_examples(tmp_path)
    assert examples == []


def test_parse_metadata_missing_files(tmp_path):
    """No library.json or library.properties → FileNotFoundError."""
    import pytest
    with pytest.raises(FileNotFoundError, match="No library.json"):
        parse_metadata(tmp_path)


def test_parse_library_json_missing_name(tmp_path):
    """library.json with no name field → defaults to 'unknown'."""
    (tmp_path / "library.json").write_text('{"version": "1.0.0"}')
    meta = parse_metadata(tmp_path)
    assert meta.name == "unknown"


def test_parse_library_json_missing_platforms(tmp_path):
    """library.json with no platforms field → defaults to wildcard."""
    (tmp_path / "library.json").write_text('{"name": "test", "version": "1.0.0"}')
    meta = parse_metadata(tmp_path)
    assert meta.platforms == ["*"]


def test_discover_examples_no_examples_dir(tmp_path):
    """Library with metadata but no examples/ directory."""
    (tmp_path / "library.json").write_text('{"name": "test", "version": "1.0.0"}')
    examples = discover_examples(tmp_path)
    assert examples == []


def test_discover_examples_skips_pio_project(tmp_path):
    """Subdirectories with platformio.ini are skipped (not examples)."""
    ex = tmp_path / "examples" / "test_project"
    ex.mkdir(parents=True)
    (ex / "platformio.ini").write_text("[env:test]")
    (ex / "main.cpp").write_text("int main() {}")
    examples = discover_examples(tmp_path)
    assert examples == []
