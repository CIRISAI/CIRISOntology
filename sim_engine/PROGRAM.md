# THE PROGRAM — three paths from 2026-08-23

Pure dependencies, no dates. Common trunk first; the three paths run in parallel after it.
House rules bind throughout: pre-register, separable kills, mutation-test every gate,
misfit → cash into the metaphysics, everything back into the Lean.

## Trunk (now): one clean main
T1. Frozen agents commit — **items defined by artifact, 2026-08-24.** The original shorthand
    ("E1 fracture; axial P2; SR+curvature slice") was defined NOWHERE in the repository, so
    "N-a done" was never checkable against a written definition: a rung marked green against
    prose. Naming the artifacts is the fix; a claim whose warrant is prose is not yet a claim.
    - **E1 fracture** → `ciris-sim-core/src/fracture.rs`, `fracture::` 9 tests.
    - **axial P2** → `ciris-sim-core/src/homogenization.rs`, `homogenization::` 4 tests.
      **NARROW FORM ONLY**, in the module's own words: it "closes the narrow form of P2
      without inventing another calibration constant" (`homogenization.rs:3`); `:145` and
      `holon-sandbox/src/scene.rs:315` both hedge that a number outside the positive-softening
      branch "would be papering over P2". **A narrow-form closure is not a closure**, and the
      hedge belongs on this spine, not only in the source.
      **NOT AN INDEPENDENT WITNESS**: this is the same work as N-b's ν = 0.24 wiring below
      ("merge homogenization.rs → demo realizes DEMO_CALIBRATION's real ν"). One witness, not
      two — the shared-lemma over-grade, caught here on the spine rather than in a campaign.
    - **SR+curvature slice** → `ciris-sim-core/src/{relativity,curvature}.rs`, `relativity::` 12
      and `curvature::` 7 tests. **Mapping RECONSTRUCTED 2026-08-24, not original**: the phrase
      is defined nowhere, so this is the best available reading of which artifacts it meant, not
      a verified correspondence. Struck or corrected by anyone who knows the original intent.
    All counts inside the 165/165 `--features alloc --release` run at `0d1a59c`.
T2. Merge the four branches: research/dm-gauge-vacuum (repaired, verified),
    research/factorization-kills (repaired, verified), feat/holon-closure-repairs
    (112/112), TEMP-revert already on main. Resolve lib.rs unions.
T3. Adopt FactorizationKill's REPAIR formally: whole-only is FACTORIZATION-RELATIVE —
    one REG_GAPS line; the frame (M15/M20) already says it, the kill makes it mandatory.

## PATH K — fastest kill (independent items, all parallel)
K1. **CLOSED 2026-08-23 — KILLED** (`929ad8a`, on main). Route → gauge identification dies
    on its own pre-registered criterion: the decomposition H(φ) = (U + U†) + (e^{iφ}U² + h.c.)
    is exact but worthless as evidence, because the truncated ladder generates the full 3×3
    algebra. A route-side diagonal gauge move that changes no observable relocates the phase
    out of the flux-change-2 corner, and the Gauss-generated link gauge flow can follow only
    if the Wilson phase is trivial — so the grading, the entire gauge content of the proposed
    map, is pinned to the hand-selected R1 representative. Survivors, exactly: link charge
    conjugation = route time reversal with exact amplitude pairings; and no similarity carries
    the nilpotent ladder onto the cyclic shift. 29 theorems, sorry-free, standard axioms.
    **Pre-commitment honoured: shared-fundamental-dynamics drops below 15%.**
