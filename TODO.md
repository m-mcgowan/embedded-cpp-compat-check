# TODO

## Build system support

Currently all platform validation uses PlatformIO. Future build systems to support:

1. **Arduino CLI / Arduino IDE** — most popular for hobbyists, different build behavior than PIO
2. **CMake / ESP-IDF** — native ESP32 development without Arduino framework
3. **Zephyr** — RTOS with its own build system (west + CMake), growing embedded adoption

The architecture separates build mechanics (`generate_batch_project` + `run_batch_build`) from orchestration (probe + classification). Each new build system needs its own implementations of these without changing the orchestrator.

The `build_system` field in platform YAMLs exists but is not currently used — all platforms assume PlatformIO.

## PlatformIO registry support for library checker

Test libraries directly from the PIO registry without downloading them first:

```bash
compat-check library ArduinoJson              # registry, latest version
compat-check library ArduinoJson@6.21.0       # registry, pinned version
compat-check library ~/my-library             # local path
```

Default behavior: if the argument exists as a directory, treat as local path; otherwise treat as a registry package name. Explicit flags (`--registry`, `--local`) to disambiguate.

Uses `pio pkg install` to download the package to a temp directory, then runs the same example-discovery and build pipeline.

## GitHub Action improvements

The composite action (`action/action.yml`) is shipped in 0.1. Future improvements:

- **Toolchain caching** — cache PIO toolchains between runs (`~/.platformio/packages/`) for faster CI
- **Fail on regression** — `--fail-on regression` to fail the check when a previously-passing platform breaks
- **Minimum platform threshold** — `--fail-on "min-platforms=3"` to enforce a coverage floor

## GitHub Marketplace App

Long-term: a GitHub App that library authors install once from the marketplace. It automatically runs compatibility checks on every PR without a workflow file — like Codecov or SonarCloud.

Requires:
- GitHub App registered on the marketplace
- Hosted service to receive PR webhooks and run checks
- Posts results back as a Check Run with annotations
- Infrastructure for running PIO builds (hosted runners or cloud build service)

The composite action is the stepping stone — same user-facing contract, self-hosted execution.

## Features-used analysis

Static analysis of a library's source to determine which C++ features it actually uses, then cross-reference against the platform compatibility matrix. This would tell library authors "you use `std::optional` — here's where that works and where it doesn't" without needing to build anything.

This is the natural complement to the build-based library checker: build testing proves it compiles, features-used analysis explains why it doesn't (and suggests polyfills).
