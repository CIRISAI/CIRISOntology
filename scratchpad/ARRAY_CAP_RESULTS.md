# RESULTS — CIRISArray cap-compliance + ceiling fraction

Pre-registration frozen and committed at `0538346` **before** any run
(`scratchpad/ARRAY_CAP_PREREG.md`). Substrate: the ACTUAL CIRISArray GPU kernel
(`/home/emoore/CIRISArray/src/runtime.py`, `Ossicle.KERNEL_CODE`) on the RTX 4090 Laptop
GPU. 124 pre-registered readings + 2 refuters. Scratchpad only.

---

## VERDICT

**JOB 1 — CAP COMPLIANCE: PASS.** 124/124 readings comply with the cap proved in
`Core/ShareK.lean`. Zero violations, zero headline-cap exceedances, both engine steps hold
numerically everywhere. The share pipeline does **not** manufacture super-classical values
on classical hardware. The Bell claim's instrument passes its matched control — with one
honest limitation, stated below: the hardware never drove the cap closer than 36 % of it,
so compliance was **confirmed but not stringently stressed**.

**JOB 2 — CEILING FRACTION: essentially zero.** Everywhere the reading is
boundary-stable, tie-clean and non-trivial, real coupled dynamics uses **≈ 0.03 % of the
machine-checked classical ceiling** (largest such reading: share = 2.7 × 10⁻⁴ nats against
the k = 3 cap of ln 2). Under the smooth boundary, the largest whole-only share anywhere
on the whole coupling dial, at any k, is **0.002 nats** — and it does not clear its own
null. The array is a classical substrate that sits at the floor of a ceiling it is
provably not allowed to cross, and it does not come near it.

**A pre-registered VOID condition FIRED** (reported loudly, as pre-committed), and a
**prior repo result is materially damaged** by the boundary discriminator. Both below.

---

## JOB 1 — cap compliance

| check | result |
|---|---|
| readings | 124 |
| violations of proved robust cap `k·ln2 − H(pair)` | **0** |
| exceedances of headline cap `(k−2)·ln2` | **0** |
| engine `H(pair pushforward) ≤ H(whole)` (`entropy_map_le`) | HOLDS, all readings × all C(k,2) pairs |
| engine `H(maxent) ≤ k·ln2` | HOLDS, all readings |
| tightest margin to the robust cap | 0.442 nats (P3-inject, clip) |
| largest share seen anywhere on hardware | 0.3067 nats (T5-state, κ = 0.35, clip) vs robust cap 2.2298 |

The headline cap's hypothesis was **audited, not assumed**: at high coupling the pair
marginals do become non-uniform (the robust cap rises to 0.84–2.62 as `H(pair)` falls), so
the two caps separate — but the measured share never approached either, so the
pre-registered CAUTION branch (exceeding `(k−2)·ln2` with non-uniform pairs) never
triggered.

### The stress test did not stress the cap — say so plainly

`P3-inject` was included precisely so the bound would be tested **at** the bound: the
three-coin parity state saturates the k = 3 cap exactly (`share_parity` = ln 2). On
hardware it reached only **share = 0.2511 = 36.2 % of the cap** (margin +0.442). This
reproduces `bench_results.md` (C3 = 0.263 at f = 1) and its caveat 2 — real hardware noise
eats ~60 % of the ideal parity. So the strongest honest statement is: the pipeline was
verified compliant across four orders of magnitude of share, but was **never driven within
0.44 nats of the proved bound on hardware**. The bound *was* exercised exactly at
saturation in the GATE, on exact distributions:

- k = 3 exact parity → share = 0.693147180560 = the cap, to 1e-12 (saturates, never crosses).
- k = 5 exact pair-uniform code state → share = 1.386294361120 = **2·ln 2**, reproducing
  the exact classical maximum of `CLASSICAL_MAX_K5.md` to 1e-12, and sitting below the
  proved 3·ln 2 cap.
- `shareK` at k = 3 equals `bench_detector.C3` to **0.0** on 20 random states — the same
  pipeline, not a lookalike.

