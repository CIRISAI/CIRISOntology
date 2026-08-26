# Pre-registration — THE COMPOSITION TEST: one frozen model, multiple substrates, zero refits

**2026-08-26, frozen before any instrument for it exists and before any new data is
read.** This is the test `OBJECT_PRIOR_ART.md` names as the only thing on trial, and it
is built to reach one of two exits. Its verdict goes on the public page either way.

## 0. The two exits, first

- **CONFIDENCE:** the frozen model's staked predictions land on every posable arm of
  ≥2 independent substrates with zero refits, zero view changes — and the declared
  economy comparison favors or ties it against per-substrate alternatives. Then the
  composition claim is MEASURED and "unusually rigorous synthesis" upgrades to
  "framework" on the page.
- **FALSIFICATION:** any substrate requires a refit, view change, or post-hoc
  parameter to avoid a miss. Then **the maximal object is a NOTATION** — a useful
  vocabulary, not a structure — and `OBJECT_PRIOR_ART.md`'s standing verdict becomes
  the page's permanent wording. No third outcome is available: partial results are
  reported per-substrate and the composition claim stays UNPROVEN, explicitly.

## 1. THE FROZEN MODEL (all parameters fixed here; none may move)

**M — the fiber closure model**, five laws:

1. **Detector.** Coarse view = the substrate's declared two-state bit (sign /
   threshold learned on train split only). Fibers = within-state position rank (8) ×
   backward-difference velocity rank (5) at the substrate's analysis rate (the
   validated 20–55 kHz-equivalent regime; for non-temporal substrates, the native
   step). Gain = held-out log-loss improvement; floors from a matched planted-truth
   gauge run per substrate BEFORE unblinding; below 5× floor ⇒ BELOW-FLOOR, never a
   detection.
2. **Independence law** (`both_closed_iff_product` + atlas S2). Non-interacting
   sectors: both directional defects at floor. Directed coupling: forward defect
   ≥ 20× the reverse. Reciprocal: both above floor. **Common driver: both directional
   defects at floor while created correlation `I(A′;B′|A,B)` is above floor** — the
   signature that separates closure (directed influence) from correlation.
3. **Timescale law.** The defect/energy-identity persistence dies at the substrate's
   own relaxation time, measured independently per substrate (a declared calibration,
   not a fit), within the gauged ruler factor: staked band **[τ/2.5, 2.5τ]** carrying
   the 2.45× calibration.
4. **Rent law.** Where per-event work exists: ΔW(Q4−Q1 of initial |v|) = ΔKE by
   equipartition calibration, ratio ∈ **[0.5, 2]**.
5. **Trained-robustness law.** A controller optimized for repeated operation reads
   rent-ratio **< 0.5** and **anti-correlates** successive energies (m=1 corr < 0).
   Corollary for substrate physics: on an OVERDAMPED substrate the velocity fiber is
   degenerate — position-fiber gain ≥ 5× velocity-fiber gain.

## 2. The substrates and their staked predictions

**S1 — QPU four-arm + common-driver** (`ibm_marrakesh`, ~543 s quota; screened pair;
one job, arms interleaved; permutation floors, Bonferroni over the arm count):
| arm | frozen prediction (law 2) |
|---|---|
| idle | both defects at floor |
| one-way CRX | forward ≥ 20× reverse; forward ≥ 50× floor |
| reciprocal CRX | both ≥ 20× floor |
| **common-driver** (shared classical bit drives X on both, two sub-circuits pooled 50/50) | **both directional defects at floor AND created correlation above floor** |

**S2 — the engine** (holon-sandbox granular dynamics; this is also the owed tier
closure certificate): (i) two non-interacting granular regions: both region-views
closed (law 2); (ii) interacting regions: defect ≥ 5× floor; (iii) the coarse
tier-view's defect contracts at the measured velocity-autocorrelation time within
band (law 3); (iv) `Aggregation`'s `K ≤ 1` measured for the declared tier map — the
horizontal-scaling condition, adjudicated as measured-true or measured-false.

**S3 — CONDITIONAL: the optimal-protocol tweezers dataset** (Zenodo 19705797,
overdamped). Gate: `data.npz` must contain per-trajectory position series and
per-trajectory work; else **S3 VOID**, declared not dropped. If posable: law 5's
corollary (position ≥ 5× velocity fiber gain — the overdamped inversion of the
underdamped result, a cross-substrate DISCRIMINATING prediction) and law 4 if work
per trajectory exists.

## 3. The economy comparison, declared

Per substrate: BIC-style two-part score = held-out log-loss + (k/2)·ln n for each
model's free parameters. The frozen model claims **k = 0** per substrate (its
calibrations — floor gauge, relaxation time, equipartition — are measured constants,
declared, not fitted to the staked quantities). The alternative: a per-substrate
2-parameter tuned variant (free threshold, free bin count, chosen post-hoc on the
same data). PASS = the frozen model's score ≤ the alternative's on every substrate
where both are computable; report all numbers.

## 4. Tree

- Gauges per substrate (planted truth) run BEFORE unblinding; STOP per substrate if
  the estimator does not transfer; a stopped substrate is VOID, and the composition
  test proceeds only if ≥2 substrates remain posable — else the whole test is VOID
  (question not posed), never a pass.
- S1 job VOID on device error → one unchanged resubmission, recorded.
- Any arm's miss is FINAL. The no-rescue clause is the falsification exit: a miss
  plus a repair-that-would-have-worked is still a miss; the repair goes in a NEW
  prereg against NEW data, and this test's verdict stands.
- Family-wise: Bonferroni 0.05/(number of staked arms across posable substrates),
  computed and printed by the instrument before unblinding.

## 5. What this is not

Not a test of the Lean theorems (mathematics; data cannot touch them). Not a claim of
new physics on any single substrate — every law is individually conventional or
already measured. **The only claim on trial is composition**: that ONE frozen
structure spans substrates that currently require separate descriptions. That is
exactly the claim whose absence keeps the object a wager.
