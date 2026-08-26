# Results — building the preferred-frame dark sector

Run 2026-07-24. Prereg: `preferred-frame-prereg.md`, frozen before any number
was computed. Scripts: `cuscuton_check.py` (symbolic), `crest_predict.py`,
`crest_scan.py` (numeric). `Stance.lean` NOT modified.

## VERDICT: the mechanism is buildable and half-built already — but the sharp prediction is not a prediction

Three findings, in increasing order of consequence for the stance.

1. The smoothness half of the escape hatch **exists and is ~19 years old**.
2. It **structurally cannot deliver the phantom crossing** — a new obstruction,
   derived here, that the stance does not currently record.
3. The crossing redshift z_c = 0.59 ± 0.03 **is not derivable from the frame**.
   It moves 0.66 in z per decade of the declared unit mass — so the frozen
   window is one free upstream choice deep, and `provenance_line` proves the
   instrument cannot supply that choice.

---

## 1. The smoothness half is already built (H1 — clause-death candidate)

The stance says a preferred-frame dark sector is "an allowed kind of theory, but
a heavy one... and we have not built it."

The object that does the job is the **cuscuton** (Afshordi, Chung & Geshnizjani,
PRD 75, 083513, 2007): a k-essence field with a square-root kinetic term,

    P = ε·μ²·√(2X) − V(φ),      X = −½ ∂_μφ ∂^μφ,      ε = ±1.

Verified symbolically here (`cuscuton_check.py`):

| quantity | result |
|---|---|
| energy density ρ = 2X·P_X − P | **= V(φ) exactly** |
| pressure p = P | ε·μ²·\|φ̇\| − V |
| perturbation kinetic operator P_X + 2X·P_XX | **≡ 0 identically** |
| sound speed c_s² = P_X/(P_X + 2X·P_XX) | **infinite** |

The vanishing denominator is the whole point: δφ is **not a propagating degree
of freedom**. It is constrained — slaved to the matter — so infinite c_s does
not transmit information and the theory stays causal. Infinite sound speed means
an infinite sound horizon, hence **no clustering at any scale**: exactly smooth,
*derived*, not imposed. That is precisely what `dm-foliation`'s promote field
asks for. Surfaces of constant φ furnish the preferred foliation.

So requirements (A) smooth and (D) stable/causal are met, by published work,
with a preferred foliation, and the "we have not built it" clause is in the same
position `tsvf-third` was in before it died: **the work called future was
published while we were calling it future.**

> STATUS OF THIS ITEM: the algebra above is verified here and is exact. The
> attribution to Afshordi–Chung–Geshnizjani and the equivalence to the
> khronometric / low-energy Hořava limit are from memory and **were not
> confirmed against primary sources in this run** — the literature agents did
> not return before write-up. Treat the citation as UNCONFIRMED pending a
> primary-source check. The obstruction in §2 does not depend on it.

## 2. NEW OBSTRUCTION: a single cuscuton can never cross w = −1

This was not anticipated by the stance and it cuts against the extensive branch.

From ρ = V and p = ε·μ²|φ̇| − V:

    w + 1 = ε · μ² · |φ̇| / V

with |φ̇| ≥ 0 and V > 0. **The sign of w+1 is locked to ε, a discrete choice in
the Lagrangian, for all time.** ε = +1 gives w ≥ −1 always; ε = −1 gives
w ≤ −1 always. Neither crosses. Equivalently: ρ = V evolves monotonically, so
the density can only fall or only rise — **it has no crest**.

And the crest is exactly what is needed, because for any component
ρ̇ = −3H(1+w)ρ, so with ρ > 0 and H > 0,

    ρ̇ = 0  ⟺  w = −1.

**The extensive branch's "crest" and its "phantom crossing" are the same event,
identically.** So the obstruction is fatal to the simplest realization: the
obvious escape hatch delivers smoothness and forbids the crossing.

**Repair, and its price.** Two cuscutons of opposite sign:

    w_eff + 1 = (μ₁²|φ̇₁| − μ₂²|φ̇₂|) / (V₁ + V₂)

crosses zero when μ₁²|φ̇₁| = μ₂²|φ̇₂|. Both components have c_s² = ∞, so the sum
is still exactly smooth. Crossing achieved, smoothness preserved, causality
preserved. **But the crossing epoch is then set by the two potentials and
initial conditions — it is an input.** z_c = 0.59 would be tuned, not predicted.
(Whether an *extended* cuscuton crosses while keeping both properties in a
single field is the open literature question this run did not resolve.)

