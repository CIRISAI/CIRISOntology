# AMENDMENT 5 — Amendment 4's central claim is now false, and one arm was citing the wrong theorem

**Two corrections, one of them to something this pilot told other campaigns. No data reading has
been taken. The primary grid, the templates, the ladders, the test statistic and VOID conditions
V1–V8 are untouched.**

---

## 1. THE DENOMINATOR IS PROVED. AMENDMENT 4 §1 IS SUPERSEDED.

`PLANCK_PILOT_AMENDMENT_4.md` audited the ceiling fraction's denominator and reported that the
**upper-bound direction was not mechanized anywhere in this repository** — that `ln 2` was backed
by attainment (`share_parity`), by a cap whose uniform-pair hypothesis no real table satisfies
(`shareK_le_of_pair_uniform`), and by a general cap that is *looser* than `ln 2`
(`shareK_le_log_sub_pair`) — with the universal bound resting on a Shearer argument that was not
in the Lean. It named the missing brick: *Shearer at k = 3, small, and it would upgrade every
campaign's denominator at once.*

**That brick has been built. `CIRISOntology/Core/ThirdCap.lean` (commit `8925843`) proves it, and
Amendment 4's claim is now FALSE.** It was true when written; it is not true now, and this pilot
propagated it to the team lead, so the correction is recorded loudly rather than quietly patched.

What is now machine-checked, sorry-free and axiom-audited (`Audit/AxiomAudit.lean` carries
`assert_no_sorry` and `assert_standard_axioms` for it):

| theorem | statement | what it fixes |
|---|---|---|
| **`share_le_log_two`** | `share p ≤ log 2` for **every** probability state on three binary slots, **no hypothesis on the pair marginals** | the gap Amendment 4 named. The denominator is proved |
| **`share_max_eq_log_two`** | attainment and bound together — `log 2` is the **exact maximum** on three bits | the ceiling is a proved number, not a convention |
| **`share_le_log_card_third`** | `share ≤ log(card of the third slot's alphabet)`, **general alphabets** | Amendment 4 §2's *"no cap of any kind is mechanized for `b > 2`"* is **also superseded**: `b = 3` and `b = 4` are capped at `ln b`, machine-checked |
| **`share_le_grouping_gaps`** | the **sharp, data-computable** ceiling `share ≤ H(pair) + H(remaining slot) − H(p)` in all three orientations; the honest ceiling is their minimum, each `≤ log 2` | replaces the `3·log2 − max H(pair)` bound this pilot was using, which was *looser* than `log 2` rather than tighter |

**Every "NOT machine-checked" flag on a ceiling fraction in this pilot is withdrawn.** The
`cap_machine_checked` field is now `true` at `b = 2, 3, 4`, with `Core/ThirdCap.lean` named as the
source in the JSON itself.

The `b ≥ 3` caveat that does **not** change: per `PLANCK_PILOT_PREREG.md` §2 the reference at
`b ≥ 3` is the surrogate's own reading and **not zero**, so those ceiling fractions remain
*differential* quantities, and an absolute one quoted without its surrogate value is still a
reporting error. That was never a statement about the cap.

### 1.1 The sharp ceiling, and why both numbers are reported

`share_le_grouping_gaps` is dramatically tighter on tables like ours. Verified here against the
new file:

| table | sharp ceiling (nats) | `ln 2` |
|---|---|---|
| the parity state | **0.6931471805599452** | 0.6931471805599453 |
| a random 2×2×2 table (seed 0) | **0.0216** | 0.693147 |

On parity the two coincide to the last digit, as they must. On a near-independent table — which is
what a Gaussian sky gives — the sharp ceiling is **~3 %** of `ln 2`. So this pilot reports **both**,
and they answer different questions:

* **against `ln 2`** — the cross-campaign comparable number, the one the synthesis wants;
* **against the sharp per-table ceiling** — the honest *headroom*: how much of the whole-only
  structure this particular table could have carried, given its own pair and single-slot entropies.

A ceiling fraction against `ln 2` alone would flatter a near-independent table, and one against
the sharp cap alone would not be comparable to anything.

### 1.2 The numerical check of §1.1 of Amendment 4, kept and now demoted to a consistency check

Run before `ThirdCap.lean` was known to exist, over **4 × 10⁵ random three-bit states**:

| ensemble | max share | as a fraction of `ln 2` |
|---|---|---|
| Dirichlet(1) on the 8-cell simplex, 2 × 10⁵ draws | 0.526590 | 0.7597 |
| Dirichlet(0.05), sparse/near-deterministic, 2 × 10⁵ draws | **0.663696** | **0.9575** |

Nothing crossed `ln 2`; the Shearer bound was violated in **0 of 20 000** draws and was strictly
below `ln 2` in **20 000 of 20 000**. Consistent with `pump-curve`'s independent 20 000-state
compliance run (max 0.6174). This is now a **consistency check on a proved theorem**, not evidence
for an unproved one, and it is labelled as such.

---

## 2. THE VALVE ARM WAS CITING A THEOREM WHOSE HYPOTHESIS THIS PIPELINE DOES NOT SATISFY

