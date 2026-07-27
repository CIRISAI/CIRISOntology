# WATER_PRIOR_ART — searched and adjudicated before the design was staked

**Stage 0 of the water campaign.** This document contains **no measurement on water of any
kind**. It exists because the house standard (`convergent-art-pattern`) is *assume the result is
already in print until the primary text says otherwise, and search by the mathematical object,
never by our vocabulary* — and because the water community has had a **three-body order
parameter** since 1998 and has been computing **entropy-beyond-pairs for water** since 2003. Both
were found by searching; neither was known to this repository before today.

**SCOPE, stated first and repeated in every document of this campaign.** The target is
**simulated water models** — TIP4P/2005, ST2, mW — **not experimental water**. Any outcome is a
contribution to a contested question (does water have a liquid–liquid critical point?), **not a
resolution of it**. **Nothing here bears on `wild-share`**, on `adequacy`, or on any claim about
nature at large, and **nothing here moves `Stance.lean`**. No Lean file is opened, `lake` is not
run, the audit is not run, nothing is pushed.

---

## 0. THE ADJUDICATION, up front

| # | prior programme | verdict |
|---|---|---|
| 1 | **Chau & Hardwick (1998) / Errington & Debenedetti (2001)** — the tetrahedral order parameter `q`, built from **angles between triplets** of first-shell oxygens, used to organise water's anomalies into an "order map" | **CONVERGENT-ADJACENT.** Same physical question, same three-body geometry. Theirs is a **chosen coordinate**; ours is the **whole gap** over all pair-matching distributions. The difference is exact and checkable (§1.1) |
| 2 | **Saija, Saitta & Giaquinta (2003)** — the **Residual Multiparticle Entropy** `Δs = s_ex − s_2` computed for **TIP4P water**, `T = 230–350 K` at **ambient pressure**, with the zero-RMPE crossing near the temperature of maximum density | **CONVERGENT-ADJACENT, and the closest hit.** Entropy-beyond-pairs, on a water model, swept in temperature, twenty-three years ago. `s_2` is a **series truncation**, ours is a **maxent gap**; RMPE **goes negative**, ours **cannot** (§1.2) |
| 3 | **Esposito, Saija, Saitta & Giaquinta (2006)** — the **pair** entropy of TIP4P water resolved into translational and orientational parts, used to give a *structurally unbiased* definition of low- and high-density water | **CONVERGENT-ADJACENT.** It decomposes `s_2`; it does not compute the residual. But "define LDL and HDL from an entropy rather than from a chosen coordinate" is *our* framing, in print, in 2006 (§1.2) |
| 4 | **M. S. Shell (2008)**, `S_rel`, and the whole coarse-graining / IBI industry | **OUR OBJECT, computed daily, as a fitting loss.** Carried verbatim from the glass credit block, and it bites harder here: the failure of pair potentials to represent water *is* a qualitative measurement of a nonzero share (§1.4) |
| 5 | **Torquato & Stillinger (2003)** — `g₂`-invariant point processes | **OUR NICHE STATED AS A THEOREM, by someone else, in 2003.** Carried verbatim (§1.5) |
| 6 | **The two-state / Ising mapping of the LLCP** (Holten & Anisimov; Russo & Tanaka; the three-state models) — the order parameter is the fraction of locally favoured tetrahedral structures | **NOT prior art on our object — a THREAT to our design.** If our binary label is a good Ising-order-parameter proxy, `Core/SignSymmetry.lean` sends the share toward **exactly zero** at the critical point. This is the single most important thing this survey found and it reshapes the forward prediction (§2) |
| 7 | **A pairwise-blind, non-negative maximum-entropy gap on three discrete slots, traced across water's supercooled region** | **CLEAR, as far as this search reaches** (§4 states the reach). And the narrowing owed to the registry is paid in §1.3 |

**The one-line summary.** The object is not new to information theory (Schneidman et al. 2003),
the question is not new to water (Chau & Hardwick 1998; Errington & Debenedetti 2001), and
entropy-beyond-pairs is not new to water (Saija et al. 2003). What is not in print, as far as
this search reaches, is **the non-negative maxent gap, on water, across the Widom line**. That
is the campaign, and it is a narrow claim.

---

## 1. THE CREDIT BLOCK — mandatory before any number in this campaign

