# ADVERSARIAL REFEREE REPORT — RECOGNITION registration

**Filed 2026-08-20, before freeze.** Target documents read in full:
`scratchpad/RECOGNITION_PREREG.md` (921 lines, "READY-FOR-REFEREE") and
`scratchpad/RECOGNITION_PREREG_ADDENDUM_A1.md` (500 lines). Context read: `CLAUDE.md`,
`epistemology.md`, `GATES.md`, `scratchpad/POLYGLOT_RESOURCE.md`,
`scratchpad/GROSS4_FORWARD_PREREG.md`, `scratchpad/POLARITY_PREREG.md`,
`Core/{Generator,WrongKind,Fit,Stack,Surface}.lean`, `scratchpad/plane_annotate.py`,
`scratchpad/plane_corpus/_helper.py`, `scratchpad/gaugetest/analyse_gauge.py`.

**Primary-source verifications performed** (per the brief's instruction not to assert from
memory):

| checked | against | result |
|---|---|---|
| WALS ch. 73 title/author | `wals.info/chapter/73` | "The Optative", Dobrushina / van der Auwera / Goussev — **confirmed**; two values (inflectional optative present 48 / absent 271) |
| WALS ch. 77 title/author/values | `wals.info/chapter/77` | "Semantic Distinctions of Evidentiality", de Haan — **confirmed**; values are a **three-way presence/type** contrast (no grammatical evidentials 181 / only indirect 166 / both direct and indirect 71), **not** the six semantic values T5.6 ranges over |
| WALS ch. 37 values | `wals.info/feature/37A` | "Definite Articles" — **confirmed**; value set includes "No definite, but indefinite article" (45 languages) |
| ISO 24617-2 nine dimensions + three qualifiers | Bunt 2017 (local copy of the PDF text), §2 and §3.4 | **confirmed verbatim**, including Contact Management as DIT++'s tenth and Task Management as DAMSL's, proposed for re-inclusion in §3.4 |
| every Lean name cited by either document | local `.lean` files | all exist: `generator_image`, `record_not_site_generated`, `basePlane_card` (11), `warrant_invisible_to_kind`, `repairable_does_not_factor`, `carrier_inert_under_mention`, `modulate_idempotent`, `depth_counts = [3,2,0,2]`, `surfaceAlt` |
| `Generator.lean` header line quoted "verbatim" in §T5.1 | `Core/Generator.lean` | **confirmed verbatim** |
| `plane_annotate.HARD_CAP_USD` | `scratchpad/plane_annotate.py:18` | `HARD_CAP_USD = 10.0`, single global — **contradicts §5** (see BLOCKER-11) |
| `analyse_gauge.py` | filesystem | exists at `scratchpad/gaugetest/analyse_gauge.py` (cited without path); its stage 1 loads arms **A and C**, not "arm D" |

**Counts: 11 BLOCKER · 16 MAJOR · 11 MINOR.**

---

## 0. A finding that precedes the others: which document is being frozen?

The brief instructs attack on `§0.5`, `§0.6` (idempotency), `§14` (combination readings),
`§15` (order of execution), `G7` (global $6 cap) and `G15` (adaptivity), and on T2's
`SPLIT` vs `NO-HOME` distinction. **None of these exist in `RECOGNITION_PREREG.md`.** They
exist in a *second, structurally different* registration of the same five legs at
`<session-scratchpad>/RECOGNITION_PREREG.mydraft.md` (940 lines, §0–§17, defaults G1–G15),
which pins different values for the same choices. I have refereed **both**, and every
finding below names the document it is against:

- **[D]** = the delivered draft on disk, `scratchpad/RECOGNITION_PREREG.md`
- **[R]** = the rival draft, `RECOGNITION_PREREG.mydraft.md`
- **[A1]** = the addendum on disk
- **[D+R]** = fires only if the two are merged, which the brief's section numbering implies
  is the plan

---

## BLOCKERS

### BLOCKER-1 — the freeze target is ambiguous, and A1 already cites a section that exists in neither document. [A1, D+R]

`A1.1.7`'s CASE—distinct row restrains an escalation by reference to "§0.5-style
candidate-site machinery"; `RECOGNITION_PREREG.md` has no §0.5 (its §0 stops at §0.4), and
neither does the rival draft (whose candidate-site rule is §3). A restraint whose referent
does not exist is unenforceable, and a registration cannot be frozen while its own addendum
points at a section of a document that has not been written.

