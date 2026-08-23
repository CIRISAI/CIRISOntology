# INTEGRATION FRAME — one holon, values only
Status: binding integration constraints for the descriptor-chain program.
Role: the tier specs (workflow `wf_29f9c722-2bd`) are integrated INTO this frame; any
tier content that cannot be expressed inside it is a **misfit to cash**, not a reason to
extend the frame.
Date: 2026-08-23.

## The three hard rules (Eric)

1. **All tiers use THE holon.** `Holon<W>` / `RuntimeArena` as they exist: `parent, depth,
   grain_units, gross (REG+), whole[W], channels, boundary, decomposition`. No per-tier
   structs, no new fields.
2. **Same frame and objects precisely.** Descriptor holons, relation holons,
   `MaterialBinding`, `CohesiveBond`, certificates, `GrainFloor`/`RefinementUnavailable` —
   identical at every tier. **The only difference between tiers is VALUES.**
3. **A stone holon must describe containing the three levels below it accurately enough
   to decompose** — grain, crystal, atomic — on certificate demand.

## What the code already has, and the one structural gap

`Decomposition::{Leaf, Latent, Expanded}` and transactional `materialize()` already give
us containment-without-enumeration: a Latent holon "represents recursively implied
children without enumerating them," and no materialization commits unless children
compose exactly back to the parent's REG+ ledger.

**The gap: the demo materializer is structurally empty.** `split_gross(parent.gross)`
halves counts. The children carry no mineral identity, no size distribution, no flaws —
because the parent carries no information about what its interior IS. Accurate
decomposition needs a **generator**, and the rules say it may not be a new object.

## The resolution: the descriptor holon IS the generator, and containment statistics are
## its WHOLE-ONLY state

No new machinery is needed — the frame already contains the answer if we use it fully:

- **Descriptors are holons**, so they decompose like everything else. The stone
  descriptor's children are the mineral descriptors; the mineral descriptor's children
  are bond/force-constant descriptors; theirs are atomic descriptors. "Three levels
  below" is the descriptor holon's OWN depth-3 subtree.
- **Mineral fractions are the descriptor's gross ledger.** Quartz 30% / feldspar 60% /
  mica 10% of a million-constituent wall is literally `GrossState` arithmetic on the
  descriptor's children: 300k/600k/100k constituent counts that must compose exactly.
  The existing conservation check enforces modal composition for free.
- **Distribution parameters are whole-only state on the descriptor** — and this is not a
  storage convenience, it is the metaphysics landing exactly where it should: a
  grain-SIZE distribution, an orientation texture, a Weibull flaw modulus are facts about
  the ENSEMBLE that do not factor through any single materialized child. Information
  that cannot be reconstructed from partial views is precisely what `whole[W]` exists to
  carry. The variable-width whole-state pool in `RuntimeArena` already supports a
  different W per holon, so a stone descriptor can carry {modal weights, grain-size
  log-normal (mu, sigma), Weibull (m, sigma_0, flaw density), texture parameters} while
  a bond descriptor carries {stiffness, energy} — same object, different values and W.
- **"Made of" stays `MaterialBinding`** — subject holon → descriptor holon. Unchanged.
- **Materialization becomes: read the binding, walk the descriptor subtree, draw
  children deterministically from the descriptor's distributions.** Seeded from the
  parent holon ID (the engine's `EntropyProvenance::Seeded` idiom), so replay is
  bit-identical — decomposing the same wall twice yields the same grains. The existing
  transactional commit then enforces ledger exactness.

## The new certificate this forces (and it is a check, not a new object)

Ledger exactness is already enforced. Accurate decomposition adds ONE obligation:
**statistical composition** — the empirical distribution of a materialized ensemble must
converge to the descriptor's declared distributions (KS-distance or moment bounds at the
materialized count, with the tolerance scaled to how many children were drawn: 288
resident nodes cannot and need not match a Weibull tail that only 10^6 grains would
show). A materialization that passes the ledger but fails the statistics is REJECTED the
same way a ledger violation is. This is the per-edge homogenization certificate of the
descriptor DAG, run in the DOWNWARD direction.

## What each tier is, under the rules

One schema, six value-sets. Per tier: (a) which `whole[W]` fields the descriptor carries
(values), (b) which channel evaluates it, (c) the certificate values (validity domain,
tolerance), (d) the gate values (reference sim, observables, thresholds). The tier table
comes from the workflow output, integrated under this frame — any tier demanding a new
FIELD rather than new VALUES is a misfit.

## Immediate consequences worth noting

- The mechanical channel almost never refines past crystal scale: the chain terminates
  at `GrainFloor` for mechanics at grain/crystal, by design. The atomic and floor tiers
  exist to CERTIFY the crystal descriptor's values (DFT-derived force constants), not to
  be materialized in a game frame.
- `deterministic_flaw`'s mod-43 pattern is the degenerate ancestor of the Weibull draw:
  same role, hand-tuned values. Replacing it is a VALUES change, which is the point.
- The demo's similarity-scaled cohesive law becomes a DERIVED value: descriptor
  properties + bond length + node spacing → law constants, with the derivation being
  T4's homogenization certificate run downward.
