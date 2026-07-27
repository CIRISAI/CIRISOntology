# PRE-REGISTRATION — the whole-only order-3 reading of supercooled water, across the Widom line

**Committed before any water configuration exists.** No water has been simulated, downloaded or
read by this campaign. The only numbers in this document come from `water_feasibility.py`, which
runs on **synthetic bracketing point patterns** and reads no water (§6); its outputs decided the
templates, the system size, the configuration count and — most consequentially — **which parts of
this campaign are declared infeasible on this box before anything was attempted** (§7).

**SCOPE, stated first and repeated in every document of this campaign.** The target is
**simulated water models** — TIP4P/2005 and mW — **not experimental water**. This is a
contribution to a contested question, **not a resolution of it**: whether water has a
liquid–liquid critical point has been argued since 1992 and is not settled (Poole et al. 1992;
Palmer et al. 2014; Debenedetti, Sciortino & Zerze 2020; against: Limmer & Chandler 2011, 2013;
the disagreement declared unresolved in Palmer et al. 2018). **Nothing here bears on
`wild-share`**, on `adequacy`, or on any claim about nature at large, and **nothing here moves
`Stance.lean`**. No Lean file is opened, `lake` is not run, the audit is not run, nothing is
pushed.

**The credit block is `WATER_PRIOR_ART.md` and it is part of this pre-registration by
reference.** Its §1 is mandatory before any number: the water community has had a **three-body
order parameter** since Chau & Hardwick (1998) and Errington & Debenedetti (2001), and
**entropy-beyond-pairs on a water model** since Saija, Saitta & Giaquinta (2003). Neither is our
object and the differences are stated there exactly, before the design, rather than argued after
a result.

---

## 1. WHY WATER, AND WHY IT IS A SHARPER TARGET THAN A GLASS FORMER

Simple liquids are well described by **pair** potentials. Water is not: hydrogen bonding is
**directional**, and the physics that makes water water is effectively **three-body** — which is
precisely the sector this instrument measures and precisely the sector a pair description
provably cannot reach (Torquato & Stillinger 2003's `g₂`-invariant processes). Water is therefore
the archetypal system in which our quantity should be **physically load-bearing rather than
incidental**.

Two independent confirmations of that from outside this repository: the **mW** model reproduces
water's structure and anomalies with a monatomic particle carrying nothing but a two-body and a
**three-body** term (Molinero & Moore 2009), and the many-body-expansion programme finds that
**two-body plus three-body determines water's local structure** (`WATER_PRIOR_ART.md` §1.6).

The concurrent glass campaign reads a system whose interactions are pairwise by construction
(Kob–Andersen is a binary Lennard-Jones mixture). If the instrument reads anything there, it is
reading structure that a pair *potential* generated. Here it can read structure a pair potential
**cannot** generate. That is the whole reason for this campaign, and it is also the reason the
Kob–Andersen baseline (§5.3) is the required deflation control rather than an afterthought.

---

## 2. THE DESIGN PROBLEM, ADMITTED FIRST: water has no atomic alphabet

`GLASS_PREREG.md` §3.1 chose **species** as its slot label, and its first and decisive reason was
that *the alphabet is atomic, so the binarization-minting channel is absent by construction
rather than bounded by a sweep*. It explicitly **rejected** the local-order-parameter design
(§3.2) as primary, because a local order parameter is a **filter over a neighbourhood** and the
composition `pointwise map, then filter` manufactured **66 σ** of share from nothing in the sky
pilot.

**Water is one component. There is no species. The atomic alphabet does not exist.**

So this campaign is forced into the design the glass campaign rejected. The consequence is stated
now, not later:

> **The binmint / filter battery (§5.2, §5.5) is not a formality in this campaign — it is the
> campaign's primary risk, and the pair-matched point-process null (§5.3) is load-bearing rather
> than confirmatory.** A verdict reached without both discharged is **ungauged**, not clean.

The mitigation, chosen and priced, is to pick a label whose alphabet is **integer-valued with an
integer threshold**, so no continuum is binned even though a neighbourhood is still filtered.

### 2.1 The slots, exactly

> **Three oxygen atoms whose three mutual O–O separations all lie in pre-registered shells. Each
> slot carries that oxygen's own FIRST-SHELL COORDINATION NUMBER, thresholded at an integer:
> `n ≤ 4 → 0` ("LDL-like"), `n ≥ 5 → 1` ("HDL-like"). Nothing else.**

* `n` is the count of oxygens within `r_cut` of the given oxygen, minimum image. `r_cut = 3.50 Å`
  is the **first minimum of `g_OO`** and is the primary; the ladder `r_cut ∈ {3.3, 3.4, 3.5, 3.6,
  3.7}` is run and reported. `g_OO` is a **pair** quantity this instrument is blind to by
  construction, so fixing `r_cut` from it is legitimate and is declared.
* The threshold `n ≥ 5` is **the interstitial**: it is the field's own two-state distinction
  (a fifth neighbour intruding into the tetrahedral cage is what makes HDL high-density), it is
  an integer, and it is **not** chosen from our own data. It is fixed here and never moved.
* Only oxygens are used. Hydrogens are not read, so the reading is invariant under every
  molecular reorientation that leaves the oxygen sublattice fixed. This is a deliberate loss of
  reach, stated in §9.
* Triples are enumerated in every order the template's own symmetry allows (the three molecules
  are not physically distinguishable, so the reading must not depend on which was called slot 1).
* The estimator is `share_2x2x2` from `glass_share.py`: **exact**, one-dimensional fibre,
  bisection to machine precision. **No IPF anywhere** (`ipf-sharek-boundary-drift`).

### 2.2 The designs NOT chosen