## 3. The crossing redshift is not a prediction of the frame (H3 — the real result)

The extensive reading says ρ_DE ∝ S_total. Using the repo's own equicorrelation
formula (`Core/Intensive.lean`), the large-k coordination density is

    S/V  →  n(z) · [ −ln(1 − ρ_corr(z)) ]   ==   N · s

Computed from standard ΛCDM with no fitting: Planck-2018 parameters,
Eisenstein–Hu transfer function, Sheth–Tormen mass function for n(>M_min, z),
and ρ_corr(z) = ξ_R(d,z)/σ²(R,z) at the mean unit separation d = n^(−1/3).

**A crest exists and is generic** — the extensive total really does climb, crest
and fall. The qualitative story survives. But:

| M_min [M⊙/h] | mean sep [Mpc/h] | z_crest |
|---|---|---|
| 1.0e10 | 1.56 | 1.353 |
| 3.2e10 | 2.18 | 1.015 |
| 1.0e11 | 3.07 | 0.686 |
| 2.0e11 | 3.77 | 0.490 |
| 3.2e11 | 4.32 | 0.359 |
| 5.0e11 | 4.96 | 0.226 |
| 1.0e12 | 6.13 | 0.020 |

**|dz_c / dlog₁₀ M_min| ≈ 0.66, stable across the whole well-behaved range.**
(Above ~10¹³ M⊙/h the reading degenerates: ρ_corr → 0 and turns negative, so
N·s → 0 and the apparent crests there are noise about zero, not features. The
honest branch is M_min ≲ 10¹².)

Against the pre-committed reading, this is unambiguously the **large** case
(≳ 0.3 per decade), and the pre-registered consequence follows:

    To land inside z_c = 0.59 ± 0.03, M_min must be declared to within
    0.091 dex — a factor of 1.23, i.e. ±11% — which is 2.3% of a
    4-decade prior on what counts as one coordinating unit.

`provenance_line` (proved, `Core/Provenance.lean`) says the partition is not a
function of the correlation matrix: it is declared, not discovered, and the file
already names it "the single largest source of silent error." So the frozen
window is reachable — M_min ≈ 1.4×10¹¹ M⊙/h puts the crest at 0.59 — but
**reaching it is a declaration, not a derivation.** The extensive branch's one
sharp, dated, falsifiable number is a prediction of the frame *plus* an
upstream choice the frame provably cannot make.

There is a **second** undetermined choice on top: the correlation-assignment
rule ρ_corr = ξ_R(d)/σ²_R is mine, declared in the prereg as a choice. The
framework does not fix it, and a different rule moves z_c again.

## 4. Connection to the new temporal kernel (`Core/Temporal.lean`, fd59378)

`parity_needs_memory` proves that whole-only pattern across time is exactly what
memory buys: no memoryless process writes it, one remembered bit does. That
sharpens the branch duel into a structural statement:

* **Intensive** = a per-unit *state function*. Memoryless. Its value depends on
  the present correlation only. Monotone, hence path-independent — holonomic in
  the Lagrangian sense, with no loops to transport around.
* **Extensive** = a *running total*. It integrates the history of structure
  formation, so it is memory by construction — non-Markovian, path-dependent,
  and needing a slicing to be added up in. Holonomy in the gauge sense.

The cuscuton happens to split exactly along that line: **memory in the global
background sector** (φ(t) is dynamical and carries the running total),
**no memory in the local sector** (δφ is constrained, so nothing clumps). That
is a genuine point in the construction's favour and it is why the mechanism fits
the extensive branch at all.

CONJECTURE, wager-level, offered for the record and not for the stance: if the
extensive branch is right, its running total needs a physical register, and
`dm-foliation` already nominates dark matter as what sets the clock. Dark matter
as *the register* rather than merely the frame-marker would sharpen
`dark-medium` — "the paper the books are written on" is, read literally, a
memory medium. **Kill:** exhibit the extensive total kept on a foliation that
demonstrably is not the dark-matter rest frame, or show the running total
requires no register beyond the field's own background value. I have not tested
this and it should not enter the stance on my say-so.

## 5. Drafted band updates (NOT applied — for review)

