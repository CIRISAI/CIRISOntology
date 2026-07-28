# Resource-theory adjudication — what the share is, who else found it, and what they know that we do not

**Asked by:** the coordinator's four-verb proposal (STORE / MINT / MAINTAIN / HIDE) and Eric's
question — are those the right verbs, and what is the prior art?
**Answered by:** the resource-theory agent, 2026-07-27. No Lean run, no `lake`, no stance touched.
**Posture:** convergence-seeking. A literature that already reached our object is a **hit**, not a
strike: it corroborates that the object is real rather than an artefact of our framing, it hands us a
better-tested vocabulary, and it is the only way to learn the object's correct name. The governing
question of every section below is **"who else found this, and what did they learn that we have
not?"** — not "is anything still ours".

> ### CORRECTION to the first version of this document (commit `c4efd47`)
>
> That version concluded "the share is not a resource and cannot be made into one." **The second
> clause is wrong and the conclusion is materially different.** Following the reframe, I looked for
> what the resource-theory community does when a candidate monotone increases under the natural
> operations — exactly the question Eric asked me to add — and the answer inverts the verdict.
>
> The share satisfies `share(p) = min_{q ∈ F} D(p ‖ q)` over the free set `F` **exactly** (verified
> below, ≤ 5.7e-16 on seven states). It is therefore a **relative entropy of resource**, and every
> such quantity is *automatically* a monotone under the **maximal** free-operation class. **There is
> a resource theory. What fails is the specific choice of local operations as the free ones — and
> the framework has a standard name for that failure and a standard repair for it.**

---

## THE HEADLINE, in the literature's vocabulary rather than ours

| our sentence | the literature's sentence |
|---|---|
| "per-cell noise mints whole-only share" | **damping is not a resource-non-generating operation** |
| "the share is not a monotone under local channels" | **local operations are not in RNG for this free set** — Zhou, PRA 80, 022113 (2009) |
| "the pump is a convex combination" | **the free set is an exponential family: e-flat, not m-flat** — Amari (2001) |
| "share = sup(pairEnvelope) − entropy" | **the deviance of the no-three-factor-interaction model** — Bartlett (1935) |
| "the estimator floor is 0.227/N" | **Wilks' theorem, df = 1** (1938) |
| "is the binarization lumpable?" | **is the model collapsible onto that margin?** — Asmussen & Edwards (1983) |

Every row is a gain. The right-hand column is what this repository should be saying.

---

## (a) THE VERB QUESTION

### Ruling on the coordinator's two pre-search claims

**Claim 1 — "HIDE is an adversarial verb presuming an agent and does not belong beside three
dynamical ones." AGREED as to the conclusion; the reason is different and stronger.**

Hide should go, but not because it presumes an agent. It should go because **it is the definiens,
not a verb.** "Invisible to every pair" is not something the share *does*; it is what the share *is*.
`SamePairs` is the constraint set of the variational problem; `pairwise_blind_to_parity` is the
exhibited instance; `share_copied = 0` against `S_total_copied = log 2` is this repository's own
proof that pair-blindness is the defining property and not an incidental one. A campaign on HIDE
could only rediscover `Core/Share.lean`.

The agential reading is not empty — it has a name and a fifty-year literature (§(c)2) — but there it
is a property of a *scheme somebody designs*, not a process a system undergoes. And that literature
is worth adopting for the CAPACITY verb, which is where its results actually bite.

**Claim 2 — "STORE collapses into MAINTAIN under `unpaid_decays`." REJECTED, on two grounds.**

*Ground one — the inference is the model-to-world laundering `epistemology.md` forbids.*
`unpaid_decays` is a theorem about `Core/Maintenance.lean`'s scalar recursion `S ↦ (1−γ)S + α` with
`0 < γ` as an explicit hypothesis. It says nothing about `share`, and no theorem in this repository
connects a decay rate to any share dynamics. That file's own SCOPE paragraph says so. "Nothing keeps
itself" is a physical claim about substrates and must be staked as one. In the model, storage is the
*generic* case: the identity preserves the share exactly, and
`share_pushforward_percell_of_bijective` proves relabelling does too.

*Ground two — there is a real question under STORE, and it is not MAINTAIN.* It is **CAPACITY**:
how much a substrate can hold at all. Static, extremal, mathematically disjoint from every dynamical
question, and it is where this repository's strongest machine-checked results already live —
`ThirdCap.share_max_eq_log_two`, `HammingCap.shareK_le_of_four_pair_uniform`,
`BellCeiling.qShareK_max_five`. Folding it into MAINTAIN discards three `proved` claims into a verb
that does not contain them.

### The decomposition that survives, with their names preferred over ours

