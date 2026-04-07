# Embedded C++ Compatibility Check

Find out which C++ features actually work on embedded platforms — not just what the compiler claims to support.

## Features

- **394 SD-6 feature tests** — every language feature, library type, and attribute in the C++ standard's feature-test macro catalog
- **12 platforms** — AVR, ARM Cortex-M, ESP32, RP2040, Teensy, and more
- **Real PIO builds** — tests are compiled through PlatformIO exactly like your code, including framework precompilation
- **Library compatibility checker** — test your PlatformIO library's examples across platforms and C++ standards
- **Static site** — browsable HTML report with per-feature cppreference links and expandable compiler errors
- **Error audit** — automated classification of failures to catch test bugs vs real incompatibilities

## Compatibility Matrix

<!-- compat-matrix-start -->
| Platform | Board | Standards | Effective Support |
|----------|-------|-----------|-------------------|
| ESP32-S3 (Arduino v3) | esp32s3 | c++11–c++26 | **100%** |
| ESP32-S3 (espressif32 official) | esp32s3 | c++11–c++26 | **100%** |
| SAMD51 Adafruit Feather M4 | SAMD51 Cortex-M4F | c++11–c++17 | **97%** |
| Teensy 4.1 | i.MX RT1062 Cortex-M7 | c++11–c++20 | **97%** |
| STM32 Nucleo F411RE | STM32F411 Cortex-M4 | c++11–c++20 | **97%** |
| Raspberry Pi Pico (RP2040) | RP2040 Cortex-M0+ | c++11–c++23 | **97%** |
| SAMD21 Arduino Zero | SAMD21 Cortex-M0+ | c++11–c++17 | **95%** |
| Arduino Uno R4 Minima | Renesas RA4M1 | c++11–c++20 | **95%** |
| nRF52840 Arduino Nano 33 BLE | nRF52840 Cortex-M4F | c++11–c++20 | **95%** |
| ESP8266 NodeMCU | ESP8266 Xtensa LX106 | c++17 | **94%** |
| megaAVR Arduino Nano Every | ATmega4809 | c++11–c++17 | **86%** |
| AVR Arduino Uno | ATmega328P | c++11–c++17 | **86%** |
<!-- compat-matrix-end -->

"Effective support" = percentage of features that compile successfully, regardless of whether the SD-6 feature-test macro is defined.

| Counts as working | Counts as failing |
|---|---|
| **supported** — macro defined and compiles | **macro_lies** — macro defined but compile fails |
| **unreported** — compiles but no macro | **unsupported** — does not compile |

## Quick Start

```bash
# Install
python3 -m venv .venv
.venv/bin/pip install -e .

# Run feature tests across all platforms (~20 min)
.venv/bin/compat-check run

# Run a single platform (~2 min)
.venv/bin/compat-check run --platform stm32-nucleo-f411re

# Generate the browsable HTML site
.venv/bin/compat-check generate
open site/index.html
```

## Check Your Library

Test whether your PlatformIO library builds across embedded platforms at each C++ standard. Your library needs:

- A `library.json` or `library.properties` file
- An `examples/` directory with `.ino` or `.cpp` example sketches

### Run locally

```bash
# Test across all 12 platforms
compat-check library ~/my-library --report report.md

# Test specific platforms
compat-check library ~/my-library \
  --platform stm32-nucleo-f411re \
  --platform esp32s3-arduino-v3 \
  --platform avr-uno

# JSON output for automation
compat-check library ~/my-library --report-format json --report results.json
```

### What you get

