# Pre-registration — building the preferred-frame dark sector the extensive branch owes

Frozen 2026-07-24, before any numerical result was computed. Rebuilt claims
touch `dark-balance-extensive` and `dm-foliation` only. `Stance.lean` is NOT
modified by this work.

## What is owed

`dark-balance-extensive` (wager) needs a dark energy that is simultaneously:

* **(A)** exactly smooth — never clumps, at any measurable scale;
* **(B)** evolving in equation of state w(z);
* **(C)** crossing w = −1 at z_c = 0.59 ± 0.03 (its frozen kill window);
* **(D)** ghost-free, gradient-stable, and not transmitting information faster
  than light.

The stance records the obstruction: for any ordinary local fluid, (A)+(B)
together force superluminal sound speed. It names the only escape — "one
universe-wide quantity pinned to a single special slicing of time, a
'preferred-frame' dark sector" — and states "we have not built it."

`dm-foliation` (wager) supplies the slicing: the dark-matter / CMB rest frame.
Its promote field demands the smoothness be "a derived consequence, not an
imposed one."

## Hypotheses, and what each possible answer means

**H1 — the escape hatch is already built by others.**
If a published theory delivers (A)+(D) with a preferred foliation, then the
"we have not built it" clause is false in the same way `tsvf-third` was false:
work called future that was already published. Consequence: the clause dies,
and the owed work shrinks from "invent a mechanism" to "import and test one."

**H2 — the imported mechanism also delivers (C).**
If yes: `dark-balance-extensive` pays a large part of its promote price and the
duel with the intensive branch becomes purely observational.
If no: a *new* obstruction is found, internal to the escape hatch, and the
extensive branch is worse off than the stance currently says — it would owe
not just a mechanism but a mechanism that provably cannot be the obvious one.

**H3 — z_c = 0.59 is derivable from the coordination reading.**
The extensive total is N(t)·s(t): number of coordinating units times the
per-unit balance. Since ρ̇ = −3H(1+w)ρ, the crest (ρ̇ = 0) and the phantom
crossing (w = −1) are the *same event*. So z_c is fixed by
d/dt[N·s] = 0 — a competition between halo formation and per-unit decay,
both computable from standard ΛCDM.
If the crest lands in the frozen window without tuning: this is the single
strongest result available to the extensive branch, converting a branded
retrodiction into a derivation.
If it lands elsewhere, or moves freely with an undetermined input: the frozen
window is not a prediction of the frame, and the stance must say so.

## Method, fixed in advance

1. **Symbolic.** k-essence background for P = ε·μ²√(2X) − V(φ): compute ρ, p,
   w+1, and the perturbation kinetic operator P_X + 2X·P_XX. Determine whether
   the sign of w+1 can change.
2. **Numerical.** Planck-2018 ΛCDM (Ωm=0.315, Ωb=0.0493, h=0.674, n_s=0.965,
   σ8=0.811). Eisenstein–Hu 1998 transfer function. Sheth–Tormen mass function
   for N(z) = n(>M_min, z). Per-unit balance from the repo's own
   equicorrelation formula (`Core/Intensive.lean`): in the large-k limit the
   coordination density is n(z)·[−ln(1−ρ_corr(z))].
3. **Correlation assignment.** ρ_corr(z) = ξ_R(d,z)/σ²(R,z), the correlation
   coefficient between two units at their mean separation d = n^(−1/3), for the
   density field smoothed on the unit scale R. **Declared in advance as a
   choice, not a derivation** — the framework does not fix it.
4. **Crest.** Stationary point of n·s in z. Scan M_min over 1e10–1e14 M⊙/h.

## The pre-committed reading of the partition scan

This is the load-bearing pre-commitment, because it is the one that can
embarrass us. `provenance_line` (proved, `Core/Provenance.lean`) says the
partition — which degrees of freedom count as one unit — is not a function of
the correlation matrix. It is declared, not discovered, and the file already
calls it "the single largest source of silent error."

Therefore, *before looking*:

* If |dz_c / dlog₁₀ M_min| is **small** (≲ 0.1 per decade), the crest is robust
  to the partition and z_c is a genuine prediction of the frame.
* If it is **large** (≳ 0.3 per decade), then hitting a ±0.03 window requires
  declaring M_min to a precision the instrument provably cannot supply, and the
  frozen window is **not a prediction of the frame** — it is a prediction of the
  frame *plus an undetermined upstream choice*. In that case the honest move is
  to say so in the stance's confidence band, not to quote the hit.

We commit to reporting the sensitivity number whichever way it comes out, and
to reporting how wide a range of M_min lands inside the frozen window.

## Kills staked in advance

* The **H1 clause-death** fires if a published theory meets (A)+(D) with a
  preferred foliation. Named candidate: the cuscuton (Afshordi, Chung &
  Geshnizjani 2007) and its khronometric/Hořava relatives.
* The **H2 obstruction** fires if the sign of w+1 is structurally fixed for a
  single cuscuton, i.e. if crossing requires added machinery.
* The **H3 partition exposure** fires per the pre-committed reading above.

## What this work may not do

It may not modify `Stance.lean`. Any status or confidence-band change is
drafted here for review and applied, if at all, by a separate deliberate act.
A construction that works is not a measurement, and nothing here can promote a
wager above wager.
