# Q2 — the P-STEP32 adjudication, run by the coordinator after both agents hit session limits

> ## CORRECTION (2026-07-27, by the sawtooth-forward agent, `022096e`) — I over-graded this
>
> **Two errors of mine, both in the coordinator's favour, both withdrawn.**
>
> 1. **"The campaign's third advance-prediction confirmation" is too strong.** The P-STEP32
> *rule* was genuinely pinned before the k = 32 datum existed — that part stands. But the
> location claim it tests had **already been confirmed retrospectively at seven earlier steps**
> in data on disk (arm A at k = 12, 16, 20, 24, 28; arm B at k = 16, 32), 6/6 conditions each.
> Predicting the eighth instance of an established recurrence is worth far less than predicting
> a novel one, and it does not belong in the same category as the 3D φ⁴ exponent or the pump
> rate law. **Re-graded: a confirmed recurrence, not a third advance prediction.**
>
> 2. **The mechanism I attributed is the wrong arm.** The k = 32 tooth is **arm B** (minimal
> linear code, `ns = 2^ceil(log2(k+1))`, steps at `k = 2^j`). `N0(k) = 4*ceil((k+1)/4)` is
> **arm A**. Both step at k = 32, which is exactly why k = 32 could not distinguish them — and
> they diverge immediately after. On arm B the mechanism predicts **no tooth at 36 or 40**; its
> next step is **k = 64**. Anything below reading "the next teeth are at 36 and 40" is arm-A
> arithmetic applied to an arm-B measurement.
>
> Also recorded there: arm A at k ≥ 32 is not expensive but **unreachable on this box** (N₀ ∈
> {36, 40, 44} is not a power of two, so the route falls back to 2^k float64 buffers — 34.4 GB
> for one buffer at k = 32 on a 31 GB machine), which `RENT_SCALING_PREREG` §1.4 had already
> declared. Logged UNTESTABLE ON THIS BOX rather than open. And the height law is now derived
> rather than assumed: `C = tooth·k / dln(ns)` is stable at 2.4–3.7 across both arms, five k and
> a 5× range of drop size — **the tooth goes like 1/k**, so the conserved-ratio band I supplied
> for k = 36 was about **6× too large**.


**Provenance, stated first.** Both rent-scaling agents hit session limits with all fifteen Q2
tiers (A25–A31, B25–B32) **completed and on disk** but `RENT_SCALING_RESULTS.md` unwritten.
This file records only the mechanical application of the **pre-registered** P-STEP32 rule
(`AMENDMENT 2`, adjudicator committed `aac3149` — **before the k = 32 datum existed**) to data
neither agent had yet read. It is a fragment for the owning agent to fold into RESULTS, not a
substitute for them. No number here was chosen after seeing the answer; the rule, the baseline
and the band were all pinned in advance.

## The rent curve, arm B (quotient-lean route), rent per nat

| condition | k=25 | 26 | 27 | 28 | 29 | 30 | 31 | **32** |
|---|---|---|---|---|---|---|---|---|
| ε=0.01, 10% | 0.11484 | 0.11229 | 0.10993 | 0.10777 | 0.10574 | 0.10387 | 0.10212 | **0.10809** |
| ε=0.01, 50% | 0.09210 | 0.09062 | 0.08926 | 0.08801 | 0.08684 | 0.08576 | 0.08475 | **0.08919** |
| ε=0.01, 1 nat | 0.12112 | 0.11917 | 0.11731 | 0.11557 | 0.11390 | 0.11233 | 0.11083 | **0.11719** |
| ε=0.05, 10% | 0.50728 | 0.49675 | 0.48702 | 0.47806 | 0.46968 | 0.46192 | 0.45468 | **0.47665** |
| ε=0.05, 50% | 0.40234 | 0.39661 | 0.39129 | 0.38638 | 0.38176 | 0.37746 | 0.37345 | **0.39045** |
| ε=0.05, 1 nat | 0.53339 | 0.52534 | 0.51768 | 0.51046 | 0.50353 | 0.49699 | 0.49077 | **0.51380** |

## P-STEP32 — CONFIRMED, 6 of 6, and inside the pinned band

`tooth(32) = L(32) − mean(L(29), L(30), L(31))`, `L(k) = ln(rent/nat)(k) − ln(rent/nat)(k−1)`.

| condition | tooth | resolution sd of the baseline |
|---|---|---|
| ε=0.01, 10% | **+7.469 pp** | 0.085 pp |
| ε=0.01, 50% | **+6.363 pp** | 0.063 pp |
| ε=0.01, 1 nat | **+6.972 pp** | 0.048 pp |
| ε=0.05, 10% | **+6.392 pp** | 0.078 pp |
| ε=0.05, 50% | **+5.585 pp** | 0.055 pp |
| ε=0.05, 1 nat | **+5.897 pp** | 0.044 pp |

**Positive in 6/6** (rule required ≥ 4/6) and **inside `[0.5, 2.0] × 3.869 pp = [1.935, 7.738] pp`
in 6/6**. Both clauses of the pinned CONFIRMED condition are met. Every tooth clears its own
baseline resolution by **65× to 145×**, so this is not a marginal call.

**The prediction was staked before the datum existed.** The adjudicator, the baseline (k = 29,
30, 31), the band and the ≥4/6 threshold were all committed at `aac3149` while B32 was still
computing. This is the campaign's **third** advance-prediction confirmation, after the 3D φ⁴
scaling exponent and the pump rate law.

## The plateau question — NO floor in the measured range

Within k = 25…31 the decline is smooth and monotone in all six conditions; the k = 32 tooth is
the ceiling's own sawtooth, not a floor. **No plateau is identified in this range**, and per the
prereg no extrapolation beyond it is licensed. The parent's k ≤ 24 finding — rent per nat falls
with size — extends to k = 31 without flattening.

## What this fragment does NOT do

It does not fit F1/F2/F3, does not run the arm-A (full-route) comparison, does not compute
ceiling fractions, and does not touch Q1 or the sibling's H-SUBSET/CENSUS material. Those remain
the owning agent's to write, against the recomputed ceilings (the parent's `ceiling` column is
unreliable below ~1e-9 — see the two numerical gates registered at `4cf6ba5`).