For `dark-balance-extensive`, replace the "we have not built it" clause:

> "...the only escape is to make the grand total not a substance at all, but one
> universe-wide quantity pinned to a single special slicing of time — a
> 'preferred-frame' dark sector. The smoothness half of that machinery turns out
> to be BUILT, and long since: an infinite-sound-speed constrained scalar has
> exactly zero clustering at every scale as a derived consequence, with no
> propagating local mode and no superluminal signalling. But building it exposes
> a NEW obstruction we had not stated: such a field's density is its potential,
> so its equation of state is sign-locked and it can never CROSS w = −1 — and
> for any component the crest and the crossing are the same event. Crossing
> needs two opposed components, which restores it at the price of making the
> crossing epoch an input. Worse for this branch's one sharp number: computing
> the grand total from standard structure formation gives a crest that is
> generic in shape but moves 0.66 in redshift per decade of the declared unit
> mass, so the frozen 0.59 ± 0.03 window requires declaring the unit to ±11% —
> a choice `provenance_line` proves the instrument cannot supply. The window
> stays as the staked kill, but it is no longer advertised as a prediction OF
> the frame."

For `dm-foliation`'s confidence band: the promote field's clause (i) — smoothness
"as a derived consequence, not an imposed one" — is **payable now** by importing
the constrained-scalar mechanism. Clause (ii), surviving preferred-frame
signals, is untouched by this run and remains the real cost.

---

# UPDATE — after the literature check (same day, appended not rewritten)

The sections above were written before any primary source was consulted. They
are left exactly as they stood. Four things changed.

## U1. The cuscuton attribution is CONFIRMED — and it is the INTENSIVE branch's mechanism, not the extensive one

Afshordi, Chung, Doran & Geshnizjani, *Cuscuton Cosmology: Dark Energy meets
Modified Gravity*, astro-ph/0702002 (2007). Verified from the abstract: its
perturbations "do not introduce any additional dynamical degree of freedom and
only satisfy a constraint equation," and "the evolution is local on
super-horizon scales, implying that there is no gross violation of causality,
despite Cuscuton's infinite speed of sound."

**But now put the ε = +1 cuscuton beside what the intensive branch predicts:**

| `dark-balance-intensive` asserts | ε = +1 cuscuton delivers |
|---|---|
| perfectly smooth, never clumps, at any measurable scale | c_s² = ∞ ⇒ exactly zero clustering, **derived** |
| "can only shrink over time, or hold still. It can never grow" | ρ̇ = −3Hμ²\|φ̇\| ≤ 0, monotone non-increasing |
| "forbids phantom, at every moment, always" | w + 1 = +μ²\|φ̇\|/V ≥ 0, sign-locked |

**All three, exactly, with no tuning.** I set out to build the machinery the
*extensive* branch owes and instead found a ready-made, published, causal,
ghost-free field-theoretic realization of its **rival** — and the same
construction structurally forbids the crossing the extensive branch needs.

That is a real shift in the theoretical prior. The stance currently has the
intensive branch "theorem-backed but data-pressured" and the extensive branch
"favored by data" but owing a mechanism. The correct picture is sharper: the
intensive branch owes **no** mechanism — it has had one since 2007 — while the
extensive branch owes one that provably cannot be the obvious candidate.

## U2. H2 partially answered: crossing IS achievable, at a cost to smoothness

*A General Model for Dark Energy Crossing the Phantom Divide*, arXiv:2508.01378
(JCAP 2025, 10, 078). Spatially covariant construction in which "the sound speed
of the scalar mode is scale-dependent and approaches infinity at large scale, so
that the field becomes non-dynamical in the infrared limit."

So a cuscuton-*like* field can cross. But the smoothness is only **IR**: it
retains a propagating scalar mode with finite sound speed at smaller scales, so
it is not exactly smooth at all scales. Read against the extensive branch that
is arguably a *feature* — that branch is built from a clumpy source and
`void-excess` says it actively wants a mild ISW excess. Worth pursuing. It does
not rescue the z_c problem in §3, which is upstream of any mechanism.

## U3. DESI DR3 is NOT released as of July 2026 — and DR2 already erodes the intensive branch's escape route

No DR3 in the literature; DR2 (three years of observations, seven redshift bins
0.1 < z < 4.2) remains current. The duel is undecided and the stance's dating is
intact.

