# Fiber-closure robustness battery — results. **ALL FOUR CELLS PASS. τ_c = 20 ms.**

Tree frozen in `FIBER_ROBUSTNESS_PREREG.md`; quantified bands frozen in `battery.py`'s
header before the run; instrument gauged on planted truth first (`BATTERY_VALIDATION.md`,
measured floor ~2e-4 bits — every reading below is 75–200× above it). R0 reproduced the
pilot bit-exactly beforehand. One instrument crash mid-battery (numpy-2 NEP-50:
`int8 × 144` overflow at R4's 16×9 cell) was fixed and the full battery rerun;
**R1–R3 reproduced the crashed run's numbers line-for-line identically** under the
fixed seeds, which is the rerun's own integrity check.

## R1 — view robustness: PASS on all four views

| view | low-state fraction | pooled 0.1–5 ms gain | CI>0 | contracts |
|---|---|---|---|---|
| tutorial (authors') | 0.038 | +0.0232 | yes | yes |
| free GMM (best-of-10) | **0.195** | +0.0306 | yes | yes |
| fixed threshold 9.3 pN | 0.100 | +0.0160 | yes | yes |
| hysteresis (q05/q95) | 0.070 | +0.0177 | yes | yes |

The unconstrained GMM carves a 5× larger low state and the effect survives anyway.
**Not an artifact of the authors' view.**

## R2 — sampling robustness: PASS

Gains at matched millisecond horizons agree across ×2/×4/×8 downsampling (99.5% CIs
overlap at 0.5, 1 and 5 ms). **The witness contracts in TIME, not in samples —
dynamical, not measurement noise.**

## R3 — the surrogate gate: PASS, decisively

| horizon | real | surrogate 95th |
|---|---|---|
| 0.10 ms | +0.02518 | +0.00008 |
| 0.51 ms | +0.02697 | +0.00010 |
| 1.00 ms | +0.02552 | +0.00007 |
| 4.99 ms | +0.01510 | +0.00023 |

Real gain 100–300× above 200 state-conditional AR(2) surrogates preserving the exact
state sequence and dwell times. **Matched autocorrelated noise cannot produce the
effect; the within-fiber position genuinely informs the coarse future.**

## R4 — resolution: PASS (saturates)

Grid from 4×3 to 16×9 runs 0.0282 → 0.0425; max/8×5 = 0.0425/0.0373 = **1.14 ≤ 1.5**.
No unbounded growth; the estimator is reading structure, not bin count.

## τ_c — the frozen deliverable

**τ_c = 20.0 ms** (first horizon whose 99.5% CI touches zero), bracketed by 5 ms
(significant, +0.0151) and 20 ms (+0.0060, CI includes 0). All readings 75–200× above
the instrument's measured floor.

## What this buys — exactly one claim, and the license

*The estimator recovers a physically meaningful witness timescale on wild data.* The
two-state view of a real DNA-hairpin trace is not dynamically closed below ~20 ms;
within-fiber position and velocity carry real predictive information that contracts
away on a physical timescale. Expected physics (trap inertia, correlated noise); zero
new physics claimed.

Per the prereg §2, passing licenses **freezing this analysis unchanged for the 8.4 GB
underdamped-erasure dataset** — τ_c against measured work, temperature and survival:
the H1′/rent bridge on data with thermodynamic ground truth. That prereg is written
before any erasure byte is read, and carries its own tree.
