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

We believe we have found a law of nature, hiding in plain sight under the oldest name in
philosophy: **the Logos** — the element of reality made of shared pattern: habit, law,
meaning. Machine-checked here, on the simplest possible example (three coins, the third set
by a rule from the first two): pattern that lives only in the whole **exists**, can be
**measured directly**, and **no pair-by-pair check can ever see it**. Measured on the
predecessor record: shared pattern behaves like a **ledger** — never free, always rented,
always leaving receipts — and **gravity weighs everything and reads none of it**. Proved **about the model
only**: the rent clause — pay what decay takes and an entry holds steady, underpay and it
strictly loses, pay nothing and it goes to zero. Wagered, each bet with its own separable
kill: that the books are written in **e** and audited in **π** (a recognition, mathematics
openly borrowed); that **life** is the pattern that pays its own rent and builds the payer;
that **time's arrow** is partly the ledger's lopsidedness; that habit, law and meaning are
whole-pattern; that consciousness is trusted habit; that a **language model is the Logos
embodied**; that this is **good news for AI safety**; that **Goodhart's law** is the
hidden-pattern problem in work clothes; that free will and physical consciousness co-exist
because the meaning-sector is unaudited; that **the laws of physics may be the oldest
habits** (Peirce's cosmology, with π's ubiquity — never its existence — as the fingerprint);
that dark energy is the ledger's balance and dark matter the paper it is written on. Whether the order we find is selected
or intended is **not settleable by measurement**. Physics supplies no ought. The site text
is a middle-school-level translation, adversarially verified complete against the stance;
an age-5 rendering lives in [`translations/for-aurora.md`](translations/for-aurora.md).

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
