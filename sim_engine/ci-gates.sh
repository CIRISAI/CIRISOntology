#!/bin/bash
# Workspace invariants, each one empirically derived rather than assumed.
# Run from the workspace root.
set -u; fail=0
ok(){ printf "  PASS  %s\n" "$1"; }
no(){ printf "  FAIL  %s\n" "$1"; fail=1; }

# 1. The no_std core must build for native and BOTH wasm targets, on its own.
#    Use -p, never --workspace: a sibling's features can pull in a C++ build script.
for T in "" "--target wasm32-unknown-unknown" "--target wasm32-wasip1"; do
  cargo build -q -p ciris-sim-core $T 2>/dev/null && ok "core builds ${T:-native}" || no "core builds ${T:-native}"
done

# 2. The core's dependency graph must be EXACTLY the permitted set.
#    Rationale: the invariant is not "zero deps" — that threshold was calibrated against
#    a stub. It is "nothing that can unify with a sibling's features, pull an allocator,
#    or require a C/C++ toolchain". `libm` is permitted because it is the no_std math
#    implementation the core needs (fabs/sqrt in the eigensolver) and its entire graph is
#    itself, with no transitive dependencies. An allowlist keeps the teeth a count loses:
#    this fails on ANY new name, including an innocuous-looking one.
ALLOWED="libm"
got=$(cargo tree -p ciris-sim-core --edges normal --prefix none 2>/dev/null \
      | grep -v '^$' | sed 's/ v[0-9].*//' | grep -v '^ciris-sim-core' | sort -u | tr '\n' ' ' | sed 's/ $//')
[ "$got" = "$ALLOWED" ] && ok "core deps are exactly {$ALLOWED}" || no "core deps are {$got}, expected {$ALLOWED}"

# 3. Default features must not pull an inference engine: the physics core has to be
#    buildable on a machine with no cmake and no C++ toolchain.
d=$(cargo tree -p ciris-nl --edges normal --prefix none 2>/dev/null | grep -cE "llama-cpp|rten")
[ "$d" -eq 0 ] && ok "default build pulls no engine" || no "default build pulls $d engine crates"

# 4. The browser path must actually compile for wasm.
cargo build -q -p ciris-nl --features web --target wasm32-unknown-unknown 2>/dev/null \
  && ok "web feature -> wasm32-unknown-unknown" || no "web feature -> wasm32-unknown-unknown"

# 5. Grammar invariants, and the closed-set decode filter used by the browser path.
cargo test -q -p ciris-nl 2>/dev/null >/dev/null && ok "grammar tests" || no "grammar tests"
cargo test -q -p ciris-nl --features web 2>/dev/null >/dev/null \
  && ok "web decode-filter tests" || no "web decode-filter tests"

# 6. The native path must still build (it is feature-gated and easy to break silently).
cargo build -q -p ciris-nl --features native 2>/dev/null \
  && ok "native feature builds" || no "native feature builds"

# 7. The interactive fracture gate must execute in native tests and compile as the same
#    raw Rust module loaded by the browser. Rendering is screenshot-gated in the release
#    artifact; this protects the physics/WASM half on every commit.
cargo test -q -p holon-ball-game 2>/dev/null >/dev/null \
  && ok "holon ball/material fracture tests" || no "holon ball/material fracture tests"
cargo build -q -p holon-ball-game --release --target wasm32-unknown-unknown 2>/dev/null \
  && ok "holon ball game -> wasm32-unknown-unknown" || no "holon ball game -> wasm32-unknown-unknown"

# 8. The multiscale sandbox. Its tests carry the certifier equivalence gate (incremental
#    vs the shipped `certify_runtime_adaptive`, bit-for-bit over one model), the five
#    planted mutants that gate has to catch, the ledger arithmetic that fixes the zoom
#    ladder, and the energy/landing gates on the solver. Same shape as gate 7: physics
#    and WASM on every commit, rendering screenshot-gated in the artifact.
cargo test -q -p holon-sandbox --release 2>/dev/null >/dev/null \
  && ok "holon sandbox certifier/ledger/solver gates" || no "holon sandbox certifier/ledger/solver gates"
cargo build -q -p holon-sandbox --release --target wasm32-unknown-unknown 2>/dev/null \
  && ok "holon sandbox -> wasm32-unknown-unknown" || no "holon sandbox -> wasm32-unknown-unknown"

# 9. The no_std core's own test suite (sectors, runtime, relativity, linalg, sparse,
#    locality, descriptor, regplus, impact, bridge, dynamics, fracture, material, field,
#    data, twin_probe, quantum_link, curvature, mechanical, gaps, holon, homogenization,
#    structure — one #[test] module per file) never actually ran under this script: gate
#    1 only builds the crate for three targets, it never tests it. ciris-sim-core IS a
#    member of this workspace, so -p reaches it directly (unlike gate 11's two
#    standalone crates, which need --manifest-path).
cargo test -q -p ciris-sim-core 2>/dev/null >/dev/null \
  && ok "ciris-sim-core test suite" || no "ciris-sim-core test suite"

