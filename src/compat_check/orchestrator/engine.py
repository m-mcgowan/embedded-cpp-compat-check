"""Main orchestration engine — ties together probe, build, and results."""

import hashlib
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import json

from compat_check.build.compiler import (
    extract_compiler_config, extract_linker_config,
    compile_test, link_test,
)
from compat_check.build.project import generate_pio_project, wrap_for_arduino
from compat_check.build.runner import run_build, run_build_verbose
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

        # Stage 1: Macro probe (PIO verbose build)
        probe_source = generate_probe_source(self.features)
        probe_hash = hashlib.sha256(probe_source.encode()).hexdigest()[:12]

        probe_dir = self.work_dir / platform.slug / standard / "probe"
        probe_file = probe_dir / "probe.cpp"
        probe_dir.mkdir(parents=True, exist_ok=True)
        probe_file.write_text(probe_source)

        project_dir = self.work_dir / platform.slug / standard / "probe_project"
        # Don't use custom core_dir — we need PIO to resolve real package
        # paths in verbose output for direct compiler invocation.
        core_dir = None

        generate_pio_project(project_dir, platform, standard, probe_file)

        if dry_run:
            return []

        # Delete cached main.cpp.o so PIO recompiles it and shows the compiler
        # command in verbose output (needed to extract compiler/linker config).
        # Framework objects are preserved for fast incremental builds.
        for obj in (project_dir / ".pio" / "build").glob("*/src/main.cpp.o"):
            obj.unlink(missing_ok=True)
        # Also delete firmware.elf to force re-link (needed for linker config)
        for elf in (project_dir / ".pio" / "build").glob("*/firmware.*"):
            elf.unlink(missing_ok=True)

        probe_result, verbose_output = run_build_verbose(project_dir, core_dir=core_dir)
        macro_values = {}
        compiler_config = None
        linker_config = None
        if probe_result.success:
            raw = extract_probe_strings(project_dir)
            macro_values = parse_probe_output(raw)
            try:
                compiler_config = extract_compiler_config(verbose_output)
                # Ensure the -std flag is present (PIO's unflag/flag
                # mechanism can strip it from the actual compiler command)
                std_flag = f'-std=gnu++{standard.replace("c++", "")}'
                if not any('std=' in f for f in compiler_config.flags):
                    compiler_config.flags.append(std_flag)
                linker_config = extract_linker_config(verbose_output)
                # Resolve relative paths in linker config to absolute
                # (PIO outputs paths relative to its project dir)
                linker_config.objects = [
                    str(project_dir / obj) if not Path(obj).is_absolute() else obj
                    for obj in linker_config.objects
                ]
                if linker_config.probe_main_obj and not Path(linker_config.probe_main_obj).is_absolute():
                    linker_config.probe_main_obj = str(project_dir / linker_config.probe_main_obj)
                linker_config.scripts = [
                    str(project_dir / s) if not Path(s).is_absolute() else s
                    for s in linker_config.scripts
                ]
                # Resolve relative -L paths in flags
                linker_config.flags = [
                    f'-L{project_dir / flag[2:]}' if flag.startswith('-L') and not Path(flag[2:]).is_absolute() else flag
                    for flag in linker_config.flags
                ]
            except ValueError:
                compiler_config = None
                linker_config = None

        # Determine which tests need building
        std_prefix = standard.replace("c++", "cpp")
        test_files = sorted(self.test_dir.glob(f"{std_prefix}/*.cpp"))
        tests_to_build = []
        for test_file in test_files:
            meta = _parse_test_metadata(test_file)
            feature_key = f"{test_file.parent.name}/{test_file.stem}"
            test_hash = _file_hash(test_file)
            if manifest.needs_rebuild(
                platform.slug, platform.version, probe_hash, feature_key, test_hash
            ):
                tests_to_build.append((test_file, meta, feature_key, test_hash))

        if not tests_to_build:
            probe_pio = project_dir / ".pio"
            if probe_pio.exists():
                shutil.rmtree(probe_pio)
            return []

        # Stage 2: Fast compile (direct compiler or fallback to PIO)
        obj_dir = self.work_dir / platform.slug / standard / "objs"
        obj_dir.mkdir(parents=True, exist_ok=True)

        compile_results = {}  # feature_key -> (success, error, obj_path)
        for test_file, meta, feature_key, test_hash in tests_to_build:
            source_content = test_file.read_text()
            if platform.framework == "arduino":
                source_content = wrap_for_arduino(source_content)

            wrapped_path = obj_dir / f"{test_file.stem}.cpp"
            wrapped_path.write_text(source_content)
            obj_path = obj_dir / f"{test_file.stem}.o"

            if compiler_config:
                success, error = compile_test(compiler_config, wrapped_path, obj_path)
            else:
                # Fallback: use PIO per-test (slow path)
                test_project_dir = self.work_dir / platform.slug / standard / "test_project"
                generate_pio_project(test_project_dir, platform, standard, test_file)
                fallback_result = run_build(test_project_dir, core_dir=core_dir)
                success = fallback_result.success
                error = fallback_result.error

            compile_results[feature_key] = (success, error, obj_path)

        # Stage 3: Verification link (only for tests that compiled)
        # Link verification is informational — compile success is the
        # primary signal. Complex linker setups (RP2040, ESP32) can fail
        # to link even when compilation succeeds, due to platform-specific
        # libraries and boot code we don't fully capture.
        for test_file, meta, feature_key, test_hash in tests_to_build:
            compiled, compile_error, obj_path = compile_results[feature_key]
            macro_name = meta.get("macro", "")
            macro_val = macro_values.get(macro_name, 0)

            link_failure = False
            if compiled and linker_config:
                link_ok, link_error = link_test(linker_config, obj_path)
                if not link_ok:
                    link_failure = True

            status = classify_feature(macro_val, compiled)

            result = {
                "platform": platform.slug,
                "platform_version": platform.version,
                "standard": standard,
                "feature": feature_key,
                "macro": macro_name,
                "category": meta.get("category", "unknown"),
                "macro_value": macro_val,
                "compiles": compiled,
                "status": status.value,
                "compile_time_ms": 0,
                "compiler": compiler_config.compiler if compiler_config else "",
                "timestamp": datetime.now().isoformat(),
                "error_output": compile_error if not compiled else None,
                "link_failure": link_failure,
            }
            results.append(result)

            manifest.record(
                platform.slug, platform.version, probe_hash,
                feature_key, test_hash, status.value
            )

        # Cleanup
        probe_pio = project_dir / ".pio"
        if probe_pio.exists():
            shutil.rmtree(probe_pio)
        if obj_dir.exists():
            shutil.rmtree(obj_dir)

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