### 1.1 The water community already has a three-body order parameter

**P.-L. Chau & A. J. Hardwick, *Mol. Phys.* 93:511–518 (1998)**, "A new order parameter for
tetrahedral configurations", introduces an order parameter built from the distribution of
**angles `φ_jk` between triplets** of first-shell oxygen neighbours centred on a given molecule.
**J. R. Errington & P. G. Debenedetti, *Nature* 409:318 (2001)**, "Relationship between
structural order and the anomalies of liquid water", use the normalised form

> `q = 1 − (3/8) Σ_{j<k} ( cos φ_jk + 1/3 )²`

together with a translational order parameter `t`, to build water's **order map** and to bound
the *structurally anomalous region* — the region in which both orientational and translational
order **decrease** on compression, which is exactly where water's anomalies live. Anyone reading
this campaign should read that paper first; the physical question is theirs and the priority is
theirs.

**How our object differs, stated exactly and checkably, before any result.** Three ways:

1. **A coordinate versus a supremum.** `q` is one scalar function of the angles — a *chosen
   projection*. Our share is `S(Q) − S(P)` with `Q` the maximum-entropy distribution over the
   set of **all** distributions carrying `P`'s three pair marginals. It is a supremum over a
   convex set, not a projection onto a direction. A coordinate is blind to whatever it does not
   project onto; a supremum is not.
2. **The reference state.** `q` is normalised so that it reads **0 for the ideal gas** and 1 for
   a perfect tetrahedron. So a **pair-potential liquid with no three-body physics whatsoever has
   `q ≠ 0`** — hard spheres have angular structure. Our share is **zero exactly when `P` is
   reconstructible from its own pair marginals**, so the pair-potential liquid's contribution is
   subtracted by construction rather than by argument. This is the whole difference between
   "contrast against no structure" and "contrast against no structure *beyond pairs*".
3. **Sign.** `q` is a mean of a bounded quantity and moves in either direction. `share ≥ 0`
   always, identically, with no condition, because `Q` maximises entropy over a set that
   *contains* `P`.

**This is our sharpest claim to a distinct object, and it is stated here, before the design,
rather than argued after a result.**

Also in this neighbourhood and credited: **"A tetrahedral entropy for water", PNAS 106:22130
(2009)** *(title and journal verified; authors not verified in this session)*; **Russo & Tanaka,
"Understanding water's anomalies with locally favoured structures", *Nat. Commun.* 5:3556
(2014)**, whose `ζ` is a two-state local structural parameter; and the local-structure-index /
`d₅` family, which are the field's standard continuous two-state coordinates.

### 1.2 Entropy-beyond-pairs has been computed for water twice, in 2003 and 2006

The multiparticle correlation expansion of the entropy — `s_ex = s_2 + s_3 + …`; **Green (1952)**;
**Nettleton & Green, JCP 29:1365 (1958)**; made computable from simulation by **Baranyai & Evans,
*Phys. Rev. A* 40:3817 (1989)** — with the remainder

> `Δs = s_ex − s_2`, the **Residual Multiparticle Entropy**, **Giaquinta & Giunta, *Physica A*
> 187:145 (1992)**

has been applied to water twice by the same group:

* **F. Saija, A. M. Saitta & P. V. Giaquinta, JCP 119:3587 (2003)**, "Statistical entropy and
  density maximum anomaly in liquid water": RMPE for the **TIP4P** model, **`T = 230–350 K` at
  ambient pressure**, finding the **zero-RMPE ordering threshold close to the temperature of
  maximum density**.
* **R. Esposito, F. Saija, A. M. Saitta & P. V. Giaquinta, *Phys. Rev. E* 73:040502(R) (2006)**,
  "Entropy-based measure of structural order in water": the **pair** entropy of TIP4P water
  resolved into **translational and orientational** components, giving *"a structurally unbiased
  definition of low-density and high-density water"* and mapping the anomalous region where both
  orders are disrupted by compression.

**Not our object, and the tell is exact.** `s_2` is a **truncation of an infinite series**, not
the entropy of the pair-maxent distribution; `Δs` **can and does go negative**, and our share
**cannot**. Two different objects answering the same physical question. The generality of the
zero-RMPE criterion is itself disputed — **Krekelberg, Mittal, Ganesan & Truskett, JCP
128:161101 (2008)**, with **Giaquinta's comment, JCP 130:037101 (2009)** — and that dispute is
carried, not hidden.