**Minimal fix.** Name one file as the freeze target in one line at the top of both documents;
replace "§0.5-style candidate-site machinery" with the literal rule it means ("the
CANDIDATE SITE band of §T5.9"); mark the non-frozen draft **SUPERSEDED** in its first line,
in the same commit as the freeze.

### BLOCKER-2 — A1 moves a VOID threshold while declaring itself additive, and misattributes the new value to the document it is amending. [A1 vs D]

`A1.2.4` states: "Fresh-annotation κ **< 0.6** on clear items ⇒ **VOID**, per the delivered
draft's floor." The delivered draft's floor is **κ < 0.4**, twice, in `§T2.5` and `§T5.9`
("chance-corrected mapper agreement κ < 0.4"). A1's opening paragraph claims it "alters no
band, no kill, no VOID condition"; this alters a VOID condition by citation, and the cited
authority says the opposite.

**Minimal fix.** Either write "κ < 0.6, which is *stricter* than the delivered draft's 0.4
and applies to this instrument only", or change to 0.4. Do not leave two floors with one of
them attributed to the wrong source.

### BLOCKER-3 — T1's five primary stakes are entailed by T1's own freeze; the outcome table lists outcomes the freeze forbids. [D §T1.2 / §T1.4 / §T1.5]

`§T1.2` freezes **both** the eleven `RSite` constructors **and** the `RSite.kind` map.
Given that table, all five stakes of `§T1.4` — completeness, image = the eleven, injectivity,
Record excluded, and the transport bijection with `Site` — are immediate arithmetic
consequences and cannot fail except by transcription error. Meanwhile `§T1.5` offers
"DIFFERENT IMAGE — count ≠ 11", "same count, different kinds" and "RECORD BECOMES
SITE-GENERATED" as live outcomes, each of which requires the compiled `RSite` to differ from
the frozen table — which `T1-VOID-1` declares **VOID**. The leg's outcome table and its VOID
condition are mutually exclusive.

**Minimal fix.** Import the rival draft's §6.4 discount verbatim: add to `§T1.0` — "Because
§T1.2 freezes the site list *and* the kind map, §T1.4's stakes are a consistency check on the
freeze, not a result. T1's evidential content is exactly (i) the §T1.6 placebo comparison and
(ii) an independent reader's verdict on the R2 arguments." Then delete the three unreachable
rows from §T1.5 or re-label them "outcomes reachable only under the re-registration of
T1-VOID-1".

### BLOCKER-4 — F1, the failure mode given "real probability", cannot be reported as a result. [D §T1.5, §T5.11, §7.1]

`F1` fires when R2 forces a `transitionStrength` site and the count becomes **12**. A twelfth
constructor is precisely an "addition" to the §T1.2 table, and `T1-VOID-1` says any addition
makes the leg **VOID and it must be re-registered**. So F1 can only ever surface as a VOID,
never as the escalation-to-the-steward outcome §T1.5 describes; and `§T5.11`'s exception
("if T1 fires F1 … §T5.6's three outcomes are re-registered") and `§7` doubt 1 are dead
clauses resting on it.

**Minimal fix.** One sentence in T1-VOID-1: "An addition arising from an R2 derivation
written and dated **before** the image is computed is an **F1 result**, not a VOID; only an
addition made after the image is read voids the leg. The Lean header's dated R2 section is
the evidence, and the steward certifies which case obtains."

### BLOCKER-5 — the anti-tautology control applies the recipe asymmetrically, and the only mitigation that would fix it is optional. [D §T1.3 vs §T1.6]

Generator2's R2 output is **frozen in advance** (§T1.2's eleven rows); the placebos' R2
outputs are frozen **nowhere** — only their mode sets are — so the number of gap sites
Jakobson's six functions or Habermas's three claims "independently yield" is chosen at
authoring time by an author who knows that "not eleven" is the wanted answer. The
DISCRIMINATING verdict is therefore decided by unconstrained authorial freedom over exactly
the quantity the leg exists to audit, and §T1.6's mitigation (iii) — an independent third
placebo — is written as an invitation ("**may** add a third placebo mode set at any time"),
i.e. optional.

**Minimal fix.** Promote (iii) to blocking: "the two placebos' R2 gap arguments must be
authored by an agent with no repository access, not told the target count, and given only
R1–R4 plus the mode set. Without them the placebo leg is **UNGAUGED** and, per T1-VOID-3,
the primary is uncashable." (T1-VOID-3 already supplies the consequence; only the mandate is
missing.)

### BLOCKER-6 — the idempotency discriminator conflates iteration with composition, and two of its three worked examples are not stacking tests. [R §4; consumed by §3 C3, P2.3/P2.4, P5.2/P5.3/P5.4]

The rule is "a candidate axis is a MODULATOR if **stacking it** collapses". Example 1 iterates
**one marker with one argument** ("probably probably p"). Example 2 composes **two different
antecedents** ("if A, if B, then p"), and example 3 composes **two different evidential
values** ("reported that it was inferred that p") — a source *chain*, not a repetition. Under
same-marker iteration all three collapse (hearsay-of-hearsay is hearsay; "if A, if A, then p"
≡ "if A, then p"); under any-composition none do ("probably certainly p" ≠ "probably p"). The
discriminator can be steered to "everything is a modulator" or "everything is a kind" at
scoring time, and it is the C3 criterion of the candidate-twelfth rule.

**Effect on the predictions the brief names:** the certainty prediction (idempotent →
modulator) survives, because it is stated on same-marker iteration. **The conditionality
prediction and the source-of-knowing prediction do not** — both are stated on the broken
convention, and both flip under the repaired one.

