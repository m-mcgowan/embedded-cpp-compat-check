# Embedded C++ Compatibility Check

## Quick Start

```bash
# Setup (one time)
python3 -m venv .venv
.venv/bin/pip install -e .

# Run feature tests across all platforms
.venv/bin/compat-check run

# Run a single platform
.venv/bin/compat-check run --platform avr-uno

# Run a single test
.venv/bin/compat-check run --test optional

# Check a library's compatibility
.venv/bin/compat-check library ~/e/note-cpp --report report.md

# Check a library on one platform
.venv/bin/compat-check library ~/e/note-cpp --platform esp32s3-arduino-v3

# Generate the static site + README
.venv/bin/compat-check generate
```

## Commands

### `compat-check run`

Runs the feature compatibility tests. Two-stage pipeline per platform per C++ standard:

1. **Macro probe** — PIO builds a source that embeds SD-6 feature-test macro values as strings,
   then runs `strings` on the ELF to extract them (no device needed, compile-only).
2. **Compile tests** — compiles individual test files (in `tests/cpp11/`, `tests/cpp17/`, etc.)
   using the compiler extracted from the probe build. Fast (~0.1s per test).

Results classified as: `supported`, `unsupported`, `macro_lies` (macro says yes but compile fails),
`unreported` (compiles but macro not defined).

```
Options:
  --catalog PATH        Catalog file (default: catalog/data.yaml)
  --platforms-dir PATH  Platform definitions (default: platforms/)
  --tests-dir PATH      Test files (default: tests/)
  --results-dir PATH    Output directory (default: results/)
  --work-dir PATH       Build artifacts (default: .work/)
  --platform SLUG       Run only this platform
  --test NAME           Run only this test
  --parallel N          Max parallel builds, 1=serial (default: 4)
  --dry-run             Show what would be built
```

### `compat-check library`

Tests a PlatformIO library's examples against target platforms. Discovers examples automatically
from the library's `examples/` directory.

```
Options:
  --platforms-dir PATH  Platform definitions (default: platforms/)
  --platform SLUG       Test only these platforms (repeatable)
  --example NAME        Test only these examples (repeatable)
  --report PATH         Write report to file
  --report-format FMT   md or json (default: md)
  --work-dir PATH       Build artifacts (default: .work/)
```

Optimizations:
- **Build cache**: reuses PIO framework objects between builds for the same board
- **Standard skip**: tests highest standard first; if it fails, skips lower standards

### `compat-check generate`

Generates a static HTML site and README from results.

### `compat-check sync`

Updates the feature catalog from upstream SD-6 data.

## Adding Tests

Tests are minimal `.cpp` files in `tests/cpp<NN>/`:

```cpp
// feature: optional
// macro: __cpp_lib_optional
// standard: cpp17
// category: library
// description: std::optional

#include <optional>
auto main() -> int {
    std::optional<int> x = 42;
    return x.value() == 42 ? 0 : 1;
}
```

The `scripts/generate_tests.py` script has a `TESTS` list — add entries there and run:
```bash
.venv/bin/python scripts/generate_tests.py
```

## Adding Platforms

Create a YAML file in `platforms/`:

```yaml
name: Human-readable name
slug: short-identifier
version: "1.0.0"
architecture: arm-cortex-m4
mcu: chip_name
build_system: platformio
framework: arduino

platformio:
  platform: platformio-platform-name
  board: pio-board-id
  framework: arduino

standards: [c++11, c++14, c++17, c++20]

release_monitor:
  type: platformio_registry
  platform: platformio-platform-name
```

Find board IDs with `pio boards | grep -i <board>`.

## Platforms

| Slug | Board | Architecture | Standards | Pass% |
|------|-------|-------------|-----------|-------|
| `stm32-nucleo-f411re` | STM32 Nucleo F411RE | Cortex-M4 | c++11–c++20 | 93% |
| `samd21-zero` | Arduino Zero | Cortex-M0+ SAMD21 | c++11–c++17 | 90% |
| `samd51-feather-m4` | Adafruit Feather M4 | Cortex-M4F SAMD51 | c++11–c++17 | 90% |
| `esp32s3-arduino-v3` | ESP32-S3 DevKit | Xtensa gcc 14 | c++11–c++26 | 89% |
| `uno-r4-minima` | Arduino Uno R4 Minima | Cortex-M4 RA4M1 | c++11–c++20 | 88% |
| `nrf52840-nano33ble` | Arduino Nano 33 BLE | Cortex-M4F nRF52840 | c++11–c++20 | 77% |
| `rp2040-pico` | Raspberry Pi Pico | Cortex-M0+ RP2040 | c++11–c++23 | 73% |
| `teensy41` | Teensy 4.1 | Cortex-M7 i.MX RT1062 | c++11–c++20 | 66% |
| `avr-uno` | Arduino Uno | AVR ATmega328P | c++11–c++17 | 40% |
| `megaavr-nano-every` | Arduino Nano Every | megaAVR ATmega4809 | c++11–c++17 | 38% |
| `esp8266-nodemcu` | NodeMCU v2 | Xtensa LX106 | c++17 only | 0% |

Note: ESP8266's Arduino framework requires C++17 internally but has broken standard library
support. It cannot override the C++ standard and fails all feature tests.

## Incremental Builds

The manifest (`results/manifest.json`) tracks hashes of probe source and test files per platform.
If nothing changed, the orchestrator skips the rebuild. To force a rebuild for a platform, delete
its entry from the manifest, or delete `results/<slug>/`.

The `.work/` directory contains PlatformIO build artifacts and cached toolchain cores.
Don't delete `.work/` unless you want to re-download toolchains (~2GB total for all platforms).

## Results

Output: `results/<slug>/<version>/cpp<NN>.json`

Each JSON file is an array of result objects:
```json
{
    "platform": "stm32-nucleo-f411re",
    "platform_version": "17.6.0",
    "standard": "c++17",
    "feature": "cpp17/optional",
    "macro": "__cpp_lib_optional",
    "macro_value": "201606",
    "status": "supported",
    "compile_time_ms": 85
}
```

Status values: `supported`, `unsupported`, `macro_lies`, `unreported`.

## Related Projects

- [nonstd-lite-bundle](https://github.com/m-mcgowan/nonstd-lite-bundle) — polyfill library
  providing `std::optional`, `std::string_view`, `std::variant`, `std::span` etc. on platforms
  missing them. Works on STM32, SAMD, ESP32, RP2040, nRF52840. Not AVR (needs avr-libstdcpp).