* **`q_tet` or `d₅` or LSI, binarized at the median.** Rejected as primary, retained as a named
  secondary (§8h). These are the field's own coordinates and would be the recognisable choice,
  but each is a **continuum** filtered over a neighbourhood and then binned — the binmint channel
  wide open on top of the filter. If run, they carry the full binmint battery and are reported
  second.
* **Hydrogen-bond count.** Integer, and physically the right object — but every H-bond definition
  is a threshold on a *pair* of continua (distance and angle), so the design would import two
  arbitrary cuts instead of one. Named, not chosen.
* **Coarse-grained density in three cells.** Rejected for the same reason the glass campaign
  rejected it: near-Gaussian local density under a median split is near flip-symmetric, hence
  near a theorem-zero by `Core/SignSymmetry.lean`, with the minting channel unbounded.

---

## 3. THE TEMPLATES — fixed by arithmetic, before any water

Stage 0 (`water_feasibility.py`, §6) enumerated five candidate templates on two synthetic
bracketing point patterns and **the occupancy gate decided the ladder**. In Å:

Ordered triples per particle, at the matched tolerance `Δ = 0.25 Å`. The **LDL→HDL** column is
the like-for-like bracket at one thermal width (`σ = 0.35 Å`); the last column is the same HDL
proxy at a **realistic** width (`σ = 0.20 Å`, closer to `g_OO`'s actual first-peak width), which
is where the occupancy failures appear.

| template | `(r₁₂, r₁₃, r₂₃)` | LDL → HDL | at `σ = 0.20` | min cell (all runs) | verdict |
|---|---|---|---|---|---|
| **tetrahedral** | `(2.80, 2.80, 4.573)` | **0.89 → 1.03** | **3.47** | 66 – 4768 | **PRIMARY** |
| second shell | `(2.80, 4.573, 4.573)` | 0.83 → 0.92 | 0.50 | 50 – 5044 | secondary |
| equilateral nn | `(2.80, 2.80, 2.80)` | **0.0017 → 0.26** (a **164 ×** count swing) | 0.65 | **0** | **EXCLUDED as primary by G-OCC** |
| interstitial | `(2.80, 3.20, 3.20)` | **0.0070 → 0.25** (**40 ×**) | 0.47 | **0** | **EXCLUDED as primary by G-OCC** |
| **far null** | `(7.00, 7.00, 7.00)` | 0.73 → 2.80 | 6.00 | 84 – 9294 | **PLUMB LINE** (P4) |

`4.573 Å = 2 × 2.80 × sin(109.47°/2)` is the **third side of the ideal tetrahedral triangle**,
computed from the tetrahedral angle and `g_OO`'s first peak, both fixed before any run. It is not
a fitted number.

**The exclusion is a finding, not a convenience, and it is recorded before any water exists.**
The equilateral nearest-neighbour triangle is **geometrically forbidden in a tetrahedral
network** — 60° against 109.47° — so it exists only where interstitials do. Its triple count
swings by a factor **164** between the two bracketing proxies and its eight-cell table goes
**empty** at a realistic thermal width. Three consequences:

1. It **cannot** be a primary template: G-OCC (§5.4) fires on it in advance, exactly as the b=16
   ladder was excluded in advance at `8b0c108`.
2. It is nonetheless the template whose **count itself** tracks the LDL/HDL balance most
   strongly, which makes it the campaign's sharpest **count-confound** warning: selecting triples
   by a geometric template is a **selection on the configuration**, and at this template the
   selection *is* the order parameter. Any reading there is a reading on a conditioned
   subensemble and would be reported as such.
3. **A gate-interaction finding, recorded because it would otherwise be read the wrong way
   round.** On the LDL proxy this excluded template returns the *widest* LP headroom in the whole
   stage-0 run — **0.6555 nats**, three times the primary template's best — on a table holding
   **three triples per configuration**. **A wide headroom on a starved table is not a pass.**
   G-OCC is therefore checked **before** G-LP at every cell, and a headroom reading on a cell that
   failed occupancy is not reported as a gate discharge.

**Tolerance ladder** `Δ ∈ {0.15, 0.20, 0.25, 0.30} Å` on every shell; **`Δ = 0.25 Å` is
primary** (≈ 9 % of the O–O bond, matching the glass campaign's 10 % in its own units).

---

## 4. THE FORWARD PREDICTION — staked before any number, and it is NOT the obvious one

Support comes only from confirmed advance predictions (`epistemology.md` rule 6). This section is
the point of the campaign.

### 4.1 What the repository has already measured, twice

The pairwise-blind share **peaks at criticality under weak symmetry breaking**:

* the **2D Ising ridge** (`CFT_RIDGE_RESULTS.md`) — critical ridge at ceiling fraction 0.66 %;
* the **3D `φ⁴` confirmation** (`PHI4_RIDGE_RESULTS.md`) — which **staked in advance**
  `d ln I_C^(3) / d ln L = −6β/ν = −3.109` and **measured `−3.084 ± 0.219`**, the campaign's only
  rule-L6 support.

Both found the ridge at **`u = h·L^{y_h} ≈ 1.1–1.2`, i.e. at small but NONZERO ordering field**,
and both read a theorem's exact zero at `h = 0` (`Core/SignSymmetry.lean`,
`share_eq_zero_of_signSymmetric`).

### 4.2 The LLCP, if it exists, is 3D-Ising in a binary local-structure label

The field's own reading: the order parameter is the **fraction of locally favoured tetrahedral
structures**, and the criticality is **3D-Ising** — the two-state and three-state models of
TIP4P/2005 (`WATER_PRIOR_ART.md` §1.7). **The Widom line is the `h = 0` line**: it is the
extension of the coexistence line above `T_c`, i.e. the locus of vanishing ordering field.

### 4.3 Therefore the naive stake is the WRONG SIGN, and the right stake is a double peak

Composing §4.1 and §4.2: a *pure* Ising-order-parameter label would be **suppressed** on the
Widom line, not enhanced. Our label is not the pure order parameter — first-shell coordination
mixes the ordering and non-ordering fields, and LDL/HDL are **not** related by any symmetry, so
the theorem does not apply and the share does not vanish. But its **shadow** does fall exactly on
the crossing. So:

> **P1 — THE HEADLINE STAKE. Along an ISOTHERM crossing the Widom line in pressure (the exact
> analogue of sweeping `h` through zero at fixed `T > T_c`), the floor-subtracted share shows a
> DOUBLE peak straddling the crossing, with a local MINIMUM at the crossing itself.**
>
> Scored: two interior maxima at `P₋ < P_W < P₊`, each ≥ 5 σ above the local minimum at `P_W`,
> where `P_W` is the compressibility maximum located from the **same runs** before any share is
> read.

> **P2 — the single-peak alternative, staked as a distinguishable competitor, not a hedge.** A
> single interior maximum within `|P − P_W| ≤ 100 bar`, with no dip. Verdict if P2 and not P1:
> *the coordination label is NOT behaving as an Ising order-parameter proxy, and the reading is
> tracking the response-function maximum rather than the ordering field.* That is a result and it
> is reported as one.

> **P3 — the distance-to-criticality ladder.** The peak-to-dip contrast of P1 (or the peak height
> of P2), measured at `T = 240, 230, 220 K`, **increases monotonically as `T` decreases toward
> `T_c`**. This is the finite-`|T − T_c|` analogue of the `φ⁴` amplitude scaling and it is the
> only leg of this campaign that touches critical behaviour at all. It is also the **most
> expensive** leg, because the rungs get exponentially slower in exactly the direction the
> prediction needs (§7).

> **P4 — the far arm reads floor.** At `(7, 7, 7) Å`, beyond the structural correlation length,
> the three coordination labels are effectively independent, the state is a product state, and
> `Core/Valve.lean`'s `valve_from_nothing` gives share **exactly zero**. Predicted: below 3 × the
> p99 of its own matched floor, at every state point. This is the campaign's plumb line and it
> runs through the byte-identical pipeline.

> **P5 — the three-body DOSE.** In **mW**, sweeping the tetrahedrality parameter `λ` from **0**
> (a strictly **pair** potential — Stillinger–Weber with the three-body term switched off) to
> **23.15** (water) at matched density and matched reduced temperature, the floor-subtracted
> share **increases monotonically with `λ`**, and at `λ = 0` it reads **floor**.

> **P6 — the pair-potential baseline does NOT reproduce the peak.** The Kob–Andersen binary
> Lennard-Jones mixture, read with the **same** coordination-number label through the **same**
> instrument across its own supercooling ladder, shows **no interior peak** of the P1/P2 kind.

**P5 is the sharpest instrument this campaign has and it is cheap.** `λ` is a dial on three-body
interaction strength inside one code at one density, with `λ = 0` a strictly pairwise
Hamiltonian. It is a far cleaner contrast than "water versus Kob–Andersen at matched reduced
conditions", which is a matching argument nobody can make airtight. The brief requires the KA
baseline and it is run (P6); **P5 is the one that decides whether the reading is three-body
physics.**

**If P5 fails — if the share does not track `λ` — the campaign's premise is dead**, whatever any
water reading says, and that is recorded as K1 below.

### 4.4 The path, and how it is located

The control parameter is **pressure along an isotherm**. The Widom line for TIP4P/2005 runs from
the LLCP (`≈ 193 K, 1350 bar`, Abascal & Vega 2010) **up in temperature and DOWN in pressure**,
reaching `1 atm` at **220–230 K**; above that it continues into **negative** pressure. So the
ladder and its pressure ranges are asymmetric, and the cheap rung is the one at negative pressure:

| rung | `T` | pressure grid (6 points) | where the crossing is | note |
|---|---|---|---|---|
| 1 | **240 K** | `−1200 … +400 bar` | negative pressure | fastest; **carries a cavitation gate** (§5.6) |
| 2 | **230 K** | `−600 … +800 bar` | near ambient | the primary rung |
| 3 | **220 K** | `0 … +1200 bar` | a few hundred bar | closest to `T_c`; the **stretch** rung |

**The cheap direction and the informative direction are opposite**, and that is stated now
rather than discovered as an excuse later: rung 1 is minutes and sits furthest from `T_c` and at
negative pressure where water can cavitate; rung 3 is the one P3 needs and is ~10 days of
contended GPU. If only rungs 1 and 2 complete, **P3 is scored on two points and is reported as a
two-point trend, not a monotone ladder** — or, if the two-point contrast is within its own error,
as NOT RUN.

**`P_W` is measured, not assumed.** The isothermal compressibility `κ_T` is computed from the
volume fluctuations of the *same* NPT runs, and its maximum located, **before any share is
computed at that temperature**. `κ_T` is a thermodynamic/pair-level quantity the instrument is
blind to, exactly as `g(r)` was in the glass campaign. The located `P_W` per isotherm is written
into `WATER_RESULTS.md` §1 before any §2 number.

---

## 5. THE CONTROLS AND THE GATE BATTERY

Gates are named by their reach in `GATES.md`. "Discharge point" is the stage at which the gate is
run and the artifact in which its reading is filed.

### 5.1 The three nulls, and why this campaign's are NOT the glass campaign's

**This is the most important structural difference between the two campaigns and it is stated
before any run.** In the glass campaign, species is a genuine extra degree of freedom, so "hold
the positions, resample the labels" is a well-defined pair-matched surrogate. **Here the label is
a FUNCTION of the positions.** Coordination number cannot be resampled independently of the
geometry. So a label permutation is *only* the estimator floor and is **not** a physical null,
and the physical null must act on the **positions**.

| | null | what it gauges | theorem pin |
|---|---|---|---|
| **N1** | **label permutation** on the byte-identical triple list — same configurations, same template, same tolerance, same triples, only the labels move | the **estimator floor**, carrying the triples' own overlap structure | `valve_from_nothing`: product state ⇒ share exactly 0 |
| **N2** | **ideal gas** — Poisson points at matched number density, through the byte-identical template selection and the byte-identical coordination filter | **template-selection and filter minting.** Selecting triples by a template is a selection on the configuration, and coordination number is a filter over a neighbourhood — FACT 3's trap, doubled | must read N1's floor |
| **N3** | **the pair-matched point process** — a configuration ensemble carrying water's **own measured `g_OO(r)` and nothing else**, built by Reverse Monte Carlo (McGreevy & Pusztai 1988) / iterative Boltzmann inversion (i.e. by Shell's `S_rel` programme, used to *build* the null rather than to fit a model) | **the physical null.** "Nothing beyond what the pair correlations already imply" | none — this one is measured, and it will read NONZERO |