**Minimal fix.** Replace the rule's operative clause with: "**stacking** means iterating the
**same value of the same marker**; composing two different values of one axis is
*composition*, tested by C4, not by C3." Then re-stake the conditionality and
source-of-knowing predictions **before** freeze, since both currently predict
non-idempotence on a test that no longer supports it.

### BLOCKER-7 — T5's E1, the author's own prediction, is defined by the frozen statistics to read INDETERMINATE, and the frame does not code the values it ranges over. [D §T5.3 row 1, §T5.4, §T5.5, §T5.6]

`§T5.4` gives **one minimal pair per (category × language)**, so evidentiality yields exactly
three readings; `§T5.5` makes a category determinate only when "≥2 of the 3 language instances
agree". `E1` predicts the evidential values **DISTRIBUTE across Confidence / Model /
Premises** — which, over three instances, is precisely the non-agreement pattern the rule
scores as **indeterminate**. §T5.6 anticipates this for *mappers* ("if the three mappers each
pick a different one … that is indeterminate, not distributed") and never addresses the
identical collision *across instances*, which is where E1 actually lives. Compounding it:
WALS 77A codes a **three-way presence/type contrast only** (verified above), so the six
evidential values E1/E2/E3 range over are not in the primary frame at all and must come from
Aikhenvald — the *secondary*, weaker-independence frame that row 1 does not declare itself to
be using.

**Minimal fix.** For category 1 only: one minimal pair **per evidential value per language**
(≈4–6 × 3), recount the judgment total and the cost line; add to §T5.6 — "E1 obtains iff the
per-value determinate landings are a subset of {Confidence, Model, Premises} using at least
two of the three; dispersion across those three is E1, not indeterminacy"; and mark row 1's
frame "WALS 77/78 for presence, **Aikhenvald 2004 for values (secondary frame)**".

### BLOCKER-8 — three T5 rows pre-register NO-FIT as a *confirmed prediction*, converting the leg's only site-naming outcome into a hit. [D §T5.3 rows 4, 8, 12]

Row 4 predicts "**Manner, or NO-FIT**", row 12 "**Confidence, or NO-FIT**", row 8 "NO-FIT …
**pre-registered as NOT adverse**". NO-FIT is the outcome that feeds `R`, stage-2 recurrence
and the CANDIDATE SITE band — i.e. the only route by which this leg can do the thing it is
advertised to do ("the leg most likely to break the eleven"). Six of the fourteen predictions
are disjunctive, and the two prongs the document itself calls most and second-most dangerous
are both disjunctions containing NO-FIT, so on those rows no result is a miss.

**Minimal fix.** One predicted landing per row; move every alternative into a separate
"alternative landing" column pre-declared to score as a **MISS**; and add one line to §T5.3:
"a NO-FIT on any row, including rows 4, 8 and 12, enters `R` and routes through §T5.9's
CANDIDATE SITE band. §T5.8's defence applies only after the reason fields are read, and only
to row 8."

### BLOCKER-9 — A1's REFUTED band cannot fire on the cleanest possible disconfirmation. [A1 §A1.2.5 / A1.h]

REFUTED requires the three predicted pairs at **≤10% AND some other three pairs at ≥25%**. If
the predicted concentration is simply absent and the residue is diffuse — no rival triple
reaching 25% — the result is INDETERMINATE at best, and on the literal reading of "anything
between" (10–25%) it is **unbanded**. The band as written protects the prediction against
exactly the evidence that would refute it, and the same document already concedes (§A1.2.6)
that the only sample seen so far points that way.

**Minimal fix.** Drop the second conjunct: **REFUTED := the three predicted pairs take
≤10%.** Naming the top rival triple becomes a *reporting* requirement, not a band condition.
Restate INDETERMINATE as "anything not covered above".

### BLOCKER-10 — A1's seen/unseen rule removes the only pre-staked contrary evidence from the test and then pre-commits that it loses. [A1 §A1.2.6(b) / A1.i]

The 30 `language_guidance` parts are where the n = 4 disagreements live, and §A1.2.6(c)
concedes those disagreements are "prima facie AGAINST the concentration prediction". A1.i
excludes them from the primary (defensible — blindness) **and** pre-commits that "if the SEEN
stratum and the primary disagree, **the primary governs**". Together these mean the contrary
evidence cannot enter the test and cannot overturn it if it recurs: the prediction is
protected by the exclusion *and* by the tie-break. The brief's suspicion is confirmed in
direction — removing the seen items removes items whose known pattern is adverse, which
biases the primary toward the prediction, and the addendum never says so.

**Minimal fix.** Keep the exclusion; change the tie-break to: "**Neither governs.** A
disagreement between the SEEN stratum and the primary is reported as an unresolved split, and
the primary may not be quoted in any sentence that does not also carry the SEEN stratum's
result." Add one sentence to §A1.2.6(b): "the exclusion removes items whose observed pattern
is contrary to the prediction; the primary is therefore not a fair test *against that
pattern*, only against a fresh one."

### BLOCKER-11 — the one commitment advertised as mechanically enforced is not enforced by the named mechanism. [D §5]

`§5` states: "Caps are enforced in-process by `plane_annotate.HARD_CAP_USD`, **per leg**, and
a cap event **voids the leg**." The actual constant is `HARD_CAP_USD = 10.0`
(`scratchpad/plane_annotate.py:18`) — a **single global** ceiling, **18× the registration's
entire $0.55 budget**, checked once against cumulative spend with no per-leg notion and no
VOID semantics (it prints and returns). `CLAUDE.md` is explicit: "No process commitment is
advertised as machine-checked", and `epistemology.md` §4 draws the same line.

**Minimal fix.** Either (a) set `HARD_CAP_USD` to the leg's cap before each run and record the
value set in the results file — one line per leg, verifiable after the fact — or (b) restate
§5 as "caps are human-upheld; the module's global `HARD_CAP_USD = 10.0` is a backstop, not the
enforcement." (b) is honest and free.

---

## MAJOR

### MAJOR-1 — the two documents pin contradictory execution orders, and the contradiction is substantive. [D §5 vs R §15]

The delivered draft runs **T1 → T5 → T2 → T3+T4**, with T5 second *because* it is most likely
to break the eleven; the rival runs **T1 → T4 → T3 → T2 → T5**, with T5 last *because* the
adjudication rule should be exercised twice first. Both reasons are good and they are
incompatible.
**Fix:** pick one in the frozen file and delete the other's rationale paragraph.

### MAJOR-2 — the spend regimes differ tenfold, and A1 adds instruments with no cost line under legs whose caps VOID on breach. [D §5, R G7, A1]

Delivered: $0.55 total, per-leg caps summing exactly ($0 + $0.15 + $0.05 + $0.15 + $0.20).
Rival: **G7 $6.00** global with per-leg caps summing $5.50. A1 adds T5-I2, T5-I3 (fresh
annotation by ≥2 annotators over an unspecified frame) and the A0 screen with **no cap at
all**, under a leg whose cap event "**voids the leg** rather than truncating it".
**Fix:** give each A1 instrument its own cap outside T5-I1's $0.15, or state that A1
instruments run only after T5-I1's cap is discharged.

### MAJOR-3 — the T2/T5 mapping instruments differ in size and decision rule, and a ≥50% home rule on 3 judges is near-degenerate. [D §T2.3/§T5.5 vs R §5/§7.3/T2.4/T2.5]

Delivered: **three** mappers, DETERMINATE = **unanimity**. Rival: **five** blind matchers,
home = **modal ≥50%**, with SPLIT and NO-HOME "distinct outcomes, never merged" plus chimera
foils and leave-one-out ablation. On **three** judges, "≥50%" resolves to **2/3, i.e. bare
plurality**, so a home and a modal NO-HOME are certified at the same strength, and SPLIT can
only mean a 1/1/1 three-way scatter — which over twelve labels is rare, making the distinction
the rival says must never be collapsed nearly vacuous in practice.
**Fix:** if the 3-mapper instrument is kept, state the thresholds as counts (3/3 = home;
2/3 = weak home, reported separately; 1/1/1 = SPLIT) rather than as a percentage, and say
whether a mapper's *second* choice (the schema already returns `second`) counts toward any of
them. **It currently does not say, and that is a scoring-time freedom.**

### MAJOR-4 — the RECORD-ANALOGUE band is triggered by a judgment the instrument never elicits. [D §T2.3 vs §T2.5]

The band fires when an ISO device is "**unanimously judged** to be a frame-relation of
Record's type", but the mappers are asked only "a change to this is a change of which kind?"
and the adjudication criterion ("makes a verdict depend on what survives OUTSIDE the artifact
being classified") is never put to them. §T2.5 promises "the blind mappers decide" for a
question they are not asked, so in practice the author applies the criterion to free text —
the exact freedom the paragraph says it removes.
**Fix:** add one frozen field to the mapper schema: "Does deciding this require knowing what
survives outside the artifact being classified? yes/no" and define the band on unanimity of
that field.

### MAJOR-5 — T2's bands do not partition. [D §T2.5]

`D ≥ 6` with **P2.1 holding and P2.2 failing** is in no band: not STRONG (needs P2.2), not
PARTIAL (which covers D 3–5, or D ≥ 6 with **P2.1** failing), not WEAK (D ≤ 2). The ADVERSE
rows are not declared to be overlays, so their interaction with the D bands is undefined.
**Fix:** extend PARTIAL to "…or D ≥ 6 with P2.1 **or** P2.2 failing", and add one line: "the
two ADVERSE rows are overlays; they fire independently of the D band and are reported
alongside it."

### MAJOR-6 — T3's control gate is a decision point with no power statement. [D §T3.5 gate 1]

Gate 1 requires the 15 `appliedRule` vs 15 `factContent` control to separate at **p < 0.01**;
at n = 15 vs 15 that needs roughly a 50-point difference in Model-modal rate. The document's
only registered power statement covers the 30-vs-30 primary. A VOID caused by an underpowered
*gate* is indistinguishable from the instrument-cannot-resolve-kinds finding the gate claims
to measure — `GATES.md` reach 13 ("power of the control itself") is exactly this.
**Fix:** state the gate's own power numerically, or move 9 items from arms A/B into arm D
(24 + 24) at no authoring cost.

### MAJOR-7 — T3's decision threshold rides on an unbounded estimate of R. [D §T3.4/§T3.5]

`R` is estimated from 30 control items and `0.5 R` is the threshold for **both** SUBSTRUCTURE
and ONE KIND, yet R's own sampling error is never carried; a lucky R inflates the
substructure bar and deflates the null bar simultaneously.
**Fix:** use the **lower** 95% bound on R for the SUBSTRUCTURE threshold and the **upper**
bound for the ONE KIND threshold, and say so in the band table.

### MAJOR-8 — T4's arm P is unconstrained on cut ratio yet sets the pass threshold. [D §T4.3 vs §T4.6]

§T4.3 constrains the M-arm and C-arm cut ratios to match within 20% and says nothing about
arm P — but `shift(P) − shift(C)` is both the gate and the denominator of HOLISM CONFIRMED's
`≥ 0.5 × (shift(P) − shift(C))`. A more aggressive cut in P makes the gate pass more easily
*and* raises the bar for M; a gentler one does the reverse. The decisive threshold is an
authoring choice.
**Fix:** extend the ±20% cut-ratio constraint to all three arms, measured and reported per
arm as §T4.3 already requires for M and C.

### MAJOR-9 — T4's gate 1 also has no power statement, on 12 vs 24 items. [D §T4.5]

Same defect as MAJOR-6, worse n: a one-sided p < 0.05 on 12 P-items against 24 C-items needs
a very large shift difference, and gate failure VOIDs the leg for reasons unrelated to holism.
**Fix:** state the gate's power, or raise arm P to 24 (the authoring budget line in §5 counts
150 items across T3+T4 and can absorb it).

### MAJOR-10 — T5's bands leave the pre-registered *expected* outcome unbanded. [D §T5.9]

Evaluated in the stated order, two live cases fall through: (i) `R ≥ 1` with **stage-2
recurrence passing but reason fields not clustering** — CANDIDATE SITE needs all four
conjuncts, RESIDUAL/UNDERPOWERED needs recurrence to **fail**, PARTIAL needs the remainder to
be indeterminate rather than NO-FIT; (ii) `R ≥ 1` where **§T5.8's who-defence applies** —
which is precisely what row 8 (egophoricity) is pre-registered to produce. The leg's own
predicted result has no band.
**Fix:** add two no-verdict bands — "**EXPECTED NO-FIT — warrant axis**" (`R ≥ 1`, §T5.8
applies, reasons about WHO) and "**RESIDUE, UNCLUSTERED**" (recurrence passes, reasons do not
cluster).

### MAJOR-11 — stage 2's trigger over-runs its own budget, and the overflow is then a free choice. [D §T5.5]

Stage 2 triggers on "any category with `R ≥ 1` **or an indeterminate reading**" but is
budgeted at "up to 54" judgments = exactly **three** categories (3 languages × 2 glosses × 3
mappers = 18 each). With determinacy requiring unanimity across three mappers **and**
stability across two gloss conventions, more than three indeterminate categories is the likely
case, and who gets recurred is then chosen by the author at the sharpest point in the design.
**Fix:** pre-declare a deterministic recurrence order (ascending category number) and a hard
cap, and record un-recurred qualifying categories by name as un-recurred.

### MAJOR-12 — GLOSS-T is not kind-neutral, and its bias runs toward the staked secondary. [D §T5.4]

Under GLOSS-T the before/after texts are **byte-identical except a bracketed tag**, so the only
thing that changed is a piece of metadata notation — a systematic pull toward Structure /
Circumstances for *every* category, independent of grammar. The tag strings themselves carry
kind cues (`[EVID:reported]` is a Record/warrant cue; the fixed preamble must gloss the
category in English words that name our kinds). Two consequences: the "stable across both
conventions" rule will register instability whose cause is the tag rendering, which §T5.9's
**VOID — gloss** band then mis-attributes as "we measured English, not grammar"; and the
staked secondary ("≥ 6 of 13 landing on a **non-content** site") is pushed in the favourable
direction by the convention itself.
**Fix:** add a tag-null control — for ≥3 categories, run a GLOSS-T pair whose tag is
**unchanged** while the text differs, and one whose tag changes to a *different value of the
same category* — and pre-commit that carrier-label landings present under GLOSS-T and absent
under GLOSS-N are scored as **convention artifacts**, reported separately from gloss-borne
instability.

### MAJOR-13 — per-item attestation is owed on all 39–42 pairs, and two rows are prima facie at risk. [D §T5.2, §T5.3, §T5.4]

§T5.2 says the **chapter numbers** were verified (I confirmed 73 and 77 above), but §T5.4's
attestation requirement is **per minimal pair** — "a named published example or a WALS
datapoint", verified against the primary, **VOID-bearing** — and the frozen table records
none. Two rows look most likely to fail: **row 3** names Ancient Greek for WALS 73A, and the
chapter's own text does not treat Ancient Greek (its discussion is Caucasian and South Asian;
WALS's sample is overwhelmingly modern); **row 14** names Persian for WALS 37A, whose value
set includes "**No definite, but indefinite article**" — the value Persian is standardly
assigned, which would make the instance fail T5's own *obligatory-marking* selection
criterion. Row 1's Cuzco Quechua is also not discussed in ch. 77's text (Tuyuca and Turkish
are).
**Fix:** add a citation/datapoint column to the frozen table and fill it before freeze; where
WALS has no datapoint for the named language, mark the row **secondary frame** in the table
itself rather than in prose.

### MAJOR-14 — the two most dangerous prongs share a witness. [D §T5.3 rows 1 and 12]

Row 1's Turkish instance and row 12's Turkish instance are **the same morpheme** — `-mIş`, the
non-firsthand past, which is simultaneously the canonical Turkish evidential and the canonical
Turkish mirative, and whose status as a separate mirative category is the live dispute in the
literature the rows cite (DeLancey vs Aikhenvald). So the "most dangerous" and
"second-most-dangerous" prongs are not independent categories on that language, and a
candidate site emerging from both would be one witness counted twice. `§7` doubt 14 registers
the T3/T5 version of this risk and misses this one; the repository's own record names it as a
recurring over-grade.
**Fix:** replace Turkish in row 12 with a language whose mirative is not its evidential, or
add to §T5.3: "rows 1 and 12 share the Turkish morpheme and are **not independent**; a site
supported by both counts as **one** witness."

### MAJOR-15 — the two-witness rule is not scoped to a candidate, and the combination readings contradict each other. [R §3 vs R §14; D §7 doubt 14]

§3 says the Lean count moves "only after a second, independent leg agrees"; §14's
`T2 THEIR-SURPLUS + T5 TWELFTH` row says two unrelated candidates are "**not** mutual
corroboration"; §14's `T3 SPLIT-AND-DIVIDES + T5 TWELFTH` row says "**the count moves
twice**, for unrelated reasons". Whether unrelated candidates each need their own second
witness, or jointly witness "the count is wrong", decides the headline and is left open — and
the delivered draft's §7 doubt 14 takes the first side against §14's second row. Applied to
the brief's case (T5 names a twelfth **and** T1-F1 fires): these are two *different*
candidates, so the non-independence rule forbids what the combination table permits.
**Fix:** one sentence in §3 — "the two-witness bar is **per candidate site**: two independent
legs must name the **same** site. N unrelated candidates are N separate challenges, each
owing its own second witness." Delete "the count moves twice" from the §14 row.

### MAJOR-16 — §T5.11's conditional re-registration is an adaptivity leak, and it contradicts the paragraph above it. [D §T5.11 vs R G15]

§T5.11 first argues that "the **kind-level** mapping is invariant to T1's outcome — the eleven
kinds are the same set either way", then carves an exception in which an F1 result forces
§T5.6's **kind-level** outcomes (Confidence / Model / Premises) to be "re-registered". If the
kind level is invariant, a new *site* cannot require re-registering it; and if it is not
invariant, the leg's sharpest prong has its outcome meanings rewritten after an earlier leg's
result — which G15 forbids and which no constraint bounds (no author, no blindness
requirement, no deadline).
**Fix:** pre-write the twelve-site version of §T5.6 now — it is three rows — so the branch is
frozen rather than re-registered; or delete the exception and rely on the invariance claim the
same section already makes.

---

## MINOR

1. **`rfl` is not available for the stake as written.** [D §T1.0 vs §T1.4] §T1.0 says
   `generator2_image` is `rfl`; §T1.4 stakes it "**as a set**" and §T1.2 deliberately orders
   the table differently from `Site.all` (verified: positions 3–8 are permuted). A set-level
   equality over a deliberately permuted list is not `rfl`, and proving it by `rfl` would mean
   re-ordering the list back to `Generator.lean`'s order, silently undoing §T1.2's anti-rigging
   device. **Fix:** state the stake as `List.Perm` (or `Finset` equality) proved by `decide`,
   and say `rfl` is unavailable.

2. **The blind-deriver prompt leaks the answer.** [R §6.6 / T1.7] Derivers receive "the five
   primitives **with their motivations**", and the motivation column names active inference's
   `A`, `B`, `C`, `D`, `π`, `γ` — a tower whose element count and roles are the answer §6.4 maps
   onto Model / Premises / Priorities / Process / Confidence. **Fix:** strip the factor names
   from the deriver-facing copy; keep the literature names.

3. **The blind arm's pass criterion is not scoreable as written.** [R §6.6] "3/3 reproduce the
   eleven-site structure", scored by "a depth matches if a neutral reader would route the same
   example change to it" — the example changes are never specified and the scorer knows the
   target. **Fix:** publish the eleven routing examples in the prereg and have a third party
   score.

4. **The Lean warrant for the idempotency test is overread.** [R §4] `Stack.lean` defines
   `modulate : Rung → Rung | _ => .strengthMarker` — a literal constant function on a
   four-element type — so `modulate_idempotent` is the idempotence of a constant map and the
   file's own docstring says "DEFINITION; its idempotence is then a theorem about it". It
   cannot license "a sharp, domain-independent test" of modulator-vs-kind. **Fix:** present the
   test as a stipulated criterion; delete the claim that Stack.lean grounds it.

5. **K5b is unreachable as written.** [D §T4.6] "Moved M-items land predominantly on carrier
   labels" is the complement of the ≥2/3-content direction requirement, so K5b can only obtain
   when the primary has already failed — yet the text says "reported adverse **even if the
   primary passes**". **Fix:** delete that clause, or define K5b on a carrier share (e.g.
   ≥1/3) that can co-occur with a pass.

