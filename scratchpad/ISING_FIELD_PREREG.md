# PREREG — mapping the pairwise-blind order-3 share over the (T, h) plane of the 2D Ising model

Pre-registered **before any run**. Scratchpad only: this touches no Lean file, not `Stance.lean`,
not the audit. Committed before `ising_field.py` exists.

**Scope, stated first so it cannot be lost later.** This is a **model system**. The 2D Ising model
is not nature, a lattice of spins is not a brain or a language model, and nothing measured here
bears on the `wild-share` open claim or on any claim about the world. The most this experiment can
establish is a fact about a canonical statistical-mechanical model. It will be reported that way.

---

## 1. Why this experiment exists

`scratchpad/temporal-share/SPIKE_SURVEY.md` (commit `1ffb17a`) surveyed thirteen published
"higher-order spike" claims and found that **none** measures a pairwise-blind quantity. Three of
them (Marinazzo et al. 2019; Barnett et al. 2013; Khajehabdollahi et al. 2020) locate a
higher-order peak in an Ising-type model, and all three are disposed of at once by a lemma derived
in that survey and since machine-checked as
`CIRISOntology/Core/SignSymmetry.lean : share_eq_zero_of_signSymmetric`:

> A three-bit state invariant under the global sign flip, `p(s) = p(−s)`, has whole-only share
> **exactly zero** — no hypothesis on the pair correlations, no temperature, no coupling strength.

A zero-field Ising model is sign-symmetric at every temperature, criticality included. So the whole
"higher-order structure peaks at T_c" literature concerns, for our functional, a quantity that is
identically zero throughout the region it scans.

The Lean file states the design principle in the other direction, and this experiment is that
sentence turned into a measurement:

> **order-3 whole-only structure requires broken global sign symmetry. If a spin system is to carry
> any, the field must be nonzero.**

Turning on a field is the obvious next move, and the survey found no evidence anyone has made it.
`I_C^(3)` has never been published as a function of a swept control parameter in any field.

## 2. The quantity

The connected information of order 3 (Schneidman, Still, Berry & Bialek, PRL **91**, 238701 (2003)),
which `Core/Third.lean` and `Core/ShareK.lean` call the whole-only share:

> `I_C^(3)(X₁,X₂,X₃) = S[P̃⁽²⁾] − S[P̃⁽³⁾] = max{ S(q) : q carries all three pair marginals of p } − S(p)`

It is **pairwise-blind by construction**: it is exactly the entropy gap the pair marginals cannot
close, and it is zero on any distribution that *is* its own pairwise maxent projection. Units:
nats. Machine-checked cap for three binary slots: `ln 2` (`Core/ShareK.lean`, saturated by the
three-coin parity state).

**Alongside it, on the same distributions, the ordinary measures** — reported so the survey's
thesis can be checked inside one model rather than across a literature:

