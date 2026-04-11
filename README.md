# Embedded C++ Compatibility Check

Embedded toolchains often claim C++17 or C++20 support, but ship incomplete standard libraries. A macro might say `__cpp_lib_optional` is defined, but `#include <optional>` fails to compile. This tool finds the truth — testing 394 C++ features across 12 embedded platforms using real PlatformIO builds, so you know exactly what works before you write a line of code.

- **394 [SD-6](https://wg21.link/p0941) feature tests** — every language feature, library type, and attribute in the C++ standard's feature-test macro catalog (C++11 through C++26)
- **12 platforms** — AVR, ARM Cortex-M (STM32, SAMD, nRF52, RP2040, Renesas), ESP32, Teensy
- **Real PIO builds** — tests compile through PlatformIO exactly like your code, including framework precompilation
- **Library compatibility checker** — test any PlatformIO library across platforms and standards, with markdown/JSON reports
- **Browsable HTML site** — per-feature results with cppreference links and expandable compiler errors

**Library authors:** [test your library](#test-a-librarys-compatibility) across platforms and C++ standards in one command, locally or in CI.

## Compatibility Matrix

<!-- compat-matrix-start -->
*12 platforms, all support c++17 above 80% compatibility. Effective support: 86%–100%. Updated 2026-04-07.*

| Platform | Board | Standards | Effective Support |
|----------|-------|-----------|-------------------|
| ESP32-S3 (pioarduino) | esp32s3 | c++11–c++26 | **100%** |
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

## Library Compatibility Testing

Test any PlatformIO library across embedded platforms and C++ standards — from the PlatformIO registry or a local directory.

```bash
# Install
pip install git+https://github.com/m-mcgowan/embedded-cpp-compat-check.git
pip install platformio

# Test a library from the PlatformIO registry
compat-check library ArduinoJson --report report.md

# Test with a pinned version
compat-check library ArduinoJson@6.21.0 --report report.md

# Test a local library directory
compat-check library ~/my-library --report report.md

# Test specific platforms
compat-check library ~/my-library \
  --platform stm32-nucleo-f411re \
  --platform esp32s3-arduino-v3 \
  --platform avr-uno

# JSON output (auto-detected from .json extension)
compat-check library ~/my-library --report results.json
```

If the argument is a directory, it's used directly. Otherwise it's installed from the PlatformIO registry. Platforms are auto-detected from the library's metadata unless overridden with `--platform`.

### What you get

The tool starts with testing the highest C++ standard supported on each platform. If it fails, indicating the library uses newer C++ features than supported, lower standards are skipped since they can't do better. If it passes, it tests downward to find the minimum working standard.

```
$ compat-check library ~/nonstd-lite-bundle \
    --platform stm32-nucleo-f411re --platform avr-uno

Library: nonstd-lite-bundle v1.1.0
Examples: ['  optional_demo', 'span_demo', 'string_view_demo', 'variant_demo']
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

Add `<!-- compat-matrix-start -->` and `<!-- compat-matrix-end -->` markers to your README where you want the compatibility table, then use the action:

**Option A: CI verifies the matrix is up to date** (developer updates locally, CI gates)

```yaml
name: Embedded Compatibility
on: [push, pull_request]

jobs:
  compat-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: m-mcgowan/embedded-cpp-compat-check@v0.1
        with:
          readme: verify

      - name: Show report in job summary
        run: cat compatibility.md >> $GITHUB_STEP_SUMMARY
```

**Option B: CI auto-updates the matrix** (useful for PR workflows)

```yaml
      - uses: m-mcgowan/embedded-cpp-compat-check@v0.1
        with:
          readme: update

      - uses: peter-evans/create-pull-request@v6
        with:
          title: "ci: update compatibility matrix"
          commit-message: "ci: update compatibility matrix"
```

The action handles Python, PlatformIO, and compat-check installation. Pin to a release tag (e.g. `@v0.1`) for stability.

| Input | Default | Description |
|-------|---------|-------------|
| `library` | `.` | Path to the library directory |
| `platforms` | from library.json | Space-separated platform slugs (auto-detected from library metadata if omitted) |
| `report` | `compatibility.md` | Report output path |
| `report-format` | auto | `md` or `json` (auto-detected from extension) |
| `readme` | `none` | `update` to inject report into README, `verify` to fail if outdated |
| `readme-path` | `README.md` | Path to the file containing the matrix markers |
| `setup-python` | `true` | Set to `false` if your workflow already configures Python |
| `setup-platformio` | `true` | Set to `false` if your workflow already installs PlatformIO |

### CLI reference

<!-- cli-library-help-start -->
```
$ compat-check library --help

Usage: compat-check library [OPTIONS] LIBRARY_REF

  Test a PlatformIO library across embedded platforms and C++ standards.

  LIBRARY_REF is either a local directory path or a PlatformIO registry
  package name (with optional @version). If the argument exists as a
  directory, it's treated as a local path. Otherwise it's installed from the
  registry.

  Examples:
    compat-check library ~/my-library          # local directory
    compat-check library ArduinoJson            # registry, latest
    compat-check library ArduinoJson@6.21.0     # registry, pinned

  For each platform, tests the highest C++ standard first and works downward
  to find the minimum working standard. Generates a compatibility report
  showing which platforms and standards your library supports.

Options:
  --platforms-dir PATH       Directory containing platform YAML definitions
                             [default: platforms]
  --platform TEXT            Test only these platforms (repeatable). Defaults
                             to platforms from library.json.
  --example TEXT             Test only these examples (repeatable). Defaults
                             to all examples.
  --report PATH              Write report to file (default: stdout)
  --report-format [md|json]  Report format. Auto-detected from --report
                             extension if omitted.
  --work-dir PATH            Build cache directory  [default: .work]
  --help                     Show this message and exit.
```
<!-- cli-library-help-end -->

## Feature Compatibility Tests

All commands: `compat-check --help`

### `compat-check run`

<!-- cli-run-help-start -->
```
$ compat-check run --help

Usage: compat-check run [OPTIONS]

  Test C++ feature compatibility across embedded platforms.

  Runs 394 SD-6 feature tests against each platform at every supported C++
  standard. Results are saved as JSON and can be rendered as an HTML site with
  'compat-check generate'.

  The first run downloads PlatformIO toolchains (~200MB per platform).
  Subsequent runs are incremental — only changed tests are rebuilt.

Options:
  --catalog PATH        SD-6 feature catalog YAML  [default:
                        catalog/data.yaml]
  --platforms-dir PATH  Directory containing platform YAML definitions
                        [default: platforms]
  --tests-dir PATH      Directory containing C++ test files  [default: tests]
  --results-dir PATH    Output directory for JSON results  [default: results]
  --work-dir PATH       Build cache directory  [default: .work]
  --platform TEXT       Run only this platform (slug from platforms/*.yaml)
  --test TEXT           Run only this test (filename without .cpp)
  --parallel INTEGER    Max parallel builds (1=serial)  [default: 4]
  --dry-run             Show what would be built without building
  --recipe              Apply platform recipes (test with polyfill libraries
                        like nonstd-lite-bundle)
  --help                Show this message and exit.
```
<!-- cli-run-help-end -->

### `compat-check generate`

<!-- cli-generate-help-start -->
```
$ compat-check generate --help

Usage: compat-check generate [OPTIONS]

  Generate a browsable HTML site and update the README compatibility matrix.

  Reads JSON results from a previous 'compat-check run' and produces: - An
  HTML site with per-platform feature tables - An updated compatibility matrix
  in README.md (between marker comments)

Options:
  --results-dir PATH    Directory containing JSON results from 'compat-check
                        run'  [default: results]
  --output-dir PATH     Output directory for the HTML site  [default: site]
  --platforms-dir PATH  Directory containing platform YAML definitions
                        [default: platforms]
  --site-url TEXT       Base URL for platform links in README (e.g.
                        https://user.github.io/repo)
  --help                Show this message and exit.
```
<!-- cli-generate-help-end -->

### `compat-check sync`

<!-- cli-sync-help-start -->
```
$ compat-check sync --help

Usage: compat-check sync [OPTIONS]

  Sync the SD-6 feature catalog from upstream.

  Downloads the latest feature-test macro database from
  github.com/cpplearner/feature-test-macro and saves it locally.

Options:
  --target PATH  Output path for the catalog YAML  [default:
                 catalog/data.yaml]
  --help         Show this message and exit.
```
<!-- cli-sync-help-end -->

## How It Works

Two-stage pipeline per platform per C++ standard:

1. **Macro probe** — A generated C++ file checks every SD-6 feature-test macro (e.g. `#ifdef __cpp_lib_optional`) and embeds the results as strings in the compiled binary. PlatformIO compiles this file for the target platform, then `strings` extracts the macro values from the ELF. This tells us what the compiler *claims* to support.

2. **Batch compile** — all 394 test files are placed in a single PIO project and built with `SCONSFLAGS="-k"` (keep going on errors). Each test is a minimal `.cpp` that `#include`s the relevant header and exercises the feature. Pass/fail is determined by which `.o` files were produced. This tells us what *actually compiles*.

Using PIO for the test compilation (rather than invoking the compiler directly) means the results match what developers experience — framework precompilation, real include paths, and real build flags. The framework is compiled once per platform+standard, making it efficient too.

Results are classified by comparing stage 1 (what the compiler claims) against stage 2 (what actually works). A feature that compiles but has no macro is `unreported`; a macro that's defined but the feature doesn't compile is `macro_lies`.

### Error audit

When adding new tests or platforms, the audit script checks that every compile failure is caused by the feature under test — not by a framework bug, Arduino macro conflict, or test that depends on an unrelated feature:

```bash
python scripts/audit_errors.py              # full report
python scripts/audit_errors.py --suspects-only  # just potential problems
```

If the audit reports suspects, the test may need fixing (e.g. a `[[noreturn]]` test that uses `throw` will fail on platforms with exceptions disabled — the fix is to use `while(true){}` instead).

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

## Acknowledgments and References

- **[cpplearner/feature-test-macro](https://github.com/cpplearner/feature-test-macro)** — the SD-6 feature-test macro database that powers our test catalog
- **[cppreference.com](https://en.cppreference.com/)** — documentation links for each feature in the generated reports
- **[PlatformIO](https://platformio.org/)** — the build system that makes cross-platform embedded compilation possible from a single machine
- **[WG21 P0941](https://wg21.link/p0941)** — the C++ standard's feature-test macro proposal (SD-6)

## Related Projects

- **[nonstd-lite-bundle](https://github.com/m-mcgowan/nonstd-lite-bundle)** — Polyfill library providing `std::optional`, `std::string_view`, `std::variant`, `std::span` on platforms missing them. Write `std::optional` and it works everywhere.
