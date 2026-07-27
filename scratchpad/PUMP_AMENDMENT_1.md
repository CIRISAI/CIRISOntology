# PUMP campaign — AMENDMENT 1

**Dated 2026-07-27, after `PUMP_PREREG.md` (commit `64028fb`) and after partial results were
seen.** That is stated first because it is the thing that matters: every change below was made
*with data in hand*, and each one says exactly what was seen and whether it touches a staked
prediction. None of them changes the content of P-EVEN, P-EXP, P-FORM, P-K or P-QPU, and none
was made to rescue a stake. Three were forced by the instrument, one by a discovery, one is an
honest correction to a band the prereg drew too wide.

---

## 1. The instrument's DEPTH — declared, because the prereg gated on cells and not on the reading

**What was seen.** The first `curveA` run returned `exponent = NaN` at κ = 0.05 and κ = 0.02, and
the `P_EXP_pass` summary read False on that account alone. Diagnosis: at those strengths the
predicted coefficient is `6.96e-10` and `4.6e-13`, so at the a-values in use the share was
`1e-18`-ish — the solver returned **exactly zero**, and `log 0` produced the NaN.

**Why the prereg missed it.** Section 5's reach-11 row gated on *cell occupancy* (`any cell below
1e-12 is ungauged`) and no cell was anywhere near that. The reading itself was below the
instrument's resolution and nothing was watching for it. That is the same reach — depth — applied
to the wrong quantity.

**The amendment.** The k = 3 two-solver bracket was measured at **6.6e-14 nat** over 20 000 random
states (`pump_dye.json`). A reading below **1e-11 nat** — 150× the measured bracket — is declared
**UNGAUGED**: not zero, not a detection. The a-window for every fitted row is then chosen *from
measured values only*: start at the top of the declared expansion band, walk down geometrically,
and drop points once the **measured** share falls below the depth. No predicted value enters the
window choice, so the window cannot bias the exponent it is used to fit.

**What it changes:** two rows of arm A (κ = 0.05 and 0.02) and zero rows of arm B are now reported
as **ungauged rather than as measurements**, with the reason stated. Nothing else moves. The
honest reading is that this is not a limitation to apologise for but a **measured result**: the
pump falls off as κ⁸ and **passes below our instrument's floor at κ ≲ 0.1**.

## 2. Arm C: the symmetric baseline is separated from the asymmetry-driven excess — a DISCOVERY, not a fix

**What was seen.** The first `curveC` run returned `exponent ≈ 0.005` at k ≥ 4 with coefficients
around `1e4` — obvious nonsense as a pump measurement, and the signature of a **constant** term
swamping the a-dependence.

**Diagnosis, and it is real physics rather than a bug.** Checked directly:

- `share(repetition(k)) = 0` exactly at every k = 3…7 (measured ≤ 5e-14, at the dual solver's floor);
- at k = 3 the **unital** (a = 0, flip-covariant) channel mints **exactly zero** — `valve_needs_asymmetry` confirmed to 4e-16;
- at k = 4, 5, 6, 7 the same unital channel mints **strictly positive** share — 0.0132, 0.0273, 0.0428, 0.0566 nat at s = 0.1 — on an output verified sign-symmetric to **7e-18**.

**`Core/SignSymmetry.share_eq_zero_of_signSymmetric` is a THREE-SLOT theorem, and
`valve_needs_asymmetry` inherits that restriction.** Sign symmetry kills the *odd* orders; from
four slots up the *even* orders survive it. This programme's own `SPIKE_SURVEY.md` recorded
exactly that numerically (four variables: odd orders at 1.7e-13 while order 4 survived at 0.169
nats) and the consequence for the valve was never drawn.

**The amendment.** Arm C reports two objects instead of one:

| | |
|---|---|
| `B_k(s)` | the **symmetric baseline** — what unital noise alone mints. Zero at k = 3, positive at k ≥ 4 |
| `D_k(a,s)` | the **asymmetry-driven excess**, `share(a,s) − B_k(s)`. This is the pump |

**This is not a correction of the prereg's observable.** The prereg defined `Δ = share(K·p) −
share(p)` and noted `share(p) = 0` on every arm, which is *true and measured*. What the prereg
got wrong was the unstated assumption that `Δ(a=0) = 0` at every k, imported from a k = 3
theorem. `Δ` is still reported as defined; it is now also decomposed, because `Δ(0,s) = B_k(s)`
turns out to be a nonzero object nobody expected. P-EXP is tested on `D`, which is the quantity
the hypothesis was about.

## 3. The dual solver's Newton polish — a gate fired on our own instrument

**What was seen.** The first `dye` run had `dual_vs_exact_max = 7.1e-9` against a staked 1e-9 —
the k = 3 plumb line **fired on the k ≥ 4 machinery**. L-BFGS-B's stopping tolerance, not an
accuracy floor.

**The amendment.** Sixty Newton steps on the dual, whose Hessian is the feature covariance under
`q` and is available in closed form. Re-gated: **1.55e-15**, inside the stake by six orders of
magnitude. The firing is kept in the record because a plumb line that fires and is quietly
re-tuned has stopped being a plumb line.

## 4. Arm F gets a dye test, because without one its exponent means nothing

**What was seen.** Arm F's binarized reading came back with exponent 1.09–1.53 in its own
abscissa. Before reporting that as "the a² law fails under coarse-graining", one thing had to be
ruled out: arm F's abscissa parametrizes the **fine** channel, and a non-lumpable fine channel
induces no well-defined binary per-cell channel at all, so its exponent is not comparable to arm
A's by construction.

**The amendment.** A **lumpable** positive control was added — a four-letter channel that acts
identically within each block of the partition, and therefore *does* induce an exact binary
per-cell channel with known `(a, s)`. Result: exponent **2.02–2.03**, coefficient ratio to the
closed form **1.00002**. The instrument reads the a² law correctly through a coarse-graining when
the law is there. The difference between 2.02 and 1.09–1.53 is therefore the coarse-graining, not
the probe.

## 5. The expansion band was drawn too wide for a claim about the VALUE — measured and corrected

The prereg declared the closed form valid for `|a| ≤ 0.25`, reasoning that the next term is
`O(a⁴)` and `0.25² = 6 %`. Measured, at s = 0.1:

| a | closed form / exact |
|---|---|
| 0.008 | 0.9997 |
| 0.048 | 0.9898 |
| 0.100 | 0.9555 |
| 0.148 | 0.9016 |
| 0.200 | 0.8158 |

So the closed form is within **2 % of the value only for a ≲ 0.07**, not 0.25. The a⁴ term is
larger than the prereg's estimate.

**[SUPERSEDED BY AMENDMENT 2 — the sentence that opened this paragraph read "This does not move
P-FORM's verdict", and that was wrong. It does: P-FORM's verdict is now TWO rows, a pass on the
coefficient and a firing on the literal pointwise wording. The paragraph is kept as written, with
its superseded claim struck, per the current-numbers-hygiene gate.]**

~~This does not move P-FORM's verdict, and the reason is stated so it cannot look like a rescue.~~
P-FORM stakes the **coefficient** `C = lim_{a→0} Δ/a²`, which is measured at the smallest a in
each row and is confirmed to 3e-4. The band correction affects only how far out the formula may
be quoted as a value. Both are reported: **the coefficient to 3e-4, the value to 2 % out to
a ≈ 0.07 and to 20 % out to a ≈ 0.2**, with the exact solver quoted beyond. What this paragraph
missed — and AMENDMENT 2 fixes — is that the prereg's kill was worded *pointwise*, so the gap
measured here is not merely a quoting caveat: under the literal wording it is a fired kill.

---

## What was NOT amended

No staked band was widened. No kill was withdrawn. P-K's stake (K-COUNT) was left exactly as
written and is **refuted by the measurement** — see `PUMP_RESULTS.md`, where it is reported as
loudly as the passes.

---

# AMENDMENT 2 — P-FORM is restated on the coefficient, and the pointwise table is kept

**Dated 2026-07-27, after `PUMP_RESULTS.md` was committed (`2dc6cfc`) and in response to an
independent gate of this campaign's instrument by a second agent
(`PUMP_INSTRUMENT_GATE.md` §3, commit `a4d3b38`). The finding is theirs, it is correct, and it
is logged here because it is *this* pre-registration's wording that was ambiguous and *this*
results document that carried the under-qualified verdict.**

**The two tests.** `PUMP_PREREG.md` §4.3 states the kill as: *"measured `Δ/a²` departing from the
closed form by more than 2 % **anywhere** in `κ ∈ [0.1, 0.95]`"* — a **pointwise** test. The same
prereg, §3, defines the observable as **`C ≡ lim_{a→0} Δ/a²`** — a **limit** test. The instrument
implemented the limit. They are different tests and on the committed run they return **opposite
verdicts**.

**As implemented (the limit):** `C_ratio ∈ [1.0000036, 1.0000285]` on all 13 gauged rows, across
seven decades of `C` (7.16e+01 at κ = 0.99 down to 1.73e−07 at κ = 0.10). **PASS**, and a real one.

**As literally written (pointwise, at the top of each row's own declared window),** recomputed by
the second agent with a solver independent of this campaign's:

| κ | 0.99 | 0.98 | 0.96 | 0.90 | 0.85 | 0.80 | 0.70 | 0.60 | 0.50 | 0.40 | 0.30 | 0.20 | 0.10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| deviation % | 4.50 | 4.37 | 4.15 | 3.85 | 4.04 | 4.65 | 7.43 | 12.97 | 22.76 | 25.80 | 29.66 | 33.67 | **36.85** |

**13 of 13 exceed the staked 2 %.** Under the literal wording P-FORM fires everywhere.

**This is not a physics failure and not an instrument fault.** The closed form is an `a → 0`
expansion; the deviation is the next term, and it is well-behaved — fitting `(ratio − 1)` against
`a` gives exponent **2.015** at κ = 0.99 and **2.018** at κ = 0.50, so `Δ = C(r₀)·a²(1 + B(r₀)a² + …)`
and extracting `C` over nine geometrically spaced points spanning two decades is sound.
`AMENDMENT 1` §5 already reported the value-versus-coefficient gap and measured it (2 % out to
a ≈ 0.07, 18 % low at a = 0.2). What it did not do — and this is the correction — is carry that
qualification into the **verdict line**, which read a bare "PASS".

**The amendment.** **P-FORM is restated on the coefficient `C = lim_{a→0} Δ/a²`, kill band 2 %.**
That is the deliverable — the exponent is textbook, the coefficient is what nobody had measured —
and on that statement P-FORM genuinely passes at 0.03 %. The pointwise reading is **not dropped**:
the table above stays, and the verdict grid in `PUMP_RESULTS.md` now carries **both rows**, the
pass and the firing, because `epistemology.md` rule 7 is *report the fired kill as plainly as the
survival* and a restatement that made the inconvenient number disappear would be the exact failure
that rule exists to prevent.

**What a reader should take.** The closed form's **coefficient** is confirmed to four or five
significant figures over seven decades. The closed form as a **formula for the value** is good to
2 % only for a ≲ 0.07 and is ~37 % low at the top of the widest window. Quote the first; do not
quote the second without its band.

**Also recorded from the same gate, in its favour:** the instrument passed every one of the second
agent's seven independent checks, two of them strong — applying its channel to `ferro` with `damp`
kernels reproduced `Core/Valve.lean`'s `channel3_damp_ferro` (9/16, 1/16 × 7) at error **exactly
0.000e+00**, and Schneidman et al. 2003's Fig. 1 came back at four significant figures from
independent code (AND/OR at `I_C^(3)` 0.0000 and `I_C^(2)` 0.8113 bits; XOR at 1.0000 and 0.0000).
A third, structurally different solver (Brent on the stationarity condition, with a 200 001-point
dense-grid fallback) agreed with both shipped solvers to 8.9e-16.

---

# AMENDMENT 3 — the phenomenon and the first curve are 2003, the pump is a convex combination, and "asymmetry" has two hypotheses not one

**Dated 2026-07-27, after `PUMP_RESULTS.md` (`2dc6cfc`) and AMENDMENT 2 (`cc01ed2`), prompted by a
second agent's sweep (`PUMP_PRIOR_ART_ADDENDUM.md`, `a758ebc`). Their finding; I verified it
against the primary source and then measured the part that was exactly computable, because on this
one an inference was not good enough.**

## 3.1 A sentence in `PUMP_PRIOR_ART.md` was false, and the leg it supported shrinks

Verified verbatim from arXiv `physics/0307072`'s text layer: Schneidman, Still, Berry & Bialek,
PRL 91:238701 (2003), **Fig. 2 plots `I_C^(3)` against noise amplitude**, and the body text says
*"pure 2-body interactions such as AND and OR show a 3-body interaction component for some types
of noise."* My L4 said no curve had ever been published. **It had, in the paper we cite for the
quantity.**

Which noise column does it was a figure reading neither agent could extract, so it was **computed**
(`pump_schneidman_fig2.py`, `.log`, `.json`; Fig. 1 reproduces at four figures as the calibration):

| gate | column | per-cell? | created `I_C^(3)` |
|---|---|---|---|
| **AND** | **P(flip σ₃)** | **yes** | **0 → 0.0774 bits, peak q = 0.10** |
| **OR** | **P(flip σ₃)** | **yes** | **0 → 0.0774 bits, peak q = 0.10** |
| AND/OR | P(flip σ₁) | no | none |
| OR | P(flip σ₃\|σ₁=σ₂=1) | no | 0 → 0.6031 bits |

**L1 is scooped from 2003, by a per-cell channel, on a state with exactly the `ferro` starting
condition** (zero whole-only share, 0.8113 bits of pure pair structure). L4's CLEAR verdict
survives **only for the asymmetry-resolved law** — exponent, closed-form coefficient, pinned zero,
k-scaling, hardware overlay. Corrected in place at the head of `PUMP_PRIOR_ART.md`, with the false
clause struck rather than deleted.

## 3.2 "The pump is asymmetry" has TWO hypotheses, and this campaign only found the second limit

The channel that creates in Schneidman's AND panel is a **fixed-probability flip** — the binary
symmetric channel, which is **unital**, i.e. exactly the `IsFlipCovariant` class
`valve_needs_asymmetry` says mints nothing. It mints. The reason is that **AND is not
sign-symmetric**, and the theorem hypothesises the *state* as well as the channel.

So the honest statement is that `valve_needs_asymmetry` needs **both**:

| hypothesis | status | what breaks it |
|---|---|---|
| three slots | **measured false at k ≥ 4 by this campaign** (`PUMP_RESULTS.md` §2, 1–1.6 % of the ceiling) | the repetition code at k = 4…7 |
| sign-symmetric input | **published counterexample since 2003** | Schneidman's AND under a unital per-cell flip |

`PUMP_RESULTS.md` §2 reported the first as "the campaign's most consequential finding" and did not
mention the second. **State asymmetry and channel asymmetry are independent axes**, and every
sweep in arms A–E holds the input sign-symmetric, so the a = 0 control is pinned **along that axis
only**. Any continuation that varies input asymmetry loses the pinned zero silently.

## 3.3 The pump IS a convex combination — measured exactly, and it answers Kahle's open question

A per-cell channel is linear and `ferro` is a two-point mixture, so

> **`K(ferro) = ½·K(δ₀₀₀) + ½·K(δ₁₁₁)`**

and each `K(δ)` is a **product** state. Measured: `|mixture − output| = 0.00e+00` exactly, and

| s | a | share(component 1) | share(component 2) | share(**mixture**) |
|---|---|---|---|---|
| 0.10 | 0.20 | 0.00e+00 | 0.00e+00 | **0.061776** |
| 0.20 | 0.30 | −3.3e-16 | 0.00e+00 | **0.015717** |
| 0.25 | 0.50 | 0.00e+00 | −2.2e-16 | **0.021185** |
| 0.25 | **0** | 0.00e+00 | −1.1e-16 | **0.00e+00** |

**Two constituents of whole-only share exactly zero; the combination carries the closed form.**
Kahle, Olbrich, Jost and Ay called *"whether the complexity of a convex combination of two
distributions is related to the complexities of the individual constituents"* an **unsolved
problem**. For this family the constituents are exactly zero and the combination is
`18r₀⁴a²/[(1+2r₀)(1+3r₀)(1−r₀)]`. That is a better and more accurate statement of what this
campaign contributes than "the rate at which noise pumps", and it is the one to use.

## 3.4 GATES.md reach 3 (mixture null) — restated, because my discharge was the wrong argument

`PUMP_RESULTS.md` listed the `a = 0` control as a discharged mixture null "theorem-pinned". A
second agent objected that a null which *provably* reads zero cannot **manufacture** the effect,
and reach 3 requires the null to be able to. **The objection is right about the wording and the
measurement answers it better than either of us argued.**

The mixture does not fail to manufacture the effect — **the mixture is the effect** (§3.3). So the
gate cannot be "mixture versus no mixture"; there is no no-mixture arm. What the `a = 0` control
isolates is the correct thing: **the identical two-component convex structure, same strength, same
geometry, components mirror images instead of skewed — and it reads exactly zero** (6.7e-16 over
180 configurations). That is a null which reproduces the data's whole generative structure except
the one claimed ingredient, which is what reach 3 actually asks for. Restated on that basis.

The residual risk the second agent named — the `n`-sweep's interior peak — is discharged by the
composition identity instead: `n` steps of `K` is one step of `K^n`, measured to 3.3e-16, so the
peak over `n` is the single-step curve reparametrised and there is no separate mixing process to
confound it.

**And Kahle et al. are the cautionary precedent, not a scoop:** their peak came from mixing two
*phases*, which is this repository's own metastability artifact (`broken-phase-metastability-artifact`).

## 3.5 Smaller corrections, all folded into `PUMP_RESULTS.md`

- **Exponent 2 is a CALIBRATION, not a finding.** The share is a KL divergence from the pairwise
  exponential family, and a KL divergence is locally quadratic with the Fisher metric as its
  Hessian (Amari & Nagaoka 2000). P-EXP passing confirms the instrument and the geometry; **the
  coefficient is the only deliverable.** The prereg derived exponent 2 from evenness and
  smoothness, which is correct but understates how forced it was.
- **The exponent drift 2.0056 → 2.0720 is a fitting-window artifact, not physics** — the window
  runs to the top of the expansion band where the `a⁴` term contributes.
- **At `damp` the closed form gives 0.008929 nat against an exact 0.021185 — a factor 2.37 low**,
  at the extreme-asymmetry corner. Consistent with the 18 %-low trend at a = 0.2 continuing.
  `valve_upward_bound`'s 0.011962 captures 56 % of the share it bounds.
- **`damp` and the QPU both sit near the extreme-asymmetry corner, so the hardware comparison is
  extrapolation toward the boundary, not interpolation.** The QPU's in-band points reach
  a = 0.221 against a feasible max of 0.238 — 93 % of the way out. Declared, late, as §4.5 should
  have.
- **`share(repetition(k)) = 0` at k ≥ 4 is MEASURED (≤ 5e-14), not proved** —
  `share_eq_zero_of_signSymmetric` is `Bool × Bool × Bool` only. `PUMP_RESULTS.md` says "measured"
  throughout and is correct; `PUMP_PREREG.md` §2 says "hence share exactly zero at every k", which
  is **argued**. That row is an instrument check, not a plumb line.
- **IPF did NOT drift here.** It agreed with the dual to 1.0000 on every pumped state. The stored
  taint (`ipf-sharek-boundary-drift`) is about *near-deterministic* states; pumped states are not
  near-deterministic. Recorded as plainly as the taint would have been invoked.

---

# AMENDMENT 4 — the correction term is measured, and three catches from siblings are folded in

**Dated 2026-07-27, after AMENDMENT 3 (`98a040e`). Prompted by `planck-pilot` (a systematic
deviation in `a`) and `pump-curve` (a grid number and a structural mechanism). One is a
rediscovery of something already in this record, one is a real error of mine, and one makes a
finding of mine stronger than I could make it.**

## 4.1 The `a²` correction term, measured — `planck-pilot`'s deviation is real, already recorded, and now quantified

`planck-pilot` gated the law on synthetic sign-symmetric triples and reported measured/predicted
of 0.975, 1.030, 1.092, 1.130 at a = 0.05, 0.10, 0.15, 0.20 — a systematic positive deviation
growing as `a²`, fitted at `c = 3.4`.

**It is real, and it is the same object AMENDMENT 1 §5 tabulated and AMENDMENT 2 restated the kill
on.** Their reading — *"the law is not falsified, its validated domain is just narrower in a than
the formula's appearance suggests"* — is exactly right, and is why P-FORM is now staked on
`C = lim_{a→0} Δ/a²` rather than on the value.

**What was missing, and is now supplied: `c` is not a constant.** Measured exactly
(`pump_correction_c.json`), writing `exact = closed × (1 + c(r₀)·a² + …)`:

| r₀ | 0.81 | 0.64 | 0.49 | 0.36 | 0.25 | 0.16 | 0.09 | 0.04 |
|---|---|---|---|---|---|---|---|---|
| **c(r₀)** | **14.37** | 4.42 | 3.13 | **3.01** | 3.23 | 3.62 | 4.08 | 4.53 |

`c` has a **minimum of 3.01 near r₀ ≈ 0.36** and rises steeply toward high pair correlation —
**14.4 at r₀ = 0.81 and ≈ 95 at r₀ = 0.92**. So a single correction coefficient is safe only in
the basin and is badly wrong on a strongly pair-correlated substrate.

**And their measurement independently confirms mine.** Their 1.030 / 1.092 / 1.130 at
a = 0.10 / 0.15 / 0.20 against this campaign's exact values at r₀ = 0.36 — **1.0306 / 1.0705 /
1.1297** — agree to 0.3 % at a = 0.10 and a = 0.20 and 2 % at a = 0.15, and their fitted c = 3.4
sits against an exact 3.01–3.23 across their stated ρ range. A sampled sky-geometry pipeline
reproducing an exact eight-cell computation to sub-percent is a stronger result than either of us
set out to get, and it is reported as such rather than as a discrepancy.

## 4.2 A grid number was wrong — P-QPU-2 is six delays, not seven

`pump-curve` caught that `PUMP_RESULTS.md`'s verdict grid says "0.758 – 1.348 over 7 in-band
delays" while §5's table starts at 0.815. **They are right and the grid was wrong.** The seventh
point is t = 0, where `a = 5×10⁻⁴`, there is no pump, and both terms sit at the hardware's own
floor (measured 2.35e-4 against a predicted 3.10e-4) — `QPU_HABIT_RESULTS.md` calls that 0.00023
the instrument floor itself. Including it quotes a floor-over-floor ratio as if it were a test of
the law.

**Corrected everywhere to `0.815 – 1.348` over six delays**, with t = 0 excluded by the same depth
rule the rest of the campaign uses. The verdict is unchanged and the range is narrower.

## 4.3 The k ≥ 4 finding becomes structural, and the credit is `pump-curve`'s

`PUMP_RESULTS.md` §2 reported the k ≥ 4 symmetric-noise floor as a measurement with a stated
reason. `pump-curve` supplied the counting argument that makes it a **theorem-shaped fact**, and
verified it on the k = 4 output directly.

Under the global sign flip a sign-basis coefficient transforms as `χ_S → (−1)^{|S|} χ_S`, so sign
symmetry kills exactly the **odd** `|S|`. Pair-blindness means `|S| ≥ 3`. The surviving directions
are therefore the **even** subsets of size ≥ 3, and there are

| k | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|
| even pair-blind directions | **0** | 1 | 5 | 16 | 42 |

(counts confirmed here: `Σ_{|S| even, |S|≥4} C(k,|S|)`). **k = 3 is the only case where every
pair-blind direction is odd.** The vanishing at three slots is not a general fact with an
exception at four — it is an accident of three, and the floor grows with k because the number of
even survivors does. Verified on the k = 4 output: the only non-zero coefficients are the six
pairs at `κ² = 0.640000` and the single `|S| = 4` term at `κ⁴ = 0.409600`, every odd one
identically zero.

This is a better statement of the finding than the one in §2 and the argument is not mine.

## 4.4 Cap compliance: our stress test was weak

`planck-pilot` reports a maximum share of **0.663696 = 0.9575 × ln 2** over 4×10⁵ random three-bit
states drawn half from Dirichlet(1) and half from Dirichlet(0.05). This campaign's
cap-compliance gate reached only **0.6174 = 0.891 × ln 2** over 20 000 states. Both comply, but
theirs is the sharper stress case: **sparse ensembles approach the ceiling much more closely**, so
a future cap check should sample near the simplex corners rather than from a flat Dirichlet. Our
gate is not wrong, it is weak, and that is worth saying.

## 4.5 One question answered honestly in the negative

`water` asks whether there is a case where **lumpability holds for a threshold on an integer count
under a physically realised channel** — the exact shape of their coordination-number partition.
**There is not one here.** Arm F's lumpable control was *constructed by hand* — a channel built to
act on block labels — precisely so it would be lumpable, as a dye test for the instrument. It is
an existence proof that the instrument can see the a² law through a coarse-graining, and it is
**not** evidence that any physically realised channel is lumpable with respect to any natural
partition. Their declared prior that it fails for coordination number looks right for the reason
they give, and nothing in this campaign supports the optimistic direction.

---

# AMENDMENT 5 — there are TWO pump axes, the "fifth floor" was the second one, and my strength guidance was right on one axis and wrong on the other

**Dated 2026-07-27, after AMENDMENT 4 (`fbcb3ea`). `pump-curve`'s finding
(`PUMP_MIXTURE_AXIS.md`, `a2b05d2`), verified here independently before propagating, because it
changes downstream guidance I had already sent to three campaigns.**

## 5.1 Everything verified, independently

| claim | verified here |
|---|---|
| `mix(γ) = γδ₀₀₀ + (1−γ)δ₁₁₁` has share **exactly zero at every γ** | `+0.000e+00` at all seven weights — a clean axis |
| off γ = ½ a **unital** channel mints | yes, up to 7.2e-4 at δ = 0.08 |
| exponent in the detuning `δ = ½ − γ` | **1.9983 and 1.9934** — the same quadratic law |
| their closed form `Δ = 8δ²κ⁶(1−κ²)/[(1+2κ²)(1+3κ²)]` | ratio to exact **0.99997 at δ = 0.01**, degrading to 0.957 at δ = 0.10 as an O(δ⁴) truncation should |
| peak at s = 0.0999 | **closed form 0.0999, exact 0.1001** (κ = 0.800) |
| Schneidman **Fig. 3** is the hidden-bit figure with γ on the abscissa | quote verified verbatim; caption reads *"as a function of γ = P(σ₄ = 0)"* |

## 5.2 The "fifth floor" was not a fifth thing — verified to 1.1e-15

> **`shareK₄(repetition₄ through BSC(s))` = `share₃(mix(γ=s) through BSC(s))`**

across eleven strengths, worst difference **1.1e-15**: 7.152099e-03, 1.306685e-02, 1.410565e-02,
1.323255e-02, … identical to every digit. And the mechanism, checked rather than asserted:
conditioning the k = 4 state on slot 4 gives a **uniform** slot-4 marginal and a conditional on
slots 1–3 that **is** the γ = s mixture (`|difference| = 1.4e-17`, shares equal to all digits).

**So `PUMP_RESULTS.md` §8's "fifth floor nobody had budgeted for" is the state-asymmetry pump seen
at four slots, with the fourth slot playing the latent bit.** §2's character-counting says *which*
directions carry it; this says *what it is*. Recorded as a measured identity on this family, not a
general theorem.

## 5.3 "Strength is a savage brake" is AXIS-SPECIFIC, and I gave three campaigns the wrong axis

The two laws are mirror images:

| | channel axis (§1) | state axis (this amendment) |
|---|---|---|
| what is detuned | the **channel** (`a ≠ 0`) | the **state** (`γ ≠ ½`) |
| requires | channel asymmetry; a unital channel mints nothing | **nothing of the channel — a unital channel suffices** |
| requires of the input | sign-symmetric | **not** sign-symmetric |
| noise factor | `κ⁸` with **`(1−r₀)` in the DENOMINATOR** | `κ⁶` with **`(1−κ²)` in the NUMERATOR** |
| as noise → 0 | **diverges** — strength is a brake | **vanishes** — strength is the enabling ingredient |
| peak | monotone; no interior peak in s at fixed a | **interior peak at κ ≈ 0.80 (s ≈ 0.10)** |

The reason is physical and `pump-curve` states it correctly: **with no noise the two components
never overlap and nothing mixes.** The state axis needs noise to do its work; the channel axis is
suppressed by it.

**The consequence, and it is a correction to advice already sent.** I told the glass, water and
Planck campaigns that "strength is a savage brake" and that a floor falls off as `κ⁸`. **That is
true on the channel axis and false on the state axis** — and their substrates (galaxy/particle
triples, CMB pixel triples, water coordination labels) are **not** sign-symmetric, so **the state
axis is the one that governs them**. A floor estimated from `κ⁸` suppression on a
non-sign-symmetric substrate is estimated from the wrong axis, and estimated **low**, because the
state axis *peaks* at intermediate noise instead of decaying.

Corrected in `PUMP_RESULTS.md` §8, which now carries **four** floors with an explicit axis column,
and sent to all three campaigns.

## 5.4 The Kahle claim is tempered

AMENDMENT 3 §3.3 and the RESULTS headline said the closed form "answers the question Kahle et al.
called unsolved". **Too strong, and `pump-curve` is right to push back.** It is a *worked special
case*: one two-parameter family of product-state pairs, k = 3, small detuning. And Schneidman had
already computed the two-component hidden-bit case **numerically** in 2003 (Fig. 3), six years
before Kahle et al. called the general problem unsolved. Restated as: *a closed form for one
family of convex combinations of two product states*, which is what it is.

## 5.5 The Fig. 2 grid number

`pump-curve`'s 26-point grid gave 0.0761 at q = 0.12; the finer grid used here gives **0.0774 at
q = 0.10**, matching the value independently recorded in `eca-spike-is-convergent-art` from the ECA
adjudication. **0.0774 is the number**; theirs was a grid-resolution artifact and they have said so.

---

# AMENDMENT 6 — the closing pass: how to apply the correction, one coincidence killed, and reach 3's real home

**Dated 2026-07-27. Three siblings' refinements, each verified here before adoption.**

## 6.1 `r₀` WALKS during a Z-channel sweep — how to apply `c(r₀)` correctly

`planck-pilot` found that with `p10 = 0` (a Z-channel, which is what `damp` and every physical
relaxation ray are) the strength is tied to the asymmetry, `s = a/2`, so
**`r₀ = (1−a)²ρ` moves as `a` is swept.** Verified, reproducing their numbers to the digit at
ρ = 0.65:

| a | 0.02 | 0.05 | 0.10 | 0.15 | 0.20 |
|---|---|---|---|---|---|
| r₀ | 0.624 | 0.587 | 0.527 | 0.470 | 0.416 |
| c(r₀) | 4.28 | 3.96 | **3.44** | 3.11 | **3.06** |

**So a single template walks across the `c` curve, and holding `c` fixed across an a-sweep mixes
the basin with its walls.** The rule: **interpolate `c` at each row's own `r₀`.**

**This also dissolves the one apparent tension between their gate and my table.** At ρ = 0.6467,
a = 0.20 they measured +13.3 % where a fixed `c = 4.42` (read off r₀ = 0.64) predicts +17.7 %. But
that row's actual r₀ is **0.416**, where `c ≈ 3.06`, predicting **+12.4 %** against their +13.3 %.
They withdrew the tension before I could check it; the check agrees.

**My own arm A is unaffected** — it sweeps `a` at **fixed s**, so `r₀ = (1−2s)²ρ` does not move.
Recorded because the two sweep geometries are easy to confuse and only one of them holds `r₀`
still.

## 6.2 The `B_k` subtraction is principled, and the identity travels where the formula does not

`pump-curve` observes that §3's k-scaling subtracts `B_k` before fitting, and `B_k` **is** the
state-axis pump — so the excess `D_k` really is the channel-axis object and the two mechanisms are
already cleanly separated. **That makes the subtraction principled rather than convenient**, and
§3 should say so.

Their caveat, verified: the identity `B_4 = share₃(mix(γ=s))` is **exact at every s** (1.1e-15),
but the **small-δ closed form does not predict it there**, because `δ = ½ − s` is far outside the
expansion:

| s | 0.02 | 0.05 | 0.10 | 0.20 | 0.30 | 0.40 |
|---|---|---|---|---|---|---|
| δ = ½−s | 0.48 | 0.45 | 0.40 | 0.30 | 0.20 | 0.10 |
| formula / exact | 1.478 | 1.393 | 1.371 | 1.322 | 1.212 | 1.071 |

**The identity travels; the formula does not.** It converges toward 1 only as δ → 0, exactly as an
O(δ⁴) truncation should.

## 6.3 A coincidence, killed and recorded so nobody chases it twice

Schneidman's AND-panel peak sits at **q\* = 0.09988** and the state-axis closed form peaks at
**s\* = 0.09988** — indistinguishable to 1e-6, and it looks like an exact correspondence between
the 2003 figure and the second axis. **`pump-curve` checked it and it is false:** the ratio
`share(AND,q)/g((1−2q)²)` runs **3.78 → 97.6** across q ∈ [0.02, 0.40], a 25× spread. Two
different functions that happen to peak at the same place. Recorded as a negative result, because
a numerical coincidence at six figures is exactly the kind of thing this programme would otherwise
spend a day on.

**And the Fig. 2 peak is settled at `0.077401 bits at q\* = 0.099879`** (Brent on the curve).
`pump-curve`'s earlier 0.0761 was a prose error from a stride-2 printout that skipped the q = 0.10
node — their committed JSON had 0.0774 correctly all along, and they corrected it in place rather
than silently, against a published figure.

## 6.4 GATES.md reach 3 — the objection is withdrawn for simulation and has teeth on hardware

`pump-curve` withdraws the n-sweep mixture-null objection, with the right reason: reach 3 guards
against **an estimate pooled over heterogeneous regimes**, which needs (a) estimation from samples
and (b) an unmodelled second population. The simulation arms have neither — the distributions are
exact and fully specified, and the composition identity means the n-sweep is not an independent
experiment but the single-step curve reparametrised.

**But they name the one place it does apply, and they are right.** The QPU's 12-point curve **is**
estimated from counts pooled across a 100-second job, so *"pooled over two calibration regimes"* is
a live reach-3 instance on the hardware arm. It is already bounded — calibration drift **0.0009**
against a 0.02 ceiling — but that number was reported as a *validity check* and never framed as
reach 3. **Reframed here at no cost: same number, correct label.** That is the only reach-3
instance in this campaign that is not already the `a = 0` control.

## 6.5 Two formulations adopted from `water`

**On the trade, and this is the cleanest statement of it anyone has produced:** *escaping the
zero-theorem also forfeits the protection-theorem.* A campaign that argues its way out of sign
symmetry in order to have a nonzero reading has, by the same step, given up
`valve_needs_asymmetry`'s protection — **at k = 3 as much as at k ≥ 4**. The two hypotheses are
one trade, not two hazards.

**On sizing, worth carrying wherever the floor law is quoted:** detection and precision are
different budgets. Sizing on `floor_p99 ≤ S/3` buys **detection**; the reading's own relative
standard deviation is `sqrt(2 + 8·N·share)/(2·N·share)`, so **a 10 % sd costs roughly 19× the
tuples a 5σ detection does.** Anyone quoting a *ratio* rather than a detection needs the second
budget.

---

# AMENDMENT 7 — the state-axis law gets its validity limits, and a gate reach this campaign supplies five instances for

**Dated 2026-07-27. `glass` verified the state-axis law independently and found two limits I had
stated unconditionally. Both verified here; both reproduce their numbers exactly.**

## 7.1 Independent verification, and the two limits I owed

`glass` reproduced the state-axis law on their own instrument to **0.1–2 %**, with the peak at
**s = 0.100 (κ = 0.800)** exactly as stated, and `share/d²` flat at 0.1134 → 0.1125 across
d = 0.01…0.10. **I propagated that law to three campaigns as though it were unconditional. It is
a leading quadratic and needs the same caveat the channel-axis law carries.**

**Limit 1 — it over-predicts at large detuning, worst at strong noise.** At d = 0.30, verified:

| s | 0.05 | 0.10 | 0.20 | 0.30 | 0.40 | 0.49 |
|---|---|---|---|---|---|---|
| measured / law | 0.955 | 0.896 | 0.756 | 0.595 | 0.461 | **0.410** |

i.e. the law is **up to 2.44× optimistic** at the far corner — glass's 0.41 and "2.4×" exactly.

**Limit 2 — the quadratic is exact only as d → 0.** `share/d²` at s = 0.10:

| d | 0.005 | 0.05 | 0.10 | 0.15 | **0.20** | 0.30 |
|---|---|---|---|---|---|---|
| drift | 0.00 % | −0.20 % | −0.82 % | −1.95 % | **−3.71 %** | −10.36 % |

glass's "3.7 % low by d = 0.20" reproduces to the digit.

**Neither threatens the physics; both bind anyone using the law to PREDICT a floor rather than to
know its shape** — the same distinction AMENDMENT 2 drew for the channel axis, and I failed to
carry it across when I sent the second law out.

## 7.2 The trap glass named, which is better than my warning

The state axis **vanishes as noise → 0** and **peaks at s ≈ 0.10**. So:

> **"our channel is symmetric" and "our noise is weak" are BOTH inadequate arguments unless you
> know where on that curve you sit — because someone reducing noise from s = 0.30 toward 0.10 to
> be careful walks UP the curve.**

That is a sharper and more useful statement of the hazard than anything I sent, and it is the one
to quote. Its constructive half is a **design lever, not just a hazard**: the floor scales as the
*square* of the order parameter's asymmetry about its binarization threshold, so **bin at the
median to make d small by construction, then MEASURE the residual d** rather than assume it zero.

## 7.3 The proposed reach — this campaign supplies five instances, and they are all mine

`glass` proposes a named GATES.md reach for **a claim whose substance survives while its warrant
does not** — a right answer held for a wrong reason — observing that nothing in the battery looks
for it, and that the substance surviving is exactly what stops anyone from checking. They count
their own two and water's one.

**This campaign supplies five more, and every one is mine:**

| claim | substance | warrant |
|---|---|---|
| **P-FORM passed** | coefficient confirmed to 3e-4 — true | the kill *as written* fired on 13 rows of 13 |
| **the mixture null is discharged** | the `a=0` control is a good control — true | "theorem-pinned" was the wrong argument for reach 3; a null that *provably* reads zero cannot manufacture |
| **no such curve has been published** | the asymmetry-resolved law is genuinely new — true | the negative existence claim was **false**; Schneidman 2003 Fig. 2 |
| **the closed form answers Kahle's open question** | the closed form is real — true | it is one family at k=3 and small detuning, and Schneidman had done the numerics in 2003 |
| **strength is a savage brake** | true on the channel axis | **false on the axis that governs every substrate I sent it to** |

Five claims, five surviving substances, five failed warrants — **and not one of them was caught by
this campaign's own eight-gate battery**, which passed everything at 1e-15. Every one was caught
by a sibling reading a primary artifact instead of my summary of it.

**That is strong support for the reach, and it locates it precisely: the failure is invisible to
numerical gates by construction, because the number is right.** The only instrument that catches
it is a second reader going to the source. Endorsed, with this campaign's five offered as the
kept taint, and with the observation that the reach's dye test cannot be numerical.

---

# AMENDMENT 8 — the lead I sent was malformed, and the sixth instance arrived after I endorsed the reach

**Dated 2026-07-27. `glass` answered the "does your substrate reach the steep `c` wall" lead with
a measurement, and found that the reasoning which routed it to them contains a conflation. The
conflation was mine, and the deeper version of it makes the question itself malformed.**

## 8.1 The conflation, which was mine

I wrote to `glass` that their r = 1.30 template *"has particles sitting in several enumerated
triples, which is the regime where pair correlations run high."* **Two different objects:**

- **triple overlap** — a particle appearing in several enumerated triples — is a property of the **sampling**;
- **`r₀`** is a property of the **label distribution**.

Their data separates them and in the inconvenient direction: **r = 1.50 has the campaign's
heaviest overlap (18.1×) and `r₀ = −0.065`**, essentially uncorrelated; **r = 1.30 has less than
half that overlap (7.5×) and the highest `r₀` (+0.638)**. Heavy overlap does not imply high pair
correlation, and a hunt for a high-`r₀` substrate steered by overlap is steered wrong — which
matters because overlap is the more visible property.

**Note what my reasoning did: it named the right template for a wrong reason.** r = 1.30 *is*
their highest `r₀`. That is the sixth instance of the substance-survives/warrant-fails pattern
this campaign supplied five of in AMENDMENT 7 — and it was produced **after** I endorsed the gate
reach for it, in the message endorsing it. The pattern is not a historical list; it is live.

## 8.2 The deeper version: the question was malformed, and the wall may be unreachable on a segregating substrate

`glass` names the real driver of their `r₀`: not overlap but **chemical segregation** — the
r = 1.30 template is dominated by `AAA` (0.681) and `BBB` (0.130). **But that mechanism raises the
magnetisation at the same time as the pair moment**, and my `r₀` is defined on a **sign-symmetric**
input, where `⟨z⟩ = 0`. The mapping from their Pearson slot-correlation to my raw pair moment is

> **`⟨z_i z_j⟩ = ρ_Pearson·(1 − m²) + m²`**

so at ρ_P = 0.638 the raw moment reaches 0.81 only once **m ≳ 0.7** — and a state with m ≈ 0.7 is
*strongly* non-sign-symmetric, which means **the channel-axis law and the whole `c(r₀)` apparatus
do not apply to it at all.** It is on the state axis, parametrised by detuning, not by `r₀`.

**So "find a physical substrate with high `r₀` to test `c(r₀)`" is self-defeating when the route to
high `r₀` is species imbalance**: the imbalance that raises the pair moment is exactly what moves
the substrate off the axis the correction belongs to.

**The corrected lead, which is better than the one I sent.** To reach the wall on a physical
substrate you need high pair correlation with **balanced** species — `AAA` and `BBB` at comparable
weight, giving `m ≈ 0` and `r₀` large. That is a **50:50 mixture that phase-separates**, not an
80:20 one. Kob–Andersen at 80:20 is imbalanced by construction and cannot get there;
`glass` reached +0.638 and correctly reports it as short of the anchor.

## 8.3 What `glass` does supply, and it is cleaner than the wall

Their temperature ladder gives **`r₀` = 0.447 → 0.508 → 0.568 → 0.638 at fixed substrate** — same
model, box, composition and instrument, with only temperature varying. That scans the correction
over a factor of 1.4 in `r₀` with everything else held. A weaker test of `c(r₀)` than the wall
would be, and a **cleaner** one, since nothing else moves between the points. Offered here as the
better-conditioned option for whoever picks the correction up, with the caveat from §8.2 that the
magnetisation must be measured before those points are read as channel-axis `r₀` at all.

---

# AMENDMENT 9 — I ran the citation-class audit on myself and it fired

**Dated 2026-07-27. `water` suggested running `glass`'s rule — when a correction lands on a
citation, re-audit every citation of that object in every document, not just the one pointed at —
over my own files, noting that this campaign cites `valve_needs_asymmetry`, `valve_upward` and the
caps across a prereg, results and eight amendments. It cost one command. It fired.**

## 9.1 What the audit found

Twenty-seven theorem citations across four documents and the instrument. Three are wrong, all the
same way, all in **one table** — `PUMP_PREREG.md` §5.2's plumb lines:

| row, as written | the theorem's actual signature |
|---|---|
| "**any product state** — exactly 0 — `share_prod3`" | `{p₁ p₂ p₃ : Bool → ℝ}` — **three binary slots** |
| "**any sign-symmetric state** — exactly 0 — `share_eq_zero_of_signSymmetric`" | `{p : Bool × Bool × Bool → ℝ}` — **three binary slots** |
| "**every reading, any state** — ≤ ln 2 — `share_le_log_two`" | `{p : Bool × Bool × Bool → ℝ}` — **three binary slots** |

**And this campaign then ran arms at k = 4, 5, 6 and 7** against a plumb-line table that, as
written, licensed applying all three there. Corrected in place with the signatures quoted, and the
amendment note left in the table rather than the edit made silently.

## 9.2 What it did and did not cost

**No number moves.** Every k ≥ 4 reading in `PUMP_RESULTS.md` was reported as **measured** — the
inputs at ≤ 5e-14, the baselines with their brackets — and AMENDMENT 6 §3.5 had already demoted
the k ≥ 4 zero from plumb line to instrument check on exactly this ground. So the substance was
right throughout and the campaign's conclusions are untouched.

**The table was still wrong**, and it is the document a later reader would trust *instead of*
re-deriving. That is the whole shape of the reach `glass` proposed: substance survives, warrant
fails, and nothing numerical can see it because the number is right.

## 9.3 The count, and what it says about the rule

That makes **eight** instances from this campaign, and this one is the most instructive, because
of when it was found:

- I wrote the "sweep for the class, not the instance" rule to project memory;
- I wrote that the failure is *"invisible to numerical gates by construction"*;
- I endorsed a gate reach for it and supplied five instances;
- **and I had not run the one-command grep over my own documents until `water` suggested it.**

The rule is cheap, mechanical, and I did not apply it to myself while writing it down. Three
campaigns have now hit the same thing on the same day: `glass` found a second citation error by
auditing the class, `water` found a third (`valve_from_nothing` pinned to asymptotically
independent labels, which are not a product state), and this is the fourth.

**The operational form, which is what should survive this exchange:** when a correction lands on a
citation, `grep` every citation of that object across every document you own, and check each
against the theorem's actual signature rather than your memory of it. It costs one command. It has
now fired on three of the four agents who ran it, including the one who wrote the rule down.

---

# AMENDMENT 10 — the two axes INTERFERE, and on a non-sign-symmetric substrate the minting has an exact interior NULL

**Dated 2026-07-27. Prompted by `glass` correcting their own r₀ with my mapping formula. Their
arithmetic is right and their number is better than the one they first quoted — and checking
whether the LAW accepts it turned up something neither of us had: the two axes are not
independent, they interfere, and the interference has an exact zero.**

## 10.1 glass's correction is right, and the law still does not accept it

`⟨z_i z_j⟩ = ρ_P(1−m²) + m²` reproduces their raw pair moment to 0.0e+00, giving **0.749** at
r = 1.30, T = 0.44 rather than the 0.638 they first reported. Nearer my 0.81 anchor than either of
us thought.

**But the translation of the statistic does not make the state usable in the law**, because the
law has *two* hypotheses and I gave them a one-parameter translation: `r₀` is the pair moment **of
a sign-symmetric input**, where m = 0 and ρ_P and ⟨z_iz_j⟩ coincide. Their m is 0.553.

**Measured rather than argued.** Constructing a permutation-symmetric state with exactly their
(m = 0.553, r = 0.749), on the pair-maxent manifold so its share is 0 to 1.1e-16, and pushing it
through the channel:

| a | s | measured | closed form at r₀ = 0.749 | ratio |
|---|---|---|---|---|
| 0.010 | 0.05 | 1.11e-03 | 9.92e-05 | **11.2** |
| 0.020 | 0.05 | 6.58e-04 | 3.97e-04 | 1.66 |
| 0.050 | 0.05 | **2.53e-07** | 2.48e-03 | **0.0001** |
| 0.010 | 0.10 | 2.30e-03 | 3.82e-05 | **60.2** |

Not the right order of magnitude, and **not even monotone in `a`.** The law is not merely
inaccurate there; it has the wrong shape.

## 10.2 The reason: an exact interior NULL

On a non-sign-symmetric input the minting **starts nonzero at a = 0** (the state axis), **falls as
channel asymmetry rises**, hits an **exact zero**, and rises again:

| a | 0.000 | 0.010 | 0.025 | 0.040 | **0.050** | 0.060 | 0.065 |
|---|---|---|---|---|---|---|---|
| share (m=0.553, s=0.05) | 1.65e-3 | 1.11e-3 | 4.71e-4 | 8.61e-5 | **2.5e-7** | 7.6e-5 | 1.8e-4 |

The zero is machine-exact, not merely small — located to 1e-10 it reads **−1.1e-16 / 0.0e+00**
across every configuration tested. **The channel's asymmetry cancels the state's own.**

**Where it sits, measured across state asymmetry and noise strength:**

| m | s | share at a=0 | **a_null** | `2ms = m(1−κ)` |
|---|---|---|---|---|
| 0.200 | 0.05 | 2.78e-4 | 0.01704 | 0.0200 |
| 0.400 | 0.05 | 1.02e-3 | 0.03508 | 0.0400 |
| 0.553 | 0.05 | 1.66e-3 | 0.05050 | 0.0553 |
| 0.700 | 0.05 | 1.84e-3 | 0.06822 | 0.0700 |
| 0.553 | 0.10 | 2.72e-3 | 0.10572 | 0.1106 |
| 0.700 | 0.10 | 2.71e-3 | 0.14085 | 0.1400 |

> **The null sits near the MAGNETISATION-PRESERVING channel, `a_null ≈ 2ms = m(1−κ)`** — the
> asymmetry for which `m_out = κm + a` returns the state's own magnetisation. Accurate to ~15 % at
> small m and to ~1 % by m = 0.7. Approximate, not exact; the exact condition is the output
> landing back on the pair-maxent manifold, which is transcendental.

## 10.3 What this does to the downstream guidance — a third correction to the same advice

Every substrate I have sent guidance to — sky, glass, water, and the CMB data branch — is
non-sign-symmetric. For all of them:

1. **The floor is nonzero at zero channel asymmetry.** Already said (state axis).
2. **The floor is NOT MONOTONE in channel asymmetry.** New, and it invalidates both directions of
   the obvious argument: *"our channel is nearly symmetric so the floor is small"* is wrong, and so
   is *"we increased the asymmetry so the floor grew"*. Between a = 0 and `a_null` the floor
   **falls** as asymmetry **rises**.
3. **There is an exact null, and it is a DESIGN LEVER.** This generalises `glass`'s "bin at the
   median so d is small": instead of only *reducing* the state's asymmetry, you can **cancel** it
   with a matched channel asymmetry at `a ≈ 2ms`. Tuning to the null kills the minting exactly, not
   approximately.

**That is the third time this campaign's downstream advice has needed correcting in the same
place**, and each correction has been in the direction of *less* monotone, *less* one-parameter,
and *more* dependent on a property of the substrate the guidance did not ask about. The honest
summary for a downstream reader is now: **measure your m, measure your a, and expect neither knob
to be monotone alone.**

## 10.4 And glass's own framing of the self-defeat is sharper than mine

They note that on their ladder cooling *raises* ρ_P (0.447 → 0.638) and *lowers* m (0.655 →
0.553), so the raw moment is a compromise that never exceeds 0.75, and reaching 0.81 from
ρ_P = 0.638 would need m ≥ 0.689 — which the ladder has, but only where ρ_P has already fallen to
0.447. **On a real glass former the two knobs are anticorrelated along the only control parameter
available.** That is a stronger statement than my "imbalance moves you off the axis": it is not
just that the route is self-defeating in principle, it is that the substrate's own physics enforces
the trade.

## 10.5 The state-axis floor is exactly quadratic in the magnetisation — and that gives a usability threshold

`planck-pilot` asked whether their branch is reachable at all: their binarization splits at the
median of the **pooled** values of three slots, which pins the pooled magnetisation near zero and
leaves each slot's own `m` free but small. Measured (r = 0.75, s = 0.05):

| m | 1e-4 | 1e-3 | 1e-2 | 3e-2 | 0.1 | 0.4 | 0.7 |
|---|---|---|---|---|---|---|---|
| floor (nat) | 7.12e-11 | 7.12e-9 | 7.12e-7 | 6.41e-6 | 7.08e-5 | 1.02e-3 | 1.84e-3 |
| floor / m² | 0.00712 | 0.00712 | 0.00712 | 0.00712 | 0.00708 | 0.00636 | 0.00375 |

> **`floor ≈ 0.00712·m²` for m ≲ 0.05**, exact to five significant figures over four decades,
> saturating above m ≈ 0.1. The `m²` scaling is universal; the prefactor depends on r and s.

**The usability threshold that follows**, and it is the number a downstream campaign actually
needs: the state-axis floor matters only when it clears the campaign's own estimator floor
`0.227/N`. At N = 4e6 that is 5.7e-8 nat, so

> **below `m ≈ 2.8e-3` the state-axis floor is beneath the shot-noise floor and cannot matter;
> above it, the floor climbs as `m²` — a factor of 10 in m is a factor of 100 in the floor.**

So *whether* a substrate is off the symmetric point (the sign-symmetry p-value) and *whether that
matters* (`m` against the threshold) are different questions, and only the second decides anything.
Both belong in the table.
