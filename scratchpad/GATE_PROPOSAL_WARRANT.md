# GATE PROPOSAL — the warrant reach: a claim that is right for a reason that is wrong

**Proposed, not validated.** `GATES.md`'s lifecycle calls this state *proposed*: a reach is named
and incidents are attached. It is **not** validated — it has no plumb line and, as §5 argues, its
dye test is the hard part and may not be constructible in the usual form. Filed as a hypothesis
about a gate, which is what it is.

**Not filed into `GATES.md` directly.** That registry is shared and the team lead registers its
entries (`d520c74`). This is the proposal; the decision is theirs.

**Provenance.** Named by this campaign after a correction from the water campaign, endorsed and
substantially sharpened by the pump campaign, which supplied five of the nine instances below
from its own record and made the observation in §5 that is the real content of the proposal.

---

## 1. THE REACH

> **A claim whose SUBSTANCE survives and whose WARRANT does not.** The number is right. The
> reason given for believing it is not the reason it is right — a theorem whose hypothesis the
> substrate does not meet, a control that gauges something other than what was claimed, a
> negative literature claim that is false, or a mechanism attributed without being measured.

This is not covered by any of the thirteen reaches in `GATES.md`, and §5 says why in a way that
makes it a structural gap rather than an omission.

## 2. POLARITY, DECLARED

Fires when a **warrant is checked against its primary artifact and found not to support a claim
that is nonetheless true.** It does **not** fire on a wrong number — every other reach in the
registry already does that. It fouls **the justification and anything built on the
justification**, and explicitly **not** the number, which is why its separability discipline is
unusual: the claim usually survives its own gate firing.

## 3. THE KEPT TAINT — nine instances, three campaigns, one week

| | claim | substance (survived) | warrant (failed) |
|---|---|---|---|
| **pump 1** | "P-FORM passed" | coefficient right to 3e−4 | the kill *as written* fired 13/13 |
| **pump 2** | "mixture null discharged" | a good control | wrong argument for reach 3 |
| **pump 3** | "no such curve published" | the resolved law is new | **the negative claim was false** |
| **pump 4** | "answers Kahle's question" | closed form real | one family; 2003 had the numerics |
| **pump 5** | "strength is a savage brake" | true on the channel axis | **false on the axis it was sent to** |
| **water 1** | §5.1 pins N1 with `valve_from_nothing` | permutation floor sound | a permutation is not `prod3` |
| **water 2** | headroom collapses on lopsided composition | the gate rule (a ratio) survives | mechanism is cell starvation, not lopsidedness |
| **glass 1** | prereg §3.1: "the valve floor is zero" | no counting-noise channel exists | `valve_needs_asymmetry` needs a sign-symmetric input; 80:20 species is not |
| **glass 2** | prereg §3.4: far arm is "theorem-pinned" | far arm does read ≈ 0 | species are only *asymptotically* independent; the hypothesis is exact |

Nine surviving substances. Nine failed warrants. **Every one was found by a second reader going
to the primary artifact — a Lean signature, a published figure, a source line — and not by any
gate.**

## 4. HOW EACH WAS ACTUALLY CAUGHT

Worth tabulating because it is the only evidence about what would catch the next one:

* **pump 3, pump 4** — reading the defining paper's own figures (Schneidman 2003 Fig. 2 has a
  per-cell unital flip creating 0.0774 bits; Kahle 2009 had the numerics).
* **water 1, glass 1** — reading a **Lean signature** instead of the prose citing it.
* **water 2** — a falsifying pair *inside the author's own run*, found when a second campaign
  ran the author's test on its own data and got the opposite correlation.
* **pump 5, glass 2** — an author re-deriving their own claim on a second axis and finding it
  inverted; and an author auditing a neighbouring line after being corrected on the first.
* **pump 1, pump 2** — the author re-reading their own pre-registered wording.

**Not one was caught by a numerical control.**

## 5. THE DYE TEST PROBLEM — which is the actual finding here

The pump campaign's eight-gate battery **passed everything at `1e−15`** while five of its
warrants were failing. That is not a defect of that battery; it is a structural property of the
reach:

