# PRE-REGISTRATION — the pairwise-blind order-3 share on 3D lattice φ⁴ (Wilson–Fisher)

Written and committed **before `phi4_ridge.py` existed**. Scratchpad only: no Lean file, no
`Stance.lean`, no audit, and `lake` is never run.

**Scope, first and load-bearing.** 3D single-component lattice φ⁴ is a **model computation**.
It sits in the 3D Ising universality class, which is the classical-critical universality class
of the Standard Model Higgs sector's scalar — that is a statement about a *universality class*,
not about the Higgs, not about nature, and not about any physical field. Nothing here bears on
the `wild-share` open claim. The near-criticality resonance remains a **wager** on the page;
this run informs it and cannot promote it. No sentence in the results document may be read as
a claim about the world.

**One prior disclosure.** Before writing this file I ran a **timing-only** microbenchmark of the
Metropolis kernel (sweeps/second at four lattice sizes, no observable computed, no physics
parameter set). It fixed the compute budget in §9 and nothing else. It is disclosed rather than
hidden because a budget declared from an unmeasured guess is not a cap.

---

## 1. WHY THIS RUN, AND WHAT WOULD MAKE IT WORTHLESS

The sibling runs (`ISING_FIELD_RESULTS.md`, `CFT_RIDGE_RESULTS.md`) found, in 2D Ising: under
weak symmetry breaking the pairwise-blind order-3 share `I_C^(3)` peaks at criticality, on a
ridge at `h* ∝ L^(−y_h)` with `y_h = 15/8`, carried by well-separated triples, with the
mechanism identified as the CFT's magnetisation sector.

The question here is **whether that is a fact about 2D Ising or a fact about criticality**. 3D
φ⁴ at the Wilson–Fisher fixed point is the same *phenomenon* in a different *universality
class*, with different exponents:

| | 2D Ising | 3D Ising / WF |
|---|---|---|
| `η` | 1/4 | 0.0362978(20) |
| `ν` | 1 | 0.629971(4) |
| `Δ_σ = β/ν = (d−2+η)/2` | **0.125** | **0.5181489** |
| `y_h = (d+2−η)/2` | **1.875** | **2.4818511** |
| `2Δ_σ` (pair) | 0.25 | 1.0362978 |
| `3Δ_σ` (triple) | 0.375 | 1.5544467 |
| `6Δ_σ` (share, if quadratic) | 0.75 | 3.1088934 |

(3D values: Kos–Poland–Simmons-Duffin–Vichi conformal bootstrap. `β/ν + y_h = d = 3` is the
internal check.) **Finding the ridge with 3D-class exponents would show the phenomenon is
universality-class-portable. Finding it with 2D-class exponents, or with no exponent at all,
would show it is not what we think it is.** The exponents differ by a factor ≈ 4 in the share,
so the test has real discriminating power rather than being a consistency check.

**What would make this run worthless, stated first.** φ⁴ is a *continuous* field. Every reading
requires a binarization, and binarizing a purely **pairwise** continuum distribution generically
mints nonzero binary order-3 share. The 2D siblings had no such channel — Ising spins are
natively binary. This is the single largest new risk here and it is gated in §5 as **K3**. If
the measured ridge does not exceed its matched pairwise-continuum surrogate, the run reports a
binarization artifact and no ridge.

---

## 2. THE MODEL, fixed now

Euclidean action on a periodic `L³` lattice, single real component:

> `S[φ] = Σ_x [ ½ Σ_{μ=1..3} (φ_{x+μ̂} − φ_x)² + ½ m² φ_x² + λ φ_x⁴ − h φ_x ]`,  weight `e^{−S}`

Local form used by the sampler (`A` = sum of the 6 neighbours):
`E(φ_x) = (3 + m²/2) φ_x² + λ φ_x⁴ − (A + h) φ_x`.

**`λ = 1.0`, fixed, one value.** `m²` and `h` are the swept parameters. `λ = 0` is used **only**
as a control (§5, K2), always at `m² > 0` where the free theory is stable.

