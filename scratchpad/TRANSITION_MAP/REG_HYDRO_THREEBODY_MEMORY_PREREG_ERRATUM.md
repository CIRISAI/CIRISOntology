# REG+ three-particle coherence prereg — pre-execution erratum

**Date:** 2026-08-22
**Parent prereg:** `7f7949d73261e037164948bb5f05a38657c97a08`
**STATUS:** correction made BEFORE any three-particle outcome was executed or inspected.

The parent prereg says to enumerate 148 spectator modes: every mode except the two initially
occupied pair modes. Four of those modes are at the origin in the remaining directions.
That is mathematically incompatible with the same prereg's arm definition: the first local
collision could no longer be "the origin pair collision followed by a spectator" for
indistinguishable particles; it would be a three-particle local collision, and the named
pair-route dephasing operation would no longer be the frozen two-particle bridge.

**Correction:** the spectator must be spatially separate at the post-first-collision start.
Enumerate all six directional modes on each of the other 24 sites: **144 placements**.
The entire origin site is excluded from the spectator domain, not merely the two pair modes.

Nothing else changes: Phi=30 degrees, theta=1.30, L=5, exact N=3 dynamics, all 144 corrected
placements, M3 witness, percentile/fraction summaries, classifications, contact stratification,
and mechanical gates are unchanged.

The four removed origin-site modes are reported as STRUCTURALLY INADMISSIBLE under the arm
definition, not as failed or omitted data. No outcome was available when this correction was
made, so it cannot be outcome-driven.