---

## THE PRE-REGISTERED VOID CONDITION FIRED

The prereg states: if the architecturally-uncoupled controls fire at z > 5, "the run is
VOID … (false positive on channels that cannot physically be coupled)". **They fired.**
Four readings, all under CLIP, all at κ ≥ 0.35: S5-phase κ = 0.50 (z = 31.2), S3-phase
κ = 0.35 (z = 17.7), S5-phase κ = 0.35 (z = 14.8), S3-phase κ = 0.50 (z = 7.3). These are
disjoint ossicle groups, and the kernel gives ossicles **no** mutual coupling.

### Refuter (DIAG B) — cross-run control, and the cause is identified

Channels were rebuilt from **two independent runs** (different seeds, identical
parameters): guaranteed independent, identical marginals, identical autocorrelation. If
the null were sound, this must floor.

| κ | boundary | τ_int of the channel | within-run z | **cross-run z** |
|---|---|---|---|---|
| 0.05 | clip | 1.09 | −0.8 / 1.0 | −0.7 / 0.7 |
| 0.20 | clip | 1.00 | −0.7 / −0.9 | −0.5 / −0.5 |
| 0.35 | clip | **87.4** | 17.7 / 16.6 | **2.8 / 18.6** |
| 0.50 | clip | **365.0** | 7.2 / 35.2 | **29.8 / 34.9** |
| 0.35 | fold | 1.05 | 2.6 / 0.7 | −0.7 / 2.6 |
| 0.50 | fold | 1.00 | −0.6 / 1.3 | −0.2 / −0.2 |

Channels that **cannot** share structure fire at z = 34.9. The cause is exact: under clip
at κ ≥ 0.35 the integrated autocorrelation time of the readout explodes to 87 and 365, so
at T = 6000 the effective sample size is ~70 and ~16. The iid multinomial surrogate is
under-dispersed by roughly that factor and the z is meaningless. This is the standing
whole-only/autocorrelation trap, refired on a new substrate and caught by the
pre-registered control.

### Scope of the VOID — stated precisely, not narrowed quietly

- **VOID**: every surrogate-null z, and therefore every significance statement, for
  **clip at κ ≥ 0.35**. Those readings are also tie-contaminated (tie ≈ 0.14) and
  boundary-unstable, so they were already excluded three ways over.
- **NOT void — and this is a fact about the test, not a rescue**: the JOB 1 cap-compliance
  verdict uses **no null at all**. `share_obs` and both caps are computed deterministically
  from the same empirical distribution `p̂`; the theorem applies to `p̂` whatever its
  provenance. All 124 readings, including the voided ones, are cap-compliant. The
  compliance verdict stands.
- **Validated**: the null is sound where τ_int ≈ 1 — all κ ≤ 0.20 and all fold conditions
  (cross-run |z| < 3 throughout). Every quoted JOB 2 number lives in that region.

---

## JOB 2 — ceiling fraction

`CF = (share − null_mean) / cap`, bias-corrected. Only entries that are clip/fold STABLE,
non-trivial (the clamp actually binds), and tie-clean are quoted.

**Clamp-binding rate by coupling** (fraction of clamp applications that actually bound):

| κ | 0.00 | 0.02 | 0.05 | 0.10 | 0.20 | 0.35 | 0.50 |
|---|---|---|---|---|---|---|---|
| clip | 0 | 0 | 2.4e−5 | 2.0e−2 | 1.4e−1 | 2.8e−1 | 3.7e−1 |
| fold | 0 | 0 | 3.1e−5 | 2.3e−2 | 1.6e−1 | 2.4e−1 | 3.5e−1 |

At κ ≤ 0.02 the clamp never binds, so clip and fold are *the same function on the data that
occurred*; agreement there is **TRIVIAL** and carries no information, exactly as
pre-registered.

### The quotable measurements

