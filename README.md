# Embedded C++ Compatibility Check

Test which C++ standard library features actually work on embedded platforms — not just what the compiler claims to support.

## Why?

Embedded toolchains often claim C++17/20 support but ship incomplete standard libraries. A macro might say `__cpp_lib_optional` is defined, but `#include <optional>` fails to compile. This tool tests 394 features across 11 platforms to find the truth.

## Results

<!-- compat-matrix-start -->
| Platform | Board | Standards | Effective Support |
|----------|-------|-----------|-------------------|
| ESP32-S3 (Arduino v3) | esp32s3 | c++11–c++26 | **100%** |
| ESP32-S3 (espressif32 official) | esp32s3 | c++11–c++26 | **100%** |
| SAMD21 Arduino Zero | SAMD21 Cortex-M0+ | c++11–c++17 | **97%** |
| Arduino Uno R4 Minima | Renesas RA4M1 | c++11–c++20 | **97%** |
| SAMD51 Adafruit Feather M4 | SAMD51 Cortex-M4F | c++11–c++17 | **97%** |
| STM32 Nucleo F411RE | STM32F411 Cortex-M4 | c++11–c++20 | **97%** |
| nRF52840 Arduino Nano 33 BLE | nRF52840 Cortex-M4F | c++11–c++20 | **97%** |
| Raspberry Pi Pico (RP2040) | RP2040 Cortex-M0+ | c++11–c++23 | **97%** |
| ESP8266 NodeMCU | ESP8266 Xtensa LX106 | c++17 | **94%** |
| Teensy 4.1 | i.MX RT1062 Cortex-M7 | c++11–c++20 | **93%** |
| megaAVR Arduino Nano Every | ATmega4809 | c++11–c++17 | **86%** |
| AVR Arduino Uno | ATmega328P | c++11–c++17 | **86%** |
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

Tests a PlatformIO library's examples against embedded platforms to find which C++ standards work. Your library needs:
- A `library.json` or `library.properties` file
- An `examples/` directory with `.ino` or `.cpp` example sketches

```bash
# Test across all platforms
compat-check library ~/my-library --report report.md

# Test specific platforms
compat-check library ~/my-library \
  --platform stm32-nucleo-f411re \
  --platform avr-uno

# JSON output for CI
compat-check library ~/my-library --report-format json --report results.json
```

| Option | Default | Description |
|--------|---------|-------------|
| `--platform SLUG` | all | Test only these platforms (repeatable) |
| `--example NAME` | all | Test only these examples (repeatable) |
| `--report PATH` | stdout | Write report to file |
| `--report-format FMT` | md | `md` or `json` |
| `--work-dir PATH` | `.work` | Build cache directory |

**How it works:** For each platform, the tool tests the highest supported C++ standard first. If it fails, lower standards are skipped (they can't do better). If it passes, it tests downward to find the minimum working standard. Build artifacts are cached between runs.

#### Example output

Testing [nonstd-lite-bundle](https://github.com/m-mcgowan/nonstd-lite-bundle) on STM32 and AVR:

```
$ compat-check library ~/nonstd-lite-bundle --platform stm32-nucleo-f411re --platform avr-uno
Library: nonstd-lite-bundle v1.1.0
Platforms: ['stm32-nucleo-f411re', 'avr-uno']
Examples: ['optional_demo', 'span_demo', 'string_view_demo', 'variant_demo']
  [1/28] stm32-nucleo-f411re c++20 optional_demo... PASS (5323ms)
  [2/28] stm32-nucleo-f411re c++17 optional_demo... PASS (3836ms)
  [3/28] stm32-nucleo-f411re c++14 optional_demo... PASS (3484ms)
  [4/28] stm32-nucleo-f411re c++11 optional_demo... PASS (3752ms)
  ...
  [17/28] avr-uno c++17 optional_demo... FAIL (2580ms)
  [18/28] avr-uno c++14 optional_demo... SKIP
  [19/28] avr-uno c++11 optional_demo... SKIP
  ...
```

The generated report:

```markdown
| Platform             | Min Standard | Examples |
|----------------------|-------------|----------|
| stm32-nucleo-f411re  | c++11       | 4/4      |
| avr-uno              | —           | 0/4      |
```

This shows nonstd-lite-bundle works at all standards on STM32 but fails on AVR (avr-libc lacks the standard library headers the polyfill depends on).

#### Using in CI

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

      - name: Install compat-check
        run: |
          pip install git+https://github.com/m-mcgowan/embedded-cpp-compat-check.git
          # First run downloads PlatformIO toolchains (~200MB each)

      - name: Run compatibility check
        run: |
          compat-check library . \
            --platform stm32-nucleo-f411re \
            --platform esp32s3-arduino-v3 \
            --platform avr-uno \
            --report compatibility.md \
            --report-format md

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

This builds your library's examples against each platform at every supported C++ standard and produces a compatibility matrix. The sticky comment posts the report directly to your PR.

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
