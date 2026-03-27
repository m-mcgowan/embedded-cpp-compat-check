"""Generate the Stage 1 macro probe source file."""

from compat_check.catalog.models import Feature

_HEADER = """\
// Auto-generated macro probe — do not edit.
// Embeds "name=value" strings in a single array referenced from main/setup
// so the linker cannot strip them. Extract with `strings` on the binary.

#if __has_include(<version>)
#include <version>
#endif

#define STRINGIFY2(x) #x
#define STRINGIFY(x) STRINGIFY2(x)

"""

_ARRAY_START = """\
// Collect all probe strings into one referenced array.
static const char* const probe_results[] = {
"""

_ARRAY_END = """\
    "__SENTINEL__=-1",
};

static const int probe_count = sizeof(probe_results) / sizeof(probe_results[0]);

// Force the linker to keep every element by iterating.
volatile char probe_sink;

auto main() -> int {
    for (int i = 0; i < probe_count; i++) {
        probe_sink = probe_results[i][0];
    }
    return 0;
}
"""


def _macro_check(name: str) -> str:
    return (
        f"#ifdef {name}\n"
        f'    "{name}=" STRINGIFY({name}),\n'
        f"#else\n"
        f'    "{name}=0",\n'
        f"#endif\n"
    )


def generate_probe_source(features: list[Feature]) -> str:
    """Generate a .cpp file that records the value of every feature-test macro."""
    parts = [_HEADER, _ARRAY_START]
    for feature in features:
        parts.append(_macro_check(feature.name))
    parts.append(_ARRAY_END)
    return "".join(parts)
