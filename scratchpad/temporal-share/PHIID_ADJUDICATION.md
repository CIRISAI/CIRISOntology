# ΦID and neighbours vs. the temporal-share novelty note — adversarial adjudication

**Date:** 2026-07-25. **Role:** refuter. **Target:** the separable novelty note now live on the
page inside `third-in-tsvf`:

> "The mathematics is openly borrowed (it is the connected information of Amari and of
> Schneidman and colleagues, Zhou's quantum form); the recognition of putting it on the
> multi-time object is, after two literature passes, still not found in print."

Stated falsifier: *find a published pairwise-blind share on a multi-time object predating ours
(2026-07-24).*

**Our object, as pre-registered** (`DEFINITION_PREREG.md`, `TEMPORAL_ATTACK_PREREG.md`):
`share(p) := sup{H(q) : q matches ALL two-slot marginals of p} − H(p)`, with the slots being
TIME SLOTS — classically the 3-time joint distribution, quantumly the process-tensor Choi state
with von Neumann entropy and two-slot marginals by partial trace.

---

## VERDICT: **PARTIAL — the kill FIRES on the classical half and DOES NOT FIRE on the quantum half.**

- **FIRES:** putting the Amari/Schneidman connected-information construction on a *classical*
  multi-time object (a joint distribution over 3+ time bins of a discrete-time process) **is in
  print, twice, and by Amari himself.** The sentence as currently worded is false and must be
  changed. ΦID is *not* what fires it — ΦID is a clean miss on both conditions. What fires it is
  the neural spike-train maximum-entropy literature, which the two prior passes did not search.
- **DOES NOT FIRE:** no published work defines the maximum-entropy irreducible-correlation share
  on a *multi-time quantum* object — process tensor, quantum comb, or multi-time Choi state —
  nor anything equivalent. Zhou's quantum irreducible correlation exists only on spatial
  n-partite states; the multi-time quantum literature uses bipartite mutual information, GME
  witnesses, and memory hierarchies, never a maxent-over-marginals share. The
  memory-saturation characterisation is likewise unfound.

The honest reading: **the recognition was ours only in the quantum sector.** The classical
recognition is twenty years old and belongs to the people who invented the mathematics.

---

## Per-candidate adjudication

### 1. ΦID — Mediano, Rosas et al., arXiv:1909.02297 · **DOES NOT FIRE (clean miss, both conditions)**

Read in full text (PDF extracted locally). The decomposed object is stated verbatim in Eq. (1):
`E = I(X1, X2; Y1, Y2)`, and immediately afterwards: *"where X and Y denote the states at times t
and t + 1 respectively, and the subscript denotes variable index. We consider the decomposition
of E into modes of information dynamics, focusing on systems with Markovian dynamics, leaving
extensions to processes with memory for future work."* So the object is a mutual information
between **exactly two time slices**, and the indices being decomposed are the **spatial** variable
labels 1 and 2, not time. Condition (a) fails outright. Condition (b) fails independently: the
construction is a double-redundancy lattice `A := {{1},{2},{1,2},{{1},{2}}}` with a Möbius
inversion over the PID redundancy lattice — no maximum-entropy projection anywhere. The paper's
only mention of maxent is a footnote holding it at arm's length: *"the maximum entropy
distributions employed by some causal integration frameworks are well-defined for discrete
Markovian systems, but in general may not always exist."* ΦID's atoms (Red→Syn, Syn→Un¹, …) are
pairs of PID atoms evolving past→future; being Möbius-lattice quantities they are functions of
low-order marginals by construction, the opposite of pairwise-blind.

### 2. Extended/unified taxonomy — arXiv:2109.13186 → PNAS 122(39):e2423297122 (2025) · **DOES NOT FIRE**

Read in full text. Same two-time structure, and the paper says so in its own limitations section,
verbatim: *"it is important to remark that the framework presented in this paper focuses on
decomposing the mutual information between two time points. While this captures all the
information carried from past to future in Markovian systems, it might miss relevant phenomena in
systems with non-Markovian dynamics."* The Methods confirm the construction: a forward PID
(*"variables at time t and t + 1 are sources and targets"*) crossed with a backward PID, giving
16 atoms — 4×4 over the two *spatial* variables. A footnote defers the multi-time case entirely:
*"In non-Markovian systems the corresponding quantity is known as excess entropy. Information
decomposition in non-Markovian systems will be covered in a subsequent publication."* Note the
general excess entropy `E = I(past ; future)` does involve many time points, but only as **two
blocks**; the decomposition indices remain the spatial variables, so nothing in ΦID quantifies
what is invisible to all two-*time* marginals. The PNAS version could not be read (HTTP 403,
paywall); arXiv shows only v1 and the PubMed abstract adds no time-point statement, so this
adjudication rests on the preprint of the same work. The PLOS One variant "Decomposing past and
future: ΦID based on shared probability mass exclusions" (2023) changes the redundancy function
inside the same lattice and inherits the same two-block time structure.

