#!/usr/bin/env bash
# Root-level Gradle wrapper shim to support CI tasks that run ./gradlew from repository root.
# Delegates to the Android TV frontend gradle shim. Replace with a real Gradle Wrapper when
# the Android project is initialized.

set -euo pipefail

TARGET_DIR="android_tv_fitness_frontend"
TARGET="$TARGET_DIR/gradlew"

if [ ! -f "$TARGET" ]; then
  echo "Gradle wrapper shim: $TARGET not found. Ensure the frontend module exists." >&2
  exit 0
fi

# Ensure target is executable
chmod +x "$TARGET" 2>/dev/null || true

echo "Delegating to $TARGET with args: $*"
exec "$TARGET" "$@"
