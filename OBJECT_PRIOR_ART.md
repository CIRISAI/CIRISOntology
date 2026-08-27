# OBJECT — prior art, compared as complete systems

*2026-08-26. The dedicated comparison `Q10_PREREG.md` §11 and `Core/ExchangeSign.lean`
both said was owed before any novelty claim. Synthesis by Eric Moore; verification
status marked per row. **Conclusion first: no single row is the object, and no piece
of the object is unprecedented.***

## The finding, stated before the table

The likely novelty is **not** "views," not "closure," not "global sections," not
"whole-only information," and not "information has thermodynamic cost." Each exists,
developed, elsewhere. The only candidate is:

> A single recursively applied closure/factorization object in which effective scale,
> interaction, contextuality, transport and maintenance become different measurable
> properties of the same structure.

That is a claim about COMPOSITION, and composition claims need a formal comparison
paper before priority is asserted. Until then this file is the standing answer to
"is this new?": **the pieces are not.**

## The closest composite

> Topos quantum theory + computational mechanics + dynamical coarse-graining +
> algebraic QFT + stochastic thermodynamics.

## The table

| Program | Strong overlap | Important difference |
|---|---|---|
| **Döring–Isham topos quantum theory** ([quant-ph/0703062](https://arxiv.org/abs/quant-ph/0703062)) | Physical quantities are arrows in a contextual topos; the spectral presheaf replaces the classical state space and has **no global elements**. **VERIFIED 2026-08-26**: Kochen–Specker IS the non-existence of a global section of the spectral presheaf. This is not adjacent to `OBJECT.md` §1 — it IS §1's central move, and it precedes us by ~20 years (Isham–Butterfield, late 1990s). | A reformulation of quantum theory and its logic. Supplies **no** recursive dynamical tiers, **no** closure test, **no** maintenance cost. |
| **Abramsky–Brandenburger contextuality** ([1102.0264](https://arxiv.org/abs/1102.0264)) | Measurement contexts form a presheaf; contextuality is obstruction to global sections. Already credited in `Core/NonFactoring.lean`. | Concerns empirical compatibility across measurement contexts, not general coarse-graining or induced dynamics. |
| **Computational mechanics** ([cond-mat/9907176](https://arxiv.org/abs/cond-mat/9907176)) | Causal states are the coarsest classes retaining full predictive power and carry autonomous Markov dynamics. **Very close to "a tier is a Closed predictive view."** | Built for stochastic processes and prediction; no contextuality, no gauge transport, no maintenance. |
| **Lumpability / Mori–Zwanzig** ([1607.01237](https://arxiv.org/abs/1607.01237), [2101.05873](https://arxiv.org/abs/2101.05873)) | Exact lumpability is effectively `v ∘ T = φ ∘ v` — **literally `Core/Habit.Closed`**. Eliminating hidden variables generates memory and noise. | Treated as model reduction, not ontology. Closure failure means "your reduced model needs memory," not necessarily interaction or coherence. |
| **Algebraic QFT** ([2305.12923](https://arxiv.org/abs/2305.12923)) | A net of local observable algebras with restriction/inclusion, states, dynamics. | Spacetime regions and locality are INPUTS. The maximal reading wants scale and possibly geometry to emerge from view/transport structure. |
| **RG and causal emergence** ([2202.01854](https://arxiv.org/abs/2202.01854)) | Effective levels from repeated coarse-graining; macrovariables can be more predictive than micro. | The coarse-graining is selected by a particular physical or informational criterion, not one universal `Factors`/`Closed` relation. |
| **Constructor theory** ([1210.7439](https://arxiv.org/pdf/1210.7439)) | Information as physically instantiated; scale-independent laws about possible/impossible transformations. | Makes counterfactual tasks fundamental; we make dynamics and predictive closure fundamental. |
| **Relational quantum mechanics** ([quant-ph/9609002](https://arxiv.org/abs/quant-ph/9609002)) | Facts are physical but relative to interacting systems. | An interpretation, not a theory of coarse levels, higher-order information, or maintenance. |

More distant: categorical process theories, integrated information, predictive-state
representations, information bottleneck.

| **Einselection / predictability sieve** (Zurek, quant-ph/0105127) | Pointer states are the states whose records survive decoherence; the sieve selects them by predictability. **This is closure-selection**: pointer views are the `Closed` ones, and `Core/DiagonalLift.lean`'s wall (`diag_not_closed_under_coherence`) is einselection's boundary stated as a non-closure certificate. | Zurek selects STATES within quantum theory; the square selects VIEWS across substrates, and mechanizes the selection criterion. |
| **Hydrodynamic Lyapunov modes** (Posch–Hoover; McNamara–Mareschal, and covariant Lyapunov vectors, Ginelli et al.) | Collective, momentum-like Lyapunov modes in particle systems: perturbation fields aligning with conserved-quantity directions. **Very likely the phenomenon our organization discovery measured** (the difference field organizing into momentum-x, peaked in the intermediate settling window). | Their instruments are spectra and mode shapes; ours is a chart battery with a conditioning control and a settling-dose axis. LITERATURE CHECK OWED before any first-claim on the peak. |

## What this costs us, concretely

Three claims in the tree need their credit corrected or their scope narrowed:

1. **`OBJECT.md` §1's global-section framing is Döring–Isham**, not ours and not only
   Abramsky's. Corrected in `OBJECT.md` the same day this file was written.
2. **`Closed` is exact lumpability.** `Core/Habit.lean` already credits Kemeny–Snell;
   the Mori–Zwanzig reading (closure failure ⇒ memory) is the sharper neighbour and is
   NOT yet credited there.
3. **"A tier is a Closed view" is close to computational mechanics' causal states.**
   Shalizi–Crutchfield get the coarsest predictively-sufficient partition; we get a
   predicate. Theirs is constructive, ours is not.

## The de-risking step, and it is the cheapest one available

Formalize the object as a dynamic presheaf/stack and prove RECOVERY results:
deterministic `Closed` recovers semiconjugacy/lumpability; stochastic closure recovers
Markov lumpability or zero-memory Mori–Zwanzig; quantum contexts recover the
Abramsky–Brandenburger presheaf; local observable views embed an AQFT net; repeated
approximate closure recovers an RG-like flow.

**The valuable outcome is a theorem none of those translations gives alone.** Absent
that, the maximal object may be a common NOTATION rather than a new STRUCTURE, and
this file exists so that possibility stays on the table.

## The four bridges that would make it a framework

A clean parameter-free law connecting any ONE of these pairs, surviving a fresh
substrate, is worth more than another isolated high-sigma detection:

1. closure residual ↔ thermodynamic maintenance cost
2. closure failure ↔ transport curvature
3. whole-only share ↔ contextual fraction
4. predictive closure ↔ objectively selected physical scale

**Without such a bridge the campaign is an unusually rigorous synthesis of existing
ideas.** With one, it is a new physical framework. That sentence is the standing
verdict until a bridge is measured.

## Verification status

Döring–Isham row: **independently verified** by literature search, 2026-08-26 —
spectral presheaf as classical-state-space analogue, Kochen–Specker as absence of a
global section. Abramsky–Brandenburger: cross-validated, already independently
credited in `Core/NonFactoring.lean`. Remaining arXiv identifiers are **as supplied
and not independently fetched**; anyone relying on a specific row should open it.
