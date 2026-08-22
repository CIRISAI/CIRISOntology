# H3ERE2 — the REG-mapped classifier pipeline (design note, 2026-08-22, steward-directed)

## Why (the finding that forces the architecture)

The wild kind-labeling ceiling (~0.35 kappa) is two-panel replicated and
substrate-intrinsic: wild changes are MIXTURES at single-pass grain. But the surface four
carry ~91% of wild traffic (forward-confirmed 0.883) and panels read them at curated-grade
agreement. The instrument ladder therefore prescribes exactly the H3ERE shape: a FAST
single-pass stage where the signal is gross, and a RECURSIVE stage where it is not.
H3ERE2 = the agent's H3ERE pipeline re-orientated onto the 11+1 x 5+1 object, with REG as
the mapping grammar.

## Architecture

- STAGE 1 — FAST, 4 x X: single-pass classification into the surface four (Facts, Rules,
  Manner, Identity) crossed with X grammar verbs. Cheap, high-recall on ~91% of traffic,
  confidence-gated; everything below the gate falls through.
- STAGE 2 — RECURSIVE, 7 x (5−X): the long-tail engine over the deep seven with the
  remaining verbs, run conscience-style: propose a deep kind, apply CARRIES-INVERSION,
  re-classify sub-spans, iterate to fixpoint; the +1 (Record) and mutation handling live
  here, as the steward's original DMA-reduction plan specified.
- THE KEY MOVE — carries-inversion: deep kinds arrive WEARING surface kinds ("a changed
  assumption arrives as a burst of changed Facts"). Stage 2's job is un-laundering the
  wearing: given a surface-classified change, ask which deep kind would wear THIS surface
  here, using the MEASURED boundary channels as priors (Premises/Facts, Model/Facts,
  Structure/Manner — the same three, panel-predicted, Babel-localized). The transition
  map's off-diagonal structure is the recursion's prior, which is what "uses REG to map
  the space" cashes out to.

## Finding X (an empirical design parameter, not a choice)

X = how many of the five CEG-surface verbs belong to the fast stage. Evidence in hand:
verb-kind determinacy from the alignment runs — delegates_to->Rules (3/3 both grammars),
withdraws->Record (3/3 both), recants->Facts (3/3 CEG, 2/3 REG v0.2); scores and
supersedes split everywhere. Fast-legible verbs are those with determinate act-kind
signatures: X is 2 (delegate, withdraw) or 3 (+recant). carries is stage-2's verb BY
CONSTRUCTION (it is the wearing operation the recursion inverts); scores/supersedes carry
the ambiguity that needs recursion.
STAKED EXPERIMENT (H3ERE2-X, owed its own prereg): run stage-1 candidates X=2 and X=3 on
the curated corpus + the sealed wild units; X = the split maximizing stage-1 coverage x
agreement at a frozen confidence gate, with stage-2 load as the cost term. No X chosen
before that runs.

## Fences

Design note only; nothing here is built or claimed. The agent-side implementation belongs
to CIRISAgent/RATCHET (issue to be filed after the X experiment); REG remains lab-frame —
H3ERE2 uses REG's MAP (the object + measured channels), not REG-as-trust-infrastructure.