**Sampler: checkerboard Metropolis**, GPU, `R` independent replicas advanced in parallel; a
custom CUDA kernel, uniform proposal `φ' = φ + δ·(2u−1)`. `δ` is adapted to ≈ 50 % acceptance
**during burn-in only** and then frozen, so the measurement segment is a proper time-homogeneous
Markov chain. At `h = 0` a **global sign flip** `φ → −φ` is offered once per sweep per replica
and accepted with probability ½; it is exact there (the action is invariant) and it is what makes
the `h = 0` column a fair test of the sign-symmetry lemma rather than a test of tunnelling.

**Cluster updates are declared unavailable and why.** The Brower–Tamayo embedded-Ising cluster
update requires the global `Z₂` symmetry, which is exactly what `h ≠ 0` breaks. It is therefore
used nowhere in this run — not at `h = 0` either, so that one algorithm carries the whole map and
no comparison is confounded by an algorithm change. The price is critical slowing down, paid for
by measuring `τ_int` at every point, thinning by it, and reporting `N_eff` rather than nominal
`N`. This is the same disclosure the 2D sibling made, for the same reason.

---

## 3. THE INSTRUMENT — two routes, both reported, roles declared in advance

### Route 1 — the b-level exact share on binarized field values

Digitize `φ` at each site into `b` levels by **global quantiles of the pooled single-site field
distribution**, estimated on a dedicated calibration segment taken after burn-in and *before* the
accumulation segment, so no threshold is fitted to the data it is applied to. Build the `b³`
joint histogram of a site triple, pooled over all `L³` lattice translates and all replicas.
`I_C^(3) = S[maxent state carrying all pair marginals] − S[p]`.

Two thresholdings, with **different jobs**, both primary, neither a fallback for the other:

- **(1b) `θ = 0`, the `Z₂`-covariant order parameter.** `s = sign(φ)` is the Ising spin of this
  model: at `h = 0` it is exactly the variable the `Z₂` symmetry acts on. This is the
  **apples-to-apples route for the cross-class comparison** with the 2D runs, and it is the route
  on which every scaling prediction in §4 is scored. It has a computable Gaussian artifact
  baseline (K3), which must be quoted with every number.
- **(1a) the median (`q = 0.5`).** By `Core/SignSymmetry.lean`, any distribution symmetric under
  reflection about its median vector binarizes at the median to a sign-symmetric 8-cell state, whose
  share is **exactly zero**. Every multivariate Gaussian is such a distribution, at any mean, so
  **the median route has an exactly-zero Gaussian baseline at every `h`**. It is the
  **artifact-immune existence route**: a nonzero median-route reading is a measurement of the
  triple's joint reflection asymmetry, which no Gaussian dependence of any covariance can supply.
  It is not immune to skewed marginals carried through a Gaussian copula, so K3 is run on it too.

At `h = 0` the two coincide (the median is 0 by symmetry) and both must read the floor.

**Solvers.** `b = 2`: the **exact one-dimensional `k = 3` solver** — the pair envelope is
one-dimensional (`p + t·σ`, `σ = s₁s₂s₃`), the maxent member is the unique root of
`Σ_s σ(s) log(p_s + tσ(s)) = 0`, solved by bisection in float64 and adjudicated against a
60-digit `mpmath` reference in the gate. **IPF is not used at `b = 2`** — the repository's own
record (`ISING_FIELD_RESULTS.md` §2, memory `ipf-sharek-boundary-drift`) is that IPF one-sidedly
*overstates* the share by up to five orders of magnitude on near-deterministic cells.
`b ∈ {3,4}`: IPF, reported **with a two-sided certificate** — the IPF primal entropy and a dual
bound from the fitted exponential-family potentials — and any point whose bracket is wider than
10 % of the reading is reported **ungauged**, not as a number.

