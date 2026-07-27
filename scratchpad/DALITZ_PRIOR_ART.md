# DALITZ PRIOR ART — convergent-art adjudication

**Campaign.** Measure the pairwise-blind whole-only share (order-3 connected information) of a
three-body decay Dalitz distribution, and its CP-conjugate difference.

**House standard applied** (`convergent-art-pattern`): *assume the result is already in print
until the primary text says otherwise; search by the mathematical object, not by our
vocabulary.* This document is written before any measurement and before `DALITZ_PREREG.md`.

**Scratchpad only.** No Lean, no `Stance.lean`, no audit, `lake` never run.

---

## VERDICT, in one paragraph

**CLEAR on the instrument, CROWDED on the target, and the mission brief's own premise is
WRONG on one point of physics.**

The specific quantity — a maximum-entropy-over-pair-marginals entropy gap on the Dalitz plane —
appears **nowhere** in the indexed high-energy-physics literature. Four independent
fulltext probes return literally zero hits. But the *target* — model-independent, amplitude-fit-free
detection of CP violation in three-body phase space — is a mature seventeen-year-old
programme with at least four established method families and dozens of published measurements,
and **every one of those methods is a two-sample test or a moment, not an entropy gap**. So the
honest verdict is **CONVERGENT-ADJACENT**, not CLEAR: nobody has computed our number, and we
are nonetheless the fifth instrument onto a well-stocked shelf. The credit paragraph in §4 is
mandatory on anything we publish.

**And the correction we owe ourselves, stated first because it is load-bearing:** the mission
brief says *"T-odd triple products in three-body decays are already-measured CP observables and
are sign-triple moments (our b=2 instrument in particle-physics clothes)."* **That is false for
three-body decays.** See §5. It does not sink the campaign, but it removes the claim that our
instrument is a known observable in disguise, and it changes what the prereg may assert.

---

## 1. WHAT THE OBJECT IS, so the search can be by object

The quantity we propose to measure, stated so a statistician outside this repository could
recognise it under any name:

> Given a joint distribution `P` on three discrete slots, form the maximum-entropy distribution
> `Q` carrying **all three pair marginals of `P` exactly** and nothing else. The whole-only
> share is `S(Q) − S(P)`: the entropy gap between the state and the best reconstruction of it
> from its own pairs. It is zero if and only if `P` is reconstructible from its pairs.

Names it goes by in other fields, all searched:

| name | field | reference |
|---|---|---|
| **connected information** of order 3 | computational neuroscience | Schneidman, Still, Berry & Bialek, PRL 91:238701 (2003) |
| **irreducible correlation** | quantum information | Zhou, PRA / arXiv:0803.2747 (2008); Linden–Popescu–Wootters |
| higher-order **interaction information** / maxent hierarchy | information geometry | Amari, IEEE Trans. Inf. Theory 47:1701 (2001) |
| **multi-information minus its pairwise part** | statistics | Studený–Vejnarová |

This repository's own machine-checked form is `share` in `Core/Share.lean`, with
`share_parity = log 2` and the vanishing lemma `share_eq_zero_of_signSymmetric`
(`Core/SignSymmetry.lean`).

---

## 2. THE SEARCH ACTUALLY PERFORMED, with counts

**Instrument.** INSPIRE-HEP REST API (`inspirehep.net/api/literature`), which supports
**fulltext** search over the indexed corpus via the `ft` operator — the right tool for
convergent-art work in this field, because it finds a method mentioned in a body paragraph and
not in any title or abstract. Queries were run 2026-07-26. Session WebSearch budget was
exhausted before this campaign began, so Google Scholar, ADS and the general web were **not**
searched; that limitation is stated again in §6.

### 2a. The object itself — four probes, all empty

| query (INSPIRE fulltext) | hits | what they were |
|---|---|---|
| `ft "Dalitz plot" and ft "Shannon entropy"` | **0** | — |
| `ft "Dalitz plot" and ft "connected information"` | **0** | — |
| `ft "entropy of the Dalitz"` | **0** | — |
| `ft "Dalitz plot" and ft "earth mover"` … (see §3c) | 0 for "earth mover" as a phrase | the EMD paper says "earth mover's" |

### 2b. Near-object probes — nonzero, but nothing is a measurement