| reading | κ | share (clip) | share (fold) | CF vs proved cap | z clip / fold | verdict |
|---|---|---|---|---|---|---|
| S3-state (spatial k=3, the real a—b—c chain) | 0.10 | 2.72e−4 | 1.78e−4 | **0.039 % / 0.026 %** | 246 / 159 | STABLE |
| X5-state (spatiotemporal k=5) | 0.10 | 2.58e−4 | 1.57e−4 | **0.012 % / 0.007 %** | 137 / 88 | STABLE |
| S3-phase (uncoupled control) | 0.05, 0.10 | ~0 | ~0 | −0.01 % | <1 | STABLE, floor |
| S5-phase (uncoupled control) | 0.05 | ~0 | ~0 | +0.03 % | <2 | STABLE, floor |

**The answer to JOB 2: ~0.03 % of the machine-checked classical ceiling, at the one
coupling where a genuinely coupled reading is boundary-stable and the clamp is active.**
The two boundaries agree in order of magnitude but only within a factor of ~1.5
(2.7e−4 vs 1.8e−4) — disclosed rather than hidden behind the STABLE label; see the
criterion caveat below.

At k = 5 both tiers are reported and not blurred: the proved cap is 3·ln 2 = 2.0794, the
exact classical maximum is 2·ln 2 = 1.3863. X5-state at κ = 0.10 is 0.012 % of the former,
0.019 % of the latter.

### Everything that looked large is an artifact, by three independent criteria

The largest hardware shares — T3-state CF = 0.245, T5-state CF = 0.148, X5-state
CF = 0.107, all at κ = 0.35 clip — fail on all three pre-registered grounds at once:
the fold variant reports **0.00000** (z ≈ 0) at the same coupling; the tied fraction is
0.14, fourteen times the pre-registered 0.01 threshold; and the surrogate null is void
there (τ_int = 87). **Under the smooth boundary the maximum share anywhere on the entire
dial, at any k, is 0.002 nats, and it does not clear its own null.**

### Why the temporal readings had nothing to measure

At the shipped operating point the kernel runs **100 logistic iterations per burst** at
r = 3.70. Measured τ_int ≈ 1.00 at every κ ≤ 0.20 and under fold everywhere: successive
measurements are fully decorrelated. So the array as shipped presents **no temporal
structure at its own measurement cadence**, and the trap's "expected" temporal order-3
never appeared except through the clamp. This is a property of the device's readout
cadence, not evidence about order-3 in coupled-logistic dynamics generally.

---

## MATERIAL FINDING ABOUT A PRIOR RESULT — the adversary-channel bench demo

`bench_results.md` records VERDICT **SUCCESS** for the adversary-channel bench demo, and
its prereg states the injection is "a smooth parameter modulation, **NOT** a clip/threshold
readout nonlinearity (clip-boundary lesson honored)". The boundary discriminator says
otherwise.

Re-running that exact construction (f = 1, δ = 0.10 coupling modulation, T = 4000) under
both boundaries — **DIAG A**:

| boundary | bit recovery A,B,C | d′ | channel response bit 0 → 1 | share | z |
|---|---|---|---|---|---|
| clip (native) | 0.940, 0.942, 0.938 | 3.17 | −0.0295 → −0.0012 (**+0.028**, +1.7 sd) | **0.2511** | 1362 |
| fold | 0.667, 0.676, 0.692 | 0.92 | −0.0291 → −0.0368 (−0.008, −0.8 sd) | **0.0010** | 4 |

The clip arm reproduces `bench_results.md` exactly (recovery .94/.94/.94, C3 ≈ 0.25–0.26).
Replacing only the clamp with a reflecting fold — nothing else changed — drops recovery to
chance-plus and the recovered share by a factor of 259, and **reverses the sign** of the
channel's response to the injected bit.

**What this does and does not mean.** It is *not* a false positive: the parity was
externally constructed, and the f = 0 negative control floors. The detection was real. What
is not supported is the mechanism claim. The modulation was smooth *in the parameter*, but
the parameter's path to the readout runs substantially **through the clamp** — raising
coupling pushes more cells onto the 0.001/0.999 rails, pinned cells are perfectly
correlated, and the phase metric (mean pairwise correlation across cells) jumps. The
demo therefore honoured the clip-boundary lesson in intent and not in fact, and its
headline number is boundary-specific rather than a property of the array's dynamics.

