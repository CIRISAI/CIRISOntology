# PRE-REGISTRATION — the whole-only order-3 reading of a supercooled liquid, swept in temperature

**Committed before any share was computed on any real configuration.** The instrument's
docimasia (`glass_gate.py`, nine checks, three of them theorem-pinned) ran first and on
synthetic data only; its result is quoted in §6 because a gate that has not seen dye cannot
gauge anything, and because none of it is a reading on a glass.

**SCOPE, stated first and repeated in every document of this campaign.** This is a measurement
on **simulated glass formers** — the three-dimensional Kob–Andersen binary Lennard-Jones
mixture and a two-dimensional ternary mixture, as distributed in `GlassBench` — and **not on
experimental glasses**. It is a contribution to a decades-old dispute about whether static
structural order grows as a liquid is supercooled; it is **not a solution to the glass
transition** and nothing in it is offered as one. **Nothing here bears on `wild-share`**, on
`adequacy`, or on any claim about nature at large, and **nothing here moves `Stance.lean`**.
No Lean file is opened, `lake` is not run, the audit is not run, nothing is pushed.

---

## 1. THE CREDIT BLOCK — read before any number in this campaign

The physical question this campaign asks has been asked for seventy years, and the quantity
that answers it has a name in a literature this repository had not been searching. Per the
house standard (`convergent-art-pattern`: *assume the result is already in print until the
primary text says otherwise; search by the mathematical object, never by our vocabulary*), the
credits come before the design, not after the result.

### 1.1 Residual Multiparticle Entropy — the same physical question, a different object

The excess entropy of a fluid expands in multiparticle correlations,

> `s_ex = s_2 + s_3 + …`

— **Green (1952)**; **Nettleton & Green, JCP 29:1365 (1958)** — made computable from simulation
by **Baranyai & Evans, *Phys. Rev. A* 40:3817 (1989)**, "Direct entropy calculation from
computer simulation of liquids". The two-body term is built from the pair correlation function
alone; for a mixture, from the *partial* pair correlation functions,

> `s_2/k_B = −2πρ Σ_αβ x_α x_β ∫₀^∞ { g_αβ(r) ln g_αβ(r) − [g_αβ(r) − 1] } r² dr`.

The remainder is the **Residual Multiparticle Entropy**,

> `Δs = s_ex − s_2` — **Giaquinta & Giunta, *Physica A* 187:145 (1992)**,

described in that literature as *the net contribution to entropy due to spatial correlations
involving three, four, or more particles*. It carries a famous **zero-crossing** as a control
parameter is swept — the **zero-RMPE criterion**, read as the onset of emergent local
structural organisation — and the generality of that crossing is **disputed**:
**Krekelberg, Mittal, Ganesan & Truskett, JCP 128:161101 (2008)**, "Residual multiparticle
entropy does not generally change sign near freezing", with **Giaquinta's comment, JCP
130:037101 (2009)**.

**It is not our quantity, and the difference is exact and checkable.** `s_2` is a **truncation
of an infinite series**, not the entropy of the pair-maxent distribution. The decisive tell:
**RMPE can go negative**, and our share **cannot** — `share = S(Q) − S(P)` where `Q` maximises
entropy over a set that *contains* `P`, so `share ≥ 0` always, identically, with no condition.
They are different objects answering the same physical question. **This is our sharpest claim
to a distinct object and it is stated here, before the design, rather than argued after a
result.**

### 1.2 The correction this campaign owes its own survey, paid before the first number

`scratchpad/TARGET_REGISTRY.md` §3.1 and §4.1 state that what has *not* been done is *"to trace
it across the glass transition as a physical observable rather than as a fitting loss. That gap
is the campaign."* **Searching before computing, that statement is too strong, and the
narrowing is recorded here rather than left to be found later:**

> **Banerjee, Nandi, Sastry & Maitra Bhattacharyya, JCP 145:034502 (2016)** (arXiv:1604.03674),
> "Effect of total and pair configurational entropy in determining dynamics of supercooled
> liquids over a range of densities", computes the **species-resolved two-body excess entropy
> `s_2` and defines `ΔS = S_ex − S_2`** for the **Kob–Andersen 80:20 binary mixture** — *the
> exact system this campaign's primary arm reads* — at **densities ρ = 1.2, 1.4, 1.6**, and
> plots it **against temperature** into the supercooled regime, remarking that the residual
> term is "really small" against the pair contribution.

So the RMPE-family object **has** been traced across temperature, on our own primary model.
What survives of the registry's gap statement, and all that this campaign may claim, is the
narrower thing:

> **A non-negative, pairwise-blind maximum-entropy gap has not, as far as this search reaches,
> been traced across the supercooling of a glass former.** The *truncated-series* version has
> been, on this very model, ten years ago.

This is the same correction, in the same direction, that §3.1 itself made to `SPIKE_SURVEY.md`.
The reach of the present search is stated in §9.

### 1.3 Torquato & Stillinger — our niche stated as a theorem, by someone else, in 2003

**Torquato & Stillinger, *Phys. Rev. E* 68:041113 (2003)**, "Local density fluctuations,
hyperuniformity, and order metrics", constructs **`g₂`-invariant processes**: explicitly
different point processes that share an identical pair correlation function. That the pair
correlation function does not determine a configuration is not a discovery available to this
campaign; it is a theorem somebody else proved twenty-three years ago. **Our surrogate (§4.4)
is a `g₂`-invariant construction in the species channel and is credited as such.**

