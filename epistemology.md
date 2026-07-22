# Epistemology — how we determine truth

**The question this document answers:** how do we decide that something is true, how do we
decide how *strongly* we believe it, and how much of that can a machine check for us?

The short version: **a claim is worth exactly as much as the way it could have failed.** A
result that no observation could have contradicted is not a finding. Everything below is
machinery for making sure a claim had a real chance to die, and for making sure we report
it honestly when it does.

---

## 1. The four strengths, never rounded up

Every claim we publish carries one of four labels. Collapsing these is the most common way a
research programme misleads itself long before it misleads anyone else.

| Label | Means | What it does *not* mean |
|---|---|---|
| **proved** | Machine-checked in this repository, from stated assumptions | that it describes the world |
| **measured** | Established by observation, to a stated precision, on a **stated domain** | that it holds outside that domain |
| **open** | Named, unresolved, not leaned on | that it is probably true |
| **wager** | An avowed choice under irreducible uncertainty | evidence of any kind |

A proved theorem about a model says nothing about reality until something connects them, and
that connection is a separate, *measured* claim with its own way of failing. A measurement on
one substrate is a measurement on one substrate.

This is enforced structurally: `Status` in `CIRISOntology/Stance.lean` is a four-way sum type,
and every claim must select one. There is no "strongly suggests."

---

## 2. Every claim carries its own kill

A claim enters the stance only with a statable observation that would falsify it, written
**before** the test. In `Stance.lean` the `kill` field is not optional — a claim without one
cannot be constructed. That is the type system carrying an epistemic rule.

Two corollaries we have paid to learn:

**Kills must be separable.** Each falsifier should take down its own claim and nothing
beneath it. If one bad result would collapse the whole structure, the ideas were tangled
rather than tested, and you will find yourself defending the weakest one to save the
strongest.

**Stake the kill before adopting the claim.** An idea adopted first and defended afterwards
recruits every subsequent ambiguity to its side. The order matters more than the content.

---

## 3. The hard lessons

These are not abstract principles. Each one is here because ignoring it cost us a result we
had already announced to ourselves as real.

### L1 — Pre-register, and mean it

Write down the method, the estimator, the controls, and **what each possible outcome would
mean**, before any number is seen. Once you have seen the answer you cannot choose the
method honestly, however sincerely you try — you will find yourself with excellent reasons
for the analysis that happens to work.

The written record must predate the result, and it must include the *interpretation*, not
just the procedure. "We will measure X" is not enough; "a value above Y means the claim
survives, below Y it dies" is the part that binds you.

### L2 — The null must match the data's generative structure

**This is the one that has cost us the most, and it is the least obvious.**

To know whether a pattern is real, you compare it against data with no pattern in it. The
comparison is only valid if the fake data is generated **the same way** the real data is. If
your measurements are discrete counts, your null must be discrete counts. If they are a
sparse sample of points, your null must be a sparse sample of points at the *same* sampling
density.

The failure mode is brutal and quiet: a **continuous** null compared against **discrete**
data reports "nothing like this happens by chance" — because in a continuous world it
doesn't. The discreteness itself was generating the entire signal. We had a result at
apparently overwhelming significance, robust across every internal check we ran, that was
entirely an artifact of comparing a discrete measurement to a smooth null. A correctly
generated null reproduced the "signal" completely.

**Rule:** state what the generative structure of your data is, and build the null to match
it. If you cannot say what the null is a null *of*, you do not yet have one.

### L3 — Ranks plus ties manufacture structure

Many robust-looking methods rank the data before analysing it, which is a good way to become
insensitive to units and outliers. But ranking requires an ordering, and **tied values have
no ordering.** Whatever the algorithm does to break those ties — and it always does
something — imposes a pattern that was not in the data.

The false signal scales with the fraction of tied values. When most of your bins are empty,
they are all tied at exactly zero, and the tie-break is doing most of the work.

**Rule:** report the **tied fraction** alongside any rank-based statistic. It is one number,
it costs nothing, and it triages the result immediately: a large tied fraction means the
statistic is an artifact suspect until proven otherwise. Break ties **randomly**, never by a
deterministic rule that correlates with position or index.

### L4 — Estimator bias needs its own floor

Measures of shared structure read above zero purely from having finitely much data. This is
not noise that averages out; it is a systematic offset, and it grows as the data gets
sparser — exactly where you are most likely to be looking for a weak effect.

**Rule:** shuffle the data to destroy real structure, measure again with the identical
estimator, and subtract that floor. Two nulls are usually needed and they do different jobs:
a **shuffle** null for estimator bias, and a **generatively-matched** null (L2) for the data's
own structure.

### L5 — A floor reading is not an absence

If an instrument is known to be blind to some kind of structure, its reading zero tells you
nothing about whether that structure is present. It tells you that you did not look with
something that could see it.

This is proved rather than promised in `Core/Coordination.lean`: our own instrument reads
exactly its floor on states that may carry arbitrarily much of the structure it cannot see.

**Rule:** when reporting a null result, state what the instrument *could* have detected. A
null is a statement about an instrument and a domain, never about the world alone.