| verb | what it asks | **the name to use** | who owns it, and what they know |
|---|---|---|---|
| **CAPACITY** | how much can a substrate of given size hold | *maximum connected information*; equivalently *minimum entropy of d-wise-independent variables* | Lancaster 1965, Babai 2013, Gavinsky–Pudlák 2016; orthogonal-array form Hedayat–Sloane–Stufken 1999. Already adjudicated in `ShareK.lean`'s header — and the secret-sharing literature has an independent capacity theory for the same shape of question (§(c)2) |
| **MAKING** | what operations create it | **"created by local operations"** — the phrase is a paper title | Zhou, PRA 80, 022113 (2009); first measured instance Schneidman et al. 2003 Fig. 2. In the framework's vocabulary: *local operations are not RNG* |
| **MOVING** | how it flows between orders | *the correlation-order hierarchy under channels*; Amari's **orthogonal decomposition** | Amari 2001; Kahle–Olbrich–Jost–Ay 2009; Galla–Gühne 2012 |
| **READING** | what it takes to see it in data | *deviance of the no-three-factor-interaction model*; *exact conditional test*; *collapsibility* | Bartlett 1935, Birch 1963, Wilks 1938, Diaconis–Sturmfels 1998, Asmussen–Edwards 1983 — §(e) is mostly this |

**MAINTAIN is a sub-case of MAKING**, not a peer: a repair map is a map, and
`repair_mints_from_noise` is one application of one map. `Core/Creation.lean`'s header says the
dynamical version is proved nowhere. The one genuinely open piece under it is the *steady state*
(§(f) P4).

**READING is the verb the list was missing**, and it is the one with the deepest unexploited
literature — ninety-one years of it, with no trace anywhere in this tree.

---

## (b) THE RESOURCE-THEORY VERDICT — there is a theory, and the failure has a name

### What must hold

From Coecke, Fritz & Spekkens, *A mathematical theory of resources*, Inf. Comput. 250, 59 (2016)
(arXiv:1409.5531) and Chitambar & Gour, *Quantum resource theories*, Rev. Mod. Phys. 91, 025001
(2019) (arXiv:1806.06107): a set **F** of free states; a monoid **O** of free operations with
**O(F) ⊆ F**; and a monotone **M** vanishing on F and non-increasing under O. Convexity of F and a
tensor structure are the further properties that buy the *convex toolkit* and *asymptotic rates*
respectively.

### Our free set, named correctly

`F = {p : share p = 0}` is the closure of the pairwise-maxent exponential family — which is
**Bartlett's (1935) no-three-factor-interaction model**, cut out at k = 3 binary by the single
odds-ratio equation `p₁₁₁p₁₀₀p₀₁₀p₀₀₁ = p₀₀₀p₀₁₁p₁₀₁p₁₁₀`.

### The identity that decides the question

**`share(p) = min_{q ∈ F} D(p ‖ q)`.** This is Csiszár's I-projection duality / Amari's Pythagorean
theorem: for an exponential family the reverse-I-projection of `p` is the family member sharing `p`'s
sufficient statistics — here, its pair marginals — and the divergence to it equals the entropy gap.
Verified numerically against an independent six-parameter log-linear fit:

| state | `share` | `min_q D(p‖q)` | difference |
|---|---|---|---|
| `parity` | 0.693147181 | 0.693147181 | 0.0e+00 |
| `bulge` | 0.021185155 | 0.021185155 | 4.2e-16 |
| `ferro` | 0.000000000 | −0.000000000 | 2.8e-17 |
| 4 random states | — | — | ≤ 5.7e-16 |

**So the share is a relative entropy of resource, in the framework's exact sense.**

### The consequence: a monotone, automatically, under the maximal class

Chitambar & Gour: the **resource-non-generating (RNG)** operations, `O_max = {Λ : Λ(F) ⊆ F}`, are
*the maximal possible set of free operations in any non-trivial resource theory*. And for any
relative entropy of resource, monotonicity under `O_max` is three lines:

```
share(Λp) = min_{q∈F} D(Λp ‖ q)  ≤  D(Λp ‖ Λq*)  ≤  D(p ‖ q*)  =  share(p)
```

where `q*` is `p`'s minimiser and `Λq* ∈ F` by the RNG condition. It uses only the data-processing
inequality. **It does not use convexity.** So:

> **The whole-only share IS a resource monotone — under the resource-non-generating operations. The
> resource theory exists. The open question is not "is it a resource" but "how big is RNG".**

### What Zhou 2009 and `valve_upward` actually say, restated

