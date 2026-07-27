# AMENDMENT 5 — the target quantity becomes the excess over a POISSON-RESAMPLED surrogate

Committed **before the control is built and before the data is re-scored.** The frozen
prediction (`sky_stage5_frozen_prediction.json`, `b06a3fe`) **does not move.**

## A5.1 The re-specification

> **TARGET := `I_C⁽³⁾`(field) − `I_C⁽³⁾`(Poisson-resampled surrogate)**, where the surrogate is
> the phase-randomised field **then Poisson-sampled at the field's own `n̄(z)` through the
> identical selection**, so the null carries the shot-noise **power** *and* the shot-noise
> **non-Gaussianity**.
>
> **VALVE FLOOR := `I`(Poisson-resampled surrogate) − `I`(plain phase-randomised surrogate)**,
> reported per row. It is a measurement, not a model.

This is the amendment A3.4 demanded before any Stage 6 reading could be normalised. It
supersedes nothing else: outcome (a)'s criterion applies **as originally written** — ≥5 σ above
the combined floor, folded primary, two or more `b` passing G9, consistent with the frozen
prediction — and outcome (c) likewise.

## A5.2 Why the plain surrogate was insufficient

Phase randomisation preserves `|F(k)|`, so the plain surrogate carries the shot-noise *power*.
But it is Gaussian, so it carries none of the shot-noise *non-Gaussianity*. `Core/Valve.lean`
proves a per-cell **stochastic** channel acting on a **pair-structured** state can mint
whole-only share, and this campaign measured that minting at **130 % of the mock signal** at
DESI-like density. BOSS sits at `n̄V_R = 4.81` (`R = 10`) and `16.2` (`R = 15`) — the same
regime. So the Stage 6 reading was (gravity) + (valve), unseparated.

## A5.3 Construction, and the one distortion it cannot avoid

The clustering modulation is a **Gaussian** field, generated pre-smoothed, and Poisson sampling
supplies the rest of the variance. A Gaussian modulation must be clipped at `1 + δ ≥ 0`, and
clipping manufactures skewness — measured at **+0.69 with 28 % of cells clipped** when a
Gaussian modulation was pushed to carry the *whole* variance.

The lognormal escape is closed: it does not commute with smoothing (that is what disqualified
the Stage 3 control at skewness +1.6688), and it would add non-Gaussianity the null is not
supposed to have.

**So the clipped fraction and the null's own smoothed skewness are reported with every row.**
If the Poisson-resampled null's skewness is not dominated by the Poisson term — i.e. if
clipping contributes comparably — the valve floor is an **upper bound** on the true valve
contribution rather than a measurement of it, and the verdict must be stated that way.

## A5.4 Outcomes

Unchanged and binding. **(a)** ≥5 σ above the combined floor, folded primary, consistent with
the frozen prediction; **(c)** consistent with zero after all floors, reported as an honest
bound; **VOID** on the pre-registered conditions. Outcome **(b) remains withdrawn**
(Amendment 4). `NGC / R=15 / b=4 / squeezed` remains excluded. The shape-dependent deficit
remains reported-not-claimed.

**If the valve floor eats the signal, that is outcome (c), and it is reported at exactly the
volume outcome (a) would have been.**

---

*Amendment ends. The control has not been built.*