### 1.3 The narrowing this campaign owes its own survey, paid before the first number

`TARGET_REGISTRY.md` §3.1 and `GLASS_PREREG.md` §1.2 already recorded that the RMPE family had
been traced across temperature on the Kob–Andersen glass former. The same correction is owed
here and is larger:

> **The RMPE family has been traced across temperature on a water model, at ambient pressure,
> since 2003 (Saija et al.), and the pair-entropy decomposition has been used to define LDL and
> HDL since 2006 (Esposito et al.).**

What survives, and all this campaign may claim:

> **A non-negative, pairwise-blind maximum-entropy gap has not, as far as this search reaches,
> been computed on water at all — and no entropy-beyond-pairs quantity of any family has been
> traced across the Widom line or into the liquid–liquid critical region.** Saija et al. (2003)
> is ambient pressure only and stops at 230 K; Esposito et al. (2006) computes the pair
> decomposition, not the residual.

The second half of that sentence is the campaign's actual niche, and it is a **pressure** claim
as much as an object claim. §4 states how far the search behind it reaches.

### 1.4 M. S. Shell — our share, computed routinely, as a fitting loss; and water is its hardest case

**M. S. Shell, JCP 129:144108 (2008)**, "The relative entropy is fundamental to multiscale and
inverse thermodynamic problems." By the Pythagorean identity for exponential families,
`min_q D(p‖q)` over a pair-potential family **equals** `S(Q) − S(p)` with `Q` carrying `p`'s pair
correlations — **exactly our share**, computed every day in the coarse-graining literature under
the name `S_rel`, as an objective to be minimised.

**And water is the canonical failure case of that programme.** A pair potential fitted to water's
`g_OO(r)` reproduces the pair structure and fails on the angular structure and on the
thermodynamics — the *representability problem*. That failure **is** a qualitative statement that
water's share is large, made by a different community, for a different purpose, decades ago. Our
contribution can only be to **measure** it on a defined three-slot object and **trace** it, never
to discover it. Relatedly: **Reverse Monte Carlo** (**McGreevy & Pusztai, *Mol. Simul.* 1:359
(1988)**) is the community's pair-matched generator and is the same construction we need for a
null.

### 1.5 Torquato & Stillinger — our niche stated as a theorem, in 2003

**Torquato & Stillinger, *Phys. Rev. E* 68:041113 (2003)**, "Local density fluctuations,
hyperuniformity, and order metrics", constructs **`g₂`-invariant processes**: explicitly
different point processes sharing an identical pair correlation function. That the pair
correlation function does not determine a configuration is not a discovery available to this
campaign; it is a theorem somebody else proved twenty-three years ago.

### 1.6 Three-body physics in water is already known to be load-bearing

* **Molinero & Moore, JPCB 113:4008 (2009)** — the **mW** model: water as a monatomic
  Stillinger–Weber particle with an explicit **three-body** term, `λ = 23.15` the tetrahedrality
  parameter. The existence of a *dial* on three-body strength is what makes this campaign's dose
  gate possible at all, and the dial is theirs.
* **Molinero, Sastry & Angell, PRL 97:075701 (2006)** — sweeping `λ` in the Stillinger–Weber
  silicon potential (arXiv:cond-mat/0510292); **"Water-like anomalies as a function of
  tetrahedrality", PNAS (2018), doi:10.1073/pnas.1722339115** — the same sweep against water's
  anomalies *(doi verified; authors, volume and page not verified in this session)*. **A `λ`
  sweep is not our idea and is not new**; what is ours is reading the pairwise-blind share along
  it.
* **"Low-order many-body interactions determine the local structure of liquid water" (2019)**
  *(title verified; authors and journal not verified in this session — it is from the MB-pol /
  many-body-expansion programme)* — two-body plus three-body suffices for water's local
  structure. This is the strongest published reason to expect the order-3 sector to be physically
  load-bearing in water, and it is somebody else's result.
