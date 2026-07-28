# RESULTS — the whole-only order-3 reading of a three-body water model, swept in the three-body coupling

Pre-registered in `WATER_PREREG.md`, committed **before any water configuration existed**, and
amended by `WATER_AMENDMENT_1.md` … `WATER_AMENDMENT_12.md`. The instrument's own examination
(`WATER_ARM_A_GATE.md`, `feae80c`) ran on published properties only, before any share was
computed on anything. **`WATER_AMENDMENT_12.md` was written after the configurations existed and
before the first share was computed on any of them**, and it is the document that decides what
this one can score.

---

## SCOPE, FIRST

The target is the **mW monatomic water model** (Molinero & Moore, JPCB 113:4008 (2009)) —
**simulated water, not experimental water**, and one model among several. This is a contribution
to a contested question — whether supercooled water's structure carries order beyond its pair
correlations — **and not a resolution of it**. **No reading here goes near water's putative
liquid–liquid critical point**: `WATER_PREREG.md` §7 declared that out of reach on this box by
two to four orders of magnitude in wall time before anything was run, and that verdict stands
untouched.

**Nothing here bears on `wild-share`, on `adequacy`, or on any claim about nature at large.
Nothing here moves `Stance.lean`.** No Lean file was opened, `lake` was never invoked, the audit
was not run, nothing was pushed.

**The credit block is `WATER_PRIOR_ART.md` and it is part of this document by reference.** Its §1
is mandatory and is not optional reading: the water community has had a **three-body order
parameter** since **Chau & Hardwick, *Mol. Phys.* 93:511 (1998)** and **Errington & Debenedetti,
*Nature* 409:318 (2001)**, whose `q = 1 − (3/8) Σ_{j<k} (cos φ_jk + 1/3)²` is built from the
angles between triplets of first-shell oxygens and was used to build water's *order map* and to
bound its structurally anomalous region. **The physical question is theirs and the priority is
theirs.** **Saija, Saitta & Giaquinta (2003)** computed entropy-beyond-pairs (the Residual
Multiparticle Entropy) for TIP4P water across `230–350 K` twenty-three years ago.

**How our object differs, stated exactly** — with `WATER_AMENDMENT_8.md`'s corrections carried,
because the first version of two of these three was over-broad:

1. **A supremum, not a coordinate.** `q` is one scalar function of the angles, a chosen
   projection. The share is `S(Q) − S(P)` with `Q` the maximum-entropy distribution over **all**
   distributions carrying `P`'s three pair marginals — a supremum over a convex set. A coordinate
   is blind to what it does not project onto.
2. **The reference state.** `q` reads 0 for the ideal gas and 1 for a perfect tetrahedron, so an
   **interacting** pair-potential liquid at liquid density has `q ≠ 0` — hard spheres have
   angular structure. The share is zero exactly when `P` is reconstructible from its own pair
   marginals, so the pair contribution is subtracted by construction rather than by argument.
   *(Amendment 8 W4: the first form of this said "a pair-potential liquid with no three-body
   physics whatsoever has `q ≠ 0`", which is false at the ideal gas — the very reference point the
   preceding sentence names.)*
3. **Sign.** `q` moves in either direction; **`share ≥ 0`, with no condition beyond `IsProb`**,
   because `Q` maximises entropy over a set containing `P`. *(Amendment 8 W4: the first form said
   "with no condition", and there is one.)*

**And the substantive scope limit specific to this result:** §2.1 of the pre-registration reads
the **oxygen sublattice only**. Every molecular reorientation leaving the oxygens fixed is
invisible to this design. **A null here is a null about positional whole-only structure in the
coordination channel, and may not be reported as a null about water's three-body structure in
general.**

---

## THE HEADLINE

> **The pre-registered arm A could not be run as designed, for a reason that is itself the
> result: the `n ≥ 5` coordination label is not neutral between the two ends of the dose it was
> built to sweep. It saturates on every homogeneous pair-potential liquid — measured, at each
> `λ`'s own ambient density, where `p₁ = 1.000` for every `λ ≤ 11` — and the pre-registered
> matched-density sweep drives the low-`λ` liquid into two-phase coexistence, which the
> campaign's own §5.6 gate caught before the estimator was imported. `K1`, the campaign's premise
> kill, is therefore UNGAUGED: it cannot fire and cannot be survived.**

> **On the `λ` window that does pass both gates, the rescoped dose P5′ FIRES. The ladder is not
> monotone in the share or in the floor-subtracted excess, five of its seven cells sit at or below
> their own floor, and its smallest reading lies between its two largest. And the load-bearing
> control settles what a raw reading would not have: at `λ = 23.15` a pair-potential liquid
> carrying mW's own `g(r)`, built by Iterative Boltzmann Inversion, accounts for the whole
> reading — the beyond-pair excess is `+0.65 σ`, and `K4` fires under both of the bars that were
> written for it.**

> **Two cells do carry a reproducible excess over their own label floor, and both are VOID for the
> same measured reason.** `λ = 27`'s excess survived a declared out-of-sample test at five times
> the data (**T1 PASSES**: `56.6 ×` its floor, `p` at its resolution limit). But **a structureless
> ideal gas, pushed through the same template selection and the same coordination filter,
> manufactures `1.61 × 10⁻⁴` nats — more than any mW reading in this campaign, and `22 ×` the
> reading at `λ = 23.15`.** By the pre-registration's own rule (*pedestal ≥ 50 % of the reading ⇒
> VOID*) every cell in arm A is void, and the mechanism is confirmed by an advance prediction: the
> minting vanishes by a factor of **13 000** once the template is wider than `2 r_cut`, where the
> three slots' cutoff spheres no longer share a point.

**This is the opposite of the sibling glass result, and the contrast is the deliverable.**
`GLASS_RESULTS.md` measured the share growing **×44** on cooling a Kob–Andersen pair-potential
glass former, with a pair-matched surrogate reproducing **82–94 %** of it and a beyond-pair excess
of **+3.8 σ** at its coldest rung. Here, on a liquid whose physics is genuinely three-body, in
the channel chosen because it should be where three-body physics shows, **there is no reading to
deflate.** The campaign's own §1 argument — *water is the archetypal system in which our quantity
should be physically load-bearing rather than incidental* — is **not supported by this
measurement in this channel**, and that is reported as loudly as a signal would have been.

**Three findings about the instrument came out of this and are worth more than the null:** the
label's tetrahedrality bias (§1.3), the ideal gas's minted excess over the label floor (§2.4), and
the measured detection limit of the whole battery (§2.3), which is **an order of magnitude above
the pre-registered design sensitivity**.

---

## 1. WHAT THE GATES DID BEFORE ANY SHARE WAS READ

`WATER_PREREG.md` §5.6 fixes four equilibration checks at every state point and declares that
*"Any state point failing any of the four is NOT RUN, not a null."* They were run first. The full
adjudication is `WATER_AMENDMENT_12.md`; this section reports the readings.

### 1.1 Six of the eight pre-registered `λ` points had cavitated

At the pre-registered matched density `ρ = 0.997 g/cm³`, 298 K, NVT, over 11 frames per state
point spanning the whole 500 ps production window (`water_homog.py`, which computes no share):

| `λ` | over-dispersion | Poisson | max void (Å) | `r_void^max` (Å) | `⟨n⟩` at 3.50 Å | ideal-gas `⟨n⟩` | `p₁` | max `S(k)` | verdict |
|---|---|---|---|---|---|---|---|---|---|
| 0 | **0.875** | 0.179 | **13.06** | 4.66 | **12.61** | 5.99 | **1.000** | 274 | **CAVITATED** |
| 2 | **0.773** | 0.179 | **14.08** | 4.66 | **12.21** | 5.99 | **1.000** | 429 | **CAVITATED** |
| 5 | **0.603** | 0.179 | **11.96** | 4.66 | **11.85** | 5.99 | **1.000** | 352 | **CAVITATED** |
| 8 | **0.512** | 0.179 | **14.99** | 4.66 | **10.01** | 5.99 | **1.000** | 86 | **CAVITATED** |
| 11 | **0.426** | 0.179 | **13.37** | 4.66 | 8.69 | 5.99 | **0.996** | 57 | **CAVITATED** |
| 14 | **0.344** | 0.179 | **11.76** | 4.66 | 7.54 | 5.99 | **0.989** | 33 | **CAVITATED** |
| 15 | 0.328 | 0.179 | 10.89 | 4.66 | 7.17 | 5.99 | 0.982 | 26 | **CAVITATED** |
| 16 | 0.294 | 0.179 | 10.56 | 4.66 | 6.89 | 5.99 | 0.975 | 22 | **CAVITATED** |
| 17 | 0.260 | 0.179 | 9.98 | 4.66 | 6.53 | 5.99 | 0.961 | 14 | **CAVITATED** |
| 18 | 0.235 | 0.179 | **9.08** | 4.66 | 6.27 | 5.99 | 0.950 | 10 | **CAVITATED** |
| 19 | 0.190 | 0.179 | 7.79 | 4.66 | 5.97 | 5.99 | 0.929 | 6.6 | **CAVITATED** |
| **20** | **0.072** | 0.179 | 3.50 | 4.66 | 5.57 | 5.99 | 0.866 | 5.8 | **PASS** |
| **20.5** | 0.077 | 0.179 | 3.44 | 4.66 | 5.52 | 5.99 | 0.858 | 6.2 | **PASS** |
| **21.5** | 0.072 | 0.179 | 3.24 | 4.66 | 5.33 | 5.99 | 0.816 | 6.0 | **PASS** |
| **22** | 0.072 | 0.179 | 3.21 | 4.66 | 5.24 | 5.99 | 0.783 | 7.8 | **PASS** |
| **23.15** | **0.071** | 0.179 | **3.13** | 4.66 | 5.11 | 5.99 | 0.743 | 6.1 | **PASS** |
| **25** | 0.065 | 0.179 | 3.07 | 4.66 | 4.89 | 5.99 | 0.647 | 7.7 | **PASS** |
| **27** | 0.074 | 0.179 | 3.00 | 4.66 | 4.55 | 5.99 | 0.464 | 8.1 | **PASS** |

