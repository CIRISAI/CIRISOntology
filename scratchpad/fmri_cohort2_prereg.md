# Pre-registration — adequacy, second independent fMRI cohort

**Frozen before any whole-only statistic is computed on the new cohort.**
Written 2026-07-23. Author: research session (Opus). Target claim: `adequacy`
(measured) — its live kill lives in human fMRI, where cohort 1 (ABIDE-CC200,
n≈139) gave a mild +2.4–2.9σ group lean that stayed inside the null band. This
run asks whether that lean **replicates on an independent cohort** (settle toward
floor) or **climbs past detection** (fires the kill).

## Instrument — IDENTICAL to cohort 1 (scratchpad/fmri_whole_only.py)

Copied verbatim, no changes to estimator or null:

- **Statistic**: per-triplet ΔI₃ = H(P*) − H(P_data), P* = pairwise-maximum-
  entropy model fit by IPF (40 iters). This is the order-3 connected information
  (KL from data to the best pairwise model). Averaged over M=1500 random region
  triplets per subject.
- **Preprocessing of each region series**: normal-score (rank → ndtri, copula
  transform), then equal-frequency binning at b=2 (median split, rank-based →
  tie-robust). Primary b=2; b=3 as a pre-registered secondary if b=2 is
  interesting.
- **Null**: common-phase multivariate phase-randomised surrogate (Prichard–
  Theiler) — preserves every region's power spectrum AND the full cross-spectrum
  (hence ALL pairwise/co-fluctuation structure, including any shared-stimulus
  co-activation), destroys order≥3. N_SURR=100 per subject → per-subject
  z = (ΔI₃_data − μ_surr)/σ_surr.
- **Group statistic**: Z_group = mean_i(z_i) · sqrt(n).
- **Positive control**: plant sign-parity order-3 coupling s = sign(g1·g2)·|N(0,1)|
  into pairwise-preserving surrogate fields at SNR f ∈ {.05,.1,.2,.3,.5,.8,1};
  report smallest f firing z≥5 (the detection floor) and the unplanted (f=0)
  control (must stay within ±3). Validates power AND the null on THIS cohort.
- Seeds fixed (SEED=0 main, 123 control).

## Cohort — the only thing that changes

- **Dataset**: nilearn `fetch_development_fmri` (Richardson et al. 2018) — a single
  independent site (MIT), children + adults, naturalistic movie-watching.
  Genuinely disjoint from ABIDE in site, scanner, population, and task.
- **Atlas**: Schaefer-2018 200-region, 17-network, 2 mm (deterministic labels).
  A DIFFERENT 200-region parcellation than cohort 1's CC200 — deliberately, so a
  replication is robust to atlas choice, not tied to one parcellation. The
  estimator is atlas-agnostic (random triplets of regions).
- **Extraction**: NiftiLabelsMasker, standardize=zscore_sample, detrend=True,
  low_pass=0.1, high_pass=0.01, t_r=2.0, provided confounds regressed (approximates
  cohort 1's filt band-pass + nuisance regression; NO global-signal regressor, to
  match filt_noglobal). Regions with ~zero variance dropped.
- **Inclusion**: every subject returned by the fetcher passing T≥60 timepoints and
  R≥30 surviving regions. n is whatever that yields (recorded, not chosen).

## Naturalistic-stimulus caveat (pre-registered, not post-hoc)

The movie is a shared stimulus, so all regions partly track it — but that is
**pairwise** co-fluctuation, and the common-phase null PRESERVES the full
cross-spectrum, so stimulus-driven pairwise structure is subtracted exactly. Only
genuinely triadic (order-3, not reducible to any pairwise) stimulus- or
brain-driven structure can fire. Interpretation is stated up front:
- If it FIRES: a real order-3 detection on a natural system — the kill fires — with
  the honest note that a shared stimulus is one plausible generator of genuine
  triadic structure (still a legitimate kill: a movie-watching brain is a natural
  system, and the null already removed all pairwise stimulus locking).
- If it reads FLOOR: a strong independent null — even a shared naturalistic
  stimulus did not manufacture order-3 beyond pairwise.

## Decision — meaning of every possible outcome (fixed now)

Let Z = Z_group, and require the positive control to be VALID first
(smallest firing f ≤ ~0.3 AND unplanted f=0 within ±3); if the control is invalid
the run is discarded as a pipeline failure — NOT reported as a null (this guards
the known +42σ false-fire failure mode from a mismatched null).

Given a valid control:
- **Z ≥ +5**, or any single subject convincingly past +5 with Z>3 group support →
  **DETECTION. adequacy's kill FIRES on an independent cohort.** Page-changing:
  adequacy moves toward wounded/dead. Report the fired kill as plainly as a
  survival (epistemology rule #7). Then confirm with b=3 and a resting-state
  cohort before any stance edit.
- **|Z| ≤ 3** → **CLEAN NULL replicated.** The cohort-1 mild lean does NOT
  reproduce; adequacy settles further toward the floor and hardens. This is the
  most likely outcome if the cohort-1 lean was a cohort/pipeline quirk.
- **3 < Z < 5** → **INCONCLUSIVE — the mild lean reproduces at similar magnitude.**
  Neither settles nor fires. adequacy's "least-clean, human-fMRI" status persists,
  now on two independent cohorts — mildly notable, worth recording, not
  page-changing on its own.

## Provenance lock & disclosures

- Report ONLY dimensionless quantities: whole-only fraction φ = ΔI₃/TC (median) and
  z/σ. No units, no size laundering (pattern-not-size rule).
- Disclose the exact-tie fraction (rule #4) on the new cohort.
- Nothing here is pushed to the stance. Findings go back for team-lead review
  (research-first-then-stance). A single independent cohort, whatever it shows,
  is evidence toward — not a settlement of — the kill.

## Files
- `fmri_whole_only_cohort2.py` — estimator/null/control imported verbatim from
  cohort 1; only the loader (development_fmri + Schaefer-200 extraction) is new.
- Results → `fmri_cohort2_result_b2.json`, `fmri_cohort2_poscontrol.json`.