### 1.4 M. S. Shell — our share, computed routinely, as a fitting loss

**M. S. Shell, JCP 129:144108 (2008)**, "The relative entropy is fundamental to multiscale and
inverse thermodynamic problems." By the Pythagorean identity for exponential families,
`min_q D(p‖q)` over a pair-potential family **equals** `S(Q) − S(p)` with `Q` carrying `p`'s
pair correlations — **that is exactly our share**, computed every day in the coarse-graining
literature under the name `S_rel`, as an objective function to be minimised. The whole
Iterative-Boltzmann-Inversion / relative-entropy programme is therefore machinery for building
our null, and §4.4 uses it as such rather than pretending otherwise.

### 1.5 The three-point structure of this exact model has been measured

**Coslovich, JCP 138:12A539 (2013)** (arXiv:1212.5360), "Static triplet correlations in
glass-forming liquids: A molecular dynamics study", evaluates three-point static correlation
functions `S⁽³⁾` and direct triplet correlations `c⁽³⁾` **in the Kob–Andersen Lennard-Jones
mixture and its WCA variant**, finds more pronounced local ordering in the LJ model consistent
with its slower dynamics, and identifies a broad positive small-wavevector peak indicating
**genuine three-body contributions** beyond the pair level. Anyone reading this campaign should
read that paper first. Our object differs — a triplet *correlation function* is a moment, and
`Core/SignSymmetry.lean`'s recorded trap is that a large three-point correlator is **not**
order-3 structure (a pairwise Hamiltonian with a field reaches `⟨s₁s₂s₃⟩ ≈ 0.91` at a share of
order `1e−14`) — but the physical question is the same one and the priority is his.

### 1.6 The rest of the neighbourhood, named

* **Amorphous order** as a programme: point-to-set correlations, **Biroli, Bouchaud, Cavagna,
  Grigera & Verrocchio, *Nat. Phys.* 4:771 (2008)**; the dynamical competitor `χ₄`; the
  machine-learning programme (**Bapst et al., *Nat. Phys.* 16:448 (2020)**).
* **Connected information of order 3**, the measure itself: **Schneidman, Still, Berry &
  Bialek, PRL 91:238701 (2003)**; **Amari, IEEE TIT 47:1701 (2001)**.
* **Coarse-graining creates connected information**: **Kahle, Olbrich, Jost & Ay, PRE
  79:026201 (2009)** — which is why §5's binmint gate exists.
* **Reverse Monte Carlo**, the community's pair-matched generator: **McGreevy & Pusztai,
  *Mol. Simul.* 1:359 (1988)**.
* **Copula invariance** of rank-based readings: **Sklar (1959)**; in a physics setting,
  **Scherrer, Berlind, Mao & McBride, ApJL 708:L9 (2010)**.
* **The data**: `GlassBench`, **Jung et al., "Roadmap on machine learning glassy liquids"**
  (arXiv:2311.14752), Zenodo 10.5281/zenodo.10118191, CC-BY-4.0; the KA trajectories are
  **Shiba, Hanai, Suzumura & Shimokawabe, JCP 158:084503 (2023)** (BOTAN); the KA2D set is
  **Jung, Biroli & Berthier, PRL 130:238202 (2023)**. Every required citation in the dataset's
  own README is carried in `GLASS_DATA.md`.

**Assume convergence.** The searches behind §1 are recorded in §9 with their reach. A null from
a survey is weaker than a null from an experiment, and "not found" is not "does not exist".

---

## 2. THE QUESTION, in the field's own words

A glass has the pair correlation function `g(r)` of a liquid while behaving mechanically like a
solid. Does **static order invisible to `g(r)`** grow as temperature falls toward the glass
transition?

Our instrument measures exactly that quantity and nothing else: the entropy gap between a
configuration's distribution and the maximum-entropy distribution carrying **all** of its pair
structure. On three discrete slots,

> `share = S(Q) − S(P)`, `Q = argmax { S(q) : q has P's three pair marginals }`.

It is **zero exactly when `P` is reconstructible from its own pairs**, and it is **never
negative**.

---

## 3. THE SLOT DESIGN — the one decision this campaign turns on

Continuous particle configurations must become a discrete trivariate object, and
**coarse-graining mints share** (`Core/Creation.lean`: `repair_mints_from_noise`; Kahle et al.
2009; `GATES.md` reach 5). The choice below is made, justified, and its residual minting
channel is measured rather than assumed.

### 3.1 The primary design: SPECIES at a geometric template

> **Three particles whose three mutual separations all lie in a pre-registered shell. Each slot
> carries that particle's own SPECIES label. Nothing else.**

Three candidate designs were considered. The reasons for this one, in order of weight:

1. **The alphabet is atomic, so the most dangerous channel is absent by construction, not
   bounded by a sweep.** Species is already discrete. In the 3D arm it is already *binary*
   (A/B, 80:20). There is **no continuum to bin**, so the binarization-minting channel — the
   one `GATES.md` reach 5 records with a kept taint and **no plumb line**, and the one the
   brief for this campaign names as the single most dangerous here — **does not act on the
   label at all**. The only coarse-graining left in the design is *geometric* (the shell
   tolerance), and §5.2 measures that one directly.
2. **The pair marginals ARE the field's own object.** The pair structure our `Q` carries is
   the species-resolved pair correlation — `g_AA`, `g_AB`, `g_BB` restricted to the template.
   The field's statement "the glass has the `g(r)` of a liquid" is a statement about exactly
   these functions. The correspondence between our null and the field's question is therefore
   not analogical; it is the same object.