### 3. Nakahara, Amari & Richmond — *A comparison of descriptive models of a single spike train by information-geometric measure*, Neural Computation 18(3):545–568 (2006); RIKEN BSIS Tech. Report No05-1 (2005) · **FIRES (classical)**

This is the kill. Read in full from the RIKEN technical report (the authors' extended version of
the journal paper). The variables are **time bins of one neuron**, verbatim: *"For a spike train
of a single neuron, consider a time period of N bins, where each bin is so short that it can have
at most a single spike… Let X_N = (X_1, ⋯, X_N) be N binary random variables… Each X_i indicates
a spike in the i-th bin."* That is exactly our classical object: a joint distribution over N ≥ 3
time slots. The pairwise-blind construction is then stated explicitly, verbatim: *"This model is
characterized by setting (θ_3, ..., θ_N) = (0, ..., 0) and thus, the model that can be determined
completely by the first and second-order statistics (η_1, η_2) under the maximum entropy
principle. We call this model the 2nd-order IG model."* For binary variables (η_1, η_2) is
precisely the set of all pairwise marginals, at **all lags**, with no contiguity restriction — the
same constraint set as our `share`. The paper's whole analytic content is the behaviour of
θ_3, θ_4, … (they compare the inhomogeneous-Markov and mixture-of-Poisson models by the sign
structure and magnitude of the third- and higher-order terms), i.e. exactly the content the
all-pairs maxent cannot see, on a multi-time object. **One residual difference, and it is thin:**
they report the orthogonal θ-coordinates rather than the scalar entropy gap. Amari's own
divergence decomposition makes those the same information (the connected information of order ≥3
is `KL(p ‖ p_2nd-order-IG) = H(p_2nd-order-IG) − H(p)`), and the paper is built on that framework
— but the scalar is not printed here. Enough to fire: the *recognition* our sentence claims is
Amari's, applied by Amari, to time bins, in 2005.

### 4. Marre, El Boustani, Frégnac & Destexhe, Phys. Rev. Lett. 102, 138101 (2009) · **FIRES (scalar, weaker constraint set)**

Read in full text (arXiv:0903.0127). They print the scalar our claim is about, on multi-time
objects, verbatim: *"We also computed the fraction of the ensemble correlations that was captured
by the Markov model, I_2/I_n = (S_1 − S_2)/(S_1 − S_n), where S_k is the entropy when taking into
account the correlations up to the k-th order [7, 16]. … The value is maximal for two time bins,
and then decreased (Fig. 2B)."* References [7, 16] are Schneidman's — this *is* the connected
information ratio — and Fig. 2B plots it against the number of time bins in the pattern, with
Fig. 1 showing patterns of *"1, 2 and 3 time bins."* So a Schneidman connected-information
quantity, computed on a 3-time-bin joint distribution, in 2009. **The scope caveat is real:**
their order-2 model constrains only `m_i`, `C_ij = <σ_i(t)σ_j(t)>` and `C¹_ij =
<σ_i(t)σ_j(t+1)>` — pairs at lag ≤ 1 — plus a detailed-balance/Markov approximation. The lag-2
pair marginal of a 3-bin block is *not* constrained, so their residual `S_2 − S_n` is strictly
larger than the pairwise-blind share and does not isolate content invisible to *all* two-time
marginals. Cessac's review (arXiv:1302.5007) confirms the constraint set independently: *"Here
spatio-temporal pairs with memory depth 1 are considered."* Taken alone this would be a near
miss; taken with candidate 3, which supplies exactly the missing all-pairs maxent on time bins,
the classical recognition is fully covered in print.

### 5. Cessac and colleagues — spatio-temporal maximum-entropy / Gibbs distributions for spike trains (arXiv:1302.5007 review; 1209.3886; 1404.3470) · **NEAR MISS, does not itself fire**

