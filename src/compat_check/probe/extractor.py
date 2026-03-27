"""Extract macro values from compiled probe output."""


def parse_probe_output(raw: str) -> dict[str, int]:
    """Parse 'name=value' lines from probe output into a dict.

    The probe generates string literals like "__cpp_concepts=201907"
    embedded in the binary. These are extracted via `strings` on the
    compiled ELF. Returns a dict mapping macro name to integer value (0 = not defined).
    The __SENTINEL__ entry is excluded.
    """
    result: dict[str, int] = {}
    for line in raw.strip().splitlines():
        line = line.strip()
        if "=" not in line:
            continue
        name, _, value_str = line.partition("=")
        name = name.strip()
        if name == "__SENTINEL__":
            continue
        try:
            # Strip C literal suffixes (L, LL, UL, etc.)
            result[name] = int(value_str.strip().rstrip("LlUu"))
        except ValueError:
            continue
    return result
