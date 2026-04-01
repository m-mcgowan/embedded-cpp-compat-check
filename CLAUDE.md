# Embedded C++ Compatibility Check

## Running Checks

The project has a `.venv` with the package installed in editable mode:

```bash
# Run all platforms
.venv/bin/python -m compat_check run

# Run a single platform
.venv/bin/python -c "
from pathlib import Path
from compat_check.catalog.parser import parse_catalog
from compat_check.platform.loader import load_platform
from compat_check.orchestrator.engine import Orchestrator

features = parse_catalog(Path('catalog/data.yaml'))
platform = load_platform(Path('platforms/<slug>.yaml'))
orch = Orchestrator(
    platforms=[platform], features=features,
    test_dir=Path('tests'), results_dir=Path('results'),
    work_dir=Path('.work'), max_parallel=1
)
results = orch.run()
for r in results:
    print(f\"  {r['standard']} {r['feature']}: {r['status']}\")
"
```

If the venv is missing, recreate it:
```bash
python3 -m venv .venv
.venv/bin/pip install -e .
```

## How It Works

Two-stage pipeline per platform per C++ standard:

1. **Macro probe** — compiles a source that embeds SD-6 feature-test macro values as strings,
   then runs `strings` on the ELF to extract them (no device needed, compile-only).
2. **Compile tests** — compiles individual test files (in `tests/cpp14/`, `tests/cpp17/`, etc.)
   to see if the feature actually works.

Results are classified as: `supported`, `unsupported`, `macro_lies` (macro says yes but compile fails),
`unreported` (compiles but macro not defined).

## Incremental Builds

The manifest (`results/manifest.json`) tracks hashes of probe source and test files per platform.
If nothing changed, the orchestrator skips the rebuild. To force a rebuild for a platform, delete
its entry from the manifest.

The `.work/` directory contains PlatformIO build artifacts and cached toolchain cores
(`.work/.pio-cores/<platform>/`). These are large but speed up subsequent builds significantly.
Don't delete `.work/.pio-cores/` unless you want to re-download toolchains.

## Platforms

Defined in `platforms/*.yaml`. Current platforms:

| Slug | Board | Architecture | Standards | Version |
|------|-------|-------------|-----------|---------|
| `avr-uno` | Arduino Uno | AVR ATmega328P | c++11–c++17 | 5.0.0 |
| `megaavr-nano-every` | Arduino Nano Every | megaAVR ATmega4809 | c++11–c++17 | 1.6.1 |
| `esp8266-nodemcu` | NodeMCU v2 | Xtensa LX106 | c++11–c++17 | 4.2.1 |
| `esp32s3-arduino-v3` | ESP32-S3 DevKit | Xtensa (gcc 14) | c++11–c++26 | 55.03.36 |
| `rp2040-pico` | Raspberry Pi Pico | ARM Cortex-M0+ | c++11–c++23 | 1.13.0 |
| `samd21-zero` | Arduino Zero | ARM Cortex-M0+ SAMD21 | c++11–c++17 | 8.1.0 |
| `samd51-feather-m4` | Adafruit Feather M4 | ARM Cortex-M4F SAMD51 | c++11–c++17 | 8.1.0 |
| `nrf52840-nano33ble` | Arduino Nano 33 BLE | ARM Cortex-M4F nRF52840 | c++11–c++20 | 9.5.0 |
| `stm32-nucleo-f411re` | STM32 Nucleo F411RE | ARM Cortex-M4 STM32F411 | c++11–c++20 | 17.6.0 |
| `uno-r4-minima` | Arduino Uno R4 Minima | ARM Cortex-M4 Renesas RA4M1 | c++11–c++20 | 1.1.0 |
| `teensy41` | Teensy 4.1 | ARM Cortex-M7 i.MX RT1062 | c++11–c++20 | 5.0.0 |

Note: The ESP32-S3 results are stored under the slug `esp32s3-test` (the original session used
a different slug). The canonical platform file uses `esp32s3-arduino-v3`.

## Build Times

Each PlatformIO compile takes 2-5 minutes (mostly toolchain overhead). A full platform run
with ~10 tests across 2-3 standards takes 30-60 minutes. Use `--timeout 600000` on Bash calls.

## Results

Output goes to `results/<slug>/<version>/cpp<NN>.json`. The manifest tracks what's been built
to avoid redundant work.
