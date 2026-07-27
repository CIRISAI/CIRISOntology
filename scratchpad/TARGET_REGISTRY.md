# TARGET REGISTRY — where to point the whole-only instrument next

**Scratchpad only.** No Lean file was opened for editing, `Stance.lean` is untouched, the audit
was not run, `lake` was never invoked. Nothing here is proposed for the published page. This is a
survey and an adjudication, not a measurement.

**The question.** Across three scales — micro/SM, macro, cosmology — where should the
pairwise-blind order-3 instrument (`share` / `I_C^(3)`, `Core/Share.lean`) go next, ranked by
expected yield and scored honestly for prior art?

**The house standard applied throughout** (`convergent-art-pattern`): *assume the result is
already in print until the primary text says otherwise; search by the mathematical object, never
by our vocabulary.* Two of the searches below came back with the result already in print, under
names this repository had not been searching. Both are recorded in §3 before any ranking, because
finding them now is the whole point of writing this document before a campaign rather than after.

---

## 0. WHAT THE INSTRUMENT IS, AND THE THREE FACTS THAT DECIDE EVERY ROW

The quantity is the **connected information of order 3** (Schneidman, Still, Berry & Bialek, PRL
**91**:238701 (2003)): given a joint distribution `P` on three discrete slots, form the
maximum-entropy distribution `Q` carrying all three pair marginals of `P` exactly, and read
`share = S(Q) − S(P)`. It is zero exactly when `P` is reconstructible from its own pairs. On
`k = 3` binary slots the exact solver is one-dimensional (the fibre is the line `p + δ·χ` along
the parity character), and it is already written: `scratchpad/dalitz_share.py::share_2x2x2`.

Three properties of this instrument decide most of the rankings below, and they are stated first
so that no row has to re-argue them.

### FACT 1 — the sign-symmetry theorem (machine-checked; `Core/SignSymmetry.lean`)

`share_eq_zero_of_signSymmetric`: a three-bit state invariant under the global flip `p(s) = p(−s)`
has whole-only share **exactly zero**, with no hypothesis on the pair correlations, the
temperature, or the coupling. **Do not send anyone to measure zero.** This removes the whole
zero-field spin family (Ising, transverse-field Ising, kinetic Ising, Z₂-symmetric maxent models
of neural criticality) and it removes any target whose binary labels come from a symmetric
continuous field split at its own median — which, read the other way, is the source of our best
*nulls*.

### FACT 2 — the valve (machine-checked; `Core/Valve.lean`) and its measured floor

`valve_from_nothing` — a product state through any per-cell channel stays a product state, share
exactly zero. `valve_needs_asymmetry` — a **flip-covariant** kernel carries sign-symmetric states
to sign-symmetric states, so it mints exactly nothing at any noise strength. But an **asymmetric**
per-cell channel mints share out of pair structure, and the sky campaign measured how much: at
`R = 10, b = 8`, Poisson resampling alone multiplied the null by **5.8×**
(`SKY_REALDATA_RESULTS.md` §2). **Counting noise is asymmetric; additive symmetric noise is not.**
Any target whose pipeline turns a field into *counts* inherits a large, unavoidable minting floor.
Any target whose noise is additive and symmetric inherits **none**. This single distinction is
worth more than any other criterion in the ranking below.

### FACT 3 — the b=2 share is a **copula** statistic, and that cuts both ways

The median-split share is exactly invariant under any strictly monotone pointwise map applied
slot-wise (`share-is-not-negentropy`, `binning-and-filter-traps`; Sklar 1959, and Scherrer et al.
ApJL **708**:L9 (2010) state it for LSS). Re-verified here as a calibration, exact solver,
N = 8 × 10⁶ triples, correlated trivariate Gaussian `ρ = (0.60, 0.35, 0.60)`, field
`δ = g + a(g² − 1)`:

| `a` | one-point skewness | share (nats) |
|---|---|---|
| 0 | +0.001 | 7.708e−08 |
| 0.003 | +0.019 | 7.708e−08 |
| 0.01 | +0.061 | 7.708e−08 |
| 0.03 | +0.181 | 7.708e−08 |
| 0.1 | +0.591 | 7.708e−08 |
| 0.3 | +1.573 | 2.018e−06 |

The reading is **bit-for-bit identical** until `a = 0.3`, which is exactly where
`g ↦ g + a(g²−1)` stops being monotone on the sampled range (turning point at `g = −1/2a`). A
skewness of +0.59 moves the instrument by **nothing at all**.

* **The strength.** Immunity to gain, calibration, arbitrary units, and any one-point
  transformation of the observable. The Lyman-α flux transform `F = e^{−τ}`, the log-density
  transform in LSS, the choice of normalisation for a glass order parameter — all free.