| query | hits | adjudication |
|---|---|---|
| `ft "Dalitz plot" and ft "mutual information"` | **4** | *Review of Particle Physics*-class reviews and school proceedings (coincidental co-occurrence); Friedman 1974 lectures; and one thesis (Tan, *Learning invariant representations*, 2020) that uses mutual information as an **adversarial training penalty** to decorrelate a classifier from a variable — an optimisation objective, not a measurement of the data's information structure. **None computes an information quantity of a Dalitz distribution.** |
| `ft "Dalitz plot" and ft "relative entropy"` | **2** | two theses, neither a Dalitz information measurement |
| `ft "Dalitz plot" and ft "Kullback-Leibler"` | **10** | RPP; a 3π rescattering paper; a machine-learning sampling paper (Kofler 2024, KL as a training loss); Rolke's two-sample power study (§3d). **KL appears as a fit/training loss or a two-sample distance, never as a maxent gap.** |
| `ft "connected information"` (all of INSPIRE, no Dalitz restriction) | **20** | only one is the object: **Zhou, arXiv:0803.2747**, "Irreducible multi-particle correlations in states without maximal rank" — the *quantum* version of exactly our hierarchy, on quantum states, with no phase-space or decay application. The rest are the English words "connected" and "information" adjacent. |
| `t "entropy" and t "CP violation"` (titles) | **1** | Berger 2012, entropy flow in `B⁰B̄⁰` evolution — a different object entirely (von Neumann entropy of the two-state system, not a phase-space distribution) |
| `ft "interaction information" and ft "Dalitz"` | 11 | **all false positives** — the English phrase "the interaction information", in meson–nucleus and Efimov papers |
| `ft "Dalitz plot" and (ft "synergy" or ft "redundancy" or ft "O-information")` | 201 | reviews using "synergy" in its ordinary English sense (experimental synergies). **No partial-information-decomposition literature in HEP.** |
| `ft "irreducible correlation" and ft "Dalitz"` | 3 | false positives |
| `ft "Dalitz plot" and ft "maximum entropy"` | **10** | RPP and large reviews only; **no method paper**. Maximum entropy in hadron physics means the Maximum Entropy Method for spectral-function inversion from lattice correlators — a *different* maxent problem (Bryan/MEM deconvolution), on a different object, and not on a Dalitz plot. |

**Reading.** The zero at `"Dalitz plot" ∧ "Shannon entropy"` is the load-bearing one. A field
that had ever computed an entropy of a Dalitz distribution would say "Shannon entropy" at
least once in a body paragraph somewhere in the indexed corpus. It does not.

---

## 3. THE ADJACENT FAMILIES — the four we were told to clear, cleared

For each: **is the quantity pairwise-blind in our sense (a maxent-over-pairs entropy gap)?**
The answer is **no** in every case, and the reason is structural rather than incidental: all
four are **two-sample** statistics comparing `P` to `P̄` (the CP conjugate), whereas ours is a
**one-sample** statistic computed on `P` alone, which is then differenced between `P` and `P̄`.
A two-sample test asks *are these two distributions different?* Ours asks *how much of this one
distribution is not reconstructible from its own pairs?* — a question that has a nonzero answer
even when `P = P̄` exactly.

### 3a. The Miranda method — Bediaga *et al.*

- **Bediaga, Bigi, Gomes, Guerrer, Miranda, dos Reis**, "On a CP anisotropy measurement in the
  Dalitz plot", **arXiv:0905.4233**, Phys. Rev. D **80** (2009), 142 citations.
- **Bediaga, Miranda, dos Reis, Bigi, Gomes, Otalora Goicochea**, "Second Generation of
  'Miranda Procedure'…", **arXiv:1205.3036**, Phys. Rev. D **86** (2012), 47 citations.

**The quantity.** Bin the Dalitz plane; in each bin `i` form the normalised difference between
the particle and antiparticle yields,
`S_CP(i) = (N_i − α N̄_i)/√(N_i + α² N̄_i)`, and read the set of `S_CP(i)` and their χ².
The 2009 abstract is explicit that this is "an observable inspired by astronomers' practice,
namely **the significance in the difference between corresponding Dalitz plot bins**."

**Pairwise-blind? NO.** It is a **binned two-sample residual map**. It is linear in each bin's
counts, computes no entropy, and constructs no maximum-entropy reference of any kind. It is
blind to nothing and sensitive to everything, including pure pair structure — indeed a CP
asymmetry confined entirely to one resonance band (pure pair structure in our language) is
exactly what Miranda is *designed* to find, and is exactly what our instrument is designed to
be blind to. **The two instruments are close to complementary.**

### 3b. The energy test — Williams; and LHCb's model-independent searches

- **Williams**, "Observing CP Violation in Many-Body Decays", **arXiv:1105.5338**,
  Phys. Rev. D **84** (2011), 65 citations.
- **Barter, Burr, Parkes**, "Calculating p-values and their significances with the Energy Test
  for large datasets", **arXiv:1801.05222** (2018) — the null-distribution scaling method.
