# Pre-registration — human-fMRI whole-only remainder (adequacy's live kill)

Frozen 2026-07-23, BEFORE any statistic on the real data was computed or
inspected. This run targets the ONE substrate the CIRISOntology `adequacy`
claim names as where its kill still lives: human fMRI at whole-population
scale, where outside work (Luppi et al.) reports NONZERO whole-only /
O-information synergy under weaker nulls than ours.

Two honest, symmetric outcomes, decided in advance:
- **Detection** (>= 5 sigma above matched surrogate): adequacy's kill FIRES.
  Report loudly; draft the adequacy narrowing-or-death per its kill text.
- **Clean null** (within +- 3 sigma): adequacy extends to a FOURTH substrate.
- **Between 3 and 5 sigma**, or a positive control that fails: INCONCLUSIVE.

## The object under test — OUR instrument, not generic O-information

`S = -ln det C` reads only the second-order (pairwise-Gaussian) part of the
total dependence. The quantity it is BLIND to — the object every prior
adequacy run (mouse V1, BOSS) measured — is the **order>=3 connected-information
remainder**: `S_total` minus its pairwise-maxent part. This is the field
deployment of `Core/Third.lean`'s toy witness (`S_total parity = log 2` while
`S_pairwise parityCorr = 0`).

Operationalised at order 3 (triplets of regions), exactly as the mouse V1
("three-way order") and BOSS runs did. For a triplet with binned joint
distribution `P_data` and the maximum-entropy distribution `P*` matching all
three PAIRWISE marginals (fit by iterative proportional fitting, IPF):

    DeltaI3  =  TC_data - TC_pairwise-maxent
             =  H(P*) - H(P_data)
             =  D_KL( P_data || P* )   >= 0

DeltaI3 is exactly the total dependence that survives conditioning on all
pairwise structure — the order>=3 connected information, the discrete analog of
what `-ln det C` discards. NOT a bare O-information detection (a referee escapes
that on "different quantity"); this is `S_total` minus its pairwise part, the
CIRIS object.

## Data — assessed before freezing

ABIDE Preprocessed (ABIDE-PCP), CC200 functional parcellation (k=200 regions),
`cpac` / `filt_noglobal` pipeline (band-pass, NO global signal regression),
`quality_checked=True`. Already cached locally at
`~/nilearn_data/ABIDE_pcp/cpac/filt_noglobal/*_rois_cc200.1D`: **250 subjects**,
7 sites (UM_1 86, Pitt 50, Trinity 33, Olin 28, SDSU 27, OHSU 25, UM_2 1),
T ~ 120-300 TRs each.

- **Primary sample: typically-developing CONTROLS** (`DX_GROUP == 2` in
  `Phenotypic_V1_0b_preprocessed1.csv`) — the healthy coordinated substrate,
  matching the predecessor corridor run. n reported (expected ~139).
- **Sensitivity: ALL 250 subjects.** If controls read clean but the full set
  (incl. autism group) detects, that is reported — the kill is "any natural
  system," so the all-subjects direction is the more kill-seeking one and is
  run honestly.
- Per-region timeseries, T timepoints x 200 regions. Regions with zero variance
  dropped. Subjects with T < 60 dropped.

## Instrument pipeline (frozen)

1. **Copula transform.** Normal-score each region's timeseries (rank -> ndtri),
   per subject. This makes every marginal exactly Gaussian, so all detected
   structure is DEPENDENCE, and the pairwise part is exactly what `-ln det C`
   reads. (Removes marginal non-Gaussianity as a confound up front.)
2. **Binning.** Equal-frequency bins per region. **PRIMARY b = 2** (median
   split; 8 joint cells; matches the binary XOR/parity witness and Luppi-style
   binarisation; ~20-40 samples/cell at these T, low plug-in bias).
   **Robustness b = 3** (27 cells) reported alongside.
3. **Triplets.** Sample **M = 1500** random region-triplets per subject
   (fixed seed 0), shared across data and surrogates within a subject.
4. **DeltaI3 per triplet** via batched IPF (marginals matched to a tolerance,
   capped iterations), pooled statistic = mean over triplets.

## Null — pairwise-preserving, matched to fMRI generative structure (frozen)

fMRI is continuous, autocorrelated timeseries. A Gaussian-iid null is NOT
sufficient (it drops autocorrelation and mis-states the finite-sample bias).

