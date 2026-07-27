# DRIFT AUDIT — PRE-REGISTRATION

**Frozen: 2026-07-26, before any bound was assembled.**
**Instrument:** the second named promote instrument on the `law-as-habit` claim —
"the maintenance audit of the constants — a pre-registered drift comparison across
the two classes, protected dials against unprotected ones."
**Target:** kill leg (3) of `law-as-habit`, the separable inversion kill:

> "show the maintenance ordering backwards — a protected dial caught drifting while
> the unprotected ones sit perfectly rigid."

This document fixes the classification rule, the evidence standard, the drift
thresholds, the power criterion, and the scoring table **before** the numbers are
looked up. Nothing below may be revised once `DRIFT_AUDIT_RESULTS.md` exists; a
revision is a new pre-registration with its own commit, and the old one stays.

---

## 0. What this instrument can and cannot do — declared first

Three limits are declared here, in advance, so they cannot be quietly dropped later.

**(a) This audit is one-directional. It can fire the kill. It cannot support the
claim.** House rule 6: a residual is never support. The protected/unprotected
classification was composed on 2026-07-26 *knowing* that α-drift searches come back
null and that Λ is the worst number in physics. The sort is therefore retrodictive
with respect to the drift record, and a null on a protected dial confirms only that
the ordering has not been caught backwards. Expected outcome is NOT FIRED, and NOT
FIRED buys **consistency, never confirmation**.

**(b) The reading predicts an ORDERING, not a RATE.** Nothing in Wilsonian
survivorship, in 't Hooft protection, or in this page's rent clause fixes how fast an
unmaintained habit should decay. So there is no first-principles drift rate to test
against, and a pre-registered yardstick has to be imported from outside the framework
(§4). Any conclusion is conditional on that imported yardstick, and the yardstick is
declared, not derived.

**(c) The classes are not measured in commensurable units, and no common metric will
be manufactured.** Fractional drift per year (α, μ, mass ratios) — dimensionless
equation-of-state deviation (Λ) — a tunnelling lifetime inferred from two pole masses
(Higgs). These are three different observables. This audit will **not** invent a
conversion between them. Each dial is scored on its own natural observable against its
own pre-declared threshold, and the ordering is compared class-to-class only
qualitatively (moving / rigid / not-powered). The absence of a common metric is this
instrument's deepest weakness and it is structural, not fixable by more data.

Consequence of (c): the effective sample on the unprotected side is
**n = 1 watchable dial** (Λ). The Higgs entry is not an observation of motion at all —
it is a theoretical extrapolation of a default schedule from measured pole masses. It
will be scored in a separate register (§6.3) and never counted as observed motion.

---

## 1. The classification rule

### 1.1 The criterion, stated properly

**'t Hooft's naturalness criterion** (G. 't Hooft, *Naturalness, chiral symmetry, and
spontaneous chiral symmetry breaking*, in *Recent Developments in Gauge Theories*,
Cargèse 1979, NATO ASI B59 (1980) 135):

> "at any energy scale μ, a physical parameter or set of physical parameters
> α_i(μ) is allowed to be very small only if the replacement α_i(μ) = 0 would increase
> the symmetry of the system."

Two things follow that this audit will hold itself to:

* The criterion is a licence for **anomalous smallness**. It applies to a parameter
  that is very small compared to its natural scale. It says nothing about a parameter
  of order one. Applying it to a dial that is not anomalously small is a category
  error, and any dial in that position will be labelled **N/A ('t Hooft)** and
  protected — or not — on a separately stated argument.
* The pay-off of passing is **multiplicative renormalisation**: δα_i ∝ α_i, so
  radiative corrections are proportional to the parameter itself and smallness is
  stable under the RG flow. That, and only that, is what "pays its own rent" is
  allowed to mean in this audit.

### 1.2 The three labels (fixed now)

Every dial gets exactly one:

* **PROTECTED** — a stated symmetry or RG argument makes the parameter radiatively
  stable: either (i) it passes 't Hooft strictly (zeroing it restores a symmetry of
  the theory that is *not* broken elsewhere in the same theory), or (ii) it is a
  Wilson-marginal coupling whose only cutoff sensitivity is logarithmic, with the
  relevant operator in its sector forbidden by an exact gauge symmetry.
* **UNPROTECTED** — the parameter multiplies a *relevant* operator (positive mass
  dimension), and zeroing it restores no symmetry of the quantum theory. Cutoff
  sensitivity is power-law; holding the observed value requires order-by-order
  cancellation with no identified payer.
* **UNKNOWN-PROTECTION** — the dial does not sort cleanly: it passes the formal
  criterion but by a symmetry the theory violates elsewhere, or its protection is
  conjectural (depends on a proposed but unobserved mechanism), or the criterion does
  not apply for a stated technical reason.

A fourth, **NOT-SCORED**, is reserved for quantities that are not dimensionless
Standard-Model parameters at all. Their bounds may be reported for completeness but
they contribute no row to the scorecard. Rationale, declared now: for a *dimensionful*
constant, "it varied" is not a unit-independent statement (M. J. Duff,
*Comment on time-variation of fundamental constants*, hep-th/0208093), so a drift
bound on it cannot bear on an ordering claim without first choosing units. **G falls
here**, and this is decided before its bounds are read.

