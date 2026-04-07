# TODO

## Build system support

Currently all platform validation uses PlatformIO. Future build systems to support:

1. **Arduino CLI / Arduino IDE** — most popular for hobbyists, different build behavior than PIO
2. **CMake / ESP-IDF** — native ESP32 development without Arduino framework
3. **Zephyr** — RTOS with its own build system (west + CMake), growing embedded adoption

The architecture separates build mechanics (`generate_batch_project` + `run_batch_build`) from orchestration (probe + classification). Each new build system needs its own implementations of these without changing the orchestrator.

The `build_system` field in platform YAMLs exists but is not currently used — all platforms assume PlatformIO.

## GitHub Action for library authors

Reusable GitHub Action so library authors can add embedded compatibility testing with minimal setup:

```yaml
- uses: m-mcgowan/embedded-cpp-compat-check@v0.1
  with:
    platforms: stm32-nucleo-f411re esp32s3-arduino-v3 avr-uno
    report: compatibility.md
```

The action handles Python/PIO setup, toolchain caching, and report generation. As the tool grows, library authors get new capabilities without changing their workflow.

## Features-used analysis

Static analysis of a library's source to determine which C++ features it actually uses, then cross-reference against the platform compatibility matrix. This would tell library authors "you use `std::optional` — here's where that works and where it doesn't" without needing to build anything.

This is the natural complement to the build-based library checker: build testing proves it compiles, features-used analysis explains why it doesn't (and suggests polyfills).