6. **K4b's "incoherent" has no definition.** [D §T3.5] "No semantic pattern, or the reverse of
   the staked direction" — two honest scorers will differ on the first disjunct. **Fix:**
   pre-declare the staked destinations (B → Process/Rules, A → Facts/Premises) and define
   incoherence as ≥50% of leak mass outside them.

7. **Two rows label a genus as a family.** [D §T5.2/§T5.3 rows 5 and 12] The gate is
   "top-level family (Glottolog/WALS family level, **not genus**)"; "Athabaskan" is a genus
   under **Na-Dene** in WALS. No row is lost by relabelling, but an honest scorer applying the
   gate literally could drop both. **Fix:** write Na-Dene.

8. **The denominator 13 is assumed, and the bands are written against it.** [D §T5.3/§T5.9]
   "F in 8–12 **of 13**" and the ≈20% power bound presuppose that row 10 fails the family gate.
   If it survives, both are unanchored. **Fix:** state the bands as fractions of the surviving
   denominator N and the power bound as a formula in N.

9. **A1's chance baseline is uniform where the marginals are not, and the pair-extraction rule
   is undefined for 3-class blocks.** [A1 §A1.2.5] "Eleven classes give 55 unordered pairs;
   three pairs = 5.45%" assumes uniform class use, but the shipped `en` marginals run 128 → 15
   with `axiomatic` at 0; and "record the unordered class **pairs**" does not say whether a
   3-class block contributes one pair or three, which moves the ≥25% denominator. **Fix:**
   define chance by the fresh-label marginals, drop "≈4.6× chance", and specify "all unordered
   pairs, each block weighted equally by dividing by its own pair count".

