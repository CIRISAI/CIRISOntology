# Pre-registration — fiber-closure robustness battery on the OT_arHMM trace, WITH ITS DECISION TREE

**2026-08-26, frozen before any battery cell runs.** This prereg practices the
correction Eric issued the same day: the contingent follow-up for every named outcome
is PRE-COMMITTED here, in one tree. A rescue is post-hoc reinterpretation; a branch is
design. No branches other than these run.

## 0. The pilot being hardened, at its honest strength

`fiber_pilot.py` + `fiber_pilot_results.json` (AS-REPORTED from Eric's external
session; the dataset is not in this repository). Reading: within-fiber witness data
(force rank, backward velocity) improves held-out prediction of the future coarse
state by 0.015–0.040 bits/sample at 0.1–5 ms (12–22 % of baseline log-loss),
block-bootstrap CIs excluding zero, and the gain contracts away by 20–100 ms. In the
ladder's terms: the two-state view's fibers are split by the dynamics at short
horizons, and the split contracts on a finite timescale — the first WILD-data fiber
reading.

**Caveats carried, not smoothed:** the 20 ms row's CI already includes zero
(n_test = 605); the 100 ms row rests on 121 test origins; the 500 ms row has 24
origins, ZERO coarse switches, and its p = 0.0495 with positive sign is a boundary
artifact — it is VOID-grade and the contraction claim must not lean on it. The
permutation p-values saturate at 1/101 (100 permutations). Low state occupancy 3.8 %.

## 1. THE TREE

**R0 — REPRODUCE.** Fetch the public trace; rerun `fiber_pilot.py` unmodified; all
seven `force_gain_bits` must match to 1e-9.
→ *pass:* R1–R4 run. → *fail:* **STOP.** The pilot is environment-bound; nothing
downstream runs and the record says AS-REPORTED, UNREPRODUCED permanently.

**R1 — VIEW ROBUSTNESS.** Re-derive the coarse view three ways (unconstrained GMM
best-of-10; fixed threshold at the 9.3 pN valley; 5/95-quantile hysteresis). Gain
profile (sign and contraction shape) must survive all three.
→ *pass:* continue. → *fail on any:* **branch R1′ pre-committed:** the effect is
view-artifact-suspect; run the view-selection arm — gain vs threshold curve on the
TRAIN split only, pick the argmax, score once on test. If the effect exists only at
the authors' view, report VIEW-FRAGILE and do not proceed to the erasure freeze.

**R2 — SAMPLING ROBUSTNESS.** Downsample ×2, ×4, ×8. A dynamical witness contracts in
TIME (gain vs horizon-in-ms invariant); measurement noise contracts in SAMPLES.
→ *time-invariant:* continue. → *sample-locked:* **branch R2′:** pre-whiten within
state (AR(1) residuals) and rerun once; if the gain vanishes, report
NOISE-ARTIFACT — killed, kept, marked.

**R3 — THE SURROGATE GATE (the load-bearing one).** State-preserving surrogate:
resample within-state segments from a state-conditional AR(2) model fitted on train,
preserving the exact coarse state sequence and dwell times. 200 surrogates; the real
gain must exceed the surrogate 95th percentile at every horizon where the pilot's CI
excluded zero. House memory binds here: iid and Gaussian nulls false-fire on
timeseries at +42σ; the null MUST match the generative structure.
→ *pass:* continue. → *fail:* **KILLED** — the estimator detects binning/spectral
artifact, not within-fiber dynamics. Record dead; the erasure freeze does NOT run.

**R4 — FIBER RESOLUTION.** Force bins {4, 8, 16} × velocity bins {3, 5, 9}. Gain must
saturate, not grow unboundedly (unbounded growth = estimator bias, the IPF lesson).
→ *saturates:* freeze `τ_c` = the first horizon whose CI includes zero, reported with
its bracketing horizons. → *grows:* **branch R4′:** shrinkage `ALPHA` sweep
{0.5, 2, 8} with 5-fold block CV on train only; if no plateau exists, report
RESOLUTION-UNSTABLE and freeze at 8×5 with that label attached.

**Family-wise correction, declared now:** the battery is 7 horizons × 4 cells; all
CIs at 99.5 % (Bonferroni-conservative for ~28 comparisons); permutation counts
raised to 1000 so p can resolve below the family threshold.

## 2. What passing buys, and the erasure freeze it licenses

Passing R0–R4 buys ONE claim: *the estimator recovers a physically meaningful witness
timescale on wild data* — expected physics (trap inertia, correlated noise), zero new
physics. It then licenses freezing THIS analysis, unchanged, for the 8.4 GB
underdamped-erasure dataset, where the decisive pre-stakeable question is: **does the
contraction statistic τ_c predict measured work, temperature, and survival** — the
H1′/rent bridge on data with real thermodynamic ground truth. That prereg is written
AFTER this battery reports and BEFORE any erasure byte is read, and it carries its own
tree.

## 3. No rescue beyond the tree

The tree above is the complete set of permitted responses to every outcome. Anything
else that seems worth doing after seeing data is a NEW prereg.