`pump-curve` states the licensing conditions for a valve-floor prediction: the noise must be a
**same-alphabet per-cell channel**, and the binarization must be **lumpable** with respect to it —
the noise must act identically within each block of the partition.

**Checked, and condition (b) fails here.** `PLANCK_PILOT_PREREG.md` §6.7 adds continuous noise to
a continuous field and binarizes **afterwards**. `binarize(x + e)` is not a function of
`binarize(x)`: a pixel just above the threshold flips readily, one far above essentially never.
The composite is therefore **not** a per-cell channel on the binary alphabet, and the binarization
is **not** lumpable with respect to additive noise. `Core/Valve.lean`'s `valve_needs_asymmetry` is
a statement about a kernel on `Bool`, and **it does not license the N-sym prediction.**

**The predictions do not change; the theorem behind them does, and it is a cleaner one.** For a
symmetric field `X` and independent symmetric noise `E`, `X + E` is symmetric under global
negation, so a split at the symmetry centre gives a sign-symmetric table and the share is exactly
zero — **directly by `share_eq_zero_of_signSymmetric`, with no channel formalism at all.** For
skewed `E`, symmetry is broken and the share may be nonzero. Same two predictions, correct
justification.

**Consequence for the gate-discharge list, stated as a downgrade.** `PLANCK_PILOT_PREREG.md` §7.4
claimed the N-sym arm would supply `GATES.md` **reach 9**'s missing *data* plumb line for the
valve. It will not: this pilot **does not test `valve_needs_asymmetry`**, because its pipeline does
not satisfy that theorem's hypothesis. What the arm does supply is a data-pipeline case for
`share_eq_zero_of_signSymmetric` **under additive noise on a real sky field** — still a filled
cell, and still worth having, but it is a different cell and the results document will say so.

### 2.1 An added arm that DOES satisfy the hypothesis — and tests `pump-curve`'s rate law

Since the licensing conditions fail only because of the *order* of operations, they can be made to
hold by reversing it. **Arm G7b**, declared here before it runs:

Take the binarized surrogate slots — sign-symmetric, share pinned at the floor — and apply an
**independent per-slot binary asymmetric channel** with flip probabilities `(p01, p10)` directly to
the bits. That is a same-alphabet per-cell channel on the binary alphabet, trivially lumpable
because the alphabet *is* the partition. `valve_needs_asymmetry` then applies, and so does
`pump-curve`'s measured rate law (`scratchpad/PUMP_RESULTS.md`, commit `2dc6cfc`):

> `share = 18 r₀⁴ a² / [(1 + 2r₀)(1 + 3r₀)(1 − r₀)]`, with `r₀ = (1 − 2s)² ρ`,
> `a = p01 − p10`, `s = (p01 + p10)/2`.

**This is a forward prediction with no free parameters**, on a substrate the law was not fitted to:
`ρ` is the *measured* sign-correlation of real sky triples, and the equilateral templates `E032`,
`E064`, `E128` supply three different values of it. Pre-registered before the run: the law is
credited to `pump-curve` and is **not** this pilot's result; what this pilot contributes is a test
of it at a `ρ` the pump campaign did not choose. Reported as agreement or disagreement in
percentage terms, with the floor subtracted and matched to sample size.

Declared limitation: the law assumes a single `r₀`, i.e. all three pair correlations equal, so
**only the equilateral templates are used** — the folded and squeezed families have unequal pair
correlations and are excluded from G7b by construction, not by result.

---

## 3. `k ≥ 4` — NOT APPLICABLE, RECORDED ANYWAY

`pump-curve` warns that `valve_needs_asymmetry` is a three-slot theorem and does not generalise,
and that symmetric noise alone mints 1–1.6 % of the `(k−2)·log 2` ceiling at `k = 4…7`.
**Every reading in this pilot is `k = 3`** — three pixels at an angular template. The warning does
not bite here and no `k ≥ 4` number is produced. It is recorded so that a future sky campaign at
four or more slots does not inherit this pilot's `k = 3` reasoning by habit.

---

## 4. ON THE FLOOR FORMULA — AGREEMENT, NOT A CORRECTION

`pump-curve` warns that the naive `(cells − 1)/2N = 3.5/N` overstates the `k = 3` finite-`N` floor
by 15×, the correct median being `0.227/N` with a `χ²` of **one** degree of freedom.

**This pilot never used the naive formula.** Its floors are *measured* from 300 phase-randomised
surrogates per cell, and its one analytic cross-check already uses the one-degree-of-freedom form:
`N_eff = 0.45494/(2·median)`, i.e. `median = 0.2275/N` — the same number. Recorded as an
independent agreement between two campaigns rather than as a correction to either.

---

## 5. WHAT THIS DOES NOT CHANGE

The primary grid (72 cells), the twelve templates, the `b`-ladder, the surrogate counts, the
primary test statistic and its leave-one-out calibration, the pre-registered expectation of §7.1,
and VOID conditions V1–V8 are **untouched**. No data reading has been taken.

The scope is also untouched: a ceiling fraction against a now-proved denominator is still **not a
cosmology result**.