Recommendation for Eric's review: `bench_results.md` should carry this as a correction to
its caveat list, and any promote it pays should be re-scoped to "demonstrated on this
kernel's native clamped readout" rather than to the array's dynamics as such. **Not
actioned here** — no stance file, Lean file, or prior result has been edited.

---

## Pre-registration flaw found in execution (disclosed, post-hoc repair marked)

The stability criterion's relative-difference clause (`rel > 1.0 ⇒ ARTIFACT`) was written
assuming CF of order 0.1. At readings sitting on the estimator floor, CF ≈ ±1e−6, and the
clause divides one noise value by another — so it labels pure floor-vs-floor agreement
"ARTIFACT" (e.g. S3-state at κ = 0.05: CF −5e−7 vs +5e−7, both |z| < 1). Those labels are
artifacts of the criterion, not findings. The substantive artifact calls — the ones this
report relies on — are those where one arm fires at z ≫ 5 and the other does not
(κ = 0.20, 0.35, 0.50). This is a **post-hoc reading of a pre-registered rule**, flagged as
such; no threshold was moved and no verdict was changed by it.

---

## What is NOT claimed

- **No discovery of order-3 / whole-only structure in the array.** Pre-committed in the
  prereg and honoured. The only large order-3 readings are clamp artifacts, and the small
  boundary-stable ones (2.7e−4 nats) are reported as a *magnitude against a ceiling*, not
  as a finding — order-3 in a nonlinear lattice is expected and is not news.
- **No world-claim.** This is an instrument control plus a measurement of one engineered
  device. Nothing here bears on the Logos claims, on `adequacy` (engineered, not nature),
  or on `third-in-tsvf` (quantum, needs a quantum apparatus).
- **No proof that the pipeline is correct in general** — only that on 124 real-hardware
  readings plus 8 exact gate cases it never violated the proved bound. Compliance is
  evidence against a specific failure mode, not a correctness proof.
- **No claim the cap was stringently tested on hardware**: 36 % of the cap is the closest
  approach. The saturating tests are synthetic (GATE).
- **IAAFT was not used** and its absence is not a gap: a clip artifact survived IAAFT at
  z = 86 on 2026-07-24, so its survival certifies nothing.

## Honest caveats

1. SR noise (σ = 1e−3) is injected between the kernel's 100-iteration bursts, not
   per-update — the kernel has no per-iteration hook. Same caveat as `bench_results.md`.
2. The CLIP arm runs the shipped kernel's arithmetic **verbatim** with a clamp-event
   counter appended; the counter does not enter the state update. The FOLD arm changes
   only the three clamp expressions. Both were asserted present before substitution — the
   script refuses to guess.
3. The device has no native 5-slot spatial structure (cells and ossicles do not interact;
   only a—b—c couples). Stated in the prereg before the run, so the k = 5 spatial floor is
   not retrofitted as a finding.
4. Median binarization forces exact channel balance, which injects ~0.1 % random flips per
   channel and costs ~e·ln(1/e) of share (visible in GATE (7): 0.673 vs the ideal 0.693).
   This biases the ceiling fraction **downward**, the safe direction for a compliance test.
5. Temporal windows: non-overlapping stride-k is primary; the overlapping variant is
   recorded and agrees.
6. Replication at κ = 0.05 across seeds 20260725 / 99 / 7: all readings at the floor,
   |CF| < 3e−4, consistent across seeds.

## Files

- `scratchpad/ARRAY_CAP_PREREG.md` — frozen prereg, committed `0538346` before any run
- `scratchpad/array_cap_experiment.py` — gate, kernel variants, sweep
- `scratchpad/array_cap_diagnostics.py` — DIAG A (bit recovery) and DIAG B (cross-run refuter)
- `scratchpad/summarize_array_cap.py` — applies the pre-registered verdict rules
- `scratchpad/array_cap_results.json`, `scratchpad/array_cap_diagnostics.json` — machine-readable
