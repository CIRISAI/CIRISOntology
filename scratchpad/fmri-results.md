# Results — human-fMRI whole-only remainder (adequacy's live kill)

Run 2026-07-23. Pre-registration: `fmri-prereg.md`, frozen before any statistic
on the real data. Script: `fmri_whole_only.py`. Nulls: `secondary_null.py`.

## VERDICT: CLEAN NULL — adequacy's kill does NOT fire; it extends to a 4th substrate

The order>=3 whole-only remainder our instrument reads on real human
resting-state fMRI, at whole-population scale, sits at the pairwise-preserving
floor. No detection. The one substrate the `adequacy` claim named as where its
kill still lives now reads clean, like the other three (simulated cosmic field,
mouse V1, BOSS galaxies).

## The number vs the floor

**Primary: b=2 (median split), typically-developing CONTROLS, n=139**
(ABIDE-PCP CC200, cpac/filt_noglobal, cached locally; T = 78-296 TRs/subject,
7 sites).

- Per-subject whole-only remainder DeltaI3 vs its own multivariate
  phase-randomised (pairwise-preserving, autocorrelation-matched) surrogate
  floor: **median z = +0.18, mean z = +0.25**, sd 1.03, range [-1.90, +3.31].
- **No single subject reaches detection** (max +3.31; the bar is +5).
- **M-independent effect size:** the mean remainder ABOVE the matched floor is
  **1.1% of the floor** (delta = 6.0e-5 vs floor 5.6e-3 bits), positive in
  78/139 subjects (56%). Across-subject **t = +2.37**.
- **Whole-population group z:** the pre-registered Z_group = mean_z*sqrt(n) =
  **+2.89** — below the 3-sigma clean-null ceiling, far below the 5-sigma
  detection bar. (See the M-sensitivity note below: the M-independent t=+2.37
  is the more honest group figure; both are < 3.)
- Whole-only FRACTION phi = DeltaI3/TC_data: median **2.5%** (raw, dominated by
  the shared finite-sample floor; the genuine excess above the matched floor is
  the 1.1% above).

The per-instance floor reading (z ~ 0.18-0.25) is the SAME floor the in-scope
substrates sit at: mouse V1 read 0.14 and 0.28 sigma; BOSS 1-2 sigma. Human
fMRI joins them.

## Positive control — power PROVED

Identical pipeline; a triadic (sign-parity) order-3 signal planted into a
pairwise-preserving surrogate field (true order-3 = 0) at fraction f, over 500
disjoint triplets:

| f | planted z | whole-only fraction phi |
|---|---|---|
| 0 (unplanted) | **+0.36** (clean, no false positive) | — |
| 0.05 | +1.95 | 0.050 |
| **0.10** | **+5.95 (FIRES)** | **0.065** |
| 0.20 | +24.6 | 0.148 |
| 0.30 | +58.8 | 0.299 |
| 1.00 | +728 | 0.936 |

The instrument fires at z>=5 once a genuine order-3 signal reaches a whole-only
fraction of **~6.5%**, and climbs monotonically thereafter; the unplanted
control stays at the floor (+0.36). The human data's genuine excess is ~1% of
the floor — **far below** the level a real signal at Luppi-reported magnitude
would produce. If the human brain carried whole-only structure at the fraction
outside work claims, this instrument would fire. It does not.

## Tie fraction

**Exact-tie fraction = 0.0** (continuous BOLD, normal-scored; median over first
10 subjects 0.00e+00). Rank-based binning manufactures signal in proportion to
ties (the mechanism that killed the predecessor's "20% hidden" cosmic reading);
here there are none to exploit.

## The decisive methodological finding — an insufficient null FALSE-FIRES at +42 sigma

The pre-registered secondary null (pairwise-maxent IPF **resample**, iid draws
that preserve the FULL pairwise distribution but DESTROY autocorrelation) was
run on 30 subjects against the same data:

- Autocorrelation-matched MVPR null: **mean z = +0.06 (Z_group +0.32)** — clean.
- iid pairwise-maxent null: **mean z = +7.6 (Z_group +42)** — a massive FALSE
  detection.

The iid floor (~0.0025-0.004 bits) sits far below both the data and the MVPR
floor (~data), because destroying autocorrelation raises the effective sample
size and understates the plug-in bias. In most subjects the data DeltaI3 is
indistinguishable from (or below) its autocorrelation-matched floor, but sits
well above the autocorrelation-blind floor. **A null that fails to preserve the
data's autocorrelation manufactures a +42-sigma detection on data that is
actually at the floor** — a textbook instance of epistemology L2 (match the null
to the generative structure) and a concrete mechanism by which weaker-null
outside work can report nonzero human synergy. This is why the prereg demanded
an autocorrelation-preserving null and why "Gaussian-only / iid nulls are not
sufficient."

## The M-sensitivity note (kept, because it bears on the verdict)

The per-subject z divides the data-minus-floor offset by the surrogate SD of a
mean over M triplets, which shrinks as sqrt(M). So the z-based Z_group is
tunable by the (arbitrary) triplet count: at M=1500 it is +2.89, at M=800 the
subset reads +0.06-0.3. The M-INDEPENDENT quantity — the effect size (remainder
above floor, 1.1%) and its across-subject t (+2.37) — is what the verdict rests
on, and it is a clean null. Reported plainly rather than by picking the M that
flatters a headline.

## Honest scope and edges

- ONE measure (order-3 connected information, binary median-split, MVPR null),
  ONE parcellation (CC200), resting-state, ABIDE controls (not HCP; T is short,
  78-296 TRs — the matched surrogate is the control for short T).
- The remainder is a lower-bound instrument (order-3; parity-complete but a
  floor reading is not proof of absence at higher orders) — consistent with the
  stance's own "floor is not an absence."
- b=3 robustness — and the undersampling trap, caught: at b=3 (27 cells) the
  raw per-subject z is elevated (running mean ~1.6). But this is the kill's own
  "too little data" trap, proven: ABIDE's short runs give only 3-11 samples/cell
  at b=3, and the excess-above-floor correlates **+0.55 with 1/T (p<0.001)** —
  it SHRINKS as recordings lengthen (T<100: 3.0e-3 bits; T>220: 4.1e-4), the
  textbook 1/T signature of finite-sample bias, not a T-constant signal. The b=3
  floor itself balloons at short T (0.094 -> 0.024 bits). The pipeline is
  calibrated (a pure order-3-free Gaussian field reads z~0 at b=3, mean -0.16),
  so the elevation is a data-vs-surrogate bias mismatch in the sparse regime, not
  order-3. By contrast the b=2 excess is FLAT in T (r=-0.13, p=0.42) — the
  well-sampled regime. No b=3 subject reaches detection either. b=3 at this T
  therefore does not clear the pre-registered bias guard and is reported as an
  undersampling artifact; the well-sampled b=2 clean null stands, and b=3
  extrapolates to it as T grows.
- The small T-independent b=2 residual (1.1% of floor, t=2.37, below the 3-sigma
  clean-null ceiling) is flat in T, so it is NOT finite-sample bias; its origin
  (a genuine negligible order-3, or a constant Gaussian-surrogate vs non-Gaussian
  mismatch) is unresolved and immaterial — it is far below detection.
- Sensitivity to including the autism group (all 250 subjects): not run as
  primary; the kill is "any natural system," and controls already read clean.

## Files
- `fmri-prereg.md` (frozen), `fmri_whole_only.py`, `secondary_null.py`
- `fmri_result_b2_controls.json`, `fmri_poscontrol.json`, `secondary_null_b2.json`
- DID NOT touch `Stance.lean`.