* **Coslovich, JCP 138:12A539 (2013)** — static triplet correlations `S⁽³⁾` in the Kob–Andersen
  mixture (carried from `GLASS_PREREG.md` §1.5 because this campaign's baseline arm uses that
  model). `Core/SignSymmetry.lean`'s recorded trap applies verbatim: **a large three-point
  correlator is not order-3 structure** — a pairwise Hamiltonian with a field reaches
  `⟨s₁s₂s₃⟩ ≈ 0.91` at a share of order `1e−14`.

### 1.7 The LLCP hypothesis and its dispute — cited honestly, on both sides

**The hypothesis.** **Poole, Sciortino, Essmann & Stanley, *Nature* 360:324 (1992)**, "Phase
behaviour of metastable water" — a second critical point terminating a first-order transition
between a low-density and a high-density liquid, in the deeply supercooled region.

**Evidence in models.**
* **ST2**: **Palmer, Martelli, Liu, Car, Panagiotopoulos & Debenedetti, *Nature* 510:385 (2014)**;
  critical point located by **Liu, Palmer, Debenedetti & Panagiotopoulos, JCP 137:214505 (2012)**
  at **`T = 237 ± 4 K`, `ρ = 0.99 ± 0.02 g/cm³`, `P = 167 ± 24 MPa`** with Ewald electrostatics
  (earlier reaction-field estimates give `≈ 247 K, 186 MPa`).
* **TIP4P/2005 and TIP4P/Ice**: **Debenedetti, Sciortino & Zerze, *Science* 369:289 (2020)**,
  "Second critical point in two realistic models of water" — `T_c ≈ 172 K`, `P_c ≈ 1861 bar` for
  TIP4P/2005. Earlier: **Abascal & Vega, JCP 133:234502 (2010)**, "Widom line and the
  liquid–liquid critical point for the TIP4P/2005 water model" — `T_c = 193 K`, `P_c = 1350 bar`,
  `ρ_c = 1.012 g/cm³`, and **the Widom line as the locus of compressibility maxima**, which is
  the path this campaign will walk.
* **E3B3** (a water model with an explicit **three-body** term): *"Evidence for a liquid-liquid
  critical point in supercooled water within the E3B3 model…"*, **JCP 144:214501 (2016)**
  *(title and journal reference verified; authors not verified in this session)* — LLCP estimated
  at `≈ 180 K, 2.1 kbar`. Named here because a model whose *defining feature* is a three-body
  term is the natural second atomistic arm if this campaign ever gets one.

**The dispute, cited because it is not settled.** **Limmer & Chandler, JCP 135:134503 (2011)** and
**JCP 138:214504 (2013)**, "The putative liquid–liquid transition is a liquid–solid transition in
atomistic models of water" I and II, argue that the apparent transition in ST2 and mW is a
liquid–crystal transition made to look like a liquid–liquid one by a separation of timescales.
The reply is **Palmer et al. (2014)** above and **Palmer, Haji-Akbari, Singh, Martelli, Car,
Panagiotopoulos & Debenedetti, "Comment on …", JCP 148:137101 (2018)**, which states plainly that
the **origin of the disagreement remains unresolved**. **Holten, Limmer, Molinero & Anisimov, JCP
138:174501 (2013)** fit mW to two-state thermodynamics and place its critical point at negative
pressure, i.e. **mW has no accessible LLCP** — which is why mW is this campaign's *dose* arm and
never its *criticality* arm. Experimental claims exist (**Kim et al., *Science* 370:978 (2020)**)
and are themselves contested, and **"Constraints on the location of the liquid–liquid critical
point in water", *Nature Physics* (2024)** narrows the experimental window.

**This campaign takes no side in that dispute and cannot settle it.** It reads a structural
quantity along a path. If the LLCP does not exist, the Widom line is still a real locus of
maximum response and the prediction below is still testable against it.

### 1.8 The instrument's own ancestry, carried

* **Connected information of order 3**, the measure itself: **Schneidman, Still, Berry & Bialek,
  PRL 91:238701 (2003)**; **Amari, IEEE TIT 47:1701 (2001)**.
* **Coarse-graining creates connected information**: **Kahle, Olbrich, Jost & Ay, PRE 79:026201
  (2009)** — the reason the binmint gate exists, and it is *more* load-bearing here than in the
  glass campaign (§3).
* **Copula invariance** of rank-based readings: **Sklar (1959)**; **Scherrer, Berlind, Mao &
  McBride, ApJL 708:L9 (2010)**.