* **The blindness.** Any non-Gaussianity that is a *pointwise function of a Gaussian field* is
  invisible. A target whose only known departure from Gaussianity is of that form is a target
  where we will read the floor.
* **The trap.** A linear filter applied **after** a pointwise map manufactures share from nothing
  — measured at **66 σ** in the sky pilot with zero real signal. Every window, beam, mass
  assignment, aperture, spectrograph LSF and selection function is such a filter.

### The floor, measured

Finite-sample floor of the exact solver on a theorem-pinned zero (Gaussian triples, median split),
120 draws each, this session:

| N triples | median share | mean | p99 | `1/(2N)` |
|---|---|---|---|---|
| 1e5 | 1.86e−06 | 4.62e−06 | 3.20e−05 | 5.00e−06 |
| 1e6 | 2.73e−07 | 5.83e−07 | 3.99e−06 | 5.00e−07 |

Two things to carry into every cost estimate below. **The floor scales as `1/(2N)`** — one
degree of freedom, the parity direction — so a target's sensitivity is set by its count of
*independent* triples and nothing else. And **the null is χ²₁-shaped**: mean ≈ 2 × median,
p99 ≈ 14 × median. Quote p-values, never `z` from a median and a sigma
(`share-null-is-chi2-shaped`, and the Dalitz D7 near-miss that would have fired a kill on one
draw).

---

## 1. KILLED BEFORE RANKING — removed, with the reason

These are not ranked low. They are **out**, and each one is out for a reason that can be checked
without spending a day.