3. **The sign-symmetry theorem does not bite.** `Core/SignSymmetry.lean`'s
   `share_eq_zero_of_signSymmetric` sends the share to *exactly zero* on any state invariant
   under the global flip. At 80:20 composition the flip A↔B is not a symmetry of the state, so
   the theorem does not apply and we are not being sent to measure a proved zero (FACT 1 of
   `TARGET_REGISTRY.md` §0).
4. **The valve floor is zero.** There is no counting noise anywhere: the configurations are
   exact particle coordinates from a deterministic integrator. `Core/Valve.lean`'s
   `valve_needs_asymmetry` gives a minting floor of exactly zero for a design with no
   asymmetric per-cell channel — contrast the sky campaign, where Poisson resampling alone
   multiplied the null by 5.8× (FACT 2, `SKY_REALDATA_RESULTS.md` §2).
5. **Chemical short-range order is a real and named phenomenon**, and "structure invisible to
   the total `g(r)`" is how metallic-glass work already describes it.

**The cost of this choice, stated.** It reads the *compositional* channel only. A one-component
glass has no species, and a purely geometric amorphous order — icosahedral packing, locally
preferred structures — is **outside this design's reach**. A null here is a null about
compositional order-3 structure and may not be reported as a null about amorphous order in
general. That limitation is not a caveat added later; it is the price of removing the minting
channel, and it is paid knowingly.

### 3.2 The designs NOT chosen, and why

* **Coarse-grained density in three cells at fixed geometry.** Rejected. It requires binning a
  continuum (minting channel wide open), and the local density of a dense liquid is close to
  Gaussian — hence close to sign-symmetric under a median split, hence close to a theorem-zero
  by `share_eq_zero_of_signSymmetric`. We would be measuring the departure from a proved zero
  with the minting channel unbounded. This is the weakest of the three.
* **Local order parameters (Voronoi volume, `q₆`/`ψ₆`, softness) binned at three sites.**
  Rejected as *primary*, retained as a named secondary (§7.3). It is the design the field would
  recognise, and it reaches the geometric order that §3.1 cannot. But it walks straight into
  FACT 3's trap: a local order parameter is a **filter over a neighbourhood**, the sites' values
  share particles by construction, and the binning follows the filter — the exact composition
  (`pointwise map, then linear filter`) that manufactured **66 σ** of share from nothing in the
  sky pilot. If it is run, it is run with the full binmint battery and it is reported second.
* **Species occupancy** — chosen, above.

### 3.3 The slots, exactly

* A **triple** is an ordered vertex triple `(i, j, k)` of distinct particles in one
  configuration such that `|r_ij| ∈ S₁₂`, `|r_ik| ∈ S₁₃`, `|r_jk| ∈ S₂₃`, under the minimum
  image convention in the periodic box.
* Slot `m` carries the **species** of the `m`-th vertex. 3D KA: binary, `A = 0`, `B = 1`. 2D
  KA2D: ternary — see §3.5.
* **Triples are enumerated in every order the template's own symmetry allows** (for the
  equilateral template, all six). The three particles are not physically distinguishable, so
  the reading must not depend on which one was called slot 1. This makes the state exchangeable
  in the equilateral case, which leaves exactly one free direction — the parity direction — and
  that is precisely the direction the share reads.
* The estimator is `share_2x2x2`: **exact**, one-dimensional fibre, bisection to machine
  precision. **No IPF is used anywhere in the primary reading** (`ipf-sharek-boundary-drift`).

### 3.4 The geometry ladder — the FULL grid, not the diagonal

Per `order3-probe-geometry` (*scan the full lag-pair grid; the equally-spaced diagonal is
provably blind to maximal permanent order-3*), the templates are a grid, not a line. In LJ
units with `σ_AA = 1`, box `L ≈ 15.04` for the 3D arm:

* **Equilateral ladder** `(r, r, r)` for
  `r ∈ {0.89, 1.07, 1.3, 1.5, 1.8, 2.1, 2.5, 3.0, 4.0, 5.0, 6.0}`. Two of these rungs are fixed
  from `GLASS_DATA.md` §3.2's measured `g_αβ(r)` — **`r = 1.07` is the measured `g_AA` first
  peak** and the primary rung, and **`r = 0.89` is the measured `g_AB` first peak**, included
  deliberately as a **stress test for the LP gate**: it sits *below* the `g_AA` onset (0.97), so
  an equilateral triangle there nearly forbids A–A contacts and the eight-cell table is
  structured by excluded volume alone. If any rung is pair-pinned, that is the one, and it is
  put in so the gate has something to catch. Choosing rungs from `g(r)` is legitimate and is
  declared: `g(r)` is a *pair* quantity that this instrument is blind to by construction, and it
  has been published for this model since 1995.
* **Full scalene grid** `(r₁₂, r₁₃, r₂₃)` over all combinations from
  `{1.1, 1.5, 2.1, 3.0}` satisfying the triangle inequality within tolerance.
* **Tolerance ladder** `Δ ∈ {0.05, 0.10, 0.15, 0.20}` on every shell; `Δ = 0.10` is the primary.
* **The far arm** `r ∈ {5.0, 6.0}` is a **theorem-pinned internal null on the real data**: at
  separations beyond the structural correlation length the three species are independent, the
  state is a product state, and `valve_from_nothing` gives share **exactly zero**. It runs
  through the byte-identical pipeline as every other template. This is the campaign's plumb
  line and `GATES.md` records that six of thirteen reaches have none.

