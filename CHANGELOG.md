# Changelog

## 0.1.0 — 2026-04-07

Initial release.

### Feature compatibility matrix

- **394 SD-6 feature tests** covering C++11 through C++26 — every language feature, library type, and attribute in the standard's feature-test macro catalog
- **12 embedded platforms**: AVR Uno, megaAVR Nano Every, SAMD21 Zero, SAMD51 Feather M4, STM32 Nucleo F411RE, nRF52840 Nano 33 BLE, RP2040 Pico, Teensy 4.1, ESP32-S3 (Arduino + espressif32), ESP8266, Arduino Uno R4 Minima
- **Batch PlatformIO builds** — tests compile through PIO the same way developers use it, with framework precompilation. Results reflect real-world compatibility.
- **SD-6 macro probe** — extracts feature-test macro values from compiled firmware to detect `macro_lies` (compiler claims support but feature doesn't compile)
- **Incremental builds** — manifest tracks file hashes, only rebuilds changed tests

### Library compatibility checker

- `compat-check library <path>` tests a PlatformIO library's examples across platforms and C++ standards
- Cross-standard sweep finds the minimum working C++ standard per platform
- Smart skip optimization — if the highest standard fails, lower standards are skipped
- Markdown and JSON report output
- GitHub Actions CI workflow documented in README

### Static site generator

- Browsable HTML site with per-platform feature tables
- Features grouped by category (language, library, attribute)
- Per-standard progress bars and percentages
- Expandable compiler error output on click
- cppreference documentation links for each macro (~386/394 linked)
- Color-coded compatibility matrix (90%+ green, 50-89% yellow, <50% red)
- Status classification legend

### Error audit

- `scripts/audit_errors.py` classifies every compile error as legitimate, framework, or suspect
- 15+ classification rules covering missing headers, missing symbols, framework header pollution, Arduino macro conflicts, deprecated APIs, and more
- Fuzzy feature-name matching with known-dependency overrides
- `--suspects-only` flag for quick CI checks

### Testing

- 65 unit tests (mocked PIO, <1s)
- 12 acceptance tests (real PIO builds on STM32, ~5 min)
- pytest in CI workflow