The framework admits arbitrary spatio-temporal monomials `σ_{i1}(t_1)…σ_{ik}(t_k)` with finite
memory depth D, so a "pairwise, depth-D" model does constrain pairs across a block of D+1 time
bins — a maximum-entropy model on a multi-time object. But this line fits models and reports
Kullback–Leibler divergence and prediction quality; I found no paper in it computing the
Schneidman/Amari connected-information hierarchy or an entropy gap identified as the
pairwise-invisible content of the multi-time block, and practice stays at D = 1–2. Supporting
context for the fire above, not an independent one.

### 6. Tang et al., J. Neurosci. 28(2):505 (2008) · **DOES NOT FIRE**

Their maximum-entropy model is fitted on **single time bins**. The temporal analysis is post-hoc:
states drawn from P₂ are *"randomly concatenat[ed]"* into artificial sequences and compared to
data by a Kolmogorov–Smirnov test; time-lagged correlations are discussed only as *"a candidate"*
for future work, never entered as model constraints. No multi-bin joint maxent, and the
multi-information fraction is reported for single-bin patterns only. The follow-up
"higher-order Markov representation of instantaneous pairwise maximum entropy model"
(PMC3240351) also constrains only t and t−1 and computes no information ratio.

### 7. O-information and dynamic O-information — Rosas et al., Phys. Rev. E 100, 032305 (2019); Stramaglia, Scagliarini, Rosas & Faes, Front. Physiol. 11:595736 (2020) · **DOES NOT FIRE**

Two independent failures. (b): the O-information is `TC − DTC`, an algebraic combination of
entropies of subsets — no maximum-entropy projection, no marginal-matching variational problem.
It is a *low-order* descriptor of high-order structure by its authors' own framing (cf. "Gradients
of O-information: Low-order descriptors of high-order dependencies", PRR 5, 013025), which is the
opposite of pairwise-blind. (a): dΩ is defined as the variation of O-information from adding a
target to a set of sources while conditioning out the target's own past — a directed measure over
multivariate time series with the temporal structure collapsed to past-block/present, not a
functional of a 3-time joint. The quantum sibling, Rosas et al. "Quantifying High-Order
Interdependencies in Entangled Quantum States" (PRA 109, 042605 / arXiv:2310.03681), carries the
same construction onto spatial quantum states — same two failures, plus it is not multi-time.

### 8. James, Ellison & Crutchfield, *Anatomy of a Bit*, Chaos 21, 037109 (2011) · **DOES NOT FIRE**

This one genuinely operates on multi-time joints — L consecutive observations, past/present/future
— so condition (a) is met. Condition (b) is not: the measures are I-diagram/Möbius quantities
(entropy rate, total correlation, multivariate mutual information, binding information, predictive
information rate). There is no maximum-entropy projection onto pairwise marginals anywhere in the
construction. Total correlation is *order-1*-blind (it is measured against the product of
singleton marginals), not pairwise-blind; it therefore counts as "whole-only" exactly the content
our share is designed to exclude.

### 9. Quantum multi-time literature · **DOES NOT FIRE — swept, nothing close**

- **Zhou, PRL 101, 180505 (2008)** — irreducible k-party correlation `C^(k)(ρ) = S(ρ̃^(k)) −
  S(ρ̃^(k−1))` via the maximum-entropy state with fixed k-RDMs. This is our functional's quantum
  form and we cite it as borrowed — but it is defined on **spatial n-partite states**. No temporal
  or causal-ordering content.
- **arXiv:2312.10147, "Relations between Markovian and non-Markovian correlations in multitime
  quantum processes"** — re-verified independently of the earlier pass by grepping the full text:
  zero occurrences of "maximum entropy", "maxent", "irreducible", or "connected information"; the
  single "tripartite" hit refers to a maximally entangled tripartite state. Bipartite mutual
  information on Choi states only. Prior pass confirmed.
- **Milz, Modi et al., "Genuine Multipartite Entanglement in Time", SciPost Phys. 10, 141 (2021)**
  — GME structure of causally ordered combs. Entanglement classification, not an entropy share;
  excluded by the adjudication criteria and, independently, defines no maxent quantity.
- **"Characterising the Hierarchy of Multi-time Quantum Processes with Classical Memory",
  Quantum 8, 1328 (2024)** — full text grepped: no "maximum entropy", no "irreducible", no
  "connected information". The hierarchy is by memory type, not by correlation order.
- **Das & Sen, "Maximum entropy principle for quantum processes" (arXiv:2506.24079, June 2025)** —
  title is the closest false alarm in the corpus. It concerns maximal *output* entropy of a
  channel under a fixed-energy constraint (answer: absolutely thermalizing channels). No
  marginals, no multi-time object, no share.
