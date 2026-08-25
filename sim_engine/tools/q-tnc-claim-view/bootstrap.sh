#!/bin/sh
set -eu

TNC_REVISION=0b35c58146751cafeadcf31684cd51ae8f4602c2
TNC_REMOTE=https://github.com/qc-tum/TNC.git

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
VENDOR_DIR="$SCRIPT_DIR/vendor/TNC"
PATCH_FILE="$SCRIPT_DIR/patches/tnc-local-only.patch"

if ! command -v git >/dev/null 2>&1; then
    echo "REFUSAL: required bootstrap command 'git' is unavailable" >&2
    exit 2
fi

if [ ! -d "$VENDOR_DIR/.git" ]; then
    if [ -e "$VENDOR_DIR" ]; then
        echo "REFUSAL: $VENDOR_DIR exists but is not a git checkout" >&2
        exit 2
    fi
    mkdir -p "$(dirname -- "$VENDOR_DIR")"
    git clone "$TNC_REMOTE" "$VENDOR_DIR"
    git -C "$VENDOR_DIR" checkout --detach "$TNC_REVISION"
fi

ACTUAL_REVISION=$(git -C "$VENDOR_DIR" rev-parse HEAD)
if [ "$ACTUAL_REVISION" != "$TNC_REVISION" ]; then
    echo "REFUSAL: TNC is at $ACTUAL_REVISION, expected $TNC_REVISION" >&2
    exit 2
fi

if git -C "$VENDOR_DIR" apply --unidiff-zero --reverse --check "$PATCH_FILE" >/dev/null 2>&1; then
    : # already patched
elif git -C "$VENDOR_DIR" apply --unidiff-zero --check "$PATCH_FILE" >/dev/null 2>&1; then
    git -C "$VENDOR_DIR" apply --unidiff-zero "$PATCH_FILE"
else
    echo "REFUSAL: pinned TNC checkout is neither clean nor recognizably patched" >&2
    exit 2
fi

echo "TNC local-only View ready at $TNC_REVISION"
echo "Run: cargo run --release -- 8 16 32"
