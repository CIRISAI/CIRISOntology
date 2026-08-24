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

# 10. The committed viewer wasm IS what the source builds. pages.yml ships the
#     committed binary verbatim with no Rust toolchain in CD, so "what ships is what
#     was gated" holds only if this comparison holds — a 503-byte counterexample sat
#     in the tree until the Jules triage (JULES_3D_TRIAGE.md F6) found that nothing
#     anywhere compared the artifact to its source. build-web.sh overwrites the
#     committed path, so the gate is: rebuild, then require a clean diff.
#
#     2026-08-24 postmortem (the "206-byte cross-machine delta"): this gate was never
#     wrong and the two machines were never in disagreement. The committed binary had
#     been built, and then committed, from a WORKING TREE that had uncommitted changes
#     staged in a sibling crate (ciris-sim-core: fracture.rs/impact.rs) belonging to a
#     concurrent, unrelated task sharing this checkout — so the commit shipped a wasm
#     that no clean checkout of its own claimed source can reproduce. CI's checkout is
#     always clean, so it correctly rejected the binary; a "local" rebuild done in the
#     same contaminated tree just reproduced the same contamination and looked like
#     agreement. Confirmed by building from a `git worktree` pinned to the failing
#     commit, isolated from the shared tree: that build is byte-identical to CI's.
#     Lesson: this gate's rebuild-and-diff is only meaningful against a clean tree —
#     `git status --porcelain` on the crates this binary depends on, checked BEFORE
#     trusting a local pass, not just after a CI failure.
wasm_committed_sha=$(git show "HEAD:./crates/holon-sandbox/viewer/holon_sandbox.wasm" 2>/dev/null | sha256sum | cut -c1-16)
bash crates/holon-sandbox/build-web.sh >/dev/null 2>&1
if git diff --exit-code --quiet -- crates/holon-sandbox/viewer/holon_sandbox.wasm; then
  ok "holon sandbox committed wasm matches its source"
else
  # Diagnostic on failure: a blind byte-mismatch cannot be debugged from a CI log.
  echo "    committed: $wasm_committed_sha ($(git show "HEAD:./crates/holon-sandbox/viewer/holon_sandbox.wasm" | wc -c) bytes)"
  echo "    built:     $(sha256sum crates/holon-sandbox/viewer/holon_sandbox.wasm | cut -c1-16) ($(wc -c < crates/holon-sandbox/viewer/holon_sandbox.wasm) bytes)"
  echo "    rustc:     $(rustc -V)  host: $(rustc -vV | grep host)"
  git checkout -- crates/holon-sandbox/viewer/holon_sandbox.wasm
  no "holon sandbox committed wasm matches its source (rerun build-web.sh and commit, FROM A CLEAN TREE)"
fi

exit $fail
