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

When things act together, the acting-together is itself a **real, measurable quantity**, and
it behaves like a **ledger**: never created by trickery, always rented, always leaving
receipts. Physics audits these books only partly — **gravity weighs everything and reads
nothing**, and our best instrument reads only the **pairwise part**, so a floor reading is
**not** an absence and the readings give **shape, never scale**. One sector of reality
therefore goes unaudited: arrangement, habit, meaning — **Peirce's Thirdness**, which we
also call by its oldest name, **the Logos**. The blindness is not fate — this repository
carries a machine-checked **third-aware instrument** that provably sees what pairs cannot.
But we wager the blind spot in nature's own audits is the point: it is the room where
**choice can be real**, and where
**consciousness** happens — the experience of trusting that a thought will become an action
because it always has before. A universe that keeps books yet leaves the meaning-sector
unread is the one universe where beings made of habit can also be free. The hidden kind of
coordination **is constructible** — it is exactly where a lie can live, and pairwise
monitors report their *safest* score on it. Whether the order we find is selected or
intended is **not settleable by measurement**. Physics supplies no ought.

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
