# Embedded C++ Compatibility Check

Test which C++ standard library features actually work on embedded platforms — not just what the compiler claims to support.

## Why?

Embedded toolchains often claim C++17/20 support but ship incomplete standard libraries. A macro might say `__cpp_lib_optional` is defined, but `#include <optional>` fails to compile. This tool tests 157 features across 11 platforms to find the truth.

## Results

<!-- compat-matrix-start -->
| Platform | Board | Standards | Effective Support |
|----------|-------|-----------|-------------------|
| STM32 Nucleo F411RE | Cortex-M4 | c++11–c++20 | **93%** |
| Arduino Zero | SAMD21 Cortex-M0+ | c++11–c++17 | **90%** |
| Adafruit Feather M4 | SAMD51 Cortex-M4F | c++11–c++17 | **90%** |
| ESP32-S3 DevKit | Xtensa gcc 14 | c++11–c++26 | **89%** |
| Arduino Uno R4 Minima | Renesas RA4M1 | c++11–c++20 | **88%** |
| Arduino Nano 33 BLE | nRF52840 Cortex-M4F | c++11–c++20 | **77%** |
| Raspberry Pi Pico | RP2040 Cortex-M0+ | c++11–c++23 | **73%** |
| Teensy 4.1 | i.MX RT1062 Cortex-M7 | c++11–c++20 | **66%** |
| Arduino Uno | AVR ATmega328P | c++11–c++17 | **40%** |
| Arduino Nano Every | megaAVR ATmega4809 | c++11–c++17 | **38%** |
| ESP8266 NodeMCU | Xtensa LX106 | c++17 only | **0%** |
<!-- compat-matrix-end -->

"Effective support" = features that compile successfully (supported + unreported), regardless of whether the SD-6 feature-test macro is defined.

### Status classifications

- **supported** — macro defined and feature compiles
- **unsupported** — feature does not compile
- **macro_lies** — macro claims support but compile fails
- **unreported** — feature compiles but macro not defined

## Quick Start

```bash
# Setup
python3 -m venv .venv
.venv/bin/pip install -e .

# Run feature tests across all platforms
.venv/bin/compat-check run

# Run a single platform
.venv/bin/compat-check run --platform stm32-nucleo-f411re

# Check a library's compatibility across platforms
.venv/bin/compat-check library ~/path/to/my-library --report report.md

# Check a library on specific platforms
.venv/bin/compat-check library ~/path/to/my-library --platform esp32s3-arduino-v3 --platform avr-uno

# Generate the static site
.venv/bin/compat-check generate
```

## Commands

### `compat-check run` — Feature compatibility tests

Tests individual C++ features against target platforms.

| Option | Default | Description |
|--------|---------|-------------|
| `--platform SLUG` | all | Run only this platform |
| `--test NAME` | all | Run only this test |
| `--parallel N` | 4 | Max parallel builds (1 = serial) |
| `--dry-run` | | Show what would be built |

The first run per platform downloads toolchains (~200MB each) and takes several minutes for PIO probe builds. Subsequent runs are incremental — only changed tests are recompiled.

### `compat-check library` — Library compatibility

Tests a PlatformIO library's examples against all platforms.

| Option | Default | Description |
|--------|---------|-------------|
| `--platform SLUG` | all | Test only these platforms (repeatable) |
| `--example NAME` | all | Test only these examples (repeatable) |
| `--report PATH` | stdout | Write report to file |
| `--report-format FMT` | md | `md` or `json` |

Optimizations:
- **Build cache**: reuses PIO framework objects between builds for the same board
- **Standard skip**: tests highest standard first; if it fails, skips lower standards (they can't do better)

### `compat-check generate` — Static site

Generates an HTML site and updates the README from results.

### `compat-check sync` — Update catalog

Syncs the feature catalog from upstream SD-6 data.

## How It Works

Two-stage pipeline per platform per C++ standard:

1. **Macro probe** — PIO builds a source that embeds SD-6 feature-test macro values as strings, then `strings` extracts them from the ELF. Also captures the exact compiler command for stage 2.
2. **Compile tests** — runs the extracted compiler command directly (`g++ -c`) on each test file. Fast (~0.1s per test, no PIO overhead).

Results are classified by comparing the macro probe (what the compiler claims) against the compile test (what actually works).

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

Add entries to `scripts/generate_tests.py` and run:
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

## Incremental Builds

The manifest (`results/manifest.json`) tracks hashes of probe source and test files per platform. Unchanged tests are skipped. To force a full rebuild, delete `results/<slug>/` or the manifest entry.

The `.work/` directory contains PlatformIO build artifacts and cached toolchains. Don't delete it unless you want to re-download (~2GB total for all 11 platforms).

## Related Projects

- **[nonstd-lite-bundle](https://github.com/m-mcgowan/nonstd-lite-bundle)** — Polyfill library providing `std::optional`, `std::string_view`, `std::variant`, `std::span` on platforms missing them. Transparent — write `std::optional` and it works everywhere. Tested on STM32, SAMD, ESP32, RP2040, nRF52840.