For each platform, the tool tests the highest supported C++ standard first. If it fails, lower standards are skipped (they can't do better). If it passes, it tests downward to find the minimum working standard.

```
$ compat-check library ~/nonstd-lite-bundle \
    --platform stm32-nucleo-f411re --platform avr-uno

Library: nonstd-lite-bundle v1.1.0
Examples: ['optional_demo', 'span_demo', 'string_view_demo', 'variant_demo']
  [1/28] stm32-nucleo-f411re c++20 optional_demo... PASS (5323ms)
  [2/28] stm32-nucleo-f411re c++17 optional_demo... PASS (3836ms)
  [3/28] stm32-nucleo-f411re c++14 optional_demo... PASS (3484ms)
  [4/28] stm32-nucleo-f411re c++11 optional_demo... PASS (3752ms)
  ...
  [17/28] avr-uno c++17 optional_demo... FAIL (2580ms)
  [18/28] avr-uno c++14 optional_demo... SKIP
  [19/28] avr-uno c++11 optional_demo... SKIP
```

The generated report shows the minimum C++ standard that works on each platform:

```markdown
| Platform             | Min Standard | Examples |
|----------------------|-------------|----------|
| stm32-nucleo-f411re  | c++11       | 4/4      |
| avr-uno              | —           | 0/4      |
```

### Add to your CI

Add to your GitHub Actions workflow to test library compatibility on every push:

```yaml
name: Embedded Compatibility
on: [push, pull_request]

jobs:
  compat-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install tools
        run: |
          pip install platformio
          pip install git+https://github.com/m-mcgowan/embedded-cpp-compat-check.git

      - name: Check compatibility
        run: |
          compat-check library . \
            --platform stm32-nucleo-f411re \
            --platform esp32s3-arduino-v3 \
            --platform avr-uno \
            --report compatibility.md

      - name: Upload report
        uses: actions/upload-artifact@v4
        with:
          name: compatibility-report
          path: compatibility.md

      - name: Post to PR
        if: github.event_name == 'pull_request'
        uses: marocchino/sticky-pull-request-comment@v2
        with:
          path: compatibility.md
```

### CLI reference

| Option | Default | Description |
|--------|---------|-------------|
| `--platform SLUG` | all | Test only these platforms (repeatable) |
| `--example NAME` | all | Test only these examples (repeatable) |
| `--report PATH` | stdout | Write report to file |
| `--report-format FMT` | md | `md` or `json` |
| `--work-dir PATH` | `.work` | Build cache directory |

## Feature Compatibility Tests

### `compat-check run`

Tests individual C++ features against target platforms using real PlatformIO builds.

| Option | Default | Description |
|--------|---------|-------------|
| `--platform SLUG` | all | Run only this platform |
| `--test NAME` | all | Run only this test |
| `--parallel N` | 4 | Max parallel builds (1 = serial) |
| `--dry-run` | | Show what would be built |

The first run per platform downloads toolchains (~200MB each). Subsequent runs are incremental — only changed tests are recompiled. A full 12-platform sweep takes ~20 minutes.

### `compat-check generate`

Generates a browsable HTML site and updates the compatibility matrix in this README.

### `compat-check sync`

Syncs the feature catalog from the upstream [SD-6 feature-test macro database](https://github.com/cpplearner/feature-test-macro).

## How It Works

Two-stage pipeline per platform per C++ standard:

1. **Macro probe** — PIO builds a source that embeds SD-6 feature-test macro values as strings, then `strings` extracts them from the ELF.
2. **Batch compile** — all test files are placed in a single PIO project and built with `SCONSFLAGS="-k"` (keep going on errors). Pass/fail is determined by which `.o` files were produced. This matches real developer experience — the framework is precompiled once, and test code is compiled against it.

Results are classified by comparing the macro probe (what the compiler claims) against the compile test (what actually works).

### Error audit

After a sweep, run the audit script to check that every failure is about the feature being tested (not a framework bug or test bug):

```bash
python scripts/audit_errors.py              # full report
python scripts/audit_errors.py --suspects-only  # just potential problems
```

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
python scripts/generate_tests.py
```

## Adding Platforms

Create a YAML file in `platforms/`:

```yaml
name: Human-readable name
slug: short-identifier
version: "1.0.0"
architecture: arm-cortex-m4
mcu: chip_name
board_family: Short board description
build_system: platformio
framework: arduino

platformio:
  platform: platformio-platform-name
  board: pio-board-id
  framework: arduino

standards: [c++11, c++14, c++17, c++20]
```

Find board IDs with `pio boards | grep -i <board>`.

## Related Projects

- **[nonstd-lite-bundle](https://github.com/m-mcgowan/nonstd-lite-bundle)** — Polyfill library providing `std::optional`, `std::string_view`, `std::variant`, `std::span` on platforms missing them. Write `std::optional` and it works everywhere.