| candidate | why it is out |
|---|---|
| **Zero-field Ising / transverse-field Ising / kinetic Ising / Z₂-symmetric neural maxent** | **FACT 1.** Share is *exactly zero* at every temperature including `T_c`. Already in `Core/SignSymmetry.lean` and in `SPIKE_SURVEY.md`. Published "higher-order structure peaks at criticality" results are peaks in O-information, PID synergy, Φ, TSE complexity or specific heat — every one of which is nonzero on purely pairwise systems (Caprioglio, Mediano & Berthouze, PRL **136** (2026), arXiv:2505.24686). |
| **Vicsek / polar flocking in the disordered phase** | **FACT 1** again on the binarised heading component; and in the *ordered* phase, Bialek, Cavagna, Giardina et al. (PNAS **109**:4786 (2012)) already showed a **pairwise** maxent model reproduces natural starling flocks. The field's own answer is "pairs suffice." |
| **The PDG tension list as such** — muon g−2, W mass, `V_us`/Cabibbo, neutron lifetime (beam vs bottle), `R(K)`, `R(D*)` | **Not distributions.** Every one of these is a *fitted scalar with an error bar*. There is no joint distribution over three slots to read. The brief asked which of these are distributions we can read; the honest answer is **none of them**. This is a finding, not an omission. |
| **B → K\*μμ angular anomaly (`P₅′`)** | The angular distribution is a **complete finite basis** — twelve coefficients `J_i` including genuine three-way angular terms. There is no hidden sector for a maxent gap to find: our number would be a nonlinear function of quantities the field already measures completely. And only the fitted `J_i` are public, not the event-level angles. |
| **Nuclear β-decay correlation coefficients (`a`, `b`, `A`, `B`, `D`, `R`)** | Moments of a distribution, published as moments. Same structural problem as above, with worse statistics. |
| **Lyman-α forest 1D flux field** | **FACT 3's trap in its purest form.** `F = e^{−τ}` is a pointwise map (so the primary non-Gaussianity is *invisible* to us), and the spectrograph line-spread function is a linear filter applied **after** it (so it *manufactures* share). The one mechanism that could give a signal and the one mechanism that fakes one are the same mechanism, applied in that order. Do not go. |
| **ECA noise-enhancement (`SPIKE_SURVEY.md`'s single recommended reproduction)** | Already run, already adjudicated: the spike survives an iid null and **collapses 1886× under a mixture null**, the rules peak at fixed noise *dose* not rate, and Schneidman 2003's own Fig. 2 had already swept noise and found order-3 creation (`ECA_SPIKE_RESULTS.md`, `eca-spike-is-convergent-art`). Closed. |

---

## 2. THE RANKED TABLE

Scores are **A** (best) / **B** / **C** / **D**, with **F** disqualifying. Legend:

* **(a) blind shape** — is the open problem literally about structure invisible to pair
  correlations? A = the field says so itself.
* **(b) baseline** — is the two-point structure known well enough that a residual means something?
* **(c) theorem** — does FACT 1 kill it, or FACT 2 drown it? A = no kill and no minting floor.
* **(d) data** — public, a distribution/field (not fitted parameters), reachable *from this
  machine*.
* **(e) prior art** — A = clear, D = our quantity already measured there.
* **(f) cost** — A = days on this box, D = infeasible here.

| # | scale | candidate | a | b | c | d | e | f | verdict |
|---|---|---|---|---|---|---|---|---|---|
| **1** | MACRO | **Glass transition / amorphous order** — is there static order invisible to `g(r)`? | **A** | **A** | **A** | **A** | **C** | **B** | **THE CAMPAIGN.** The field's own framing is our niche verbatim; data is 6 GB on Zenodo; no counting noise; sign symmetry does not apply. Prior art is adjacent and must be credited (§3.1). |
| **2** | COSMO | **Planck SMICA + WMAP ILC as a theorem-pinned plumb line** | C | **A** | **A** | **A** | **A** | **A** | **THE PILOT.** Weak as a discovery target (§4.2) but unbeatable as a *plumb line*: the null is a theorem, the data is already on this disk, and the noise is the one kind that provably mints nothing. Fills four NONE-YET cells in `GATES.md`. |
| **3** | MICRO | **Multi-time quantum process tensor (3-time memory) on a QPU** | **A** | B | **A** | B | B | B | Strong. The field states pairwise-blindness itself ("two-time pictures are insufficient… memory is inherently a multi-time phenomenon"). We already run IBM hardware. Data must be *made*, not found. |
| **4** | MACRO | **Turbulence — JHTDB velocity/dissipation fields** | C | **A** | B | **A** | B | B | Best available **calibration** target: two-point structure known to textbook precision, DNS has no measurement noise, 100 TB public and the host is reachable. Weak as a mystery — nobody thinks turbulence is pair-reconstructible. |
| **5** | COSMO | **eBOSS DR16 LSS (LRG / ELG / QSO) as the substitute confirmation for the wounded BOSS reading** | B | **A** | C | **B** | B | **B** | **The standing open claim's only reachable instrument.** DESI is network-blocked (`SKY_BGS_STAGE0.md`, re-verified today: `data.desi.lbl.gov` still unroutable). eBOSS DR16 data **and randoms** ARE reachable at `data.sdss.org`. One Stage-0 blocker: mocks (§4.5). |
| 6 | MACRO | Neural population data (Allen, IBL, retina) | **A** | B | B | B | **D** | B | **Scooped.** Ohiorhenuan & Victor, *Nature* **466**:617 (2010) measured the order-3 maxent gap in macaque V1 and found it nonzero and systematic; the 2021 follow-up separates executive from sensory areas. Plus our own fMRI and LLM nulls (`adequacy-fmri-fourth-substrate`, `llm-synergy-effect-size`). Do not lead with this. |
| 7 | MACRO | Protein folding trajectories (DE Shaw / Folding@home) | B | C | B | C | **D** | C | **Scooped.** The Mutual Information Expansion (Killian, Kravitz & Gilson, JCP **127**:024107 (2007)) computes exactly the third-order terms of the configurational-entropy expansion, routinely. Access is request-gated for the Anton trajectories. |
| 8 | COSMO | Weak-lensing convergence maps (DES Y3 / KiDS-1000) | B | **A** | C | B | **D** | C | **The most crowded target in the survey.** "Beyond two-point" is an entire subfield with its own name: peak counts, convergence PDF, Minkowski functionals, scattering transforms, wavelet phase harmonics, field-level inference. We would be the twentieth instrument. |
| 9 | MICRO | Jet substructure / energy correlators (CMS, ATLAS open data) | C | B | B | C | **D** | **D** | The field measures **projected N-point energy correlators directly** — it is already computing three-point structure by name. And the data is CMSSW-format at TB scale. |
| 10 | MICRO | Four-body / T-odd decays from LHCb stripping streams | B | B | B | **D** | B | **D** | **Cost-killed, quantified.** The CHARM 2011 MagDown stream alone is **1.87 TB / 154 M events in MDST format** (opendata.cern.ch rec. 28014), requiring the LHCb VM and DaVinci. The 3-body derived ntuple we already used (rec. 4900) is 1.11 GB — that ratio is the whole story. |
| 11 | MICRO | Short-baseline neutrino anomalies (MicroBooNE public data) | C | C | B | C | B | B | Low dimensionality, low statistics; the anomaly is a normalisation excess, not a structure claim. |
| 12 | COSMO | CMB anomalies — hemispherical asymmetry, low-ℓ alignments, Cold Spot, lensing anomaly | **D** | **A** | **A** | **A** | B | **A** | **Instrument mismatch, stated plainly.** These are claims about *statistical isotropy*, not about non-reconstructibility from pairs. A hemispherical power asymmetry is a statement about the two-point function varying across the sky. Our instrument does not address it. (The Cold Spot is a one-point excursion.) |

---

## 3. THE TWO CONVERGENT-ART FINDINGS THAT MATTER

Both were found by searching the mathematical object into fields this repository had not
searched. Both change how the top candidate must be written up.

### 3.1 Liquid-state theory has been computing "the entropy the pairs do not explain" since 1952

The object is called the **multiparticle correlation expansion of the entropy** (Green 1952;
Nettleton & Green 1958), made computable by **Baranyai & Evans, *Phys. Rev. A* **40**, 3817
(1989)**, "Direct entropy calculation from computer simulation of liquids": the excess entropy is
expanded `s_ex = s_2 + s_3 + …`, with `s_2` the two-body term built from `g(r)`. The remainder,

> **Residual Multiparticle Entropy** `Δs = s_ex − s_2` (Giaquinta & Giunta, *Physica A* **187**:145
> (1992)),

is described in the literature in words that could have been lifted from this repository: *"the
net contribution to entropy due to spatial correlations involving three, four, or more
particles."* And it has a famous **sign change as a function of a control parameter** — the
**zero-RMPE criterion**: `Δs` crosses from negative to positive at a packing fraction that
overlaps the hard-sphere freezing threshold, and is read as a signature of emergent local
structural organisation. (Contested in generality: Krekelberg et al., JCP **128**:161101 (2008),
"Residual multiparticle entropy does not generally change sign near freezing", with a Giaquinta
comment at JCP **130**:037101 (2009); the criterion holds in d = 2, 3 and fails in other
dimensions.)

**Is it our quantity? No — and the difference is exact and checkable.** `s_2` is a *truncation of
an infinite series*, not the entropy of the pair-maxent distribution. The decisive tell: **RMPE
goes negative**, and our share **cannot** — `share = S(Q) − S(P)` where `Q` maximises entropy over
a set containing `P`, so `share ≥ 0` always. They are different objects that answer the same
physical question. Verdict: **CONVERGENT-ADJACENT**, exactly as the Dalitz campaign was. The
credit paragraph is mandatory on anything we publish about liquids or glasses.

**And a correction owed to `SPIKE_SURVEY.md`.** That survey's §"WHAT I DID NOT FIND" states: *"No
published measurement of `I_C^(k≥3)` as a function of a swept control parameter, in any field."*
That bullet was written after searching neuroscience, quantum information and complexity science.
It is **too strong**: liquid-state theory has been sweeping density and temperature against a
non-pair entropy remainder for thirty years. The survey's core adjudication (nobody has swept a
*pairwise-blind, non-negative maxent gap*) survives; its reach did not extend to condensed matter,
and it said so in its own caveat. Recorded here rather than left to be discovered later.

