# Pre-registration — LLM whole-only synergy EFFECT-SIZE calibration

Frozen 2026-07-23, BEFORE any calibration statistic was computed. Goal: turn the
`llm-embodiment` synergy result from SIGN-ONLY into a SIZED statement — map the
trained-model whole-only synergy to an inferred order-3 FRACTION with an error
bar, and resolve the MIXED positive-control puzzle (one planted triad fired at
z=-2768, another at z=+0.58).

Note on provenance: the original pipeline (run_synergy.py / referee_synergy.py)
and its results files were cleaned from scratchpad and are not recoverable. This
is therefore a self-consistent REBUILD: the trained-model whole-only fraction is
re-measured with the SAME estimator used for the calibration, so the mapping is
internally valid even though the absolute D need not equal the prior -0.0086 nats.

## Object under test — two quantities, one estimator

On rank/copula-transformed, binned LLM activations, per random triplet (i,j,k):
1. **O-information Omega** (nats; Rosas et al. 2019), the SIGN: Omega<0 =
   synergy-dominated (parity/GHZ-type), Omega>0 = redundancy. Reproduces the
   prior sign detection (trained model expected Omega<0).
2. **Whole-only remainder DeltaI3** = TC - TC_pairwise-maxent (IPF), the nonneg
   MAGNITUDE (order>=3 connected information), and the dimensionless
   **whole-only fraction phi = DeltaI3 / TC**. This is the fraction the
   calibration maps to. Same estimator validated in the fMRI run
   (parity -> phi=1.0, pairwise-only -> 0).

Reusing `fmri_whole_only.py` primitives (normal_score, eqfreq_codes,
joint_counts, deltaI3_batch, mvpr_surrogate); adding a batched O-information.

## Data (frozen)

- **Models (cached, offline):** `gpt2` (124M) PRIMARY; `facebook/opt-125m`
  cross-architecture confirm; `EleutherAI/pythia-160m` (GPT-NeoX arch) if time.
  Trained vs an UNTRAINED control (same config, randomly-initialised weights).
- **Corpus:** `wikitext-2-raw-v1` (cached), real text (not repeated strings).
- **Representation:** residual-stream `hidden_states[L]`, L=6 (mid), d=768.
  N ~ 4000 token positions = samples (large N; undersampling is NOT the fMRI
  risk here — b can be finer).
- Per-dim rank/copula transform (marginals exactly Gaussian; pairwise = what
  -ln det C reads). **Binning b=2 PRIMARY** (8 cells, ~500 samples/cell),
  **b=3 robustness** (27 cells, ~150/cell — both well-sampled).
- **M = 3000 random triplets** of dimensions, fixed seed.

## Null (frozen)

- **Whole-only DeltaI3 z:** pairwise-preserving surrogate. Token-position
  activations form an autocorrelated sequence, so — carrying the fMRI lesson —
  the PRIMARY null is multivariate phase-randomisation (MVPR, common phase,
  preserves every power spectrum + full cross-spectrum, kills order>=3). A
  pairwise-maxent IPF resample is the confirmatory null; if they disagree the
  autocorrelation term is reported (as in fMRI).
- **O-information sign z:** independent-shuffle null (permute each dim across
  positions) for the total-structure detection.
- The matched surrogate is the estimator-bias floor (bias-subtracted, never raw).

## Planting method — the one the estimator PROVABLY recovers (frozen)

Base = a pairwise-preserving surrogate of the REAL trained activations (real
pairwise structure, TRUE order-3 = 0). Into P disjoint dimension-triplets inject
sign-parity (pure order-3, pairwise-null), mixed at fraction f:

    g3' = (1-f) * g3  +  f * sign(g1 * g2) * |g3_noise|

This is the fMRI-validated plant (f=0.10 -> z=5.95 there). f-GRID (frozen):
**{0, 0.02, 0.05, 0.10, 0.20, 0.30, 0.50, 1.0}**. Build z(f), Omega(f), phi(f).

## Mixed-control resolution (frozen protocol)

Run THREE planting variants through the identical estimator to explain the
z=-2768 vs z=+0.58 disagreement:
- **A. survives-binning sign-parity** (above) — expect FIRES (recoverable).
- **B. wash-out plant**: order-3 injected in a form the rank-binning removes
  (e.g. a tiny-amplitude continuous perturbation below the bin width, or a
  structure re-ranked away) — expect MISS (z~0). Candidate explanation for +0.58.
- **C. pairwise-contaminating plant**: a plant that also shifts the pairwise
  marginals so the whole-only remainder is masked/absorbed — expect the SIGN to
  move but phi to stay low. 
The variant whose behaviour matches each observed control number is the
resolution: which planting strength/method the estimator recovers, and why one
control fired enormously while the other did not.

## Decision rule and mapping (frozen)

- Reproduce the SIGN: trained model Omega < 0 with shuffle-z clearly negative,
  and clearly more synergistic than the untrained control. (Sanity; expected.)
- **Effect size:** measure trained-model phi = DeltaI3/TC with a bootstrap CI
  over triplets/positions. Read the inferred planted-equivalent fraction f* off
  the calibration curve phi(f), with the CI propagated -> **"the trained-model
  synergy corresponds to ~f* whole-only structure (CI ...)."**
- **Sized statement earned** iff (a) the calibration is monotonic and the
  positive control fires cleanly at a stated f, (b) the trained-model phi sits
  resolvably above its matched floor, and (c) the mixed-control puzzle is
  explained. Otherwise report what blocks it (sign stays, size does not).

## Discipline guards (frozen)
- Tie fraction disclosed (rank-transform -> ~0 for continuous activations).
- Bias floor = matched surrogate (L5). Report dimensionless phi and z, never
  raw nats as a scale (provenance lock).
- Separable: this touches ONLY `llm-embodiment`'s effect-size leg. If it lands,
  draft the confidence-band update adding SIZE; do not change the sign claim.
- Prereg meaning of every answer (above) fixed before running.

## Files
- `llm_synergy.py` (rebuild), `llm-effectsize.md` (results, written after).
- DO NOT touch `Stance.lean` in this run (draft the band update in the results md).