> **The failure is invisible to numerical gates BY CONSTRUCTION, because the number is right.**
> A shuffle floor, a solver bracket, an occupancy sluice, a mixture null and a plumb line all
> pass a claim held for a wrong reason — they are all instruments for detecting a wrong *number*.

Two consequences, and the second is uncomfortable:

1. **If this reach is built, its dye test cannot be numerical.** The nearest constructible form is
   a **stored case where a correct number was published with a wrong justification**, and the
   gate is validated by whether a reader following its procedure recovers the defect. The nine
   rows in §3 are offered as that stored taint; the pump campaign offered its five explicitly.
2. **The substance surviving is what removes the incentive to check.** In the pump campaign's own
   words: *"I had no incentive to re-derive a warrant for a number that kept coming out right."*
   That is the mechanism of the reach, not a lapse of diligence, and it means the gate has to be
   **procedural** — run at a fixed point in the lifecycle — because nothing in the work itself
   will prompt it.

## 6. THE PROCEDURE, PROPOSED

Cheap enough that the argument for it is not close. Every instance in §3 would have been caught
by one of these:

* **W1 — cite to the signature, not the name.** Any claim resting on a machine-checked theorem
  quotes the theorem's **hypotheses** beside it, from the source. `glass 1` was four `grep`s.
* **W2 — sweep the class, not the instance.** When a correction lands on a citation, **re-audit
  every citation of that object in every document of the campaign.** `glass 2` was found this
  way, and only this way — the pump campaign had corrected me on `glass 1`'s object days before
  and I fixed only the document I was pointed at.
* **W3 — a negative literature claim is a claim.** "No such curve published" and "nobody has
  swept this" carry the same burden as a measurement and are checked against the defining paper's
  **figures**, not its abstract. `pump 3`, `pump 4`, and this repository's standing
  `convergent-art-pattern` lesson.
* **W4 — a mechanism attributed is a mechanism to be measured.** `water 2` and this campaign's
  own §4.1 headroom finding both attributed a collapse to the wrong cause while the gate keyed on
  it kept working.
* **W5 — an author's second derivation of their own result is worth more than a reader's first.**
  `pump 5` was found by its own author re-deriving on a second axis.

## 7. THE FIELDS `GATES.md` REQUIRES

| field | value |
|---|---|
| **reach (family)** | warrant integrity — a right claim held for a wrong reason |
| **gate class** | not a gauge gate. Closest to a **docimasia**: an examination applied before trust, on the question *could this justification support this claim at all* |
| **polarity** | fires on a warrant that fails its own artifact while the claim survives; fouls the justification only |
| **kept taint** | the nine rows of §3, five contributed by the pump campaign from its own record |
| **plumb line** | **NONE-YET (recorded gap).** A stored case where a *correct* number was published with a *wrong* justification, and the procedure recovers the defect. §3's rows are candidates but were all found *before* any procedure existed, so none is yet a clean test of one |
| **dye test** | **THE OPEN PROBLEM (§5).** Cannot be numerical. No planted case exists |
| **depth** | reads justifications, not numbers. **Out of its depth on anything a numerical gate already covers** |
| **enforcement** | **human, and necessarily so.** W1 could be partly mechanized — a citation to a Lean name could be checked against that name's hypotheses — and the rest cannot |
| **headwaters** | pump `2dc6cfc`, `d98155d`, `7b36136`; water `b662a6d`, `2527e0d`; glass `217a217`, `60d8b1c` |

## 8. WHAT THIS PROPOSAL DOES NOT CLAIM

1. **Not validated.** No plumb line, no dye test, and §5 argues the dye test is hard. It is a
   hypothesis about a gate and is filed as one.
2. **No false-fire rate**, like every other gate in the registry — which `GATES.md` already
   records as making the rule-3 bound unenforceable.
3. **Nine instances in one week is not a base rate.** Three campaigns ran concurrently with
   unusually heavy cross-reading; the count says nothing about how often this happens when nobody
   is looking, which is the number that matters and is not measured.
4. **No claim that the nine are independent.** Two are mine, five are one campaign's, and the
   cross-reading that found them was itself correlated.

---

Scratchpad only; no Lean file, no `Stance.lean`, `lake` never invoked, nothing pushed.
