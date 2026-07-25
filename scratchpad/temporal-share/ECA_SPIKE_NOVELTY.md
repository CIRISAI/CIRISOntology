# NOVELTY ADJUDICATION — the ECA noise spike

Adjudicates `scratchpad/ECA_SPIKE_RESULTS.md` (`95d1b3c`) against the published record, to the
standard set by `SPIKE_SURVEY.md` (`1ffb17a`): for each candidate, (1) is the quantity actually
**pairwise-blind** — a maxent-over-pairs entropy gap, connected information of order ≥ 3 — or is it
lower-order wearing higher-order clothes? (2) data or model? (3) was a noise parameter swept and an
interior peak found? Only YES on all three is a scoop; partial overlaps are neighbours and get
credit lines, not kills.

Scratchpad only. Nothing here touches the Lean library, `Stance.lean` or the audit.

---

## VERDICT

| question | verdict |
|---|---|
| **(1)** connected information / pairwise-maxent gap measured on cellular automata, at all | **SCOOPED** — twice, independently: Kahle–Olbrich–Jost–Ay (2009) and Chliamovitch–Chopard–Velasquez (2014/2019) |
| **(2)** noise-induced *enhancement* of an irreducible third-order dependency, in any system | **SCOOPED** — Schneidman, Still, Berry & Bialek (2003), Fig. 2, the paper that defines our quantity |
| **(3)** O-information vs connected information disagreeing on the same distributions | **SCOOPED** — Schneidman et al. (2003), Fig. 1, in **both** signs |
| the **combination** (pairwise-blind instrument × dynamical noise × spatially extended system, family-wide and exact) | **CONVERGENT-ADJACENT** — not in print, credit paragraph below |

Assume-convergent was the right prior. Every one of the three headline framings in
`ECA_SPIKE_RESULTS.md` is in print, and two of the three are in the founding paper we already
cite. This adjudication was closed against primary text (PDF extraction), not abstracts, and two of
the findings were re-derived with this repository's own instrument.

**Two mechanism controls we never ran now fire against the memo.** They are §5 and they matter
more than the credit question.

---

## 1. Connected information on cellular automata — SCOOPED, twice

### Kahle, Olbrich, Jost & Ay, *Phys. Rev. E* **79**, 026201 (2009) — [arXiv:0806.2552](https://arxiv.org/abs/0806.2552)

Defines, verbatim:

> I^(k)(P) := D(P ‖ E_{k−1}) − D(P ‖ E_k)

with `E_k` the exponential family of k-interactions, projection by iterative proportional fitting.
Since `D(P‖E_k) = H(P̃^(k)) − H(P)`, this **is** `I_C^(k)`, algebraically. Pairwise-blind: yes.

Computed on elementary cellular automata — rules 18, 20, 22, 30, 45, 50, 54, 90, 110, 126, 150 —
in two settings: the invariant measure (length-14 windows cut from length-20000 CA, 10⁶ steps) and
the 3 → 1 elementary interaction cone.

**Their Table II contains our P1 gate.** Rule 90 under uniform inputs reads `I^(3) = 1` bit
exactly; rule 150 reads `I^(4) = 1`. Our "rule 90 is parity, so it must read ln 2 — a gate, not a
finding" was published as a measurement in 2009. They also derive the parity result in general:

> "Y is the set of all configurations with even parity. It can be seen that for this distribution
> I^(N) is maximal while all other components vanish."

They attribute the measure to Amari (2001), not to Schneidman. **No noise anywhere** — the CA are
strictly deterministic.

### Chliamovitch, Chopard & Velasquez — [arXiv:1408.0368](https://arxiv.org/abs/1408.0368); journal version Chliamovitch, Velasquez Reynaga, Falcone & Chopard, *Int. J. Parallel Emergent Distrib. Syst.* **34**(1):142 (2019)

Defines (their eq. 8):

