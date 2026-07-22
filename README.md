# CIRISOntology

**What we think is true, how we decide what is true, and how we decide what matters —
with the claims machine-checked and every one of them carrying the observation that would
prove it wrong.**

This is a clean seed. It deliberately inherits no experimental history and no accumulated
caveats. Predecessor work exists and is not repudiated; it is simply not imported, because a
stance that can only be understood through its own errata has stopped being a stance.

## The three documents

| File | Question it answers |
|---|---|
| **[`CIRISOntology/Stance.lean`](CIRISOntology/Stance.lean)** | What do we currently claim, how strongly, and what would falsify each claim? |
| **[`epistemology.md`](epistemology.md)** | How do we determine what is true — and which parts of that can a machine check? |
| **[`axiomology.md`](axiomology.md)** | How do we determine what is valuable? |

The stance lives in the Lean, not in prose. The published page is *generated* from it, so the
page cannot drift from the repository: to change what we claim in public, you change the
machine-checked source and CI republishes.

## The shape of a claim

Every claim carries four things, and the type system enforces the fourth:

- **headline** — what it says, in one line
- **plain** — what it means for a general reader
- **status** — `proved` · `measured` · `open` · `wager`, never rounded up
- **kill** — what observation would falsify it — **mandatory, not optional**

A claim with no kill is not a claim about the world, and cannot be constructed.

Two provenance fields are audited on top: a claim marked `proved` must name the
machine-checked declarations that carry it, and a claim marked `measured` must name where
its measurement record lives — for this seed, the predecessor programme at
[CIRISAI/coherence-ratchet](https://github.com/CIRISAI/coherence-ratchet). Declaring either
status without its backing fails the audit, as does attaching backing to a claim that does
not claim it.

## The stance in one paragraph

Coordination is **one quantity** — the total dependence of a joint state over all interaction
orders. Our instrument reads only its **second-order (pairwise) part**, so it is a
**lower-bound instrument**, and a floor reading is **not** an absence. It reports **shape,
never scale**. Where the missing higher-order part has been measured on a natural substrate
it was consistent with zero — so the instrument's slack is *measured*, not assumed. But that
hidden coordination **is constructible**, and anything built that way is invisible to
pairwise monitors, which report their *safest* score on it. Whether order we cannot account
for is selected or intended is **not settleable by measurement**. Physics supplies no ought.

## Verification

```bash
lake exe cache get && lake build      # build (CI adds --wfail)
lake env lean Audit/AxiomAudit.lean   # the gate that decides
lake exe report site                  # generate the published page + figures
```

The audit is the load-bearing check. It asks the proof assistant what each theorem actually
depends on — no admitted gaps, nothing outside the standard axioms, dependency sets pinned in
**both** directions, every claim carrying a falsifier, and the gates advertised as
machine-checked being exactly those enforced. Textual greps and `--wfail` run first but are
not trusted alone; `epistemology.md` §5 explains precisely how each of them can be defeated.

## License

[AGPL-3.0](LICENSE).

## Honest scope

The gates that a machine can enforce are enforced. The ones it cannot — that a
pre-registration truly predates a result, that a null is the *right* null, that a stated
domain is the honest one — are marked as human commitments and not dressed up as checks. CI
cannot make us honest. It can only make dishonesty require a deliberate act rather than a
lapse, which is the most any tooling can do.