K2. **CLOSED 2026-08-23 — KILLED** (`scratchpad/h3ere2_eval/RESULTS_K2.md`, tracked).
    VERDICT: NOT SUPPORTED, within its pre-committed scope. C over B = 0.531 (26W/23L of 49
    decisive), paired sign test p = 0.775 — rules out a large effect, cannot exclude a modest
    one (<0.58). Soft encoding did not change the verdict, so the categorical bottleneck was
    not the limiting factor. Scope, sealed: this falsifies THIS PIPELINE's use of the engine
    for response generation, not the engine, taxonomy, or classifier.
    **The secondary result is larger than the primary and is a product-direction finding:
    the scaffold does not merely fail to help, it COSTS quality.** C is significantly worse
    than the bare 0.6B model — win rate 0.303, p = 0.0019 (gold 0.362, p = 0.0295) — while
    spending ~40% more tokens (78 vs 56) and ~40% more wall time. Per this file's own
    cross-path coupling, that feeds the CIRIS UI direction regardless of sign.
    OWED, not blocking: the verdict rests on ONE judge — the secondary (qwen3:14b) was
    DISQUALIFIED on both gates (identical-pair slot-1 = 1.000; sensitivity 0.870 against a
    0.90 bar) and judged no real pairs, so the protocol's split-verdict provision never ran.
    A second qualified judge is **firming a fired kill, not re-running one**, and is picked
    up after Q9 closes.
    **REPRODUCIBILITY, recorded here because a reader of this spine sees CLOSED-KILLED and
    reasonably infers a reproducible result. THE KILL'S NUMBERS STAND** — they rest on
    committed judgment artifacts (`scratchpad/h3ere2_eval/judge_*.jsonl`, `RESULTS_K2.md`),
    unaffected by any of the below. **But the RESPONSES ARE NOT REGENERABLE from the
    repository as of 2026-08-24.** The build check owed with `9f95754` was discharged by
    k2-judge with a NEGATIVE: `bin/generate` fails to compile at HEAD. Two causes, both in
    `ciris-nl`, both named in RESULTS_K2 deviation #2 as "code uncommitted, for review" —
    (A) nothing declares `pub mod chat;` though `chat.rs` is committed, and (B)
    `Session::generate` does not exist: `native.rs` carries only a private, llguidance
    JSON-grammar-constrained `complete()`, not the free-text generator the eval calls. (B)
    was reconstructed from a shipped binary's embedded fragments, never committed, and is
    now gone from the worktree as well (stash empty, no surviving binary) — **LOST, not
    merely unwired.** Anyone re-running K2 end to end gets as far as `bin/paths`.
    Repair assigned to k2-judge, (A) and (B) to land in one commit. **If the generator
    cannot be faithfully rebuilt, that becomes permanent and this entry must say so** — a
    plausible reconstruction that silently differs from the one which produced these
    responses would be worse than the loss, because it would look like regenerability
    without being it.
K3. **Modular locality at 2–3 plaquettes.** quantum_link + the Jacobi path at growing
    size; kill = modular locality fails to persist beyond one link. Their own 30% line.

## PATH N — all of Newton (serial where shown)
N-a. Land frozen work [= T1].
N-b. (k_n, k_t) wiring: merge homogenization.rs → demo realizes DEMO_CALIBRATION's real
     ν = 0.24 (the stencil's ν = 1/3 Cauchy restriction is the measured reason scalar
     stiffness was never enough) → THEN P3 knob rerun → P4 specimen pin.
N-c. MEET-2: T4 rigid chart ↔ T5 Newtonian chart over the same holon, Rapier as the
     limiting-case control. Needs N-a (curvature slice) + E2 (done).
N-d. **N1, the aggregation theorem** — fine REG+ evolution bounded by a
     boundary-supported residual. locality.rs's z^d/d! bound is the executable shape;
     the Lean theorem is the deepest single item on the board and the certificate's
     mathematical warrant.
N-e. Full fracture composition: E1 adaptive crack-tip + node-node contact + derived
     (k_n, k_t) laws, certified end to end (B4 regimes B/C).
     **GREEN, with FOUR independent checks — and one claim explicitly NOT among them.**
     Verified `4262553` (165/165, prize gate 3.91 mm ≤ 4.27 required) and `5471bea`
     (190/190). The four checks are the first things here that are not the engine checking
     itself: two LOOSE — the momentum window (J = 6.609 inside [3.6, 7.2] N·s) and the
     energy inequality — and two SHARP — an **exact** Griffith bound and a **measured**
     fracture threshold (between 2.50 and 4.00 m/s) with a sub-threshold elastic anchor
     (zero crack area, impulse 1.8594 inside [1.000, 2.000] N·s, restitution 0.859).
     The Griffith bound accumulates the engine's own per-bond `law.fracture_energy_j`
     rather than estimating from `crack_area`: **fracture work 0.6737 J against KE lost
     4.8836 J.** The area estimate reads 0.5917 J, and **that 14% gap IS the quenched
     per-bond roughness** — a measured mechanism, NOT a tolerance the anchor tolerates.
     **THE MULTI-RESOLUTION CLAIM IS REFINEMENT-STABLE, NOT VERIFIED, AND THE FOUR CHECKS
     DO NOT DISCHARGE IT.** They bound the COMPOSED observables; the convergence gate is
     still three runs of one engine with no external reference — `SelfAudit` turned on
     ourselves — and that retraction stands. Recorded here because a reader meeting "N-e
     green" beside four fresh anchors would otherwise reasonably infer it settled.
     Measured and kept, not deleted: damage is **NOT monotone in the drive** (6 m/s
     exceeds 9 m/s on both crack area and fracture work). Discriminator run rather than a
     mechanism invented — all rungs certify at the same finest 0.00391 m, differing only
     in frontier EXTENT (289/277/264/228), so damage feeds extent feeds quench feeds
     damage and a 5% inversion is quench variability, not physics.
