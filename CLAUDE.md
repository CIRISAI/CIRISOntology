# CIRISOntology — Claude Code Context

## What this is

CIRISOntology is a **clean seed**. It carries the current maximal stance, the rules by
which values are chosen (`axiomology.md`), and the rules by which truth is determined
(`epistemology.md`) — and nothing else. It deliberately inherits no experimental history,
no accumulated caveats, and no prior campaign's file tree. Predecessor work exists and is
not repudiated; it is simply not imported, because a stance that can only be understood
through its own errata has stopped being a stance.

**This file states the current stance only.** History belongs in git. Do not re-litigate it
here and do not import its hedging into new work: state the stance, then test the stance.

## CURRENT STANCE

The stance lives in **`CIRISOntology/Stance.lean`**, not in this file, and not in prose
anywhere else. That is deliberate: the published page is generated from that source, so the
page cannot drift from the repository. To change the stance, change the Lean.

Every claim carries four things, and the type system enforces the fourth:

| | |
|---|---|
| **headline** | what it says, in one line |
| **plain** | what it means for a general reader |
| **status** | `proved` (machine-checked here) · `measured` · `open` · `wager` |
| **kill** | what observation would falsify it — **mandatory, not optional** |

A claim with no kill is not a claim about the world, and cannot be constructed. On top of
the four, the audit enforces provenance bidirectionally: `proved` requires named
machine-checked witnesses, `measured` requires a basis naming where the measurement record
lives (the predecessor programme, CIRISAI/coherence-ratchet) — and neither backing may
appear on a claim of any other status.

In one paragraph: coordination is **one quantity** — the total dependence of a joint state
over all interaction orders. Our instrument `S = −ln det C` reads only its **second-order
(pairwise) part**, so it is a **lower-bound instrument**, and a floor reading is **not** an
absence. It reports **shape, never scale**: no magnitude, no unit, no construction datum is
recoverable from it. Where the missing higher-order part has been measured on a natural
substrate, it was consistent with zero — so the instrument's slack is measured, not assumed.
But that hidden coordination **is constructible**, and anything built that way is invisible
to pairwise monitors — which report their *safest* score on it. Whether order we cannot
account for is selected or intended is **not settleable by measurement**, and we call our
answer there a wager. Physics supplies no ought.

## Formal core (one line each; full statements in the Lean)

| Object | Where |
|---|---|
| `S_pairwise`, `S_pairwise_identity` — the instrument, and its floor reading on a zero-correlation state | `Core/Coordination.lean` |
| `not_computable_from` — the domain argument (a lossy summary cannot output what it discarded) | `Core/Coordination.lean` |
| `provenance_line` — no upstream construction datum is a function of the correlation matrix | `Core/Provenance.lean` |
| `Gate`, `Gate.plain`, `Gate.mechanized` — the honesty gates, with an honest flag for which are CI-enforced | `Core/Epistemics.lean` |
| `Claim`, `Status`, `stance`, `summary` — the published claims; `proved` claims name audited witnesses, `measured` claims name their basis (the predecessor record, CIRISAI/coherence-ratchet) | `Stance.lean` |

Records whose fields are `True` are **recorded commitments, not proofs**. This is never
blurred: `Gate.mechanized` states, per gate, whether CI enforces it or a human must.

## Discipline (load-bearing — these rules are the falsifiability, keep them)

The full set with reasoning is `epistemology.md`; the short form:

1. **Pre-register.** Method and the meaning of every possible answer, written down before any
   result is seen.
2. **Stake kills first**, and make them **separable** — each falsifier takes down its own
   claim and nothing beneath it.
3. **Match the null to the data's generative structure.** Discrete data needs a discrete null.
   This is the most common way to fool yourself and it has cost us a headline result.
4. **Disclose the tied fraction** before believing any rank-based statistic.
5. **Control estimator bias** with a shuffle/permutation floor.
6. **A residual is never support.** Support comes only from confirmed advance predictions.
7. **Report the fired kill as plainly as the survival**, and **keep the dead claim in the
   record, marked dead.**

## Layout

```
CIRISOntology/            # the Lean library
  Core/{Coordination,Provenance,Epistemics}.lean
  Stance.lean             # the published claims — single source of truth
axiomology.md             # how values are determined
epistemology.md           # how truth is determined + the CI mechanization
.github/workflows/        # CI (verification gates) and CD (publish the page)
```

## Style discipline

- **Current stance, stated plainly.** Equivocation is not humility and it is not
  falsifiability — the kill conditions are.
- **State strength honestly and never round up.** `proved` means machine-checked *here*;
  `measured` names its domain and precision; `wager` is a choice, not a result.
- Where a proof is open, say so and name the open step. Where a route is closed, record it
  once and move on.
- No claim enters the stance without a kill. No process commitment is advertised as
  machine-checked.
- Plain language is a requirement, not a courtesy: if a claim cannot be stated so a general
  reader can grasp what would falsify it, it is not yet understood well enough to publish.