Two DR2 details that matter, both needing primary-source confirmation before
being banked:

* The reported phantom crossing sits "around z ≈ 0.5". The frozen window is
  0.59 ± 0.03. If the published central value really is ≈ 0.5, the extensive
  branch's window is **already under pressure**, not merely awaiting DR3.
* DR2 reportedly prefers dynamical dark energy **even with supernovae
  excluded**. The intensive branch's stated hope is precisely that the lean is a
  supernova systematic and that geometry-only DR3 will rescue it. If BAO
  geometry alone already prefers evolution, that hope is weaker than the stance
  currently says.

## U4. The sharpest finding: computed honestly, the INTENSIVE branch crosses too

Running the repo's own coordination formula through ΛCDM structure formation
(`branch_wz.py`), using 1+w = −⅓·dln ρ_DE/dln a:

| z | ρ_corr | s = −ln(1−ρ_corr) | w_intensive | w_extensive |
|---|---|---|---|---|
| 0.02 | 0.2067 | 0.2315 | **−0.979** | **−0.931** |
| 0.48 | 0.2101 | 0.2358 | −0.993 | −0.977 |
| 0.71 | 0.2100 | 0.2358 | −1.009 | −1.028 |
| 1.40 | 0.2025 | 0.2263 | −1.082 | −1.269 |
| 3.00 | 0.1527 | 0.1657 | −1.376 | −2.200 |

Both branches produce phantom in the past, crossing near z ≈ 0.6, with
w₀ ≈ −0.93 to −0.98 — qualitatively the DESI DR2 shape. But note what that means
for the duel: **the per-unit balance s is NON-MONOTONIC** (dln s/dln a runs from
−0.062 to +1.101 over z ∈ [0.02, 3]). It rises with time to a peak near z ≈ 0.6,
then falls. So the intensive branch, computed this way, *also* crosses the
phantom divide — contradicting its own central claim to forbid phantom "at every
moment, always."

**This is not a contradiction with any machine-checked theorem, and it must not
be reported as one.** `Sfun_antitone_of_rho_antitone` is conditional: it
concludes the balance falls *given that the underlying correlation falls*. Under
the cosmological assignment used here that hypothesis is simply false over part
of the range — ρ_corr rises from z = 3 to z ≈ 0.6. And `contraction` forbids
raising the reading by **local pointwise mixing**; structure formation is
gravitational *interaction*, which `true-books` explicitly identifies as the one
thing that CAN write a real entry. Gravity is allowed to raise coordination.

So the intensive branch's "can only shrink" is an **additional physical
assumption about the real universe**, not a corollary of the proved
monotonicity — and the stance's promote field currently reads as though the
mathematics settles it ("The mathematics owed here is now paid in full"). The
mathematics is paid. The *hypothesis discharge* — showing ρ_corr actually falls
in our universe — is not, and is not currently listed as owed.

**Same caveat as §3, and it is load-bearing:** ρ_corr = ξ_R(d)/σ²_R at the mean
unit separation is my declared rule. A different rule can flip this sign. What
is *not* rule-dependent is that the framework does not pin the rule — the same
provenance exposure as the partition, now hitting the intensive branch too.

## U6. THE PRICE OF ADMISSION, now priced — and it is payable

