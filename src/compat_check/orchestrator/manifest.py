"""Build manifest for incremental builds."""

import json
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime


@dataclass
class Manifest:
    builds: dict = field(default_factory=dict)

    @classmethod
    def load(cls, path: Path) -> "Manifest":
        if path.exists():
            data = json.loads(path.read_text())
            return cls(builds=data.get("builds", {}))
        return cls()

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"builds": self.builds}, indent=2) + "\n")

    def needs_rebuild(
        self,
        platform_slug: str,
        platform_version: str,
        probe_hash: str,
        feature_key: str,
        test_hash: str,
    ) -> bool:
        build = self.builds.get(platform_slug)
        if not build:
            return True
        if build.get("platform_version") != platform_version:
            return True
        if build.get("probe_hash") != probe_hash:
            return True
        feat = build.get("features", {}).get(feature_key)
        if not feat:
            return True
        if feat.get("test_hash") != test_hash:
            return True
        return False

    def record(
        self,
        platform_slug: str,
        platform_version: str,
        probe_hash: str,
        feature_key: str,
        test_hash: str,
        status: str,
    ) -> None:
        if platform_slug not in self.builds:
            self.builds[platform_slug] = {
                "platform_version": platform_version,
                "probe_hash": probe_hash,
                "features": {},
            }
        build = self.builds[platform_slug]
        build["platform_version"] = platform_version
        build["probe_hash"] = probe_hash
        build["features"][feature_key] = {
            "test_hash": test_hash,
            "status": status,
            "timestamp": datetime.now().isoformat(),
        }