The 2D arm uses the same ladder scaled to its own first peak, fixed from `g(r)` before any
share is read.

### 3.5 The 2D ternary arm, and its extra channel

KA2D has **three** species. Two readings are pre-registered:

* **the merged binary reading** — type 1 versus types {2,3} — which introduces an
  **alphabet coarse-graining** that the 3D arm does not have, and is therefore gated by the
  binmint construction of §5.2 applied to the *alphabet* rather than to the geometry;
* **the full 3×3×3 reading**, which needs a maxent solve on 27 cells and therefore needs the
  IPF-versus-dual certificate of §5.5. If that certificate fails, the rung is **VOID**.

### 3.6 The control parameter

**Temperature**, swept over the ladder the data provides. 3D KA (primary):
`T ∈ {0.44, 0.50, 0.56, 0.64}` at `ρ = 1.2`, against `T_MCT = 0.435` and an onset/melting
temperature `≈ 1.03`. 2D KA2D (replicate): `T ∈ {0.23, 0.30}`. `GLASS_DATA.md` states exactly
what this ladder does and does not straddle, and that statement is part of this
pre-registration by reference: **the ladder bottoms out at the mode-coupling temperature and
does not reach the laboratory glass transition.**

### 3.7 Count-matching across the ladder — mandatory, and stated before the sweep

The number of triples found at a fixed template **changes with temperature**, because `g(r)`
sharpens on cooling. The estimator's floor scales as `1/(2N)`. **An uncorrected sweep would
therefore show a temperature trend built entirely out of the floor.** Two readings are
pre-registered and both are reported:

* **count-matched** — every temperature subsampled to the minimum triple count across the
  ladder at that template, fixed seed, recorded;
* **full-count** — every temperature at its own `N`, each against a floor drawn at **its own
  `N`** (`GATES.md` harvest: *floor matched to sample size*; the Dalitz D2 taint, where a rise
  vanished entirely under size-matched floors).

If the two disagree in sign, the trend is **void**.

---

## 4. THE CONTROLS

### 4.1 Product control — theorem-pinned zero, and it IS the floor

Same configurations, same positions, same template selection, **species drawn iid Bernoulli**
at the ensemble composition. The state is a product state, so `valve_from_nothing` gives share
**exactly zero**; whatever is read is the finite-sample floor at that sample. Drawn at least
200 times per (T, template) so the **shape** of the null is measured before any `z` is quoted
(`share-null-is-chi2-shaped`; the null is `χ²₁`-like, so **p-values are quoted and a `z` from a
median-and-sigma is not**).

**THE FLOOR IS THE CONTROL, NOT A MULTINOMIAL RESAMPLE — and this correction is why the
examination in §6.1 was run before this document was committed.** The obvious floor, a
multinomial resample of the pooled table at its raw triple count `N`, is **wrong here and wrong
in the dangerous direction**. The enumerated triples **share particles**: at the first
coordination shell each particle sits in several of them, so the effective independent count is
far below `N` and the finite-sample bias is far above `1/(2N)`. Measured on a synthetic ideal
gas through the identical pipeline, the multinomial floor read `3.3e−6` where the control's own
spread was `1.5e−4` — **a factor of 45**. Every floor in this campaign is therefore the
**control itself, pushed through the byte-identical triple selection**: same configurations,
same template, same tolerance, same cap, same triples, **only the labels change**. The naive
multinomial floor is still computed and reported, purely so the **overlap penalty** — the ratio
between the two — is visible in the record instead of being argued about.

### 4.2 Permutation control — the finite-population correction, measured not assumed

Same positions, species **randomly permuted within each configuration**. This holds the
composition exactly, but a permutation of a fixed multiset is *not* iid: it carries a
finite-population correlation of order `1/N ≈ 2.4 × 10⁻⁴` at `N = 4096`, which enters the share
at second order and is **not obviously below the floor** at the triple counts this campaign
will reach. The difference between §4.1 and §4.2 **gauges it**, and is reported. Any reading
smaller than that difference is ungauged.

### 4.3 Ideal-gas / random-configuration control