**Occupancy sluice, declared in advance:** a reading is *trustworthy* only if
`min_cell · N_eff ≥ 20` **and** `N_eff ≥ 10³`. Points failing it are reported as excluded, with
the count. Tied fraction is **structurally 0** for a continuous field (no ties possible); this is
stated as vacuous, not as a clean bill.

**Estimator floor.** For every reading: a matched **pair-maxent multinomial surrogate drawn at
`N_eff`, not nominal `N`** (variance inflation `F` measured from the across-replica variance of
the cell frequencies against multinomial), plus a **shuffle floor** (single-site marginals kept,
all cross-site structure destroyed), plus a configuration-level bootstrap. All shares are reported
as **excess over the measured floor**, with raw and floor both printed.

### Route 2 — the continuum moment route

Connected correlators of the field itself, per geometry:
`m₁ = ⟨φ⟩`, `c(r) = ⟨δφ₀ δφ_r⟩`, `U = ⟨δφ₀ δφ_{r₁} δφ_{r₂}⟩` with `δφ = φ − ⟨φ⟩`.

**The criticality-breakdown lesson is carried forward explicitly.** `CFT_RIDGE_RESULTS.md` §3
established that the route "`I_C^(3) ≈ ½ · (connected 3-point)²`" **overstates by 25–64×** in the
linear-response limit and 2.3–6.1× on the ridge, because at criticality the *pair* correlations
stay `O(1)` and they are the expansion parameter. Therefore:

> **The dimensionless pair correlation `ρ(r) = c(r)/c(0)` is quoted beside every moment-route
> number.** Where `ρ = O(1)` the moment route is reported as a **detector** (is there order-3
> structure at all, and how does it scale) and **never as a meter** (how many nats).

The exact bridge that *does* hold is Step A of the sibling: on the one-dimensional `b = 2` pair
envelope, `I_C^(3) = (1/128)·[Σ_s p_s^(−1)]·(Δτ)² + O(Δτ³)` with `Δτ = τ_p − τ_q` the gap between
the state's own triple moment `τ = ⟨s₁s₂s₃⟩` and the pair-maxent's. This is a relation among
*binary* moments and is used as such. The **ratio `U/Δτ`** is measured and reported, as the direct
3D test of whether the 2D breakdown ports.

---

## 4. THE PRE-REGISTERED PREDICTIONS, with thresholds and the meaning of every answer

Scored on route (1b), `θ = 0`, collinear triple at `r = L/4`, unless stated. Lattice sizes
`L ∈ {8, 12, 16, 24, 32}`.

| # | prediction | PASS | MARGINAL | FIRES |
|---|---|---|---|---|
| **E1** | a ridge exists: at `m² = m_c²`, `I_C^(3)(h)` has an interior maximum at `h* > 0`, exceeding its floor by ≥ 5σ at `L ≤ 16` | as stated | 3–5σ | < 3σ, or no interior max |
| **E2** | **`h* ∝ L^(−y_h)` with `y_h = 2.4819`**, read from the **moment collapse** (primary) | `\|y−2.4819\| ≤ 0.10` | ≤ 0.25 | > 0.25 |
| **E2′** | the same read from the **peak locus** (secondary; expected biased) | ≤ 0.10 | ≤ 0.30 | > 0.30 |
| **E3** | moments collapse at matched `(u, r/L)`: `m·L^{0.5181}`, `c·L^{1.0363}`, `τ·L^{1.5544}`, `U·L^{1.5544}` each drift < 3 % over the largest `L`-pair | < 3 % | < 8 % | ≥ 8 % |
| **E4** | **amplitude**: `d ln I_C^(3) / d ln L` at matched `u` over `L = 16→32` equals `−6β/ν = −3.109` | in `[−3.6, −2.6]` | `[−4.2, −2.0]` | outside |
| **E4′** | the **parameter-free scaling ray** (rescale each connected binary moment by `(L₂/L₁)^{−β/ν}` per spin, rebuild the 8-cell state, evaluate the share exactly) predicts the next lattice's share | < 5 % residual | < 15 % | ≥ 15 % |
| **E5** | **`I_C^(3) ∝ h²` at small `h`** (a **gate**, not evidence: it follows from `Z₂` + analyticity at finite `L` whatever the mechanism) | slope `2.00 ± 0.05` | ±0.15 | outside |
| **E6** | **separated > local at `t = 0`**: the `r = L/4` collinear triple exceeds `star` at the ridge, at every `L ≥ 12` | as stated | true at ≥ half the sizes | local ≥ separated everywhere |
| **E7** | **the ridge is critical**: peak share at `t = 0` exceeds the peak at `t = ±Δ` by ≥ 3× | as stated | ≥ 1.5× | < 1.5× |
| **E8** | `U/Δτ` does **not** tend to 1 as `h → 0` at `t = 0` (the 2D breakdown ports) | ratio outside `[0.7, 1.4]` | — | ratio → 1 ± 0.3 |