**N3 is the deliverable's denominator and it will read nonzero**, because a pair-matched point
process has genuine triplet structure (Kirkwood superposition is violated in every real liquid).
**That is the point.** The deliverable is the **difference**, `share(data) − share(N3)`, and
nothing else.

**N3's own dye test, required before its null reading means anything** (`GATES.md` reach 13):
plant an explicit three-body coupling of known amplitude into a synthetic ensemble; RMC must
reproduce `g(r)` and **fail** to reproduce the planted three-body term at the amplitude that
matters. **A control that cannot see the dye returns "ungauged", not "clean".** The mW `λ = 0`
liquid (§4.3, P5) is a second, independent realisation of the same null — a real pair-potential
MD liquid rather than a reconstructed point process — and N3 and the `λ = 0` liquid must agree.
If they disagree, both are ungauged.

### 5.2 G-BINMINT — coarse-graining minting (reach 5) — **THE MOST DANGEROUS CHANNEL**

§2.1 removes the continuum from the *label* (an integer thresholded at an integer). It does
**not** remove it from the **geometry** (the shell tolerance `Δ`) or from the **filter**
(`r_cut`, which is a threshold on a continuum applied over a neighbourhood).

**Run, in the sky campaign's own pedestal form** (`REFUTER_RESULTS.md` §A9a): build the fine
object with slot `m` carrying `(coordination bin, radial sub-bin of one incident edge)` at
alphabet `b_lab · b_r`; take its **pair-maxent at fine resolution**; **merge** to the analysis
alphabet; read the share of the merged pair-maxent. That number is share manufactured by the
merge and nothing else — the **pedestal**. `b_r ∈ {2,3,4}`; `b_lab` from the raw coordination
histogram (`n ∈ {2,3,4,5,6,7+}`) merged to binary.

