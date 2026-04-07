# TODO

## Build system support

Currently all platform validation uses PlatformIO. Future build systems to support:

1. **Arduino CLI / Arduino IDE** — most popular for hobbyists, different build behavior than PIO
2. **CMake / ESP-IDF** — native ESP32 development without Arduino framework
3. **Zephyr** — RTOS with its own build system (west + CMake), growing embedded adoption

The architecture separates build mechanics (`generate_batch_project` + `run_batch_build`) from orchestration (probe + classification). Each new build system needs its own implementations of these without changing the orchestrator.

The `build_system` field in platform YAMLs exists but is not currently used — all platforms assume PlatformIO.