> C_k := D(p, p_ME^(k−1)) − D(p, p_ME^(k)) ≥ 0

and names it themselves, knowingly:

> "This quantity is sometimes referred to as the connected multi-information of order k [4], but in
> our opinion this name is unfortunate (where does connectedness enter into the play ?) and will not
> be used here."

Their ref. [4] **is** Schneidman, Still, Berry & Bialek (2003). Pairwise-blind: yes.

Computed on **all 88 inequivalent ECA rules**, ring topology, N = 4…14 — and by **exact
propagation of the probability density, explicitly rejecting sampling**:

> "Often this is done by means of Monte-Carlo methods… Here we follow an alternative approach which
> is to determine the time evolution of the probability density exactly. Then we may, so to speak,
> follow simultaneously all trajectories down to the least probable ones."

That is our exact-refuter move, twelve years earlier, on the same substrate, with the same
justification. They sweep Langton's λ and system size N. **The string "noise" occurs zero times in
the paper** (grep of the extracted text).

**Consequence.** "First measurement of connected information on cellular automata" is false, and
"we deleted the estimator question by propagating exactly" is not novel methodology on this
substrate. What neither paper did is add noise.

---

## 2. Noise creating irreducible third-order structure — SCOOPED by the founding paper

**Schneidman, Still, Berry & Bialek, *Phys. Rev. Lett.* **91**, 238701 (2003)** — the paper that
defines `I_C^(k)`, already cited throughout `SPIKE_SURVEY.md` — sweeps noise amplitude from 0 to
0.5 on three boolean gates in its **Figure 2**, under three noise channels (output noise, input
noise, input-dependent output noise). The text, verbatim:

> "When we add noise either to the input or output of the boolean functions (Fig. 2) we degrade the
> correlations, but more interestingly we find that pure 2-body interactions such as AND and OR show
> a 3-body interaction component for some types of noise (even for noise sources which are state
> dependent). For the pure 3-body XOR, noise may result in the appearance of 2-body interactions."

Their Figure 1 gives AND and OR `I_C^(3) = 0` **exactly**. So the sentence above says, in print in
2003: *noise creates irreducible third-order structure in a system that has none.* That is our
headline.

**Re-derived here with our own exact solver** (`verify_schneidman.py`), AND under output noise:

| P(flip σ₃) | 0 | 0.001 | 0.01 | 0.05 | **0.10** | 0.20 | 0.30 | 0.40 | 0.50 |
|---|---|---|---|---|---|---|---|---|---|
| `I_C^(3)` bits | 0.0000 | 0.0042 | 0.0253 | 0.0658 | **0.0774** | 0.0571 | 0.0277 | 0.0072 | 0.0000 |

Biphasic, on the same 0 → ½ axis as ours, zero at both ends. **0.0774 bits is roughly half our
single best ECA peak** (rule 25, 0.1643 bits) and larger than the peak of 249 of our 256 rules.

**The one piece of daylight, stated precisely:** they never write "peak", never name a maximising
noise value, and never quantify the height. The non-monotonicity is visible in their Fig. 2 and
forced by their own endpoints, but it is not a claim they make. Ours is the first *quantified*
statement — of a phenomenon they published, on a system they did not use.

### Two more neighbours in the same class

- **Barreiro, Gjorgjieva, Rieke & Shea-Brown, "When do microcircuits produce beyond-pairwise
  correlations?", *Front. Comput. Neurosci.* (2014).** Quantity is `D_KL(P, P̃)` against the pairwise
  maxent model — **pairwise-blind**, equal to Σ_{k≥3} `I_C^(k)`. Model (threshold neurons with
  common input). They sweep input correlation, threshold, coupling and **input variance**, and
  report explicit interior maxima: *"the impact of coupling on D_KL is maximized at intermediate
  values of the coupling strength"*, and D_KL *"maximized for large input correlation and moderate
  input variance σ²"*. Largest value reported **0.091 bits on three cells** — the same range as our
  numbers. This is the closest published thing to our claim outside CA, and it is on the noise-ish
  axis.
