"""Parse the SD-6 feature catalog from data.yaml."""
from pathlib import Path
import yaml
from .models import Feature, FeatureKind

def _infer_standard(support: dict | None) -> str:
    """Infer the C++ standard from the 'since' field in support data."""
    if not support:
        return "unknown"
    for compiler_data in support.values():
        if not compiler_data:
            continue
        for entry in compiler_data:
            if "since" in entry:
                return entry["since"].lower().replace("c++", "cpp")
    return "unknown"

def _parse_section(entries: list[dict], kind: FeatureKind) -> list[Feature]:
    features = []
    for entry in entries:
        name = entry["name"]
        if kind != FeatureKind.ATTRIBUTE and not name.startswith("__cpp"):
            name = f"__has_cpp_attribute({name})"
        rows = entry.get("rows", [])
        values = [r["value"] for r in rows]
        description = rows[0].get("cppreference-description", "") if rows else ""
        header_str = entry.get("header_list", "")
        headers = header_str.split() if header_str else []
        standard = _infer_standard(entry.get("support"))
        features.append(Feature(name=name, kind=kind, standard=standard, description=description, values=values, headers=headers))
    return features

def parse_catalog(path: Path) -> list[Feature]:
    """Parse a data.yaml catalog file into a list of Features."""
    with open(path) as f:
        data = yaml.safe_load(f)
    features: list[Feature] = []
    if "language" in data:
        features.extend(_parse_section(data["language"], FeatureKind.LANGUAGE))
    if "library" in data:
        features.extend(_parse_section(data["library"], FeatureKind.LIBRARY))
    if "attributes" in data:
        features.extend(_parse_section(data["attributes"], FeatureKind.ATTRIBUTE))
    return features
