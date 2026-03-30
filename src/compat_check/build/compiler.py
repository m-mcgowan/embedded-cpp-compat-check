"""Direct compiler invocation for fast test compilation and linking."""

import shlex
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CompilerConfig:
    compiler: str
    flags: list[str]
    includes: list[str]


@dataclass
class LinkerConfig:
    linker: str
    flags: list[str]
    objects: list[str]
    scripts: list[str]
    probe_main_obj: str


def _resolve_tool(name: str) -> str:
    """Resolve a compiler/linker name to its absolute path.

    PIO verbose output uses bare names like 'avr-g++' that are on PIO's
    internal PATH but not necessarily on the system PATH. Search
    ~/.platformio/packages/*/bin/ as a fallback.
    """
    if Path(name).is_absolute():
        return name
    found = shutil.which(name)
    if found:
        return found
    for bin_dir in Path.home().glob('.platformio/packages/*/bin'):
        candidate = bin_dir / name
        if candidate.exists():
            return str(candidate)
    return name  # give up, let subprocess raise the error


def extract_compiler_config(verbose_output: str) -> CompilerConfig:
    """Parse the src/main.cpp compilation line from PIO verbose output."""
    for line in verbose_output.splitlines():
        if 'src/main.cpp' not in line or 'main.cpp.o' not in line:
            continue
        if '-c' not in line:
            continue

        tokens = shlex.split(line)
        compiler = tokens[0]
        flags = []
        includes = []

        skip_next = False
        for i, tok in enumerate(tokens[1:], 1):
            if skip_next:
                skip_next = False
                continue
            if tok == '-o':
                skip_next = True
                continue
            if tok == '-c':
                continue
            if tok == 'src/main.cpp':
                continue
            if tok.startswith('-I'):
                inc = tok[2:]
                if inc == 'src':
                    continue
                includes.append(inc)
                continue
            flags.append(tok)

        return CompilerConfig(compiler=_resolve_tool(compiler), flags=flags, includes=includes)

    raise ValueError("Could not find src/main.cpp compilation line in verbose output")


def extract_linker_config(verbose_output: str) -> LinkerConfig:
    """Parse the final link line from PIO verbose output."""
    for line in verbose_output.splitlines():
        if 'firmware.elf' not in line:
            continue
        if '-c' in shlex.split(line):
            continue

        tokens = shlex.split(line)
        linker = tokens[0]
        flags = []
        objects = []
        scripts = []
        probe_main_obj = ''

        skip_next = False
        for i, tok in enumerate(tokens[1:], 1):
            if skip_next:
                skip_next = False
                continue
            if tok == '-o':
                skip_next = True
                continue
            if tok.startswith('-T'):
                scripts.append(tok[2:] if len(tok) > 2 else tokens[i + 1])
                if len(tok) == 2:
                    skip_next = True
                continue
            if tok.endswith('.o') or tok.endswith('.a'):
                if 'src/main.cpp.o' in tok:
                    probe_main_obj = tok
                else:
                    objects.append(tok)
                continue
            flags.append(tok)

        return LinkerConfig(
            linker=_resolve_tool(linker), flags=flags, objects=objects,
            scripts=scripts, probe_main_obj=probe_main_obj,
        )

    raise ValueError("Could not find firmware.elf link line in verbose output")


def compile_test(
    config: CompilerConfig, source_path: Path, output_obj: Path,
    timeout: int = 30,
) -> tuple[bool, str]:
    """Compile a single test file. Returns (success, error_output)."""
    cmd = [
        config.compiler, '-c',
        *config.flags,
        *[f'-I{inc}' for inc in config.includes],
        '-o', str(output_obj),
        str(source_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return result.returncode == 0, result.stderr


def link_test(
    config: LinkerConfig, test_obj: Path,
    timeout: int = 30,
) -> tuple[bool, str]:
    """Link a test object against the framework. Returns (success, error_output)."""
    cmd = [
        config.linker,
        '-o', '/dev/null',
        *config.flags,
        str(test_obj),
        *config.objects,
        *[f'-T{s}' for s in config.scripts],
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return result.returncode == 0, result.stderr