- **LHCb**, "Measurements of CP violation in the three-body phase space of charmless B±
  decays", **arXiv:1408.5373**, Phys. Rev. D **90** 112004 (2014), 193 citations — the flagship
  application, and the paper whose Dalitz-position-resolved asymmetries are the physics
  benchmark for anything we do.
- Also LHCb **arXiv:1306.1246** (B± → K±π⁺π⁻, K±K⁺K⁻) and **arXiv:1310.4740**
  (B± → K⁺K⁻π±, π±π⁺π⁻); **arXiv:1310.7953** (D⁺ → π⁻π⁺π⁺).

**The quantity.** `T = Σ_{i<j∈P} ψ(d_ij)/n(n−1) + Σ_{i<j∈P̄} ψ(d_ij)/n̄(n̄−1) − Σ_{i∈P,j∈P̄}
ψ(d_ij)/(n n̄)`, with `ψ` a distance-weighting kernel (usually Gaussian) on the Dalitz metric.
An unbinned energy-statistic / maximum-mean-discrepancy two-sample test, with the null
distribution obtained by permutation.

**Pairwise-blind? NO.** It is an **unbinned two-sample test**, a kernel MMD in disguise. Nothing
about it is an entropy, and it constructs no marginal-constrained reference. Its null is
"`P` and `P̄` are the same distribution", which our instrument does not test.

### 3c. Earth mover / optimal transport

- **Davis, Menzo, Youssef, Zupan**, "Earth mover's distance as a measure of CP violation",
  **arXiv:2301.13211**, JHEP **06** (2023) 098, 15 citations. **Demonstrated on precisely our
  targets**: the Dalitz distributions of `B⁰ → K⁺π⁻π⁰` and `D⁰ → π⁺π⁻π⁰`.
- **Bogorad et al.**, "Generative models on phase space", arXiv:2604.02415 (2026) — Wasserstein
  distances on decay phase space, generative-model evaluation.

**The quantity.** The Wasserstein-1 distance between `P` and `P̄` and its optimal transport
plan, in windowed, binned and sliced variants. The paper's own abstract: "**a new unbinned two
sample test statistic** sensitive to CP violation utilizing the optimal transport plan".

**Pairwise-blind? NO.** A metric between two distributions. Its stated advantage over the energy
test is that the transport plan "retains information about the **localized** distributions of CP
asymmetry over the Dalitz plot" — i.e. it is *more* local, where ours is deliberately blind to
everything a pair marginal can express. Different axis entirely.

**This is the closest paper in the literature to our campaign** — same modes, same
model-independence motivation, same "borrow a statistic from another field" move, three years
old. It is the one that must be cited in our first sentence, not our last.

### 3d. Unbinned goodness-of-fit, kNN, and the general two-sample toolkit

- **Williams**, "How good are your fits? Unbinned multivariate goodness-of-fit tests in high
  energy physics", **arXiv:1006.3019**, JINST **5** (2010), 89 citations — surveys kNN,
  energy-test, point-to-point dissimilarity and local-density methods, **in the context of a
  real Dalitz-plot analysis**.
- **Rolke**, "Power Studies For Two-Sample and Goodness-of-Fit Methods For Multivariate Data",
  **arXiv:2605.12089** (2026) and arXiv:2507.16630 (2025) — large simulation power studies over
  the whole multivariate two-sample toolkit, including KL-based statistics, with 2D discrete
  data. Conclusion worth carrying: *"no single method can be relied upon to provide good power;
  any one method may be quite good for some combination of null hypothesis and alternative and
  may fail badly for another."*
- **Hou et al.**, arXiv:2504.17494 (2025) — ML-based goodness-of-fit in amplitude analysis.

**Pairwise-blind? NO**, all two-sample. But Rolke's conclusion is a warning aimed at us: adding
a fifth statistic to this shelf is only interesting if we can say **what class of alternative it
sees that the other four do not**, and that statement has to be pre-registered, not discovered.

### 3e. Adjacent-but-different, recorded so it is not rediscovered

- **Binning-scheme optimisation for the Dalitz plane** — **Bovill, Jurik, Malde**,
  arXiv:2606.13948 (2026), and the CLEO-c / BESIII equal-`Δδ_D` and "optimal" binnings. These
  are Dalitz-plane partitions optimised for sensitivity to `γ` and to charm mixing. They are
  the state of the art on *how to bin a Dalitz plot*, which is directly relevant to our binning
  ladder, and they are **not** information-theoretic — the figure of merit is the Fisher
  information for `γ`, not an entropy of the data.