10. **A1's permutation null is probably degenerate, and its axiomatic stake presumes a frame
    the protocol never fixes.** [A1 §A1.2.5, §A1.2.4, §A1.2.7] "A permutation of class labels
    **within blocks**" leaves each block's unordered pair invariant, so the null cannot move
    the statistic (the same shape as the margin-preserving cluster null already on the record).
    Separately, §A1.2.7 stakes "≥1% of blocks (**≥7 of 635**)" while §A1.2.4 fixes no sample
    size and the only floor is "≥40 mixed blocks" — a 40–90 block annotation cannot produce a
    rate over 635; and the stake (≥7) and KILL-A1.2 (exactly 0) leave 1–6 in no band. **Fix:**
    specify the null as a random reassignment of per-block label multisets across blocks (or an
    exact fixed-margin sampler); pin the fresh-annotation frame and restate the stake as a rate
    on it; add "1–6 ⇒ no verdict".

11. **Three small citation defects.** [D §5, D §T3.5, A1 §A1.1.7] (i) §5 attributes the
    reporting rule to "epistemology.md §7"; §7 is "What is borrowed here, and what is ours" —
    the rule is **L8** (§3), and item 7 of CLAUDE.md's discipline list. (ii) §T3.5 cites
    `analyse_gauge.py` without a path (it is `scratchpad/gaugetest/analyse_gauge.py`) and says
    the control stage opens "arm D"; that script's stage 1 loads **arms A and C**, so the arm
    mapping must be restated for this leg. (iii) A1.1.7's **VOID — register** and **NULL** rows
    both describe "the grammar was never engaged" (source-side clause count vs target-side
    constancy) with no evaluation order; state the order.

