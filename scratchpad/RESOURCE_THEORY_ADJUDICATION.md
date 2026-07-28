# Resource-theory adjudication — is the whole-only share a resource, and are the four verbs the right four?

**Asked by:** the coordinator's four-verb proposal (STORE / MINT / MAINTAIN / HIDE) and Eric's
immediate question — are those the right verbs, and what is the prior art?
**Answered by:** the resource-theory agent, 2026-07-27. No Lean run, no `lake`, no stance touched.
**Method:** read the repository's own formal core first (`Core/{Share,ShareK,ThirdCap,SignSymmetry,
Creation,Valve,Maintenance}.lean`, `scratchpad/PUMP_RESULTS.md`, `scratchpad/PUMP_PRIOR_ART{,_ADDENDUM}.md`),
then six object-directed literature sweeps, then two exact numerical checks against the repository's
own instrument.

**One-line verdict.** **The whole-only share is not a resource in the technical sense, it cannot be
made into one by any interesting choice of free operations, and the reason is structural rather than
incidental: its free set is not convex — a fifty-fifty mixture of two of this repository's own
machine-checked zero-share states has machine-checked positive share, and one of the two is white
noise.** The non-monotonicity itself is published (Zhou 2009, whose title is the finding); the
structural obstruction and its two-point witness appear not to be, and are the only genuinely new
thing in this document.

---

## 0. What had to be established first, and what it costs the verb list

Three facts from the repository, quoted precisely because everything below turns on them:

| fact | where | exact statement |
|---|---|---|
| the quantity | `Core/Share.lean` | `share p = sSup (pairEnvelope p) − entropy p`: the entropy gap from `p` to the maximum-entropy state carrying all of `p`'s two-slot marginals |
| local **stochastic** channels **raise** it | `Core/Valve.lean` `valve_upward_strict` | `share ferro < share (channel3 damp damp damp ferro)`, machine-checked, strict |
| local **deterministic** same-alphabet maps do **not** | `Core/Creation.lean` `percell_no_creation` | `share (pushforward (percell f g h) p) ≤ share p` |

The second of those is, on its own, the answer to the central question. A resource theory needs free
operations that do not increase the resource. The obvious candidate class — per-cell channels — is a
perfectly good monoid (closed under composition, contains the identity), and it strictly increases
the quantity on a state this repository has already exhibited. That is not a near-miss; it is a
counterexample with a Lean proof behind it.

---

## (a) THE VERB QUESTION

### Ruling on the coordinator's two pre-search claims

**Claim 1 — "HIDE is an adversarial verb presuming an agent and does not belong beside three
dynamical ones." VERDICT: the conclusion is right, the reason is wrong, and the right reason is
stronger.**

Hide should be struck, but not because it presumes an agent. It should be struck because **it is the
definiens, not a verb.** "Invisible to every pair" is not something the share *does*; it is what the
share *is*. `SamePairs` is the constraint set of the variational problem, `pairwise_blind_to_parity`
is the exhibited instance, and `share_copied = 0` versus `S_total_copied = log 2` is the repository's
own proof that this is the defining property and not an incidental one. A decomposition in which one
entry restates the definition of the object being decomposed is a category error, and it would have
produced a campaign that could only rediscover `Core/Share.lean`.

The agential reading is not empty — it has a name and a literature (§(c)2) — but there it is a
property of a *scheme* someone designs, not a process a system undergoes. It belongs to engineering,
not to the dynamics.

**Claim 2 — "STORE collapses into MAINTAIN under `unpaid_decays` (nothing keeps itself, so there is
no passive storage)." VERDICT: rejected, on two independent grounds.**

*Ground one — the inference is the laundering `epistemology.md` forbids.* `unpaid_decays` is a
theorem about `Core/Maintenance.lean`'s scalar recursion `S ↦ (1−γ)S + α`, with `0 < γ` as an
explicit hypothesis. It says nothing about `share`, and there is no theorem anywhere in this
repository connecting a decay rate to any share dynamics. That file's own SCOPE paragraph says so:
*"Nothing here asserts that any real system obeys this model."* "Nothing keeps itself" is a physical
claim about substrates — a Landauer/error-correction claim — and it must be argued and staked as one.
As a matter of the mathematics, the identity channel preserves the share exactly, and
`share_pushforward_percell_of_bijective` proves relabelling preserves it exactly. Passive storage is
not merely possible in the model; it is the *generic* case, and the decay is an added hypothesis.

*Ground two — and this matters more — there is a real question under "store", and it is not
"maintain".* It is **capacity**: how much a substrate can hold at all. That is a static, extremal
question, mathematically disjoint from every dynamical one, and it is where this repository's
strongest machine-checked results already live —

- `ThirdCap.share_max_eq_log_two` — exactly `log 2` on three binary slots, no hypothesis;
- `HammingCap.shareK_le_of_four_pair_uniform` — `(k−3)·log 2` from four pair-uniform slots up;
- `BellCeiling.qShareK_max_five` — the C5 ring state's `5·log 2`, above the classical cap.

Folding "store" into "maintain" discards three of the stance's thirteen `proved` claims into a verb
that does not contain them. The correct move is to rename, not to merge.

### The decomposition that survives, in the literature's vocabulary where one exists

| verb | what it asks | the literature's own word | who owns it |
|---|---|---|---|
| **CAPACITY** | how much can a substrate of given size hold | *maximum connected information*; equivalently *minimum entropy of d-wise-independent variables* | Lancaster 1965, Babai 2013, **Gavinsky–Pudlák 2016**; orthogonal-array form Hedayat–Sloane–Stufken 1999. Already adjudicated in `ShareK.lean`'s header |
| **MAKING** | what operations create it | **"created by local operations"** — the phrase is the title of the paper | **Zhou, PRA 80, 022113 (2009)**; the first measured instance is Schneidman et al. 2003 Fig. 2 |
| **MOVING** | how it flows between orders | *correlation-order hierarchy under channels* | Amari 2001; Kahle–Olbrich–Jost–Ay 2009; Galla–Gühne 2012 |
| **READING** | what it takes to see it in data | *deviance of the no-three-factor-interaction model*; *collapsibility* | **Bartlett 1935**, Birch 1963, Wilks 1938, Asmussen–Edwards 1983 — §(c)4 |

**MAINTAIN is not a peer verb; it is a sub-case of MAKING.** A repair map is a map, and
`repair_mints_from_noise` is one application of one map — `Core/Creation.lean`'s own header says the
dynamical version "is NOT proved anywhere". The one thing under "maintain" that would be genuinely
new is the *steady state*: the stationary share of a chain alternating repair against noise. That is a
legitimate open piece (§(e)), and it is the only part of the coordinator's four that survives as a
question rather than as a restatement.

**READING is the verb the list was missing**, and on this campaign's record — five convergent-art
strikes out of five findable results — it is also the one where the programme's actual output has
been. It is also, per §(c)4, the verb with the oldest and least-searched prior art in this
repository.

---

## (b) THE RESOURCE-THEORY VERDICT

### What must hold

From Coecke, Fritz & Spekkens, *A mathematical theory of resources*, Inf. Comput. 250, 59 (2016)
(arXiv:1409.5531), and Chitambar & Gour, *Quantum resource theories*, Rev. Mod. Phys. 91, 025001
(2019) (arXiv:1806.06107), a resource theory is:

1. a set **F** of *free states*;
2. a set **O** of *free operations* forming a monoid — closed under composition, containing the
   identity — and satisfying **O(F) ⊆ F** (a free operation cannot leave the free set);
3. a *monotone* **M** with `M = 0` on F and `M(Λρ) ≤ M(ρ)` for every `Λ ∈ O`.

Two further properties are not optional decorations, they are what makes the theory *do* anything:
**convexity of F** (so that forgetting which free state you hold is itself free — otherwise the
theory has a source it cannot account for), and a compositional/tensor structure, without which
*asymptotic conversion rates* — the question CFS is built to ask — cannot even be posed. Fritz's
ordered-commutative-monoid programme (arXiv:1504.03661) is precisely the machinery for rates, and it
presupposes both.

### Test 1 — per-cell channels as free operations: **FAILS, and the failure is machine-checked here**

`Core/Valve.lean`'s `valve_upward_strict` gives `share ferro < share (channel3 damp damp damp ferro)`.
`ferro` is free (`share_ferro = 0`); its image `bulge` is not. So per-cell channels violate both
requirement 2 (**O(F) ⊄ F**) and requirement 3 (**M is not monotone**).

**State the consequence plainly, because it is the sharpest thing available: under local operations
the whole-only share is not a monotone, and the quantity is therefore not a resource in the CFS /
Chitambar–Gour sense.**

And state the credit just as plainly: **this is not ours.** D. L. Zhou, *"Irreducible multiparty
correlation can be created by local operations"*, **Phys. Rev. A 80, 022113 (2009)**
(arXiv:0904.1863), abstract:

> "…although the degree of the total correlation in a three-party quantum state does not increase
> under local operations, the irreducible three-party correlation can be created by local operations
> from a three-party state with only irreducible two-party correlations."

That is `valve_upward` and `valve_no_downward` together, on the same object, seventeen years earlier
and in the quantum generality. `PUMP_PRIOR_ART.md` already found and adjudicated it (leg L1,
**SCOOPED**), and `PUMP_PRIOR_ART_ADDENDUM.md` pushed the first measured instance back further to
Schneidman, Still, Berry & Bialek, PRL 91, 238701 (2003), Fig. 2. Nothing here disturbs that record;
this document only names the framework-level consequence the pump campaign did not draw.

### Test 2 — the community's own axiom list: **the share fails Postulate 2**

Bennett, Grudka, Horodecki, Horodecki & Horodecki, *"Postulates for measures of genuine multipartite
correlations"*, **Phys. Rev. A 83, 012312 (2011)** (arXiv:0805.3060), state three postulates that any
measure of genuine n-partite correlations should satisfy. Postulate 2, verbatim:

> "If an n-partite state does not have genuine n-partite correlations then local operations and
> unanimous postselection … cannot generate genuine n-partite correlations."

`ferro` has no genuine three-partite correlations *by our own measure* (`share_ferro = 0`), and three
per-cell damping kernels — local operations, no postselection at all — generate them. **The whole-only
share violates Postulate 2 of the standard postulate set for measures of genuine multipartite
correlation.** The paper uses the same postulate to disqualify covariance as an indicator. This is
worth carrying on the page's face rather than in a footnote: it does not make the quantity wrong, but
it does mean the quantity is *not* a measure of genuine multipartite correlation in the sense the
literature has agreed on, and the stance should not lean on the phrase.

### Test 3 — the structural reason, and the part that appears not to be in print

Non-monotonicity under one candidate class would leave open the question the brief asks: *is there
some other class that works?* The answer is no, and the obstruction is one level deeper than the
operations.

**The free set is not convex.** Take the repository's own objects:

```
bulge = ½ · δ(false,false,false)  +  ½ · indep
```

— an exact eight-cell identity (`9/16 = ½·1 + ½·⅛`, `1/16 = ½·0 + ½·⅛`; verified to 0.0e+00). Both
endpoints have share **exactly zero**, and both are covered by `Core/Valve.lean`'s `share_prod3`:
`δ(F,F,F)` is `prod3` of three deterministic cells, `indep` is `prod3 unifBool unifBool unifBool`
(`indep_eq_prod3`). And `share bulge > 0` is `valve_upward`, with `valve_upward_bound` giving
`≥ 0.011962` and the campaign's gated solver reading `0.021185`.

> **A fifty-fifty mixture of two machine-checked free states is machine-checked resourceful — and one
> of the two is white noise. Adding white noise to a free state creates the resource.**

Depolarizing is free in essentially every resource theory in the literature. Here it is a *source*.

**Not merely non-convex — not star-shaped either.** The recent generalization that relaxes convexity
(*Quantum Resource Theories beyond Convexity*, Quantum 10, 2104 (2026)) requires only that F be
star-shaped: some centre `c ∈ F` with the whole segment from `c` to any free state inside F. The
natural centre is the uniform state. The identity above is exactly a segment from the uniform state to
a free state leaving F, so **the uniform centre fails.** Checked away from the boundary as well, so it
is not an artefact of using a point mass — mixing white noise 50/50 with a strictly interior product
state `(q,q,q)`:

| q | share(product) | share(½·product + ½·uniform) |
|---|---|---|
| 0.01 | 5.6e-17 | **1.709e-02** |
| 0.05 | 2.2e-16 | **7.028e-03** |
| 0.10 | 0.0e+00 | **2.100e-03** |
| 0.20 | 2.2e-16 | **1.137e-04** |
| 0.30 | 2.2e-16 | **1.908e-06** |
| 0.40 | 4.4e-16 | **1.817e-09** |

and two *different* strictly-interior product states, `A = (0.05,0.05,0.05)`, `B = (0.9,0.8,0.7)`,
both share 2.2e-16, mix to **2.207e-02 / 1.267e-02 / 1.429e-03** at λ = 0.25 / 0.5 / 0.75.

The information-geometric statement of the same fact, which is Amari's and is why it could have been
predicted rather than discovered: **the free set is the pairwise exponential family — e-flat, not
m-flat.** Mixing is an m-geodesic. An m-geodesic between two points of an e-flat family leaves that
family except in degenerate cases. So every mechanism the pump campaign measured — the local channel
(a mixture), the latent bit (a mixture), the coarse-graining (a mixture) — is *the same mechanism*,
and it is the one mechanism no resource theory can tolerate, because "forget which free state you
hold" must be free.

This also explains, rather than merely records, `PUMP_RESULTS.md`'s own observation that "the pump is
a convex combination" (`|mixture − output| = 0.00e+00`): that is not a curiosity of the damping
kernel, it is the whole of why the valve exists.

### Test 4 — what operation class *would* make it a monotone, and is that class a gerrymander

`percell_no_creation` proves non-increase for **deterministic per-cell same-alphabet** maps. Two
things must be said about that class, and both are unflattering.

**It is degenerate at binary alphabets.** The proof runs on the dichotomy "every `Bool → Bool` is a
bijection or a constant". On bijections the share is *exactly invariant*
(`share_pushforward_percell_of_bijective`); on constants it is *exactly zero*. So the class is a
finite group of relabellings, plus absorbing maps. The induced preorder is "`p ≥ q` iff `q` is a
relabelling of `p`, or `share q = 0`" — no rates, no catalysis, no non-trivial interconversion, no
content. It satisfies the letter of requirement 3 and nothing of its purpose.

**It dissolves the moment the alphabet grows.** On three letters or more the deterministic per-cell
class contains coarse-grainings, and a coarse-graining is a marginalization of the within-block
label — which is *the published creation mechanism*: Schneidman et al. 2003 Fig. 3 (the hidden-bit
family, abscissa `γ = P(σ₄=0)`), and Macke, Opper & Bethge, **PRL 106, 208102 (2011)**, *"Common
input explains higher-order correlations and entropy in a simple model of neural population
activity"* — a latent common input generating apparent higher-order structure from pairwise inputs.
`Core/Valve.lean`'s header already flags the coarse-graining gap as open in both directions; the
literature's expected answer is *creates*, and the honest reading of `percell_no_creation` is that it
is **an artefact of the two-letter dichotomy, not a data-processing inequality in embryo.** The file
already forbids citing it as one. This is the reason why.

A resource theory whose free operations exclude coarse-graining is not merely unusual — it is
backwards. Coarse-graining is free in thermodynamics, in entanglement theory, in coherence theory, in
every theory built on a data-processing inequality. Excluding it is the tell that no such theory is
there.

### The verdict, stated once

**The whole-only share is a divergence, not a resource.** Precisely: it is a relative entropy to a
model family, `share p = D(p ‖ π₂(p))` where `π₂` is the m-projection onto the pairwise exponential
family — mathematically the same shape as the relative entropy of non-Gaussianity, except that there
the free family *is* closed under the natural free operations and here it provably is not. It has a
cap, an attainment, a rate law and an estimator. It does not have, and cannot be given, an ordering
under a non-trivial free-operation monoid.

The cleanest way to say what it is *not*: **it is the top term of the decomposition of a monotone,
and it is not itself a monotone.** Total correlation *is* monotone under local operations (elementary:
`TC = D(p ‖ ⊗ pᵢ)`, and a product channel carries `⊗ pᵢ` to the output's own marginals, so
monotonicity of relative entropy applies; the quantum statement follows from strong subadditivity).
Zhou 2009 states exactly this contrast in his abstract. Decomposing a monotone by order does not give
monotones.

---

## (c) THE FOUR PRIOR-ART ADJUDICATIONS

### 1. Common information — Gács–Körner and Wyner. **VERDICT: CLEAR (different object).**

**Does it already answer "store"?** No, and the reason is the interesting part.

Gács & Körner (*Probl. Contr. Inform. Theory* 2, 149 (1973)) ask how much *common randomness can be
extracted* from correlated sources by separate deterministic functions. Wyner (*IEEE Trans. IT* 21,
163 (1975)) asks the dual: how much *common randomness must be supplied* — the minimum `I(X,Y;W)` over
`W` rendering the sources conditionally independent. Both are **asymptotic rates about many copies**,
and both are corner points of the Gray–Wyner region.

**The relation to our gap: neither bounds the other in either useful direction, and the repository's
own discriminator already exhibits the separation.**

- On `parity`: Gács–Körner common information is **0** (every pair is exactly independent, so there is
  no function of one that agrees with a function of another), while `share parity = log 2`.
- On `copied` (slots 1 and 2 equal, slot 3 free): the triple's Wyner common information is **one bit**
  (take `W` = the copied bit; the three are then conditionally independent), while
  `share copied = 0` — `Core/Share.lean`'s `share_copied`, proved.

So a state can be maximal in one and zero in the other, in both directions. The only true inequality
is elementary and already in the repository: `share ≤ multi-information` (subadditivity of entropy
against the pair envelope), which is exactly what `share_copied` vs `S_total_copied` demonstrates.

**Credit owed, one paragraph.** *The formal theory of how much shared structure can be extracted from,
or must be supplied to, correlated sources is Gács & Körner (1973) and Wyner (1975), with the two
quantities placed as corner points of the Gray–Wyner region. Our whole-only share is a different
object: a single-shot divergence to a model family rather than an asymptotic rate, and the two are
separated in both directions by states this repository already carries (`parity`, `copied`).*

**Adversarial note, and it is the sharpest warning in this document.** This is where a future scoop
lives. If this programme ever tries to give the share an *operational* meaning — a rate, a task, a
number of bits someone actually pays — it will be doing to the share what Gray–Wyner did to common
information, and that literature is fifty years deep and still active (approximate Gács–Körner,
common information dimension, distributed simulation). **Search there first, before staking anything
operational.**

### 2. Data hiding and secret sharing. **VERDICT: CONVERGENT-ADJACENT — the construction is 1979, the measure is not theirs.**

**Our exhibited state is a textbook cryptographic scheme.** `parity` — three bits, uniform on the
even-parity words — *is* the 3-party XOR secret-sharing scheme. `pairwise_blind_to_parity` is its
perfect-security condition (any two shares are jointly uniform and independent of the secret) and
`third_sees_parity` is its correctness condition. That pair is the definition of a perfect `(n,n)`
threshold scheme, and it long predates this repository.

**Credit owed, one paragraph.** *That structure can be arranged to be invisible to every proper subset
of the parties while determined by the whole is the founding construction of secret sharing —
Blakley, AFIPS 48, 313 (1979) and Shamir, CACM 22, 612 (1979), with the XOR `(n,n)` scheme folklore
and the general-access-structure treatment in Ito, Saito & Nishizeki (1987); the partial-leakage
family is the ramp schemes of Blakley & Meadows (1985). The quantum strengthening to parties
restricted to LOCC is quantum data hiding — Terhal, DiVincenzo & Leung, PRL 86, 5807 (2001), and
DiVincenzo, Leung & Terhal, IEEE Trans. IT 48, 580 (2002). This repository's `parity` state is the
three-party instance, and its pairwise blindness is that literature's security property.*

**Is our share the same quantity as any established hiding measure? No, and the mismatch is
diagnostic.** Hiding is measured *operationally and relative to a restricted operation class*: the
LOCC-norm distinguishability `‖ρ₀ − ρ₁‖_LOCC` in the quantum case, the leakage `I(S ; subset)` in the
classical ramp case. Both are "how much can this restricted adversary learn". The share is a
divergence to a model family with no adversary in it — which is precisely why §(b) finds no free
operations: the operational content that would supply them was never there.

**Consequence for the verb list.** If the programme wants "hiding" as a verb rather than as the
definition, the honest move is to adopt the leakage measure, which is standard, well-understood and
*is* monotone under the relevant operations — not to reinterpret the share as one.

### 3. Multipartite correlation, LOCC, and what local operations cannot create. **VERDICT: SCOOPED, and this leg supplies the cleanest sentence available.**

The brief asks for the sharpest way to say what our quantity is *not*. Here is the three-line ladder,
each rung published:

| statement | status | source |
|---|---|---|
| LOCC cannot create entanglement | textbook | Bennett, DiVincenzo, Smolin & Wootters, PRA 54, 3824 (1996); the monotone framework, Vidal, J. Mod. Opt. 47, 355 (2000) |
| local operations cannot increase **total** correlation | theorem | strong subadditivity; stated as the contrasting fact in Zhou 2009 |
| local operations **can** create **irreducible three-party** correlation | theorem | **Zhou, PRA 80, 022113 (2009)** |

And the axiom this violates is the community's own: Bennett–Grudka–Horodecki–Horodecki–Horodecki,
PRA 83, 012312 (2011), **Postulate 2** (§(b) Test 2).

**Credit owed, one paragraph.** *That local operations cannot create entanglement is the foundational
fact of entanglement theory (Bennett–DiVincenzo–Smolin–Wootters 1996; Vidal 2000), and that they
cannot increase total correlation follows from strong subadditivity. Our quantity is neither. Zhou
(PRA 80, 022113, 2009) proved in the same breath that total correlation is monotone under local
operations while the irreducible three-party correlation is not, and can be created by them from a
state carrying only two-party correlation; that is exactly the content of `Core/Valve.lean`'s
`valve_upward`, in greater generality and seventeen years earlier. The postulate set our quantity
thereby fails is Bennett, Grudka, Horodecki, Horodecki & Horodecki, PRA 83, 012312 (2011).*

Two adjacent items worth carrying: Girolami, Tufarelli & Susa, PRL 119, 140505 (2017), *Quantifying
genuine multipartite correlations and their pattern complexity*, is the modern measure built to
satisfy those postulates — the right pointer for a reader who asks "what should I use instead?"; and
Kahle, Olbrich, Jost & Ay, PRE 79, 026201 (2009) is the convex-combination question, already credited
in `Core/Valve.lean` and already corrected by `PUMP_RESULTS.md` §9.

### 4. Interaction information under operations — Amari, and the literature this repository has never cited. **VERDICT: CONVERGENT, and one half of it is a 1935–1983 statistics literature with no trace anywhere in this tree.**

Amari (*IEEE Trans. IT* 47, 1701 (2001), *Information geometry on hierarchy of probability
distributions*) is already the right ancestor for the hierarchy, the e-/m-projections, and the
orthogonality of the decomposition. `Core/Share.lean` credits Schneidman et al. 2003 and Zhou 2008;
Amari 2001 should be beside them, because the e-flatness of the free family — the fact that makes
§(b) Test 3 work — is his.

**But the classical statistics of exactly our object is older and is entirely absent from this
repository.** A grep of the whole `scratchpad/` tree for `Bartlett|contingency|collapsib|log-linear|
Birch|Darroch|Deming|Csisz` returns nothing but incidental uses of "log-linear" meaning "a fit on log
axes". The following are all the same object as `share` at k = 3 binary:

- **Bartlett, "Contingency table interactions", Suppl. J. Roy. Statist. Soc. 2, 248–252 (1935)** —
  defines the *no-three-factor-interaction* model on a 2×2×2 table (conditional odds ratios stable
  across the third factor). **Our free set at k = 3 is exactly Bartlett's null model.**
- Roy & Kastenbaum (1956); Darroch, JRSS B 24, 251 (1962); Plackett, JRSS B 24, 162 (1962);
  **Birch, JRSS B 25, 220 (1963)** — the MLE under the no-three-factor model is the unique
  exponential-family member matching the observed two-way margins. **That is the maximizer of
  `pairEnvelope`, and Birch proved existence and uniqueness in 1963.**
- **Deming & Stephan (1940)** — iterative proportional fitting, the algorithm this repository's
  `shareK` uses; **Csiszár, Ann. Probab. 3, 146 (1975)** — its convergence, as an I-projection. The
  memory note `ipf-sharek-boundary-drift` is a rediscovery of IPF's known boundary behaviour.
- **The estimator floor is Wilks (1938).** `2N · share` is the deviance `G²` of Bartlett's model. At
  k = 3 binary the saturated model has 7 free parameters and the no-three-way model has 6, so
  **df = 1** and `G² → χ²₁`. `PUMP_RESULTS.md` §6 measures `bias × N` flat at ≈ 0.22 against
  `median(χ²₁)/2 = 0.2275` and calls it "a correction useful to every campaign here". It is —
  and it is Wilks' theorem confirming itself. It should be reported at that size.
- **The coarse-graining question is the collapsibility literature.** Whittemore, JRSS B 40, 328
  (1978); Bishop, Fienberg & Holland, *Discrete Multivariate Analysis* (1975); **Asmussen & Edwards,
  Biometrika 70, 567 (1983)** — necessary and sufficient conditions, in terms of the generating class,
  for a hierarchical log-linear model to be collapsible onto a margin. `PUMP_RESULTS.md` §7's
  lumpability condition and `KAPPA_EDGE`'s binarization worry are special cases of a question with a
  1983 necessary-and-sufficient answer.

**Credit owed, one paragraph.** *The order-3 whole-only share of three binary variables is, up to the
factor `2N`, the likelihood-ratio deviance of Bartlett's no-three-factor-interaction model
(Bartlett 1935), whose maximum-likelihood fit is Birch's (1963) unique exponential-family member
matching the two-way margins, computed by Deming–Stephan (1940) iterative proportional fitting, whose
convergence as an I-projection is Csiszár's (1975), with the null distribution given by Wilks (1938)
and the behaviour under marginalization by the collapsibility results of Whittemore (1978) and
Asmussen & Edwards (1983). The information-geometric form of the same hierarchy is Amari (2001); the
information-theoretic naming as connected information is Schneidman, Still, Berry & Bialek (2003);
the quantum lift is Zhou (2008).*

This is the fifth-through-eleventh convergent-art strike. It is also the most useful one, because it
hands the READING verb a hundred-year-old toolbox instead of a campaign.

---

## (d) WHAT IS LEFT THAT IS NOT ALREADY IN PRINT

Being adversarial, as instructed. Four candidates; one survives as a result, one as a question, and
two are contributions of kind rather than of content.

**1. The mechanization. Contribution of kind — keep advertising it as exactly that.** The Lean proofs
of the k = 3 cap with no hypothesis, the three valve directions, the sign-symmetry vanishing, and the
minting theorems appear to have no machine-checked counterpart anywhere. That is real and it is what
the stance already claims. It is not a mathematical discovery and the page correctly does not say it
is.

**2. The non-convexity of the free set as a formal obstruction to a resource theory, with a
two-point machine-checked witness. SURVIVES — small, and worth a short note rather than a campaign.**
Zhou 2009 gives non-monotonicity under local operations. I found nothing making the framework-level
step: that the obstruction is the *free set*, not the operations; that `bulge = ½·δ_FFF + ½·indep` is
a two-point witness both of whose endpoints are machine-checked free and whose midpoint is
machine-checked resourceful; that this also defeats the 2026 star-shaped relaxation at the natural
centre; and that white noise is therefore a source. It is a corollary of theorems already in the tree
and it is **one Lean lemma from being machine-checked**: `bulge = fun t => ½ · δ_FFF t + ½ · indep t`
is an eight-cell `norm_num`, after which `share_prod3` and `valve_upward` close it with no new
mathematics. *Caveat, stated because the campaign's record demands it: the underlying fact —
mixtures of pairwise-only states carry higher-order structure — is Schneidman 2003 Fig. 3, Kahle et
al. 2009 and Macke et al. 2011. What is not in print is the resource-theoretic reading. Assume that
is convergent too until a sweep of the resource-theory literature for "non-convex free set",
"star-shaped", "discord", "total correlations" comes back empty; the 2026 Quantum paper cites discord
and total correlations as its non-convex examples and may well cite this case.*

**3. The asymmetry-resolved rate law. Already settled — PUMP's L4, verdict CLEAR.** Unchanged by
anything here. The closed form in `(a, s, ρ)`, its exponent, its theorem-pinned zero, its k-scaling
and its hardware overlay remain this programme's.

**4. The open mathematical question this adjudication generates. A QUESTION, not a result.**
Characterize the stochastic maps under which `share` is non-increasing — equivalently, the stabilizer
of the no-three-factor-interaction model under the semigroup of column-stochastic matrices. The
deterministic-marginalization case has a 1983 necessary-and-sufficient answer (Asmussen–Edwards). The
stochastic case I did not find. At k = 3 it is a concrete elimination problem on a degree-4
hypersurface in the 7-simplex (`p₁₁₁p₁₀₀p₀₁₀p₀₀₁ = p₀₀₀p₀₁₁p₁₀₁p₁₁₀`), and its expected answer is
"only slot permutations, per-slot bit flips, and the constant maps" — which, if proved, closes the
resource-theory question permanently instead of by counterexample. **Warning before anyone spends a
day on it: this is a stabilizer question about a toric variety, squarely inside algebraic statistics
(Sturmfels; Drton–Sturmfels–Sullivant, *Lectures on Algebraic Statistics*), a field with Markov bases
for exactly this model already in the literature. Search there first. Assume convergence.**

**And the honest bottom line.** Everything on the *mechanism* side of this programme — creation,
transfer, capacity, estimation — is 1935 to 2012 with a 2019 review on top. The one question here
whose answer is not sitting in a library is the stance's single `open` claim: **which of nature's wild
processes carry whole-only share.** Nothing in this adjudication touches it, helps it, or is a
substitute for it. A four-verb programme would have been four more ways to not run that experiment.

---

## (e) THE CONCRETE NEXT CAMPAIGN THIS IMPLIES

**Do not build the four-verb programme.** Two of the four are not verbs (HIDE is the definition,
MAINTAIN is a case of MAKING), and of the two that are, CAPACITY is largely done and MAKING is
scooped qualitatively and quantified by our own PUMP campaign.

**Recommended, in priority order:**

**P1 — Corrections owed now. Not a campaign; a morning.** Three of them, all naming, none touching a
proof:
1. `Core/Share.lean` header — add **Amari 2001** beside Schneidman 2003 and Zhou 2008, and add
   **Bartlett 1935 / Birch 1963** as the classical-statistics identity of the k = 3 binary case.
2. `PUMP_RESULTS.md` §6 — the `0.227/N` floor is **Wilks (1938)** with df = 1, not a new correction.
   Say so in the section rather than in an amendment.
3. `PUMP_RESULTS.md` §7 / the kappa-edge prereg — lumpability is a special case of **collapsibility**,
   with necessary and sufficient conditions in **Asmussen & Edwards (1983)**. Cite before measuring
   again.

**P2 — The resource-theory note. One day, one Lean lemma, one page.** Sweep the resource-theory
literature for the non-convex-free-set case (query on "star-shaped", "non-convex free set", discord,
total correlations, non-Markovianity). If it comes back empty on *this* free set, mechanize
`bulge_eq_half_delta_add_half_indep` (an eight-cell `norm_num`) and state the corollary:
`share` admits no resource theory with a convex or star-shaped free set, witnessed by two of its own
free states. **Kill:** a published statement that the pairwise-maxent family is non-convex and
therefore admits no resource theory — in which case the note becomes a citation and nothing more.
This is worth doing because it is cheap and because it *retires* a whole direction rather than opening
one.

**P3 — The one dynamical question the four verbs contained that is genuinely open.** The **steady
state** of repair against noise: iterate `parityRepair` (or any code projection) alternating with a
per-cell channel, and ask what the stationary whole-only share is as a function of the noise. This is
the only piece of MAINTAIN that is not a restatement — `Core/Creation.lean`'s header says the
dynamical version is proved nowhere, and `Core/Maintenance.lean`'s rent clause is about a scalar
recursion, not about `share`. It is tractable with the gated exact solver, it composes with the PUMP
closed form, and it is the natural next brick. **Prior-art gate before any measurement, non-negotiable
given the record:** probabilistic cellular automata with error correction (Toom's rule, Gács),
nonequilibrium steady states of error-correcting dynamics, and the neural-maxent literature on
maintained higher-order structure. Assume convergence; search by mathematical object.

**P4 — And the standing recommendation.** The programme's one `open` claim is `wild-share`, its named
next instrument is DESI BGS, and nothing in this document is a substitute for pointing an instrument
at the sky. Everything above is bookkeeping about a quantity whose behaviour has been known for
between fourteen and ninety-one years.

---

## Sources

- [Coecke, Fritz & Spekkens, *A mathematical theory of resources*, arXiv:1409.5531](https://arxiv.org/abs/1409.5531)
- [Chitambar & Gour, *Quantum resource theories*, Rev. Mod. Phys. 91, 025001 (2019), arXiv:1806.06107](https://arxiv.org/pdf/1806.06107)
- [Fritz, *Resource convertibility and ordered commutative monoids*, arXiv:1504.03661](https://arxiv.org/pdf/1504.03661)
- [Zhou, *Irreducible multiparty correlation can be created by local operations*, PRA 80, 022113 (2009), arXiv:0904.1863](https://arxiv.org/abs/0904.1863)
- [Bennett, Grudka, Horodecki, Horodecki & Horodecki, *Postulates for measures of genuine multipartite correlations*, PRA 83, 012312 (2011), arXiv:0805.3060](https://arxiv.org/abs/0805.3060)
- [*Quantum Resource Theories beyond Convexity*, Quantum 10, 2104 (2026)](https://quantum-journal.org/papers/q-2026-05-13-2104/)
- [Macke, Opper & Bethge, *Common input explains higher-order correlations and entropy…*, PRL 106, 208102 (2011), arXiv:1009.2855](https://arxiv.org/abs/1009.2855)
- [Amari, *Information geometry on hierarchy of probability distributions*, IEEE Trans. IT 47, 1701 (2001)](https://people.csail.mit.edu/jrennie/trg/papers/amari-ig-hierarchy-01.pdf)
- [Whittemore, *Collapsibility of multidimensional contingency tables*, JRSS B 40, 328 (1978)](https://academic.oup.com/jrsssb/article/40/3/328/7027572)
- [Asmussen & Edwards, *Collapsibility and response variables in contingency tables*, Biometrika 70, 567 (1983)](https://academic.oup.com/biomet/article-abstract/70/3/567/247512)
- [Birch, *Maximum likelihood in three-way contingency tables*, JRSS B 25, 220 (1963)](https://academic.oup.com/jrsssb/article/25/1/220/7035241)
- [Darroch, *Interactions in multi-factor contingency tables*, JRSS B 24, 251 (1962)](https://rss.onlinelibrary.wiley.com/doi/abs/10.1111/j.2517-6161.1962.tb00457.x)
- [Terhal, DiVincenzo & Leung / DiVincenzo, Leung & Terhal, *Quantum data hiding*, IEEE Trans. IT 48, 580 (2002)](https://ui.adsabs.harvard.edu/abs/2001quant.ph..3098D/abstract)
- [Girolami, Tufarelli & Susa, *Quantifying genuine multipartite correlations and their pattern complexity*, PRL 119, 140505 (2017)](https://www.researchgate.net/publication/317590964_Quantifying_Genuine_Multipartite_Correlations_and_their_Pattern_Complexity)

**Numerical checks behind §(b) Test 3** are in
`/tmp/claude-1000/-home-emoore-CIRISOntology/4cf4fa5c-aaa3-4173-83b9-978cb75c887f/scratchpad/conv.py`
and `conv2.py` (exact 1-D `p + t·χ` solver, the same parametrization `Core/Valve.lean`'s header
records). They reproduce `share bulge = 0.021185`, the value `PUMP_RESULTS.md`'s gate table reports
against `valve_upward_bound = 0.011962`.