**Also run:** the `Δ` ladder, the `r_cut` ladder, and the fine-resolution LP
(`t_range_given_fine_marginals` ported to this alphabet).

**Rule fixed now:** pedestal ≥ 50 % of the reading ⇒ that rung is **VOID**. Between 10 % and
50 % ⇒ a quoted systematic on every number in that rung, never a footnote.

### 5.3 G-LP — pair-pinning at analysis resolution (reach 4) — **MANDATORY**

`KAPPA_EDGE_RESULTS.md`: on our own hardware every distribution carrying the measured fine pair
marginals had a share of *exactly* the measured value — the LP interval had width `0.00000`, and
a live headline was re-scoped three times.

**Run:** `share_headroom(P)` at every `(T, P, template)`, on cells that have already passed G-OCC.

**Advance prediction (P7), stated as a RATIO because stage 0 showed the absolute form would be
wrong:** **headroom ≥ 30 × the measured share at every read cell.** The VOID threshold is
3 ×, so P7 stakes an order of magnitude of margin above the kill.

**Why not an absolute threshold.** The first draft of this section staked *"headroom ≥ 0.10 nats
at every read template"* on the strength of the two HDL-proxy runs, which read **0.19–0.21 nats**
at the primary template. Checking it against the third proxy before committing, **it would have
fired on our own stage-0 data**: the LDL proxy reads **0.0222 nats** at that same template. The
headroom collapses when the label composition becomes lopsided (`p₁ = 0.091` there) — the **same
mechanism, at the same end of the path, as the ceiling collapse in §5.4**. Absolute headroom is
therefore not a property of the template; it is a property of the state point, and the two gates
fire together. Measured stage-0 range at the primary template: **0.0222 – 0.2099 nats.**

**Where it could bite:** at the lopsided-composition end of every isotherm, and at the excluded
small templates where excluded volume nearly empties cells. Cells with headroom < 3 × the
measured share are **VOID**.

### 5.4 G-OCC — occupancy / sparsity (reach 11)

**Rule fixed now, before any water exists:** the 8-cell analysis table is read only if **every
cell holds ≥ 30 counts**; a fine table of `(b_lab·b_r)³` cells only if occupancy ≥ 50 % and every
occupied cell ≥ 10. Below either bar the rung is **ungauged** — neither zero nor a detection —
and is reported as loudly as a reading. Tied fraction and empty fraction disclosed for every
table.

**This gate has already fired, in advance, on two of the five candidate templates** (§3). That
is its dye test for this campaign and it is on the record before any water exists.

**And a second, subtler occupancy failure specific to this design, found at stage 0 and
pre-registered because it will decide how the sweep can be read:** the honest ceiling
**collapses when the label composition becomes lopsided**. On the LDL-like proxy the HDL fraction
is 0.091, the label entropy is 0.30 nats, and the `ThirdCap` ceiling falls to **0.0004 nats**
against **0.0693** on the HDL-like proxy — **a factor of 170 between two ends of the very path
this campaign walks**. So:

> **Rule fixed now: the label composition `p₁` and the `ThirdCap` ceiling are reported for EVERY
> cell, and any cell whose ceiling is below 10 × its own measured floor is UNGAUGED. A trend in
> the ceiling *fraction* across the path may be entirely a trend in the DENOMINATOR, and no
> ceiling fraction is compared across cells whose ceilings differ by more than 3 ×.**

### 5.5 G-CERT, G-FLOOR, G-MIX, G-DOSE, G-POL, G-DYE, G-REPRO

* **G-CERT** (reach 12): the primary 2×2×2 reading is **exact** and uses no solver, so this gate
  is vacuous there and that is stated rather than claimed as a pass. Wherever a maxent solve is
  needed (the fine binmint tables), **both** IPF and a dual/L-BFGS solve are run; disagreement in
  `H(Q)` above `1e−9` **VOIDs** that rung. IPF is never used alone.
* **G-FLOOR** (reach 1): every reading is quoted **after subtraction of a floor drawn at its own
  `N`**, from N1, over ≥ 200 draws. Sub-sample readings get sub-sample floors (the Dalitz D2
  taint). The floor's **shape** is reported before any significance; significance is a **p-value
  against the empirical null**, never a median-and-sigma `z` (`share-null-is-chi2-shaped`, the
  Dalitz D7 near-miss). Stage 0 measured the floor law as **`median ≈ 0.43/N_tri`,
  `p99 ≈ 6.7/N_tri`** — an **overlap penalty of ≈ 1.9–2.0 ×** over the asymptotic multinomial
  `χ²₁/(2N)` (median `0.227/N`, p99 `3.32/N`) (§6).
* **G-MIX** (reach 3): P1's double peak and P2's single peak are both *interior structure*, so a
  null that cannot manufacture them must be shown not to. **Run:** a mixture of the isotherm's own
  endpoint ensembles, count-matched, against the interior points. The ECA taint is the anchor: a
  spike surviving an iid null collapsed **1886 ×** under a mixture null.
* **G-DOSE** (reach 7): the nuisance tracking pressure here is the **triple count** — stage 0
  measured a 164 × count swing at the excluded templates and a 1.2–3.9 × swing at the retained
  ones. **Run:** the reading against triple count at fixed `(T,P)` by subsampling, and against `P`
  at fixed triple count. If the reading tracks the count rather than `P`, the trend is **void**.
  **Count-matching across the isotherm is mandatory and both readings are reported** (count-matched
  and full-count, each against a floor at its own `N`); if they disagree in sign, the trend is
  **void**.