- **Maximum Entropy Method (MEM)** in lattice/hadron physics — Bryan-style spectral
  deconvolution. Same two words, different problem, different object. Not prior art.
- **Zhou 2008 (arXiv:0803.2747)** — the quantum irreducible-correlation hierarchy. This is
  genuinely the same mathematical object, indexed in INSPIRE, with **no** decay or phase-space
  application. It is the strongest evidence that the object is *known* to physics and simply has
  never been pointed at a Dalitz plot.

---

## 4. THE CREDIT PARAGRAPH WE MUST CARRY

To be reproduced, in substance, in any results document, any Lean header, and any stance text
arising from this campaign:

> Model-independent CP-violation searches in three-body phase space are an established
> programme, and this measurement is a new instrument aimed at a well-worked target, not a new
> target. The binned significance map is the Miranda procedure of Bediaga, Bigi, Gomes,
> Guerrer, Miranda and dos Reis (arXiv:0905.4233, PRD 80 (2009); second generation
> arXiv:1205.3036, PRD 86 (2012)). The unbinned energy test is Williams (arXiv:1105.5338,
> PRD 84 (2011)), with the large-sample null calibration of Barter, Burr and Parkes
> (arXiv:1801.05222); its flagship application is LHCb, PRD 90 (2014) 112004
> (arXiv:1408.5373). Optimal-transport CP statistics on exactly these Dalitz distributions are
> Davis, Menzo, Youssef and Zupan (arXiv:2301.13211, JHEP 06 (2023) 098). The unbinned
> goodness-of-fit toolkit these sit in is surveyed by Williams (arXiv:1006.3019). The
> information measure we use is not ours: it is the connected information of Schneidman, Still,
> Berry and Bialek (PRL 91:238701, 2003) and the maximum-entropy hierarchy of Amari (IEEE TIT
> 47:1701, 2001), whose quantum counterpart is Zhou (arXiv:0803.2747). What is ours is the
> composition — pointing a maximum-entropy-over-pair-marginals entropy gap at a Dalitz
> distribution and at its CP conjugate — together with the pair-pinning certificate that says
> when such a reading is a measurement rather than a restatement of the pair marginals.

---

## 5. THE CORRECTION: T-ODD TRIPLE PRODUCTS ARE A FOUR-BODY OBSERVABLE

The mission brief states that T-odd triple products in three-body decays are already-measured CP
observables and are sign-triple moments — "our b=2 instrument in particle-physics clothes."
**This is wrong, and the error is elementary rather than subtle.**

**The physics.** A triple product is `C_T = p⃗₁ · (p⃗₂ × p⃗₃)`. In the rest frame of a decaying
spin-0 parent, momentum conservation gives `p⃗₁ + p⃗₂ + p⃗₃ = 0`, so the three momenta are
**coplanar**, and `C_T ≡ 0` identically, event by event, with no dynamics involved. A three-body
Dalitz plot is two-dimensional for exactly the same reason: after the constraints there are only
two independent kinematic variables, and no orientation degree of freedom survives to be odd
under time reversal.

**The literature agrees, and says so in its abstracts.** Bevan, "C, P, and CP asymmetry
observables based on triple product asymmetries" (arXiv:1408.3813, and 1506.04246) states that
"it is possible to construct twelve measurable triple product asymmetries for the decay of a
particle into a **four body final state**." Every published measurement is four-body or has a
spin vector supplying the fourth direction: LHCb's search (arXiv:1805.03941) is in
`Λ⁰_b → pK⁻π⁺π⁻`, `Λ⁰_b → pK⁻K⁺K⁻` and `Ξ⁰_b → pK⁻K⁻π⁺` — **`p h⁻h⁺h⁻`, four-body**.

**What this costs us, precisely.**

1. **We may not claim our instrument is a known observable in disguise.** There is no measured
   three-body T-odd triple product for it to be in disguise *of*. That sentence must not appear
   in the prereg or in any results document.
2. **`Core/FlavorBridge.lean` is unaffected**, and its header already says so with more care
   than the mission brief did: it states that the physics of T-odd triple products "is NOT
   formalized here", that in real decays a triple-product asymmetry is faked by final-state
   interactions, and that `cpState`'s `parityChar = σ₁σ₂σ₃` is a **model** three-bit parity
   character, not a momentum triple product. The Lean was already scoped correctly; the mission
   brief over-read it.
3. **Our three slots are not three momenta.** They will be three ±1 functions of the *2D Dalitz
   coordinate* (a binarisation, per `DALITZ_PREREG.md`). The sign triple `s₁s₂s₃` of those slots
   is a legitimate statistic, but it is a statistic of the **binned density on the plane**, not
   of the decay's momentum geometry, and it has no kinematic T-odd interpretation.
