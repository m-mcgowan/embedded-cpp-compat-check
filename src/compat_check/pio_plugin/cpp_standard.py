"""PlatformIO extra script to set the C++ standard cleanly.

Usage in platformio.ini:
    extra_scripts = pre:cpp_standard.py
    custom_cpp_standard = c++17

This script can also be used as a standalone module for flag manipulation.
"""


def find_std_flag(flags: list[str]) -> str | None:
    """Find the -std= flag in a list of compiler flags."""
    for flag in flags:
        if flag.startswith("-std="):
            return flag
    return None


def replace_std_flag(flags: list[str], standard: str) -> list[str]:
    """Replace or add the -std= flag in a list of compiler flags."""
    num = standard.replace("c++", "").replace("gnu++", "")
    new_flag = f"-std=gnu++{num}"
    result = [f for f in flags if not f.startswith("-std=")]
    result.append(new_flag)
    return result


# PlatformIO extra_scripts hook — only runs inside PlatformIO's SCons environment
try:
    Import("env")  # type: ignore[name-defined]
    std = env.GetProjectOption("custom_cpp_standard", None)  # type: ignore[name-defined]
    if std:
        flags = env.get("BUILD_FLAGS", [])  # type: ignore[name-defined]
        current = find_std_flag(flags)
        if current:
            env.Append(BUILD_UNFLAGS=[current])  # type: ignore[name-defined]
        num = std.replace("c++", "").replace("gnu++", "")
        env.Append(BUILD_FLAGS=[f"-std=gnu++{num}"])  # type: ignore[name-defined]
except NameError:
    pass  # Not running inside PlatformIO