**Three independent diagnostics agree and none is marginal at a failing point.** A homogeneous
liquid is *more* ordered than a Poisson process and must read **below** the Poisson value; mW at
`λ = 23.15` reads `0.40 ×` it. `r_void^max` is the radius a Poisson process at the **same**
measured mean number density exceeds with probability `0.01` over the same `24³` grid — computed
from the density, not chosen — and the failing points carry voids of 9–15 Å radius in a 39.15 Å
box. And `⟨n⟩` at the failing points is the **close-packed** value while the box-mean density
implies 5.99: *the particles are not at the density the box says they are at.*

**Pressure, promised by `WATER_ARM_A_GATE.md` §4 and now recorded** (it was not recorded by the
sweep as first run): every point in the readable window sits under large tension —
`−2599` to `−1691 atm` at `λ = 20…21.5`, `+1851` and `+3912 atm` at `λ = 25, 27`. The sign
crossing between `λ = 22` and `λ = 25` is where the matched density stops stretching the liquid
and starts compressing it.

### 1.2 The mechanism was measured in advance and the wrong conclusion drawn from it

`WATER_ARM_A_GATE.md` §4 measured that removing the three-body term at fixed pressure makes the
liquid **2.40 × denser**, concluded correctly that the sweep must run at matched density, and then
wrote that the resulting large negative pressure *"is legitimate in NVT and it is what 'matched
density' costs."* **It is not legitimate.** A liquid held at 42 % of its own liquid-branch density
at 298 K is not under tension; it is inside the two-phase region, and the constant-volume ensemble
does not prevent phase separation — it hosts it.

> **This is a warrant-reach instance (`GATES.md`, PROPOSED) of a variety not in that registry's
> list: the measurement was right, the number was right, and the inference drawn from the right
> number was wrong.** And the refutation was already inside this campaign's own battery — §5.6
> check 4 exists to catch exactly this and was pre-registered as mandatory *"on every
> negative-pressure point"*. **The campaign's gate battery contradicted the campaign's own design
> document, and the contradiction survived because the run order let the measurement precede the
> gate.** That ordering is now fixed: §5.6 runs the moment configurations exist and before the
> estimator is imported.

### 1.3 The label saturates on a homogeneous pair-potential liquid — measured, not argued

The independent arm: every `λ` at **its own ambient density** (NPT, 1 atm, 298 K). Here nothing
cavitates — over-dispersion `0.050–0.073`, all below the Poisson `0.179`, no voids, no Bragg
peaks. And yet:

| `λ` | `ρ_amb` (g/cm³) | `P` (atm) | over-disp | max void (Å) | `⟨n⟩` at 3.50 Å | `p₁` | verdict |
|---|---|---|---|---|---|---|---|
| 0 | **2.4061** | +3.9 | 0.050 | 1.74 | **14.04** | **1.000** | **LABEL-DEGENERATE** |
| 2 | 1.9911 | +4.8 | 0.073 | 1.93 | 13.18 | **1.000** | **LABEL-DEGENERATE** |
| 5 | 1.6547 | +6.3 | 0.060 | 2.46 | 12.91 | **1.000** | **LABEL-DEGENERATE** |
| 8 | 1.4444 | +2.0 | 0.056 | 2.31 | 10.85 | **1.000** | **LABEL-DEGENERATE** |
| 11 | 1.3100 | −1.3 | 0.063 | 2.44 | 9.12 | **1.000** | **LABEL-DEGENERATE** |
| 14 | 1.2122 | −1.5 | 0.066 | 2.62 | 7.87 | 0.999 | **LABEL-DEGENERATE** |
| 18 | 1.1092 | +1.5 | 0.066 | 2.85 | 6.46 | 0.974 | PASS |
| 23.15 | 0.9972 | +1.4 | 0.069 | 3.06 | 5.13 | 0.750 | PASS |

**`ρ_amb(λ = 0)/ρ_amb(λ = 23.15) = 2.413`, reproducing the gate document's independently measured
2.40 × to 0.5 %.**

> **THE FINDING. The `n ≥ 5` coordination label is itself a tetrahedrality detector.** It has
> variance only where a three-body term holds an open network open. P5 asked it to compare a
> tetrahedral liquid against a close-packed one, and on the close-packed one it saturates —
> **at every density at which that liquid exists**. The two candidate matchings fail for two
> *different* reasons (matched density: two-phase; matched pressure: label-degenerate) and the
> deeper failure is the label's, not the matching's.

**Why stage 0 could not have caught it.** `water_feasibility.py` bracketed the design with an
LDL-like diamond/ice-Ic network and an HDL-like version of the same network with interstitials.
**Both are tetrahedral networks.** The *control* end of the dose — a close-packed liquid with no
tetrahedral term — was never proxied. This is `GATES.md` reach 13 in its design-stage form: **the
feasibility study gauged the instrument only over the range where it works.**

### 1.4 Hot/cold start, and a metastable crystal

§5.6 check 1 requires two independent starts to agree. A diamond-lattice ("ice-like") start at the
same density was run at the two ends of the readable window (`N = 1728`, `--start cold`):

| `λ` | quantity | hot start | cold start | agreement |
|---|---|---|---|---|
| **20** | `p₁` | 0.866 | **0.862** | **0.5 %** |
| | `⟨n⟩` | 5.57 | **5.54** | 0.5 % |
| | `P` (atm) | −3089 | **−3002** | 2.8 % |
| | max `S(k)` | 5.8 | 6.6 | liquid |
| **23.15** | max `S(k)` | 6.1 | **733.4** | **CRYSTALLINE** |
| | `⟨n⟩` | 5.11 | **4.01** | — |
| | `p₁` | 0.743 | **0.006** | — |

**At `λ = 20` the check is DISCHARGED** — the two starts agree to better than 3 % in every
reported quantity. **At `λ = 23.15` the cold start did not melt within 600 ps**: `max S(k) = 733`
against a liquid's `6.1` is a Bragg peak, and `⟨n⟩ = 4.01` is perfect tetrahedral coordination.
Per §5.6 that configuration is **NOT RUN**, and the hot/cold check at `λ = 23.15` is
**undischarged** — reported as a gap, not as a pass. It is also a physical datum: **mW at
`ρ = 0.997 g/cm³` and 298 K supports a metastable crystal on this timescale**, which is exactly
the hazard Limmer & Chandler's critique of the LLCP is about, appearing in the cheapest arm of
the campaign.

### 1.5 Independence, and the correlation length

The independent axis is the independent **configuration**, never the pooled triple. Measured, per
state point, on the label field's own autocorrelation across frames:

* **`τ = 1.00–1.15` frames** at every readable `λ`. Frames are 2.5 ps apart, so **the 201 frames
  are 201 independent configurations** and no thinning is applied.
* **`ξ = 1.06–2.66 Å`** across the ladder, from the envelope of `r·(g(r) − 1)` beyond the first
  shell. `ξ` is a **pair** quantity the instrument is blind to, so measuring it is legitimate and
  is declared.
* Therefore `3ξ ≤ 7.97 Å ≪ L/2 = 19.58 Å`: **the far arm exists at every state point**, at
  `r_far = max(3ξ, 7.0 Å)` per `WATER_AMENDMENT_10.md` J3, and is not capped by the box. `ξ` does
  **not** grow along this ladder, which is the one respect in which this arm is easier than the
  Widom-line arms it was meant to precede.

---

## 2. THE INSTRUMENT'S OWN EXAMINATION — and it found two defects

`glass_gate.py`'s nine checks on the shared estimator (three theorem-pinned) are inherited
byte-identically and **PASS** (`glass_gate.json`). They do not cover what `water_arm_a.py` adds:
the dump reader, the coordination filter, the triangle cap, the class-partitioned ceiling, the two
floors and the ideal-gas control. Those were examined in `water_arm_a_gate.py`.

### 2.1 The analysis instrument could not run at all