- multi-information / total correlation `TC = Σᵢ H(Xᵢ) − H(X₁X₂X₃)` (the repo's `S_total`);
- O-information `Ω = H(X₁X₂X₃) + Σᵢ H(Xᵢ) − Σᵢ H(X_{jk})` for n = 3;
- and `I_C^(2) = TC − I_C^(3)`, which is where all of `TC` lives whenever `I_C^(3) = 0`.

## 3. The model

Standard 2D Ising on a periodic square lattice, `s ∈ {−1,+1}`:

> `E(s) = −J Σ_⟨ij⟩ sᵢsⱼ − h Σᵢ sᵢ`, `J = 1`, `T` in units of `J/k_B`, `T_c = 2/ln(1+√2) = 2.269185…`

Sampling in a field: **Metropolis single-spin flip with checkerboard updates.** Wolff and
Swendsen–Wang cluster algorithms do not apply in a field (the cluster construction assumes the
global sign symmetry we are deliberately breaking) — this is stated here explicitly because it is
exactly the symmetry whose absence is the point of the experiment. Metropolis with a field it is,
with the critical-slowing-down cost that implies, and the decorrelation is measured rather than
assumed (§6).

## 4. Two arms, and why the exact one is primary

**ARM A — EXACT ENUMERATION (primary).** For a periodic lattice small enough to enumerate, the
Boltzmann distribution is computed in closed form over all `2^N` configurations and the three-spin
marginals are obtained by exact summation. There is **no sampling, no estimator, and therefore no
estimator bias** — the map is exact to floating point. Lattices: **4×4 (N = 16, 65 536 states)** on
the full grid and **6×4 (N = 24, 16 777 216 states)** on the same grid via GPU, as the finite-size
check.

Arm A is primary because the quantity being mapped is expected to be *small* (§7), and a small
quantity measured by a positively-biased plugin estimator is precisely the shape of finding this
programme has twice been burned by. An exact arm removes the failure mode instead of controlling
for it.

**ARM B — METROPOLIS MONTE CARLO (thermodynamic-limit check).** L = 16, 32, 64 with the full null
apparatus of §6. Arm B answers the question Arm A structurally cannot: whether the effect survives
to large lattices, and whether the peak locus moves with L (§7, the (b1)/(b2) split).

**The cross-validation that makes Arm B believable** is not a surrogate — it is Arm A. Arm B is run
at 4×4 and 6×4 as well, where the exact answer is known. The bias-corrected Monte Carlo excess must
reproduce the exact `I_C^(3)` there. Pre-registered tolerance: **agreement within 2 combined
standard errors at every (T,h) grid point tested, and no systematic sign to the residual.** If the
Monte Carlo pipeline cannot recover an answer we already know exactly, its readings at L = 64 are
not reported as measurements of anything.

## 5. Grid and geometry classes

**Temperature.** 48 points, `T ∈ [0.40, 5.00]`, denser in `[1.6, 3.2]` around `T_c = 2.269185`.

**Field.** `h = 0` **exactly** (the lemma's control column, reported first), then 32 points
log-spaced `h ∈ [10⁻³, 4.0]`. The magnetisation saturates well inside the top of that range.

**Geometry classes, kept separate and never averaged together** (the mission is explicit and it is
right: these behave differently and pooling them blurs the answer). All are defined by lattice
displacement vectors from a base site, and every translate of the class on the lattice is pooled —
translational invariance makes them the same triple.

| class | sites | why it is in the list |
|---|---|---|
| `star` | (0,0), (1,0), (0,1), taken as three of the four neighbours of (1,1)… i.e. displacements {(1,0), (0,1), (−1,0)} about a common centre | the direct integrate-out mechanism: three spins sharing one neighbour. Where an effective 3-body coupling is *generated* |
| `Lcorner` | {(0,0), (1,0), (0,1)} | the tightest triple on a square lattice: two NN bonds and one diagonal |
| `colin1` | {(0,0), (1,0), (2,0)} | collinear, nearest-neighbour spacing |
| `colin2` | {(0,0), (2,0), (4,0)} | collinear, spacing 2 — the separation-dependence handle |
| `plaq` | {(0,0), (1,0), (1,1)} | three of the four corners of one plaquette |
| `far` | three mutually maximally separated sites | the "well-separated" class; on the small exact lattices this is only mildly separated and that limitation is reported, not hidden |

**A square lattice is bipartite, so there is no nearest-neighbour triangle.** The mission's
"nearest-neighbour triangles" is realised here as `Lcorner`/`plaq`/`star`, which are the tightest
triples the geometry admits. Recorded because it is a substantive deviation from the brief.

## 6. Nulls, floors, and the honesty ledger — Arm B

Mandatory, per house rules 3, 4 and 5.

1. **Matched pairwise-maxent multinomial surrogate** at every grid point — the estimator-bias
   floor. Built by IPF onto the observed pair marginals (never an iid or Gaussian null; an iid null
   false-fired at +42σ on timeseries in this repository and voided an array run at τ_int = 87).
2. **Effective sample size, not nominal.** Pooling `L²` translates within one configuration does
   **not** give `L²` independent samples, and near `T_c` it gives far fewer. The surrogate is
   therefore drawn at `N_eff = N / F`, where `F` is the measured variance-inflation factor of the
   eight cell frequencies across independent configurations, relative to multinomial. Both the
   naive-`N` and `N_eff` floors are reported. Since plugin bias for this nested-family statistic
   goes as `1/(2N_eff)`, using nominal `N` would **understate the floor** — this is the exact trap,
   and it is being pre-empted rather than discovered.
3. **Configuration-level bootstrap** over independent configurations for the error bar, alongside
   the surrogate sd. The **more conservative of the two** is used for every z.
4. **Shuffle floor**: independently permute each of the three site-series across configurations,
   destroying all cross-site structure.
5. **Cross-configuration refuter**: build triples with slot *j* drawn from an independent run at the
   same (T,h), different seed. True share is zero by construction; any `|z| > 5` proves the null
   mis-specified and voids the grid point. This control saved the habit-dynamics numbers and voided
   the array-cap ones.
6. **Decorrelation measured, not assumed**: integrated autocorrelation time `τ_int` of the
   magnetisation at every (T,h); configurations are separated by `≥ 10 τ_int` sweeps and `τ_int` is
   reported. Grid points where the run is shorter than `200 τ_int` are marked **undersampled** and
   are not used for any peak claim.
7. **Tied fraction: structurally zero, and this is vacuous rather than reassuring.** Ising spins are
   natively binary; there is no analogue quantity being thresholded, so there are no ties to
   disclose and no static-nonlinearity artifact channel to fold. Stated as *the artifact mechanism
   is structurally absent* — **not** as *we checked and it was fine*. Those are different claims
   and this repo has been careful about the difference before (`SPIKE_SURVEY.md` §7 of the ECA
   controls).
8. **Everything reported as excess over the floor, never raw.** Raw share is printed alongside so
   the size of the correction is visible.
9. **Ceiling fraction** `I_C^(3) / ln 2` against the machine-checked three-slot cap, reported for
   every peak.

**Where the estimator is not to be trusted, stated in advance.** At strong field the distribution
approaches a point mass and the plugin estimator's bias-to-signal ratio diverges; at low `T` the
same happens by ordering; near `T_c` the correlation length diverges and `N_eff` collapses. A grid
point is marked **untrustworthy** and excluded from peak claims when any of: `min_cell p < 20/N_eff`;
`N_eff < 10³`; run length `< 200 τ_int`. These thresholds are fixed now.

## 7. Machinery gate — must PASS before any grid runs

The `k = 3` pair envelope is one-dimensional: adding `t·s₁s₂s₃` to the eight cell probabilities
preserves normalisation and all three pair marginals, and nothing else does. So the maxent member
is found by a single monotone root solve of `Σ_s σ(s)·log(p(s) + t·σ(s)) = 0`, `σ(s) = s₁s₂s₃`,
which is exact to machine precision and far better conditioned than IPF on a near-deterministic
distribution. **This fast solver is not trusted until it is gated against the repository's
validated machinery.** Gate, all conditions required to pass:

| # | test | required |
|---|---|---|
| 1 | fast solver vs. `array_cap_experiment.shareK` (IPF, tol 1e-13) on 2000 random 3-bit states | max abs diff `< 1e-12` |
| 2 | same, on 2000 states drawn near the boundary of the simplex (min cell `< 1e-6`) | max abs diff `< 1e-9`, and the fast solver is the reference where IPF fails to converge |
| 3 | exact three-coin parity | `I_C^(3) = ln 2` to `< 1e-12`, saturating the cap |
| 4 | exact independent state | `|I_C^(3)| < 1e-14` |
| 5 | explicit 3-body coupling `K = 0.9` (the survey's positive control) | `I_C^(3) ≈ 0.247` nats |
| 6 | 2000 random **sign-symmetric** states (the lemma) | `max |I_C^(3)| < 1e-12` |
| 7 | exact 4×4 Ising enumeration at `h = 0`, all 48 temperatures, all 6 geometries | `max |I_C^(3)| < 1e-12` |
| 8 | independent re-derivation of the 4×4 Boltzmann weights against a brute-force energy sum | exact agreement |

**GATE 7 IS THE RUN'S VALIDITY CONDITION**, and it is outcome (a) below. A failure there means the
pipeline is broken and every number produced by it is void.

## 8. Pre-registered outcomes and what each one means

Stated with their meanings before any data is seen. **No re-interpretation after the fact.**

**(a) `I_C^(3) ≡ 0` at `h = 0` for all `T`, to estimator precision.** The lemma's positive control.
Anything else means the pipeline is broken and **the run is VOID** — not "interesting", void. This
column is reported first, before any result.

**(b) `I_C^(3) > 0` for `h ≠ 0`, with a peak somewhere in the (T,h) plane.** Split, because the
split is where the actual information is:

- **(b1)** the peak locus tracks the critical point — approaches `(T_c, 0)` as `h → 0`, and the peak
  height grows with `L` → the order-3 structure is a **critical** phenomenon, and "higher-order
  structure peaks at criticality" turns out to be true for our quantity too, once the symmetry that
  forced it to zero is broken.
- **(b2)** the peak sits at `h = O(1)` and does **not** approach `T_c` as `h → 0`, and the peak
  height is `L`-independent once `L ≫ 1` → the structure is a **local, short-range** effect with no
  critical enhancement, and the literature's association of higher-order structure with criticality
  fails for our quantity in both directions: zero at the critical point by symmetry, and peaked
  somewhere else once symmetry is broken.

**(c) `I_C^(3) > 0` but monotone in `h` with no interior peak.** Report the magnitude and where it
saturates. **This outcome is close to excluded a priori and I am saying so now rather than
claiming a discovery later** — see §9.

**(d) `I_C^(3) ≈ 0` everywhere, including `h ≠ 0`.** A clean negative that goes strictly beyond the
lemma: the Ising universality class would carry no odd-order connected information at any field, not
merely at zero field. This would be worth stating plainly and would deserve its own attempt at a
proof.

## 9. What I expect, and why — stated before running

**I expect (b), and within it (b2). I also expect the magnitude to be small: peak `I_C^(3)` of order
`10⁻³` to `10⁻²` nats, a ceiling fraction of roughly 0.1 %–1 % of `ln 2`.**

**Why (b) rather than (c) or (d) — the boundary argument, and it is nearly a proof.** `I_C^(3) ≥ 0`
always (the state itself lies in its own pair envelope, so the supremum is at least its entropy).
And it vanishes on the *entire* boundary of the quadrant `{T > 0, h > 0}`:

| edge | why `I_C^(3) → 0` |
|---|---|
| `h = 0`, any `T` | sign-symmetric — the machine-checked lemma |
| `T → ∞`, any `h` | `β → 0`, spins independent and uniform |
| `h → ∞`, any `T` | point mass at all-up |
| `T → 0`, `h > 0` | unique ground state, point mass at all-up |
| the corner `T → 0, h → 0` | the two-fold degenerate ferromagnetic ensemble — which this repo has *already* machine-checked at zero share, `SignSymmetry.share_ferro` |

A continuous non-negative function that vanishes on the whole boundary of a region and is positive
somewhere inside **must** have an interior maximum. So "we found a peak" is, on its own, close to
trivial here, and **it must not be reported as a discovery.** The genuine content of this experiment
is exactly three things: (i) whether the quantity is nonzero at all, i.e. (b) vs. (d); (ii) **where**
the peak sits, i.e. (b1) vs. (b2); (iii) **how big** it is against the cap. Writing this down now is
the point of pre-registration — it removes the option of dressing an inevitability as a result.

**Why (b2) rather than (b1).** The mechanism that generates an effective three-body coupling is
local: integrating out a spin `s₀` coupled to `s₁,s₂,s₃` and to the field contributes
`log cosh(β J(s₁+s₂+s₃) + βh)`, whose `s₁s₂s₃` component is `¼[tanh(3a) − 3 tanh(a)]·βh + O((βh)²)`
with `a = βJ`. At `a = 0.4407` (the critical coupling) that is `≈ −0.094·βh` — a short-distance
quantity, set by the local coordination, with nothing in it that diverges as `ξ → ∞`. And
`I_C^(3) ≈ ½K²·Var(s₁s₂s₃)` for small effective coupling `K`, which is **quadratic** in an already
small number. Hence both the (b2) prediction and the `10⁻³`–`10⁻²` nat magnitude estimate. Since
`K ∝ βh` at small field but the fluctuation factor dies as the system orders, the peak should sit
where the system is **partially** magnetised — my advance guess is `|m| ≈ 0.5–0.8`, at `h` of order
`T`, and **not** at `T_c`.

**Advance prediction with teeth, and its own separable kill.** The `star` class — three spins
sharing a common neighbour — should carry the **largest** `I_C^(3)` of the six geometry classes at
the peak, because it is the class in which the integrate-out mechanism above operates directly. If
some other class beats it, my mechanistic account is wrong even if the map is right, and I will say
so. This kill takes down the mechanism story and nothing else: the map survives it.

**On the ordinary measures.** I expect `TC` and `Ω` to peak in the **ordered** region — at `h = 0`
and low `T`, where `TC → 2 ln 2` on this very lattice (`SignSymmetry.S_total_ferro`, machine-checked)
while `I_C^(3)` is **exactly zero** by the lemma proved in the same file. If that is what the map
shows, the survey's thesis is demonstrated inside a single canonical model, on one set of samples:
**the standard higher-order instruments are maximal exactly where the pairwise-blind quantity is
provably zero.** I expect this and will report it whichever way it comes out.

## 10. Kills, staked first and separable

Each takes down its own claim and nothing beneath it.

- **K1 (validity).** `I_C^(3)` at `h = 0` exceeds `1e-12` (Arm A) or `5σ` above its floor (Arm B) at
  any grid point → **the run is void**, the pipeline is wrong, nothing else in it is reported as a
  measurement.
- **K2 (existence).** Peak `I_C^(3)` over the whole `h ≠ 0` plane fails to exceed its floor by `5σ`
  (Arm B) and is below `1e-10` nats exactly (Arm A) → **outcome (d)**: broken sign symmetry is not
  sufficient to produce odd-order connected information in this model, and the "turn on a field"
  move is refuted. Takes down this experiment's hypothesis, not the lemma.
- **K3 (locality of the mechanism).** The peak locus approaches `T_c` as `h → 0` **and** the peak
  height grows with `L` across L = 16, 32, 64 → my (b2) prediction is dead and (b1) stands. Takes
  down my prediction, not the map.
- **K4 (mechanism).** Some class other than `star` carries the largest peak `I_C^(3)` → the
  integrate-out account in §9 is wrong. Takes down the mechanism story, not the map.
- **K5 (cross-arm).** Arm B's bias-corrected excess fails to reproduce Arm A's exact value at 4×4
  and 6×4 within 2 combined standard errors → **Arm B is not reported**, at any lattice size. Takes
  down the Monte Carlo arm, not the exact map.

## 11. What this experiment cannot establish, recorded now

- Nothing about nature. A spin lattice is a model; no reading here is evidence for or against
  `wild-share`, and no sentence in the results memo will suggest otherwise.
- Nothing about `k > 3`. The lemma's general odd-order form is unmechanized and untouched here.
- Nothing about priority. If a peak is mapped, the claim is "we did not find this in the
  literature", not "this is the first time it has been done" (`SPIKE_SURVEY.md` reach caveat).
- No promotion of anything to `Stance.lean`. This is a scratchpad experiment; any stance change
  would require a separate refuter pass and Eric's review.

---

Deliverables: this file (committed first), then `ising_field.py` and `ISING_FIELD_RESULTS.md`.