In this vocabulary, `Core/Valve.lean`'s `valve_upward_strict` is a machine-checked proof that **the
γ = ½ amplitude-damping per-cell channel is not resource-non-generating for this free set** — it
carries `ferro ∈ F` to `bulge ∉ F`. That is a cleaner and more useful statement than "the valve
pumps", and it is the statement the literature already holds in general: D. L. Zhou, *"Irreducible
multiparty correlation can be created by local operations"*, **Phys. Rev. A 80, 022113 (2009)**:

> "…although the degree of the total correlation in a three-party quantum state does not increase
> under local operations, the irreducible three-party correlation can be created by local operations
> from a three-party state with only irreducible two-party correlations."

`PUMP_PRIOR_ART.md` already found and adjudicated this (leg L1), and
`PUMP_PRIOR_ART_ADDENDUM.md` pushed the first measured instance to Schneidman et al. 2003 Fig. 2.
Nothing here disturbs that record; it renames the finding in the framework's own terms and draws the
consequence the pump campaign did not.

The corresponding axiom is Bennett, Grudka, Horodecki, Horodecki & Horodecki, **PRA 83, 012312
(2011)**, Postulate 2: *"If an n-partite state does not have genuine n-partite correlations then
local operations and unanimous postselection … cannot generate genuine n-partite correlations."*
`ferro` has share exactly 0 and three damping kernels generate from it. **The share fails Postulate
2**, so it is not a measure of *genuine multipartite correlation* in the sense the community has
agreed on — and the page should stop reaching for that phrase. The measure that does satisfy the
postulates is Girolami, Tufarelli & Susa, PRL 119, 140505 (2017); adopt it if a genuine-multipartite
claim is ever wanted (§(e) A5).

### How big is RNG? Two facts, one of them striking

**RNG contains** slot permutations, per-slot bit flips (share exactly invariant,
`share_pushforward_percell_of_bijective`), per-slot freezes (share exactly zero), and every constant
map onto a free state — including the **completely depolarising** channel `p ↦ uniform`.

**RNG does not contain the depolarising semigroup's interior.** From the repository's own objects:

```
bulge  =  ½ · δ(false,false,false)  +  ½ · indep       (exact; verified to 0.0e+00)
```

Both endpoints are machine-checked free — `share_prod3` covers `δ(F,F,F)` (three deterministic cells)
and `indep` (`indep_eq_prod3`) — and `valve_upward` proves the midpoint resourceful. Checked away
from the boundary too, so it is not a point-mass artefact; mixing white noise 50/50 with a strictly
interior product state `(q,q,q)`:

| q | share(product) | share(½·product + ½·uniform) |
|---|---|---|
| 0.01 | 5.6e-17 | **1.709e-02** |
| 0.05 | 2.2e-16 | **7.028e-03** |
| 0.10 | 0.0e+00 | **2.100e-03** |
| 0.20 | 2.2e-16 | **1.137e-04** |
| 0.30 | 2.2e-16 | **1.908e-06** |
| 0.40 | 4.4e-16 | **1.817e-09** |

and two *different* interior product states `A = (0.05,0.05,0.05)`, `B = (0.9,0.8,0.7)` — both at
2.2e-16 — mix to **2.207e-02 / 1.267e-02 / 1.429e-03** at λ = 0.25 / 0.5 / 0.75.

> **Full depolarisation is free; partial depolarisation is not.** The canonical "weak noise is free"
> regime of every standard resource theory is absent here: RNG contains the identity and the
> completely depolarising channel but not the path between them. There is no gentle discarding — only
> exact preservation or complete destruction.

Structurally this is Amari's: **F is an exponential family, e-flat and not m-flat**, and mixing is an
m-geodesic, which leaves an e-flat family except degenerately. Every creation mechanism this
programme has measured — local channel, latent bit, coarse-graining — is *the same mechanism*, and it
is the one no convex resource theory can tolerate, because "forget which free state you hold" must be
free. It also explains rather than records `PUMP_RESULTS.md`'s own observation that the pump *is* a
convex combination (`|mixture − output| = 0.00e+00`).

### What the non-convexity costs, precisely

Not monotonicity — the three-line argument above needs none. What it costs is the **convex toolkit**:
convex-roof extensions, resource witnesses by convex duality, robustness and weight measures, and the
convexity axiom in Chitambar–Gour's own list. The frontier for free sets like ours is *Quantum
Resource Theories beyond Convexity*, **Quantum 10, 2104 (2026)**, which relaxes convexity to
**star-shapedness** and names quantum discord, total correlations and non-Markovianity as its
non-convex examples. **Our free set fails star-shapedness at the natural centre** — the identity above
*is* a segment from the uniform state to a free state leaving F. Worth reporting to that literature as
a further example; worth *not* claiming as a novelty until someone has checked whether the
pairwise-maxent family is already among their cases.

### `percell_no_creation`, honestly