> **As committed, `water_arm_a.py`'s LAMMPS dump reader left the `ITEM: ATOMS` header line
> unconsumed and raised on the first frame of the first file.** It had never been run. This is
> why no share existed at the moment `WATER_AMENDMENT_12.md` was written, and it is the plainest
> possible demonstration of the docimasia's point: the instrument was examined before it was
> trusted, and it failed the first check.

### 2.2 What passed, and one number worth more than a pass

| check | result |
|---|---|
| **W1** dump reader round-trip against a file of known coordinates | **PASS** after the fix (worst error `4.9e−07`, the write precision) |
| **W2** coordination filter: exact counts on a simple cubic lattice (6, 18, 26 at three radii) and invariance under random rigid translation through the periodic boundary | **PASS** |
| **W3** triangle cap: orbit deviation **exactly 0.000e+00** at every cap, with 6.000 orderings per triangle confirming complete enumeration | **PASS** (`WATER_AMENDMENT_9.md` I2, re-measured on this implementation) |
| **W4** class-partitioned ceiling on a planted 2+1 state: symmetry-equivalent orientations identical to `0.00e+00` (`0.04864075, 0.04864075`) against a third at `0.07917364`; classes `{(12\|3),(13\|2)}, {(23\|1)}` taken from the edge lengths and never from the data; scalene → three singletons, equilateral → one class | **PASS** (`WATER_AMENDMENT_7.md` G2) |
| **W5** the two floors on real mW configurations, at `N_tri = 105 686` | **PASS**, and see below |
| **W8** a saturated label's `ThirdCap` ceiling | **exactly 0.0**, and `2.0e−12` at `p₁ = 0.999997` — the arithmetic behind §1.3, checked rather than asserted |

> **W5 is a confirmed advance prediction and it is the only one this arm produced.**
> `WATER_PREREG.md` §6 measured, on **synthetic** bracketing point patterns before any water
> existed, a floor law `median ≈ 0.43/N_tri` — an **overlap penalty of 1.9 ×** over the
> independent-sample `χ²₁/(2N)` law. On **real mW configurations** the measured penalty is
> **1.859 ×** (floor median `4.001e−06` against the `χ²₁` median `2.153e−06`). **The floor law
> transferred from a synthetic proxy to a real liquid within 2 %.**

The finite-population gauge (N1b permutation minus N1a product, `WATER_AMENDMENT_4.md` D2) is
`−4.0e−07` nats, below every reading quoted in this document, so the two floors are
indistinguishable at this `N` and the theorem-pinned one (N1a) is used throughout.

**The pin, stated with its hypotheses rather than by name** (W2, applied to this document):
**N1a draws labels iid Bernoulli, so the label triple is an EXACT product state**, and
`Core/Valve.lean`'s `valve_from_nothing` — whose signature was read at source for this document:
three `IsKernel` kernels, three `IsProb` cell states, and an input of the form
`prod3 p₁ p₂ p₃` — gives share **exactly zero**. What N1a reads is therefore the finite-sample
floor and nothing else. **N1b permutes a fixed multiset, which is not a product state**, carries a
finite-population correlation of order `1/N`, and is **not** pinned by that theorem
(`WATER_AMENDMENT_4.md` D2). The three Lean statements this document leans on —
`valve_from_nothing`, `share_le_log_two` and `share_le_grouping_gaps` — were each checked against
their source signatures in this session; the latter two hypothesise only `IsProb`, and
`share_le_grouping_gaps` proves **all three** per-orientation bounds, which is what licenses taking
a minimum across symmetry classes.

**Orbit symmetry on the real tables.** The primary template `(2.86, 2.86, 4.50)` has `r₁₂ = r₁₃`,
so its symmetry group is the single 2↔3 transposition and **not** `S₃`. The deviation from the
template's **own** group is **exactly `0.000e+00` at every `λ`**, which is what
`WATER_AMENDMENT_7.md` G2's a-priori class partition requires. *(The first version of the
analysis code reported the full-`S₃` deviation, which is `0.03–0.26` here and is not a defect: an
isoceles template does not have that symmetry. A gate keyed to the wrong group is
`GATE_PROPOSAL_PROXY.md`'s reach, and it was caught by checking the group rather than the
number.)*

### 2.3 G-DYE — the detection limit, measured

`GATES.md` reach 1 records the gap this fills: *"No planted-amplitude sweep, so the smallest dye
it can still see through its own floor is unmeasured."* A three-body coupling was planted into the
labels of **real mW configurations**, on a **vertex-disjoint** subset of the real triple list
(disjointness makes the dose exact rather than saturating), with every single-slot marginal held
at 1/2 so nothing recovered can be a composition effect, and read through the byte-identical
pipeline over the **full** triple list:

| planted `ε` | share (nats) |
|---|---|
| 0.00 | 1.08e−05 |
| 0.01 | 1.09e−05 |
| 0.03 | 3.41e−06 |
| **0.10** | **3.79e−04** |
| 0.30 | 1.73e−03 |
| 0.60 | 7.56e−03 |
| 1.00 | 2.21e−02 |

Monotone above the floor; the first three points are all inside the floor's own `p99`
(`6.23e−05`) and their order is noise, which is the definition of a detection limit rather than a
failure (`GATES.md` reach 11: *a reading below the validated detection limit is not a detection*).

> **MEASURED DETECTION LIMIT: `3.8 × 10⁻⁴` nats at 25 configurations, i.e. `ε = 0.10` of the
> disjoint triples.** `WATER_PREREG.md` §6's design sensitivity was **`3 × 10⁻⁵` nats**. **The
> battery is an order of magnitude less sensitive than the design assumed**, and the reason is
> §2.4.

*(Recorded rather than rewritten: the first version of this dye planted by flipping labels on
overlapping triples and came back non-monotone at large `ε`, because a particle in two planted
triples is written twice and the dose saturates. The docimasia caught it, and the fix is the
disjoint subset.)*

### 2.4 N2, the ideal gas — and the single-draw trap, caught on ourselves

The first measurement of the ideal-gas control took **one** realisation at each of four sample
sizes, saw the reading fail to fall as `1/N`, and provisionally read that as a minting **pedestal**
— which would have fired `WATER_PREREG.md` §8 outcome (j). The mechanism check then read the
**same** template at the **same** sample size and got `6.4e−05` against `2.0e−04`, `p = 0.26`
against `p = 0.045`. **Two draws, a factor of three apart.**

> That is this campaign's own memory firing on the campaign: **the share null is `χ²`-shaped, so a
> single draw is not a measurement of it.** `GATES.md` keeps the anchor — Dalitz D7, where a
> single draw of a `χ²`-shaped null read `2.9e−4` and would have fired a kill, and was flat over
> 200 draws.

Redone as a **distribution**, 40 independent ideal-gas ensembles at each size, each with its own
N1a floor drawn on its own positions (`water_n2.py`):

| configs | `N_tri` | N2 median | N2 p99 | N1a median | N1a p99 | median ratio | `P(N2 > N1a)` |
|---|---|---|---|---|---|---|---|
| 5 | 4 041 | 1.727e−04 | 2.840e−03 | 1.143e−04 | 8.662e−04 | 1.51 | 0.623 |
| 12 | 9 646 | 1.148e−04 | 1.058e−03 | 6.088e−05 | 6.054e−04 | 1.89 | 0.605 |
| 25 | 20 174 | 1.444e−04 | 4.916e−04 | 3.556e−05 | 3.912e−04 | **4.06** | 0.715 |
| 50 | 40 362 | 7.655e−05 | 4.404e−04 | 7.531e−06 | 9.053e−05 | **10.16** | 0.858 |

**The ideal gas reads above the label floor, and the gap widens with `N`.** The log-log slope of
the N2 median in `N_tri` is **`−0.287`**, against `−1` for a pure shot-noise floor.

**What this means, stated carefully rather than as a verdict.** The coordination-number label is a
**filter over a neighbourhood**, and at a compact template the three slots' cutoff spheres
overlap, so a single particle in the triple intersection is counted by all three coordination
numbers at once. That is a genuinely three-body coupling written into the labels **by the filter**,
from positions carrying no three-body physics whatsoever. It is exactly the hazard
`WATER_PREREG.md` §5.1 named as *"FACT 3's trap, doubled"* and §2 called *"this campaign's primary
risk"*. **The pre-registration was right about the risk and the risk is real.**

> **Consequence, and it changes the floor of record: the label-permutation and iid-label floors are
> NOT the right null for this design.** They hold the positions and move the labels, and the
> minting lives in the map from positions to labels. **The operative null is an ensemble with the
> right positions statistics and no three-body physics — which is N3, §3.2 — and the ideal gas is
> its zero-structure limit.**

**Outcome (j), adjudicated rather than applied mechanically.** §8(j) as frozen fires when *"N2
reads above its floor"*, and `WATER_AMENDMENT_10.md` J3 made N2 the primary fouling detector. By
the letter, it fires. **We report it as fired, and we report what it fouls: every reading scored
against a LABEL floor.** It does not foul the readings scored against N3, which is the comparison
this document's verdict rests on, and it does not foul the far arm, whose spheres do not overlap
(§3.3). That is `GATES.md`'s axiological layer 3 — a firing gate fouls the minimum necessary —
applied with the boundary stated rather than assumed.