---

## Answers to the brief's eight surfaces, in order

1. **T1 freeze integrity.** The RSite table + recipe are decidable with zero *arithmetic*
   freedom and **total** modelling freedom, because the table is frozen **before** the R2
   arguments that are supposed to generate it (BLOCKER-3), T1-VOID-2 has no test for
   "transported" and T1-VOID-1 forbids the one result that would prove non-transport
   (BLOCKER-4). A placebo *can* give eleven in principle — Habermas's three claims through
   R1–R4 need only a 3/2/0-shaped gap argument, which is a free choice — and the design's
   response is staked (RECIPE-DRIVEN → candidate warrant failure, §T1.6), which is the
   document's strongest single passage. But the placebo authoring is asymmetric and its only
   real mitigation is optional (BLOCKER-5). The blind-deriver protocol exists only in the rival
   draft; as written it is executable but leaks the target through the motivation column and
   has an unscoreable pass criterion (MINOR-2, MINOR-3).

2. **Idempotency.** The third worked example is **composition of two markers**, not stacking of
   one — and so is the second. The rule is therefore convention-dependent and steerable
   (BLOCKER-6). The certainty prediction survives; **the conditionality and source-of-knowing
   predictions do not** and must be re-staked before freeze.

3. **T2 SPLIT vs NO-HOME.** Yes, gameable, and "≥50% on 3 judges" is bare plurality, which
   certifies a home and a NO-HOME at the same strength and makes SPLIT nearly unreachable
   (MAJOR-3). The unresolved question of whether a mapper's `second` field counts is a
   scoring-time freedom the schema already makes available.