# 10. The committed viewer wasm IS what the source builds. pages.yml ships the
#     committed binary verbatim with no Rust toolchain in CD, so "what ships is what
#     was gated" holds only if this comparison holds — a 503-byte counterexample sat
#     in the tree until the Jules triage (JULES_3D_TRIAGE.md F6) found that nothing
#     anywhere compared the artifact to its source.
#
#     2026-08-24 postmortem (the "206-byte cross-machine delta"): this gate was never
#     wrong and the two machines were never in disagreement. The committed binary had
#     been built, and then committed, from a WORKING TREE that had uncommitted changes
#     staged in a sibling crate (ciris-sim-core: fracture.rs/impact.rs) belonging to a
#     concurrent, unrelated task sharing this checkout — so the commit shipped a wasm
#     that no clean checkout of its own claimed source can reproduce. CI's checkout is
#     always clean, so it correctly rejected the binary; a "local" rebuild done in the
#     same contaminated tree just reproduced the same contamination and looked like
#     agreement.
#
#     HERMETIC BY CONSTRUCTION (fixed 2026-08-24): the gate used to run build-web.sh
#     straight at the tracked path and `git checkout --` it on failure — a lane-visible
#     mechanism for destroying another lane's uncommitted work in this shared tree
#     (this is the one known mechanism behind a lane's WIP going missing during the
#     outage window; attribution to this gate specifically was never provable, but the
#     mechanism was real and is now gone). The gate now builds to a throwaway scratch
#     path via build-web.sh's HOLON_SANDBOX_WASM_OUT override and diffs bytes straight
#     out of `git show` — it never writes to, and never runs `git checkout` on, the
#     tracked file. This retires the interim rule that ci-gates.sh may only run in a
#     clean worktree; the shared tree's contamination is still a bug in whatever writes
#     uncommitted changes across lanes, but it can no longer be THIS gate's fault.
built_wasm=$(mktemp)
trap 'rm -f "$built_wasm"' EXIT
HOLON_SANDBOX_WASM_OUT="$built_wasm" bash crates/holon-sandbox/build-web.sh >/dev/null 2>&1
if git show "HEAD:./crates/holon-sandbox/viewer/holon_sandbox.wasm" 2>/dev/null | cmp -s - "$built_wasm"; then
  ok "holon sandbox committed wasm matches its source"
else
  # Diagnostic on failure: a blind byte-mismatch cannot be debugged from a CI log.
  echo "    committed: $(git show "HEAD:./crates/holon-sandbox/viewer/holon_sandbox.wasm" 2>/dev/null | sha256sum | cut -c1-16) ($(git show "HEAD:./crates/holon-sandbox/viewer/holon_sandbox.wasm" 2>/dev/null | wc -c) bytes)"
  echo "    built:     $(sha256sum "$built_wasm" | cut -c1-16) ($(wc -c < "$built_wasm") bytes)"
  echo "    rustc:     $(rustc -V)  host: $(rustc -vV | grep host)"
  no "holon sandbox committed wasm matches its source (rerun build-web.sh and commit, FROM A CLEAN TREE)"
fi
rm -f "$built_wasm"
trap - EXIT

# 11. holon-swarm and holon-mesh each carry their own `[workspace]` table (deliberately —
#     see their Cargo.toml headers: it lets either be built and torn down without
#     touching THIS manifest, which several lanes edit). That also means `-p
#     holon-swarm`/`-p holon-mesh` from this workspace root cannot resolve to them —
#     there is no such package in this workspace's graph — so neither crate had ever
#     been reached by this script. --manifest-path reaches each on its own terms. Same
#     shape as gates 7/8: run the tests, then build the release artifact the crate
#     actually ships (a native bin; neither claims a wasm target).
cargo test -q --manifest-path crates/holon-swarm/Cargo.toml 2>/dev/null >/dev/null \
  && ok "holon-swarm determinism/mutation tests" || no "holon-swarm determinism/mutation tests"
cargo build -q --manifest-path crates/holon-swarm/Cargo.toml --release 2>/dev/null \
  && ok "holon-swarm swarm_bench builds" || no "holon-swarm swarm_bench builds"

cargo test -q --manifest-path crates/holon-mesh/Cargo.toml 2>/dev/null >/dev/null \
  && ok "holon-mesh mutation/bit-identity tests" || no "holon-mesh mutation/bit-identity tests"
cargo build -q --manifest-path crates/holon-mesh/Cargo.toml --release 2>/dev/null \
  && ok "holon-mesh mesh_bench builds" || no "holon-mesh mesh_bench builds"

exit $fail
