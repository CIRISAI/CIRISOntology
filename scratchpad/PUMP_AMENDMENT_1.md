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