4. **T5's two-gloss control.** GLOSS-T is **not** kind-neutral: the tag vocabulary cues kinds
   and, more seriously, the tag-only diff is itself a carrier change, biasing every category
   toward Structure/Circumstances and toward the staked "non-content" secondary (MAJOR-12). The
   14 landings are **not** separable in aggregate: six are disjunctive and three name NO-FIT as
   a prediction (BLOCKER-8). Against the actual rows, the family gate is satisfied everywhere
   except a genus/family mislabel in rows 5 and 12 (MINOR-7), but rows 1 and 12 share a witness
   (MAJOR-14) and per-row attestation is unrecorded with two rows at risk (MAJOR-13).

5. **A1.** The seen-stratum rule does **not** neutralize the contamination — it removes the
   adverse items and pre-commits that they lose (BLOCKER-10) — and it may additionally be a
   **no-op**, since it is nowhere established that any of the 30 seen parts lie in the
   mixed-block frame the primary is computed over; measure and report that overlap before the
   primary runs. A1.h is neither exhaustive nor non-overlapping in the adverse direction
   (BLOCKER-9). T5-I2's VOID-EXPECTED status **is** consistent with staking its bands — the
   CASE rows are explicitly conditional on a P2+ asset that does not yet exist — but the VOID
   can be undone by a provenance search conducted with the answer known; require the provenance
   class of all six evidential-set locales to be written to disk **before** any target locale
   is opened, and forbid post-hoc reclassification on testimony obtained after the §A1.1.6
   source coding is frozen.