Random positions at matched density and matched composition, iid species, through the
byte-identical template pipeline. **Must read the floor.** This is the check on
**template-selection minting** — selecting triples by a geometric template is a selection on
the configuration, and selection is a filter (FACT 3's trap). If this control reads above its
own floor, the selection is manufacturing and every reading is fouled.

### 4.4 The pair-matched generative surrogate — the load-bearing gate

The physical null is not "no structure"; it is **"nothing beyond what the pair correlations
already imply."** Concretely: hold the **positions fixed** — so the geometry, the template, the
tolerance, the box, the finite-size effects and the selection are all *byte-identical* — and
resample only the **species**, from the maximum-entropy distribution over species assignments
whose **radial species correlation function matches the data's**.

That distribution is the Gibbs measure `P(s) ∝ exp(−Σ_{i<j} u_{s_i s_j}(r_ij))` on the fixed
point pattern, with `u` on a radial grid, composition conserved by swap moves. It is fitted by
iterative Boltzmann inversion — i.e. by **Shell's `S_rel` programme (§1.4)**, used here to
*build the null* rather than to fit a model. It is a **`g₂`-invariant construction in the
species channel (§1.3)**, and it is the same object Reverse Monte Carlo produces in the
positional channel, which is why it can be trusted to be the community's null and not ours.

**This surrogate can and generally will read a NONZERO share**, because a pair-potential
ensemble has genuine triplet structure — that is the Kirkwood-superposition-violation physics
Coslovich measured (§1.5). **That is the whole point.** The deliverable is the difference.

**Its own dye test, required before its null reading means anything** (`GATES.md` reach 13):
plant an explicit three-body species coupling of known amplitude into a synthetic ensemble;
the surrogate must reproduce the pair correlations and **fail** to reproduce the planted
three-body term, at the amplitude that matters. If the surrogate cannot see the dye, every
verdict resting on it is **ungauged**, not clean.

### 4.5 The high-temperature liquid at matched density — the field's own null

**Stated honestly: GlassBench contains no high-temperature liquid.** Its hottest 3D state point
is `T = 0.64`, well below the onset temperature `≈ 1.03`; the entire ladder is inside the
supercooled regime. So this control must be **generated by us** — our own MD of the same model
at the same density at `T ∈ {1.0, 2.0}` — and it is pre-registered as a **secondary** control
with its own validation requirement: our integrator must reproduce GlassBench's own measured
`g_αβ(r)` at `T = 0.64` before its high-`T` output is used for anything.

Two things are said in advance. First, **§4.4 supersedes this control on its own terms**: the
question "does the share distinguish a glass from a liquid at *matched* `g(r)`" is answered
exactly by the pair-matched surrogate, whose `g(r)` is matched by construction, whereas a real
high-`T` liquid's `g(r)` merely resembles the glass's. Second, **this arm may not be reached**,
and §7.6 names "pre-registered arm not run" as an outcome so that its absence cannot later be
passed over in silence.

---

## 5. THE GATE BATTERY — each gate with its discharge point named

Gates are named by their reach in `GATES.md`. "Discharge point" means the stage at which the
gate is run and the artifact in which its reading is filed.

### 5.1 G-LP — pair-pinning at analysis resolution (reach 4) — **MANDATORY**

`KAPPA_EDGE_RESULTS.md` is the reason this gate is mandatory: on our own hardware, every
distribution carrying the measured fine pair marginals had a b=2 share of *exactly* the
measured value — the LP interval had width `0.00000`, and a live headline had to be re-scoped
three times. **A glass's local structure may pin the reading the same way.**

**Run:** at every `(T, template)`, `share_headroom(P)` — the exact interval the share can occupy
over every distribution carrying `P`'s own three pair marginals. **Discharge:** in
`GLASS_RESULTS.md`, one row per read cell.

**The expectation, pre-registered as the brief requires.** *I expect the LP NOT to collapse
here, and the reason is structural rather than hopeful:* the array's pinning was traced
(`KAPPA_EDGE_RESULTS.md` §5) to **near-determinism of the conditional support** — the third
variable's value, given the first two, confined to one side of its own median on most of the
support — and the load-bearing control there showed that **coupling strength is not the
variable**. Species identity given two neighbours' species is genuinely stochastic in a
disordered mixture; there is no deterministic map to collapse the support. **Numeric advance
prediction: headroom ≥ 0.30 nats at every read template, i.e. at least two orders of magnitude
above any plausible reading.** If it collapses, that is a finding about glasses, and the
affected cells are VOID.

**Where it could bite, named in advance:** at the smallest template `r = 1.1`, excluded volume
may make some species cells nearly empty (B–B contacts are strongly disfavoured in KA), which
squeezes the feasible interval and can force the share positive from the pair marginals alone.
That is the cell to watch, and §5.3's occupancy sluice fires there first.

### 5.2 G-BINMINT — coarse-graining / binarization minting (reach 5) — **THE MOST DANGEROUS CHANNEL**

§3.1 removes this channel from the *label*. It does **not** remove it from the *geometry*: the
shell tolerance `Δ` is a coarse-graining of a continuum, and merging fine radial sub-bins is
exactly the operation that mints.

**Run, in the sky campaign's own form (the `binmint` pedestal, `REFUTER_RESULTS.md` §A9a):**
build the fine object with slot `m` carrying `(species_m, radial sub-bin of one incident edge)`
under a fixed assignment rule, alphabet `2·b_r`; take its **pair-maxent at fine resolution**;
**merge** to the analysis alphabet; read the share of the merged pair-maxent. That number is
share manufactured by the merge and by nothing else — the **pedestal**. `b_r ∈ {2, 3, 4}`.

**Also run:** the tolerance ladder `Δ ∈ {0.05, 0.1, 0.15, 0.2}` (the reading must not be created
by `Δ`), and the fine-resolution **LP** — the exact range the coarse share can occupy over every
distribution carrying the *fine* pair marginals, which is `t_range_given_fine_marginals` of
`kappa_edge.py` ported to this alphabet.

**Discharge:** `GLASS_RESULTS.md`, pedestal as a percentage of the reading, per cell.
**Rule fixed now:** pedestal ≥ 50 % of the reading ⇒ that rung is **VOID**. Between 10 % and
50 % ⇒ reported as a quoted systematic on every number in that rung, never a footnote.

### 5.3 G-OCC — occupancy / sparsity (reach 11)

`KAPPA_EDGE_RESULTS.md` §7 voided a whole b-ladder because the excess climbed monotonically as
occupancy collapsed, reaching 39 % of `ln 2` on a table 82.6 % empty.

**Rule fixed now, before any table is seen:** the 8-cell analysis table is read only if **every
cell holds ≥ 30 counts**. A fine table of `(2b_r)³` cells is read only if **occupancy ≥ 50 %**
and every occupied cell holds ≥ 10. Below either bar the rung is **ungauged** — which is
neither zero nor a detection — and is reported as loudly as a reading. Tied fraction and empty
fraction are disclosed for every table.

### 5.4 G-FLOOR — estimator bias, matched to sample size (reach 1)

Every reading is quoted **after subtraction of a floor drawn at its own `N`**, from the product
control of §4.1, over ≥ 200 draws. Sub-sample readings get sub-sample floors (`GATES.md`
harvest, the Dalitz D2 taint). The floor's **shape** is reported before any significance is
quoted, and significance is quoted as a **p-value against the empirical null**, never as a
median-and-sigma `z` (the Dalitz D7 near-miss).

### 5.5 G-CERT — solver / relaxation gap (reach 12)

The primary 2×2×2 reading is **exact** and uses no solver, so this gate is vacuous there and
that is stated rather than claimed as a pass. Wherever a maxent solve is needed — the fine
binmint tables, the 3×3×3 KA2D reading — **both** IPF and a dual/L-BFGS solve are run and
compared; disagreement in `H(Q)` above `1e−9` **VOIDs** that rung. IPF is never used alone
(`ipf-sharek-boundary-drift`: one-sided overstatement by five orders of magnitude on
near-deterministic states).

### 5.6 G-MIX — mixture / manufacture (reach 3)

If the temperature sweep shows an **interior peak**, it must be shown that a null which cannot
produce the claimed structure does not reproduce it. The ECA taint is the anchor: a spike that
survived an iid null collapsed **1886×** under a mixture null. **Run:** a mixture of the
ladder's own endpoint ensembles, matched in triple count, against the interior point.

### 5.7 G-DOSE — dose vs rate (reach 7)

The nuisance that tracks temperature here is the **triple count** (§3.7) and the **degree of
structural ordering in `g(r)` itself**. **Run:** the reading against triple count at fixed `T`
(by subsampling), and against `T` at fixed triple count. If the reading tracks the count rather
than `T`, the trend is **void**.

### 5.8 G-POL — probe polarity (reach 8)

Declared **now**, before any run: **a PASS of the growth hypothesis is share *increasing* as `T`
*decreases*.** The far arm's PASS is a reading **at or below** its floor's p99. The LP's PASS is
a **wide** interval. The binmint's PASS is a **small** pedestal. Each direction is written down
here so that an implementation with the sign inverted is caught against this text and not
against intuition (`GATES.md` reach 8; commit 9180c6a, where the reviewer's own gate was the
one that was wrong).

### 5.9 G-DYE — power of the control itself (reach 13)

Every control must be shown to detect a **planted** signal of the size that matters before its
null reading is allowed to mean anything. `glass_gate.py` G5 does this for the estimator (a
planted three-body coupling, recovered monotonically from `1.3e−7` to `1.2e−2` nats). §4.4
requires it for the surrogate. **A control that cannot see the dye returns "ungauged", not
"clean".**

### 5.10 G-REPRO — gate-log provenance (record integrity)

Every committed number must be reproducible from the instrument committed beside it. Samplers
are seeded and the seeds are recorded; the deterministic parts are re-run and compared before
the log is trusted (`GATES.md` harvest; the phi4 gate log at `5e3df2f`).

---

## 6. THE INSTRUMENT'S OWN EXAMINATION, ALREADY RUN

`glass_gate.py`, on synthetic data only, **before** this document was committed and before any
real configuration was touched. Nine checks, all **PASS** (`glass_gate.json`):

| | check | result |
|---|---|---|
| G1 | parity state ⇒ `share = log 2` exactly (`Core/Share`) | `0.6931471805599452` |
| G2 | product state ⇒ `share = 0` exactly (`Core/Valve`, `valve_from_nothing`) | worst `4.4e−16` over 200 states |
| G3 | sign-symmetric state ⇒ `share = 0` exactly (`Core/SignSymmetry`) | worst `4.4e−16` over 500 states |
| G4 | agreement with `dalitz_share.share_2x2x2` | worst `0.0` over 500 random tables |
| G5 | **dye**: planted three-body coupling recovered, monotone | `0 → 1.3e−7 → … → 1.2e−2` nats |
| G6 | finite-sample floor tracks `1/(2N)` on an 80:20 base | ratios `0.63, 0.47, 0.42, 0.42` at `N = 1e4…1e7` |
| G7 | triangle enumerator, simple cubic, hand-counted | `(1,1,1) → 0` exact; `(1,1,√2) → 24N` exact |
| G8 | minimum image: count invariant under translation | identical at four shifts |
| G9 | headroom LP contains the measured share and is wide | uniform and parity both `0.693` |

**One failure is on the record and is kept.** G7's first version used the 2D triangular lattice
and **FAILED** — because that lattice is not commensurate with a square periodic box, so *the
expectation was wrong and the enumerator was right*. It was replaced by the simple-cubic case,
which is hand-countable in a periodic box, and the reason is written into the source rather
than quietly swapped.

**The floor on tables, measured:** median `2.1e−8` nats at `N = 10⁷`, `2.1e−7` at `10⁶`,
`2.3e−6` at `10⁵`; mean ≈ 2.4 × median and p99 ≈ 14 × median, so the null is `χ²₁`-shaped and
**p-values are the only summary permitted**.

### 6.1 The FULL-CHAIN examination, and the two things it changed

`glass_gate.py` examines the estimator on tables. `glass_calib.py` examines the **whole chain**
— real geometry, real template selection, real triple overlap, real pooling over
configurations — on **synthetic positions only**, and it changed the design twice. Both changes
are here because they were made **before** any real configuration was read.

**(1) It killed the naive floor.** See §4.1. Measured overlap penalty on synthetic
configurations: the true null median is **3.0–3.2 ×** the multinomial `1/(2N)` at 40–60
configurations, and **14 ×** at 20. The penalty is not a constant and must be measured per
reading, which is why the floor is drawn per (state point, template) rather than computed.

**(2) It found our error bar is CONSERVATIVE by a factor of ~2.2, and that cuts both ways.**
The verdict rests on *differences*, so the chain was examined on a difference: split one
synthetic ensemble at random in half — two draws from the *same* distribution — read the share
on each half, and score the difference against the configuration-level block bootstrap.

| template | `z_sd` | `z_mean` | 95 % coverage |
|---|---|---|---|
| `r = 1.07` | **0.43** | +0.03 | 1.00 |
| `r = 1.50` | **0.44** | +0.07 | 1.00 |
| `r = 3.00` | **0.54** | +0.01 | 0.98 |

An honest error bar gives `z_sd = 1`. Ours gives **0.43–0.54**: the block bootstrap on this
statistic **over-states the uncertainty by roughly 2.2 ×**, which is the known bad behaviour of
the bootstrap for a non-negative statistic sitting near its boundary at zero. **The consequence
is stated as a rule, now, before the run:**

* **A GROWTH claim is scored against the raw bootstrap `σ`** — the conservative one. A 5 σ bar
  is then effectively ~11 σ, and that is deliberate.
* **A NULL claim (outcome (b)) may NOT be scored against the raw bootstrap `σ`**, because an
  inflated `σ` makes "flat" too easy to declare. It is scored against an **exact permutation
  test on configuration membership**: pool the per-configuration tables of the two temperatures,
  reassign configurations at random to two groups of the original sizes, recompute `Δshare`
  2 000 times, and read the p-value off the rank. That test needs no error bar at all, and it is
  valid under the null of "same distribution at both temperatures" **provided the triple counts
  are matched** — which §3.7 already requires for an unrelated reason.

**And one candidate check was DISCARDED as vacuous rather than banked.** A
Kolmogorov–Smirnov test on leave-one-out p-values returned `KS = 0.000` against a critical
`0.124` — perfect uniformity — and that is a **tautology**: a leave-one-out p-value *is* a rank.
It is recorded here rather than quietly dropped. Its one real by-product is kept: the p-value
`glass_run.py` quotes is an **exact rank test** under exchangeability, not an asymptotic one.

---

## 7. OUTCOMES — every one of them, with its verdict fixed now

Scored on the **3D primary arm** at the nearest-neighbour equilateral template, floor-subtracted,
count-matched, with the 2D arm as replicate. `σ` throughout is the **configuration-level block
bootstrap** — the independent axis is *independent configurations*, never pooled triples
(`whole-only-null-autocorrelation`, `order3-probe-geometry`).

**(a) GROWTH.** Floor-subtracted share increases monotonically across the four-point 3D ladder;
the `T = 0.44` reading exceeds the `T = 0.64` reading by ≥ 5 σ; the excess over the §4.4
surrogate is ≥ 5 σ at `T = 0.44`; the 2D pair agrees **in sign**. Verdict: *compositional static
order not reconstructible from the species-resolved pair correlations grows on supercooling, in
these models, over this ladder.* Nothing more.

**(b) NULL — a fully acceptable and interesting result, reported as loudly as (a).** The
floor-subtracted share is flat across the ladder: the **exact configuration-permutation test of
§6.1(2)** on `T = 0.44` against `T = 0.64` returns `p > 0.05`, **and** the same test has been
shown able to detect a planted difference of the size that matters (without that leg the null is
*ungauged*, not clean — `GATES.md` reach 13). Note the scoring rule fixed in §6.1: a null may
**not** be declared against the raw bootstrap `σ`, because that `σ` is inflated ~2.2 × and would
make "flat" too easy to claim. Verdict: *over this ladder, in these models, in the
compositional channel, static whole-only order does not grow on supercooling* — which is
**evidence for the dynamical rather than the thermodynamic picture**, and is the outcome this
campaign would report with the same emphasis as a growth.

**(c) ANTI-GROWTH.** Share falls as `T` falls, by ≥ 5 σ. A result, reported as one.

**(d) NON-MONOTONE / INTERIOR PEAK.** Requires G-MIX and G-DOSE to be discharged before any
interpretation; undischarged, it is **ungauged**.

**(e) PINNED.** G-LP's headroom collapses (< 3 × the measured share) at the read templates. The
reading is a restatement of the pair marginals and is **not a measurement of three-way
structure**. Those cells are VOID and the campaign reports the pinning as its finding.

**(f) MANUFACTURED.** The binmint pedestal is ≥ 50 % of the reading. That rung is VOID.

**(g) UNGAUGED — the outcome-completeness entry, named because a campaign has already produced
it.** *"A large, well-controlled reading whose decomposition into signal and floor was not
performed."* Enumerated here as a **non-verdict**: if a big number arrives and its split between
signal, floor, pedestal and surrogate has not actually been computed, the outcome is **ungauged**
and it is reported as ungauged. It is not a detection, it is not a null, and it is not deferred
to a later document (`GATES.md` harvest: *outcome completeness*; the unblind that fit no
pre-registered outcome, `28fadbd`).

**(h) NOT RUN.** A pre-registered arm that did not complete — the 2D replicate, the 3×3×3
reading, the own-MD high-`T` liquid of §4.5, the secondary local-order-parameter design of
§3.2. Every one is listed by name in `GLASS_RESULTS.md` with the reason, and **no verdict is
scored on an arm that did not run**.

**(i) INSTRUMENT FOULED.** The far arm (§3.4) does not read inside its predicted floor band, or
the ideal-gas control (§4.3) reads above its floor. Then the pipeline is fouled and **every
reading it produced is ungauged**, including any that look good.

### 7.1 The advance predictions, staked before any reading

Support comes only from confirmed advance predictions (`epistemology.md` rule 6; the phi4
campaign's only rule-L6 support was a forward prediction). These are staked now:

| | prediction |
|---|---|
| **P1** | The **far arm** (`r ≥ 5`) reads at floor: below 3 × the p99 of its own matched floor. |
| **P2** | The share is **largest at the nearest-neighbour template** and decays with `r`. |
| **P3** | The **product control** reads floor at every template, and the **permutation** control differs from it by less than the smallest quoted reading. |
| **P4** | The **LP headroom ≥ 0.30 nats** at every read template (§5.1). |
| **P5** | The ordering across `T` at fixed template is **monotone**, not scattered. |
| **P6** | The **2D replicate agrees in sign** with the 3D trend. |
| **P7** | The **binmint pedestal < 30 %** of the reading at `Δ = 0.10`. |

A prediction that fails is reported as failing, in the scorecard, next to the ones that pass.

---

## 8. THE KILLS — staked first, and separable

Each kill takes down its own claim and **nothing beneath it**. In particular **none of them
touches** `wild-share`, the sky campaign, the rent clause, the valve, or any line of
`Stance.lean`.

**K1 — the campaign's own claim.** *If, at every template on the pre-registered grid and at the
lowest temperature in the set, the floor-subtracted share fails to exceed the §4.4 pair-matched
surrogate's share by more than 5 σ of the surrogate ensemble, then "amorphous order carries
whole-only compositional structure invisible to the species-resolved `g(r)`" is refuted, at a
sensitivity we measured rather than assumed.* Takes down that claim alone.

**K2 — the growth claim only.** *If the floor-subtracted share does not increase as `T` falls,
by ≥ 5 σ across the ladder, the growth hypothesis is dead.* A nonzero share at all temperatures
survives this kill; existence and growth are separate claims and die separately.

**K-VOID — the instrument.** *If the far arm does not read inside its predicted `1/(2N)` band on
the real configurations, the pipeline is fouled and every reading it produced is ungauged.* This
one fires on us, not on the glass.

**K-PIN.** *If the LP headroom at a read cell is below 3 × the measured share, that cell is VOID*
— the number was determined before three-way structure was consulted.

**K-MINT.** *If the binmint pedestal is ≥ 50 % of the reading at a rung, that rung is VOID.*

**K-DOSE.** *If the reading tracks the triple count rather than the temperature, the trend is
void.*

**K-DYE.** *If the §4.4 surrogate cannot detect a planted three-body coupling at the amplitude
that matters, every verdict resting on it is ungauged* — not clean, not a refutation.

---

## 9. THE REACH OF THE SEARCH BEHIND §1, AND WHAT IS NOT CLAIMED

**Reach.** The §1 credits come from a one-pass web and abstract survey run on 2026-07-27, plus
the primary-text check on Banerjee et al. (§1.2) via its full text. **No primary PDF was read
end to end.** The adjudications that RMPE is not our object (§1.1) and that `S_rel` is our
object (§1.4) rest on mathematical arguments made here, not on sentences somebody else wrote,
and both should be re-checked against primary text before either is quoted anywhere outside
this scratchpad. Fields not swept: materials science beyond metallic glasses, chemistry,
information geometry's own condensed-matter corner.

**Not claimed, and will not be claimed whatever the reading:**

1. **Nothing about experimental glasses.** Two simulated model liquids.
2. **Nothing about the glass transition itself.** The ladder stops at `T_MCT`.
3. **No priority.** §1 records five prior programmes on the same physical question; the most we
   may claim is a *different, non-negative* object and a sweep of it.
4. **No claim about geometric amorphous order.** §3.1's design reads the compositional channel
   only (§3.1, "the cost of this choice").
5. **No stance implication.** `wild-share` does not move; `Stance.lean` is not opened; no Lean
   file is edited; `lake` is not run; nothing is pushed.
6. **No claim that any reading is large in absolute terms.** `KAPPA_EDGE_RESULTS.md` measured
   that the degree-3 direction can hold ~1 % of the fine-grained structure; this is a small
   sector read precisely, not a dominant one.

---

## 10. FILES AND ORDER OF OPERATIONS

| stage | artifact | committed |
|---|---|---|
| 1 | `GLASS_DATA.md` — the inventory, no share computed | before this document |
| 2 | **this document** | **before any share on any real configuration** |
| 3 | `glass_run.py`, `glass_analyze.py`, `glass_surrogate.py` — the sweep and stage B | with, or before, stage 4 |
| 4 | `GLASS_RESULTS.md` — the sweep, the scorecard against §7.1, the verdict | last |

`glass_share.py` (the instrument), `glass_gate.py` (§6, nine checks on tables), `glass_calib.py`
(§6.1, the full-chain examination) and `glass_run.py` (the sweep driver) **already exist and are
committed with this document**, together with their synthetic-only outputs `glass_gate.json` and
`glass_calib.json`. **No real configuration has been read by any of them.** Primary seed
**20260727**. Research → scratchpad memo → Eric's review. Nothing pushed.
