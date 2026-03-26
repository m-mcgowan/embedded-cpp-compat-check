import json
from pathlib import Path

from compat_check.orchestrator.manifest import Manifest


def test_manifest_load_empty(tmp_path):
    m = Manifest.load(tmp_path / "manifest.json")
    assert m.builds == {}


def test_manifest_load_existing(tmp_path):
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps({
        "builds": {
            "esp32s3": {
                "platform_version": "1.0",
                "probe_hash": "abc",
                "features": {}
            }
        }
    }))
    m = Manifest.load(path)
    assert "esp32s3" in m.builds


def test_manifest_needs_rebuild_new_platform(tmp_path):
    m = Manifest.load(tmp_path / "manifest.json")
    assert m.needs_rebuild("esp32s3", "1.0", "abc", "cpp17/optional", "def")


def test_manifest_needs_rebuild_version_change(tmp_path):
    m = Manifest.load(tmp_path / "manifest.json")
    m.record("esp32s3", "1.0", "abc", "cpp17/optional", "def", "supported")
    assert m.needs_rebuild("esp32s3", "2.0", "abc", "cpp17/optional", "def")


def test_manifest_no_rebuild_when_current(tmp_path):
    m = Manifest.load(tmp_path / "manifest.json")
    m.record("esp32s3", "1.0", "abc", "cpp17/optional", "def", "supported")
    assert not m.needs_rebuild("esp32s3", "1.0", "abc", "cpp17/optional", "def")


def test_manifest_needs_rebuild_test_hash_change(tmp_path):
    m = Manifest.load(tmp_path / "manifest.json")
    m.record("esp32s3", "1.0", "abc", "cpp17/optional", "def", "supported")
    assert m.needs_rebuild("esp32s3", "1.0", "abc", "cpp17/optional", "xyz")


def test_manifest_save_roundtrip(tmp_path):
    path = tmp_path / "manifest.json"
    m = Manifest.load(path)
    m.record("esp32s3", "1.0", "abc", "cpp17/optional", "def", "supported")
    m.save(path)
    m2 = Manifest.load(path)
    assert not m2.needs_rebuild("esp32s3", "1.0", "abc", "cpp17/optional", "def")