NEWTON CLOSED = N-a…N-e green, wild pins DECLARED on the closing certificate
(feldspar potential et al., per the descriptor-chain GANTT). Game/DX wiring only after.

## PATH Q — quantum sim benchmark (Q1→Q2 serial; Q3, Q4 parallel; Q5→Q6 serial)
Q1. **DONE 2026-08-23** (T2_DFT_REFERENCE.md, 617e1f2 lineage): structure +0.95%/+0.88%;
    elastic tensor 10–14% soft, SIGNED (volume mechanism), shape sub-percent. The
    few-percent-absolute class is REFUTED and the gate consumes its own bias.
Q2. B2q proper, RESHAPED by Q1's verdict: the reference cannot serve absolute C_IJ at
    ±2%, so the gate is SHAPE (sub-percent, where the reference is good) plus
    bias-consumed stiffness bands — pre-stated, signed, never symmetric.
Q3. Quantum-link scaling: exact diagonalization 1→N plaquettes; gates = Gauss exactness
    (machine), modular-locality persistence, boundary-channel entropy vs region size;
    99.9/99.9/2x against the one-plaquette closed form where it exists.
Q4. **The chemistry blind protocol** — from elemental/electronic identity +
    stoichiometric inventory ONLY, recover withheld H2O/CO2/CH4/NH3 topology; the
    fail-closed validator enforces that bond graphs never parameterize dynamics.
    Their 40% line, and the single largest probability swing on the board.

### The Q-seam (Q5–Q6, commissioned 2026-08-23) — the unique-tools play
The wrong game is out-DFT-ing DFT (Q1 measured why). The right game: **the certified
meet between a quantum reference and a classical chart** — match where certified,
REFUSE where correlation makes the chart lie. Nobody else ships refusals.
Q5. **The seam certificate.** An exact quantum reference we own (Q3's machinery: small
    exactly-diagonalizable family, e.g. Hubbard/transverse-field sweep at N small
    enough for machine-checked residuals in the vacuum-tier class, ~1e-16) + the
    Boolean-occupancy/mean-field chart over the same system (`Core/ModeChart.lean` is
    the Lean home: the cap survives mixing, Booleanity is exact only for determinate
    states). Certificate criterion staked in the prereg BEFORE the instrument; the
    chart must match the exact reference inside certified regions at staked tolerance
    and refuse outside them. GATE IS MUTATION-TESTED: a planted correlated state (the
    U-sweep's far end) must be REFUSED; a certificate that never refuses proves
    nothing. Speed clause explicitly SCOPED OUT: Q5 is a correctness product.
    KILL (separable): if no staked criterion separates certified from refused better
    than certify-everywhere, the certificate is decoration — record dead, keep marked.
Q6. **The share as the failure instrument** (research rung; prereg before computing).
    Does the whole-only/beyond-pair structure of the exact state PREDICT where the
    mean-field chart fails? Predictor and null staked first; correlated-error curve
    over the same sweep. KILL (separable, its own): share at floor where chart error
    is large — or large share where the chart is fine — across the sweep kills
    instrument-as-certificate without touching Q5.
Q-seam discipline: freeze-design-early — prereg published for attack before any
instrument runs; findings batch at avenue close (no stance edits mid-avenue); every
long computation detached (setsid + done-markers + RESUME).

## Cross-path couplings, named
- K1's outcome gates Q3/Q4's INTERPRETATION (not their execution). **This gate has now
  FIRED (`929ad8a`, 2026-08-23): route → gauge died, so the lattice work continues as
  physics and THE SHARED-CARRIER CLAIM DROPS.** Q3 and Q4 execute unchanged; anything
  written about them must not read the lattice results as evidence for a shared carrier.
- K2 is also the h3ere2 deliverable Eric originally asked for; its verdict feeds the
  CIRIS UI direction regardless of sign. **That verdict is in (2026-08-23) and the sign
  is negative twice over** — the coupling shows no large effect, and the scaffold costs
  quality against the bare 0.6B baseline. See K2 above; the finding is with Eric.
- N-d (N1) and Q2 share the homogenization-certificate shape — one theorem, two faces
  (the descriptor DAG edge downward; the dynamics aggregation upward).