- Also swept without a hit: quantum comb tomography and continuum-limit comb papers, "Practical
  learning of multi-time statistics" (arXiv:2412.17862), quantum Markov order, and the
  higher-dimensional information lattice line (arXiv:2512.20793, spatial).

### 10. Non-arXiv venue pass

Searched across Neural Computation, Physical Review Letters / E / A / Research, PNAS, PLOS One,
Journal of Neuroscience, Frontiers, Nature Communications / Communications Biology / npj
Complexity, Chaos, Entropy, Scientific Reports, Quantum, SciPost. The only fires are candidates
3 and 4 — both non-arXiv-primary (Neural Computation and PRL), which is precisely why two prior
arXiv-weighted passes missed them. Recorded as a method lesson: the novelty check was searching
the information-theory and quantum-foundations literatures and not the neural spike-train
maximum-entropy literature, where this construction has lived since 2003.

---

## Required re-wording (exact)

**In `third-in-tsvf`, `plain`, step One — replace the final clause.**

Current:

> "The mathematics is openly borrowed (it is the connected information of Amari and of Schneidman
> and colleagues, Zhou's quantum form); the recognition of putting it on the multi-time object is,
> after two literature passes, still not found in print."

Replacement:

> "The mathematics is openly borrowed (it is the connected information of Amari and of Schneidman
> and colleagues, Zhou's quantum form). We claimed here that putting it on a multi-time object was
> new. For classical processes that was wrong, and a third literature pass found it: Amari's own
> hierarchy was applied to the joint distribution of a single spike train over N time bins by
> Nakahara, Amari and Richmond (Neural Computation 18, 545, 2006), whose second-order model is the
> maximum-entropy fit to all two-bin marginals, and Schneidman's connected-information ratio was
> computed on two- and three-time-bin patterns by Marre and colleagues (Phys. Rev. Lett. 102,
> 138101, 2009). We withdraw the classical half of the claim. What three passes still do not find
> in print is the quantum form — the same variational functional on a process tensor's multi-time
> Choi state, von Neumann entropy, two-slot marginals by partial trace — nor the memory-saturation
> result that goes with it."

**In `kill` — replace the second falsifier.**

Current:

> "Separable second falsifier, for the novelty note only: find a published pairwise-blind share on
> a multi-time object predating ours."

Replacement:

> "Separable second falsifier, for the novelty note only: find a published maximum-entropy
> irreducible-correlation share defined on a multi-time QUANTUM object — a process tensor, quantum
> comb, or multi-time Choi state, with two-slot marginals taken by partial trace — predating ours
> (2026-07-24). The classical case is conceded above and is no longer claimed."

**In `confidence` — replace the survival sentence.**

Current:

> "The share framing survived kill-checks on 2026-07-24 and 2026-07-25; a non-arXiv venue could
> still fire it, and would be reported the day it is found."

Replacement:

> "The share framing's classical half was KILLED on 2026-07-25 by a third pass (Neural Computation
> 2006; Phys. Rev. Lett. 2009) and is withdrawn above; the quantum half survived that pass. The
> two earlier passes missed it by searching the information-theory and quantum-foundations
> literatures and not the neural spike-train maximum-entropy literature."

None of the theorems are touched. `share_parity`, `temporal_third_saturates`,
`vnEntropy_causal_past`, `vnEntropy_triangle` and `temporal_logos_is_memory` stand exactly as
proved; only the priority sentence changes. This is the second convergent-art finding on this
claim (the first being arXiv:2505.13681 for the causal bound), and the pattern is worth naming:
every part of this result that could be found in print has been found in print, and what remains
ours is the formalization and the quantum lift.

## Sources

Primary texts read in full: arXiv:1909.02297 · arXiv:2109.13186 · arXiv:0903.0127 ·
RIKEN BSIS Tech. Report No05-1 (Nakahara, Amari & Richmond) · arXiv:1302.5007 · arXiv:2312.10147 ·
arXiv:2506.24079 · Quantum 8, 1328 (2024) · arXiv:1808.05602.
Read via abstract/secondary only (paywalled or 403): PNAS 122(39):e2423297122 ·
Neural Computation 18(3):545 journal version · J. Neurosci. 28(2):505 (read via PMC full text) ·
PRA 109, 042605 · SciPost Phys. 10, 141.