It proves non-increase for **deterministic per-cell same-alphabet** maps, i.e. it exhibits a subset of
RNG. Two caveats the file's own header already flags, and which the framework sharpens: at a binary
alphabet the class is exactly relabellings-plus-freezes (invariance and zero — no conversion content);
and at three letters or more it contains coarse-grainings, which *create*, by the published mechanism
(Schneidman et al. 2003 Fig. 3; Macke, Opper & Bethge, **PRL 106, 208102 (2011)**). So it is not a
data-processing inequality in embryo — it is a corner of RNG, and the file is right to forbid citing
it as more.

---

## (c) THE FOUR PRIOR-ART LEGS — who found it, and what they know

### 1. Common information — Gács–Körner and Wyner. **They own the extraction question; adopt their names for it.**

Gács & Körner (*Probl. Contr. Inform. Theory* 2, 149 (1973)) own *how much common randomness can be
extracted* from correlated sources by separate deterministic functions. Wyner (*IEEE Trans. IT* 21,
163 (1975)) owns the dual — *how much must be supplied*: the minimum `I(X,Y;W)` over `W` rendering
the sources conditionally independent. Both are asymptotic rates over many copies, and both sit as
corner points of the Gray–Wyner region.

**Different object from ours, and the repository's own discriminator separates them in both
directions.** On `parity`, Gács–Körner common information is 0 (pairs are exactly independent) while
`share parity = log 2`. On `copied`, the triple's Wyner common information is one bit (take `W` = the
copied bit) while `share_copied = 0`, proved. The only true inequality is the elementary
`share ≤ multi-information`, which is exactly what the `share_copied` / `S_total_copied` pair shows.

**What they know that we do not, and it is the most consequential item in this section.** They have
the *operational* theory: what these numbers buy, in bits, in a named task, with converse bounds. Our
share has no such interpretation — which is precisely why §(b) finds its free-operation class hard to
pin down; the operational content that would supply one was never there. **If this programme ever
wants the share to mean something operational, that is the literature to enter, and the honest first
move is to ask whether the share is already a corner point of some Gray–Wyner-like region.**

*Credit paragraph.* *The formal theory of how much shared structure can be extracted from, or must be
supplied to, correlated sources is Gács & Körner (1973) and Wyner (1975), placed as corner points of
the Gray–Wyner region. The whole-only share is a different object — a single-shot divergence to a
model family rather than an asymptotic rate — and the two are separated in both directions by states
this repository already carries.*

### 2. Data hiding and secret sharing. **Our exhibited state is theirs, and their capacity theory is worth taking.**

`parity` — three bits, uniform on the even-parity words — **is** the 3-party XOR secret-sharing
scheme. `pairwise_blind_to_parity` is its perfect-security condition; `third_sees_parity` is its
correctness condition. Together they are the definition of a perfect `(n,n)` threshold scheme.

*Credit paragraph.* *That structure can be arranged to be invisible to every proper subset of the
parties while determined by the whole is the founding construction of secret sharing — Blakley,
AFIPS 48, 313 (1979) and Shamir, CACM 22, 612 (1979), with the XOR `(n,n)` scheme folklore and
general access structures in Ito, Saito & Nishizeki (1987); the partial-leakage family is the ramp
schemes of Blakley & Meadows (1985). The quantum strengthening to LOCC-restricted parties is quantum
data hiding — Terhal, DiVincenzo & Leung, PRL 86, 5807 (2001); DiVincenzo, Leung & Terhal, IEEE
Trans. IT 48, 580 (2002). This repository's `parity` state is the three-party instance and its
pairwise blindness is that literature's security property.*

**Is our share one of their measures? No — and the mismatch is diagnostic.** Hiding is measured
*operationally against a restricted adversary*: `‖ρ₀ − ρ₁‖_LOCC` quantumly, leakage `I(S ; subset)`
classically. Both answer "what can this adversary learn". The share has no adversary in it. Same
diagnosis as leg 1, from a second direction.

**What they know that we do not.** A full capacity theory for the CAPACITY verb: share-size lower
bounds (Karnin–Greene–Hellman 1983 — every share is at least as large as the secret), information
rates for general access structures, and the ramp trade-off between leakage and share size. If
CAPACITY is pursued, that is a ready-made set of extremal results about the same shape of question.

### 3. Multipartite correlation and what local operations cannot create. **The cleanest sentence available, and it is theirs.**

| statement | source |
|---|---|
| LOCC cannot create entanglement | Bennett, DiVincenzo, Smolin & Wootters, PRA 54, 3824 (1996); monotone framework Vidal, J. Mod. Opt. 47, 355 (2000) |
| local operations cannot increase **total** correlation | strong subadditivity; stated as the contrasting fact in Zhou 2009 |
| local operations **can** create **irreducible three-party** correlation | **Zhou, PRA 80, 022113 (2009)** |
| the postulate this violates | Bennett–Grudka–Horodecki–Horodecki–Horodecki, PRA 83, 012312 (2011), Postulate 2 |

