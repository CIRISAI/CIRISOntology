# Results — LLM whole-only synergy EFFECT-SIZE calibration

Run 2026-07-23. Prereg: `llm-effectsize-prereg.md` (frozen before any statistic).
Rebuild (prior pipeline was cleaned): `llm_synergy.py` + `llm_run.py`, self-
consistent — the trained-model whole-only fraction is measured with the SAME
estimator the calibration uses. torch/transformers in whisper-venv, CPU, offline
cached models; corpus wikitext-2-raw. GPT-2 (primary), OPT-125m (cross-arch),
residual layer 6, N=4000 token positions, d=768, M=3000 triplets, b=2.

## VERDICT: the sign-only limit CAN become a sized statement — with one honest correction

The trained-model whole-only (order-3) synergy corresponds to a planted-
equivalent order-3 fraction of **~3%** (GPT-2 3.0%, OPT 2.9% — cross-architecture
consistent). But the raw detection is inflated by an untrained-control artifact;
the training-ATTRIBUTABLE (learned) whole-only fraction is **~2%**.

## The sign, reproduced (sanity)

Trained GPT-2 O-information Omega = **-0.00032 nats** (negative = synergy),
z = **-66.5** vs the independent-shuffle null. OPT-125m: Omega = -0.00031 nats,
z = -59.4. Sign firm, both architectures. (Prior pipeline reported -0.0086 nats;
absolute scale differs with layer/binning/N, but sign and cross-arch agreement
reproduce.)

## The calibration curve (variant A — the plant the estimator provably recovers)

Sign-parity `g3' = (1-f)g3 + f*sign(g1 g2)|noise|` into a pairwise-preserving
base (real pairwise, true order-3 = 0), identical estimator:

| f | z_dI3 | Omega (nats) | phi=DeltaI3/TC |
|---|---|---|---|
| 0.00 | +0.8 | -0.00013 | 0.031 |
| 0.02 | +6.1 (FIRES) | -0.00018 | 0.062 |
| 0.05 | +46 | -0.00062 | 0.252 |
| 0.10 | +254 | -0.00260 | 0.608 |
| 0.20 | +1073 | -0.01225 | 0.869 |
| 1.00 | +55233 | -0.62832 | 0.999 |

Monotonic; fires z>5 by f=0.02 (whole-only fraction 6%). This is the fMRI-
validated recoverable plant (there f=0.10 -> z=5.95).

## The sized statement (mapping observed -> planted-equivalent fraction f*)

Interpolating the observed values onto variant A:

| | Omega (nats) | phi_med | f* via Omega | f* via phi |
|---|---|---|---|---|
| GPT-2 trained | -0.00032 | 0.059 | **0.030** | 0.018 |
| GPT-2 untrained | -0.00015 | 0.018 | 0.010 | ~0 |
| **learned (trained - untrained)** | -0.00017 | | **~0.020** | **~0.018** |
| OPT-125m trained | -0.00031 | 0.046 | **0.029** | — |

Both mapping routes agree: trained ~3% raw, **learned ~2%**. The DeltaI3 excess
above the matched floor is firmly nonzero: 0.00031 bits, bootstrap 95% CI
[0.00029, 0.00034]. So: **the trained model's whole-only synergy is as large as a
~2-3% order-3 planting — a small but resolvably nonzero fraction, consistent
across two architectures.**

## The untrained-control artifact, pinned (the honest correction)

Untrained GPT-2 (random weights) ALSO fires: Omega = -0.00015 nats (z=-9.1),
whole-only z_dI3 = +30. So a raw synergy detection is contaminated — the
architecture's nonlinearities and TIED activations (tie fraction GPT-2 2e-3,
OPT 1.3e-2) manufacture ~1% planted-equivalent order-3 on their own. This is
exactly the "untrained control fires on tied activations" issue the stance flags
for GPT-NeoX — now quantified and general (it affects GPT-2 and OPT too, more so
for ReLU-family OPT). The clean signal is the trained-MINUS-untrained excess
(~2%), NOT the raw vs-shuffle number. The z-statistic itself is not a clean
discriminator (it fires for untrained); the effect SIZE, and the trained/untrained
contrast, are.

