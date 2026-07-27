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