* The `log 2` denominator and its per-orientation refinement: `CIRISOntology/Core/ThirdCap.lean`
  (`share_le_log_two`, `share_le_grouping_gaps`). The underlying mathematics is textbook (Cover &
  Thomas, grouping subadditivity and the Gibbs bound); ours is the mechanization.

---

## 2. WHAT THE SURVEY FOUND THAT CHANGES THE DESIGN — the two-state/Ising mapping is a THREAT

This is the most consequential finding of the survey and it is recorded here, before the
pre-registration, because it inverts the naive forward prediction.

**The field's own reading of the LLCP** is that the order parameter is the **fraction of locally
favoured tetrahedral structures**, and that the criticality is **3D-Ising** — the two-state
(Holten–Anisimov) and three-state models, and the 2023 JPCB analysis of TIP4P/2005, all say so.
So water's LLCP is, to the extent the mapping holds, an Ising critical point in a binary local
structural label.

**And `Core/SignSymmetry.lean`'s `share_eq_zero_of_signSymmetric` proves that a three-bit state
invariant under the global flip has whole-only share EXACTLY ZERO.** The repository's own memory
of this is blunt: *do not hunt order-3 in Ising-family models.* The 2D Ising ridge and the 3D
`φ⁴` confirmation both found their ridge **only under weak symmetry breaking**: at `h = 0` the
reading is a theorem's exact zero, and the measured ridge peaks at `u = h·L^{y_h} ≈ 1.1–1.2`,
i.e. at **small but nonzero field**, decaying as `L^{−6β/ν}`.

**The Widom line is the `h = 0` line.** It is defined as the extension of the coexistence line
above `T_c`, which is exactly the locus of vanishing ordering field. So a naive stake of "the
share peaks at the Widom line" is, on the repository's own theorem plus its own two measured
ridges, **the wrong sign of prediction** for a pure Ising order-parameter label.

**Why the theorem nevertheless does not simply kill the campaign**, and this is the substantive
judgement: our label is **not** the Ising order parameter. First-shell coordination number is a
physical observable that mixes the ordering field with the non-ordering (energy-like) one, and
**LDL and HDL are not related by any symmetry** — unlike up and down spins. So the three-slot
state is generically **not** flip-symmetric and the theorem does not apply. What the theorem does
say is that **to the extent the label is a good order-parameter proxy and the state is near
flip-symmetric, the share is suppressed**, and suppressed *most* exactly on the Widom line.

**The consequence, which becomes the campaign's sharpest and most distinctive advance
prediction:** along an **isotherm crossing the Widom line in pressure** — the exact analogue of
sweeping `h` through zero at fixed `T > T_c` — the repository's own measured ridge shape predicts
a **DOUBLE peak with a dip at the crossing**, not a single peak. Nobody else would predict that,
it follows from a machine-checked theorem plus two confirmed measurements, and it is
distinguishable from the single-peak alternative in one plot. It is staked in `WATER_PREREG.md`
§4, together with the single-peak alternative and the meaning of each.

---

## 3. THE DESIGN PROBLEM THIS SURVEY EXPOSES — water has no atomic alphabet

Stated here because it is a *finding about the target*, not a design choice, and because it must
not be discovered later.

`GLASS_PREREG.md` §3.1 chose **species** as its slot label and gave five reasons, of which the
first was decisive: *the alphabet is atomic, so the most dangerous minting channel — binarization
of a continuum — is absent by construction rather than bounded by a sweep.* It explicitly
**rejected** the local-order-parameter design (§3.2) as primary, because a local order parameter
is a **filter over a neighbourhood** and the composition `pointwise map, then filter` is what
manufactured **66 σ** of share from nothing in the sky pilot.

**Water is one component. There is no species channel. The atomic alphabet does not exist.**

So this campaign is forced into the design the glass campaign rejected, and the honest
consequence is that **the binmint / filter battery is not optional here, it is the campaign's
primary risk**, and the ideal-gas control (a structureless point pattern through the
byte-identical pipeline) stops being a formality and becomes the load-bearing gate. The best
available mitigation — pre-registered — is to choose a label whose alphabet is **integer-valued
with an integer threshold**, so that no continuum is binned even though a neighbourhood is still
filtered: **first-shell coordination number, thresholded at `n ≥ 5`**, which is also the
interstitial/two-state distinction the field itself uses. That is a mitigation, not a removal,
and it is reported as such.

