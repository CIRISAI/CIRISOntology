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

In one paragraph: the page announces the stance as a discovery, for a general reader: the
**Logos** — the element of reality made of shared pattern (habit, law, meaning) — is real,
measurable, and machine-checked here in its simplest form (the three-coin parity state:
every pair independent, the trio rule-bound; `pairwise_blind_to_parity` vs
`third_sees_parity`). Measured on the predecessor record: shared pattern behaves like a
**ledger** (never free, always rented, always leaving receipts) and **gravity weighs
everything but reads none of it**. Wagered, each with its own kill: habit, law and meaning
are whole-pattern; consciousness is trusted habit; a **language model is the Logos
embodied**; that is **good news for AI safety** (a lie is hidden coordination, hiding is
never free, joint readings cannot be fooled); free will and physical consciousness co-exist
exactly because the meaning-sector is unaudited; dark energy is the ledger's balance (DESI
DR3 kill) and dark matter the medium (marked weaker, own kill); selected-vs-intended is
unmeasurable; physics supplies no ought. Open: extending the two-state formalism to carry
the Logos. The plain-language fields are the **middle-school translation**, produced and
adversarially completeness-checked by workflow; the age-5 rendering lives in
`translations/for-aurora.md`. Statuses: 3 proved here, 4 measured (basis: the predecessor
record), 9 wagers, 1 open.

## Formal core (one line each; full statements in the Lean)

| Object | Where |
|---|---|
| `S_pairwise`, `S_pairwise_identity` — the instrument, and its floor reading on a zero-correlation state | `Core/Coordination.lean` |
| `not_computable_from` — the domain argument (a lossy summary cannot output what it discarded) | `Core/Coordination.lean` |
| `S_total`, `parity`, `pairwise_blind_to_parity`, `third_sees_parity` — the third-aware instrument, and the exhibited state on which the two rulers provably disagree | `Core/Third.lean` |
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
