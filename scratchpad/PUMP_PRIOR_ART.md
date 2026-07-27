# PUMP campaign — prior art, searched before any curve was computed

**Question the campaign asks.** Under per-cell stochastic noise — each slot pushed through its
own kernel, no kernel reading any other slot — at what **rate** is pair structure converted into
whole-only structure, as a function of the channel's **asymmetry**?

`Core/Valve.lean` proves four qualitative facts about the k = 3 binary model: never from
nothing, never downward, upward strictly, and the pump is asymmetry not strength. Nobody in this
repository has measured the *curve*. Before measuring it, the house standard applies: **assume
the result is convergent art, and search by mathematical object rather than by phrase.**

Search date: 2026-07-27. Searcher: the pump-curve agent. Method: five object-directed sweeps
(connected information under stochastic maps; local channels and multipartite correlation;
information geometry under Markov maps; unital vs non-unital channels; stochastic thermodynamics
of correlation production), following citation chains to primary sources and reading the primary
sources' own text rather than abstracts where the claim was load-bearing.

---

## VERDICT, one line per leg

The campaign's four legs do not have one verdict between them, and pretending they do would be
the dishonest move. Stated separately, because they are separable:

| leg | what it says | verdict |
|---|---|---|
| **L1 — creation** | per-cell/local stochastic channels CAN raise the whole-only share | **SCOOPED**, three times over, from 2009 |
| **L2 — never from nothing** | they cannot raise it from a product state | **SCOOPED**, stated as the contrasting fact in the same papers |
| **L3 — asymmetry is the pump** | flip-covariant (unital) kernels mint exactly zero from sign-symmetric states | **CONVERGENT-ADJACENT** — the same shape is a known theorem for a *different* quantity |
| **L4 — the rate law** | how much share, as a function of channel asymmetry and strength | **CLEAR** — and the closest paper calls the general question unsolved |

**The campaign proceeds, on L4 only.** L1 and L2 are not ours and must stop being presented as
though the packaging were the discovery; L3 is ours as stated but is one step from a published
result and must be credited as such. The measurement to be made is the rate law.

---

## L1 — creation. SCOOPED, and by a paper this repository does not cite

### The primary source