**The sentence to use:** *the share is the top term of the decomposition of a monotone, and is not
itself a monotone under the operations that make the total one.* Total correlation is monotone under
product channels — `TC = D(p ‖ ⊗pᵢ)`, and a product channel carries `⊗pᵢ` to the output's own
marginals, so data processing applies. Decomposing a monotone by order does not give monotones.

*Credit paragraph.* *That local operations cannot create entanglement is the foundational fact of
entanglement theory (Bennett–DiVincenzo–Smolin–Wootters 1996; Vidal 2000), and that they cannot
increase total correlation follows from strong subadditivity. Zhou (2009) proved in the same breath
that the irreducible three-party correlation is not so protected and can be created by local
operations from a state carrying only two-party correlation — exactly `Core/Valve.lean`'s
`valve_upward`, in greater generality and seventeen years earlier. The postulate set our quantity
thereby fails is Bennett, Grudka, Horodecki, Horodecki & Horodecki (2011).*

### 4. Amari, and the statistics of exactly our object. **The largest hit, and it is ninety-one years old.**

Amari (*IEEE Trans. IT* 47, 1701 (2001)) owns the hierarchy, the e-/m-projections, the orthogonality
of the decomposition, and the e-flatness that makes §(b) work. He belongs in `Core/Share.lean`'s
header beside Schneidman 2003 and Zhou 2008.

**And the classical statistics of the k = 3 binary case is older and entirely absent from this tree.**
A grep of all of `scratchpad/` for `Bartlett|contingency|collapsib|log-linear|Birch|Darroch|Deming|
Csisz` returns only incidental uses of "log-linear" meaning "fit on log axes".

- **Bartlett, "Contingency table interactions", Suppl. JRSS 2, 248–252 (1935)** — the
  no-three-factor-interaction model on a 2×2×2 table. **Our free set is Bartlett's null model.**
  `2N · share` is its likelihood-ratio deviance `G²`.
- **Birch, JRSS B 25, 220 (1963)** — the MLE is the unique exponential-family member matching the
  observed two-way margins. **That is `pairEnvelope`'s maximiser, existence and uniqueness proved in
  1963.** (Also Darroch 1962; Plackett 1962; Roy & Kastenbaum 1956.)
- **Deming & Stephan (1940)** — IPF, the algorithm `shareK` uses; **Csiszár, Ann. Probab. 3, 146
  (1975)** — its convergence as an I-projection, and the Pythagorean identity §(b) turns on.
  [[ipf-sharek-boundary-drift]] is a rediscovery of known IPF boundary behaviour.
- **Wilks (1938)** — at k = 3 binary the saturated model has 7 free parameters and Bartlett's has 6,
  so **df = 1** and `G² → χ²₁`. `PUMP_RESULTS.md` §6's measured `bias × N ≈ 0.22` against
  `median(χ²₁)/2 = 0.2275` is that theorem confirming itself.
- **Collapsibility** is the name for the coarse-graining question: Whittemore, JRSS B 40, 328 (1978);
  Bishop, Fienberg & Holland (1975); **Asmussen & Edwards, Biometrika 70, 567 (1983)** — necessary
  *and sufficient* conditions in terms of the generating class.

*Credit paragraph.* *The order-3 whole-only share of three binary variables is, up to the factor
`2N`, the likelihood-ratio deviance of Bartlett's no-three-factor-interaction model (1935), whose
maximum-likelihood fit is Birch's (1963) unique exponential-family member matching the two-way
margins, computed by Deming–Stephan (1940) iterative proportional fitting, whose convergence as an
I-projection is Csiszár's (1975), with the null distribution given by Wilks (1938) and the behaviour
under marginalisation by Whittemore (1978) and Asmussen & Edwards (1983). The information-geometric
form of the hierarchy is Amari (2001); the information-theoretic naming as connected information is
Schneidman, Still, Berry & Bialek (2003); the quantum lift is Zhou (2008).*

---

## (d) WHAT THIS PROGRAMME CONTRIBUTES

Short, and it stands on its own.

**1. The mechanization.** The Lean proofs — the k = 3 cap with no hypothesis
(`ThirdCap.share_max_eq_log_two`), the three valve directions, the sign-symmetry vanishing, the
minting theorems, the quantum ceiling — appear to have no machine-checked counterpart anywhere. That
is a contribution of kind, it is what the stance already claims, and it does not need the mathematics
to be new. Reading `valve_upward` as "damping is not RNG, machine-checked" makes it *more* valuable,
not less: a formally verified instance of a general theorem the literature states without a proof
assistant.