---

## 3. ARM A — THE DOSE, AND THE CONTROL THAT DECIDES IT

### 3.1 The ladder

Seven `λ` passed both gates on the first pass. Count-matched on **triangles** at 3 776 ordered
triples per configuration (G-DOSE; amendment 9 I2), primary template `(2.86, 2.86, 4.50) Å`,
tolerance `0.25 Å`, floor = N1a iid labels on the same positions, `p` = an exact rank test over
300 draws (so `0.0033` is its resolution floor).

| `λ` | `P` (atm) | `p₁` | `N_tri` | share (nats) | floor median | excess | `p` | sharp ceiling | ceil/floor | headroom | rel sd |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20.00 † | −3089 | 0.867 | 1.53e+05 | 1.369e−06 | 3.606e−06 | −2.237e−06 | 0.6811 | 0.00148 | 411 | 0.053 | 458 % |
| 20.50 | −2648 | 0.852 | 1.54e+05 | 6.394e−07 | 3.022e−06 | −2.382e−06 | 0.7674 | 0.00131 | 434 | 0.053 | 849 % |
| 21.50 | −1701 | 0.816 | 1.55e+05 | 3.734e−06 | 3.428e−06 | +3.052e−07 | 0.4784 | 0.00155 | 451 | 0.087 | 223 % |
| 22.00 | −1181 | 0.798 | 1.55e+05 | 6.944e−06 | 2.761e−06 | +4.183e−06 | 0.2691 | 0.00177 | 642 | 0.103 | 151 % |
| **23.15** ‡ | ≈ 0 | 0.747 | **7.59e+05** | 7.445e−06 | 6.506e−07 | +6.794e−06 | **0.0166** | 0.00196 | 3015 | 0.145 | 61 % |
| 25.00 | +1851 | 0.638 | 1.55e+05 | **6.583e−08** | 3.311e−06 | −3.245e−06 | 0.9269 | 0.00246 | 741 | 0.259 | 7078 % |
| **27.00** | +3912 | 0.463 | 1.55e+05 | **4.405e−05** | 3.174e−06 | +4.087e−05 | **0.0100** | 0.00404 | 1272 | 0.496 | 55 % |

† **`λ = 20.00` is EXCLUDED by G-HOMOG on the longer runs** and is shown struck through in effect,
not scored. Its 41-frame reading passed (mean per-frame max void `3.50 Å`); at 201 frames the same
mean rose to `4.94 Å`, above the Poisson-calibrated `4.66 Å`, and its production pressure drifted
between halves (`−3089 → −2110 atm`) where every other point is stable to `< 1 %`. **It is slowly
cavitating**, and the gate found it only when given five times the sampling. Reported because a
gate that changes verdict with sample size is a fact about the gate.

‡ **`λ = 23.15` carries 201 configurations against 41 everywhere else.** Its floor is
correspondingly `5 ×` lower and **its `p` is not comparable to the others' — this is exactly the
Dalitz D2 taint** (`GATES.md`: *a floor is drawn at the SAME sample size as the reading it
gauges*), disclosed rather than absorbed. The matched-length re-run that would remove it is
`NOT RUN` (§7.11).

> **P5′ FIRES. The share is NOT monotone in `λ`, and it is not close.**
>
> * **not monotone in share, and not monotone in the floor-subtracted excess** — checked
>   mechanically, both `False`;
> * the ladder's **smallest** reading (`6.58 × 10⁻⁸` at `λ = 25`) sits **between** its two largest
>   (`λ = 23.15` and `λ = 27`). A dose cannot do that;
> * **five of seven cells are at or below their own floor** (three have *negative* excess);
> * **two cells fall below `p = 0.05` and one below `p = 0.01`** — and with seven points,
>   `P(at least one p < 0.01) = 6.8 %` under the null, so **neither survives the ladder's own
>   multiplicity**;
> * the readings carry **relative standard deviations of 55–7 078 %** by the variance law
>   `√(2 + 8N·share)/(2N·share)`. **At this budget the individual cells have essentially no
>   precision**, which is `WATER_AMENDMENT_3.md` C2's warning arriving exactly as predicted:
>   *the design sensitivity buys DETECTION, not PRECISION, and the two were not distinguished when
>   it was frozen.*
>
> **Verdict: `WATER_PREREG.md` §8 outcome (c), NULL — over this path, in this model, in the
> coordination channel, whole-only structure does not track the three-body coupling.** And §8(c)'s
> own caveat is carried: this is evidence against either the effect or this instrument's ability
> to see it, **and the two are not separated by this design**.

**The far arm, at `r_far = max(3ξ, 7.0 Å)` with `ξ` measured per state point:**

| `λ` | `ξ` (Å) | `r_far` (Å) | far `N_tri` | far share | far floor p99 | far `p` |
|---|---|---|---|---|---|---|
| 20.00 | 2.27 | 7.00 | 3.25e+05 | 1.975e−05 | 5.745e−05 | 0.1528 |
| 20.50 | 2.66 | 7.97 | 4.37e+05 | 4.212e−06 | 4.221e−05 | 0.4751 |
| 21.50 | 2.04 | 7.00 | 3.33e+05 | 3.044e−07 | 6.183e−05 | 0.8140 |
| 22.00 | 1.99 | 7.00 | 3.39e+05 | 1.383e−05 | 6.691e−05 | 0.2326 |
| 23.15 | 1.94 | 7.00 | 1.69e+06 | 1.081e−06 | 1.163e−05 | 0.3654 |
| 25.00 | 1.23 | 7.00 | 3.49e+05 | 6.823e−07 | 4.750e−05 | 0.7807 |
| 27.00 | 1.06 | 7.00 | 3.38e+05 | 4.697e−08 | 4.558e−05 | 0.9369 |

**Every far-arm reading is inside its own floor band. P4 CONFIRMED at every state point.**

**G-OCC, G-LP and G-CEIL all pass on every readable cell**: minimum cell counts `752–22 940`
against the pre-registered `≥ 30`; headroom `0.053–0.496` nats against shares of order `10⁻⁶`;
`ceiling / floor = 411–3 015`, above §5.4's `10 ×` bar and above the amended named-denominator
gate's `≥ 100`. **The orbit deviation of every table — against the template's own 2↔3
transposition, which is its actual symmetry group — is exactly `0.000e+00`.**

**K-DOSE does not fire.** The full-count and count-matched ladders agree in sign at every cell and
neither is monotone; the count-matching changes no verdict.

### 3.1a T1 — the declared advance test, and it PASSES

`WATER_ARM_A_T1.md` was written when the 41-configuration ladder existed and the matched-length
re-run was still in the MD queue. It staked: *if `λ = 27`'s reading is a property of the state
point, the share stays near `4.4 × 10⁻⁵` while its floor falls; if it is a fluctuation of a
`χ²`-shaped null, it falls toward the new floor.*

| | | 41 configurations | **201 configurations** |
|---|---|---|---|
| **full count** | `N_tri` | 2.04e+05 | **1.002e+06** |
| | share | 5.228e−05 | **2.480e−05** |
| | floor median | 1.821e−06 | **4.380e−07** |
| | share / floor | 28.7 | **56.6** |
| | `p` | 0.0033 | **0.0033** (resolution floor) |
| | relative sd | 44 % | **29 %** |
| **count-matched** | `N_tri` | 1.55e+05 | **7.730e+05** |
| | share | 4.405e−05 | **1.312e−05** |
| | floor median | 3.174e−06 | **6.062e−07** |
| | share / floor | 13.9 | **21.6** |
| | `p` | 0.0100 | **0.0066** |
| | relative sd | 55 % | **45 %** |

> **T1 PASSES: the `λ = 27` excess is REAL and reproduces at five times the data, on both count
> modes.** Had it been a floor fluctuation it would have fallen by ~100 × to `≈ 4 × 10⁻⁷`. It fell
> by **2.1 ×** (full) and **3.4 ×** (matched) and stands at **56.6 ×** and **21.6 ×** its own
> floor, with the `p`-value at or near its resolution limit and the relative sd improved in both.
> **`λ = 27` carries a reproducible whole-only excess over its label floor.**
>
> **The fall itself is disclosed and not explained away.** A property of the state point should
> have held its magnitude; a `2–3 ×` fall is larger than the estimator's own finite-`N` bias
> accounts for (`≈ 1/(2N)`, worth `3.2 × 10⁻⁶` at the small `N` and `5 × 10⁻⁷` at the large — a
> tenth of the observed change). **The honest reading is that the 41-configuration number was
> inflated and the 201-configuration number is the estimate of record**, which is the direction the
> disclosure runs against us.

**And it changes nothing about the verdict, for two reasons that are both measured rather than
argued.**