### 1.3 The pre-committed sort

Assigned now, from theory alone, before any bound is looked up. Each dial's label and
the one-line argument that earns it are frozen here; the results document may not
re-sort a dial, only report it.

| Dial | Label | The argument that earns the label |
|---|---|---|
| α (fine-structure) | PROTECTED | **N/A ('t Hooft)** — α ≈ 1/137 is not anomalously small; the criterion does not apply. Protected instead on route (ii): gauge invariance forbids a photon mass, so the U(1) gauge sector carries no relevant operator, α is exactly marginal and runs logarithmically only. |
| m_e (and every charged-fermion mass) | PROTECTED | Strict 't Hooft. m_e → 0 restores an exact chiral U(1)_L × U(1)_R on the electron field. Hence δm_e ∝ m_e ln(Λ/m_e): multiplicative, no additive cutoff sensitivity. |
| μ = m_p/m_e | PROTECTED (two mechanisms, stated separately) | Denominator: chiral protection as above. Numerator: m_p ≈ Λ_QCD, generated by dimensional transmutation from the marginal coupling g_s, Λ_QCD ~ M exp(−c/g_s²) — exponentially small for free, and log-running. Both legs radiatively stable, by *different* arguments; the audit will not blur them. |
| quark / lepton mass ratios | PROTECTED | Strict 't Hooft, chiral, as for m_e. Ratios inherit it. |
| Λ (cosmological constant) | UNPROTECTED | Coefficient of the identity operator: mass dimension 4, the most relevant operator there is. Λ → 0 restores no symmetry of the non-supersymmetric SM (unbroken SUSY would; SUSY is broken). Quartic cutoff sensitivity; the ~120-order discrepancy. |
| Higgs mass² / vev | UNPROTECTED | m_H² multiplies a dimension-2 relevant operator. m_H² → 0 restores only *classical* scale invariance, which is anomalous — broken by the running of the very couplings it would constrain — so it is not a symmetry of the quantum theory and does not satisfy 't Hooft. **Declared dissent:** W. A. Bardeen (FERMILAB-CONF-95-391-T) argues classical scale invariance with only logarithmic anomalous breaking *is* a protection. This audit adopts the majority reading (UNPROTECTED) and records that adopting Bardeen's would move the Higgs row to UNKNOWN-PROTECTION and shrink the unprotected class to n = 1. |
| θ̄_QCD (strong-CP angle) | UNKNOWN-PROTECTION | θ̄ → 0 *does* restore a symmetry (CP, and P and T), so θ̄ formally **passes** 't Hooft — and radiative stability genuinely holds. But the restored symmetry is one the Standard Model violates elsewhere (the CKM phase is O(1)). So θ̄'s protection is real against drift yet explains nothing about its value. The proposed dynamical guardian is Peccei–Quinn (Peccei & Quinn 1977; Weinberg 1978; Wilczek 1978) — the axion, unobserved. |
| G (Newton) | NOT-SCORED | Dimensionful; see §1.2. Reported for completeness only. |

**Pre-registered warning against our own text.** The `law-as-habit` prose currently
says the strong-CP angle is "tiny without visible protection." Per the sort above,
that is imprecise: θ̄ passes the criterion, and the honest statement is that its
protecting symmetry is one the world breaks elsewhere. If the sort above survives the
results stage, the prose is a correction candidate. Registering this now so it cannot
be presented later as a finding of the audit.

---

## 2. Evidence standard

* **Primary literature only.** Every number carries a citation to the paper that
  produced it (journal ref and/or arXiv id). No review-quoted numbers without naming
  the underlying measurement.
* **No meta-analysis.** Independent measurements are *not* combined into a single
  tighter number. For each dial the audit reports the most constraining single
  published bound, plus at least one bound from an independent method, and treats them
  as separate rows.
* **Errors as published.** Central value ± 1σ as the authors state it; statistical and
  systematic separated wherever the paper separates them. Where a bound is quoted at
  another confidence level, that level is stated and no silent conversion is made.
* **Controversy is reported, not resolved.** Where a claimed detection is disputed, both
  the claim and the refutation are cited, and the scoring rule of §3 decides the row —
  not the audit's opinion about who is right.

---

## 3. Drift thresholds (protected side)

For a dimensionless dial *x* with fractional drift rate *ẋ/x*:

* **DRIFT CONFIRMED** — a nonzero drift reported at **≥ 5σ** on the published errors,
  **and** independently replicated by at least one different method or instrument
  class, **and** not withdrawn or attributed to a known systematic in the subsequent
  literature.
* **DRIFT CLAIMED-DISPUTED** — a nonzero result at ≥ 3σ that fails either the
  replication or the un-refuted condition. **Scores as not-confirmed** for the kill,
  and is reported in full with the dispute.
* **NO DRIFT** — consistent with zero at < 3σ, with a stated upper bound.

The ≥ 5σ + independent-replication bar is set high deliberately and is set *before*
looking at the Webb-dipole literature, whose disputed status is known to us in outline.
Registering the bar now removes the freedom to tune it to that case.

---

## 4. The power criterion — what makes a null informative

A null on a protected dial counts for nothing unless the bound was tight enough to have
seen a drift worth calling drift. The framework supplies no rate (§0b), so the yardstick
is imported and named: **the cosmological expansion rate**, H₀ ≈ 7.3 × 10⁻¹¹ yr⁻¹
(h = 0.7, 1/H₀ ≈ 1.37 × 10¹⁰ yr). Rationale: a habit decaying on the timescale over
which the universe has been running is the least contrived "plausible" drift available,
it is exogenous to this framework, and it is the scale every varying-constant model in
the literature is implicitly compared against.

Define **plausible drift** ≡ |ẋ/x| ≥ 0.1 H₀ ≈ 7 × 10⁻¹² yr⁻¹.

Power tiers for a null with 1σ bound *B*:

| Tier | Condition | Meaning |
|---|---|---|
| **STRONG** | B ≤ 10⁻³ H₀ ≈ 7 × 10⁻¹⁴ yr⁻¹ | would have seen a drift a thousand times slower than plausible |
| **MODERATE** | 10⁻³ H₀ < B ≤ 0.1 H₀ | would have seen plausible drift |
| **WEAK** | 0.1 H₀ < B ≤ H₀ | marginal |
| **UNPOWERED** | B > H₀ | the null carries no information; row scores UNTESTABLE |

For bounds expressed as a total fractional change Δx/x over a lookback time T rather
than a rate, the audit converts by |ẋ/x| ≈ (Δx/x)/T, states the T used, and flags the
conversion as assuming a constant rate — which is an assumption, and is recorded as one.

---

## 5. Motion thresholds (unprotected side)

Λ and the Higgs need their own pre-declared observables, since §3's units do not apply.

**Λ — via the dark-energy equation of state.** Observable: the significance of a
w₀wₐCDM preference over ΛCDM in the current large-scale-structure + CMB + SNe
compilations.

* **MOTION CONFIRMED** — ≥ 5σ preference, robust across the independent supernova
  compilations (i.e. not carried by one SNe dataset).
* **MOTION HINTED** — 2.5σ to 5σ, or ≥ 5σ in only some dataset combinations.
* **MOTION ABSENT (RIGID)** — ΛCDM preferred or w₀ = −1, wₐ = 0 recovered within 1σ,
  **with** |wₐ| bounded below 0.1 at 1σ. This is the condition the kill needs on this
  leg, and it is deliberately demanding: "sits perfectly rigid" must mean pinned, not
  merely unrefuted.

**Higgs — via the vacuum's default schedule.** Observable: the stability verdict
implied by the measured m_H and m_t.

* **DEFAULT SCHEDULED** — the electroweak vacuum is metastable at ≥ 2σ in the
  (m_H, m_t) plane, i.e. absolute stability is disfavoured.
* **NO DEFAULT (RIGID)** — absolute stability preferred at ≥ 2σ.
* **UNDECIDED** — the two are within 2σ of each other.

Declared now: a DEFAULT SCHEDULED verdict is **not** observed motion. It is a
theoretical extrapolation and is scored in its own register (§6.3), never summed with
Λ's.

---

## 6. The scorecard rules

### 6.1 The kill is a conjunction

Kill leg (3) reads: "a protected dial caught drifting **while** the unprotected ones
sit perfectly rigid." Both halves are required. Per pair (P, U):

* **FIRED** — P scores DRIFT CONFIRMED (§3) **and** U scores RIGID (§5).
* **NOT FIRED** — the conjunction fails **and** both legs are powered.
* **UNTESTABLE** — either leg is unpowered (§4) or its verdict is UNDECIDED (§5).

Each leg's individual verdict is reported separately as well, so a reader can see how
near each half came without the conjunction hiding it.

### 6.2 What a NOT FIRED buys

Exactly one sentence, fixed now, to be reproduced verbatim in the results:
*The ordering has not been caught backwards; the selection reading gains consistency
and no support.*

### 6.3 The Higgs register

Scored separately as **SCHEDULE PRESENT / ABSENT / UNDECIDED**, and reported as
"consistent with the reading's expectation for an unprotected dial" or not — never as
motion, never entering a FIRED/NOT FIRED conjunction.

### 6.4 θ̄ and G

θ̄ (UNKNOWN-PROTECTION) contributes **no pair** to the conjunction, since the kill is
defined over protected-vs-unprotected. Its bound is reported, and what it *would* mean
under each possible re-classification is stated. G contributes no row (§1.2).

---

## 7. What would make this instrument stronger — recorded now, not later

So that the results section cannot pass off wishes as findings, the honest upgrades are
listed in advance: (i) a pre-registered *rate* prediction from the framework, which
would turn nulls from consistency into a real test; (ii) more than one watchable
unprotected dial; (iii) a drift search on a protected dial at a sensitivity where a
detection would be a genuine surprise rather than an anomaly hunt; (iv) Smolin's
precedence protocol, which is a different instrument entirely and is the one that could
give this claim positive evidence.

---

*Frozen before assembly. Results in `DRIFT_AUDIT_RESULTS.md`.*