6. **Cross-document.** A1 **does** alter a delivered VOID condition despite claiming
   additivity (BLOCKER-2), and adds uncapped instruments under a cap that voids on breach
   (MAJOR-2). The spend caps sum consistently **within** each document ($0.55 and $5.50/$6.00)
   and are incompatible **between** them. The order-of-execution question is a live
   contradiction (MAJOR-1); the concrete information leak between legs is not T1→T5's mapper
   prompts but **§T5.11's conditional re-registration of T5's outcome meanings** (MAJOR-16).

7. **Two-witness vs E2.** They are **not** consistent if merged: §T5.6's E2 names a candidate
   twelfth on three unanimous mappers, while §3 permits naming only after all six criteria are
   scored; and §14's own two rows disagree with each other about whether unrelated candidates
   move the count (MAJOR-15). Scoped per candidate site, the F1 + E2 case is two challenges,
   each owing its own second witness — which is what §7 doubt 14 already says and what §14's
   T3+T5 row denies.

8. **Where two honest scorers can disagree.** T1: "transported from Searle" (no test); whether
   a placebo "produces exactly our eleven". T2: "of Record's type"; the D ≥ 6 / P2.1-holds /
   P2.2-fails cell; whether `second` counts toward a modal. T3: "incoherent" leak destinations;
   whether R's sampling error moves the threshold. T4: "predominantly carrier"; whether an
   unmatched arm-P cut ratio invalidates the threshold. T5: category-level determinacy when
   some instances are determinate and others are not; E1-distribution vs indeterminate; the
   family gate on "Athabaskan"; which categories get stage 2 when more than three qualify;
   whether a row-4/8/12 NO-FIT enters `R`. A1: 3-class blocks' pair count; a ≤10% result with
   no rival triple; **which κ floor applies**.

---

## What is solid, recorded so the report is not one-sided

- **§T2.1's source extraction is accurate.** The nine dimension names, the three qualifiers,
  Contact Management as DIT++'s tenth and Task Management as DAMSL's-proposed-for-re-inclusion
  all match Bunt 2017 §2 and §3.4 verbatim. This is the document's cleanest passage and it was
  done the hard way.
- **Every Lean object either document cites exists**, under the name cited, and the
  `Generator.lean` header line quoted "verbatim" in §T5.1 is verbatim. The
  hedging/evidentiality conflation §T5.1 attacks is genuinely in the file, named by the
  programme against its own interest.
- **The staging discipline is real and has a working precedent** — `analyse_gauge.py`'s
  two-stage refusal (stage 2 will not run without `void.json` on disk) is exactly what §T3.5
  and §T4.5 gate 1 describe.
- **§T1.6, §A1.1.4, §A1.2.2, §A1.2.6 and §T5.5's power statement are model disclosures.** The
  placebo's authored-by-an-interested-party weakness, the machine-translation circularity, the
  circularity fence on our own corpus, the not-blind prediction, and "this leg is powered to
  DETECT and NOT to establish absence" are all stated before the run, against interest, in the
  frozen text. The blockers above are defects **in mechanism**, not in candour.