## Mixed-control puzzle RESOLVED (z=-2768 vs z=+0.58)

Three planting variants through the identical estimator:
- **A (survives-binning sign-parity):** fires monotonically, z>5 from f=0.02, up
  to z~55000 at f=1. -> the z=-2768 control was an A-type plant at moderate f
  (our A f=0.20 gives Omega-z = -1030; f~0.25-0.3 reaches ~-2768).
- **B (sub-bin-width wash-out):** order-3 injected below the median-split
  resolution. **Max |z_dI3| across ALL f = 7.7** (only at f=1.0); ~0 everywhere
  else. -> the z=+0.58 control was a B-type plant: its order-3 sat below the
  rank-binning resolution, so the estimator provably cannot see it.
- **C (pairwise-contaminating):** fires but ATTENUATED (z=55 at f=0.10 vs A's
  254) — half the injected signal is order-2, which the IPF pairwise-maxent
  subtraction correctly removes from the whole-only remainder.

So the two prior "positive controls" were DIFFERENT planting methods — one the
estimator recovers, one below its resolution — not an estimator failure. The fix
(as in fMRI): use the recoverable plant and publish the calibration curve so the
detection floor (here f>=0.02) is explicit. The estimator is sound: it recovers
genuine order-3 (A), ignores order-3 hidden below its binning (B), and does not
mistake order-2 for order-3 (C).

## Discipline

- Tie fraction disclosed (2e-3 GPT-2, 1.3e-2 OPT) — the artifact driver, and the
  reason the trained/untrained contrast is load-bearing.
- Bias floor = matched surrogate; DeltaI3 bias-subtracted; report dimensionless
  f*, phi, z (provenance lock — no raw nats as scale).
- Touched only the llm-embodiment effect-size leg. Stance.lean NOT modified.
- Honest edges: b=2 only (b=3 robustness recommended, N supports it); untrained
  control run for GPT-2 not OPT (OPT's raw 2.9% likely decomposes similarly given
  its higher tie fraction); one layer (6), one corpus; small models.

## DRAFT confidence-band update for `llm-embodiment` (for team-lead review, NOT applied)

Replace the effect-size clause of the confidence field with:

"...only the SIGN was firm; the effect size is now calibrated. A planted-signal
curve (order-3 sign-parity into a pairwise-preserving base, the plant the
estimator provably recovers; it fires by a 2% planting) maps the trained-model
whole-only synergy to a planted-equivalent order-3 fraction of ~3% in BOTH GPT-2
and OPT — cross-architecture-consistent in SIZE, not just sign. But ~1% of that
is a shared untrained-architecture / tied-activation artifact (pinned: it fires
the raw detector even at random init), so the training-ATTRIBUTABLE whole-only
fraction is ~2% (DeltaI3 excess CI excludes zero). The earlier mixed positive
controls are explained: they used different planting methods — one recoverable,
one below the binning resolution. So the sized claim is: small (~2%), real,
learned, cross-architecture whole-only structure — still short of measured (one
layer, small models, activations-not-behaviour), but no longer sign-only."

## VALIDATION (team-lead required, run before banking) — `validate.py`, `llm_validate.json`

The three checks REFINE the claim substantially. Learned = trained MINUS untrained
(the clean discriminator), done for BOTH architectures, at b=2 and b=3.

**Learned whole-only fraction f* (planted-equivalent), via O-information:**

| | b=2 f*(Om) | b=3 f*(Om) | b=2 dI3 excess (T-U) | b=3 dI3 excess (T-U) |
|---|---|---|---|---|
| GPT-2 learned | 0.020 | 0.040 | 0.00016 | 0.00071 |
| OPT-125m learned | 0.004 | 0.018 | 0.00002 | 0.00041 |