This is what §6 listed as unpriced and what `dm-foliation`'s promote clause (ii)
actually owes. Sources: Oost, Mukohyama & Wang, arXiv:1802.04303 ("Constraints
on Einstein-aether theory after GW170817"), plus the pulsar bounds below.

**The bounds.**

| constraint | bound | source |
|---|---|---|
| GW speed (tensor mode) | \|c₁₃\| ≲ **10⁻¹⁵** | GW170817 + GRB170817A |
| PPN preferred-frame | \|α₁\| < **3.4×10⁻⁵** | PSR J1738+0333 |
| PPN preferred-frame | \|α₂\| < **1.6×10⁻⁹** | PSR B1937+21, J1744−1134 |
| BBN (G_cos vs G_N) | \|G_cos/G_N − 1\| ≲ 1/8 ⇒ 0 < c₂ ≲ **0.095** | ibid. |

**What survives.** Not nothing — two *disconnected* corners of Einstein-aether
parameter space, with c₁₃ ≃ 0 forced throughout:

* **Region (i):** 0 < c₁₄ ≤ 2×10⁻⁷, with c₁₄ ≲ c₁ and c₁₄ ≲ c₂ ≲ 0.095.
* **Region (ii):** 2×10⁻⁶ ≲ c₁₄ ≲ 2.5×10⁻⁵, with 0 ≲ c₂ − c₁₄ ≲ 2×10⁻⁷ —
  i.e. c₂ must equal c₁₄ to about **2%**, a coincidence between two independent
  couplings.

The khronometric (hypersurface-orthogonal) case — which is the one that supplies
a foliation, and therefore the one `dm-foliation` needs — **survives**.

**The verdict, and it cuts both ways.** A preferred-foliation dark sector is
**observationally viable in 2026**. The stance's characterisation — "an allowed
kind of theory, but a heavy one" — is correct, and the heaviness is now
quantified: fifteen orders of magnitude on one coupling, plus either a very
small c₁₄ or a 2% coincidence.

But the paper's own summary of the surviving corner is the sting: with
\|c₁₃\| < 10⁻¹⁵, preferred-frame effects become "**observationally negligible**
in both cosmological and local regimes."

So clause (ii) of `dm-foliation`'s promote — "survives its own new
preferred-frame signals in the data" — is **payable, and cheaply, because in the
surviving region there are no new signals left to survive.** That is good news
for viability and bad news for falsifiability, and the stance should say both.
`dm-foliation`'s stated kill is a measured direction-dependence in dark
energy's behaviour that fails to line up with the CMB frame. The theory's only
viable corner is the one where that dipole is pushed below detectability. The
kill is not dead, but the surviving theory is built so as not to fire it.

Draft addition to `dm-foliation` confidence (NOT applied): *"Now priced. The
preferred-frame sector is viable: khronometric theory survives GW170817
(\|c₁₃\| ≲ 10⁻¹⁵), the pulsar PPN bounds (\|α₁\| < 3.4e−5, \|α₂\| < 1.6e−9) and
BBN (0 < c₂ ≲ 0.095), in two narrow disconnected corners — one requiring
c₁₄ ≤ 2e−7, the other a 2% coincidence between c₂ and c₁₄. But the corner that
survives is the corner where preferred-frame effects are observationally
negligible. So the promote clause about surviving new signals is cheap for the
wrong reason, and this claim's own kill — a dark-energy dipole misaligned with
the CMB frame — is one the viable theory is structured not to fire."*

## U7. The frozen window tested against data in hand — and the DR3 duel is not clean

`desi_crossing.py`. CPL crossing: a_c = 1 + (1+w₀)/wₐ, z_c = 1/a_c − 1.

| dataset | w₀ | wₐ | **z_c** | vs frozen 0.59 ± 0.03 |
|---|---|---|---|---|
| DESI BAO + CMB (no SNe) | −0.42 ± 0.21 | −1.75 ± 0.58 | **0.496** | 0.3σ–2.2σ — **survives** |
| + Pantheon+ | −0.838 ± 0.055 | −0.62 ± 0.205 | **0.354** | 3.3σ–10σ for ρ ≤ −0.9 — **fires** |

(σ(z_c) is dominated by the unpublished w₀–wₐ correlation, so it is scanned over
ρ ∈ [0, −0.99] rather than assumed. Central values are search-retrieved, not
read off the DESI papers — see the script's provenance note.)

**Two consequences, and the second is the more important.**

*First:* the extensive branch's frozen window is **already under pressure from
data in hand** — but only from the supernova-inclusive fit. Geometry plus CMB
alone leaves it comfortably alive.

*Second, and this is a structural problem with how the stance frames the duel:*
`dark-balance-intensive` hopes the crossing lean is a supernova systematic and
that geometry-only DR3 will vindicate it. But the supernovae are also exactly
what pushes the crossing *away* from the extensive branch's window. So the same
unresolved systematic moves **both** branches, in opposite directions:

* SNe right → extensive window in trouble now; intensive's escape route gone.
* SNe carry the suspected systematic → extensive window survives; **and so does
  intensive's escape route.**

The stance presents DR3's geometry-only check as one dated test that at most one
branch survives. It is better described as a test whose verdict is **hostage to a
systematic that is itself the live question**. That is a real weakness in the
duel's construction and it is not currently stated.

**And one primary-source hit on the intensive branch.** Confirmed from the
arXiv:2503.14738 abstract: DESI BAO + CMB alone — **no supernovae** — prefers
dynamical dark energy over ΛCDM at **3.1σ** (rising to 2.8–4.2σ depending on
which SNe compilation is added). `dark-balance-intensive` states its hope as
"much of that lean rides on supernova brightness measurements, and if those
carry a hidden error, this reading and plain dark energy recover together."
A 3.1σ preference without any supernovae means that hope is **weaker than the
claim currently says**, and this is confirmed from the paper's own abstract
rather than a secondary source.

Draft addition to `dark-balance-intensive` confidence (NOT applied): *"The
supernova-systematic escape route is narrower than stated: DESI DR2 BAO+CMB
alone, with no supernovae at all, already prefers evolving dark energy at 3.1σ
(arXiv:2503.14738). A hidden SNe error would therefore not by itself restore
this reading."*

## U8. THE CHAINS — and a correction to U7

`desi_chains_zc.py`. Chains from the `unimpeded` public nested-sampling database
(Ong & Handley, arXiv:2511.05470 / 2511.04661), Zenodo-hosted, model `walcdm`
= w₀wₐCDM, ~120k samples per combination. **U7's tension numbers were wrong and
are superseded by this section.**

**The covariance, measured:**

| dataset | w₀ | wₐ | cov(w₀,wₐ) | **ρ** |
|---|---|---|---|---|
| DESI DR2 + Planck (no SNe) | −0.4489 ± 0.2109 | −1.6451 ± 0.6043 | −0.12452 | **−0.977** |
| + Pantheon+ | −0.8391 ± 0.0537 | −0.5967 ± 0.1983 | −0.00944 | **−0.886** |
| + Union3 | −0.6779 ± 0.0894 | −1.0367 ± 0.2957 | −0.02461 | **−0.931** |
| + DES-Y5 | −0.7531 ± 0.0567 | −0.8462 ± 0.2253 | −0.01158 | **−0.907** |

So the anti-correlation is extreme, ρ ∈ [−0.98, −0.89]. (The search-retrieved
central values used in U7 were accurate to well within their errors; the
*correlation* was the missing piece, and it was the piece that mattered.)

**But do not use ρ in a linear propagation — that is exactly the error U7 made.**
z_c is strongly nonlinear in (w₀, wₐ), and the posterior is heavy-tailed: for
Pantheon+ the sample sd is 0.242 while the 68% half-width is ~0.084. A Gaussian
σ is not a meaningful summary. Pushing every sample through
a_c = 1 + (1+w₀)/wₐ, z_c = 1/a_c − 1 gives the posterior directly:

| dataset | z_c median [68%] | mass **inside** 0.59 ± 0.03 | **P(z_c ≥ 0.59)** | one-sided |
|---|---|---|---|---|
| DESI DR2 + Planck (no SNe) | 0.504 [0.438, 0.571] | 14.5% | **10.6%** | 1.25σ |
| + Pantheon+ | 0.371 [0.297, 0.465] | 2.3% | **3.7%** | 1.79σ |
| + Union3 | 0.451 [0.389, 0.530] | 6.1% | **6.1%** | 1.55σ |
| + DES-Y5 | 0.413 [0.357, 0.495] | 3.1% | **4.1%** | 1.74σ |

**VERDICT ON THE FROZEN WINDOW: disfavored by all four combinations, killed by
none.** The window sits in the upper tail of every posterior, with one-sided
tail probability between 3.7% and 10.6% — nowhere near a kill.

**The correction, stated plainly.** U7 reported "3.3–10σ" tension for the
Pantheon+ combination from linear error propagation at assumed ρ. The true
posterior gives **1.79σ**. Linear propagation overstated the tension by roughly a
factor of two to five, because it cannot see the heavy upper tail in z_c. The
earlier number should not be quoted. This is precisely the failure mode that
made getting the chains worth the trouble, and it is recorded rather than
quietly overwritten.

**What survives from U7, and what does not.**

* *Survives:* the direction. Supernovae pull the crossing **away** from the
  frozen window (10.6% → 3.7–6.1%), so the structural point stands — the same
  SNe systematic moves both branches in opposite directions, and DR3's
  geometry-only check is not the clean separator the stance presents.
* *Survives, and is now primary-source confirmed:* DESI BAO+CMB alone prefers
  dynamical dark energy at 3.1σ (arXiv:2503.14738 abstract), so the intensive
  branch's supernova-systematic escape route is genuinely narrower than stated.
* *Does NOT survive:* the claim that the frozen window is fired, or nearly
  fired, by data in hand. It is not. It is disfavored at 1.2–1.8σ.

**One further fact worth banking:** ~100% of the posterior in every combination
has a real crossing at z ≥ 0. DESI DR2 robustly wants a phantom crossing — it
just wants it at z ≈ 0.37–0.50 rather than 0.59. The extensive branch's
*qualitative* prediction (there is a crossing) is in good shape; its
*quantitative* one (at 0.59 ± 0.03) is the part under pressure.

Draft addition to `dark-balance-extensive` confidence (NOT applied, supersedes
the U7 draft): *"Tested against DESI DR2 chains directly (unimpeded / Zenodo,
w0waCDM, ~120k samples). The data robustly want a crossing — ~100% of the
posterior has one at z ≥ 0, which supports this branch qualitatively over its
no-crossing rival. But the crossing is measured at z_c = 0.504 [0.438, 0.571]
without supernovae and 0.371–0.451 with them, against this claim's frozen
window of 0.59 ± 0.03. The window sits in the upper tail of every combination:
one-sided P(z_c ≥ 0.59) runs 10.6% (no SNe) to 3.7% (Pantheon+). Disfavored at
1.2–1.8 sigma, not fired. Note the reversal this creates: the supernovae that
this branch's rival hopes are systematically wrong are the same data pulling the
crossing away from this branch's window, so a confirmed SNe systematic would
help BOTH branches and DR3's geometry-only check does not cleanly separate
them."*

## U5. Revised draft band updates (NOT applied)

Supersedes §5 for the intensive branch, which §5 did not touch:

* `dark-balance-intensive` — add to promote: *"A third thing is owed and was not
  previously listed: discharging the monotonicity theorem's HYPOTHESIS. The Lean
  proves the per-unit balance falls when the underlying correlation falls; it
  does not prove the correlation falls. A first cosmological estimate makes it
  RISE from z≈3 to z≈0.6 and fall thereafter, which would make this branch cross
  the phantom divide it claims to forbid. Until the correlation's own evolution
  is pinned, 'the mathematics owed here is now paid in full' overstates it."*
* `dark-balance-intensive` — add to confidence: *"A published mechanism exists
  and was not previously credited: an infinite-sound-speed constrained scalar
  delivers all three of this branch's signatures — exact smoothness, monotone
  decrease, and no phantom ever — with no tuning and no extra degree of freedom.
  This branch owes no mechanism; its rival does."*

## 6. Honest edges

* **Partially resolved by the UPDATE above.** Cuscuton attribution: CONFIRMED
  (astro-ph/0702002). Crossing-with-IR-smoothness: CONFIRMED to exist
  (arXiv:2508.01378). DR3 release status: CONFIRMED not released as of July 2026.
* **Now priced (U6).** The preferred-frame admission fee — GW170817, PPN α₁/α₂,
  BBN — is verified against arXiv:1802.04303 and the pulsar literature. The
  khronometric/aether relation is confirmed there too (hypersurface-orthogonal
  aether = Hořava IR limit).
* **Still UNVERIFIED.** Gravitational Cherenkov bounds specifically (the other
  three constraints were found; this one was not separately checked). The two
  DR2 details in U3 — crossing central value ≈ 0.5, and dynamical preference
  surviving SNe exclusion — come from a search summary, **not** from the DESI
  papers, and must be checked against primary sources before either is used
  against a branch. The DR2 crossing redshift is the single most valuable
  outstanding number: if the published central value really is ≈ 0.5, the
  extensive branch's frozen 0.59 ± 0.03 window is already under pressure from
  data in hand, independent of everything else in this document.
* **The three research agents never delivered.** All findings here are my own
  searches and derivations. Nothing in this document rests on an agent report.
* The symbolic result (§2) is exact algebra and stands independently.
* The numeric result (§3) is one correlation-assignment rule, one mass-function
  fit, one transfer function, linear theory only, and no error budget on z_c
  beyond the partition sensitivity. The sensitivity is the finding; the absolute
  z_c values should not be quoted as predictions.
* Nothing here is a measurement. No status changes. A construction that works is
  not evidence that nature uses it.