**D. L. Zhou, "Irreducible multiparty correlation can be created by local operations",
Phys. Rev. A 80, 022113 (2009)** — [arXiv:0904.1863](https://arxiv.org/abs/0904.1863).

From the abstract, read in the paper's own text:

> "…although the degree of the total correlation in a three-party quantum state does not
> increase under local operations, the irreducible three-party correlation can be created by
> local operations from a three-party state with only irreducible two-party correlations."

That is `valve_upward` and `valve_no_downward`'s companion, on the same object, seventeen years
before ours. Zhou's quantity is defined exactly as ours is — he generalises Amari's hierarchy,
proves the definition equivalent to "the maximal von Neumann entropy principle", and states the
classical antecedent explicitly as "the connected information of order k for a probability
distribution of n classical variables defined in Ref. [4] by Schneidman et al." Those are the two
citations already in `Core/Share.lean`'s header. The method is an explicit counterexample: one
three-qubit state, one local operation, checked to leave the no-triple-interaction manifold.

**This is a live gap in the repository.** `Core/Share.lean` credits *Zhou 2008* (PRL 101, 180505)
for the quantum form of the quantity. `Core/Valve.lean` credits Kahle, Olbrich, Jost and Ay 2009
for the creation mechanism. Neither cites **Zhou 2009**, which is the same author's next paper
and is the exact statement `valve_upward` machine-checks. The correction is one line in a CREDIT
paragraph and is named here rather than made, because this campaign does not touch the Lean.

### The classical primary source, on our exact model

**T. Galla and O. Gühne, "Complexity measures, emergence, and multiparticle correlations",
Phys. Rev. E 85, 046209 (2012)** — [arXiv:1107.1180](https://arxiv.org/abs/1107.1180).

> "We show that these measures can increase under local transformations as well as under
> discarding particles, thereby questioning their interpretation as a quantifier for complexity
> or correlations."

Their §III.B is the classical, three-binary-variable case — our model exactly. They write the
no-triple-interaction manifold as

> P(000)·P(011)·P(110)·P(101) = P(001)·P(010)·P(100)·P(111)

which is the same condition our exact k = 3 solver roots (`p₀p₂³ = p₁³p₃` in the
permutation-symmetric parametrization), generate random members of it, apply a random local
transformation, and observe the image leaves the manifold: "This proves that D₂ can increase
under local operations." They add the sharpening that matters for scope — the increase "occurs
already in the classical regime and is also not due to possible non-commuting terms":

> "Our considerations complement those of Ref. [16] [Zhou 2009], where it was observed that a
> quantum analog of the quantity D_k can increase under local operations and classical
> communication."

So the classical statement is published too, and published *as a criticism of the measure*. That
framing is worth carrying: Galla and Gühne read non-monotonicity as a defect disqualifying the
quantity as a complexity measure, and propose a repaired definition. This programme reads the
same fact as a mechanism and builds on it. Both readings are available from the same theorem, and
a reader should be told the critical one exists.

### The third, and the one already credited

**T. Kahle, E. Olbrich, J. Jost, N. Ay, "Complexity measures from interaction structures",
Phys. Rev. E 79, 026201 (2009)** — [arXiv:0806.2552](https://arxiv.org/abs/0806.2552). Already
credited in `Core/Valve.lean`. What they actually say, in the coupled-tent-map section, is
empirical and is the seed of leg L4:

> "If the two types of sequences are mixed then higher order correlations appear, leading to the
> peak. **This corresponds to the more general and unsolved problem whether the complexity of a
> convex combination of two distributions is related to the complexities of the individual
> constituents.**"

They observed mixing creating higher-order interaction, and flagged the quantitative version as
open. That sentence is the best single justification for this campaign existing.

### The standing textbook caveat

**D. Girolami, T. Tufarelli, C. E. Susa, "Quantifying genuine multipartite correlations and
their pattern complexity", Phys. Rev. Lett. 119, 140505 (2017)** —
[arXiv:1706.04562](https://arxiv.org/abs/1706.04562) — build an axiom set for genuine
multipartite correlation measures whose property 2D-2S is:

> "Local CPTP maps … **cannot create correlations of any order k**, and cannot increase the
> amount of correlations higher than any order k."

and then say, of the max-entropy-under-k-marginals measure — ours —

> "Remarkably, independent lines of thinking converged to the very same definition. However, such
> measure … **violates contractivity under local operations in both classical and quantum
> scenarios** [Galla-Gühne 2012, Zhou 2009]. This happens because local operations do change a
> state whilst preserving its tensor product structure, **thus changing the set of states with
> the same k-marginals.**"

That last clause is the mechanism, stated in one sentence, and it is the same mechanism
`Core/Valve.lean`'s route note describes geometrically (the competitor line `p + tχ` moves when
the kernels move). It is also the answer to the sharp risk this campaign was briefed on. The
textbook fact is *"local operations cannot create entanglement"*, and a nearby published axiom
demands the same of genuine-multipartite-correlation measures. **Our quantity is neither**, it is
explicitly excluded from that axiom set for exactly this reason, and Girolami et al. are the
citation to hand anyone who objects that local channels cannot create multipartite correlation:
they can, for this quantity, and the people who wrote the axiom say so in print.

---

## L2 — never from nothing. SCOOPED, and stated as the contrast in the same papers

Galla and Gühne, same section:

> "the manifold E₁ of distributions factorizing over individual particles is clearly invariant
> under local transformations. Hence, the quantity D₁ (also referred to as multi-information) does
> not increase under local transformations."

Zhou's abstract states the same contrast for the total correlation. `valve_from_nothing` is the
share-sector form of an observation both papers make in passing; the mechanization is ours, the
fact is not. Elementary either way — a product in is a product out is a one-line identity
(`channel3_prod3`, no hypotheses).

---

## L3 — asymmetry is the pump. CONVERGENT-ADJACENT, and the near neighbour is well known

A flip-covariant binary kernel — `K(!y)(!x) = K y x` with normalized columns — is exactly the
binary symmetric channel, which is exactly the **unital** binary channel: the one that fixes the
maximally mixed state. `valve_needs_asymmetry` therefore reads, in the standard vocabulary:
*local unital channels create no whole-only share from a sign-symmetric state.*

That shape is a known theorem for a different quantity:

- **A. Streltsov, H. Kampermann, D. Bruß, "Behavior of quantum correlations under local noise",
  Phys. Rev. Lett. 107, 170502 (2011)** — [arXiv:1106.2028](https://arxiv.org/abs/1106.2028).
  Local **unital** channels can only decrease quantum discord on qubits; **non-unital** channels
  (dissipation) can create discord from a classically correlated state. Non-unitality is named as
  the enabling property.
- **F. Ciccarello, V. Giovannetti, "Creating quantum correlations through local nonunitary
  memoryless channels", Phys. Rev. A 85, 010102(R) (2012)** — the constructive companion.
- **The power of quantum channels for creating quantum correlations**,
  [arXiv:1211.4805](https://arxiv.org/abs/1211.4805) — and the caveat that in higher dimensions
  even unital channels can create discord, which is the right warning against over-reading the
  binary case.

**What is different, and it is not nothing.** Discord is not the whole-only share; the two
quantities are unrelated in general (discord is nonzero on plenty of states whose share is
exactly zero, and our sign-symmetry lemma kills the share on a family where discord does not
vanish). And our statement carries a hypothesis theirs does not: the input must be
**sign-symmetric**. Drop that and the theorem is false — a unital kernel on a non-sign-symmetric
pair-correlated state can move the share. So `valve_needs_asymmetry` is not a corollary of the
discord result and is not implied by it.

**What is not different, and must be said plainly.** The *idea* — that creation of correlation by
local noise requires the channel to break the symmetry that fixes the equilibrium state — is
fifteen years old and belongs to the discord literature. This programme arrived at it
independently, on a different quantity, with a different hypothesis, and machine-checked it. That
is a contribution. It is not a discovery of the principle.

**Not found, and searched for:** any statement of the unital/non-unital dichotomy for connected
information, irreducible correlation, or interaction information specifically. Zhou 2009 and
Galla-Gühne 2012 both give existence and neither asks what property of the channel is doing the
work.

---

## L4 — the rate law. CLEAR

Searched for, and not found: any expression, curve, fit, or scaling for **how much** whole-only
share (connected information / irreducible k-party correlation / interaction information) a local
stochastic channel creates, as a function of the channel's parameters.

What the closest sources give instead:

| source | what it delivers on magnitude |
|---|---|
| Zhou 2009 | one worked counterexample; a table of `tanh(1)`-valued parameters at one operating point. No sweep, no functional form |
| Galla & Gühne 2012 | random sampling to establish that the image generically leaves the manifold. Existence, deliberately — magnitude is not their question |
| Kahle et al. 2009 | an observed peak, and an explicit statement that the general quantitative problem is **unsolved** |
| Girolami et al. 2017 | uses the non-monotonicity only to disqualify the measure from their axiom set |
| Streltsov et al. 2011 and successors | quantitative for **discord**, not for this quantity |
| stochastic thermodynamics (Horowitz & Esposito 2014; Diana & Esposito 2014; Parrondo, Horowitz & Sagawa, *Nat. Phys.* 11, 131 (2015); Horowitz, *multipartite information flow*) | rate laws for **mutual information** production against entropy production in multipartite dynamics. Bipartite/pairwise information flow, coupled dynamics. Nothing decomposing the produced correlation by interaction order, and nothing for independent per-cell channels, where the entropy-production framing has no coupling to price |
| **Environment-driven emergence of higher-order collective behavior**, [arXiv:2602.15256](https://arxiv.org/abs/2602.15256) (2026) | the nearest live work: O-information, environmental fluctuations inducing redundancy and synergy, and the finding that *time-independent* coupling to a shared environment **rules out** synergistic higher-order behaviour. Different mechanism (a **shared** environment is a coupling; ours are independent per-cell kernels), different measure (O-information ≠ connected information), and again no rate law in the channel's parameters |

The stochastic-thermodynamics column is the one worth flagging as a live risk for a future
search: it is the field most likely to already own a rate law of this shape, its vocabulary
("correlation production rate") does not overlap ours, and this sweep reached its multipartite
information-flow line but not its whole literature. Recorded as an incomplete search, not as an
all-clear.

---

## THE CREDIT PARAGRAPH

Nothing in the underlying mathematics of the pump is ours. The quantity is the connected
information of **Schneidman, Still, Berry and Bialek** (2003), equivalently the hierarchical
decomposition of **Amari** (*Information geometry on hierarchy of probability distributions*,
IEEE Trans. Inf. Theory 47, 1701, 2001), in the quantum form of **Zhou** (PRL 101, 180505, 2008).
That local operations **can create** it — the whole of the valve's upward direction — is
**Zhou, Phys. Rev. A 80, 022113 (2009)** in the quantum setting and **Galla and Gühne,
Phys. Rev. E 85, 046209 (2012)** in the classical setting on three binary variables, our exact
model; **Girolami, Tufarelli and Susa** (PRL 119, 140505, 2017) record it as the standing reason
the quantity is excluded from their genuine-multipartite-correlation axioms, and state the
mechanism. That mixing creates higher-order interaction, and that the quantitative version of the
question is open, is **Kahle, Olbrich, Jost and Ay** (Phys. Rev. E 79, 026201, 2009). That
creation by local noise requires a **non-unital** channel is **Streltsov, Kampermann and Bruß**
(PRL 107, 170502, 2011) and **Ciccarello and Giovannetti** (PRA 85, 010102(R), 2012), for quantum
discord rather than for this quantity.

Ours, and stated no larger than it is: the mechanization at k = 3 as four separable directions
(`Core/Valve.lean`); the sign-symmetry hypothesis that makes the asymmetry statement a theorem
rather than an observation (`Core/SignSymmetry.lean`); the hardware arm that measured the upward
direction with a zero-free-parameter curve; and — the object of this campaign, and the only leg
where the search came back empty — **the rate at which the conversion happens, as a function of
the channel's asymmetry and strength.**

---

## What this changes about the campaign

1. **The deliverable is narrower than the brief's framing and should be stated that way.** "Local
   noise creates whole-only structure" is 2009. "Here is the law that says how fast" is the
   contribution. `PUMP_PREREG.md` is written to that scope.
2. **A repository correction is named, not made:** `Core/Valve.lean`'s CREDIT paragraph should
   cite Zhou 2009 and Galla-Gühne 2012 alongside Kahle et al. Flagged for the Lean-owning pass.
3. **The strongest available framing of the result is the one Girolami et al. hand us.** The
   non-monotonicity is not a curiosity of our construction; it is a published, mechanism-explained
   property of a quantity that four independent lines of work converged on. Anyone objecting that
   local operations cannot create multipartite correlation is answered by citation, not by
   argument.
4. **The measure has a published criticism attached and the record must carry it.** Galla and
   Gühne treat exactly this non-monotonicity as grounds to reject the quantity as a complexity
   measure. This programme's position is that a quantity being creatable by local noise is a
   fact about the world worth measuring rather than a defect to be defined away — but that is a
   *position*, it is contestable, and the contesting paper is named.
