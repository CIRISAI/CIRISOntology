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

**This does not move P-FORM's verdict, and the reason is stated so it cannot look like a rescue.**
P-FORM stakes the **coefficient** `C = lim_{a→0} Δ/a²`, which is measured at the smallest a in
each row and is confirmed to 3e-4. The band correction affects only how far out the formula may
be quoted as a value. Both are reported: **the coefficient to 3e-4, the value to 2 % out to
a ≈ 0.07 and to 20 % out to a ≈ 0.2**, with the exact solver quoted beyond.

---

## What was NOT amended

No staked band was widened. No kill was withdrawn. P-K's stake (K-COUNT) was left exactly as
written and is **refuted by the measurement** — see `PUMP_RESULTS.md`, where it is reported as
loudly as the passes.
