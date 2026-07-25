# PRE-REGISTRATION — the ECA noise spike, measured in *our* quantity

Frozen and committed **before any run**. Scratchpad only: nothing here touches the Lean
library, `Stance.lean`, or the audit. This is a **model system, not nature**; nothing in this
experiment bears on the `wild-share` open claim, and no outcome of it may be laundered into a
world-claim.

---

## 1. THE CLAIM BEING RE-MEASURED

Orio, Mediano & Rosas, *Chaos* **33**, 123103 (2023),
[arXiv:2305.13454](https://arxiv.org/abs/2305.13454), "Dynamical noise can enhance high-order
statistical structure in complex systems." Elementary cellular automata on a **circular grid
of 17 cells**, run **800 steps**, with **dynamical** noise: "*Noise was introduced via a
probability that governed how likely an agent would disobey the rule, i.e. do the opposite
that the rule dictated. A probability of 0.5 is equivalent to agents being completely
random.*" They report, over the 93 non-equivalent rules, that "*some rules exhibit an
increase in the absolute magnitude of their O-information for intermediate levels of noise*"
and that rule 28 shows "*a biphasic change of S-information with intermediate levels of
noise, showing an increase before decaying to zero*."

Their quantities are Ω = TC − DTC (O-information) and Σ = TC + DTC (S-information).
**Neither is pairwise-blind.** Caprioglio, Mediano & Berthouze, *Phys. Rev. Lett.* **136**
(2026), [arXiv:2505.24686](https://arxiv.org/abs/2505.24686), prove that pairwise mechanisms
alone generate synergy in measures of this family. So their spike may be a spike in the
wrong quantity. `SPIKE_SURVEY.md` (committed at `1ffb17a`) ranks this paper #1 of thirteen
candidates and selects it for reproduction **on substrate grounds only**: ECA states are
natively binary, so there is no acquisition threshold, no clipping and no saturating
nonlinearity anywhere in the chain. The static-nonlinearity artifact that has twice
manufactured order-3 in this repository *cannot operate here*.

## 2. THE QUANTITY WE MEASURE INSTEAD

The **connected information of order 3** (Schneidman, Still, Berry & Bialek, *PRL* **91**,
238701 (2003)),

> I_C^(3) = S[P̃^(2)] − S[P], P̃^(2) = the maximum-entropy distribution matching all pair
> marginals,

computed by the repository's gate-validated machinery: `shareK` / `pairwise_maxent_k` in
`scratchpad/array_cap_experiment.py`, identical at k = 3 to `bench_detector.C3`. Natural log
throughout; the k = 3 cap is ln 2 = 0.693147.

**I_C^(3) is pairwise-blind by construction**: it is exactly the entropy gap the pair
marginals cannot close, and it is zero on any distribution that *is* its own pairwise maxent.
Ω is not. That difference is the whole experiment.

## 3. HYPOTHESIS

> **H1.** Bit-flip noise on a deterministic binary rule produces a **non-monotonic** I_C^(3)
> — a maximum at nonzero P_n strictly above the P_n = 0 value — on at least one ECA rule,
> in at least one of the readings below.

## 4. SUBSTRATE AND SWEEP — fixed now

| | |
|---|---|
| lattice | ring of **n = 17** cells, periodic (as the paper) |
| initial condition | uniform i.i.d. bits (the paper enumerates all 2^17; sampling uniformly is the same ensemble) |
| noise | each cell's *new* state is flipped independently with probability P_n after the rule is applied — "disobey the rule" |
| steps | **800** in the focus stage, 400 in the screen; convergence checked at 200/400/800 |
| P_n grid | **0, and 2^−k for k = 17 … 1**: 7.63e−6, 1.53e−5, …, 0.125, 0.25, 0.5 — 18 points |
| rules | screen: **all 256**; focus: the set in §7 |

**Why dyadic P_n.** Every P_n is exactly representable by the noise generator (AND of k
uniform bit-words, or a Poisson-XOR scatter whose per-cell flip probability is exactly
1 − (1 − 2/M)^… /2 by construction), so the noise probability carries **no approximation
error at any sweep point**. The grid spans the paper's range (1e−5 … ~0.3) at finer
resolution and adds their P_n = 1/2 maximal-noise endpoint.

### Sample sizes (stated up front — estimator bias grows as sampling gets sparse)

| stage | runs R (independent ICs + noise realisations) | steps | seeds | surrogates |
|---|---|---|---|---|
| screen | 65 536 | 400 | 1 | 24 |
| focus | 1 048 576 (2^20) | 800 | 3 | 60 + 10 shuffles |
| Ω / Σ control | 2 097 152 (2^21) | 800 | 1 | — (bias checked by R vs R/4) |

For a 3-variable binary triple the plugin bias of I_C^(3) is O(1/2T): ≈ 7.6e−6 nats at
R = 65 536 and ≈ 4.8e−7 nats at R = 2^20. The full 17-cell entropies needed for Ω have
131 072 bins; at R = 2^21 the plugin bias of Ω is ≈ 0.3 bits, which is why Ω is run at 2^21
and reported with a Miller–Madow correction alongside the plugin value the paper used.
**Every reported I_C^(3) is an excess over a matched null, never a raw value.**

### Independence axis

**Replicas, not time pooling** — the run (one initial condition, one noise realisation) is
the independent unit, exactly as `HABIT_DYNAMICS_RESULTS.md` Measurement 2 used its 12 288
structurally independent units. One sample per run per reading. No pooling of correlated
cells or time points into a single histogram. The ensemble is exactly translation-invariant
on the ring, so a fixed representative triple carries the same distribution as any rotation
of it; rotations are therefore *not* pooled, they are simply not needed.

## 5. THE THREE READINGS

| tag | slots | note |
|---|---|---|
| **SPATIAL** | cells (0, d₁, d₁+d₂) at the final time | one per gap-shape; the 24 partitions of 17 into three positive parts; primary statistic = per-shape excess, reported as max over shapes and mean over shapes |
| **TEMPORAL** | cell 0 at times (T, T+1, T+2) | one cell at three successive times |
| **CAUSAL** | (s₀(T), s₂(T), s₁(T+1)) | the rule's two outer inputs and its output — the mechanism triple, and the rule-90 gate |

SPATIAL and TEMPORAL are the mission's two primaries; CAUSAL is the third because it is the
reading on which a known-parity rule must saturate, and so it gates the pipeline.

## 6. NULLS, FLOORS AND CONTROLS — each mapped to a trap this repository has been bitten by

1. **Matched pairwise-maxent multinomial surrogate at every sweep point.** IPF to the
   maxent distribution carrying the *observed* pair marginals, then R multinomial draws,
   then re-estimate. Not an i.i.d. null and not a Gaussian null: our i.i.d. nulls false-fired
   at +42 σ on timeseries. Reported as `excess = share − null_mean`, `z = excess / null_sd`.
2. **Shuffle floor.** Each slot independently permuted across runs.
3. **Cross-run refuter.** Triples built with slot *j* taken from run *j* — same rule, same
   P_n, different runs. True I_C^(3) is zero by construction. **Any |z| > 5 here proves the
   null mis-specified and voids the corresponding sweep point.** This control saved the
   habit-dynamics numbers and voided the array-cap ones.
4. **P_n = 0 is measured by the identical sampled pipeline at the identical R.** The
   exhaustive 2^17-initial-condition exact value is reported alongside as a check, but the
   spike comparison is sampled-vs-sampled, so no part of a spike can be a bias step between
   an exact and an estimated endpoint.
5. **Tied fraction.** Structurally **zero**: the substrate is natively binary, so there is no
   threshold, no median split, and no tie to disclose. Reported as zero *with that reason*.
   The live degeneracy in its place is a **frozen slot** — a triple slot whose marginal is
   within 1e−6 of 0 or 1, on which I_C^(3) is 0 by construction rather than by measurement.
   The frozen-slot fraction is disclosed at every sweep point.
6. **Boundary discriminator: vacuous, and the reason matters.** There is no clamp, no
   threshold and no saturation to replace with a reflecting fold, so clip-vs-fold carries no
   information here. Unlike the CIRISArray case — where vacuity meant "we learned nothing
   about robustness" — here it means "**the artifact mechanism is structurally absent**."
   Those are different statements and the memo will not blur them in either direction.
7. **Equivalence-class consistency.** Rules related by colour inversion or mirroring must
   give identical I_C^(3) (complementing all three slots leaves I_C^(3) exactly invariant).
   Agreement across the 256 → 88 classes is a free end-to-end check of the whole pipeline.

## 7. PRE-COMMITTED EXPECTATIONS — what is a gate and what is a finding

The survey's instruction is explicit: *pre-commit the XOR rules as expected, not discovered*.

**P1 — the two-term linear rules are expected to read high, and that is not a result.**
Rule 90 (s_{i−1} ⊕ s_{i+1}), rule 60 (s_{i−1} ⊕ s_i), rule 102 (s_i ⊕ s_{i+1}) and their
affine partners 165, 195, 153 have a parity mechanism. On the CAUSAL reading rule 90 **must**
read I_C^(3) = ln 2 = 0.693147 at P_n = 0 by construction. On SPATIAL readings, a linear rule
drives the ensemble onto a coset of a linear code, whose three-coordinate projections are
either the whole cube (I_C^(3) = 0) or a parity plane (I_C^(3) = ln 2). **Large deterministic
I_C^(3) on these rules is a gate reading, not a discovery, and a monotone decay of it under
noise is not a spike.** H1 requires a rule that *gains* order-3 at intermediate noise.

**P2 — the symmetry lemma must fire on the 16 complementation-symmetric rules.** A rule is
complementation-symmetric (self-conjugate) when f(¬a,¬b,¬c) = ¬f(a,b,c), i.e. r_k + r_{7−k} = 1
for all neighbourhood indices k. Exactly **16** of the 256 rules qualify:

> **15, 23, 43, 51, 77, 85, 105, 113, 142, 150, 170, 178, 204, 212, 232, 240**

For these, the dynamics commutes with global complementation; the initial ensemble is
complement-symmetric and so is the bit-flip noise; therefore the joint distribution satisfies
p(x) = p(¬x) at every time and every P_n, every 3-marginal of it is Z₂-symmetric, and by the
lemma in `SPIKE_SURVEY.md` **I_C^(3) is identically zero — at every P_n, in all three
readings.** Six of the sixteen (105, 150, 15, 51, 170, 204) are in the paper's own list of
rules with zero Ω and Σ, so they prove nothing; the other **ten — 23, 43, 77, 85, 113, 142,
178, 212, 232, 240 — have nonzero O-information in the paper and must read exactly zero
here.** That is the sharpest available demonstration that Ω and I_C^(3) are different
quantities, and it is a free positive control for the entire pipeline: an instrument that
fires at ln 2 on rule 90 and at 0 on rule 232 is working.

Deviation from P2 by more than the surrogate floor at any sweep point is a **pipeline
failure**, not a discovery, and will be reported as such and debugged before anything else is
believed.

**P0 — the paper's own entropy curves must reproduce.** Figure 1B: rule 8 near zero at low
noise rising steeply above P_n ≈ 1e−2; rule 19 biphasic, dipping to ≈ 7 bits near
P_n ≈ 1e−2 before rising to 17; rules 30 and 45 flat at ≈ 17 throughout; rules 46 and 22
rising monotonically. Shannon entropy is the most estimator-robust quantity in the paper, so
this is the cheapest and strongest check that our ECA and noise are theirs.

### Focus rule set, fixed now

Paper-featured: **8, 19, 22, 28, 30, 45, 46, 60, 97**. Order-3 gates: **90, 102, 150, 105**.
Symmetry-lemma controls with nonzero Ω: **23, 178, 232**. Structure controls: **0** (frozen),
**204** (identity), **110, 54, 18** (the canonical complex/chaotic rules). Plus **any rule the
screen flags**, which is why the screen runs on all 256.

## 8. STATISTIC AND DECISION RULE — fixed now

Per (rule, reading, shape, P_n, seed): `share`, `null_mean`, `null_sd` (60 surrogates),
`excess = share − null_mean`. Across the 3 seeds: `excess̄` and its standard error
`sem = sd/√3`.

**Spike statistic.** Δ = max over P_n > 0 of excess̄(P_n) − excess̄(0), and

> z_spike = Δ / √( sem(P_n*)² + sem(0)² ), P_n* the arg max.

**A spike is declared only if all five hold:**
(i) z_spike > 5; (ii) the peak excess̄ itself exceeds 5 × null_sd, so the peak is above the
estimator floor and not merely above a depressed endpoint; (iii) it replicates in all 3
seeds; (iv) the cross-run refuter at the peak has |z| < 5; (v) the peak's slots are not
frozen. A spike that survives (i)–(v) still faces a **mandatory refuter pass** before it may
be reported as anything but provisional.

## 9. OUTCOMES AND THEIR MEANINGS — written before any result is seen

Ω and Σ are computed **in the same run, on the same trajectories**, as an internal positive
control. Without their quantity as a control, a null in ours cannot be distinguished from a
broken reimplementation. That is what separates (b) from (c).

**(a) A biphasic peak survives in I_C^(3).** Some rule shows a genuine, refuter-surviving,
pairwise-blind order-3 maximum at intermediate noise. This would be **the first published
spike in a pairwise-blind higher-order quantity anywhere** — the operating point the survey
went looking for and did not find in the literature. It is a significant positive; it is
model-only; and it must face a refuter pass before it is written down as anything else.

**(b) I_C^(3) is flat or monotone while Ω reproduces their biphasic peak.** Their spike is a
spike in a non-pairwise-blind quantity, exactly as `SPIKE_SURVEY.md` predicts from the 2026
PRL. This is a **clean negative about the measure, not about the system** — and it is
publishable-grade, because the substrate is the one substrate in the survey where the
artifact mechanism is structurally absent, so the null is about the dynamics rather than the
readout. Combined with P2 (ten rules with nonzero Ω and exactly zero I_C^(3)) it is a
two-sided separation of the two quantities on a real system.

**(c) Both flat.** We failed to reproduce their result at all. The discrepancy is then about
implementation, not physics, and no conclusion about the measure may be drawn. Reported as a
failure to reproduce, with the entropy check P0 named as the diagnostic.

**Kill, staked first and separable** (from `SPIKE_SURVEY.md` §8): *if for every rule tested,
max over P_n of I_C^(3) fails to exceed its P_n = 0 value by more than the surrogate null's
5 sd, then noise-enhanced whole-only structure is refuted on the one substrate where the trap
cannot explain it away.* That kill takes down the noise-enhancement hypothesis **and nothing
beneath it** — not the rent clause, not the third-in-time result, not `pairwise_blind_to_parity`,
and not the `wild-share` open claim, which concerns nature and is untouched by a model system.

## 10. GATES — machinery must pass before any sweep number is believed

| gate | requirement |
|---|---|
| **G1** share machinery | `array_cap_experiment.gate()` PASSes: exact parity → ln 2 saturating its cap, exact independence → 0, k=5 code state → 2 ln 2, IPF residual < 1e−12, `shareK` ≡ `bench_detector.C3` |
| **G2** batched IPF | the GPU/batched IPF used here reproduces the reference `shareK` to < 1e−12 on 1000 random 2×2×2 states |
| **G3** ECA engine | the bitwise ring engine reproduces a naive per-cell reference implementation **bit-identically** for **all 256 rules**, 50 steps, n = 17, from common random initial states |
| **G4** noise engine | measured per-bit flip rate equals P_n within Monte-Carlo error at all 17 noise levels, on both the dense and the sparse code path, and the two paths agree where both are valid |

G3 is what licenses the whole experiment: without it, "rule 110" is an assumption.

## 11. DELIVERABLES

`scratchpad/eca_spike.py` (engine + gates + sweep) and `scratchpad/ECA_SPIKE_RESULTS.md`.
This prereg is committed first, on its own. Results, the script and the raw JSON follow in a
second commit. The fired kill, if it fires, is reported as plainly as a survival would be,
and any dead claim stays in the record marked dead.