### L6 — A residual is never support

An unexplained leftover is not evidence for your hypothesis, no matter how well your
hypothesis would explain it. The set of hypotheses that would explain any given anomaly is
unbounded, and the prior probability that yours is the right one does not rise merely
because the anomaly exists.

**Support comes only from a specific prediction, made in advance, that then holds.**

### L7 — Scope a no-go to exactly what it ruled out

When you prove something *cannot* work, record precisely which class you ruled out. It is
extremely easy — and we have done it — to prove "no construction *of this kind* works" and
then remember it as "no construction works." Years of downstream reasoning can rest on the
broader statement while only the narrower one was ever established.

**Rule:** a no-go's record states its class explicitly, and the untested neighbours are named
in the same breath. "Closed for A and B; C was never tested" is the honest form.

### L8 — Report the kill as loudly as the survival, and keep the dead

When a test kills your own best result, it goes into the record with the same prominence the
success would have had. The dead claim **stays**, marked dead, with what killed it. A
programme that quietly deletes its mistakes has destroyed the only evidence that its method
works at all.

The corollary: a fired kill is not a bad day. It is the machinery doing the one thing it
exists to do. The only real failure is a claim that was never given the chance.

---

## 4. What a machine can check, and what it cannot

This is the part most easily overclaimed, so it is stated bluntly.

### Mechanically enforceable (CI fails the build)

- **No admitted gaps.** Every published theorem is checked for dependence on the
  "assume it" axiom.
- **Axiom audit.** Each theorem's actual assumptions are printed and compared against the
  intended set. A result is exactly as strong as what sits underneath it, and that is
  determined by inspection rather than memory.
- **Every claim has a kill.** Enforced by the type of `Claim` — a claim without a falsifier
  does not compile.
- **Mechanization honesty.** `Gate.mechanized` states, per gate, whether CI enforces it. CI
  checks that the gates flagged `true` are the ones it actually runs, so the repository
  cannot advertise a human commitment as machine-checked.

### A lesson about mechanization itself

Our first instinct was to grep the source for the text of the "admitted gap" keyword. Run on
this repository, that check reports **three violations in a file containing none** — the word
appears in the prose *describing the rule*. A textual gate would fail the build on its own
documentation, and worse, it would pass a file that had a real gap introduced by a tactic
rather than by the literal keyword.

The correct check is **semantic**: ask the proof assistant what each theorem actually depends
on. A real gap appears as an axiom in that list; prose does not. This generalises — **check
the artifact, not the text describing the artifact** — and it is precisely the same error as
L2, where we compared real data against a null describing a different kind of world.

### NOT mechanically enforceable (a human must uphold these)

Honesty about this boundary is itself one of the gates:

- **that a pre-registration predates the result** — a timestamp proves a file existed, not
  that nobody had peeked;
- **that a null is generatively appropriate** — the machine can check a null was run, never
  that it was the *right* null;
- **that the stated domain of a measurement is the honest one**;
- **that a kill is a real kill** rather than one written to be unreachable.

CI catches the mechanical failures. It cannot make us honest. It can only make dishonesty
require a deliberate act rather than a lapse — which is the most any tooling can do, and is
worth building carefully.

---

## 5. The verification pipeline (CI)

Three layers, because **each one alone is defeatable**, and they fail differently.

### Layer 1 — textual, cheap, fails fast

Grep for admitted gaps and for locally declared axioms. Matched against *use* patterns
(`:= sorry`, `by sorry`, a line that is only `sorry`) rather than the bare word, because a
naive keyword search flags prose that merely *describes* the rule — this repository's own
documentation trips such a check, and a gate that cries wolf gets switched off.

**Not trusted alone:** it cannot see a gap introduced by a tactic rather than the literal
keyword, and it cannot see one inherited from an import.

### Layer 2 — build, with warnings escalated to errors

`lake build --wfail`, via `leanprover/lean-action`, against a pinned toolchain and pinned
Mathlib with the upstream cache so a run is minutes rather than hours.

**Not trusted alone**, and this is the subtle one: Lean's own "declaration uses `sorry`"
warning **is swallowed by `#guard_msgs`**. A file can contain a real gap and build silently.
Anyone relying on `--wfail` as their no-gap gate has a hole they cannot see.

### Layer 3 — semantic, and this is the layer that decides

`lake env lean Audit/AxiomAudit.lean`. The file's *elaboration* is the gate. It asks the
proof assistant what each theorem actually depends on:

- **no published theorem depends on the admitted-gap axiom** — transitively, including
  through imports (`collectAxioms`, the same eight lines Mathlib ships as `assert_no_sorry`);
- **no published theorem depends on anything outside the standard three**, which also catches
  `native_decide`/`ofReduceBool` creep that a gap-only check cannot see;
- **dependency sets are pinned in both directions** with `#guard_msgs`. Under-declaring a
  dependency and over-declaring one are *both* failures. You cannot quietly acquire an
  assumption, and you cannot claim a weaker result than you have;