* **G-POL** (reach 8): declared **now**. A PASS of P1 is *two maxima with a minimum between them*.
  A PASS of P4 is a reading **at or below** its floor's p99. A PASS of G-LP is a **wide** interval.
  A PASS of G-BINMINT is a **small** pedestal. A PASS of P5 is share **rising** with `λ`. Each
  direction is written here so an implementation with the sign inverted is caught against this
  text and not against intuition (`9180c6a`, where the reviewer's own gate was the wrong one).
* **G-DYE** (reach 13): every control must detect a **planted** signal of the size that matters
  before its null reading means anything. `glass_gate.py`'s nine checks already gauge the
  estimator (G5: a planted three-body coupling recovered monotonically from `1.3e−7` to `1.2e−2`
  nats) and are inherited byte-identically. N3 needs its own (§5.1). **A control that cannot see
  the dye returns "ungauged".**
* **G-REPRO**: every committed number reproducible from the instrument committed beside it;
  samplers seeded, seeds recorded, deterministic parts re-run and compared before the log is
  trusted (the phi4 gate log at `5e3df2f`). MD is **not** bitwise reproducible on a GPU; the
  weaker commitment made here is that the **initial configuration, the seed, the integrator
  settings and the engine version** are recorded, and that the *analysis* is bitwise reproducible
  from the stored configurations.

### 5.6 The equilibration gate — the one the phi4 campaign minted

`GATES.md` harvest, *equilibration diagnostics can be blind*: the phi4 run's **largest** number
(2.5 × 10⁻² nats, 700 × the ridge) was a **metastability artifact invisible to `τ_int` and to the
Binder cumulant**. Supercooled water is exactly the regime where this bites, and it has a second
form here that the phi4 run did not face: **crystallisation**. Limmer & Chandler's whole critique
is that the apparent liquid–liquid transition is a liquid–**solid** transition seen through a
separation of timescales.

**Run, at every state point, before any share is read:**

1. **hot/cold start agreement** — two independent runs, one from a high-`T` configuration and one
   from a low-density/ice-like configuration, must agree in `⟨ρ⟩`, `κ_T` and the label
   composition `p₁`;
2. **the order parameter against its own root-mean-square** — the working diagnostic that `τ_int`
   and `U₄` are blind to;
3. **an explicit crystallinity check** — the fraction of molecules in an ice-like local
   environment must be flat in time and below a threshold fixed in advance;
4. **a cavitation check, mandatory on rung 1 and on every negative-pressure point** — the largest
   void in the box, and the density's own time series, must show no nucleation event. Water under
   tension is metastable against cavitation, and a cavitated configuration reads a large share
   that is a reading on a bubble.

**Any state point failing any of the four is NOT RUN, not a null.** This is declared in advance
because a crystallised or cavitated configuration will read a large share and it will be a
reading on ice or on a void.

---

## 6. THE ARITHMETIC THAT DECIDED THE DESIGN — already run, on synthetic data only

`water_feasibility.py`, on **two synthetic bracketing point patterns** built to straddle water's
oxygen sublattice: an **LDL-like** proxy (diamond/ice-Ic network at ice density with Gaussian
thermal displacement, coordination 3.80) and an **HDL-like** proxy (the same network at liquid
density with interstitials, coordination 4.77–5.15). **These are proxies for COUNTING, not for
physics.** No share reported below is a reading on water or on anything else.

**(1) The floor law, measured.** At the primary template, over `1 → 20` pooled configurations:

| proxy, width | `N_tri` | floor median | floor p99 | `median × N_tri` | `p99 × N_tri` |
|---|---|---|---|---|---|
| HDL, `σ=0.35 Å` | 3.89 × 10⁴ | 1.15 × 10⁻⁵ | 1.95 × 10⁻⁴ | 0.447 | 7.6 |
| HDL, `σ=0.20 Å` | 1.32 × 10⁵ | 3.10 × 10⁻⁶ | 4.32 × 10⁻⁵ | 0.409 | 5.7 |
| LDL, `σ=0.35 Å` | 3.08 × 10⁴ | 1.45 × 10⁻⁵ | 2.20 × 10⁻⁴ | 0.447 | 6.8 |

So **`floor_median ≈ 0.43/N_tri` and `floor_p99 ≈ 6.7/N_tri`**, against the asymptotic
multinomial `χ²₁/(2N)` whose median is `0.227/N` and whose p99 is `3.32/N`: an **overlap penalty
of ≈ 1.9–2.0 ×** in both statistics, in the same direction as, and at the low end of, the glass
campaign's measured `3–14 ×`. **The floor is the control itself pushed through the
byte-identical selection, never a multinomial resample** (`GLASS_PREREG.md` §4.1, where the naive
version was wrong by a factor of 45). The floor is `χ²₁`-shaped, so **p-values are the only
permitted summary** and no `z` from a median-and-sigma is quoted.

**(2) The occupancy gate decided the template ladder.** §3. Two of five templates excluded in
advance; the primary is not occupancy-limited at all (min cell 66–4768 over 30–40 configurations,
i.e. `≥ 30` is met by a single configuration).

**(3) The `ThirdCap` ceilings — the honest denominator, and it is 6–1000 × tighter than `ln 2`.**
`Core/ThirdCap.lean` `share_le_grouping_gaps` gives three per-orientation ceilings whose
**minimum** is the honest data-computable denominator; `share_le_log_two` gives the universal
one. Evaluated on the proxies' own tables at the primary template:

| proxy | `ceil_min` (nats) | as % of `ln 2` |
|---|---|---|
| HDL, `σ = 0.20 Å` (`p₁ = 0.59`) | 0.1212 | **17.5 %** |
| HDL, `σ = 0.35 Å` (`p₁ = 0.50`) | 0.0693 | **10.0 %** |
| LDL, `σ = 0.35 Å` (`p₁ = 0.091`) | 0.0004 | **0.06 %** |

**This is the single most consequential stage-0 finding and it is why §5.4 carries an extra
rule.** The per-orientation ceiling is the mutual information between a slot pair and the third
slot; it collapses when the label becomes rare. A ceiling fraction quoted against `ln 2` on this
target is meaningless, and a ceiling fraction quoted against `ThirdCap`'s own minimum is **not
comparable across the sweep**. Both are reported, per cell, with `p₁` and the label entropy
beside them.

**(4) The size requirement, and it is modest.** Requiring `floor_p99 ≤ S/3` gives
`N_tri ≥ 20/S`. At the conservative end of the measured count bracket (0.9 ordered triples per
particle at the primary template):

| target `S` (nats) | `N_tri` | configurations at `N = 2000` | at `N = 4000` |
|---|---|---|---|
| 1 × 10⁻³ | 2.0 × 10⁴ | 11 | 6 |
| 1 × 10⁻⁴ | 2.0 × 10⁵ | 111 | 56 |
| **3 × 10⁻⁵** | **6.7 × 10⁵** | **370** | **185** |
| 1 × 10⁻⁵ | 2.0 × 10⁶ | 1111 | 556 |

> **The pre-registered design sensitivity is `S = 3 × 10⁻⁵` nats, requiring `N = 4000` water
> molecules and `200` independent configurations per state point** (the table's 185, rounded up).

At the realistic thermal width the counts are 3.9 × higher, so this is a conservative budget.
For scale, the `φ⁴` 3D ridge's clean-route peak was `1.6–2.6 × 10⁻⁴` nats at `L = 8` and
`3.7 × 10⁻⁶` at `L = 32`; `3 × 10⁻⁵` nats is `0.04 %` of a `0.07`-nat honest ceiling.

**The independent axis is the independent CONFIGURATION, never the pooled triple**
(`whole-only-null-autocorrelation`, `order3-probe-geometry`). Configuration spacing is set from
the **measured** structural relaxation time at each state point, not assumed; `σ` throughout is
the configuration-level block bootstrap, and — per `GLASS_PREREG.md` §6.1 — a **NULL** claim may
not be scored against that bootstrap `σ` (it over-states uncertainty ≈ 2.2 × for a non-negative
statistic near its boundary) but against an **exact permutation test on configuration
membership**.

---

## 7. FEASIBILITY — priced honestly, and half of this campaign is DECLARED OUT OF REACH

**The box.** Shared, 32 cores at load ≈ 24, **94 % disk** (55 GB free), and one **RTX 4090 Laptop
GPU at 100 % utilisation** serving the concurrent glass and Planck campaigns. **No MD engine is
installed;** `openmm 8.5.2` and `lammps 2025.7.22.4.0` are pip-installable into the venv without
root (verified from the package index; **nothing was installed**).

**The data.** `WATER_PRIOR_ART.md` §5: the definitive public dataset for the TIP4P/2005 LLCP
(Zenodo 3836542) contains **scalar time series, structure factors and GROMACS input files — and
no configurations at all**. **Every water configuration this campaign reads must be generated by
us.**

**The arithmetic.** 200 independent configurations at `N = 4000` needs `200 × τ_α` of sampling
per state point. Taking literature-order relaxation times for TIP4P/2005 (**to be measured, not
assumed**) and a contended-GPU throughput of ≈ 120 ns/day for a 16 000-site rigid-water system
with PME:

| `T` | `τ_α` (order) | sampling for 200 configs | wall time / state point | 6-pressure isotherm |
|---|---|---|---|---|
| **240 K** (rung 1) | ~30 ps | 6 ns | ~1 h | **~6 h — feasible** |
| **230 K** (rung 2) | ~150 ps | 30 ns | ~6 h | **~1.5 days — feasible** |
| **220 K** (rung 3) | ~1 ns | 200 ns | ~1.7 days | ~10 days — **stretch** |
| 210 K | ~10 ns | 2 µs | ~17 days | ~100 days — **out of reach** |
| 193 K (`T_c`, Abascal–Vega) | ≫ 1 µs | ≫ 200 µs | ≫ 5 years | **out of reach** |
| 172 K (`T_c`, Debenedetti–Sciortino–Zerze) | — | — | — | **out of reach by orders of magnitude** |

**The `τ_α` column is a literature-order estimate and is NOT a measurement.** It is used only to
price the campaign. Every state point measures its own relaxation time and sets its own
configuration spacing from that measurement; **if 200 independent configurations cannot be
reached in the allotted wall time, that state point is reported NOT RUN, never as a null.**

> **VERDICT, declared before anything is run: this box cannot reach water's liquid–liquid
> critical point, and it is not close. It is short by two to four orders of magnitude in wall
> time.** The published LLCP determinations used umbrella sampling and metadynamics over
> aggregate microseconds-to-milliseconds; reproducing that is a multi-month project on dedicated
> hardware, not a session on a shared laptop-class GPU that is already fully committed.

**What that leaves, and it is still a real experiment.** The Widom line reaches `1 atm` at
**220–230 K** and runs from there down and to the right toward the LLCP. The three isotherms of
§4.4 **each cross it** — rung 1 at negative pressure, rung 2 near ambient, rung 3 at a few
hundred bar — at successively smaller `|T − T_c|`. So **P1, P2 and P4 are testable**, and **P3 is
testable over a three-rung ladder that approaches `T_c` without reaching it**. That is the
campaign, and its ceiling is `|T − T_c| ≈ 27 K` on the Abascal–Vega location and `≈ 48 K` on the
Debenedetti–Sciortino–Zerze one.

**Priced, in order of cost:**

| arm | cost | verdict |
|---|---|---|
| **A — mW `λ`-dose (P5)** | monatomic, short-range, no electrostatics, 10 fs steps; `μs/day` class | **cheapest and most decisive. Run first.** |
| **B — Kob–Andersen baseline (P6)** | configurations **already on disk**; instrument already committed | **hours of CPU. Run second.** |
| **C — TIP4P/2005 isotherms at 240 and 230 K** | ~1 day of a *free* GPU, ~2 days contended | **feasible, but not while the GPU is at 100 %** |
| **D — the 220 K isotherm (rung 3, the one P3 needs)** | ~10 days contended | stretch; run only if C succeeds |
| **E — the LLCP itself** | months on dedicated hardware | **NOT RUN. Named, priced, and declared out of reach.** |

**Order of operations is therefore A → B → C → D, and it is deliberate: the two arms that can
kill the campaign's premise are the two that cost nothing.** If P5 fails on mW, no atomistic
water run is worth starting.

**Nothing in arm C or D begins while the glass and Planck campaigns hold the GPU.** That is a
resource commitment, stated here so its absence from `WATER_RESULTS.md` cannot be read as a
result.

---

## 8. OUTCOMES — every one, with its verdict fixed now

Scored on the primary tetrahedral template, floor-subtracted against N1 at matched `N`, excess
over N3, count-matched, with `σ` the configuration-level block bootstrap.

**(a) DOUBLE PEAK (P1 confirmed).** Two interior maxima straddling the measured `P_W`, each ≥ 5 σ
above the intervening minimum, at ≥ 2 of the 3 isotherms, with the contrast growing as `T` falls
(P3), and the excess over N3 ≥ 5 σ at the maxima. Verdict: *the pairwise-blind share reads
water's supercooled ordering sector, and it reads it with the shape a machine-checked theorem plus
two prior confirmed measurements predicted in advance.* Nothing more.

**(b) SINGLE PEAK (P2 confirmed, P1 fired).** One interior maximum at the crossing, no dip.
Verdict: *the coordination label is not an Ising-order-parameter proxy; the share tracks the
response maximum.* A result, reported as one, with P1 marked FIRED in the scorecard.

**(c) NULL — fully acceptable and reported as loudly as (a).** The floor-subtracted share is flat
in `P` across every isotherm: the **exact configuration-permutation test** returns `p > 0.05`,
**and** that test has been shown able to detect a planted difference of the size that matters
(without that leg the null is *ungauged*, not clean). Verdict: *over this path, in this model, in
the coordination channel, whole-only structure does not track the Widom line* — which is evidence
against either the LLCP's structural signature or against this instrument's ability to see it,
and **the two are not separated by this design**. That non-separation is stated now, not
discovered later.

**(d) MONOTONE, NO INTERIOR STRUCTURE.** Share rises or falls monotonically with `P`. Almost
certainly a density effect; requires G-DOSE discharged before any interpretation.

**(e) PINNED.** G-LP headroom < 3 × the measured share at the read templates. Those cells are
**VOID** and the pinning is the finding.

**(f) MANUFACTURED.** The binmint pedestal ≥ 50 % of the reading. That rung is **VOID**.

**(g) CEILING-COLLAPSED — the outcome specific to this design.** A cell whose `ThirdCap` ceiling
is below 10 × its own floor. **UNGAUGED**, and a trend built out of such cells is void. Named
here because stage 0 already measured a **170 ×** ceiling swing across the two ends of this
campaign's own path (§6(3)).

**(h) UNGAUGED — the outcome-completeness entry.** *A large, well-controlled reading whose
decomposition into signal, floor, pedestal and pair-matched null was not performed.* A
**non-verdict**: not a detection, not a null, and not deferred to a later document
(`GATES.md` harvest; the unblind that fit no pre-registered outcome, `28fadbd`).

**(i) NOT RUN.** Every pre-registered arm that did not complete is listed **by name** in
`WATER_RESULTS.md` with its reason, and **no verdict is scored on an arm that did not run**. Arm
E is already in this category before the campaign starts (§7), as are the `q_tet`/`d₅` secondary
label designs (§2.2) and the ST2 model entirely.

**(j) INSTRUMENT FOULED.** The far arm (P4) does not read inside its floor band, or N2 (ideal
gas) reads above its floor. Then the pipeline is fouled and **every reading it produced is
ungauged**, including any that look good.

**(k) CRYSTALLISED.** Any state point failing §5.6. Reported as **NOT RUN**, never as a reading,
and never averaged into a trend. Given Limmer & Chandler's critique this is the outcome most
likely to be reached by carelessness, and it is enumerated first among the failure modes for that
reason.

---

## 9. THE KILLS — staked first, and separable

Each takes down its own claim and **nothing beneath it**. **None of them touches** `wild-share`,
the sky campaign, the rent clause, the valve, or any line of `Stance.lean`.

**K1 — the campaign's PREMISE, and it is the cheapest to fire.** *If the mW share does not
increase with the three-body parameter `λ`, and in particular if the `λ = 0` pair-potential
liquid does not read floor, then "the pairwise-blind share reads three-body interaction physics"
is refuted, at a sensitivity we measured rather than assumed, and no atomistic water arm is
worth running.* Takes down the campaign and nothing else. **Run first, by design.**

**K2 — the shape claim only.** *If no interior structure of the P1 or P2 kind appears on any
isotherm at ≥ 5 σ, the Widom-line hypothesis for this observable is dead.* A nonzero share
everywhere survives this kill; existence and shape are separate claims and die separately.

**K3 — the double-peak claim only.** *If a single peak appears with no dip at the crossing, P1 is
dead and P2 stands.* This kill is separable from K2 by construction, and it is the one that tests
the repository's own theorem-plus-ridge composition rather than water.

**K4 — the excess claim only.** *If, at every template and every state point, the floor-subtracted
share fails to exceed the N3 pair-matched point process's share by more than 5 σ of the N3
ensemble, then "water's supercooled structure carries whole-only order invisible to `g_OO(r)`" is
refuted.*

**K-VOID — the instrument.** *If the far arm does not read inside its predicted floor band on real
configurations, the pipeline is fouled and every reading it produced is ungauged.* Fires on us,
not on water.

**K-PIN / K-MINT / K-DOSE / K-CEIL.** As §5.3, §5.2, §5.5, §5.4: headroom below 3 × the reading,
pedestal ≥ 50 %, the reading tracking triple count rather than pressure, ceiling below 10 × the
floor. Each VOIDs its own cells and nothing else.

**K-DYE.** *If N3 cannot detect a planted three-body coupling at the amplitude that matters, or if
N3 and the mW `λ = 0` liquid disagree, every verdict resting on either is ungauged* — not clean,
not a refutation.

---

## 10. WHAT IS NOT CLAIMED, WHATEVER THE READING

1. **Nothing about experimental water.** Simulated models only.
2. **No resolution of the LLCP dispute**, and no reading anywhere near `T_c` (§7).
3. **No priority.** `WATER_PRIOR_ART.md` §1 records six prior programmes on the same physical
   question. The most this campaign may claim is a *different, non-negative* object and a sweep of
   it across a path nobody has swept it across.
4. **No claim about the orientational channel.** §2.1 reads the **oxygen sublattice only**; every
   molecular reorientation leaving the oxygens fixed is invisible to this design. A null here is
   a null about *positional* whole-only structure in the coordination channel and **may not be
   reported as a null about water's three-body structure in general**. That is the price of
   removing the orientational continuum from the label, and it is paid knowingly.
5. **No claim that any reading is large in absolute terms.** `KAPPA_EDGE_RESULTS.md` measured
   that the degree-3 direction can hold ~1 % of the fine-grained structure; this is a small sector
   read precisely.
6. **No stance implication.** `wild-share` does not move; `Stance.lean` is not opened; no Lean
   file is edited; `lake` is not run; nothing is pushed.

---

## 11. FILES AND ORDER OF OPERATIONS

| stage | artifact | committed |
|---|---|---|
| 0 | `WATER_PRIOR_ART.md` — the credits and the adjudication | before this document |
| 0 | `water_feasibility.py` + its three synthetic-only JSONs | **with this document** |
| 1 | **this document** | **before any water configuration exists** |
| 2 | `water_mw.py` — arm A, the `λ`-dose | before arm B |
| 3 | `water_ka.py` — arm B, the Kob–Andersen baseline on the coordination label | before arm C |
| 4 | `water_md.py`, `water_rmc.py`, `water_run.py` — arms C/D and the N3 null | with, or before, stage 5 |
| 5 | `WATER_RESULTS.md` — the sweep, the scorecard against §4 and §8, the verdict | last |

`glass_share.py` (the estimator, the triangle enumerator, the headroom LP) and `glass_gate.py`
(nine checks, three theorem-pinned, all PASS on synthetic tables) are **inherited byte-identically
and are not re-written**. `water_feasibility.py` and its outputs **already exist and are committed
with this document**. **No water configuration has been read by any of them.**

Primary seed **20260727**. Research → scratchpad memo → Eric's review. Nothing pushed.