**2. The asymmetry-resolved rate law.** PUMP's L4, verdict CLEAR and unchanged: the closed form in
`(a, s, ρ)`, its exponent, its theorem-pinned zero, its k-scaling, its two measured domain limits and
its hardware overlay.

**3. One small corollary, worth a note and not a campaign.** That the obstruction is the *free set*
rather than the operations; that `bulge = ½·δ_FFF + ½·indep` is a two-point witness with
machine-checked endpoints; that full depolarisation is free while partial depolarisation is not; and
that this defeats star-shapedness at the natural centre. *Assume this is convergent too* — the
underlying fact is Schneidman 2003 Fig. 3 / Kahle et al. 2009 / Macke et al. 2011, and Quantum 10,
2104 (2026) may already list this family. Check before claiming.

**And the open question the whole programme still owns:** which of nature's wild processes carry
whole-only share. Nothing in this document touches it, and nothing here substitutes for it.

---

## (e) WHAT TO ADOPT — the section Eric asked for

Ranked by what it would have saved us, and by what it changes about the next campaign.

### A1. The standard repair when a candidate monotone increases. **Chitambar & Gour; Liu–Hu–Lloyd.**

This is the direct answer to Eric's question, and it is a two-step recipe the community has had for
years:

1. **Switch to the maximal set.** When the physically-motivated operations fail, you do not abandon
   the theory — you replace them with `RNG = {Λ : Λ(F) ⊆ F}`, *the maximal possible free-operation
   set in any non-trivial resource theory*, under which any relative entropy of resource is
   automatically monotone. The physically-motivated class is then studied as a *strict subset*, and
   the gap between them becomes the object. This is exactly how entanglement theory handles LOCC
   versus separable versus PPT operations: the physical class, a tractable superset, and a research
   programme in the gap. **A candidate monotone failing under the natural operations is a normal
   event with a standard response, not a disqualification.** That lesson alone would have changed how
   this document's first version was written.
2. **Characterize the free operations via the resource-destroying map.** Liu, Hu & Lloyd, *Resource
   Destroying Maps*, **PRL 118, 060502 (2017)** (arXiv:1606.03723): a map `λ` that "leave[s]
   resource-free states unchanged but erase[s] the resource stored in all other states". **Our `π₂`
   — the pairwise-maxent projection — is exactly such a map.** They give conditions determining
   whether an operation "exhibits typical resource-free properties" relative to `λ`, and define *a
   class of simple resource measures that can be calculated without optimization, and that are
   monotone nonincreasing under operations that commute with the resource destroying map.*

   **Two things this hands us directly.** (i) A computable handle on the free operations: "commutes
   with `π₂`" is checkable, and is a far better starting point than searching the stochastic simplex.
   (ii) A lead on an **optimization-free estimator** — our estimator solves a variational problem per
   reading, and the finite-N bias of that optimization is what [[share-null-is-chi2-shaped]] and PUMP
   §6 are about. **Caveat to read for first: `π₂` is non-linear, whereas their worked example
   (dephasing, for coherence) is a channel. Whether their theorems survive a non-linear `λ` is the
   first thing to check.**

### A2. The exact conditional null. **Diaconis & Sturmfels (1998) — the biggest single adopt.**

This programme's recurring difficulty is nulls: [[share-null-is-chi2-shaped]],
[[signsym-chi2-overrejects]], [[whole-only-null-autocorrelation]], [[mixture-null-vs-dose-disagree]],
[[resample-null-shot-noise-double-count]]. Every one is an attempt to build, by resampling, a null
distribution for a statistic whose exact conditional null **has a published sampler.**

Diaconis & Sturmfels, *Algebraic algorithms for sampling from conditional distributions*, **Ann.
Statist. 26, 363 (1998)**, give **Markov bases**: a set of moves connecting every contingency table
sharing the observed margins, so an MCMC walk samples uniformly from *exactly* the reference set the
share is defined against — all tables with the observed two-way marginals. The Markov basis for the
no-three-way-interaction model is known and tabulated (Aoki, Hara & Takemura, *Markov Bases in
Algebraic Statistics*, Springer 2012).

> **The correct null for a share measurement is the uniform distribution over tables with the
> observed two-way margins, and it can be sampled exactly rather than approximated by shuffling.**

Conditionally exact: no asymptotics, no tie corrections, no estimator-bias floor to subtract, and
immune to the autocorrelation and shot-noise pathologies that have bitten four campaigns. This should
become the house null for any k = 3 share measurement, with the existing resampling floors
re-derived against it as a gate.

### A3. When `χ²₁` is not valid. **Haberman (1977); Koehler & Larntz (1980).**