4. **The genuine T-odd analogy, if we want one, lives in four-body decays** — where the triple
   product is a real, coplanarity-evading observable and where the FSI-faking problem is exactly
   the one `FlavorBridge.lean`'s scope note describes. That is a **different campaign** and is
   recorded here as a lead, not opened.

---

## 6. WHAT WAS *NOT* SEARCHED — the limits of this adjudication

Stated so this document cannot be read as more than it is.

1. **No general-web or Google Scholar search.** The session's WebSearch budget (200 calls) was
   exhausted before this campaign started. Everything above is INSPIRE-HEP API. INSPIRE's
   fulltext index covers the arXiv HEP corpus well and the older journal-only literature less
   well; a pre-1990 or non-arXiv statistics paper applying a maxent gap to a two-dimensional
   physics histogram would **not** be found by this search.
2. **The statistics and neuroscience literatures were not swept for this application.** The
   measure's own provenance is settled (§1) and `novelty-check-spike-train-maxent` already
   governs the spike-train side. What is unswept is whether anyone in *statistics* has published
   "the maxent-over-2D-marginals entropy gap of a binned physical distribution" under a name we
   did not try.
3. **Nuclear physics and heavy-ion were not separately swept.** Heavy-ion has a large
   "three-particle correlations" literature; those are **cumulants and correlation functions**,
   not maxent gaps (and `sign-symmetry-kills-spin-models` plus `SignSymmetry.lean`'s own header
   record that a large three-point correlator is not order-3 structure). The distinction is
   sound, but the sweep was not run.
4. **Only the four families named in the mission were cleared exhaustively.** A fifth
   method family invented since 2024 and not using any of the searched phrases could exist.
   The recent-sorted sweeps in §3d/§3e are the mitigation, not a guarantee.

**Standing instruction for whoever runs the measurement:** if a WebSearch budget becomes
available, the two highest-value queries are `"Dalitz plot" "maximum entropy" CP violation` on
the open web (to catch conference proceedings INSPIRE has not fulltext-indexed) and a Google
Scholar sweep of citations *to* Schneidman 2003 filtered for particle physics. Neither was
possible here, and until they are run this document's verdict is **CONVERGENT-ADJACENT with an
unswept web**, not CLEAR.

---

## 7. SCORECARD

| family | representative | quantity | pairwise-blind in our sense? | verdict |
|---|---|---|---|---|
| Miranda | Bediaga *et al.* 0905.4233, 1205.3036 | binned two-sample significance map | **no** — linear in bin counts, no entropy, no maxent reference | CONVERGENT-ADJACENT, credit required |
| Energy test | Williams 1105.5338; Barter 1801.05222; LHCb 1408.5373 | unbinned kernel two-sample (MMD-class) | **no** — two-sample, no entropy | CONVERGENT-ADJACENT, credit required |
| Optimal transport | Davis, Menzo, Youssef, Zupan 2301.13211 | Wasserstein-1 + transport plan, two-sample | **no** — a metric between `P` and `P̄` | CONVERGENT-ADJACENT, **closest work**, credit required |
| Unbinned GoF / kNN | Williams 1006.3019; Rolke 2605.12089 | kNN, point-to-point dissimilarity, KL-based two-sample | **no** — two-sample | CONVERGENT-ADJACENT, credit required |
| Dalitz binning optimisation | Bovill, Jurik, Malde 2606.13948; CLEO-c/BESIII | Fisher-information-optimal partitions | n/a — not a CP statistic | relevant to our binning ladder, not prior art on the measure |
| MEM (lattice) | Bryan-style spectral inversion | maxent deconvolution of a spectral function | **no** — different object, different problem | not prior art |
| Irreducible correlation | Zhou 0803.2747 | **our object**, quantum version | **yes** — same hierarchy | same measure, **no phase-space application**; credit as the measure's quantum counterpart |
| **This campaign** | — | maxent-over-pair-marginals entropy gap on the Dalitz plane, and its CP difference | **yes** | **no prior art found in the indexed HEP corpus** |

---

## FILES

| | |
|---|---|
| this document | prior-art adjudication, written before any measurement |
| `DALITZ_DATA.md` | public-data inventory (next) |
| `DALITZ_PREREG.md` | pre-registration (after the inventory, before any number) |

Search performed 2026-07-26 against the INSPIRE-HEP REST API. Query strings and hit counts are
reproduced verbatim in §2 so the sweep can be re-run and disagreed with.
