"""Parse PlatformIO library metadata and discover examples."""
import json
from dataclasses import dataclass
from pathlib import Path

@dataclass
class LibraryMetadata:
    name: str
    version: str
    platforms: list[str]
    path: Path

@dataclass
class Example:
    name: str
    path: Path

def parse_metadata(library_path: Path) -> LibraryMetadata:
    json_path = library_path / "library.json"
    props_path = library_path / "library.properties"
    if json_path.exists():
        return _parse_library_json(json_path, library_path)
    if props_path.exists():
        return _parse_library_properties(props_path, library_path)
    raise FileNotFoundError(f"No library.json or library.properties found in {library_path}")

def _parse_library_json(path: Path, library_path: Path) -> LibraryMetadata:
    data = json.loads(path.read_text())
    platforms = data.get("platforms", "*")
    if isinstance(platforms, str):
        platforms = [platforms]
    return LibraryMetadata(
        name=data.get("name", "unknown"), version=data.get("version", "0.0.0"),
        platforms=platforms, path=library_path,
    )

def _parse_library_properties(path: Path, library_path: Path) -> LibraryMetadata:
    props = {}
    for line in path.read_text().splitlines():
        if "=" in line:
            key, _, value = line.partition("=")
            props[key.strip()] = value.strip()
    architectures = props.get("architectures", "*")
    if architectures == "*":
        platforms = ["*"]
    else:
        platforms = [a.strip() for a in architectures.split(",")]
    return LibraryMetadata(
        name=props.get("name", "unknown"), version=props.get("version", "0.0.0"),
        platforms=platforms, path=library_path,
    )

def discover_examples(library_path: Path) -> list[Example]:
    examples_dir = library_path / "examples"
    if not examples_dir.exists():
        return []
    examples = []
    _scan_examples_dir(examples_dir, examples_dir, examples)
    return sorted(examples, key=lambda e: e.name)

def _scan_examples_dir(base: Path, current: Path, results: list[Example]) -> None:
    cpp_files = list(current.glob("*.cpp"))
    ino_files = list(current.glob("*.ino"))
    if ino_files:
        name = str(current.relative_to(base))
        if name == ".":
            name = current.name
        results.append(Example(name=name, path=current))
        return
    if cpp_files and current == base:
        for cpp in cpp_files:
            results.append(Example(name=cpp.stem, path=cpp))
        for subdir in sorted(current.iterdir()):
            if subdir.is_dir():
                _scan_examples_dir(base, subdir, results)
    elif cpp_files and current != base:
        name = str(current.relative_to(base))
        results.append(Example(name=name, path=current))
    else:
        for subdir in sorted(current.iterdir()):
            if subdir.is_dir():
                _scan_examples_dir(base, subdir, results)