**The meaning of every possible answer, written down now.**

- **All of E1–E4 pass** → the ridge is universality-class-portable and carries 3D-Ising exponents.
  This is the strongest available outcome and it is still a statement about a model computation.
- **E1 passes, E2 fires toward `1.875`** → whatever we are measuring is not the WF magnetisation
  sector; the 2D result would then be a fact about the 2D instrument, not about criticality.
- **E1 passes, E2 passes, E4 fires flat** → the 2D outcome repeats (the sibling's ridge was flat in
  `L`, explained there as a maximum of the exact scaling ray at `L ≈ 19`). Here the approach
  parameter is `λ = L^{−0.518}`, moving **30 % per doubling** against 2D's 8 %, so the asymptotic
  regime should be reached *sooner*, not later. A flat 3D amplitude would mean the §5 explanation
  of the 2D flatness is wrong, and would be reported as such.
- **E1 fires** → no ridge in 3D. The 2D ridge is then a 2D fact and the class-portability
  hypothesis is dead. This is a real possible outcome and it is the one the run is built to be
  able to report.
- **K3 fires** (below) → the `θ = 0` route is void as a binarization artifact and only the median
  route is readable; every scaling number scored on (1b) is withdrawn.

**Separability.** Each of E1–E8 takes down itself and nothing beneath it. E2 firing does not
touch E1. E4 firing does not touch E2 or E3 (the 2D run is the precedent: its amplitude
prediction fired while its correlator scaling held to 0.1 %).

---

## 5. THE KILL GATES — run first, and any of them fouls the run