---

## 4. THE REACH OF THIS SEARCH, AND WHAT IS NOT CLAIMED

**Reach.** A one-pass web and abstract survey run on **2026-07-27**, plus abstract-level checks on
Esposito et al. (2006) and Chau & Hardwick (1998). **No primary PDF was read end to end**; the
attempt on `arXiv:cond-mat/0603764` returned an unparseable binary and only the abstract was
obtained. **The search was cut short by a weekly web-search quota**, and three intended queries
were not run: (i) triplet correlation functions in liquid water as a primary literature
(Dhabal/Chakravarty and successors are named from memory of the field and **have not been
verified in this session** — treat those as unchecked); (ii) whether any group has computed a
maxent-based order-3 quantity on molecular liquids under a name not searched here; (iii) public
supercooled-water **trajectory** repositories beyond the one checked in §5. **Fields not swept:**
chemical physics beyond the water/tetrahedral-liquid corner, the machine-learned-potential
literature, and the neutron/X-ray scattering three-body-correlation literature. A null from a
survey is weaker than a null from an experiment, and "not found" is not "does not exist".

**The adjudications in §1.1 (Chau–Hardwick/Errington–Debenedetti is a coordinate, not a
supremum), §1.2 (RMPE is a truncation, not a maxent gap) and §1.4 (`S_rel` IS our object) rest on
mathematical arguments made here, not on sentences somebody else wrote**, and every one should be
re-checked against primary text before any of it is quoted outside this scratchpad.

**Not claimed, and will not be claimed whatever the reading:**

1. **Nothing about experimental water.** Simulated models only.
2. **No resolution of the LLCP question.** A contested question gets a contribution.
3. **No priority.** §1 records six prior programmes on the same physical question; the most this
   campaign may claim is a *different, non-negative* object and a sweep of it across a path
   nobody has swept it across.
4. **No claim that three-body physics in water is a discovery.** §1.6 records that the field
   already knows it, from mW to MB-pol.
5. **No stance implication.** `wild-share` does not move; `Stance.lean` is not opened.

---

## 5. DATA REACHABILITY — checked, and the answer is mostly NO

| source | checked | verdict |
|---|---|---|
| **Zenodo 3836542**, "Data for *Second Critical Point in Two Realistic Models of Water*" (Debenedetti, Sciortino & Zerze), CC-BY-4.0 | file listing read | **NO CONFIGURATIONS.** Six files, 1.2 GB total: `e-rho-*.tgz` are **scalar time series** (potential energy, density), `sk-data.tgz` is structure factors, `mdp-gro-top-*.tgz` and `large-systems.tgz` are **GROMACS input files**. **There are no trajectories and no coordinate sets.** The definitive public dataset for the TIP4P/2005 LLCP cannot supply this campaign's configurations |
| **GlassBench** (Zenodo 10118191) | already on disk from the glass campaign | Kob–Andersen configurations, **in hand**. This is the campaign's pair-potential baseline arm and it costs nothing |
| MD engines on this box | `which`, `apt-cache policy`, `pip index` | **None installed.** `openmm 8.5.2` and `lammps 2025.7.22.4.0` are pip-installable into the venv without root; `gromacs 2023.3` and `lammps 20240207` are in Ubuntu `universe` but need root. Installability was verified **from the package index only; nothing was installed** |

**Consequence, stated plainly: every water configuration this campaign reads must be generated by
us.** That is a cost, it is priced in `WATER_PREREG.md` §7, and it is the reason that document
declares parts of the campaign **not feasible on this box** rather than promising them.

---

## 6. FILES

| | |
|---|---|
| `water_feasibility.py` | the stage-0 arithmetic: triple counts, floor ladder, `ThirdCap` ceilings and occupancy on **synthetic** bracketing point patterns. **Reads no water.** |
| `water_feas_hdl.json`, `water_feas_hdl_t25.json`, `water_feas_ldl_t25.json`, `water_feas_hdl_s20.json` | its outputs, synthetic only |
| `WATER_PREREG.md` | the pre-registration, committed before any water configuration exists |

Primary seed **20260727**.
