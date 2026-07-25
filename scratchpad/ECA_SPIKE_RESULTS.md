# RESULTS — the ECA noise spike, measured in a pairwise-blind quantity

> ## CORRECTION (2026-07-25, same day — adjudication `9630d81`, ECA_SPIKE_NOVELTY.md)
>
> **The arithmetic below is right (independently reimplemented to 6 significant figures).
> The three headline framings are wrong, and two mechanism controls this prereg did not
> carry both fire.** Read this block before any number below.
>
> SCOOPED, all three headlines: connected information on cellular automata is
> Kahle-Olbrich-Jost-Ay, PRE 79:026201 (2009) — our rule-90 "gate" is their Table II
> measurement — and Chliamovitch et al. (2014/2019, all 88 classes, exact propagation).
> Noise CREATING irreducible order-3 is Schneidman-Still-Berry-Bialek (2003) **Fig. 2, in
> the paper that defines the measure**: their sweep goes 0 → 0.077 bits → 0, larger than
> 249 of our 256 rules. The Omega-vs-I_C^(3) disagreement is their Fig. 1, in both signs.
> What is convergent-adjacent (not in print): the family-wide exact 2^17 scan with a noise
> parameter. Full credit paragraph in the adjudication.
>
> CONTROLS FIRED: (1) **The mixture null eats the 1886x headline.** Kahle et al. published
> the diagnosis — convex combinations manufacture higher-order structure — and a
> no-dynamics straight line from p_det to uniform reaches 1.9x MORE order-3 than rule 58's
> real noise sweep (6.22e-2 vs 3.31e-2). Rules 25/46 survive this null (their mixture
> surrogate is monotone; the real curves rise — genuine dynamical enhancement).
> (2) **The peak location tracks run length, not the rule.** Rules 25/46 peak at fixed
> total DOSE (P_n x n x T = 3-7 expected flips), so the location halves as T doubles, and
> the height was still rising at T=800 (+18% from T=200, against this memo's claimed <10%
> convergence). Rules 58/110 are T-invariant to five figures — but their magnitudes are
> the mixture effect. **No headline rule passes both controls.**
>
> What survives: the exact-propagation technique; the sign-symmetry lemma control
> (8.9e-16 over 7200 values); the IPF-unsafe lesson; rule 25's rise as real dynamical
> enhancement whose operating point is a dose, not a noise rate. Also noted: the memo's
> Omega comparison is not same-variables (Omega over all 17 cells, I_C^(3) over triples).
> New standing rule: every swept-parameter peak claim carries the mixture null and the
> dose-vs-rate check.


