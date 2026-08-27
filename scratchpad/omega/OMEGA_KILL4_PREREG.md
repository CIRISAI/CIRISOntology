# Pre-registration — Ω-KILL-4: the golden freeze

**2026-08-27, frozen before any staked run; admissible only if the audit exits
0.** The tuple with EVERY face on fresh data at its LEARNED scope — the freeze
the four falsifications and three interim rounds bought. Fifteen staked arms,
five faces, three substrates. Binary exit: **CONFIDENCE ⇔ every posable arm
passes — that verdict IS the golden Ω: the object with all five faces
live-tested at honestly stated scope. FALSIFICATION ⇔ any posable arm misses,
naming its face.** No rescue.

defects: D-IDENT (id-joins and id-keyed coefficients everywhere), D-MATERIALIZE
(threshold onsets), D-CHAN-DRIFT (three pinned circuit sets: backbone 71aba242…,
g-extension 7f42bebc…; in-job one-way premise), D-EPOCH (every floor and
constant in-job), D-GATE (realized channels; the analysis path is the
Ω-3-validated one with ideal-unitary planted evidence on record), D-DET (engine
arms interventional), D-BOUND-DOB (the mixing arms use the L-step out-of-sample
form with the base-lag RULE — smallest train-diagnostic lag with alpha < 0.9 —
per protocol; lag-1 refused on record), D-UNITS (all bands dimensionless or
unit-named), D-FRAME-ZERO (construction premises read pre-step meta lines).

gauge: scratchpad/omega/gauge_omega2.log
gauge: scratchpad/omega/gauge_idjoin.log
gauge: scratchpad/omega/gauge_battery.log
gauge: scratchpad/omega/gauge_n1.log
gauge: scratchpad/omega/gauge_n2.log
gauge: scratchpad/omega/gauge_nabla.log
gauge: scratchpad/omega/omega3_validate.log

Family-wise: Bonferroni over 15 staked arms; QPU floors at the 99.5th
percentile of in-job permutation nulls; N-arm sigmas chain-block bootstrapped;
QPU bands carry 3σ shot error.

## Frozen execution (all instruments and adjudicators as committed here)

- **Engine backbone**: `idjoin_probe 0.25 <dir>` (fresh probe geometry),
  adjudicated by `analyze_idjoin.py`.
- **Tier face**: `tier_closure_probe <dir> 2400 75` (never-run warm-up,
  interior of the measured organization window), adjudicated by
  `tier_battery.py` — T-levels at f = 300 ONLY (its adjudicated scope,
  4-for-4), T-protect staked WITHIN the organization window (its adjudicated
  scope: died only at deep settling).
- **∇ face**: `nabla_probe <dir> 90 16 30 75` (fresh warm-up and throw
  cadence), adjudicated by `nabla_adjudicate.py`; V2/V3 remain refused.
- **μ face**: `oos_mixing.py` with PROTO ∈ {Enhanced, OptSingle} — the two
  never-touched streams; UNBLIND=1 only after this freeze commits.
- **g face**: `s1_omega4.py submit` — one job: pinned backbone + pinned dose
  EXTENSION p ∈ {3, 6, 12, 24} (Ω-3 measured {2, 4, 8, 16}); staked qubit 95.

## The arms

| arm | stake (numeric) | witness: | posability |
|---|---|---|---|
| F1 idle | both defects ≤ 3× floor | witness: `independent_views_closed` | varied 0.1×–1.67× across five epochs |
| F2 one-way | fwd ≥ 50× floor ∧ fwd ≥ 5× reverse; premise: reverse ≤ 10× floor else VOID | witness: none | reverse has read 0.2×–137× — no posability prediction is made for this arm |
| F3 hop | both ≥ 10× floor ∧ max/min ≤ 3 | witness: none | 31–75× across four jobs |
| F4 common-driver | both ≤ 3× floor ∧ created ≥ 50× its floor | witness: `common_driver_probe_null` | created 0.606–0.624 four times |
| T1 sham | exactly 0 all frames, join full | witness: none | ULP fires (gauge) |
| T2 pre-probe | exactly 0 before frame 240 | witness: none | dust fires (gauge) |
| T3 light-cone | left onset < right, gap ≥ 10, 1%-of-max onsets | witness: none | gaps 723/843 on two geometries; planted gap 6 fires |
| T4 K | rise-epoch median growth ≤ 1.05; rise < 20 ⇒ VOID | witness: none (`Aggregation`; six geometries unbreached) | planted 1.078 fires |
| T5 tier battery at 75 | T-construction premise ∧ T-budget ≤ 1.05 ∧ T-levels(f=300) ≥ 0.8 ∧ T-organize resid > rand p75 ∧ T-protect resid < rand p25 — five conjuncts, prongs separately gauged | witness: `sum_perturb_le` (levels), `coherence_of_nonneg` (protect), `interventional_iff_closed` (construction) | every conjunct fired or voided by name in gauge_battery.log; the organization window's interior point 120 read 7.69 vs p75 3.61 |
| M1 mixing, Enhanced | held-out defect(k·L) ≤ α̂_train(L)^k + 3σ, k ∈ {1,2,4}; L = 16 by the frozen rule (α̂ = 0.5629); frozen bounds 0.5724 / 0.3251 / 0.108653 — all non-vacuous (`n1_Enhanced_train.log`); the k=1 rung fires only through kernel drift, stated | witness: `defect_le_alpha_pow` | train-side bootstrap spread + pair guard, same log; gauge PASS/FIRE at base 16 |
| M2 mixing, OptSingle | same form; L = 16 by the rule (α̂ = 0.6458); frozen bounds 0.6530 / 0.4252 / 0.1811 — all non-vacuous (`n1_OptSingle_train.log`) | witness: `defect_le_alpha_pow` | same |
| G1 rent bracket, extended doses | R(p, C=2) within [min−3σ, max+3σ] of the two in-job point predictions for ALL p ∈ {3, 6, 12, 24}; premise: monotone ladder | witness: `rent_closed_form` + `Ginf_at_Wstar`; GCOST §4.2 bracket | Ω-3's doses sat inside a tight bracket; these four points have never been measured; planted fast-channel fires (gauge_n2.log) |
| G2 cycle-memory, extended | |R(p,4) − R(p,2)| ≤ 3σ√2 for all four new doses | witness: none | planted heating fires (gauge_n2.log) |
| V1 connection law | Pearson ≥ 0.99 ∧ slope ∈ [0.90, 1.10] on momx AND ke (conjunctive), n ≥ 100; premise: uniform-weight null ≤ 1e-12 | witness: `curvature_iff_held` | NABLA-1 passed at 0.9999/1.012 on a different config; coefficient plants fire both ways (gauge_nabla.log) |

## Exits

- **CONFIDENCE — the golden Ω**: every posable arm passes. The tuple stands
  with Fib, μ, T, ∇, g each live-tested on fresh data at stated scope. This
  is the claim the campaign season was for.
- **FALSIFICATION**: any posable arm misses → the tuple is falsified at the
  named face, the miss goes through the misfit protocol, and the loop
  continues.
- **VOID paths**: F2 premise; T4 rise; T5 construction/pairs; M-arms
  pair-guard; G premise (non-monotone ladder); V1 premise and n-floor;
  device failure voids its substrate; the test VOIDs only if an entire face
  voids on every arm.
