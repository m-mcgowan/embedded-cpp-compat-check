"""Generate the Stage 1 macro probe source file."""

from compat_check.catalog.models import Feature

_HEADER = """\
// Auto-generated macro probe — do not edit.
// Embeds "name=value" strings extractable via `strings` on the compiled binary.

#if __has_include(<version>)
#include <version>
#endif

#define STRINGIFY2(x) #x
#define STRINGIFY(x) STRINGIFY2(x)
#define PROBE_DEFINED(name) \\
    static const char probe_##name[] __attribute__((used)) = \\
        #name "=" STRINGIFY(name);
#define PROBE_UNDEFINED(name) \\
    static const char probe_##name[] __attribute__((used)) = \\
        #name "=0";

"""

_FOOTER = """\
static const char probe_sentinel[] __attribute__((used)) = "__SENTINEL__=-1";

int main() { return 0; }
"""


def _macro_check(name: str) -> str:
    return (
        f"#ifdef {name}\n"
        f"PROBE_DEFINED({name})\n"
        f"#else\n"
        f"PROBE_UNDEFINED({name})\n"
        f"#endif\n"
    )


def generate_probe_source(features: list[Feature]) -> str:
    """Generate a .cpp file that records the value of every feature-test macro."""
    parts = [_HEADER]
    for feature in features:
        parts.append(_macro_check(feature.name))
    parts.append(_FOOTER)
    return "".join(parts)
