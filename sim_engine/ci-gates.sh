#!/bin/bash
# Workspace invariants, each one empirically derived rather than assumed.
# Run from the workspace root.
set -u; fail=0
ok(){ printf "  PASS  %s\n" "$1"; }
no(){ printf "  FAIL  %s\n" "$1"; fail=1; }

# 1. The no_std core must build for native and BOTH wasm targets, on its own.
#    Use -p, never --workspace: a sibling's features can pull in a C++ build script.
#
#    Same disease as gate 9's, caught in the same pass: fracture/impact/runtime/descriptor
#    are all `#[cfg(feature = "alloc")]`, and this loop only ever built DEFAULT features —
#    so the three-target BUILD guarantee never compiled the adaptive-fracture line either,
#    on any target, even though gate 9 now tests it. Fixing the test line while leaving
#    this one blind would leave half the hole open. Both feature sets, both matter: default
#    is the true no_std/no-alloc floor (a consumer with no allocator needs THIS to build);
#    alloc is what fracture/impact actually need.
for T in "" "--target wasm32-unknown-unknown" "--target wasm32-wasip1"; do
  cargo build -q -p ciris-sim-core $T 2>/dev/null && ok "core builds ${T:-native}" || no "core builds ${T:-native}"
  cargo build -q -p ciris-sim-core --features alloc $T 2>/dev/null \
    && ok "core builds ${T:-native} (alloc)" || no "core builds ${T:-native} (alloc)"
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
#
#    --features alloc is NOT optional: the crate's default feature set is EMPTY, and
#    fracture/impact/runtime/descriptor are all `#[cfg(feature = "alloc")]` — measured
#    118 tests default vs 165 under alloc, and ZERO of them fracture::/impact:: either
#    way under default. A plain `-p ciris-sim-core` here ran green while covering none
#    of the adaptive-fracture line (research-manager-2, 2026-08-24) — the gate must name
#    the feature it means to test, not the crate's cheapest build. `std` stays untested
#    by this gate; that is a separate, smaller gap (`--all-features` would close it) and
#    is not what gate 1's no_std build guarantee depends on.
#
#    --release, same reason gate 8 (holon-sandbox) takes it: impact.rs's three-leg
#    convergence test is a float-heavy numeric solver that Rust's debug profile does not
#    optimize, and it is where the suite's cost concentrates (~5 of 165 tests carry it;
#    compilation itself is cheap in either profile). This is a profile argument, not a
#    timing one deliberately — a same-environment debug-vs-release pair was going to be
#    quoted here and got pulled: two readings taken under different, uncontrolled
#    concurrent build load are not a comparison (research-manager-2, on its own numbers,
#    2026-08-24; the same defect it had just caught in an unrelated warm-start probe).
#    Debug-vs-release is a speed knob here, not a correctness one — the assertions are
#    the same either way.
#
#    SELF-VERIFYING, not self-describing (team-lead's ruling): the defect above was a
#    PROSE claim of coverage next to a COMMAND that did not deliver it — "the command
#    exits 0" cannot distinguish "fracture/impact ran and passed" from "fracture/impact
#    were never compiled in", which is exactly how 47 tests and two modules stayed
#    invisible while this gate ran green. `--list` enumerates the test binary's contents
#    without running anything, so a feature-flag regression that silently drops a module
#    fails THIS assertion instead of only living in a comment that nobody re-checks.
alloc_list=$(cargo test -q -p ciris-sim-core --features alloc --release --lib -- --list 2>/dev/null)
if printf '%s\n' "$alloc_list" | grep -q 'fracture::' && printf '%s\n' "$alloc_list" | grep -q 'impact::'; then
  ok "ciris-sim-core alloc build compiles in fracture::/impact::"
else
  no "ciris-sim-core alloc build compiles in fracture::/impact:: (feature flag regression?)"
fi
cargo test -q -p ciris-sim-core --features alloc --release 2>/dev/null >/dev/null \
  && ok "ciris-sim-core test suite (alloc) passes" || no "ciris-sim-core test suite (alloc) passes"

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

# 11. holon-swarm and holon-mesh each USED TO carry their own empty `[workspace]` table,
#     which made `-p holon-swarm`/`-p holon-mesh` from this root resolve to nothing — no
#     such package existed in this workspace's graph — so neither crate had ever been
#     reached by this script. Both are now real `members` (holon-mesh path-depends on
#     holon-swarm, so cargo refuses two workspace roots in the same graph if only one
#     joins — holon-mesh lane, measured: "multiple workspace roots found"; both joined
#     together, both empty tables removed). Plain -p reaches each directly now. Same
#     shape as gates 7/8: run the tests, then build the release artifact the crate
#     actually ships (a native bin; neither claims a wasm target).
#
#     SELF-VERIFYING (same question asked of gate 9, per team-lead's ruling — "if it can
#     pass while reaching neither crate, it has gate 9's disease"): unlike ciris-sim-core's
#     src-level `#[cfg(test)] mod tests`, these crates' interesting coverage lives in
#     tests/*.rs integration files, whose functions list with BARE names, not a
#     file-derived prefix (measured: tests/determinism.rs and tests/mutation.rs both
#     contribute unprefixed names to `--list`, so a module-prefix grep like gate 9's would
#     not distinguish "reached" from "not reached" here). A nonzero test COUNT is the
#     right assertion for THIS failure mode — "-p resolves to nothing" or "the crate
#     builds but the test binaries collect zero tests" both show up as 0, and unlike an
#     exact count it does not go red every time a test is legitimately added.
n_swarm=$(cargo test -q -p holon-swarm -- --list 2>/dev/null | grep -c ': test$')
[ "${n_swarm:-0}" -gt 0 ] \
  && ok "holon-swarm reaches $n_swarm tests" \
  || no "holon-swarm reaches 0 tests (gate 9's disease: passing without covering anything)"
cargo test -q -p holon-swarm 2>/dev/null >/dev/null \
  && ok "holon-swarm determinism/mutation tests" || no "holon-swarm determinism/mutation tests"
cargo build -q -p holon-swarm --release 2>/dev/null \
  && ok "holon-swarm swarm_bench builds" || no "holon-swarm swarm_bench builds"

n_mesh=$(cargo test -q -p holon-mesh -- --list 2>/dev/null | grep -c ': test$')
[ "${n_mesh:-0}" -gt 0 ] \
  && ok "holon-mesh reaches $n_mesh tests" \
  || no "holon-mesh reaches 0 tests (gate 9's disease: passing without covering anything)"
cargo test -q -p holon-mesh 2>/dev/null >/dev/null \
  && ok "holon-mesh mutation/bit-identity tests" || no "holon-mesh mutation/bit-identity tests"
cargo build -q -p holon-mesh --release 2>/dev/null \
  && ok "holon-mesh mesh_bench builds" || no "holon-mesh mesh_bench builds"

exit $fail
