#!/usr/bin/env bash
# Clean PlatformIO build artifacts from .work/, keeping only the shared
# toolchain/core caches (.pio-cores/) that speed up future builds.
#
# Usage: scripts/clean-work.sh [--all]
#   --all  Also remove .pio-cores (full clean, will re-download toolchains)

set -euo pipefail
cd "$(dirname "$0")/.."

WORK_DIR=".work"

if [ ! -d "$WORK_DIR" ]; then
    echo "No .work directory found, nothing to clean."
    exit 0
fi

echo "Before: $(du -sh "$WORK_DIR" 2>/dev/null | cut -f1)"

# Remove per-test and probe build artifacts for each platform/standard
for platform_dir in "$WORK_DIR"/*/; do
    [ -d "$platform_dir" ] || continue
    platform=$(basename "$platform_dir")

    # Skip the shared cores directory
    [ "$platform" = ".pio-cores" ] && continue

    for std_dir in "$platform_dir"c++*/; do
        [ -d "$std_dir" ] || continue
        for subdir in tests probe_project probe; do
            if [ -d "$std_dir/$subdir" ]; then
                echo "  Removing $std_dir$subdir"
                rm -rf "$std_dir/$subdir"
            fi
        done
    done
done

# Optionally remove toolchain caches too
if [ "${1:-}" = "--all" ]; then
    echo "  Removing $WORK_DIR/.pio-cores (toolchain caches)"
    rm -rf "$WORK_DIR/.pio-cores"
fi

echo "After:  $(du -sh "$WORK_DIR" 2>/dev/null | cut -f1)"
echo "Done."
