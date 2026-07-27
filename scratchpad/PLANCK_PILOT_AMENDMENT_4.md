# AMENDMENT 4 — the ceiling fraction, and what actually backs its denominator

**A REPORTING requirement, added at the team lead's request for cross-campaign comparability.
Presentation only. It does not touch the pre-registered expectation, which stands unchanged: the
reading is expected to be consistent with zero, and a significant nonzero reading is a pipeline
defect until proven otherwise. No data reading has been taken at the time of writing.**

The requirement: report every headline reading, every residual and every floor as a **ceiling
fraction** — the measured share divided by the cap for the same slot count and alphabet — so that
this pilot's number can be set beside the other substrates already carrying it (designed LFSR
~100 %, QPU valve bulge ~8 %, 2D Ising critical ridge ~0.66 %, chaotic oscillator array ~0.03 %).

For a theorem-pinned-zero target the useful form is an **upper limit**: *the CMB's pairwise-blind
share is below X % of its ceiling at these scales, measured with these floors.* That is a real
statement about real sky data precisely because it is consistent with zero, and it is a
sensitivity statement as much as a measurement — so the floor and the sensitivity are reported in
the same units, never the limit alone.

---

## 1. THE DENOMINATOR, AND EXACTLY WHAT BACKS IT

The lead's instruction says to state the cap and its source, and not to manufacture one where none
exists. Doing that carefully turns up a correction worth propagating, because *"the machine-checked
cap"* is not quite what backs `ln 2` for tables like ours.

**Three binary slots. Headline denominator: `ln 2` = 0.6931472 nats = one bit.** Its four
supporting statements, separated by status:

| # | statement | status |
|---|---|---|
| 1 | **`share_parity`** (`Core/Share.lean`) — the parity state's share is exactly `log 2` | **MACHINE-CHECKED.** The ceiling is *attained*, so it is not a convention |
| 2 | **`shareK_le_of_pair_uniform`** (`Core/ShareK.lean`) — a `k`-slot state with **one uniform pair marginal** has share `≤ (k−2)·log 2`, i.e. `log 2` at `k = 3` | machine-checked, **but its hypothesis fails on our tables** |
| 3 | **`shareK_le_log_sub_pair`** (`Core/ShareK.lean`) — share `≤ k·log 2 − entropy(pairMarg i j)` for **any** pair, no uniformity hypothesis | **MACHINE-CHECKED and applicable**, but **looser than `log 2`** |
| 4 | `log 2` caps **every** three-bit state — Shearer's inequality `S(Q) ≤ ½ Σ_ij S(Q_ij)` plus `S(P) ≥ max_ij S(P_ij)` | **NOT MECHANIZED ANYWHERE IN THIS REPOSITORY.** An argument, checked numerically below |

**Why (2) does not cover these readings.** It hypothesises a *uniform pair marginal*. Two
thresholded CMB pixels at 8′ separation are strongly correlated, so their joint on four cells is
far from uniform. The theorem as stated does not apply here and is not claimed to. This is not
special to the CMB: **any** substrate whose slots are correlated has non-uniform pair marginals by
construction, which is most of the cross-campaign list.

**Why (3), the one that does apply, is the wrong direction.** A two-bit entropy is at most
`2·log 2`, so `3·log 2 − max_ij S(P_ij) ≥ log 2` always — with equality only when the pair marginal
*is* uniform. The repository's applicable mechanized bound is therefore **looser** than the number
being divided by, and it loosens further as the pair correlation rises.

**Consequence, and why `ln 2` is nonetheless the right choice.** `ln 2` is the *smaller*
denominator, so it yields the *larger*, more conservative upper limit — the right direction for a
limit. It is used as the headline, and the per-table `3·log 2 − max_ij S(P_ij)` is reported
alongside for every reading. What this document will **not** say is "machine-checked cap" for the
upper-bound direction, because at present it is not one.

> **The missing brick, named so it can be built:** Shearer's inequality at `k = 3` in Lean. It
> looks small, and it would upgrade the denominator of **every** campaign in the synthesis at
> once, not just this one.

### 1.1 The numerical check standing in for the unmechanized step

**PENDING** — a direct search over random three-bit states, reported in
`PLANCK_PILOT_RESULTS.md` §5.1 with its draw count and its worst reading. It is numerics, not a
proof, and is labelled as such wherever it appears.

---

## 2. `b > 2`: NO CAP OF ANY KIND IS MECHANIZED HERE

`shareK` is defined on `Fin k → Bool` — **binary slots only**. There is no cap for a `b`-ary
alphabet anywhere in this repository, mechanized or otherwise.

The `b = 3` and `b = 4` rungs are quoted against **`ln b`** — the same Shearer-plus-monotonicity
argument carried to alphabet size `b`, and it holds for **every** three-slot state, not only
pair-uniform ones: `share ≤ ½ Σ_ij S(P_ij) − max_ij S(P_ij) ≤ ½ max_ij S(P_ij) ≤ ½ · 2 log b =
log b`. That is a stronger statement than the `b = 2` mechanized bound of §1 (3) gives, and it is
**flagged NOT MACHINE-CHECKED on every line where it appears**, per the lead's instruction not to
manufacture a cap. Every `b ≥ 3` ceiling fraction in this pilot carries that flag in the JSON
(`cap_machine_checked: false`) as well as in the prose.

Recall also `PLANCK_PILOT_PREREG.md` §2: at `b ≥ 3` the reference is **not zero** — a discretised
Gaussian at `b ≥ 3` has genuinely nonzero order-3 connected information — so the `b ≥ 3` ceiling
fractions are *differential* quantities against the surrogate, and an absolute `b ≥ 3` ceiling
fraction quoted without its surrogate value is a reporting error.

---

## 3. WHAT IS REPORTED, PER INSTRUMENT AND PER `b`

1. **`upper_limit_ceiling_frac`** — the largest reading across the primary cells, as a fraction of
   the cap, with the cell it was attained at. *The estimator is positively biased at a true share
   of zero (the finite-sample floor adds, it does not subtract), so the raw reading bounds the
   truth from above with no further assumption.* This is the number the synthesis wants.
2. **`median_cell_ceiling_frac`** — the typical cell, so one heavy-tailed draw does not set the
   headline.
3. **`floor_ceiling_frac_null_median`** — the instrument's own noise level in the same units.
4. **`sensitivity_ceiling_frac_null_p95`** — **what this pilot could not have seen.** A limit
   without this is unreadable: below it, "consistent with zero" is a statement about the
   instrument, not about the sky.
5. **`ceiling_frac_vs_mechanized_cap`** — the same reading against the per-table
   `shareK_le_log_sub_pair` bound.

All five are emitted for every primary cell in `planck_pilot/analysis.json`, and the dye, valve,
boundary and degrade arms carry the ceiling fraction too.

---

## 4. WHAT THIS DOES NOT CHANGE

The primary grid, the twelve templates, the `b`-ladder, the surrogate counts, the primary test
statistic and its leave-one-out calibration, the pre-registered expectation of §7.1, and VOID
conditions V1–V8 are **untouched**. This amendment adds units to numbers; it does not change which
numbers are computed, nor what any of them would mean.

It also does not change the scope: **a ceiling fraction is not a cosmology result.** An upper limit
on the CMB's pairwise-blind share, at these scales, with these floors, from this pipeline, remains
a statement about this instrument on public maps — not about primordial physics.