- **PRIMARY null / bias floor: multivariate phase-randomised surrogate**
  (Prichard-Theiler): one rFFT of the (T x 200) normal-scored field, add the
  SAME random phase to ALL regions at each frequency, invert. This preserves
  every region's power spectrum (autocorrelation) AND the full cross-spectrum
  (every pairwise covariance at every lag) EXACTLY, while destroying order>=3
  phase coupling. It is a linear-Gaussian-process surrogate with TRUE
  DeltaI3 = 0. Apply the SAME IPF DeltaI3 estimator to each surrogate ->
  finite-sample bias floor with matched autocorrelation. n_surr = 100.
- **WHY this + IPF together:** IPF subtracts the FULL pairwise-maxent (not just
  the covariance) analytically, so non-Gaussian bivariate copula structure does
  NOT leak into the remainder (this is what "Gaussian-only nulls not sufficient"
  guards against). The phase surrogate supplies only the autocorrelation-matched
  bias floor for significance. Its own residual (its DeltaI3, which is pure
  bias) is subtracted.
- **Confirmatory secondary null:** a pairwise-maxent RESAMPLE — draw iid samples
  from the fitted `P*` (exactly zero order>=3, full pairwise preserved, but
  autocorrelation destroyed) on a subject subset; check the two nulls' bias
  floors agree. If they disagree materially, report as a null-model dependence.

## Test statistic and decision rule (frozen)

Per subject i, triplet-averaged remainder `d_i = mean_t DeltaI3_data(t)`; the
surrogate ensemble gives `d_i^(s)` for s = 1..100. Per-subject
**z_i = (d_i - mean_s d_i^(s)) / std_s d_i^(s)**. (Under the null z_i ~ N(0,1).)

Whole-population reading: **Z_group = mean_i(z_i) * sqrt(n)** (primary), with the
full z_i distribution, median z_i, and max z_i reported. Dimensionless
whole-only FRACTION `phi = DeltaI3 / TC_data` reported per subject (median).

- **Z_group >= +5  =>  DETECTION => adequacy kill FIRES.**
- **|Z_group| <= 3  =>  clean null => adequacy extends to a 4th substrate.**
- **3 < Z_group < 5 => INCONCLUSIVE.**
(A negative Z_group is a clean null; the estimator is one-sided in truth,
DeltaI3 >= 0, but bias-subtracted z can go negative under the null.)

## Positive control — power must be proved (frozen, as mouse/BOSS did)

Take a PAIRWISE-PRESERVING surrogate field (true order>=3 = 0). Into a set of
"planted" triplets, inject a triadic (XOR/GHZ-type sign-parity) coupling on the
third region mixed with the surrogate at fraction f, i.e.
`g3' = (1-f) g3 + f * sign(g1 * g2) * |g3-noise|`, spanning f in a realistic
fMRI range. Run the IDENTICAL pipeline. **Power confirmed iff the planted
triplets fire (z >= 5) at a realistic-SNR f while un-planted triplets stay
within +-3.** Report the smallest f that fires. If only an unrealistically large
f fires, a real-data null is DOWNGRADED to inconclusive/underpowered, stated
plainly. This is the crux honesty gate.

## Discipline guards (frozen)

- **Tie fraction disclosed.** Normal-scored continuous BOLD -> essentially no
  exact ties; report the exact-duplicate fraction and the fraction landing on
  equal-frequency bin edges. Rank-based binning manufactures false signal in
  proportion to ties (an earlier "20% hidden" cosmic-field reading died exactly
  that way) — so this is disclosed before any DeltaI3 is believed.
- **Bias control.** The matched surrogate IS the estimator-bias floor
  (discipline L5); DeltaI3 is bias-subtracted, never reported raw.
- **Separable kill.** This run touches ONLY the `adequacy` claim. A detection
  fires adequacy's kill and nothing beneath it; a null extends adequacy alone.
- **Provenance lock.** Report ONLY the dimensionless fraction phi and z/sigma.
  No bits-as-magnitude, no construction datum, per `pattern-not-size`.
- **Pre-register meaning of every answer** (above): detection, null, and
  inconclusive were all assigned their consequence before the data was seen.

## Files
- `fmri_whole_only.py` — the frozen test script.
- `fmri-results.md` — written after, reporting whichever outcome fires.
- DO NOT touch `Stance.lean` in this run.