- **Kahle et al. (2009)** report interior maxima of `I^(k)` versus **coupling** ε on tent-map
  lattices (ε₃ = 0.345, ε₄ = 0.42, ε₅ = 0.355, ε₆ = 0.35), coinciding with the minimum of the
  largest Lyapunov exponent. Same quantity, same peak shape, different control axis — and see §5,
  because their diagnosis of *why* is the control we skipped.

### Adjacent, credited, but **not** scoops

- **Orio, Mediano & Rosas, *Chaos* **33**, 123103 (2023).** Our substrate, our noise axis, our
  biphasic shape — but O-information and S-information, which are **not** pairwise-blind.
  Adjudicated already as #1 in `SPIKE_SURVEY.md`; unchanged.
- **Noise-induced order** (Matsumoto & Tsuda, *J. Stat. Phys.* **31**, 87 (1983); rigorous version
  Galatolo, Monge & Nisoli, [arXiv:1702.07024](https://arxiv.org/abs/1702.07024)). Noise pushing a
  chaotic 1-D map toward order is a 40-year-old idea, but it is quantified by **Lyapunov exponent,
  entropy and power spectrum** — orders 1 and 2. Nobody measured it with an irreducible higher-order
  quantity. Neighbour, not scoop; must be cited when we say "noise can create order", because that
  sentence is theirs.
- **Langton's λ and the edge of chaos** (Langton, *Physica D* **42**, 12 (1990)). Mutual information
  peaks at intermediate λ — the same peak-at-intermediate-parameter shape, on **mutual information**,
  which is order 2, and against rule-space λ rather than noise. Also substantially refuted as a
  predictor by Mitchell, Hraber & Crutchfield ([adap-org/9303003](https://arxiv.org/abs/adap-org/9303003)).
  Neighbour; the credit conversation must engage it because the *shape* claim is Langton's.

---

## 3. The measure disagreement — SCOOPED by the founding paper, in both signs

Schneidman et al. (2003) **Figure 1**, for three binary variables, with `I₃` their triplet
(co-)information:

| system | `I_C^(3)` | `I_C^(2)` | `I₃` |
|---|---|---|---|
| AND | **0** | 0.8113 | −0.1887 |
| OR | **0** | 0.8113 | −0.1887 |
| XOR | 1 | 0 | −1 |
| **FM** (pairwise ferromagnet) | **0** | 2 | **+1** |

and in words:

> "There are at least two difficulties with the triplet information defined by I3… First… we find
> that I3 can be negative (AND, OR and XOR in Fig. 1). Second, **I3 can be nonzero even for networks
> that have only pairwise interactions (FM in Fig. 1)**."

For n = 3, O-information **is** this quantity — verified numerically here, Rosas's Ω formula and
Schneidman's `I₃` agree to < 10⁻¹² on all four systems. And all four rows reproduce exactly under
this repository's own exact solver.

**The FM row is our rules 23 / 178 / 232 in miniature**: large positive O-information (redundancy),
`I_C^(3)` exactly zero. The AND/OR rows are the other direction (apparent synergy, zero irreducible
third order). Both were published in 2003, sixteen years before O-information was named.

Also on the record, from Rosas, Mediano, Gastpar & Jensen, *Phys. Rev. E* **100**, 032305 (2019),
footnote 14 — their own reason for not using our quantity:

> "An exception is the connected information, which can be elegantly derived from principles of
> information geometry; however, **there are no known methods to compute this metric from data**."

That is the honest opening. The field chose O-information for computability; the gap we actually
close is *computing* the pairwise-blind quantity exactly, not *noticing* that it differs.

### A scope defect in our own comparison, found while checking

`ECA_SPIKE_RESULTS.md` says Ω and `I_C^(3)` were computed "from the same exact 2¹⁷-configuration
distribution, so any difference is between the measures". They come from the same distribution, but
**not from the same variables**: Ω is computed over all 17 cells (hence excursions of ±8 bits),
while `I_C^(3)` is computed on 3-cell triples. A 17-variable Ω and a 3-variable `I_C^(3)` disagreeing
is a weaker statement than the memo implies. The clean same-variables version of the comparison is
exactly Schneidman's Fig. 1. **This wording must be fixed regardless of the novelty question.**

---

## 4. The symmetry lemma — the one piece still standing

`SPIKE_SURVEY.md`'s lemma (Z2-symmetric ⇒ `I_C^(odd)` ≡ 0) was searched for specifically and **not
found in general form**. Schneidman's FM row is Z2-symmetric and reads `I_C^(3)` = 0, but they never
invoke the symmetry; a grep of Amari (2001) finds no "symmetr" outside a reference title. Its use to
disqualify the Ising-family spike claims (`SPIKE_SURVEY.md` #2, #7, #8) appears to be ours. Our P2
measurement — 7200 exact values, max |`I_C^(3)`| = 8.882 × 10⁻¹⁶ — is a clean confirmation on a real
dynamical system and remains reportable.

---

## 5. MECHANISM CONTROLS WE DID NOT RUN, AND THEY FIRE

Kahle et al. found a peak in **our exact quantity** and then diagnosed it, verbatim:

> "the unordered state shows the same I vector as the region left of the peak, while the periodic
> sequences of course have I concentrated in I^(2), as the theory predicts. **If the two types of
> sequences are mixed then higher order correlations appear, leading to the peak.** This corresponds
> to the more general and unsolved problem whether the complexity of a convex combination of two
> distributions is related to the complexities of the individual constituents."

That is a published null our pre-registration does not carry. Two consequences, both measured here.

### 5a. The mixture null eats the 1886× headline

`mixture_test.py`: take the deterministic triple distribution and interpolate it toward uniform,
`(1−λ)·p_det + λ·p_unif`. **No dynamics, no noise process, no rule** — just a convex combination.

| rule | reading | real det | real peak | mixture peak | real / mixture |
|---|---|---|---|---|---|
| **58** | SPATIAL 1-1-15 | 1.753e−5 | 3.307e−2 | **6.218e−2** (λ = 0.25) | **0.53** |
| 25 | SPATIAL 1-2-14 | 7.085e−2 | 1.069e−1 | 7.085e−2 (λ = 0, monotone) | 1.51 |
| 46 | SPATIAL 1-2-14 | 3.939e−2 | 4.391e−2 | 3.939e−2 (λ = 0, monotone) | 1.11 |

**Rule 58 — the "noise CREATES structure, 1886×" headline, shared with 114/163/177 — is
out-performed by a trivial mixture that contains no dynamics at all.** The dynamical noise sweep
produces about half the order-3 that linear interpolation toward uniform produces. That claim is the
published convex-combination effect and must not be led with.

**Rules 25 and 46 survive this null**: the mixture surrogate is monotone decreasing — it produces no
rise whatsoever — while the real curves rise. Rule 25, the largest absolute peak in the experiment,
is genuine dynamical enhancement by this test.

**Why this null is well-posed rather than arbitrary.** Both families are one-parameter paths in
probability space from the same start to the same end: the noise sweep runs from `p_det` (P_n = 0) to
uniform (P_n = ½) along a curve, and the mixture runs from `p_det` to uniform along the straight
line. The question "does the dynamics reach higher order-3 than a straight line between its own
endpoints?" is exactly the right one, and for rule 58 the answer is no.

Scope of the null, stated honestly: it is one specific surrogate, run at 400 steps where the memo ran
800, and mass is interpolated toward the *global* uniform rather than the rule's own P_n-evolved
distribution. It is a screen that fired, not a refutation.

### 5b. The low-noise peak location tracks the run length, not the rule

`tscale2.py`, exact batched propagation, peak of `I_C^(3)` over the 18-level dyadic noise grid at
four run lengths T. If a peak sits at an intrinsic operating point of the dynamics its location is
T-independent; if it marks the noise level at which the run first stops being deterministic, its
location falls as 1/T.

| rule | T = 100 | T = 200 | T = 400 | T = 800 | peak height across T |
|---|---|---|---|---|---|
| **25** | 1.95e−3 | 9.77e−4 | 9.77e−4 | **4.88e−4** | 0.0859 → 0.0965 → 0.1069 → **0.1139**, still rising |
| **46** | (none) | 1.95e−3 | 9.77e−4 | 9.77e−4 | 0.0394 → 0.0417 → 0.0439 → 0.0461, still rising |
| **58** | 3.125e−2 | 3.125e−2 | 3.125e−2 | **3.125e−2** | 3.3072e−2 at **every** T |
| **110** | 1.5625e−2 | 1.5625e−2 | 1.5625e−2 | **1.5625e−2** | 3.4597e−3 at **every** T |

**Rules 25 and 46 — the two that survived the mixture null — fail this one.** Their peak location
halves as T doubles (consistent with 1/T at the grid's one-point-per-octave resolution), and the
peak height has not converged: rule 25 gains 18 % between T = 200 and T = 800 and is still climbing.
The product `P_n·n·T` at the peak is roughly constant (≈ 3–7), which says the peak sits at a fixed
total **noise dose** — a handful of flips over the whole run — not at a fixed noise **rate**. In the
T → ∞ limit that peak location goes to zero: there is no stationary operating point for rule 25.
Its spike is a finite-dose transient.

**Rules 58 and 110 pass cleanly**: peak location and peak height are identical to five significant
figures at every T. Those are genuine stationary-state features.

This also corrects the memo. `ECA_SPIKE_RESULTS.md` reports "Convergence was checked at 200/400/800
steps (primaries agree to < 10 %)". For rule 25 the peak *height* moves 0.0965 → 0.1139 (+18 %) and
the peak *location* moves by a factor of 2 across that range. The convergence claim does not hold
for the headline rule.

### 5d. The two controls together, and what they leave

They cut in opposite directions, and between them they take down every rule the memo leads with:

| rule | mixture null (§5a) | T-scaling (§5b) | verdict |
|---|---|---|---|
| 25 (largest peak, headline) | **passes** — mixture is monotone | **fails** — 1/T, unconverged | finite-dose transient |
| 46 | **passes** | **fails** — 1/T, unconverged | finite-dose transient |
| 58 / 114 / 163 / 177 (the 1886×) | **fails** — no-dynamics mixture reaches 1.9× higher | **passes** — T-invariant | mixture-explicable |
| 110 | untested | **passes** — T-invariant | **the one to test next** |

Rule 110 is T-converged and its mixture status is unmeasured. It is the only candidate in this table
that could still be both a stationary operating point and not a convex-combination effect, and its
peak is small (3.46e−3 nats, 0.50 % of the cap). **Run the mixture null on rule 110, and family-wide,
before anything is promoted.**

### 5c. The directed-percolation reading, named as the brief requires

Noisy ECA have a known critical-phenomena literature: Bagnoli & Rechtman,
[arXiv:1409.4284](https://arxiv.org/abs/1409.4284) (damage spreading mapped to directed percolation
in the Domany–Kinzel family) and Mendonça, *Int. J. Mod. Phys. C* **27**:1650016 (2016),
[arXiv:1506.08132](https://arxiv.org/abs/1506.08132), which puts the **noisy XOR CA — rules 90 and
102, ours** — in the **directed percolation universality class**.

The honest reading, with the technical point that saves us stated plainly: **our noise is a
*symmetric* per-cell bit flip** (`v ← ((1−p)I + p·X_j)v`, applied regardless of cell value), which
**destroys the absorbing state**. Standard density-DP requires an absorbing state, so the
inactive–active DP transition is not available in our setup and our peaks are not that transition.
But **damage-spreading / chaotic transitions do survive symmetric noise**, and we have **not**
checked whether our peak noise values coincide with damage-spreading thresholds for the same rules.
That check is open, it is cheap, and until it is done "the peak is an intrinsic operating point"
is not established against this alternative.

---

## 6. WHAT SURVIVES AS NEW

1. **The combination.** Pairwise-blind instrument × dynamical noise × spatially extended dynamical
   system. Kahle and Chliamovitch have instrument + CA and no noise; Orio has noise + CA and the
   wrong instrument; Schneidman has instrument + noise on a three-variable gate with no dynamics.
   Nobody has joined them.
2. **Quantification.** Schneidman's Fig. 2 shows the effect; we are the first to measure how big it
   is, where it peaks, and on how much of a rule family (160/256 rules, exact) — subject to §5.
3. **Family-wide exactness with an end-to-end invariance check.** Colour-inversion agreement to
   5.5 × 10⁻¹⁴ over 108 000 exact comparisons is a check neither prior CA paper ran.
4. **The Z2 symmetry lemma in general form**, and its use to clear the Ising-family claims (§4).
5. **An exact `I_C^(3)` solver**, which is the thing Rosas et al. say does not exist.

## 7. WHAT SURVIVES AS *SAYABLE*, AFTER §5

Less than the memo says, and the two controls between them touch every headline rule (§5d).

**Still safe to say.** (i) The instrument works and the gates hold — P1 (parity reads the cap) and
P2 (7200 exact values of a sign-symmetric rule at machine zero) are unaffected by either control, and
P2 is the one genuinely unpublished piece. (ii) The reproduction of Orio et al.'s O-information
results is unaffected. (iii) `I_C^(3)` is exactly 0 at P_n = ½ on all 256 rules, and
colour-inversion invariance holds to 5.5 × 10⁻¹⁴ — end-to-end checks that stand on their own.
(iv) O-information and `I_C^(3)` disagree about which rules are interesting, on this family, in both
directions — though see §3 on the variable-count mismatch, and the disagreement itself is
Schneidman's finding, not ours.

**No longer safe to say without more work.** "Noise creates irreducible third-order structure" as a
*finding* — it is Schneidman 2003. "1886×" — mixture-explicable. "Rule 25, 16.4 % of the cap" — a
finite-dose transient whose location vanishes as T → ∞. "160 of 256 rules carry a peak" — the peak
census has been through neither control, and on the four rules tested each control disqualified
about half.

**The honest one-line status:** we have a working exact instrument and a clean symmetry result; the
spike itself is not yet established as a property of the dynamics rather than of the run length or
of convex mixing.

---

## 8. THE CREDIT PARAGRAPH WE MUST CARRY

> The quantity is the connected information of order k of Schneidman, Still, Berry & Bialek
> (*Phys. Rev. Lett.* **91**, 238701 (2003)), equivalently the interaction-structure complexity of
> Amari (*IEEE Trans. Inf. Theory* **47**, 1701 (2001)). Measuring it on elementary cellular automata
> is not new: Kahle, Olbrich, Jost & Ay (*Phys. Rev. E* **79**, 026201 (2009)) computed it on eleven
> rules, and Chliamovitch, Chopard & Velasquez (*Int. J. Parallel Emergent Distrib. Syst.* **34**(1),
> 142 (2019); [arXiv:1408.0368](https://arxiv.org/abs/1408.0368)) computed it on all 88 inequivalent
> rules by exact propagation of the probability density. That noise can *create* irreducible
> third-order structure is likewise not new: it is stated and plotted in Schneidman et al.'s
> Figure 2, on noisy boolean gates, and it appears as an interior maximum of the pairwise-maxent
> KL gap in Barreiro, Gjorgjieva, Rieke & Shea-Brown (*Front. Comput. Neurosci.*, 2014). That
> O-information and connected information disagree — one large where the other is exactly zero —
> is Figure 1 of Schneidman et al. (2003), in both signs. The noise axis on this substrate is from
> Orio, Mediano & Rosas (*Chaos* **33**, 123103 (2023)), whose experiment we reproduce with a
> different instrument. The peak-at-intermediate-parameter shape has a long prior life in
> noise-induced order (Matsumoto & Tsuda, 1983) and at Langton's edge of chaos (1990), in each case
> measured by lower-order quantities. Our contribution is the conjunction — the pairwise-blind
> instrument, on a spatially extended dynamical system, under a swept dynamical noise, computed
> exactly and family-wide — together with the odd-order vanishing lemma for sign-symmetric states.

---

## 9. WHAT WAS SEARCHED, SO THE ABSENCE MEANS SOMETHING

Searched **by mathematical object**, not by our vocabulary: maxent-over-pairs entropy gap; connected
information / connected multi-information; Amari's θ-coordinate hierarchy and e-flat projection;
KL divergence from the pairwise exponential family / pairwise maxent model; "irreducible k-th order
interaction"; interaction-structure complexity.

Literatures swept: computational mechanics and CA complexity (Lindgren 1987; Lindgren & Nordahl
1988; Grassberger 1986; Crutchfield & Feldman entropy-convergence line; Shalizi local statistical
complexity; Wuensche input entropy; Lizier/Prokopenko/Zomaya local information dynamics and their
PID-on-CA work; Cassiano & Barbosa integrated information on ECA) — **all compute non-pairwise-blind
quantities**, and the near-miss is instructive: Lindgren's "correlational contrast" k_m constrains
only *contiguous* blocks, so it is a conditional mutual information, and Kahle et al. state in print
that k_m and I^(m) differ, with a triangle-Ising counterexample. The Amari school and neural maxent
(Ay/Olbrich/Jost/Bertschinger; Nakahara & Amari; Tkačik; Ganmor & Segev; Ohiorhenuan & Victor;
Shimazaki; Macke/Opper/Bethge). Noise-enhanced order beyond stochastic resonance (Matsumoto & Tsuda
and its rigorous descendants; coherence resonance). Probabilistic/noisy CA criticality (Domany–Kinzel,
Bagnoli & Rechtman, Mendonça). Langton's λ and the edge-of-chaos rule-space sweeps.

**Not found, and looked for specifically:** any noise-swept pairwise-blind order-k measurement on a
*spatially extended* dynamical system; any general statement of the Z2 odd-order vanishing lemma.

**Reach.** Primary text was extracted and grepped for Kahle (arXiv PDF), Chliamovitch (arXiv PDF),
Schneidman (arXiv PDF) and Rosas 2019 (arXiv PDF); all quotes above from those four are verified
against the paper text, not an abstract. Barreiro et al. was read through the PMC full-text
rendering, not a local extraction. The IJPEDS 2019 journal version is paywalled (403) — the 2019
abstract and the 2014 preprint were used, so the *local*-measure half of that paper is unread here.
Figures were never viewed as images; every claim about a figure rests on its caption, its table, or
a re-derivation. Where a peak is attributed to a figure we did not see, it is flagged as inference.

## FILES

Written to `scratchpad/` and left **uncommitted** (this commit carries only this memo):

- `verify_schneidman.py` — re-derives Schneidman Fig. 1 (all four rows, exact) and the Fig. 2 AND
  output-noise sweep with this repository's own exact k = 3 solver; also checks that Rosas's
  O-information equals Schneidman's `I₃` for n = 3.
- `mixture_test.py` — §5a, the no-dynamics convex-mixture null.
- `tscale2.py` — §5b, peak location versus run length, batched over the noise grid.