**Two more credits in the same neighbourhood, both sharper than ours on framing:**

* **Torquato & Stillinger** — the **`g₂`-invariant process** construction: explicitly different
  point processes sharing an identical pair correlation function. That is *our niche stated as a
  theorem, in 2003, by somebody else* ("Local density fluctuations, hyperuniformity, and order
  metrics", PRE **68**:041113). Any glass write-up must cite it.
* **M. S. Shell**, "The relative entropy is fundamental to multiscale and inverse thermodynamic
  problems", JCP **129**:144108 (2008), and the coarse-graining literature built on it. By the
  Pythagorean identity for exponential families, `min_q D(p‖q)` over the pair-potential family
  **equals** `S(Q) − S(p)` where `Q` carries `p`'s pair correlations — i.e. **it is exactly our
  share**, computed routinely, under the name `S_rel`, as a coarse-graining objective. What has
  *not* been done, as far as this survey reaches, is to trace it across the glass transition as a
  physical observable rather than as a fitting loss. That gap is the campaign.

### 3.2 The order-3 maxent gap in cortex was measured in *Nature* in 2010

**Ohiorhenuan, Mechler, Purpura, Schmid, Hu & Victor**, "Sparse coding and high-order correlations
in fine-scale cortical networks", *Nature* **466**:617 (2010): pairwise maxent fails in macaque V1
and the deviations are highly systematic; local networks show interactions beyond pairs while
distant neurons do not. Follow-ups extend it (Shimazaki et al.; and the 2021 result that
high-order interactions explain collective behaviour in executive but not sensory areas). Combined
with the retina's opposite answer (Schneidman et al. 2006: pairwise suffices), **neural population
data is the one macro substrate where our headline question has a published answer.** Rank 6, and
never the lead.

---

## 4. THE TOP FIVE — the concrete first experiment for each

### 4.1 GLASS TRANSITION AND AMORPHOUS ORDER — rank 1, the campaign

**Why this and not the others.** The field states our niche as its own open problem, in its own
words: the pair correlation function `g(r)` of a glass is essentially indistinguishable from that
of the liquid, while the system is mechanically a solid. The hunt for the missing structure has a
name ("amorphous order"), a dedicated observable (point-to-set correlations — Biroli, Bouchaud,
Cavagna, Grigera & Verrocchio, *Nat. Phys.* **4**:771 (2008)), a competing dynamical observable
(`χ₄`), and an entire machine-learning programme ("softness", GNNs — Bapst et al., *Nat. Phys.*
**16**:448 (2020)). **Nobody has asked the question in the form we ask it:** how much of the
configuration's entropy is not reconstructible from all of its pair marginals?

**Data.** `GlassBench`, Zenodo **10.5281/zenodo.10118191**, **6.04 GB**, CC-BY-4.0, single
`GlassBench.zip` — 2D and 3D glass formers, configurations across temperature, with the ML
benchmarks from *Roadmap on machine learning glassy liquids* (Nat. Rev. Phys., arXiv:2311.14752).
Zenodo is reachable from this box (HTTP 200). Secondary: DeepMind `glassy_dynamics` (Kob–Andersen
binary LJ, 4096 particles, `gs://deepmind-research-glassy-dynamics`, ~100 GB total, subsets
downloadable).

**Slots and estimator.** Three particles at a fixed geometric template (equilateral triangle of
side `r`, with a pre-registered tolerance), each carrying **one** binary label = its own local
order parameter split at the configuration-wide median. Pre-register the label choice — candidates
are Voronoi volume, `q₆` (3D) / `ψ₆` (2D), or the published softness field. **FACT 3 makes the
normalisation of the label irrelevant**, which removes the single largest arbitrary choice in the
design. Estimator: `share_2x2x2`, exact, no IPF anywhere (`ipf-sharek-boundary-drift`).

**The theorem-pinned control.** Two, and they are different.
1. **Product control** — randomise the labels independently across particles. `valve_from_nothing`:
   share exactly zero. Catches the estimator floor.
2. **The pair-matched generative null, which is the real gate** — a configuration ensemble that
   reproduces the observed `g(r)` *and nothing else*. This already exists as standard software:
   **Reverse Monte Carlo** (McGreevy & Pusztai, *Mol. Simul.* **1**:359 (1988)), whose documented
   property — it returns the most disordered structure consistent with the pair data — **is** the
   maxent-given-pairs statement. Equivalently, iterative Boltzmann inversion to a pair potential.
   The reading is the difference between the real ensemble and this one, and nothing else.

**The dominant floor.** Not shot noise — there is none, the configurations are exact particle
coordinates. It is `1/(2N)` estimator bias in the count of independent triples (use *independent
configurations* as the independent axis, never time-pooling: `order3-probe-geometry`,
`whole-only-null-autocorrelation`), plus one hazard specific to this design: **template-selection
minting.** Selecting triples by a geometric template is a selection *on the configuration*, and
selection is a filter. Gauge it by applying the byte-identical template selection to the RMC
surrogate — never by argument.

**The kill, staked first and separable.** *If, at every template scale `r` on the pre-registered
grid and at the lowest temperature in the set, the share fails to exceed the RMC/pair-matched
surrogate's share by more than the surrogate's own 5σ, then "amorphous order carries whole-only
structure invisible to `g(r)`" is refuted at a sensitivity we measured rather than assumed.* That
kill takes down that claim and nothing beneath it — in particular it does not touch the sky
campaign, the rent clause, or the valve.

**Cost.** Download 6 GB. The estimator is 8-cell contingency tables — free. The RMC null is the
expense: hours to a day of CPU per state point with standard code. Dominant gates: **3
(mixture/manufacture)** — the RMC null *is* the gate — and **5 (coarse-graining)**, swept over `b`
and the template tolerance.

**Named residual prior-art risk, stated so it can be discharged cheaply on day one:** search
`copula` + `glass` / `supercooled` / `amorphous` first (per `share-is-not-negentropy`), and search
`S_rel` / `relative entropy coarse-graining` + `supercooled` before writing a line of analysis. If
somebody has traced Shell's `S_rel` across `T_g`, we are reproducing, not discovering, and the
write-up must say so from the first sentence.

---

### 4.2 PLANCK SMICA / WMAP ILC — rank 2, the cheap pilot, and NOT a discovery target

**The inventory, done, since the brief asked for it.**

| file | bytes | what it is |
|---|---|---|
| `/home/emoore/coherence-ratchet/experiments/cmb_books/data/smica_2048.fits` | 2 013 312 960 | Planck **COM_CMB_IQU-smica_2048_R3.00_full**, HEALPix **NESTED**, **NSIDE = 2048** (50 331 648 pixels), **GALACTIC**, units **K_CMB**, created 2018-04-10 |
| `/home/emoore/coherence-ratchet/experiments/open_system_pomega/cmb_data/planck_smica_R3.fits` | 2 013 312 960 | **the same file** — verified byte-identical over the first 20 MB (md5 `2bb32f8b…`), same headers, same column set |
| `/home/emoore/coherence-ratchet/experiments/open_system_pomega/cmb_data/wmap_ilc_9yr_v5.fits` | 25 174 080 | WMAP 9-yr **ILC**, DR5/PASS 5, `RESOLUTN = 9` (NSIDE 512, 3 145 728 pixels), K–W bands combined, intensity |
| `…/cmb_books/data/planck_bestfit_theory.txt` | 205 647 | Planck best-fit theory `C_ℓ` — the input for the theorem-pinned null |

**Masks are present in the file** — this is the part worth knowing before planning anything. HDU 1
carries ten columns: `I_STOKES, Q_STOKES, U_STOKES, TMASK, PMASK, I_STOKES_INP, Q_STOKES_INP,
U_STOKES_INP, TMASKINP, PMASKINP`. `TMASK` is binary `{0,1}` with **f_sky = 0.8424** (42.4 M
unmasked pixels); the `_INP` columns are the inpainted maps with their own masks. HDU 2 carries the
effective beam transfer function, `INT_BEAM` and `POL_BEAM`, `ℓ = 0…4096`. Map statistics:
`I_STOKES` mean −9.4e−13 K, sd 1.084e−04 K, range [−5.755e−03, +7.899e−03]. `healpy 1.19.0` is
installed.

**Why it is not a discovery target — the adjudication, plainly.**

1. **The share is quadratic where the field's estimator is linear.** For a weakly non-Gaussian
   field the entropy gap is second order in the three-point amplitude; the KSW bispectrum estimator
   is first order in `f_NL`. Planck has already reached `σ(f_NL^local) ≈ 5`. A quadratic statistic
   cannot compete with a matched filter on the same data. We will not improve an `f_NL` bound.
2. **FACT 3 removes the naive local model outright.** `Φ = φ + f_NL(φ² − ⟨φ²⟩)` is a *pointwise*
   map; a pointwise map contributes **exactly zero** to the b=2 share (table in §0, and the
   invariance is a theorem). What survives is only what the radiation transfer function — a linear
   filter applied *after* the pointwise map — converts into genuine multi-point copula structure.
   That is a suppressed residual of an already-tiny signal.
3. **The convergent-art risk is real and dominant.** Minkowski functionals (Novaes et al.,
   CQG **34**:094002 (2017), model-independent on Planck maps), the binned/modal bispectrum,
   needlets, wavelets and phase statistics are the standing model-independent programme. INSPIRE
   fulltext confirms our *object* is unnamed there — `ft "cosmic microwave background" and
   ft "connected information"` returns **4 hits, all false positives** (checked: "Dissipative
   effects in the Early Universe", a six-dimensional inflation search, a weak-lensing NG paper, an
   ML textbook); `ft "multi-information" and ft "CMB"` returns **2, both false positives**;
   `…"maximum entropy" and "pair marginals"` returns **0**. Unnamed is not unmeasured, and here the
   substantive quantity has been squeezed harder by better estimators.

**Why it is nonetheless the right pilot, and worth a week.** The CMB is the only real-data field
this programme can reach where **the null is a theorem rather than a simulation**:

* A Gaussian field split at its own median is sign-symmetric, so `share_eq_zero_of_signSymmetric`
  gives share **exactly zero** — verified numerically above: 2.42e−07 at N = 1e6, 1.66e−08 at
  N = 1e7, tracking `1/(2N)` and nothing else.
* **The instrumental noise is the one kind that provably mints nothing.** Additive symmetric noise
  keeps the joint distribution sign-symmetric, so `valve_needs_asymmetry` applies: the minting
  floor is **exactly zero**, not "small". Contrast the sky campaign, where Poisson counting noise
  alone multiplied the null by 5.8× and had to be measured before anything could be cashed. **This
  is the only field-scale target in the registry with no valve floor at all.**
* And it is a *real* instrument: a real mask (`f_sky = 0.8424`), a real beam, real anisotropic
  noise, real foreground residuals — none of which a simulation exercises honestly.

**The pilot, concretely.** Slots: three pixels at a fixed angular template (equilateral triangle,
side `θ`, swept), labels = the smoothed field split at the median over the unmasked sky. Null: a
Gaussian realisation of `planck_bestfit_theory.txt`, beamed with HDU 2's `INT_BEAM`, masked with
`TMASK`, put through the **byte-identical** pipeline. Independent triples at NSIDE 2048 with
`f_sky = 0.84`: ~1.4e7 per template, giving a floor of ~3.6e−08 nats. Cross-instrument replicate on
WMAP ILC at NSIDE 512. Dye test: inject a known filtered-quadratic NG and verify it is seen at the
amplitude where it should be.

**What the pilot is for, and its kill.** It is a **plumb line**, not a claim about the sky. Per
`GATES.md`, four reaches currently read **NONE-YET** in the plumb-line row — boundary/static
nonlinearity (2), coarse-graining (5), geometric artifact (6), probe polarity (8) — and gate 1's
one true plumb line is "held live; not pinned as a fixed regression case." A certified reading on
the real masked Planck map, where the correct answer is *proved* zero, pins all of them at once.
The kill is on the instrument: **if the theorem-pinned null does not read inside its predicted
`1/(2N)` band on the real masked map, the pipeline is fouled and every subsequent field reading it
produces is ungauged.**

---

### 4.3 MULTI-TIME QUANTUM PROCESS TENSOR — rank 3

**Why.** The one candidate outside glass where the field states pairwise-blindness in its own
voice: *"two-time pictures are insufficient to describe the full temporal structure of open
quantum dynamics; memory is inherently a multi-time phenomenon."* The process-tensor framework
(Pollock, Rodríguez-Rosario, Frauenheim, Paternostro & Modi) exists precisely because two-time
correlation functions cannot capture multi-time memory. That is criterion (a) at grade A.

**Data must be made, not found.** Full three-time process tomography on a superconducting qubit is
published and was done partly on IBM Quantum hardware (arXiv:2308.00750), so the protocol is on
the record and we have run this hardware before (`Core/Valve.lean`'s hardware paragraph; job
`d9in8jrjf64c739fprqg`, 100 QPU seconds). Prior art is **adjacent, not identical**: our earlier
adjudication found White et al. to be a **witness plus a bipartite bound**, not a measurement of
the three-time whole-only share (`temporal-whole-only-campaign`).

**First experiment.** Three measurement times on one qubit under idling, outcomes binarised,
`share_2x2x2` on the three-time outcome distribution. Theorem-pinned control: a **Markovian**
process — the three-time outcome statistics factorise through the intermediate, so the share sits
at the floor. Second control, and this is the one that decides it: `valve_needs_asymmetry` says
amplitude damping (flip-breaking) mints while a binary symmetric channel does not, so **a
Markovian amplitude-damping process is a known-nonzero positive control that is not memory** — it
must be measured and subtracted before any reading is called non-Markovian. Dominant floor: shot
noise at the QPU's shot count, and the screening rule from `qpu-published-calibration-unusable`
(screen qubits by measured `P(0|1)` first, ~6 s; never trust `backend.properties()`).

**Kill.** If the three-time share does not exceed the Markovian-plus-damping control by 5σ on any
screened qubit, genuine three-time whole-only memory is refuted on this hardware at the sensitivity
measured.

---

### 4.4 TURBULENCE (JHTDB) — rank 4, the honest calibration target

**Why, and why not higher.** Two-point structure is known to textbook precision (Kolmogorov;
the exact 4/5 law), DNS has **no measurement noise at all**, and the data is public, huge and —
verified today — the host is **reachable** (`turbulence.pha.jhu.edu` → `turbulence.idies.jhu.edu`,
HTTP 200): isotropic DNS at 4096³/8192³/32768³, channel flow, MHD, boundary layers, 100 TB scale,
with REST/HDF5 cutout services, `pyJHTDB`, and SciServer.

But criterion (a) is only a C: **nobody believes turbulence is pair-reconstructible**. A positive
reading confirms what everyone assumes. That makes it a poor mystery and an excellent **ruler** —
and this programme has been burned specifically for not gauging its ruler first
(`forward-prediction-confirmed`: *gauge a ruler with planted values before staking a band*).

**One correction to the obvious argument, made here so it is not made later in error.** It is
tempting to say the 4/5 law *guarantees* nonzero order-3 share. It does not. `⟨δu³⟩` is a
**moment**, and FACT 3 says a field that is a pointwise monotone map of a Gaussian field has share
exactly zero however skewed it is. Turbulence's non-Gaussianity is almost certainly not of that
form — but "almost certainly" is the honest word, and the experiment is worth running for exactly
that reason.

**First experiment.** Three velocity components (or dissipation values) at three points on a
pre-registered lag template, median-split, `share_2x2x2`, swept across the inertial range. Control:
a Gaussian random field with the *identical* measured spectrum, put through the identical cutout,
interpolation and binarisation — this is the sharpest available test of whether the share tracks
the cascade or the interpolation kernel. Dominant floor: the trap of FACT 3 — **JHTDB's spatial
interpolation is a linear filter**, and if any pointwise operation precedes it, share is
manufactured. Scan the **full lag-pair grid**, never the equally-spaced diagonal
(`order3-probe-geometry`).

---

### 4.5 eBOSS DR16 — rank 5, and the only reachable instrument for the standing open claim

**The situation.** The published stance carries one `open` claim — which of nature's wild processes
carry whole-only share — and names **DESI BGS at 10–100× the density** as the next instrument.
That instrument is **unreachable from this machine**: `SKY_BGS_STAGE0.md` diagnosed the whole
`128.55.206.0/24` Spin block as unroutable, and it is still unroutable today (curl returns no HTTP
code at all, while `data.sdss.org`, `zenodo.org`, `opendata.cern.ch`, `hepdata.net`,
`turbulence.pha.jhu.edu`, `pla.esac.esa.int` and `lambda.gsfc.nasa.gov` all return 200).

**What IS reachable, checked today.** `https://data.sdss.org/sas/dr16/eboss/lss/catalogs/DR16/`
returns 200 and lists clustering **data and randoms** for **LRG, LRGpCMASS, ELG and QSO**, NGC and
SGC, plus the ELG and LRG/QSO masks and the full footprint geometry. Randoms are the selection
function, and their absence is what killed the Astro Data Lab route to DESI. **eBOSS DR16 gives
independent tracers over a partially independent volume, with randoms, today.**

**The one Stage-0 blocker, named rather than glossed.** The EZmock suite is **not** at the obvious
SAS paths (three probed, all 404). The BOSS run took its covariance *and* its forward model from
the Patchy mocks; without an eBOSS mock suite there is no covariance and no prediction, and per
`GATES.md` the harvest gate **"gate discharge before unblind"** forbids unblinding with an
undischarged gate. **Stage 0 for this target is: locate the eBOSS EZmocks, or declare the target
blocked.** Do not start Stage 1 first.

**And the prior on the reading is not neutral.** The BOSS DR12 result scored its criterion MET and
was then **wounded by our own pre-registered refuter** — corrected to 6.0/9.7σ at the primary
scale, the lower-bound framing falsified *in sign*, one VOID gate undischarged. The twelve harvest
gates in `GATES.md` are prerequisites on any survey-class rerun, and the refuter's corrected
significances are the priors of record.

---

## 5. RECOMMENDATION

**The single best next campaign: the glass transition / amorphous order.**

It is the only candidate in the survey that scores well on the criterion that actually matters —
*the field states our niche as its own open problem* — while also having public data on a
reachable host, no counting noise and therefore no valve floor, immunity from the sign-symmetry
theorem, a ready-made pair-matched null generator (RMC) that the community already trusts, and a
question whose answer is genuinely unknown in either direction. Its prior art is
convergent-*adjacent* and the credits are now identified and quotable (RMPE and the Baranyai–Evans
expansion; Torquato & Stillinger's `g₂`-invariant processes; Shell's `S_rel`), which is exactly the
position the Dalitz campaign ran from successfully. Run §4.1's design, prior-art memo first per
house practice, with the RMC surrogate as the load-bearing gate.

**The single best cheap pilot: the Planck SMICA plumb line.**

Not because it will find anything — §4.2 argues at length that it will not, and says so before any
data is read — but because it is the cheapest way this programme has ever had to buy a **real-data
plumb line where the right answer is a theorem**. The map is already on this disk with its mask and
its beam. The estimator exists. `healpy` is installed. `GATES.md` currently reads NONE-YET in four
plumb-line cells and "held live, not pinned" in the fifth, and this pilot pins all five against a
proved zero on a real instrument with a real mask and real anisotropic noise. Every campaign after
it — glass included — inherits a gauged pipeline instead of an argued one.

**Run them in that order and they compose:** the pilot certifies the instrument against a proved
zero; the campaign then points the certified instrument at a question nobody has an answer to.

---

## 6. WHAT I DID NOT FIND, AND THE REACH OF THIS SURVEY

* **No published measurement of a non-negative pairwise-blind maxent gap swept against a control
  parameter** — the `SPIKE_SURVEY.md` finding survives, but its scope statement needed the
  correction in §3.1, and that correction is the reason to distrust the same bullet in any other
  field this survey also did not reach (materials science, econometrics, ecology, climate).
* **No information-theoretic quantity of any kind computed on a Dalitz plot** — INSPIRE fulltext
  `ft "Dalitz plot" and ft "Shannon entropy"` still returns **0**, re-confirming
  `DALITZ_PRIOR_ART.md`.
* **`ft "residual multiparticle entropy"` returns 0 in INSPIRE** — which is the point: the object
  lives in condensed matter and chemistry, and searching only the physics-of-particles corpus is
  how a programme misses thirty years of work on its own quantity.
* **Reach.** This is a one-pass web and API survey. INSPIRE counts are mine and were run today;
  Zenodo, CERN Open Data and SDSS byte counts and HTTP codes are mine and were run today; the CMB
  FITS headers, column names, mask fraction and map statistics were read off the files on this
  machine. Everything attributed to a paper was taken from an abstract, a publisher page or a
  search summary — **no primary PDF was read end to end**, and several adjudications above (RMPE
  vs. our share; `S_rel` vs. our share) rest on a mathematical argument I made rather than on a
  sentence somebody else wrote. Those two in particular should be re-checked against primary text
  before either is quoted in a write-up. A null from a survey is weaker than a null from an
  experiment, and "not found" is not "does not exist".