The `0.227/N` floor is Wilks, and Wilks has conditions. The sparse-table literature knows exactly when
`G²` stops being χ²-distributed — small and variable expected cell counts, where Pearson's statistic
can be *asymptotically inconsistent* even where a χ² approximation exists for the null. **This is the
occupancy problem by its proper name** ([[occupancy-must-be-measured]],
[[eboss-measured-insufficient]]). The literature's recommendation is the same as A2: when the table is
sparse, use the exact conditional test rather than the asymptotic one. Adopting A2 and A3 together
retires a whole class of this programme's floor arguments.

### A4. Collapsibility as the lumpability gate. **Asmussen & Edwards (1983).**

`PUMP_RESULTS.md` §7 handed the glass and water campaigns the condition "the pump law transfers
across a binarization iff the binarization is lumpable", and left them to test it. **Necessary and
sufficient conditions for a hierarchical log-linear model to be collapsible onto a margin are stated
in terms of the generating class** and have been since 1983 (Whittemore 1978 correcting
Bishop–Fienberg–Holland 1975, with later extensions). Those campaigns should check the condition
algebraically instead of measuring it.

### A5. The measure that does satisfy the postulates. **Girolami, Tufarelli & Susa (2017).**

If this programme ever wants to make a *genuine multipartite correlation* claim rather than a
whole-only-share claim, quote PRL 119, 140505 (2017) — built to satisfy the Bennett et al. postulates
— rather than stretching the share into a role it provably cannot fill.

### A6. Report the whole hierarchy, not just order 3. **Amari (2001).**

The decomposition is *orthogonal*: the order-k connected informations sum to the multi-information
exactly, and each is individually meaningful. This programme reads order 3 and discards the rest.
`PUMP_RESULTS.md` §2's own discovery — that at k ≥ 4 the *even* pair-blind directions survive sign
symmetry while the odd ones vanish, so `share_eq_zero_of_signSymmetric` is an accident of three — is a
fact about the hierarchy that would have been visible from the start had the full decomposition been
reported. Adopt the habit.

### A7. The vocabulary, everywhere.

Prefer *no-three-factor-interaction model* over "the free set"; *deviance* over "the share statistic";
*collapsible* over "lumpable"; *resource-non-generating* over "operations that cannot mint";
*I-projection* over "the maxent competitor"; *connected information* over "whole-only share" wherever
addressing anyone outside this repository. Their terms are better tested and make our results
findable.

---

## (f) THE NEXT CAMPAIGN

**Do not build the four-verb programme.** HIDE is the definition, MAINTAIN is a case of MAKING, and of
the two that remain CAPACITY is largely done and MAKING is owned by Zhou 2009 with our own PUMP
campaign supplying the quantitative layer.

**P1 — Adoptions and namings owed now. A morning, no proofs touched.**
1. `Core/Share.lean` header — add **Amari 2001**, and **Bartlett 1935 / Birch 1963** as the
   classical-statistics identity of the k = 3 binary case.
2. `Core/Valve.lean` — restate `valve_upward` in the framework's vocabulary ("damping is not
   resource-non-generating") alongside the existing wording, and complete the credit paragraph as
   `PUMP_RESULTS.md` §9 already directs.
3. `PUMP_RESULTS.md` §6 — the `0.227/N` floor is **Wilks (1938)**, df = 1. §7 — lumpability is
   **collapsibility**, with an Asmussen–Edwards (1983) necessary-and-sufficient answer.

**P2 — The exact null. The highest-value item in this document, and it is an adoption, not a
discovery.** Build the Diaconis–Sturmfels Markov-basis sampler for the no-three-way-interaction model
at k = 3 binary, gate it against the existing resampling floors, and make it the house null. Expected
outcome: several measured floors move, and the χ²/permutation apparatus in four campaigns is replaced
by one conditionally exact test. **Kill:** the sampler disagrees with the gated χ²₁ floor at N where
the asymptotics should hold — which would mean the implementation is wrong, not the theory.

