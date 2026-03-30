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


def _resolve_tool(name: str, verbose_output: str = "") -> str:
    """Resolve a compiler/linker name to its absolute path.

    PIO verbose output uses bare names like 'avr-g++' that are on PIO's
    internal PATH but not necessarily on the system PATH. We parse the
    verbose output to find the exact toolchain PIO is using.
    """
    if Path(name).is_absolute():
        return name

    # Extract toolchain info from PIO verbose output
    # Format: "- toolchain-name @ version (file:///path)" or
    #         "- toolchain-name @ version (1.2.3)"
    pio_home = Path.home() / '.platformio'
    for line in verbose_output.splitlines():
        if 'toolchain' not in line.lower():
            continue
        # Try file:// path first (some platforms use custom locations)
        if 'file://' in line:
            start = line.index('file://') + 7
            end = line.index(')', start) if ')' in line[start:] else len(line)
            candidate = Path(line[start:end]) / 'bin' / name
            if candidate.exists():
                return str(candidate)
        # Parse "- toolchain-name @ version" and look in packages/tools
        line_stripped = line.strip().lstrip('- ')
        if '@' in line_stripped:
            pkg_name = line_stripped.split('@')[0].strip()
            for search_dir in [pio_home / 'packages', pio_home / 'tools']:
                # Try exact match first, then versioned directories
                candidate = search_dir / pkg_name / 'bin' / name
                if candidate.exists():
                    return str(candidate)
                # Try versioned: toolchain-name@version
                for d in sorted(search_dir.glob(f'{pkg_name}@*'), reverse=True):
                    candidate = d / 'bin' / name
                    if candidate.exists():
                        return str(candidate)

    # Fall back to PIO packages and tools directories (newest first)
    for pattern in ['.platformio/packages/*/bin', '.platformio/tools/*/bin']:
        for bin_dir in sorted(Path.home().glob(pattern), reverse=True):
            candidate = bin_dir / name
            if candidate.exists():
                return str(candidate)

    found = shutil.which(name)
    if found:
        return found

    return name  # give up, let subprocess raise the error


def extract_compiler_config(verbose_output: str) -> CompilerConfig:
    """Parse the src/main.cpp compilation line from PIO verbose output."""
    for line in verbose_output.splitlines():
        if 'src/main.cpp' not in line or 'main.cpp.o' not in line:
            continue
        if '-c' not in line:
            continue

        tokens = shlex.split(line)
        compiler = _resolve_tool(tokens[0], verbose_output)
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

        return CompilerConfig(compiler=compiler, flags=flags, includes=includes)

    raise ValueError("Could not find src/main.cpp compilation line in verbose output")


def extract_linker_config(verbose_output: str) -> LinkerConfig:
    """Parse the final link line from PIO verbose output."""
    for line in verbose_output.splitlines():
        if 'firmware.elf' not in line:
            continue
        if '-c' in shlex.split(line):
            continue

        tokens = shlex.split(line)
        linker = _resolve_tool(tokens[0], verbose_output)
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
            linker=linker, flags=flags, objects=objects,
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
