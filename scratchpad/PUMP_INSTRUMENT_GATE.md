# PUMP instrument — INDEPENDENT GATE (task #9)

**What this is.** `scratchpad/pump_curve.py` was written by one agent; this is a second agent
gating it. The discipline followed throughout: **nothing here imports `pump_curve`'s solvers in
order to check `pump_curve`'s solvers.** The share is recomputed by a **third** method, the channel
is checked **bit-exactly against a machine-checked rational identity in `Core/Valve.lean`**, and the
one external calibration is a **published figure produced by other people with other code**.

Verifiers, committed beside their logs and re-runnable:

| | |
|---|---|
| `scratchpad/gate_pump_indep.py` / `.log` | gates 1–6: channel, plumb lines, 4000 random states, P-EVEN, moment law, Schneidman Fig. 1 |
| `scratchpad/gate_kge4.py` / `.log` | gate 7: the k-general dual solver, and never-from-nothing at k = 4…6 |
| `scratchpad/gate_pform_literal.py` / `.log` | P-FORM as **written** vs P-FORM as **implemented** |
| `scratchpad/gate_shape.py` / `.log` | the shape of the pointwise deviation |

**The third solver.** Brent's method on the stationarity condition
`Π_even p = Π_odd p` along the parity-character line, with a 200 001-point dense-grid fallback
bracket. Structurally unlike golden section (the instrument's primal) and unlike the repository's
bisection (its root method). `Core/Share.lean`'s envelope at k = 3 is the one-parameter line
`p + tχ`, so this is exact, not approximate.

Box discipline: CPU only, `nice -n 15`, `OMP_NUM_THREADS=1`, single process. The box was at load
average 17 and GPU 100 % throughout (glass, water, rent-scaling, Planck running); no GPU requested,
total wall time under a minute.

---

## VERDICT

**The instrument passes every gate, and two of the passes are strong** — bit-exact agreement with a
machine-checked theorem, and exact reproduction of a 2003 published table. **One finding is
material and is not an instrument fault:** P-FORM as *written* in the prereg and P-FORM as
*implemented* in the instrument are different tests, and they return **opposite verdicts**. §3.

**And I must correct my own `PUMP_PREREG_ADDENDUM.md` Finding 1.** Its diagnosis stands; its
mechanism attribution was partly wrong and **its proposed remedy is withdrawn — the remedy makes
the fit worse, not better.** §4.

---

## 1. Gates 1–7, all PASS

| # | gate | staked | measured |
|---|---|---|---|
| **1** | channel vs `Core/Valve.channel3_damp_ferro`: `channel3 damp damp damp ferro = bulge`, i.e. 9/16 on `(0,0,0)` and 1/16 on each other cell | exact | **0.000e+00** — bit-exact against a machine-checked rational identity |
| **2** | seven plumb lines (below) | — | all pass |
| **3** | golden-section vs bisection, 4000 random states | ≤ 1e−12 | **8.882e−16** |
| **3′** | instrument mean vs the **independent third solver**, same 4000 states | — | **8.882e−16** |
| **4** | **P-EVEN**, `Δ(−a,s) = Δ(+a,s)` on `ferro`, 20 configurations | ≤ 1e−12 | **4.441e−16** |
| **5** | moment law `m = a`, `r = r₀+a²`, `c = 3r₀a+a³` (prereg §4.3), 27 configurations | — | **1.665e−16** |
| **6** | **Schneidman 2003 Fig. 1** — the one external calibration | see below | exact |
| **7** | k-general dual solver + never-from-nothing at k = 4…6 | see §2 | all pass |

### Plumb lines (gate 2), share recomputed independently

| state | theorem | independent | instrument | 2-solver gap |
|---|---|---|---|---|
| `parity` | `share_parity = ln 2` | 6.931471805599e−01 | 6.931471805599e−01 | 4.4e−16 |
| `ferro` | `share_ferro = 0` | 0.000000000000e+00 | 0.000000000000e+00 | 0.0 |
| `indep` | `share_indep = 0` | 0.0 | −2.2e−16 | 4.4e−16 |
| product | `share_prod3 = 0` | 0.0 | 3.3e−16 | 2.2e−16 |
| sign-symmetric (random) | `share_eq_zero_of_signSymmetric` | 2.2e−16 | 2.2e−16 | 0.0 |
| `bulge = damp³·ferro` | `valve_upward_bound ≥ 0.011961808` | **0.021185154563** | 0.021185154563 | — |
| every reading | `share_le_log_two ≤ ln 2` | pass | pass | — |

### Gate 6 — Schneidman, Still, Berry & Bialek 2003, Fig. 1

The external calibration `PUMP_PRIOR_ART_ADDENDUM.md` §A1 asked for. `Core/Share`'s `share` **is**
their `I_C^(3)` (their Eq. 6), so this is definitional, not analogical:

| gate | our `I_C^(3)` | paper | our `I_C^(2)` | paper |
|---|---|---|---|---|
| AND | **0.0000** bits | 0.0000 | **0.8113** bits | 0.8113 |
| OR | **0.0000** bits | 0.0000 | **0.8113** bits | 0.8113 |
| XOR | **1.0000** bits | 1.0000 | **0.0000** bits | 0.0000 |

Four significant figures against a 2003 PRL table, from independent code. **Fig. 1 is discharged;
Fig. 2 — the nine noise-swept panels, which are the actual pump curve in print — is still not
run**, and remains the campaign's outstanding external check.

---

## 2. Gate 7 — the k-general solver

| check | result |
|---|---|
| **7a** general dual vs the exact 1-D solver, 300 random k = 3 states | worst \|dual − exact\| = **8.882e−16** (staked 1e−6) |
| **7b** the same on **pumped, near-deterministic** states — the `ipf-sharek-boundary-drift` regime | worst = **4.441e−16**; and **IPF/exact = 1.0000 on all 7**, so the stored taint does **not** reproduce here |
| **7c** k = 4,5,6 repetition under the pump: two-sided bracket, cap compliance | bracket **0–4.4e−16** (staked 1e−6), moment residual **1.1–3.3e−16**, all `≥ 0`, all `≤ (k−2)·ln2` |
| **7d** **never from nothing** at k = 4,5,6: a product input through the channel | **±4.4e−16** — exactly zero to machine precision |

**7d is worth naming.** `valve_from_nothing` is a k = 3 theorem; at k = 4…6 the instrument
*measures* what the theorem asserts at k = 3, and gets zero to 4e−16. That is the honest form of
the k ≥ 4 claim flagged in `PUMP_PREREG_ADDENDUM.md` Finding 4 — an **instrument check**, not a
plumb line, because no theorem in this repository covers it.

The IPF result in 7b is a **negative** finding worth recording: `ipf-sharek-boundary-drift` warns
that IPF one-sidedly overstates near determinism by five orders of magnitude. On these states, at
these tolerances, it does not. The memory is not wrong — it is about a different, sparser regime —
but the pump's states are not in that regime, and IPF and the dual agree to 1.0000.

---

## 3. THE MATERIAL FINDING — P-FORM as written and P-FORM as implemented disagree

Prereg §4.3 stakes the kill as:

> "measured `Δ/a²` departing from the closed form by more than **2 %** **anywhere** in
> `κ ∈ [0.1, 0.95]`, in the regime where the expansion is declared valid."

That is a **pointwise** test. The instrument implements a different one: it fits `C` in the `a → 0`
limit and compares `C_measured/C_closed_form`. Both are defensible; they are not the same test, and
on the committed run they give **opposite** answers.

**As implemented** — `C_ratio ∈ [1.0000036, 1.0000285]` across all 13 rows. **PASS**, and it is a
real result: the closed form's coefficient is confirmed to four or five significant figures over
seven decades of `C`, from 7.16e+01 at κ = 0.99 down to 1.73e−07 at κ = 0.10.

**As written** — recomputed pointwise with the independent solver at the top of each row's own
declared window:

| κ | 0.99 | 0.98 | 0.96 | 0.90 | 0.85 | 0.80 | 0.70 | 0.60 | 0.50 | 0.40 | 0.30 | 0.20 | 0.10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dev % | 4.50 | 4.37 | 4.15 | 3.85 | 4.04 | 4.65 | 7.43 | 12.97 | 22.76 | 25.80 | 29.66 | 33.67 | **36.85** |

**13 rows out of 13 exceed the staked 2 %.** Under the literal wording, P-FORM fires everywhere.

**This is not a physics failure and not an instrument fault.** The closed form is an `a → 0`
expansion; nobody claimed pointwise accuracy at the top of a two-decade window, and the deviation
is exactly the next term. But the record currently says "P-FORM passed" against a criterion that,
as written, failed on every row, and `epistemology.md` rule 7 is *report the fired kill as plainly
as the survival.*

**Recommendation, and it favours the implementation.** Restate the kill on `C` — which is what it
should always have been, per `PUMP_PRIOR_ART_ADDENDUM.md` §A3: *the exponent is textbook, the
coefficient is the deliverable.* Then P-FORM is a real stake and it genuinely passes. But the
restatement is an **amendment** and must be logged as one, with the pointwise table above kept, not
dropped.

**Why the implemented test is safe.** The deviation is a clean **relative `a²` correction** —
fitting `(ratio − 1)` against `a` gives exponent **2.015** at κ = 0.99 and **2.018** at κ = 0.50.
So `Δ = C(r₀)a²(1 + B(r₀)a² + …)` with the expansion well-behaved, and extracting `C` at `a → 0`
over nine geometrically-spaced points spanning two decades is sound. The measured ratios walk
smoothly from 1.000004 at the bottom of the window to 1.045 at the top (κ = 0.99), and from
1.000020 to 1.228 (κ = 0.50).

---

## 4. CORRECTION TO MY OWN `PUMP_PREREG_ADDENDUM.md` FINDING 1

Stated plainly because it changes what someone should do.

**What stands.** The declared validity region is too loose for a pointwise 2 % band. §3's table is
the direct measurement of that, and it is worse than my estimate: I predicted the problem would
bite hardest at low κ, and it does (36.9 % at κ = 0.10), but there is also a **~4 % floor at every
κ** that my analysis did not predict at all.

**What was wrong.** I attributed the deviation to the `r₀ → r₀ + a²` shift in the expansion point.
At κ = 0.99 that term contributes about **0.13 %** of the observed **4.50 %** — so at high κ the
mechanism I named is **not** the dominant one. The rest is the genuine `O(a⁴)` term (the `m = a`
correction to `c*` and the cubic term in `Δc`), which I flagged as same-order and then failed to
account for.

**What is withdrawn.** My recommendation to "quote `C` at the output's own raw `r`" — the one-line
fix — **is wrong and must not be applied.** Measured, at κ = 0.50, a = 0.25:

| evaluation | ratio to the exact value |
|---|---|
| `C(r₀)·a²` — the prereg as written | **1.228** (23 % high) |
| `C(r₀+a²)·a²` — my proposed "fix" | **0.553** (45 % low) |

The remedy overshoots and is **worse than the thing it was meant to fix.** My own addendum warned
that the `m = a` correction enters at the same order with the opposite sign and that this "is not a
one-line patch"; I then recommended the one-line patch anyway. Withdrawn.

**What to do instead:** restate P-FORM on `C` (§3). Do not re-expand before the run.

**Net effect of Finding 1 on the committed run: none for `C`, and the exponent drift is explained.**
The fitted exponents run 2.0056 → 2.0720 monotonically as `r₀` falls, entirely inside the staked
[1.90, 2.10]. That drift is a **fitting-window artifact**, not a property of the pump, and
`PUMP_RESULTS.md` should say so rather than report a κ-dependent exponent as physics.

---

## 5. A number worth carrying

`PUMP_PREREG_ADDENDUM.md` Finding 3 could only prove, from `valve_upward_bound`, that the closed
form under-predicts by **≥ 25 %** at `damp`. Now measured:

| | |
|---|---|
| closed form at `damp` (a = ½, s = ¼, ρ = 1) | 0.008929 nat |
| **exact, independent solver** | **0.021185 nat** |
| machine-checked lower bound `valve_upward_bound` | 0.011962 nat |

The truncated form delivers **42 %** of the true value at `Core/Valve.lean`'s own witness — the
expansion is off by a factor **2.37** there. This is a boundary point (`a = 2s`, the Z-channel
edge), far outside any validity region, and it is the sharpest available statement of why the QPU
overlay must use the exact solver rather than the closed form wherever the hardware runs to large
`a`. Prereg §4.5 already requires that; this is the number behind it.

Incidentally it also tightens a Lean fact: `valve_upward_bound` proves `share(bulge) ≥ 0.011962`
from one competitor at `t = −1/32`. The true value is **0.021185**, so the machine-checked bound
captures **56 %** of the share it bounds. Recorded, not acted on — no Lean is touched here.

---

## 6. WHAT IS *NOT* GATED

1. **Schneidman Fig. 2** — the nine noise-swept panels. Fig. 1 is discharged; Fig. 2 is the one
   that is actually a pump curve, and it is still not run. This is the campaign's outstanding
   external check and the cheapest remaining piece of work.
2. **Arms F (coarse-graining) and G (sampled)** were not independently verified — only the exact
   same-alphabet core. Arm F crosses the alphabet boundary and carries its own separable verdict;
   arm G is the sampled arm and its estimator floor was not re-derived here.
3. **`stage_dose`, `stage_qpu`, `stage_coarse` outputs were not re-checked.** This gate covers the
   solvers, the channel, and arm A's P-FORM/P-EXP readings. The QPU overlay in particular is
   untouched by me.
4. **k ≥ 7 was not exercised.** Gate 7 ran k = 4, 5, 6.
5. **The `n`-sweep's interior peak has no mixture null**, per `PUMP_PREREG_ADDENDUM.md` Finding 5,
   and nothing here changes that.

---

## 7. FOR `PUMP_RESULTS.md` — the amendments this gate forces

| # | amendment | why |
|---|---|---|
| 1 | **Restate P-FORM on `C`, log it as an amendment, and keep §3's pointwise table** | as written, the kill fired on 13/13 rows; as implemented it passes. Both must be in the record |
| 2 | Report the exponent drift 2.0056 → 2.0720 as a **fitting-window artifact**, not as physics | it tracks `r₀`, and the deviation is a clean relative `a²` term |
| 3 | Withdraw the `C(r₀+a²)` remedy wherever it was carried forward | measured: 0.553 vs 1.228 — worse than the original |
| 4 | Carry the `damp` number: closed form 0.008929 vs exact 0.021185, factor 2.37 | it is why the QPU overlay must use the exact solver at large `a` |
| 5 | Mark the k ≥ 4 zero-share readings **instrument checks**, not plumb lines | no theorem here covers general k; gate 7d measures it at 4e−16 |
| 6 | Record that IPF **agrees** with the dual on these states | `ipf-sharek-boundary-drift` does not reproduce in this regime, and saying so is as much a duty as invoking it |

*No Lean touched, `lake` never run, nothing moves `Stance.lean`. Corrections owed to
`Core/Valve.lean` remain as named in `PUMP_PRIOR_ART_ADDENDUM.md` §12 — named, not made.*