1. **It is not a dose.** `λ = 25`, between `λ = 23.15` and `λ = 27`, remains the ladder's
   *smallest* reading. One reproducible point at the top of a non-monotone ladder is a state
   point, not a trend. **P5′ still fires.**
2. **It sits below the ideal-gas pedestal.** N2 at the same template reads `1.61 × 10⁻⁴` nats
   (§3.2), and `≈ 1.0 × 10⁻⁴` after §2.4's measured `N^{−0.287}` correction to `λ = 27`'s
   `N_tri`. **The pedestal is 4 × the reading**, so by `WATER_PREREG.md` §5.2's own rule
   (*pedestal ≥ 50 % ⇒ VOID*) **the `λ = 27` cell is VOID.**

> **The decisive missing control is named rather than glossed: `λ = 23.15` read `p = 0.0033`
> against its label floor too, and the pair-matched N3 null accounted for essentially all of it
> (excess `+0.65 σ`). `λ = 27` has no N3 of its own — a second IBI potential would have to be
> fitted to `λ = 27`'s own `g(r)` — so its excess is UNGAUGED for the pair-matched null.** On the
> one state point where that control exists, an identical-looking `p = 0.0033` came back
> explained.

### 3.2 The load-bearing control — a pair-potential liquid carrying mW's own `g(r)`

**This is the control `GLASS_RESULTS.md` used to deflate its own headline, and it is what
`WATER_PREREG.md` §5.1 makes the deliverable: not the share, but `share(data) − share(N3)`.**

**How N3 was built, and why not the way glass built its surrogate.** Glass could hold positions
fixed and resample species, because species is an extra degree of freedom. **Here the label is a
function of the positions**, so a label permutation is only the estimator floor and the physical
null must act on the positions — §5.1 says exactly this. N3 is therefore a **tabulated pair
potential built by Iterative Boltzmann Inversion** (Soper 1996; Reith, Pütz & Müller-Plathe 2003)
whose own equilibrium liquid, at mW's density and temperature, reproduces **mW's own measured
`g(r)`**: a liquid with **no three-body term of any kind** whose pair structure is water's.

| | |
|---|---|
| iterations | 30, `α = 0.5`, from the potential of mean force |
| convergence | `rms(g_N3 − g_mW) = 0.0182`, worst `|Δg| = 0.078` |
| `⟨n⟩` inside `r_cut = 3.50 Å`, implied by `g(r)` | **5.098 (mW) vs 5.222 (N3)** — matched to **2.4 %** |
| pressure | **+10 368 atm (N3) vs ≈ 0 atm (mW)** — the classic representability failure of IBI, disclosed: matching `g(r)` does not match the equation of state, and N3 is defined by its `g(r)`, not by its pressure |

**The comparison, at `λ = 23.15`, all three ensembles at 201 configurations through the
byte-identical pipeline:**

| ensemble | `p₁` | `N_tri` | share (nats) | its own floor median | `p` vs its own floor | sharp ceiling |
|---|---|---|---|---|---|---|
| **DATA** (mW) | 0.7466 | 8.470e+05 | **7.273e−06** | 4.784e−07 | **0.0033** | 0.00194 |
| **N3** (IBI pair-matched) | 0.7179 | 6.790e+05 | **2.420e−06** | 8.377e−07 | 0.2259 | 0.00440 |
| **N2** (ideal gas) | 0.7133 | 1.622e+05 | **1.609e−04** | 3.016e−06 | 0.0033 | 0.01275 |

> **`DATA − N3 = +4.85 × 10⁻⁶`, which is 66.7 % of the data's own reading — and it clears
> nothing.**
>
> | bar | `σ` | excess in `σ` |
> |---|---|---|
> | **K4's own letter** — *"5 σ of the N3 ensemble"* | N3's configuration bootstrap, `4.32e−06` | **`+1.12 σ`** |
> | the honest bar — the **difference**'s own bootstrap | `7.51e−06` | **`+0.65 σ`** |
>
> **K4 FIRES, and it fires under BOTH bars, which is the one respect in which this result is
> cleaner than the sibling's.** `GLASS_RESULTS.md` had to report a split — its K1 did not fire by
> its own letter (9.8 σ) and did fire on the paired bootstrap (3.8 σ) — and had to choose. Here
> there is nothing to choose between: `1.12 σ` and `0.65 σ` are both far below 5. **"Water's
> supercooled structure carries whole-only order invisible to `g_OO(r)`" is REFUTED in this
> channel, at this state point, in this model.**

**The denominators, both named** (`GATES.md`, *named-denominator reporting*, as amended):

| | value |
|---|---|
| universal cap, `ln 2` (machine-checked, `Core/ThirdCap.lean` `share_le_log_two`, hypothesis `IsProb` only) | share is **`1.05 × 10⁻⁵`** of it, i.e. **0.00105 %** |
| sharp per-table ceiling (`share_le_grouping_gaps`, class-partitioned per amendment 7 G2) | `0.00194` nats; share is **`3.75 × 10⁻³`** of it, i.e. **0.375 %** |
| sharp cap ÷ this cell's own floor | **4 056** — far above the `≥ 100` bar the amended gate requires before a sharp fraction may be quoted at all |

**Both fractions carry a `58.1 %` relative standard deviation** (`√(2 + 8N·share)/(2N·share)`, the
law confirmed on real cells by `GLASS_RESULTS.md` §2.2a-i). Per `WATER_AMENDMENT_3.md` C2 they are
**context, not the reporting unit, and no verdict is scored on them.** G-OCC passes with room to
spare — occupancy `1.00`, minimum cell `22 940`.

**And the number that says most about the design:**

> **The ideal gas reads `1.61 × 10⁻⁴` nats — twenty-two times MORE than mW does.** A structureless
> Poisson point process, pushed through the same template selection and the same coordination
> filter, manufactures far more whole-only share than the real three-body liquid carries. It is
> `53 ×` its own floor where the data is `15 ×` its own and N3 is `2.9 ×` its own.
>
> *(The ideal gas closes fewer triangles at this template — `N_tri = 1.62e5` against the data's
> `8.47e5` — so part of the gap is finite-`N`. Correcting with §2.4's measured scaling
> (`N^{−0.287}`) puts it at `≈ 1.0 × 10⁻⁴` at the data's `N_tri`, still **14 ×** the data. That
> correction is an extrapolation from four points and is labelled as one.)*

**By `WATER_PREREG.md` §5.2's own rule — *pedestal ≥ 50 % of the reading ⇒ that rung is VOID* —
the primary reading is VOID.** The pedestal is 2 200 % of it.

### 3.3 A methodological finding: the permutation test on ensemble membership is invalid here

`water_arm_a_null.py` also ran an exact permutation test on ensemble membership, which
`GLASS_PREREG.md` §6.1 recommends because the configuration bootstrap overstates the uncertainty
of a non-negative statistic near its boundary. **It returns `p = 0.0005` — the resolution floor —
in flat contradiction to the bootstrap's `z = +0.65`.** The contradiction is the permutation
test's, and the reason is worth recording:

> **A permutation test on ensemble membership assumes the two ensembles are exchangeable under
> the null. DATA and N3 are not**: they differ in composition (`p₁ = 0.7466` vs `0.7179`) and in
> triples per configuration (4 214 vs 3 378). Permuting therefore builds two **mixtures** of
> nearly identical composition, whose share difference is near zero by construction — so **any**
> real difference between the ensembles looks extreme against that null. **The test is answering
> "are these two ensembles identical?", to which the answer is obviously no, and not "is the
> excess larger than its own uncertainty?", which is the question.**

**The bootstrap is the instrument of record for this difference and the permutation test is
reported as invalid rather than as a disagreement.** This is the mixture channel of `GATES.md`
reach 3 appearing inside a *test statistic* rather than inside a null ensemble, and it would have
inverted this document's verdict if taken at face value.

### 3.4 The far arm, and where the minting comes from

The far arm at `r_far = max(3ξ, 7.0 Å)` reads **at floor at every `λ`** (`p = 0.15–0.94`), and it
reads at floor on the **ideal gas** too. That is not a coincidence and it locates the mechanism of
§2.4:

> At the primary template the three slots are mutually within `2 r_cut`, so their coordination
> cutoff spheres have a **common triple intersection**, and a single particle sitting in it is
> counted by all three coordination numbers at once — an irreducibly three-body coupling written
> into the labels **by the filter**. At `r ≥ 7.0 Å = 2 r_cut` no three cutoff spheres share a
> point, and the minting **vanishes**. **The far arm is not only a plumb line for the pipeline; it
> is the control that identifies what the pipeline is doing at short range.**

---

## 4. ARM B — THE KOB–ANDERSEN BASELINE, AND IT DOES NOT BEHAVE LIKE ARM A

Arm B reads **this campaign's coordination label** on **the glass campaign's own configurations**,
under the three conditions `WATER_AMENDMENT_1.md` A3 attached, all honoured: `glass/compact/*.npz`
and never the tarballs; the count-matched cap `1300` taken **on triangles** (A3(2) as superseded by
amendment 9 I2); every RNG seeded and recorded.