| | gate | rule | verdict if it fires |
|---|---|---|---|
| **K1** | **sign symmetry (the plumb line)** | at `h = 0` exactly, both routes must read within the estimator floor: `\|z\| < 3` at every `L`, every `m²`, every geometry. The true value is **exactly zero** by `share_eq_zero_of_signSymmetric` | **VOID.** The whole run is unreadable; no number is reported as a result |
| **K2** | **free-field (Gaussian) machine zero** | at `λ = 0`, `m² > 0`, any `h`: the **median** route must read within floor (`\|z\| < 3`). This is the same theorem with the Gaussian as the symmetric distribution | **VOID** for the median route |
| **K2′** | **sampler plumb line** | at `λ = 0` the measured `⟨φ²⟩` and `c(r)` must match the **exact lattice free propagator** (computed by direct momentum sum) to < 0.5 % | **VOID.** The sampler is wrong |
| **K3** | **binarization artifact — the central gate** | the ridge reading must exceed its **matched pairwise-continuum surrogate** by ≥ 3σ. Surrogate: Gaussian copula fitted to the triple's normal-score correlation matrix, resampled, mapped back through the **exact empirical univariate marginals**, binarized with the identical threshold. This preserves every univariate marginal and all pairwise dependence, and has no three-body structure by construction | route (1b) **VOID**; only the median route is readable, and the `θ=0` scaling scores are withdrawn |
| **K4** | **mixture null** | a **two-component Gaussian mixture** (each component pairwise-only) fitted to the triple, binarized identically. Adjudication is pre-registered and is *not* pass/fail: if the mixture reproduces the share, the finding is **"the order-3 share is carried by a single latent binary collective mode"** — which is the magnetisation-sector mechanism restated, a mechanism identification and a hard bound on interpretation. It is **not** a claim that order-3 structure is absent, and the ridge's *existence* survives it. What it kills is any reading of the ridge as *irreducibly three-body* | interpretation bounded; existence survives; stated in the headline either way |
| **K5** | **dose-vs-rate / τ-invariance** | the peak location `h*` must be invariant to burn-in (`1×` vs `4×`) and thinning gap (`1×` vs `4×`) within its own error bar; `τ_int` measured at every point | reading fouled at the sizes where it fires |
| **K6** | **instrument gate** | the `b=2` solver vs 60-digit `mpmath` (< 1e−12 on the states this run encounters, including its near-deterministic corners); parity reads `ln 2` to 12 digits; an independent state reads 0; 2000 random sign-symmetric states read < 1e−12; the `b≥3` IPF bracketed against its dual; histogram construction verified against brute-force enumeration | **VOID** until fixed. A failed gate is reported, never relaxed |
| **K7** | **coarse-graining / b-stability** | the *existence* and *location* of the ridge must survive `b ∈ {2,3,4}` and the `b=2` quantile sweep `q ∈ {0.3,0.4,0.5,0.6,0.7}` ∪ `{θ=0}`. Magnitudes are expected to differ with `b`; a ridge that exists only at one `b` is minted by the bins | ridge reported as bin-dependent, i.e. not a property of the field |

---

## 6. THE NULLS, named and matched to the data's generative structure

1. **Pair-maxent multinomial at `N_eff`** — the estimator-bias floor. Discrete null for discrete
   data, drawn at the effective, not nominal, sample size.
2. **Shuffle floor** — single-site marginals kept, all cross-site structure destroyed.
3. **Gaussian-copula surrogate (K3)** — the matched *pairwise-continuum* null. This is the null
   that matches this data's generative structure: a continuous field, binarized.
4. **Two-component Gaussian mixture (K4)** — the latent-collective-mode null.
5. **Free field `λ = 0` (K2)** — a null with a *theorem* for its answer, not an estimate.
6. **`h = 0` column (K1)** — likewise.

Nulls 5 and 6 are **plumb lines**, not surrogates: the true value is proved, not simulated. Nulls
3 and 4 are the two **defensible constructions** required by the null-construction-sweep gate;
their spread is quoted as a systematic, not a footnote.

---

## 7. GEOMETRY CLASSES — kept separate, never pooled

| name | displacements | what it is |
|---|---|---|
| `star` | `(1,0,0), (0,1,0), (−1,0,0)` | three neighbours of a common site; **no direct bond inside the triple**, one shared neighbour — the class in which integrating out that neighbour directly generates a three-body coupling. The 2D fixed-field winner |
| `Lcorner` | `(0,0,0), (1,0,0), (0,1,0)` | tightest triple: two NN bonds at a right angle |
| `colin1` | `(0,0,0), (1,0,0), (2,0,0)` | collinear, NN spacing |
| `colin-r` | `(0,0,0), (r,0,0), (2r,0,0)`, `r = L/4` | the maximally spread collinear triple on the ring — separations `(L/4, L/4, L/2)`. **The 2D ridge winner**, and the class every scaling prediction is scored on |
| `far` | `(0,0,0), (L/2,0,0), (0,L/2,0)` | well-separated, non-collinear |

A separation scan `r = 1 … L/2` on `colin-r` is run **once per `L`, at the ridge peak only**, as a
declared separate stage (§9) rather than at every grid point.

---

## 8. WHY AN INTERIOR PEAK IS NOT ITSELF THE FINDING

