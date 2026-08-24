#!/bin/sh
# Build the browser module for the multiscale sandbox.
#
# The size profile is set through environment variables rather than a
# `[profile.release]` section in the crate's own manifest: a workspace member's profile
# section is silently IGNORED by Cargo, so declaring one there would look like it
# worked and would not.
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
workspace=$(CDPATH= cd -- "$here/../.." && pwd)

# Dedicated target dir: the shipped artifact must be a function of (source, toolchain)
# alone. Sharing the workspace target/ with plain-release builds made the bytes depend
# on BUILD ORDER — cargo reused artifacts fingerprinted under other flag sets, and the
# same source produced three different binaries in one day (F6's final mechanism).
CARGO_TARGET_DIR="$workspace/target/web-dist" \
CARGO_PROFILE_RELEASE_OPT_LEVEL=z \
CARGO_PROFILE_RELEASE_LTO=true \
CARGO_PROFILE_RELEASE_CODEGEN_UNITS=1 \
CARGO_PROFILE_RELEASE_PANIC=abort \
CARGO_PROFILE_RELEASE_STRIP=true \
cargo build \
  --manifest-path "$workspace/Cargo.toml" \
  --package holon-sandbox \
  --target wasm32-unknown-unknown \
  --release

cp "$workspace/target/web-dist/wasm32-unknown-unknown/release/holon_sandbox.wasm" \
  "$here/viewer/holon_sandbox.wasm"

printf 'Built %s (%s bytes)\n' \
  "$here/viewer/holon_sandbox.wasm" \
  "$(wc -c < "$here/viewer/holon_sandbox.wasm")"