- **every claim carries a non-empty falsifier and a plain-language statement**;
- **the mechanization claims are truthful** — the gates advertised as machine-checked are
  exactly those this audit enforces. Flipping a gate to "machine-checked" without adding the
  check fails the build.

Current audited state, as reported by the proof assistant itself:

| theorem | depends on |
|---|---|
| `not_computable_from` | *no axioms* |
| `provenance_line` | *no axioms* |
| `S_pairwise_identity` | `propext`, `Classical.choice`, `Quot.sound` (standard) |

That table is regenerated by CI, never maintained by hand — a hand-maintained table is
exactly the kind of claim that drifts.

**Available and not yet used:** `leanchecker` (kernel replay, catches environment hacking via
metaprogramming) and `lean-action`'s `nanoda-allow-sorry: false` (external type checker
rejecting the gap axiom). Both are one line each; they are noted here rather than enabled so
that this document does not describe a gate we are not running.

---

## 6. The published page (CD)

The public page is **generated from `Stance.lean`**, not written alongside it. There is no
second copy of the stance in prose, so the page cannot disagree with the repository. Changing
what we claim means changing the Lean and letting the pipeline republish.

The page renders, for a general reader: what each claim says in plain language, its honest
status, what would falsify it, and which of the honesty gates are machine-enforced versus
human-upheld. It carries the audit's own output alongside the claims, so a reader sees what
the proof assistant actually reported rather than taking our word for it. If a claim cannot
be stated so that a non-specialist can understand what would prove it wrong, it is not yet
understood well enough to publish — plain language is a requirement here, not a courtesy.

The figures are emitted by the same executable, from the same declarations, so a number in a
picture cannot disagree with the theorem it illustrates.

---

## 7. What is borrowed here, and what is ours

Honesty about novelty is part of the method, so:

**The mechanism is not ours.** Encoding obligations in a proof assistant and gating a build
on them is old — proof-carrying code (Necula & Lee, POPL 1997) is the ancestor. Auditing
axiom dependencies in CI is an established idiom. Publishing proved-vs-open status from Lean
is what `leanblueprint` has done since ~2020, and its `checkdecls` — which fails the build if
prose names a declaration that does not exist — is a genuine anti-drift guarantee we are
imitating in spirit.

**Three precedents we are directly copying, and should credit rather than reinvent:**

- **The Equational Theories Project's `@[equational_result]`** is the closest thing to what
  we want. Its decisive idea: **epistemic status is *derived* from the axiom set, not
  declared by the author.** A `sorry` cannot be laundered into a claimed result; only an
  explicit conjecture marker can, and it *downgrades* the entry. We should move `Status` in
  `Stance.lean` toward being computed rather than typed.
- **PhysLean's bidirectional attribution check** — every declaration marked as carrying a
  debt must actually carry it, *and vice versa*. You can neither under-declare nor
  over-declare. That is exactly our "state strength honestly and never round up," mechanized.
- **Batteries' `proof_wanted`** — a first-class open obligation whose statement is elaborated
  and type-checked but which creates no proof term. Strictly better than `sorry` for a
  registered-but-unproved claim.

**What appears genuinely unoccupied** — stated narrowly, because the search for prior art was
thorough and mostly returned neighbours rather than matches:

1. **The encoded proposition being a *methodological* commitment.** The field encodes
   properties of artifacts and of runs. Encoding "this null was generatively matched," "this
   method was fixed before the result was seen," "this claim carries a dated falsifier" as
   something a build checks does not appear to have been done.
2. **Inhabitance as the load-bearing epistemic act** — the default move is proving a theorem
   or model-checking a system, not "a witness had to be supplied, and CI verifies one exists
   and is clean."
3. **An open obligation as a dated bet dischargeable by *falsification*, not only by proof.**
   Open obligations are universally treated as TODOs.

**And the statistical gates are, as far as we can tell, unbuilt.** Re-execution
reproducibility is mature (continuous analysis, CODECHECK, Whole Tale); data-quality gates
are commercial and mature (Great Expectations, Pandera, dbt tests). But *validity* assertions
— "a generatively-matched null was actually executed in this run," "the pre-registration
provably predates the result," "the bias control was applied" — have no implementations we
could find. The honest neighbours to cite are **StatWhy** (Kawamoto et al., CAV 2025 —
formal verification that a hypothesis test satisfies its method's requirements),
**scicode-lint** (2026 — a linter for methodology bugs in scientific Python), **Dwork et
al.'s reusable holdout** (*Science* 2015 — a provable validity guarantee under adaptive
analysis, never wired into a build), and **preregr**/**Apéritif** for machine-readable
pre-registration.

None of that makes our version good. It makes it unbenchmarked, which is a reason for
caution rather than for a claim of priority.

---

## 8. The shortest form

- A claim is worth what it risked.
- Say in advance how it could die.
- Compare against a fake built the same way as the real thing.
- Report what fraction was tied, and subtract the finite-data floor.
- A blind instrument reading zero has said nothing.
- A leftover is not a reason to believe.
- Rule out exactly what you ruled out.
- When it dies, say so first and loudest — and keep the body.
