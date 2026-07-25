# SPIKE SURVEY — who has published a peak in higher-order structure?

Literature survey, scratchpad only. Nothing here touches the Lean library, `Stance.lean` or the
audit. The question: **has anyone published a claimed spike — a peak, resonance or sharp
maximum — in higher-order / synergistic / whole-only structure as a function of a control
parameter?** A real one would be an operating point, and operating points have applications.

Our quantity, fixed here so the adjudication has something to be adjudicated against, is the
**connected information of order k** (Schneidman, Still, Berry, Bialek, *Phys. Rev. Lett.* **91**,
238701 (2003), [arXiv:physics/0307072](https://arxiv.org/abs/physics/0307072)):

> I_C^(k)({x_i}) = S[P̃^(k−1)({x_i})] − S[P̃^(k)({x_i})],  where P̃^(k) is "the maximum entropy
> distribution consistent with all of the k-th order marginals", and I({x_i}) = Σ_{k=2}^N I_C^(k).

`I_C^(3)` is what `Core/Third.lean` calls the whole-only share. It is **pairwise-blind by
construction**: it is exactly the entropy gap that all pairwise marginals cannot close. This is
the property every candidate below is tested against, and it is the property almost none of them
has.

---

## VERDICT

**Nobody has published a spike in a pairwise-blind order-3 quantity. Not one of the thirteen
candidates below measures `I_C^(≥3)`, and the four that spike sharply in real data all measure
something of order 1 or 2.**

The field is not empty because the effect is absent — it is empty because **the standard
"higher-order" instruments are not pairwise-blind**, and this is now a theorem, not a suspicion:
Caprioglio, Mediano & Berthouze prove that "*pairwise interactions can give rise to synergistic
information in the absence of explicit high-order mechanisms*" (*Phys. Rev. Lett.* **136** (2026),
[arXiv:2505.24686](https://arxiv.org/abs/2505.24686)). O-information, S-information, PID synergy,
ΦID synergy, Φ, TSE complexity and specific heat are all in that class. They can be large, and can
peak, while `I_C^(3)` is exactly zero.

Two results were derived here rather than found, and they dispose of a whole family of claims at
once — see §**The symmetry lemma**. In one line: **a spin system with global sign symmetry has
*identically zero* connected information at every odd order, at every temperature, including at
criticality.** Every "higher-order structure peaks at the critical point of the Ising model" claim
is therefore, for our quantity, a claim about a quantity that is exactly zero throughout.

**One candidate is worth reproducing** — Orio, Mediano & Rosas — and not because its measurement
is right (it is not) but because its *substrate* is the only one in the survey that is immune to
our standing static-nonlinearity trap by construction. Details in §**What to reproduce**.

---

## RANKED TABLE

Ranked by how close the claim comes to being a genuine pairwise-blind spike. Rank 1 is closest.
"Pairwise-blind?" asks whether the quantity vanishes when the system's joint distribution is the
maxent distribution matching all its pair marginals. **No candidate answers yes.**

| # | Who / where | Quantity | Spikes vs. what | Data or model | Pairwise-blind? | Static-nonlinearity vulnerable? |
|---|---|---|---|---|---|---|
| 1 | **Orio, Mediano & Rosas**, *Chaos* **33**, 123103 (2023), [arXiv:2305.13454](https://arxiv.org/abs/2305.13454) | O-information Ω, S-information Σ | **bit-flip noise probability P_n**, biphasic peak at intermediate noise | **model** (elementary cellular automata, n=17) | **No** — Ω = TC − DTC, nonzero for purely pairwise systems | **No** — states are natively binary; no acquisition threshold, nothing to fold |
| 2 | **Marinazzo, Angelini, Pellicoro & Stramaglia**, *Phys. Rev. E* **99**, 040101(R) (2019), [arXiv:1901.05405](https://arxiv.org/abs/1901.05405) | PID synergy of transfer entropy, 1 target + 2 source spins | **temperature**; "synergy peaks in the disordered phase", redundancy peaks at T_c | **model** (2D Ising) | **No** — and worse, `I_C^(3)` is *provably zero* in the regime of the peak (see lemma) | No clip; but the peak sits where our quantity is identically 0 |
| 3 | **Fang, Mahankali, Wang et al.**, *Nat. Commun.* **16** (2025), [10.1038/s41467-025-57778-7](https://doi.org/10.1038/s41467-025-57778-7), [arXiv:2402.18552](https://arxiv.org/abs/2402.18552) | quantum Fisher information density f_Q | **"a sharp peak at the QCP, reaching the value around 2.2"**, exceeding the bound of 2 ⇒ ≥3-partite entanglement | **DATA** (inelastic neutron scattering, heavy-fermion metal) | **No** — f_Q is an integral of χ″(Q,ω), a **two-point** correlation function | No; but multipartiteness is *inferred via a bound on 2-point data*, never measured |
| 4 | **Tkačik, Mora, Marre, Amodei, Berry & Bialek**, [arXiv:1407.5946](https://arxiv.org/abs/1407.5946) | specific heat c(T) of a fitted **K-pairwise** maxent model | **temperature T and population size N** — "a dramatic peak … the peak grows and moves closer to T=1" | **DATA** (salamander retina) | **No** — computed *entirely from a pairwise model*, so `I_C^(≥3)` contributes exactly 0 by construction | **Yes** — spike detection is a voltage threshold; and see the Nonnenmacher refutation below |
| 5 | **Timme, Marshall, Bennett, Ripp, Lautzenhiser & Beggs**, *Front. Physiol.* **7**:425 (2016), [10.3389/fphys.2016.00425](https://doi.org/10.3389/fphys.2016.00425) | TSE neural complexity C_N | **transmission probability p_trans**: "complexity peaked near p_trans ≈ 0.265" | **model** (cortical branching model). The cultures have **no** control parameter | **No** — built from mutual information of subsets | **Yes** — 5-sd voltage threshold, then binarised at ~7 ms bins. *And see the authors' own control* |
| 6 | **de Oliveira, Rigolin & de Oliveira**, *Phys. Rev. A* **73**, 010305(R) (2006), [arXiv:quant-ph/0507253](https://arxiv.org/abs/quant-ph/0507253) | Meyer–Wallach Global Entanglement Q | **transverse field**: "maximal at the critical point for the Ising chain" | **model** (analytic) | **No** — Q = (2/n) Σ_i (1 − tr ρ_i²) is a function of **single-qubit** reduced states: an *order-1* quantity | No |
| 7 | **Barnett, Lizier, Harré, Seth & Bossomaier**, *Phys. Rev. Lett.* **111**, 177203 (2013) | global transfer entropy | **temperature**; peaks *in the disordered phase*, not at T_c | **model** (kinetic Ising) | **No** — bipartite (source → target) | No; same symmetry lemma applies |
| 8 | **Khajehabdollahi et al.**, *Entropy* **22**, 339 (2020), [10.3390/e22030339](https://doi.org/10.3390/e22030339) | integrated information Φ | **temperature**; susceptibility of Φ peaks at T_c | **model** (generalised Ising) | **No** — Φ is defined by **minimising over bipartitions**: bipartite by construction | No; same lemma |
| 9 | **Stocks**, *Phys. Rev. E* **63**, 041114 (2001) — suprathreshold stochastic resonance | input–output mutual information | **noise intensity**; peaks at nonzero noise, ≈ 0.5 log₂(N) bits | model + experiment | **No** — bipartite | **Yes, definitionally** — the effect *requires* an array of threshold devices. This is the family our own σ=1e-3 peak fell into |
| 10 | **Wang, Zhu & Liu**, *Proc. R. Soc. A* **482**:20250945 (2026) | SR response / SNR | **noise intensity**, under 3-body simplicial coupling | model | **No** — the "higher-order" is in the *coupling*, not in the measured quantity | **Yes** — bistable potential (a saturating nonlinearity) |
| 11 | **Luppi, Mediano, Rosas et al.**, *Nat. Neurosci.* **25** (2022); *eLife* **12**:RP88173 (2024), [10.7554/eLife.88173](https://doi.org/10.7554/eLife.88173) | ΦID synergy | **no spike** — discrete state contrasts, no control parameter | DATA (fMRI) | **No** — "*groups of four variables: the past and future of region X, and the past and future of region Y*": an **edge** quantity on region *pairs* | n/a |
| 12 | **Tononi, Sporns & Edelman**, *PNAS* **91**, 5033 (1994) | TSE complexity | peak between order and disorder is **definitional**, built into the construction | definitional | **No** | n/a |
| 13 | **Varley & Bongard**, *Chaos* **34**, 063127 (2024), [arXiv:2401.14347](https://arxiv.org/abs/2401.14347) | O-information | **no spike** — synergy is an evolutionary *target*, not a function of a swept parameter | model | **No** | n/a |

---

## THE SYMMETRY LEMMA — derived here, and it disposes of #2, #7, #8 at once

Candidates 2, 7 and 8 all claim a higher-order peak in an Ising-type model. All three are
disqualified by a single fact, which is easier to state than to find in the literature:

> **A distribution over binary variables that is invariant under global sign flip, p(s) = p(−s),
> has connected information exactly zero at every odd order.**

The reason is elementary. Global sign symmetry forces every odd moment to vanish — ⟨s_i⟩ = 0,
⟨s_i s_j s_k⟩ = 0 — so the third-order marginals contain no information the second-order marginals
do not already carry, and the maxent distribution matching all pairs already matches all triples.
The gap I_C^(3) = S[P̃^(2)] − S[P̃^(3)] is therefore identically zero, for *any* pair-correlation
structure and at *any* temperature, including at T_c.

Checked numerically rather than asserted (`ising3b.py`, `z2_k4.py`, scratchpad, not committed;
maxent by iterative proportional fitting, tolerance 1e-15):

| test | result |
|---|---|
| 2000 random Z2-symmetric 3-variable distributions | max &#124;I_C^(3)&#124; = **1.9e−10 nats** |
| 60 random Z2-symmetric 4-variable distributions, odd order | max &#124;I_C^(3)&#124; = **1.7e−13 nats** |
| the same 60 draws, **even** order | max &#124;I_C^(4)&#124; = **0.169 nats** — even orders survive |
| positive control: 3-coin parity | I_C^(3) = **0.693147181** = ln 2 exactly (saturates the cap) |
| positive control: explicit 3-body coupling K = 0.9 | I_C^(3) = **0.247 nats** |
| positive control: 4-bit parity | I_C^(3) = **0.0**, I_C^(4) = **0.693147181** = ln 2 |

The instrument is not stuck at zero — it fires at the cap on parity and at 0.247 on an explicit
three-body term. It reads zero on sign-symmetric systems because there is nothing there.

**Two consequences, and the second is the one that costs us something.**

1. **The 2D Ising model in its disordered phase — exactly where Marinazzo et al. locate their
   synergy peak — has zero order-3 connected information at every temperature they scan.** Their
   peak is real, and it is a peak in a quantity that is not ours. This is the sharpest available
   demonstration that PID synergy and whole-only share are different things: one peaks where the
   other is identically zero.
2. **Do not go looking for whole-only spikes in symmetric spin models.** Ising, transverse-field
   Ising, the kinetic Ising model, and the Z2-symmetric maxent models of neural criticality are all
   *structurally* incapable of carrying odd-order connected information above the symmetry-breaking
   transition. If we want an order-3 spike from a spin system, the field must be nonzero or the
   symmetry must be broken — and then the effect competes with the magnetisation, not with the
   critical fluctuations.

A related trap worth recording, because it caught us in draft: **a large three-point correlation
function is not order-3 structure.** A pairwise Hamiltonian with a field gives ⟨s₁s₂s₃⟩ = +0.914
and I_C^(3) = 1.8e−14 nats. The three-point correlator is a moment; the connected information is
what the pair marginals cannot reconstruct. They are not the same measurement and they do not
agree in sign, size or presence.

---

## ADJUDICATIONS THAT NEED MORE THAN A TABLE ROW

### #1 Orio, Mediano & Rosas — the only mechanically clean spike in the survey

The claim, verbatim from the text: "*some rules exhibit an increase in the absolute magnitude of
their O-information for intermediate levels of noise*", and for some rules "*a biphasic change of
S-information with intermediate levels of noise, showing an increase before decaying to zero*".
Noise is a bit flip: "*Noise was introduced via a probability that governed how likely an agent
would disobey the rule*". Estimators: plugin for deterministic runs, NSB for noisy ones, n = 17
agents.

**Three things are right about this paper and one thing is wrong.**

Right: the substrate has **no static nonlinearity anywhere in the chain**. Elementary cellular
automata are natively binary — there is no analogue state being thresholded, no clipping, no
saturation, nothing our reflecting-fold discriminator could even be applied to. The trap that has
now twice manufactured order-3 in this repository *cannot operate here*. Right, second: the noise
is dynamical, injected into the rule, not observational — so it is not a readout artifact.
Right, third, and to the authors' credit, they refute their own headline: "*when structure is
created by intermediate levels of noise … then it is of the redundant type … and not
synergistic*."

Wrong: the quantity. Ω = TC − DTC is not pairwise-blind, and by the 2026 PRL it can be driven
negative by pairwise structure alone. So the paper cannot distinguish "noise created whole-only
pattern" from "noise rearranged pairwise pattern", and its own S-information analysis suggests the
latter.

### #3 Fang et al. — the sharpest real-data spike in the survey, on a two-point observable

f_Q is extracted as f_Q = (2/π) ∫ tanh(ω/2T) χ″(Q,ω) dω, where χ″ is the imaginary part of the
dynamical spin susceptibility measured by inelastic neutron scattering. **That is a two-point
correlation function.** The three-partite conclusion comes from the witness inequality: f_Q >
m(h_max − h_min)² implies (m+1)-partite entanglement, and f_Q ≈ 2.2 > 2 gives m+1 = 3.

This is a legitimate and impressive result, and it is not our result. A *bound* saying "no
2-partite state can produce this two-point data" is not a *measurement* of three-body structure.
The distinction matters to us specifically: our `Core/ShareK.lean` cap works the same way — it
bounds what classical structure can produce — and we have been careful to say that hardware
reached only 36 % of the cap rather than that it saturated it. The same care applies in the other
direction here.

### #4 Tkačik et al. — a pairwise model's thermodynamics, and an artifact refutation on record

The specific heat is computed from the fitted K-pairwise maxent model, so it is a functional of
the pairwise marginals; `I_C^(≥3)` contributes exactly nothing to it. The paper is explicit that
third-order structure is a *prediction* it validates, not a quantity it measures: "*the model
accurately predicts the correlations among triplets*." A pairwise model predicting triplets
correctly is a statement that order-3 structure is *absent*, not present.

Independently, the peak itself is under an artifact charge that our own house rules would have
made mandatory to report: Nonnenmacher, Behrens, Berens, Bethge & Macke, "Signatures of
criticality arise from random subsampling in simple population models", *PLoS Comput. Biol.*
**13**(10):e1005718 (2017), [arXiv:1603.00097](https://arxiv.org/abs/1603.00097), reproduce the
same divergence from **random subsampling of a simple latent-variable population model** with no
criticality and no higher-order interactions. This is the same shape of finding as our own
whole-only/autocorrelation trap: a signature that survives its authors' checks and is then
reproduced by a null nobody had matched to the data's generative structure.

### #5 Timme et al. — the authors' own control is more damaging than anything I could add

The peak is in the branching **model** ("*complexity peaked near p_trans ≈ 0.265*"); the cultures
provide a correlation, not a swept parameter. But the decisive line is the authors' spike-swapping
control, which destroys pairwise spiking relationships and leaves complexity essentially
unchanged: "*complexity in neural systems was primarily dependent upon neuron firing rate and
avalanche profiles, not precise spiking relationships*", and, disarmingly, "*we did not expect to
find complexity values essentially unchanged by spike swapping*."

A complexity measure insensitive to the correlations between the units is measuring the marginals.
It is not an order-2 quantity in disguise; it is an **order-1** quantity in disguise. Reported here
as plainly as a positive result would be, because the authors reported it that way themselves.

### #6 Meyer–Wallach — the most extreme name/quantity mismatch found

Q(|ψ⟩) = (2/n) Σ_i (1 − tr ρ_i²) depends on nothing but the **single-qubit** reduced density
matrices. It is an average over one-body marginals. It is published, cited, and correct as
mathematics — and "Genuine Multipartite Entanglement in Quantum Phase Transitions" is a paper whose
headline quantity is order 1. The generalised measure the same paper introduces improves on this by
moving to **bipartite blocks**, which is order 2, not order 3.

### #9–#10 The stochastic-resonance family — our own artifact's home address

Suprathreshold stochastic resonance is the canonical noise-optimal information peak, and it exists
*because of* an array of threshold devices: remove the thresholds and the peak goes with them. Our
own apparent SR peak at σ = 1e-3, which collapsed 259× under a reflecting-fold boundary, is a
member of this family and should be cited as one rather than described from scratch. The 2026
Royal Society paper adds three-body coupling to the *dynamics* and then measures a classical SR
response in a bistable potential — the higher-orderness never reaches the observable, and the
bistable well is itself a saturating nonlinearity.

---

## WHAT TO REPRODUCE, AND WHAT IT MUST CONTROL FOR

**Reproduce #1 (Orio/Mediano/Rosas), with our instrument substituted for theirs. Reproduce
nothing else.**

The rationale is narrow and worth stating precisely, because it is not "this claim is probably
right". It is: **this is the only candidate whose substrate cannot express our standing trap.** In
elementary cellular automata there is no analogue quantity being clipped, thresholded, rectified or
saturated — the state is binary before anything measures it. Every other spike in the table either
runs through a threshold (4, 5, 9, 10) or measures a quantity that is provably zero or
provably low-order in the regime of its own peak (2, 3, 6, 7, 8, 12). So a null result here would
be informative in a way that a null result anywhere else would not: it would be about the
dynamics, not about the readout.

The hypothesis to pre-register, stated so its answer means something either way:

> Does bit-flip noise on a deterministic binary rule produce a **non-monotonic** `I_C^(3)` — a
> maximum at nonzero P_n strictly above the P_n → 0 value — on any rule?

Controls it must carry, each mapped to a trap this repository has already been bitten by:

1. **Substitute the instrument.** Measure `I_C^(3)` (the `shareK` / `C3` machinery in
   `scratchpad/array_cap_experiment.py` and `scratchpad/bench_detector.py`), not Ω or Σ. This is
   the whole point; O-information cannot answer the question asked.
2. **Pre-commit the XOR rules as expected, not discovered.** Rule 90 is s_{i−1} XOR s_{i+1} — that
   *is* parity, so it must read I_C^(3) = ln 2 at P_n = 0 by construction. It is a gate, not a
   finding. The real test is a rule with *low* deterministic order-3 that *gains* it at
   intermediate noise. Name those rules before running.
3. **Pairwise-maxent surrogate null, by IPF**, matched to the observed pair marginals — not an iid
   or Gaussian null. Our iid nulls false-fired at +42σ on timeseries and the i.i.d. multinomial
   surrogate went void at τ_int = 87 on the array.
4. **Replicas, not time pooling.** ECA rows are strongly autocorrelated in both space and time.
   Use independent initial conditions as the independent axis, exactly as
   `HABIT_DYNAMICS_RESULTS.md` Measurement 2 did with 12 288 structurally independent units — that
   is what made its z-scores quotable at κ ≥ 0.35 where the sibling run's were void.
5. **Cross-run control.** Build triples with slot j drawn from run j, identical rule and P_n,
   different seed. True share is zero by construction; any |z| > 5 proves the null mis-specified.
   This is the control that saved the habit-dynamics numbers and voided the array-cap ones.
6. **Disclose the tied fraction** at every P_n before believing any statistic (house rule 4).
7. **State the boundary discriminator as vacuous — and say why.** There is no clamp to fold, so
   clip-vs-fold carries no information. Unlike the CIRISArray case, where vacuity meant "we
   learned nothing about robustness", here it means "the artifact mechanism is structurally
   absent". Those are different statements and the memo must not blur them, in either direction.
8. **The kill, staked first and separable:** if for every rule tested, max over P_n of `I_C^(3)`
   fails to exceed its P_n → 0 value by more than the surrogate null's 5 sd, then *noise-enhanced
   whole-only structure is refuted on the one substrate where the trap cannot explain it away*.
   That kill takes down the noise-enhancement hypothesis and nothing beneath it.

Cost is small — ECAs are 256 rules, one dimension, and n = 3 triples are exactly what our
estimator is built for. The `I_C^(3)` machinery, the IPF surrogate, the cross-run refuter and the
tie counter all already exist in the scratchpad and have passed their gates.

**Second-ranked target: none.** This is worth saying rather than padding the list. Of the other
twelve, five have no swept control parameter at all, four measure a quantity that the symmetry
lemma pins to exactly zero in the regime of their own peak, and three are threshold-array
resonances of the kind we have already reproduced and already refuted in our own data.

---

## WHAT I DID NOT FIND — stated so the absence is on the record

- **No published measurement of `I_C^(k≥3)` as a function of a swept control parameter, in any
  field.** Schneidman et al. define it and evaluate it on fixed examples; the neural literature
  uses it to *compare model orders* at a fixed condition, not to trace a curve. The specific
  experiment we would want has, as far as this survey reaches, not been done by anyone.
- **No spike claim in a genuinely pairwise-blind quantity, anywhere.** Not in criticality, not in
  stochastic resonance, not in PID/ΦID, not in quantum many-body.
- **No empirical TSE-complexity peak.** The peak is definitional in Tononi–Sporns–Edelman and
  model-only in Timme et al.
- Searches that returned nothing usable: synergy vs. coupling strength in Kuramoto and coupled
  oscillator systems; higher-order interactions vs. bin width or population size in spike-train
  maxent work (population-size dependence is reported, but as a monotone trend toward
  pairwise-insufficiency, not a peak); dose-response inverted-U in synergy under anaesthesia or
  psychedelics.

**Caveat on reach.** This is a web-literature survey conducted in one pass. Several primary PDFs
would not render and were read through abstract pages, ar5iv, or locally extracted text; where a
paper's own words are quoted they were taken from the text or the abstract, and where I am relying
on a secondary summary I have not quoted. The Tkačik citation is given as its arXiv ID because that
is what was verified. A null from a survey is weaker evidence than a null from an experiment, and
the first bullet above should be read as "not found" rather than "does not exist".

---

## SOURCES

- Schneidman, Still, Berry & Bialek, *Phys. Rev. Lett.* **91**, 238701 (2003) — [arXiv:physics/0307072](https://arxiv.org/abs/physics/0307072)
- Caprioglio, Mediano & Berthouze, *Phys. Rev. Lett.* **136** (2026) — [arXiv:2505.24686](https://arxiv.org/abs/2505.24686)
- Orio, Mediano & Rosas, *Chaos* **33**, 123103 (2023) — [arXiv:2305.13454](https://arxiv.org/abs/2305.13454)
- Marinazzo, Angelini, Pellicoro & Stramaglia, *Phys. Rev. E* **99**, 040101(R) (2019) — [arXiv:1901.05405](https://arxiv.org/abs/1901.05405)
- Fang, Mahankali, Wang et al., *Nat. Commun.* **16** (2025) — [10.1038/s41467-025-57778-7](https://doi.org/10.1038/s41467-025-57778-7), [arXiv:2402.18552](https://arxiv.org/abs/2402.18552)
- Tkačik, Mora, Marre, Amodei, Berry & Bialek — [arXiv:1407.5946](https://arxiv.org/abs/1407.5946)
- Nonnenmacher, Behrens, Berens, Bethge & Macke, *PLoS Comput. Biol.* **13**(10):e1005718 (2017) — [arXiv:1603.00097](https://arxiv.org/abs/1603.00097)
- Timme, Marshall, Bennett, Ripp, Lautzenhiser & Beggs, *Front. Physiol.* **7**:425 (2016) — [10.3389/fphys.2016.00425](https://doi.org/10.3389/fphys.2016.00425)
- de Oliveira, Rigolin & de Oliveira, *Phys. Rev. A* **73**, 010305(R) (2006) — [arXiv:quant-ph/0507253](https://arxiv.org/abs/quant-ph/0507253)
- Barnett, Lizier, Harré, Seth & Bossomaier, *Phys. Rev. Lett.* **111**, 177203 (2013) — [10.1103/PhysRevLett.111.177203](https://doi.org/10.1103/PhysRevLett.111.177203)
- Khajehabdollahi et al., *Entropy* **22**, 339 (2020) — [10.3390/e22030339](https://doi.org/10.3390/e22030339)
- Luppi, Mediano, Rosas et al., *eLife* **12**:RP88173 (2024) — [10.7554/eLife.88173](https://doi.org/10.7554/eLife.88173)
- Stocks, *Phys. Rev. E* **63**, 041114 (2001) — [10.1103/PhysRevE.63.041114](https://doi.org/10.1103/PhysRevE.63.041114)
- Wang, Zhu & Liu, *Proc. R. Soc. A* **482**:20250945 (2026) — [10.1098/rspa.2025.0945](https://doi.org/10.1098/rspa.2025.0945)
- Varley & Bongard, *Chaos* **34**, 063127 (2024) — [arXiv:2401.14347](https://arxiv.org/abs/2401.14347)
- Tononi, Sporns & Edelman, *PNAS* **91**, 5033 (1994)