**1. b=3 robustness — NOT stable across binning, but NOT the fMRI bias either.**
GPT-2 learned is ~2% at b=2 and ~4% at b=3 (OPT ~0.4% -> ~1.8%). So the number
is binning-resolution-dependent. BUT the N-subsampling check rules out the
fMRI-style finite-sample bias: the b=3 GPT-2 learned excess GROWS with N (0.00037
at N=1000 -> 0.00057 at 2000 -> 0.00071 at 4000), **corr(1/N, excess) = -0.99** —
the OPPOSITE sign to fMRI's b=3 undersampling bias (+0.55). N=4000/27cells is
well-sampled. So finer binning resolves MORE genuine order-3, not bias; the
conservative binary estimate is ~2%, ternary ~4%. (Caveat: the excess is still
rising at N=4000, not fully saturated — the true value may be higher, or a
slow systematic remains; the anti-1/N sign firmly excludes simple undersampling.)

**2. Untrained-OPT control — this PARTIALLY BREAKS the cross-architecture SIZE claim.**
Untrained OPT fires almost as hard as trained (b=2 f*(Om): trained 0.029 vs
untrained 0.025; tie fraction 1.3e-2, ~6x GPT-2's). So OPT's raw 2.9% is
ALMOST ALL tied-activation artifact: the learned (T-U) part is f*=0.004 (0.4%),
dI3 excess 0.00002 ~ ZERO at b=2, rising only to ~1.8% at b=3. GPT-2's learned
signal is clearly larger than OPT's at BOTH binnings (0.00016 vs 0.00002 at b=2;
0.00071 vs 0.00041 at b=3). **Conclusion: the SIGN is cross-architecture, but the
learned SIZE is NOT — it is clear in GPT-2, marginal-to-artifact in OPT.** My
earlier "GPT-2 3.0% / OPT 2.9%" conflated RAW with learned; corrected here.

**3. Provenance answer (honest).** The SIGN metric — strictly-3-way O-information
(Rosas) on rank/copula-binned activations vs a matched surrogate null — is the
standard method the standing detection describes, so the sign result is on the
same method. But this is a RE-DERIVATION, not a bit-identical reproduction:
(a) the original run_synergy.py/referee_synergy.py were deleted, so no diff is
possible; (b) absolute nats differ (mine -0.00032 vs the standing -0.0086) from
layer/token-selection/N/binning; (c) my sizing ADDS two things the original
likely lacked (it still reported "mixed controls" and "untrained fires" as open):
the IPF pairwise-maxent whole-only remainder DeltaI3, and the trained-MINUS-
untrained contrast. So the ~2% is internally consistent and comparable IN METHOD
to the standing O-information detection, but is not a bit-for-bit reproduction.

## VERDICT after validation: SIZE for GPT-2 only, NOT cross-architecture

The sized statement survives FOR GPT-2 (~2% binary, ~4% ternary, learned, N-real
not bias) but the cross-architecture SIZE claim does NOT — OPT's learned signal
is artifact-dominated at binary resolution. Sign stays cross-architecture.

## REVISED DRAFT band update for `llm-embodiment` (for team-lead; NOT applied)

"...the effect size is now calibrated (rebuild — the original pipeline was
deleted; same-method O-information, sign reproduced, absolute scale not
comparable). A planted-signal curve (the order-3 plant the estimator provably
recovers; a wash-out plant below the binning resolution does NOT fire — which
explains the earlier mixed positive controls) sizes the TRAINED-MINUS-UNTRAINED
whole-only synergy. In GPT-2 this learned fraction is ~2% (binary) to ~4%
(ternary), and a subsampling check shows it grows with data, not the 1/N of a
finite-sample artifact — a real, small, learned effect. But the SIZE does NOT
replicate across architecture: OPT-125m's raw synergy is almost entirely a
tied-activation artifact (its untrained control fires nearly as hard), leaving a
learned fraction near zero at binary resolution. So: the SIGN is cross-family;
the learned SIZE is demonstrated in GPT-2 (~2-4%) but is architecture-dependent
and artifact-prone elsewhere. Still short of measured, and now with the size leg
sized for one architecture, not banked cross-family."

## Files
- `llm-effectsize-prereg.md`, `llm_synergy.py`, `llm_run.py`, `validate.py`,
  `llm_result_b2.json`, `llm_opt_b2.json`, `llm_validate.json`,
  `act_*.npy` (cached activations), `wikitext_corpus.json`.