Pre-registration frozen and committed at **`421ba25`** *before any run*
(`scratchpad/ECA_SPIKE_PREREG.md`). Substrate: elementary cellular automata on a ring of
**n = 17** cells with dynamical bit-flip noise, reproducing Orio, Mediano & Rosas, *Chaos*
**33**, 123103 (2023), [arXiv:2305.13454](https://arxiv.org/abs/2305.13454). Quantity: the
connected information of order 3, `shareK` at k = 3, from `array_cap_experiment.py`.
Scratchpad only; nothing touches the Lean library, `Stance.lean` or the audit.

**This is a model system, not nature. Nothing here bears on the `wild-share` open claim**,
which concerns the world and is untouched by a cellular automaton.

---

## VERDICT

**Pre-registered outcome (a) fires, and so does outcome (b) — on different rules.**

1. **A biphasic peak survives in I_C^(3).** Bit-flip noise on a deterministic binary rule
   produces a genuine, pairwise-blind, non-monotonic order-3 maximum at intermediate noise.
   The largest is **rule 25 (and its colour-inverse 103)** on three cells at one time,
   rising from **0.0662 to 0.1139 nats** at P_n = 4.88 × 10⁻⁴ — **16.4 % of the ln 2 cap** —
   before falling to exactly zero at maximal noise. The sharpest *relative* rise is **rules
   58 / 114 / 163 / 177**, from 1.75 × 10⁻⁵ to 0.0331 nats: a factor of **1886**. This is
   not a rare corner: **160 of the 256 rules (51 of the 88 equivalence classes)** carry such
   a peak on a primary reading.

2. **And their spike is, on many rules, a spike in the wrong quantity — exactly as the
   survey predicted.** On rules **23, 178 and 232**, O-information rises biphasically to as
   much as **+8.07 bits** — the largest Ω excursions measured anywhere in this experiment —
   while I_C^(3) is **8.9 × 10⁻¹⁶ nats**, machine zero, at every noise level and every
   reading. These are the complementation-symmetric rules the symmetry lemma pins to
   exactly zero, and ten of the sixteen are rules the paper reports as having nonzero Ω.

3. **Where both quantities fire, they fire in different places.** Rule 28: Ω peaks at
   P_n = 1.95 × 10⁻³, I_C^(3) at 6.25 × 10⁻² — **32× apart**. And on rules 46, 188, 18, 104
   and 130 the order-3 peak is plainly there while Ω either is strictly monotone (rule 46)
   or excurses by less than the 0.5-bit threshold and reports nothing.

So the two measures disagree about *which rules are interesting*, in both directions, and
about *where the operating point is* when they agree a rule is interesting at all.

**Everything above is computed exactly.** After the sampled sweep found the spikes, the
whole result was recomputed with **no sampling and no estimator**: the distribution over all
2¹⁷ = 131 072 configurations was propagated directly for 800 steps, so the triple marginals
and hence I_C^(3) are exact. Probability mass is conserved to 1.000000000000. The sampled
and exact answers agree (rule 110: sampled excess 3.49 × 10⁻³, exact 3.4597 × 10⁻³).

Two things this is **not**. It is not large: the median peak across the family is **0.98 %
of the ln 2 cap**, and even the best is a sixth of it. And it is not a claim about nature.

---

## GATES — all pass, before any sweep number was believed

| gate | result |
|---|---|
| **G1** share machinery | PASS — `array_cap_experiment.gate()`: exact parity → ln 2 saturating its cap, exact independence → 0, k = 5 code state → 2 ln 2, IPF residual 0.0, `shareK` ≡ `bench_detector.C3` to 0.0 |
| **G2** batched maxent solver | PASS — reproduces the reference `shareK` to **4.17 × 10⁻¹³** on 1000 random 2×2×2 states; exact parity → 0.693147180560 (ln 2 to 1 ulp) |
| **G3** ECA engine | PASS — **bit-identical** to a naive per-cell reference for **all 256 rules**, 50 steps, 512 runs, n = 17 ring |
| **G4** noise engine | PASS — measured per-bit flip rate matches P_n at all 17 levels, \|z\| < 2 everywhere, on both the dense and the sparse code path |
| **G5b** shuffle floor | PASS — the product-of-marginals construction agrees with direct independent permutation |

G3 is what licenses the experiment: without it, "rule 110" would be an assumption.

### Deviation from the prereg, disclosed

The prereg specified **IPF** for the pairwise maxent. **It was replaced mid-run by an exact
solver**, for cause: on the near-deterministic distributions this substrate actually
produces, IPF hit its 20 000-iteration cap at a marginal residual of **3.1 × 10⁻⁶** — above
this experiment's floor of ~10⁻⁶, therefore unusable. For three binary variables the
pairwise maxent is the unique distribution with the given pair marginals and vanishing
three-way log odds ratio; fixing the marginals leaves one free parameter in which every cell
is affine, the feasible interval brackets a sign change, and bisection converges to machine
precision in every case including the boundary ones. The replacement was re-gated under G2
(agreement 4.17 × 10⁻¹³ with the reference, marginal residual **exactly 0.0**) and is
strictly more accurate and ~25× faster. Nothing else in the pre-registered protocol changed.

---

## P0 — the paper's own entropy curves reproduce

Shannon entropy of the 17-cell configuration, bits, exactly as their Figure 1B:

| rule | det | 1e-4 | 1e-3 | 3.9e-3 | 1.6e-2 | 6.3e-2 | 0.5 | their Fig 1B |
|---|---|---|---|---|---|---|---|---|
| 8 | 0.00 | 0.03 | 0.19 | 0.63 | 2.00 | 5.95 | 16.91 | near zero, rises late ✓ |
| **19** | 10.54 | 10.13 | 8.17 | **6.76** | 9.04 | 13.55 | 16.91 | **biphasic, dips to ≈7** ✓ |
| 22 | 7.45 | 8.08 | 9.48 | 11.81 | 14.28 | 15.92 | 16.91 | monotone rise ✓ |
| 30 | 13.45 | 14.44 | 15.94 | 16.62 | 16.86 | 16.91 | 16.91 | affected by very low noise ✓ |
| 45 | 16.91 | 16.91 | 16.91 | 16.91 | 16.91 | 16.91 | 16.91 | flat at maximum ✓ |
| 46 | 9.25 | 9.26 | 9.27 | 9.70 | 10.98 | 13.89 | 16.91 | flat then rises ✓ |

Their O-information results reproduce too: **rule 28** is redundancy-dominated and its Ω
*increases* with intermediate noise (3.54 → **7.14** bits at P_n = 1.95 × 10⁻³); **rule 97**
starts positive and **goes negative** at intermediate noise (2.08 → **−3.46**) before
returning; **rule 60** decreases monotonically (−14.91 → 0). Those are precisely the three
rules of their Figure 2 and precisely the three behaviours they report.

**So this is not outcome (c).** The reimplementation reproduces their result in their own
quantity, which is what licenses reading a difference in ours as a difference between the
measures.

---

## P1 and P2 — the two pre-committed gates, both fire

**P1, the parity gate.** The two-term linear rules read the cap at zero noise, by
construction, exactly as pre-committed — a gate, not a finding:

| rule | mechanism | reading | I_C^(3) at P_n = 0 |
|---|---|---|---|
| 90 | s_{i−1} ⊕ s_{i+1} | CAUSAL-LR | 0.693145 |
| 60 | s_{i−1} ⊕ s_i | CAUSAL-LC | 0.693145 |
| 102 | s_i ⊕ s_{i+1} | CAUSAL-CR | 0.693146 |

(ln 2 = 0.693147; the shortfall is sampling at R = 2²⁰.)

**P2, the symmetry lemma.** Over the **16** complementation-symmetric rules × 18 noise
levels × 25 readings — **7200 exact values** — the largest \|I_C^(3)\| is

> **8.882 × 10⁻¹⁶ nats** (float64 epsilon is 2.2 × 10⁻¹⁶).

The lemma holds to machine precision on a real dynamical system, at every noise level, and
it is not the instrument being stuck: the same instrument reads 0.693145 on rule 90 and
0.1139 on rule 25. **Ten of those sixteen rules have nonzero O-information in the paper**,
and three of them (23, 178, 232) carry the largest biphasic Ω peaks measured here.

---

## THE PRE-REGISTERED SPIKE TEST

Sampled focus stage (R = 2²⁰ runs, 800 steps, 3 seeds, 60 matched surrogates, 10 shuffles,
cross-run refuter): **95 readings satisfied all five pre-registered conditions**. The
refuter did its job — rule 19 CAUSAL-LC was struck out by condition (iv) at \|z\| = 10.0.

Rather than defend those against estimator objections, the whole measurement was redone
exactly. **Exact, 800 steps, no sampling, ranked by the pre-registered statistic
Δ = peak(P_n > 0) − det:**

| rule(s) | reading | det | peak | Δ | at P_n | ratio | % of ln 2 |
|---|---|---|---|---|---|---|---|
| **25, 103** | SPATIAL 1-2-14 | 6.624e−2 | **1.1391e−1** | +4.77e−2 | 4.88e−4 | 1.7 | **16.43** |
| 94, 133 | SPATIAL 2-2-13 | 4.229e−2 | 7.491e−2 | +3.26e−2 | 1.95e−3 | 1.8 | 10.81 |
| **58, 114, 163, 177** | SPATIAL 1-1-15 | 1.753e−5 | 3.307e−2 | +3.31e−2 | 3.12e−2 | **1886** | 4.77 |
| 73, 109 | SPATIAL 1-1-15 | 3.688e−2 | 6.292e−2 | +2.60e−2 | 1.95e−3 | 1.7 | 9.08 |
| 58, 114, 163, 177 | TEMPORAL | 3.397e−4 | 2.539e−2 | +2.51e−2 | 6.25e−2 | 74.7 | 3.66 |
| 62, 118, 131, 145 | TEMPORAL | 4.668e−3 | 2.808e−2 | +2.34e−2 | 3.12e−2 | 6.0 | 4.05 |
| 152, 188, 194, 230 | TEMPORAL | 1.627e−4 | 1.755e−2 | +1.74e−2 | 6.25e−2 | 107.8 | 2.53 |
| 46 | SPATIAL 1-2-14 | 3.939e−2 | 4.613e−2 | +6.74e−3 | 9.77e−4 | 1.2 | 6.65 |
| 28 | TEMPORAL | 0.0 | 8.402e−3 | +8.40e−3 | 6.25e−2 | ∞ | 1.21 |
| 110 | SPATIAL 1-1-15 | 3.097e−5 | 3.460e−3 | +3.43e−3 | 1.56e−2 | 111.7 | 0.50 |

**Both pre-registered primary readings carry spikes** — SPATIAL (three cells at one time)
and TEMPORAL (one cell at three successive times). Every curve returns to **exactly 0.0** at
P_n = 1/2, where the distribution is uniform, so each is genuinely biphasic and not a
monotone rise cut off at the edge of the sweep.

**Across the whole family** (exact, all 256 rules, 400 steps): 160 rules — 51 of the 88
equivalence classes — show a peak with Δ > 10⁻⁴ nats and peak > 10⁻³ nats on a primary
reading. Median peak **0.98 % of ln 2**, maximum 15.4 %. The peak locations cluster
strikingly: 48 rules peak at P_n = 1/16 and 40 at 1/32, with a second group near 10⁻³.

---

## THE REFUTER PASS — the estimator removed entirely

Everything that could be wrong with a sampled spike is an estimator question. An n = 17 ECA
has only 131 072 configurations, so the question can be deleted rather than argued:

- deterministic step: v′[f(s)] += v[s], the exact push-forward through the rule;
- noise step: v ← ∏ⱼ((1−p)I + p·X_j)v, exact independent bit flips;
- start from the exact uniform distribution over initial conditions, run the same 800 steps.

The result is the exact distribution the sampled pipeline was estimating. Checks:

| check | result |
|---|---|
| probability mass after 800 steps | **1.000000000000** (worst case, rule 0: 0.999999998809) |
| exact vs sampled, rule 110 SPATIAL 1-1-15 peak | 3.4597e−3 vs 3.49e−3 (agree within sampling error) |
| exact vs sampled, rule 163 SPATIAL 1-1-15 peak | 3.307e−2 vs 3.190e−2 (screen, R = 65 536, 1 seed) |
| batched vs sequential propagator | max difference **8.1 × 10⁻²⁰** |
| I_C^(3) at P_n = 1/2 | **exactly 0.0** — all 256 rules × 25 readings, max \|I_C^(3)\| = 0.000e+00 |
| colour-inversion invariance | max disagreement **5.53 × 10⁻¹⁴ nats over 108 000 exact comparisons** |

That last line is a strong end-to-end check that costs nothing: I_C^(3) is exactly invariant
under complementing all three slots, so a rule and its colour-inverse must agree tag for tag.
They do, to 5.5 × 10⁻¹⁴, across the whole family.

### Sampled-stage floors and controls (all disclosed, per house rules)

| | |
|---|---|
| matched pairwise-maxent surrogate null | mean 4.485e−7, sd 6.188e−7 (max 1.074e−6) over 10 584 sweep points |
| shuffle floor | 4.497e−7 |
| maxent solver residual | **0.0** at every point |
| **cross-run refuter** | \|z\| max 10.79, mean \|z\| 0.69; **72 of 10 584 points exceed 5** and are voided, including one otherwise-qualifying spike |
| **tied fraction** | **0.00000 everywhere, structurally** — the substrate is natively binary: no threshold, no median split, no tie to disclose |
| frozen slots (slot marginal < 1e−6) | 66 of 10 584 points; flagged, and disclosed per declared spike |
| sample sizes | screen R = 65 536 × 400 steps × 1 seed × 16 surrogates; focus R = 1 048 576 × 800 steps × 3 seeds × 60 surrogates; Ω control R = 2 097 152 |

**Boundary discriminator: vacuous, and the reason matters.** There is no clamp, threshold or
saturating nonlinearity anywhere in this substrate, so clip-versus-fold cannot be applied.
Unlike the CIRISArray case — where vacuity meant *we learned nothing about robustness* — here
it means **the artifact mechanism is structurally absent**. That is why this substrate was
chosen, and it is why the positive result cannot be the reflecting-fold artifact that has
twice manufactured order-3 in this repository. Convergence was checked at 200/400/800 steps
(primaries agree to < 10 %).

### The no-dynamics control — which readings are mechanism, which are emergence

The rule applied **once** to uniform i.i.d. inputs, computed exactly, isolates what the truth
table alone contributes. It cleanly separates the two:

- **rule 90 CAUSAL-LR: measured 0.6931 tracks the control 0.6931 at every noise level.** The
  entire curve is the truth table. Same for rules 45 and 30. These causal readings measure
  the mechanism, not emergence, and are reported as gates only.
- **rules 46 and 54: the control is exactly 0 at every noise level, yet the measured curve is
  nonzero and biphasic.** Those are entirely dynamical.

**The two pre-registered primary readings are not mechanism readings at all** — a spatial
triple at one time is not the rule's input set — which is why the headline table above is
restricted to SPATIAL and TEMPORAL.

---

## THE MEASURE COMPARISON — both quantities from the same exact distribution

Ω and I_C^(3) computed from the *same* exact 2¹⁷-configuration distribution, so any
difference is between the measures, not between two estimators.

"Ω excursion" is the size of the interior extremum measured against *both* endpoints — the
pre-registered biphasic test, threshold 0.5 bits. "Ω extremum" is the raw value it reaches.

| rule | Ω biphasic? | Ω excursion | Ω extremum | at P_n | I_C^(3) best primary | peak | at P_n |
|---|---|---|---|---|---|---|---|
| **23** | yes (+) | 6.91 | **+8.07** | 7.81e−3 | SPATIAL 3-4-10 | **8.9e−16** | — |
| **232** | yes (+) | 6.91 | **+8.07** | 7.81e−3 | SPATIAL 3-3-11 | **8.9e−16** | — |
| **178** | yes (+) | 5.90 | +7.05 | 3.91e−3 | SPATIAL 3-3-11 | **8.9e−16** | — |
| **46** | **no — monotone** | — | −2.27 → 0 | — | SPATIAL 1-2-14 | 4.613e−2 | 9.77e−4 |
| **188** | no (0.10 < 0.5) | 0.10 | −0.33 | 1.22e−4 | TEMPORAL | 1.755e−2 | 6.25e−2 |
| **18** | no (0.33 < 0.5) | 0.33 | −5.85 | 1.22e−4 | SPATIAL 2-2-13 | 3.549e−3 | 4.88e−4 |
| 28 | yes (+) | 3.60 | +7.14 | 1.95e−3 | TEMPORAL | 8.402e−3 | 6.25e−2 (**32× apart**) |
| 19 | yes (+) | 6.45 | +6.46 | 3.91e−3 | TEMPORAL | 1.515e−3 | 6.25e−2 (16× apart) |
| 163 | yes (+) | 2.70 | +5.52 | 9.77e−4 | SPATIAL 1-1-15 | 3.307e−2 | 3.12e−2 (32× apart) |
| 110 | yes (−) | 5.04 | −5.04 | 3.91e−3 | SPATIAL 1-1-15 | 3.460e−3 | 1.56e−2 (4× apart) |

Rules 23 and 232 are the whole survey in two lines: **the largest O-information excursions
measured anywhere in this experiment, reaching +8.07 bits, sit on rules whose pairwise-blind
order-3 content is exactly zero at every noise level.** Rule 46 is the mirror image: Ω is
*strictly monotone* — it reports nothing at all — while I_C^(3) peaks at 6.65 % of the cap.

---

## SCOPING — what this does and does not establish

**Does.** On elementary cellular automata, dynamical noise genuinely creates pairwise-blind
order-3 structure that is absent (or nearly so) in the deterministic system and absent again
at maximal noise, with a maximum at an intermediate noise level. It is exact, it is
reproducible in two independent implementations, it survives a cross-run refuter, it is
widespread across the rule family, and it cannot be the static-nonlinearity artifact because
this substrate has no static nonlinearity to fold. As far as `SPIKE_SURVEY.md` reaches — one
pass of the web literature, so read it as *not found* rather than *does not exist* — no
spike in a pairwise-blind higher-order quantity had been published by anyone, and this is
the first one measured here.

**Does not.** (i) **It is a model system.** Elementary cellular automata are not nature, and
nothing here supports, weakens or touches the `wild-share` open claim. (ii) **It is small.**
The median peak is 0.98 % of the ln 2 cap and the largest is 16.4 %; nothing here approaches
the parity state's saturation. (iii) **It says nothing about whether the same happens in any
physical system**, and the survey's other twelve candidates remain adjudicated as they were.
(iv) The pre-registered kill did **not** fire — noise-enhanced whole-only structure is not
refuted; it is exhibited. The dead-claim ledger gains nothing from this run.

**Known coverage limit, disclosed.** The 24 spatial gap-shapes use one representative triple
each, `(0, d₁, d₁+d₂)`. On a ring, a triple with three distinct gaps has a second, reflected
orientation `(0, d₁, d₁+d₃)` that this list does not name. Every reported number is correct
for the triple actually measured, and the *family-wide* scan is nevertheless complete,
because the reflected orbit of rule R is the standard orbit of R's mirror partner and all 256
rules were scanned. For a single named rule in isolation, one orientation is unmeasured.

**What would overturn this.** The result is exact arithmetic on a fully specified finite
system, so it cannot be overturned by more data — only by an error in the specification. The
two places to attack are the ECA transition rule (checked bit-identical against a naive
reference for all 256 rules, G3) and the maxent solver (checked against the repository's
reference to 4 × 10⁻¹³ and to ln 2 on exact parity, G2). If either is wrong, so is this.

---

## FILES

`ECA_SPIKE_PREREG.md` (committed at `421ba25`, before any run) · `eca_spike.py` (engine,
gates, sampled sweep) · `eca_exact.py` (the exact refuter) · `eca_omega_exact.py` (Ω and
I_C^(3) from the same exact distribution) · `eca_analyze.py` · `eca_power.py` (injection
sensitivity harness, written but superseded by the exact computation, which makes a detection
floor moot) · results: `eca_screen.json`, `eca_focus.json`, `eca_omega.json`,
`eca_exact_all256.json`, `eca_exact_top800.json`, `eca_omega_exact_all.json`,
`eca_analysis.txt`, `eca_converge.json`.

`eca_screen.json` (the all-256-rule sampled screen, 48 MB) is **not committed** for size;
regenerate with `python3 eca_spike.py --screen`. Nothing in the verdict rests on it — the
screen only nominated candidates, and every nominated candidate was then recomputed exactly
in `eca_exact_all256.json`, which is committed and which covers all 256 rules by itself.