**P3 — Characterize RNG, using A1's recipe rather than brute force.** How big is the free-operation
class? Start from Liu–Hu–Lloyd's "commutes with the resource-destroying map" with `λ = π₂`, checking
first whether their theorems survive `λ` being non-linear. Fall back to the direct algebraic question
— the stabiliser of the degree-4 hypersurface under column-stochastic matrices — only if that fails.
**Search algebraic statistics first** (Drton–Sturmfels–Sullivant; Markov bases for this model are
already published); assume convergence. A negative answer ("only the obvious symmetries plus the
constants") closes the question permanently and is worth as much as a positive one.

**P4 — The one dynamical question the four verbs contained that is genuinely open.** The steady state
of repair against noise: iterate a code projection alternating with a per-cell channel and ask what
the stationary share is. `Core/Creation.lean`'s header says the dynamical version is proved nowhere,
and the rent clause is about a scalar recursion, not about `share`. Tractable with the gated exact
solver; composes with the PUMP closed form. **Prior-art gate before any measurement:** probabilistic
cellular automata with error correction (Toom, Gács), nonequilibrium steady states of error-correcting
dynamics, and the maximum-entropy neural literature on maintained higher-order structure.

**P5 — And the standing one.** `wild-share` is the stance's only `open` claim, its named next
instrument is DESI BGS, and none of the above is a substitute for pointing an instrument at the sky.

---

## Sources

- [Coecke, Fritz & Spekkens, *A mathematical theory of resources*, arXiv:1409.5531](https://arxiv.org/abs/1409.5531)
- [Chitambar & Gour, *Quantum resource theories*, Rev. Mod. Phys. 91, 025001 (2019), arXiv:1806.06107](https://arxiv.org/pdf/1806.06107)
- [Liu, Hu & Lloyd, *Resource Destroying Maps*, PRL 118, 060502 (2017), arXiv:1606.03723](https://arxiv.org/abs/1606.03723)
- [Zhou, *Irreducible multiparty correlation can be created by local operations*, PRA 80, 022113 (2009), arXiv:0904.1863](https://arxiv.org/abs/0904.1863)
- [Bennett, Grudka, Horodecki, Horodecki & Horodecki, *Postulates for measures of genuine multipartite correlations*, PRA 83, 012312 (2011), arXiv:0805.3060](https://arxiv.org/abs/0805.3060)
- [*Quantum Resource Theories beyond Convexity*, Quantum 10, 2104 (2026)](https://quantum-journal.org/papers/q-2026-05-13-2104/)
- [Macke, Opper & Bethge, *Common input explains higher-order correlations and entropy…*, PRL 106, 208102 (2011), arXiv:1009.2855](https://arxiv.org/abs/1009.2855)
- [Amari, *Information geometry on hierarchy of probability distributions*, IEEE Trans. IT 47, 1701 (2001)](https://people.csail.mit.edu/jrennie/trg/papers/amari-ig-hierarchy-01.pdf)
- [Diaconis & Sturmfels, *Algebraic algorithms for sampling from conditional distributions*, Ann. Statist. 26, 363 (1998) — Markov basis survey](https://arxiv.org/pdf/1907.07320)
- [Aoki, Hara & Takemura, *Markov Bases in Algebraic Statistics*, Springer (2012)](https://link.springer.com/book/10.1007/978-1-4614-3719-2)
- [Whittemore, *Collapsibility of multidimensional contingency tables*, JRSS B 40, 328 (1978)](https://academic.oup.com/jrsssb/article/40/3/328/7027572)
- [Asmussen & Edwards, *Collapsibility and response variables in contingency tables*, Biometrika 70, 567 (1983)](https://academic.oup.com/biomet/article-abstract/70/3/567/247512)
- [Birch, *Maximum likelihood in three-way contingency tables*, JRSS B 25, 220 (1963)](https://academic.oup.com/jrsssb/article/25/1/220/7035241)
- [Darroch, *Interactions in multi-factor contingency tables*, JRSS B 24, 251 (1962)](https://rss.onlinelibrary.wiley.com/doi/abs/10.1111/j.2517-6161.1962.tb00457.x)
- [García-Pérez & Núñez-Antón, *Asymptotic versus exact methods in contingency tables*, Stat. Methods Med. Res. (2020)](https://journals.sagepub.com/doi/10.1177/0962280220902480)
- [DiVincenzo, Leung & Terhal, *Quantum data hiding*, IEEE Trans. IT 48, 580 (2002)](https://ui.adsabs.harvard.edu/abs/2001quant.ph..3098D/abstract)
- [Girolami, Tufarelli & Susa, *Quantifying genuine multipartite correlations and their pattern complexity*, PRL 119, 140505 (2017)](https://www.researchgate.net/publication/317590964_Quantifying_Genuine_Multipartite_Correlations_and_their_Pattern_Complexity)

**Numerical checks** are in
`/tmp/claude-1000/-home-emoore-CIRISOntology/4cf4fa5c-aaa3-4173-83b9-978cb75c887f/scratchpad/`:
`conv.py` (the mixture identity), `conv2.py` (interior-point convexity failure), `relent.py`
(`share = min_q D(p‖q)` against an independent six-parameter log-linear fit). All use the exact 1-D
`p + t·χ` solver, the parametrization `Core/Valve.lean`'s header records; they reproduce
`share bulge = 0.021185` against `valve_upward_bound = 0.011962`.