Stated in advance so it cannot be claimed later. `I_C^(3) ≥ 0` and it vanishes on the entire
boundary of the `(m², h)` quadrant of interest: at `h = 0` by the sign-symmetry lemma; as
`h → ∞` and as `m² → −∞` by determinism; as `m² → +∞` by independence. **An interior maximum is
therefore forced by topology, not discovered.** The content of this run is exclusively: the
**magnitude**, the **locus scaling exponent**, the **geometry ordering**, the **amplitude
exponent**, and whether any of it survives §5.

---

## 9. THE GRIDS AND THE SEARCH CAPS — declared, and nothing outside them is scored

| stage | grid | cap |
|---|---|---|
| **S0** gate (K6) | analytic + enumeration tests | — |
| **S1** bracket `m_c²` | `L ∈ {8,12}`, `h = 0`, `m² ∈ {−12,−11,…,−5}` (8 pts) | 8 |
| **S2** Binder crossing | `L ∈ {8,12,16,24,32}`, `h = 0`, 9 `m²` values on a window of half-width 0.6 about the S1 bracket | 45 |
| **S3a** broad `h` scan | `L = 8`, `m² = m_c²`, `h` on a 13-point geometric grid spanning 4 decades | 13 |
| **S3b** the ridge | `L ∈ {8,12,16,24,32}`, `m² = m_c²`, 12 values of `u = h L^{2.4819}` geometric (ratio ≈ 1.7) about the S3a peak, plus `h = 0` | 65 |
| **S4** off-critical | `L ∈ {8,12,16}`, `m² = m_c² ± 0.5`, same 13-point `h` grid | 78 |
| **S5** separation scan | `L ∈ {8,12,16,24,32}` at the ridge peak, `r = 1 … L/2` | 5 runs |
| **S6** `b` / threshold sweep | at the ridge peak, `b ∈ {2,3,4}` × `q ∈ {0.3,0.4,0.5,0.6,0.7}` ∪ `{θ=0}` | on stored configurations, no new sampling |
| **S7** controls | `λ = 0` at `m² ∈ {0.1, 1.0}` × `h ∈ {0, 0.05, 0.2}`; dose-vs-rate at 3 points × 4 settings | 6 + 12 |

**Total sampled points ≤ 230.** **Wall-clock cap: 8 GPU-hours.** If the cap binds, the columns
are dropped in the order S4, S6, S5 — declared now, so a truncation is not a choice made after
seeing results. Any grid run beyond this table is labelled **post-hoc** in the results, in the row
where it appears, and is not scored against any prediction above.

**Sampling parameters.** `R = 512` replicas for `L ≤ 16`, `R = 256` for `L ∈ {24,32}`. Burn-in
20 000 sweeps. Measurement gap set to `≥ 2 τ_int` from a pilot at the same `(L, m², h)`, floor 20
sweeps; `n_samp = 400` for `L ≤ 16`, 200 for `L ≥ 24`. `τ_int` measured on the magnetisation at
every point and reported. Random seeds fixed and recorded.

---

## 10. HONESTY COMMITMENTS

- **Report the fired kill as plainly as the survival.** The scorecard in §4 is reproduced in the
  results with every row scored, including the ones that fire.
- **The dead stay in the record, marked dead.**
- **A residual is never support.** No post-hoc explanation of a fired prediction counts as a pass;
  it is reported as an explanation of a failure, and it must itself be tested against data it was
  not built on before it is believed.
- **Statuses do not move.** Nothing here can promote `Stance.lean`. Any stance change needs a
  separate refuter pass and Eric's review. This run **informs** the near-criticality wager and
  cannot settle it.
- If the exact-vs-sampled comparison is unavailable (3D admits no `2^N` enumeration and no
  transfer matrix at these sizes), that absence is stated as a **structural weakness of this run
  relative to both 2D siblings**, which each had an exact arm. The substitutes are K2′ (an exactly
  known free-field answer) and K1/K2 (two exactly known zeros).