**Two `r_cut` were declared before the run** (`water_arm_b.py`'s docstring), because §1.3 makes the
outcome predictable rather than a surprise:

* **`B-own`** — `r_cut =` Kob–Andersen's **own** measured first minimum of `g(r)`, `1.4175 σ`. The
  campaign's own rule transferred literally. **Predicted to be label-degenerate.**
* **`B-matched`** — `r_cut = 1.0599 σ`, set so the **ideal-gas** coordination at KA's density
  equals the ideal-gas coordination at mW's density and `r_cut = 3.50 Å`, namely `5.99`. Matches
  what the label can *resolve* rather than what the geometry is *called*.

Kob–Andersen: `N = 4096`, `L = 15.0522`, `ρ = 1.2010 σ⁻³`; measured `g(r)` first peak `1.058 σ`,
first minimum `1.417 σ`. 40 configurations per temperature, cap 1300 on triangles, tolerance
`0.10` (glass's own).

**`B-own`, `r_cut = 1.4175 σ` — the advance prediction, confirmed at all four temperatures**

| template | `T` | `p₁` | `N_tri` | share | ceiling | min cell |
|---|---|---|---|---|---|---|
| 1.30 | 0.44 | **1.000** | 5.09e+04 | **0.0** | 0.0 | 0 |
| 1.30 | 0.50 | **1.000** | 5.18e+04 | **0.0** | 0.0 | 0 |
| 1.30 | 0.56 | **1.000** | 5.18e+04 | **0.0** | 0.0 | 0 |
| 1.30 | 0.64 | **1.000** | 5.18e+04 | **0.0** | 0.0 | 0 |

> **`p₁ = 1.000` at every temperature. The table collapses into one cell, the `ThirdCap` ceiling is
> exactly zero, and the reading is UNGAUGED — not a floor.** §1.3's mW finding replicates on a
> different substrate, a different potential, a different code and a different unit system, and it
> was **predicted before the run** in `water_arm_b.py`'s own docstring.

**`B-matched`, `r_cut = 1.0599 σ` — the only version in which P6/P8 are scorable**

| template | `T` | `p₁` | `N_tri` | share (nats) | floor median | `p` | sharp ceiling | share/ceiling | share/ln 2 | headroom | min cell |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **1.30** | 0.44 | 0.599 | 5.09e+04 | **1.9797e−03** | 2.472e−05 | 0.0050 | 0.04560 | 4.34 % | 2.86e−03 | 0.478 | 4724 |
| | 0.50 | 0.627 | 5.18e+04 | **1.1906e−03** | 2.669e−05 | 0.0050 | 0.03037 | 3.92 % | 1.72e−03 | 0.540 | 5146 |
| | 0.56 | 0.647 | 5.18e+04 | **9.4698e−04** | 2.903e−05 | 0.0050 | 0.02200 | 4.31 % | 1.37e−03 | 0.578 | 5246 |
| | 0.64 | 0.671 | 5.18e+04 | **3.8740e−05** | 3.144e−05 | 0.4527 | 0.01438 | 0.27 % | 5.59e−05 | 0.567 | 4834 |
| 1.50 § | 0.44 | 0.599 | 5.18e+04 | 7.9222e−04 | 2.472e−05 | 0.0050 | 0.00167 | **47.6 %** | 1.14e−03 | 0.223 | 576 |
| | 0.50 | 0.627 | 5.18e+04 | 1.0206e−04 | 2.617e−05 | 0.1692 | 0.00020 | **49.8 %** | 1.47e−04 | 0.190 | 594 |
| | 0.56 | 0.647 | 5.18e+04 | 2.0086e−04 | 3.172e−05 | 0.0647 | 0.00034 | **59.4 %** | 2.90e−04 | 0.179 | 498 |
| | 0.64 | 0.671 | 5.18e+04 | 1.5566e−04 | 2.932e−05 | 0.1095 | 0.00016 | **99.4 %** | 2.25e−04 | 0.161 | 468 |

§ **Every `r = 1.50` cell is UNGAUGED by the campaign's own §5.4 rule**: `ceiling / floor` reads
`68, 7.6, 10.7, 5.5`, at or below the pre-registered `10 ×` bar, and far below the amended
named-denominator gate's `≥ 100`. The reading reaching **99.4 % of its own proved ceiling** at
`T = 0.64` is the tell. **No verdict is scored on that template**, and it is shown because a gate
firing is reported as loudly as a reading.

**At `r = 1.30`, which is clean:**

> **P6 CONFIRMED — no interior peak.** The reading is monotone in `T` across all four rungs.
>
> **P8 CONFIRMED — and it was staked by the glass campaign before it saw any coordination
> reading.** The coordination label agrees with glass's species label in **monotonicity and
> sign**: both grow on cooling, neither has an interior maximum. **The two labels do not
> disagree, so amendment 1 A4's "chase it" clause is not triggered.**
>
> **And the named-denominator gate reproduces exactly, on a new label:** raw cold/hot
> **`× 51.1`**, against the sharp ceiling **`× 16.1`** — because the ceiling itself grows
> **`× 3.17`**. Against `ln 2` the reading moves `2.86e−03 → 5.59e−05`. `GLASS_RESULTS.md` measured
> the same structure with the species label (`× 2.41` raw, flat against the sharp cap, the cap
> itself doubling). **Two different labels on byte-identical configurations, and in both the
> growth of the raw reading is partly the growth of its own denominator.** Here, unlike glass's
> `r = 1.30`, the trend **survives** the correction — `× 16.1` is not flat.

**Arm B's far arm (`r = 5.00 σ`, well beyond `2 r_cut = 2.12 σ`)** reads `2.04e−04` at `T = 0.44`
(`p = 0.0796`) and `3.44e−06` at `T = 0.50` (`p = 0.786`); its ceilings are `2.2e−04` and
`2.0e−05`, giving `ceiling / floor` of `8.0` and `0.6` — **below §5.4's `10 ×` bar, so those cells
are UNGAUGED and are not scored either way.** The remaining two temperatures did not complete
(§7.12). **Arm B's far arm therefore does NOT discharge P4 on that substrate**, and no far-arm
pass is claimed for Kob–Andersen.

### 4.1 But arm B's reading is UNGAUGED for the minting channel

`r_cut = 1.0599 σ` with templates at `1.30 σ` and `1.50 σ` puts both **below `2 r_cut = 2.12 σ`**,
so the three slots' cutoff spheres overlap and **the minting channel §2.4 measured on arm A is
open here too**. `water_arm_b_n2.py` was written to read glass's own `SYNTH_ideal` control through
the byte-identical pipeline and **did not complete** (§7.12).

> **Until it does, arm B's `B-matched` readings are UNGAUGED for template-selection and filter
> minting — not clean, not fouled.** The direction of the hazard is known and stated: on arm A the
> ideal gas read `22 ×` the data at the analogous template. **No claim is made that the
> Kob–Andersen coordination reading is beyond-pair structure**, and P6/P8 are scored on
> *monotonicity in `T`*, which a temperature-independent pedestal cannot manufacture — that is
> why those two survive the gap and a magnitude claim would not.

---

## 5. THE SCORECARD — every pre-registered stake, marked

### 5.1 The forward predictions

| | stake | outcome |
|---|---|---|
| **P1** | **the double peak** — two interior maxima straddling `P_W`, each ≥ 5 σ above the minimum between them, on an isotherm crossing the Widom line | **NOT RUN.** Requires arms C/D (TIP4P/2005 isotherms), which did not run (§7.1). **This is the intellectual centre of the pre-registration and it is untested.** No verdict is scored on it |
| **P2** | the single-peak alternative, staked as a distinguishable competitor | **NOT RUN**, same reason |
| **P3** | the peak-to-dip contrast grows as `T → T_c` over three isotherms | **NOT RUN**, same reason |
| **P4** | **the far arm reads floor** — below 3 × its own matched floor `p99`, at every state point | **CONFIRMED at every readable `λ`.** `p = 0.15–0.94`; every reading inside its own floor band. And it is a *stronger* pass than the pre-registration could promise, because `ξ` was **measured** (1.06–2.66 Å) rather than assumed, so `r_far = max(3ξ, 7.0 Å)` is licensed rather than inherited (`WATER_AMENDMENT_10.md` J1–J3), and `3ξ ≤ 7.97 Å ≪ L/2 = 19.58 Å`, so the far arm **exists** at every point |
| **P5** | **the three-body dose** — share rises monotonically with `λ`, and reads floor at `λ = 0` | **UNGAUGED.** Not confirmed and not fired. The `λ = 0` end is two-phase at matched density (§1.1) and label-degenerate at its own ambient density (§1.3); both are disqualifying on their own. See `WATER_AMENDMENT_12.md` L4 |
| **P5′** | **the rescoped dose** (amendment 12 L5) — share rises monotonically with `λ` over the window passing G-HOMOG and G-LABEL | **FIRES.** Not monotone in share and not monotone in the floor-subtracted excess; five of seven cells at or below their own floor; the ladder's smallest reading sits between its two largest (§3.1) |
| **P6** | the Kob–Andersen pair-potential baseline shows **no interior peak** of the P1/P2 kind under the same coordination label | **CONFIRMED at `r = 1.30`** — monotone in `T` on all four rungs, no interior maximum. `r = 1.50` is UNGAUGED on ceiling grounds and is not scored (§4) |
| **P7** | **LP headroom ≥ 30 × the measured share** at every read cell (VOID at 3 ×) | **CONFIRMED with an enormous margin** — headroom `0.053–0.496` nats against shares of order `10⁻⁶`, i.e. ratios of `10⁴–10⁵`. **But the margin is large for the uninteresting reason**: a reading at its floor is trivially not pair-pinned. P7 was staked to catch a *signal* that turned out to be a restatement of the pair marginals, and there is no signal here for it to catch. Reported as passed and as uninformative |
| **P8** | arm B's coordination label reads **monotone in `T`**, agreeing with glass's species reading in sign — staked by the glass campaign before it saw any coordination reading | **CONFIRMED.** Monotone in `T`, same sign as glass's species reading, no interior peak. The two labels agree on byte-identical configurations, so amendment 1 A4's "chase the disagreement" clause is not triggered. **Magnitude is NOT claimed** — arm B's ideal-gas control did not run (§4.1) |
| **T1** | (`WATER_ARM_A_T1.md`, staked before the matched-length re-run was analysed) the `λ = 27` excess **persists** at 5 × the data | **PASSES.** Share `4.41e−05 → 2.48e−05` while the floor fell `7.2 ×`; **56.6 × its own floor**, `p` at its resolution limit, relative sd halved. A floor fluctuation would have fallen ~100 ×. The excess is real — **and the cell is still VOID on the ideal-gas pedestal, and UNGAUGED for the pair-matched null** (§3.1a) |

**And one advance prediction this arm made and confirmed, which is not in the pre-registration
because it could not have been:** `water_arm_b.py`'s docstring, written before arm B read
anything, predicted that **the `n ≥ 5` label would saturate on Kob–Andersen at its own first
minimum of `g(r)`**, on the strength of §1.3's mW measurement. It does: **`p₁ = 1.000`** at
`r_cut = 1.4175 σ`, with the table collapsed into one cell, `ceiling = 0`, `min cell = 0`.
**§1.3's finding replicates on a different substrate, a different potential, a different code and
a different unit system.**

### 5.2 The kills

| kill | fired? | |
|---|---|---|
| **K1** — the campaign's premise | **UNGAUGED — which is not a pass** | K1's distinguishing observation is a floor reading at `λ = 0`, and that observation is unavailable at any density (§1.1, §1.3). Reported as loudly as a firing, per `GATES.md` axiological layer 1 |
| **K2** — the shape claim | **NOT RUN** | no isotherm was run, so no interior structure was looked for |
| **K3** — the double-peak claim | **NOT RUN** | same |
| **K4** — the excess over N3 | **FIRES, under both bars** | `+1.12 σ` by K4's own letter (5 σ *of the N3 ensemble*) and `+0.65 σ` on the difference's own bootstrap. Unlike the sibling campaign there is nothing to choose between the two readings (§3.2) |
| **K-VOID** — the instrument | **SPLIT, and reported split** | the **far arm passes at every state point** (P4). The **ideal-gas control N2 does not**: it reads above the label floor and the gap grows with `N` (§2.4). By §8(j)'s letter that fouls the pipeline; by amendment 10 J3, N2 is the primary fouling detector and carries the weight. **We report it as fired, on the readings scored against a LABEL floor, and state its boundary rather than assume one** (§2.4) |
| **K-PIN** | **DID NOT FIRE** | headroom `10⁴–10⁵ ×` the reading everywhere; no cell is pair-pinned |
| **K-MINT** | **NOT DISCHARGED** | the §5.2 binmint pedestal battery was not run in its pre-registered form (§7.8). §2.4 bounds the same channel from another direction and is **not** reported as a discharge |
| **K-DOSE** | **DID NOT FIRE** | full-count and count-matched ladders agree in sign at every cell; neither is monotone; count-matching changes no verdict (§3.1) |
| **K-CEIL** | **DID NOT FIRE** on the readable window | every readable cell has `ceiling / floor ≈ 400–1500`, far above §5.4's `10 ×` bar — and above the `≥ 100` bar `GATES.md`'s amended *named-denominator* gate requires before a sharp fraction may be quoted at all. It **DID** fire, in advance and by design, on every `λ ≤ 18` cell, whose ceiling is `0` (§1.3, W8) |
| **K-DYE** | **NOT DISCHARGED for N3** | §7.4 |

---

## 6. THE HEAD-TO-HEAD WITH `GLASS_RESULTS.md`

**This comparison is the campaign's whole discriminating value and it was set up in advance.**
`WATER_PREREG.md` §1: *"The concurrent glass campaign reads a system whose interactions are
pairwise by construction… Here it can read structure a pair potential **cannot** generate. That is
the whole reason for this campaign."* The two campaigns share the estimator byte-identically
(`glass_share.py`), share the enumerator, share the triangle cap, share the ceiling rule, and
share the floor discipline. **What they do not share is the label**, and that turns out to be
where the whole difference lives.

**Every number in the glass column is `received-not-measured`** — read from `GLASS_RESULTS.md`,
not recomputed here from glass's configurations.

| | **glass (Kob–Andersen, species label)** | **water (mW, coordination label)** |
|---|---|---|
| interactions | **pairwise by construction** (binary Lennard-Jones) | **three-body** (Stillinger–Weber, `λ = 23.15`) |
| label | **species** — an atomic alphabet, no binning channel by construction | **first-shell coordination thresholded at `n ≥ 5`** — an integer, but a *filter over a neighbourhood* |
| control parameter | temperature, `T = 0.64 → 0.44` (a factor `2.5 × 10⁵` in `τ_α`) | the three-body coupling `λ`, over the window where the label works |
| **raw reading** | **grows ×44** on cooling (×54 count-matched); monotone on all four rungs; exact permutation `p = 0.0010` | **at floor at every readable `λ`**; no monotone dose |
| **pair-matched null** | reproduces **82–94 %** of the reading at every rung | reproduces the reading **within the floor** — there is nothing left over to attribute |
| **beyond-pair excess** | `+3.82 σ` at `T = 0.44`, `+2.3` to `+3.8 σ` elsewhere; below the pre-registered `5 σ` | **consistent with zero** |
| ideal-gas control | **clean at all eleven templates**, no `p` below 0.05 | **reads above the label floor and the gap grows with `N`** (§2.4) |
| far arm | at floor (`≤ 5e−7` nats) | at floor at every `λ` |
| its own kill | **K1 fires on the honest error bar**: excess supported in sign, not cashed at the bar it set | **K1 UNGAUGED**: the premise test could not be run at all |

**The three findings that come out of putting them side by side.**

**(i) The prediction that motivated this campaign is not confirmed, and the direction is the
opposite of the one staked.** The pre-registration expected the pair-potential system to be the
*deflation control* and the three-body system to be where the instrument finally read real
physics. What happened is the reverse: **the pair-potential glass former gave a large, monotone,
gate-surviving reading with a small but nonzero beyond-pair excess, and the three-body liquid gave
nothing.** If the whole-only share were tracking three-body *interaction* physics, this is not the
ordering it should produce.

**(ii) But the two are not comparable in the way the pre-registration assumed, and the reason is
the label.** Glass's species label is an extra degree of freedom carried by the particles;
water's coordination label is a **function of the positions**. §5.1 of the pre-registration
identified this as the structural difference between the campaigns and drew the right conclusion
for the *null* (the physical null must act on the positions). What neither campaign anticipated
is the consequence for the *signal*: a label that is a function of the positions can only carry
whole-only structure that survives being read through a neighbourhood filter, and §2.4 measures
that the filter itself mints. **Glass's reading is carried by `P(BBB)` doubling on cooling — a
compositional fact with no positional-filter analogue.** The honest statement is therefore not
"three-body physics has less whole-only structure than pair physics"; it is **"these two readings
are of different objects, and the campaign that set them against each other did not notice until
it ran both."**

**(iii) Where the two campaigns independently converged, they converged hard.** Both measured the
overlap penalty rather than assuming a closed form (glass `2.7–18.1 ×`, water `1.859 ×` on real
configurations against `1.9 ×` predicted from synthetic proxies). Both found the min-of-three
ceiling estimator biased and adopted the class partition. Both found the ordered-triple cap
breaking slot exchangeability and fixed it on triangles. Both have **exactly one** null-generator
family where `GATES.md` requires two, and both disclose it. **Neither campaign's methodological
findings depended on its headline, which is the one respect in which this pairing worked as
designed.**

---

## 7. WHAT DID NOT COMPLETE — named, not omitted

`WATER_PREREG.md` §8(i) requires every pre-registered arm that did not run to be listed **by name**
with its reason, and forbids scoring a verdict on it.

1. **Arms C and D — the TIP4P/2005 isotherms across the Widom line, and with them P1, P2, P3 and
   K2, K3.** **NOT RUN.** §7 priced them at ~1 day of a free GPU (rung 1–2) and ~10 days contended
   (rung 3) and made them conditional on the GPU being free; more decisively, arm A's own result
   removes their premise as stated — the coordination label was to have been validated as a
   three-body probe by P5, and P5 came back ungauged. **The double-peak prediction P1, which is
   the intellectual centre of the pre-registration, is untested.** No verdict is scored on it.
2. **Arm E — the LLCP itself.** **NOT RUN, and declared out of reach before the campaign began**
   (§7): two to four orders of magnitude in wall time short, on a shared laptop-class GPU. That
   verdict is unchanged.
3. **The ST2 model, and the `q_tet` / `d₅` / LSI secondary label designs** (§2.2). **NOT RUN.**
4. **N3's own dye test (K-DYE), in the form §5.1 specifies.** The pre-registration required N3 to
   be shown able to *fail* to reproduce a planted three-body coupling while reproducing `g(r)`.
   **The IBI null was built and converged, but the planted-coupling dye was not run on it.**
   §5.1's own words apply: *a control that cannot see the dye returns "ungauged", not "clean"*.
   **This is the largest undischarged requirement on §3.2's verdict** and it is stated here rather
   than in a footnote. What partially substitutes — and it is a substitution, not a discharge — is
   that IBI reproduces `g(r)` to `rms 0.018` while being a strictly pairwise Hamiltonian, so by
   construction it carries no three-body term to reproduce.
5. **N3's cross-check against the `λ = 0` liquid.** §5.1 required N3 and the mW `λ = 0` liquid to
   agree, and said that if they disagree *both* are ungauged. **The cross-check is unavailable**:
   §1.1 and §1.3 measure the `λ = 0` liquid as two-phase at matched density and label-degenerate
   at its own ambient density. N3 therefore stands alone, which is weaker than the
   pre-registration budgeted for.
6. **A second, independent N3 family.** `GATES.md`'s *null-construction sweep* requires any
   surrogate-normalised reading to be reported under at least two defensible null constructions
   with the spread quoted as a systematic. **Only IBI was built.** Reverse Monte Carlo, named in
   §5.1 alongside it, was not run. **This is the same gap `GLASS_RESULTS.md` §7(1) discloses**,
   reached independently by both campaigns.
7. **The hot/cold start check at `λ = 23.15`** (§1.4): the cold start did not melt within 600 ps
   and is **NOT RUN** per §5.6, leaving that state point's check 1 **undischarged**.
8. **The binmint pedestal battery of §5.2 in its full pedestal form** — the fine
   `(coordination bin, radial sub-bin)` alphabet, merged, with the merge's own manufactured share
   read off. **NOT RUN.** What was run instead, and reported in §2.4, is the ideal-gas control as
   a distribution, which bounds the same channel from a different direction but is **not** the
   pre-registered pedestal and is not reported as one. The `Δ` and `r_cut` ladders of §5.2 were
   also **not** run.
9. **G-MIX**, the endpoint-mixture null of §5.5. **NOT RUN.** It was pre-registered to gauge
   *interior structure* (P1's double peak, P2's single peak), and no interior structure survived
   to be gauged; but the arm is listed because it did not run, not because it was unnecessary.
10. **G-CERT** is **vacuous** here and is reported as vacuous rather than as a pass: the primary
    2×2×2 reading is exact, one-dimensional, bisected to machine precision, and uses no solver, so
    there is no primal/dual bracket to compare. No fine-alphabet maxent solve was performed.
11. **The matched-length `λ` ladder.** The six short `λ` points were re-simulated at the same
    production length as `λ = 23.15` (`water_mw_sweep_matchN.json`, complete), **but the analysis
    over all six at 201 configurations did not finish** — the box was saturated by three
    concurrent campaigns and the far arm's triangle count at `r_far = 8.70 Å` dominates the cost.
    **The ladder of record therefore carries 41 configurations at six `λ` and 201 at `λ = 23.15`,
    and that mismatch is disclosed in §3.1 rather than absorbed.** What *was* run at 201
    configurations is `λ = 27` (the declared T1 test, §3.1a) and `λ = 23.15` (§3.2). The
    configurations exist on disk; the analysis is a re-run away.
12. **Arm B's own ideal-gas control** (`water_arm_b_n2.py`, written but not completed), and
    **arm B's far arm at `T = 0.56` and `T = 0.64`**. Without the first, arm B's `B-matched`
    readings are **UNGAUGED for the minting channel** (§4.1) and no magnitude claim is made from
    them; without the second, and given that the two completed far-arm cells are themselves
    ungauged on ceiling grounds, **P4 is not discharged on the Kob–Andersen substrate.**
13. **An N3 pair-matched null at any `λ` other than 23.15.** One IBI potential was fitted, to
    `λ = 23.15`'s `g(r)`. **`λ = 27`'s reproducible excess therefore has no pair-matched null**,
    which is the single most consequential gap in this document: on the one state point where that
    control does exist, an identically-significant reading came back fully explained by it.

## 8. WHAT IS NOT CLAIMED

1. **Nothing about experimental water.** One simulated model, mW, at one temperature.
2. **No resolution of the LLCP dispute, and no reading anywhere near `T_c`.** Every state point
   here is at 298 K. The campaign's own ceiling was `|T − T_c| ≈ 27–48 K` and it did not get
   there; this arm is at `|T − T_c| ≈ 105–126 K`.
3. **No priority.** `WATER_PRIOR_ART.md` §1 records six prior programmes on the same physical
   question. The most this campaign may claim is a *different, non-negative* object.
4. **No claim about the orientational channel.** The oxygen sublattice only.
5. **No claim that the null is a null about water's three-body structure in general.** It is a
   null about **positional whole-only structure in the coordination channel, at one template, at
   one temperature, in one model** — and §1.3 shows the channel is a narrow one.
6. **No claim that P5 was tested.** It was not. K1 is UNGAUGED.
7. **No claim that the readable `λ` window is water.** `λ = 25` and `λ = 27` are *more*
   tetrahedral than water and are not models of anything; they are dose points.
8. **No stance implication.** `wild-share` does not move; `Stance.lean` is not opened; no Lean
   file is edited; `lake` is not run; nothing is pushed.

## 9. FILES

| file | what it is |
|---|---|
| `WATER_PRIOR_ART.md` | the credit block; part of this document by reference |
| `WATER_PREREG.md` | the pre-registration, frozen before any water configuration existed |
| `WATER_AMENDMENT_1.md` … `_11.md` | the amendments, all written before any configuration existed |
| `WATER_ARM_A_GATE.md` | the mW docimasia on published properties only, `feae80c` |
| **`WATER_AMENDMENT_12.md`** | **the gate firing and the rescope, written after the configurations existed and before the first share** |
| **`WATER_ARM_A_T1.md`** | **the advance test on the `λ = 27` excess, staked before the matched-length re-run was analysed** |
| `water_mw.py` | arm A instrument; extended here to record production-averaged pressure and to support the cold start |
| `water_homog.py` / `*_homog.json` / `water_homog.log` | the §5.6 equilibration gate; computes no share |
| `water_arm_a.py` | the analysis library (dump reader, coordination filter, triangle cap, orbit group, class-partitioned ceiling, floors) |
| `water_arm_a_gate.py` / `.json` / `.log` | its docimasia |
| `water_arm_a_run.py` / `water_arm_a.json` / `.log` | the dose run |
| `water_n2.py` / `.json` / `.log` | the ideal-gas control measured as a distribution |
| `water_ibi.py` / `water_ibi.json` / `.log` | the N3 pair-matched null, by Iterative Boltzmann Inversion |
| `water_arm_a_null.py` / `.json` / `.log` | data against N3 and N2 at matched size |
| `water_arm_b.py` / `.json` / `.log` | the Kob–Andersen baseline |
| `water_arm_a_queue.sh` | the run driver |
| `glass_share.py`, `glass_gate.py` | inherited byte-identically from the glass campaign and not rewritten |

**Numbers taken from a sibling's file rather than re-derived here**, tagged per `GATES.md`
*received numbers are not measured numbers*:

* every number in §6's `GLASS_RESULTS.md` column is **received-not-measured** — read from that
  document, not recomputed from glass's configurations by this campaign;
* `GLASS_PREREG.md` §6.1's block-bootstrap inflation factor (`≈ 2.2 ×`) is
  **received-not-measured** and is used only as a reason to prefer a permutation test, never as a
  correction applied to a number;
* `glass_gate.json`'s nine passing checks are **received-not-measured**; this campaign re-ran
  `glass_share.py` through its own docimasia instead of re-deriving them.

Everything else in this document was computed by the files listed above, in this session, from
configurations generated in this session.

Primary seed **20260727**. MD is not bitwise reproducible on a threaded build; the initial
configuration, the seed, the integrator settings and the engine version (LAMMPS 20250722) are
recorded, and the **analysis** is bitwise reproducible from the stored dumps.
