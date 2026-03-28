# TODO

## Improve build times: batch tests into single PlatformIO project

Each test file is compiled as a separate `pio run` invocation. PlatformIO startup + SCons init adds ~5s overhead per test, so a platform run with 10 tests across 3 standards takes 30-60 min when the actual compilation is ~1s per file.

### Options (in order of effort)

1. **Multi-env single project** (recommended first step)
   Put all tests for a platform+standard into one `platformio.ini` with separate `[env:test_optional]`, `[env:test_variant]`, etc. Single `pio run` compiles them all. Collapses ~10 PIO invocations into 1.
   Changes: `project.py`, `runner.py`, `engine.py` — generate one project dir per platform+standard instead of per test. Parse per-env success/failure from PIO output.

2. **Direct compiler invocation**
   After the probe stage resolves the toolchain, extract the compiler path and flags from `pio run -v` output, then invoke the compiler directly for each test. Sub-second per test. Probe still uses PIO.

3. **Wire up parallel builds**
   `max_parallel` exists in the orchestrator but is not used. With option 2, trivially parallelizable. With option 1, SCons handles it internally.

**Expected improvement:** Option 1 alone should cut a 30-min platform run to ~5-10 min.
