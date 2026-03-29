"""Main orchestration engine — ties together probe, build, and results."""

import hashlib
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import json

from compat_check.build.project import generate_pio_project
from compat_check.build.runner import run_build, BuildResult
from compat_check.catalog.models import Feature
from compat_check.orchestrator.manifest import Manifest
from compat_check.orchestrator.results import classify_feature
from compat_check.platform.models import Platform
from compat_check.probe.extractor import parse_probe_output
from compat_check.probe.generator import generate_probe_source


def extract_probe_strings(elf_dir: Path) -> str:
    """Run `strings` on compiled firmware to extract probe results."""
    firmware_dir = elf_dir / ".pio" / "build"
    for env_dir in firmware_dir.iterdir() if firmware_dir.exists() else []:
        for ext in ("*.elf", "*.bin"):
            for f in env_dir.glob(ext):
                result = subprocess.run(
                    ["strings", str(f)], capture_output=True, text=True
                )
                lines = [
                    line for line in result.stdout.splitlines()
                    if line.startswith("__cpp") or line.startswith("__has")
                    or line == "__SENTINEL__=-1"
                ]
                if lines:
                    return "\n".join(lines) + "\n"
    return ""


def _file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def _parse_test_metadata(path: Path) -> dict:
    """Parse // key: value metadata from a test file header."""
    meta = {}
    for line in path.read_text().splitlines():
        if not line.startswith("//"):
            break
        line = line.lstrip("/").strip()
        if ": " in line:
            key, _, value = line.partition(": ")
            meta[key.strip()] = value.strip()
    return meta


@dataclass
class Orchestrator:
    platforms: list[Platform]
    features: list[Feature]
    test_dir: Path
    results_dir: Path
    work_dir: Path
    max_parallel: int = 4

    def run(self, dry_run: bool = False) -> list[dict]:
        """Run the full orchestration loop. Returns list of result dicts."""
        all_results = []
        manifest = Manifest.load(self.results_dir / "manifest.json")

        for platform in self.platforms:
            for standard in platform.standards:
                results = self._run_platform_standard(
                    platform, standard, manifest, dry_run
                )
                all_results.extend(results)
                # Save incrementally after each standard so we don't lose
                # progress if the run is interrupted.
                if results and not dry_run:
                    manifest.save(self.results_dir / "manifest.json")
                    self._write_result_files(results)

        return all_results

    def _run_platform_standard(
        self, platform: Platform, standard: str, manifest: Manifest, dry_run: bool
    ) -> list[dict]:
        results = []

        # Stage 1: Macro probe
        probe_source = generate_probe_source(self.features)
        probe_hash = hashlib.sha256(probe_source.encode()).hexdigest()[:12]

        probe_dir = self.work_dir / platform.slug / standard / "probe"
        probe_file = probe_dir / "probe.cpp"
        probe_dir.mkdir(parents=True, exist_ok=True)
        probe_file.write_text(probe_source)

        project_dir = self.work_dir / platform.slug / standard / "probe_project"
        core_dir = self.work_dir / ".pio-cores" / platform.slug

        generate_pio_project(project_dir, platform, standard, probe_file)

        if dry_run:
            return []

        probe_result = run_build(project_dir, core_dir=core_dir)
        macro_values = {}
        if probe_result.success:
            raw = extract_probe_strings(project_dir)
            macro_values = parse_probe_output(raw)

        # Clean up probe build artifacts (keep source for debugging)
        probe_pio = project_dir / ".pio"
        if probe_pio.exists():
            shutil.rmtree(probe_pio)

        # Stage 2: Compile tests — only at their native standard
        # Reuse a single project dir per platform+standard to avoid duplicating
        # the framework build (~2-5GB each). Just swap the source file.
        std_prefix = standard.replace("c++", "cpp")
        test_files = sorted(self.test_dir.glob(f"{std_prefix}/*.cpp"))
        test_project_dir = self.work_dir / platform.slug / standard / "test_project"

        for test_file in test_files:
            meta = _parse_test_metadata(test_file)
            feature_key = f"{test_file.parent.name}/{test_file.stem}"
            test_hash = _file_hash(test_file)
            macro_name = meta.get("macro", "")

            if not manifest.needs_rebuild(
                platform.slug, platform.version, probe_hash, feature_key, test_hash
            ):
                continue

            generate_pio_project(test_project_dir, platform, standard, test_file)
            build_result = run_build(test_project_dir, core_dir=core_dir)

            macro_val = macro_values.get(macro_name, 0)
            status = classify_feature(macro_val, build_result.success)

            result = {
                "platform": platform.slug,
                "platform_version": platform.version,
                "standard": standard,
                "feature": feature_key,
                "macro": macro_name,
                "category": meta.get("category", "unknown"),
                "macro_value": macro_val,
                "compiles": build_result.success,
                "status": status.value,
                "compile_time_ms": build_result.compile_time_ms,
                "compiler": "",
                "timestamp": datetime.now().isoformat(),
                "error_output": build_result.error if not build_result.success else None,
            }
            results.append(result)

            manifest.record(
                platform.slug, platform.version, probe_hash,
                feature_key, test_hash, status.value
            )

        return results

    def _write_result_files(self, results: list[dict]) -> None:
        by_platform_std = defaultdict(list)
        for r in results:
            key = (r["platform"], r["platform_version"], r["standard"])
            by_platform_std[key].append(r)

        for (platform_slug, version, standard), items in by_platform_std.items():
            std_prefix = standard.replace("c++", "cpp")
            out_dir = self.results_dir / platform_slug / version
            out_dir.mkdir(parents=True, exist_ok=True)
            out_file = out_dir / f"{std_prefix}.json"

            # Merge with existing results rather than overwriting
            existing = []
            if out_file.exists():
                existing = json.loads(out_file.read_text())
            existing_by_feature = {r["feature"]: r for r in existing}
            for item in items:
                existing_by_feature[item["feature"]] = item
            merged = sorted(existing_by_feature.values(), key=lambda r: r["feature"])
            out_file.write_text(json.dumps(merged, indent=2) + "\n")
