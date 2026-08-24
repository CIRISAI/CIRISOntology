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

# Default output is the tracked viewer copy, for the normal "build and ship" use.
# HOLON_SANDBOX_WASM_OUT overrides the destination so a caller (ci-gates.sh's gate 10)
# can build to a scratch path and never touch the tracked file at all — see that gate
# for why "never write or checkout the tracked artifact" is now a hard requirement.
out="${HOLON_SANDBOX_WASM_OUT:-$here/viewer/holon_sandbox.wasm}"

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

mkdir -p "$(dirname -- "$out")"
cp "$workspace/target/web-dist/wasm32-unknown-unknown/release/holon_sandbox.wasm" "$out"

printf 'Built %s (%s bytes)\n' "$out" "$(wc -c < "$out")"
