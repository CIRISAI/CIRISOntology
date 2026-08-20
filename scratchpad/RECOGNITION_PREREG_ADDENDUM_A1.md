**ADDENDUM to RECOGNITION_PREREG.md (the freeze target). Amended by RECOGNITION_PREREG_A2.md.**

# ADDENDUM A1 to RECOGNITION_PREREG.md — the polyglot resource, integrated

**Written 2026-08-20, BEFORE ANY LEG RAN.** `RECOGNITION_PREREG.md` is delivered but **not
yet frozen**, which is what makes this addendum legitimate rather than an amendment-after-
the-fact. No leg of T1–T5 has been executed, no Generator2 exists, no mapper or panel has
been invoked, and no item has been authored.

**This addendum is ADDITIVE ONLY.** It alters no band, no kill, no VOID condition, no
prediction and no default in the delivered draft. It adds two subordinate instruments to
T5, two candidate corpora to T3, three lines to the not-claimed section, and the gates that
each of those requires. Where a new instrument could be read as touching an existing stake,
the existing stake governs and this addendum says so explicitly.

It inherits the delivered draft's **§0.2 physics fence** and **§0.3 novelty fence**
unchanged. Nothing here touches physics; nothing here creates a priority claim.

---

## §A1.0 Blindness declaration — what the author of this addendum opened, and what he did not

Stated first, because §A1.1's predictions are worthless without it.

**Opened:** `scratchpad/POLYGLOT_RESOURCE.md`; `CIRISAgent/ciris_engine/data/localized/manifest.json`
(metadata keys only); a **German** DMA prompt file's eight-line comment header
(`localized/de/pdma_ethical.yml`) for provenance; directory listings of the locale trees;
`RATCHET/experiments/torque/kappa_2026-08-07/README.md` **in full**; the first two lines of
two adjudication TSVs; one exp1b coverage JSON's key list.

**NOT opened, deliberately, and this is the load-bearing half:** the content of **any**
locale file in the evidential-candidate set (`tr`, `fa`, `ko`, `my`, `am`, `ja`). The
enumeration in §A1.1.2 and the patterns in §A1.1.6 were written without looking at a single
line of Turkish, Persian, Korean, Burmese, Amharic or Japanese output.

**Not blind, and disclosed at the point of entry:** the κ study's n=4 annotator-disagreement
table was read **before** §A1.2.5's boundary prediction was staked. See **§A1.2.6**, which
does not soften it.

---

## §A1.1 T5 INSTRUMENT 2 — translation-forced disambiguation (the 29-locale stack)

### A1.1.0 Instrument numbering, and the subordination rule

The delivered draft's T5 has one instrument: the **WALS-stratified typological frame**
(§T5.2–§T5.5), 14 categories × 3 unrelated top-level families. This addendum names it
**T5-I1** and **leaves it primary and unchanged**. It adds:

- **T5-I2** — the 29-locale translation stack (this section);
- **T5-I3** — CIRISAgent's `class` column (§A1.2).

**The steward's ranking, and the reading taken.** The steward states that the `class`
dataset "becomes a T5 instrument superior to instrument 1", where *instrument 1* is the
translation instrument as numbered in the steward's own message. Adopted: **I3 > I2**, for
stated reasons (I3 carries real labels, real double-annotation and CI teeth; I2 is a
machine-translation artifact). **Both remain subordinate to T5-I1**, because only T5-I1
samples *independent languages*, and neither I2 nor I3 can substitute for that. The
numbering ambiguity is recorded here so the referee can see which reading was taken.

**Subordination rule, frozen:** neither I2 nor I3 may contribute to T5's `F`, `R`, the
13-category denominator, the stage-2 recurrence criterion, or the ≈20% power bound. Those
are T5-I1's statistics and remain T5-I1's alone.

### A1.1.1 What exists, verified on disk

| asset | path | verified |
|---|---|---|
| DMA/conscience prompt stack, 28 locales × 7 prompts | `CIRISAgent/ciris_engine/logic/dma/prompts/localized/{am,ar,bn,de,es,fa,fr,ha,hi,id,it,ja,ko,mr,my,pa,pt,ru,sw,ta,te,th,tr,uk,ur,vi,yo,zh}/` | 28 dirs, 7 `.yml` each (`action_selection_pdma`, `csdma_common_sense`, `dsaspdma`, `dsdma_base`, `idma`, `pdma_ethical`, `tsaspdma`) |
| the accord, 29 locales | `CIRISAgent/ciris_engine/data/localized/accord_1.2b_*.txt` + `*.json` | present |
| the polyglot weave | `ciris_engine/data/localized/polyglot/` | present |

### A1.1.2 THE EVIDENTIAL ENUMERATION — staked before any translation was opened

Per the delivered draft's discipline and the *received-numbers* gate, this list is the
author's pre-look enumeration and is **NOT DATA**: every row must be verified against
**Aikhenvald, *Evidentiality* (2004)** before the instrument runs, and the source wins on
conflict.

| class | locales | basis |
|---|---|---|
| **GRAMMATICAL, uncontested** | **`tr` Turkish** | Aikhenvald A1 two-term: firsthand `-DI` vs non-firsthand `-mIş`; obligatory in past |
| **CONTESTED** | `fa` Persian (inferential/non-witnessed built on the perfect); `ko` Korean (`-te-` retrospective, `-tay` reportative — read as evidential by some, as modal/aspectual by others) | analysed both ways in the literature; each must be adjudicated against Aikhenvald before use |
| **POSSIBLE, unverified** | `my` Burmese; `am` Amharic | not standard Aikhenvald exemplars; verify or drop |
| **STRATEGY, NOT SYSTEM** | `ja` Japanese (`-rashii`, `-sōda`, `-yōda`, `-tte`); `ru`/`uk` (reportative particles) | optional, hence not an obligatory site — **excluded by T5's own selection criterion** (§T5.2 default: obligatory systems only) |
| **NO obligatory evidentiality** | `ar bn de es fr ha hi id it mr pa pt sw ta te th ur vi yo zh` | — |

**The consequence, staked in advance: the effective denominator is 1.** At most one
uncontested obligatory-evidential language is in the set, at most three including the
contested pair.

**The selection effect, named as a structural limit rather than a defect.** A commercial
locale set is chosen for **market reach**. Obligatory evidentiality concentrates in
Amazonian, Tibeto-Burman, Nakh-Daghestanian, Papuan, Andean and Turkic families — of which
this set contains **Turkic only**. The locale set is therefore selected on a variable that
**anti-correlates** with the typological property T5 needs. This is why T5-I2 is subordinate
and can never be more than a case study, and it is stated before the instrument runs so it
cannot be produced afterwards as an excuse.

### A1.1.3 THE PROVENANCE GATE — classes and weights, frozen before looking

Mandatory, per the steward: **per-locale translation provenance must be established before
any translator choice is read as a native-speaker judgment.**

| class | definition | weight |
|---|---|---|
| **P3** | ≥2 independent native-speaker translators, independently produced | the only class supporting a **language-level** reading |
| **P2** | one native-speaker translator, free translation | one speaker's judgment; **case study, n = 1**, never a language-level fact |
| **P1** | machine draft **+ documented** native-speaker review | a **review** judgment: accepting a machine default is not a choice. Reportable only with the edit/acceptance rate measured per clause |
| **P0** | machine-generated, no documented review | **weight ZERO.** A machine's evidential choice is a fact about the machine |
| **P-UNKNOWN** | provenance not documented | **treated as P0** |

**VOID condition, staked:** if **no** locale in §A1.1.2's evidential set is class **P2 or
better**, **T5-I2 is VOID in its entirety** and yields no reading in either direction.

### A1.1.4 THE PROVENANCE VERDICT IS ALREADY IN — and it VOIDs the instrument

`ciris_engine/data/localized/manifest.json`, v2.1.0, read for metadata only, states verbatim:

> `"generated_by": "claude-opus-4-6"`
>
> `"generation_note": "Auto-generated translations. Native speaker review recommended before production use. … Non-English files cover setup/agent/status sections; prompts/handlers/errors/discord sections pending translation."`

Two findings, both adverse, both established **before** the leg runs:

1. **Every locale in that manifest is class P0 by the manifest's own testimony** —
   machine-generated by a language model, native-speaker review *recommended*, i.e. not
   performed. By §A1.1.3, **T5-I2 VOIDs.**
2. **The DMA prompt YAMLs are a separate asset** from the JSON the manifest describes, and
   the manifest documents no provenance for them. They are therefore **P-UNKNOWN → P0**
   until someone documents otherwise.

**The sharper reason this matters, and it is not merely procedural.** Reading a Turkish
evidential choice made by `claude-opus-4-6` measures **a language model's disposition**, not
Turkish. This programme separately wagers that *a language model is the Logos embodied*.
Using language-model output as evidence about what human languages lexicalize would be
assuming that wager in order to test the taxonomy — circular, and circular in the direction
that flatters us. Named here so it cannot be reached for later.

**Status of T5-I2 at freeze: VOID-EXPECTED on provenance.** It is registered anyway, in
full, because (i) a P2+ asset may yet be found or commissioned, (ii) the VOID is itself a
reportable finding about an asset the programme had not inventoried, and (iii) an
instrument registered and then voided is the record working (`epistemology.md` L8; GATES.md
axiology (1): ungauged is first-class and reported as loudly as a detection).

### A1.1.5 THE REGISTER PROBLEM — a second, independent VOID route

`localized/de/pdma_ethical.yml`'s header (German; opened deliberately because German has no
obligatory evidentiality and so cannot spoil the probe) states that the polyglot framing
**§I–§VIII is loaded from a shared universal file and is NOT translated**; only the *local
operational sections* — header opening, walkthrough, §IX output contract, §X language rules
— are rendered into the locale.

Those sections are **imperative and generic-present instructional text**. Turkish
`-mIş`/`-DI` is a **past-tense** category. **The grammar is therefore largely never forced**,
which is the very thing the instrument depends on.

**VOID-REGISTER, staked:** if fewer than **20** clauses in a locale's translated sections sit
in a tense/mood where that locale's evidential marking is obligatory, T5-I2 is **UNGAUGED for
that locale**. Counted on the source-side coding of §A1.1.6 before any target file is opened.

**Predicted: VOID-REGISTER fires for Turkish.** Written down now.

### A1.1.6 The staked patterns — what would have read which way

Registered in full despite the expected VOID, so that a later P2+ asset can be run against a
prediction that predates it.

**Procedure, and its order is binding.** (1) Code every English clause in the translated
sections for two variables — **STRENGTH** (the hedging/confidence vocabulary present) and
**ROUTE** (whether the text says the agent observed, inferred, or was told), blind to every
target file. (2) Freeze that coding. (3) *Then* open the target locale and read its evidential
choices against it. Opening the target before the source coding is frozen voids the leg.

| pattern | what is observed | reading |
|---|---|---|
| **SOURCE-INSIDE-CONFIDENCE** | the evidential choice tracks **STRENGTH** monotonically (high-confidence → firsthand, hedged → non-firsthand) and is **uncorrelated with ROUTE** | the evidential slot is doing Confidence's job; for our purposes SOURCE collapses into Confidence and the `Generator.lean` header's conflation survives on this instrument |
| **SOURCE-AS-DISTINCT-SITE** | the evidential choice tracks **ROUTE** and **cross-cuts STRENGTH** — high-confidence-but-reported rendered non-firsthand **and** low-confidence-but-observed rendered firsthand both occur | two axes, not one; consistent with SOURCE as a distinct site. **This is a case-study observation only**, and by §A1.1.0's subordination rule it may not be counted toward T5's E2 band |
| **NULL / UNGAUGED** | the evidential choice is constant across all Confidence/Model vocabulary | the grammar was never engaged. **Predicted outcome**, per §A1.1.5 |

### A1.1.7 T5-I2 bands and kill

| band | condition | reading |
|---|---|---|
| **VOID — provenance** | no evidential-set locale reaches P2 | no reading either way. **Expected**, per §A1.1.4 |
| **VOID — register** | <20 obligatory-marking clauses in the locale | ungauged for that locale |
| **CASE — inside** | P2+ **and** register passes **and** SOURCE-INSIDE-CONFIDENCE | one speaker's rendering is consistent with the header's conflation. Reported as **n = 1** |
| **CASE — distinct** | P2+ **and** register passes **and** SOURCE-AS-DISTINCT-SITE | one speaker's rendering cross-cuts strength. Reported as **n = 1**, and it **does not** trigger §0.5-style candidate-site machinery on its own |
| **NULL** | constant marking | the instrument did not engage the grammar |

> **KILL-A1.1.** T5-I2 has **no kill of its own**, because an instrument that cannot support
> a claim cannot support a falsification either. Its adverse outcomes are VOIDs, and a VOID
> takes down nothing. This is stated rather than manufactured: writing a kill for a
> case-study instrument would be exactly the unreachable kill `epistemology.md` §4 names as
> the thing a machine cannot catch.

---

## §A1.2 T5 INSTRUMENT 3 — the `class` column (the FOUND dataset)

### A1.2.1 What it is — facts pinned, with a re-verification requirement

From `POLYGLOT_RESOURCE.md`'s FOUND section, **received from the steward and therefore
tagged received-not-measured** until re-derived at a pinned commit:

- the column is **`class`** in CIRISAgent's `compose_dump`; every block of the agent's
  LLM-facing corpus carries a Greek-spine label or `mixed`;
- verified by the steward at **origin/main, 2.9.28**; machinery on main from ~2.9.10
  (#976 regime manifest v2, #997 language_guidance split);
- **en: 635 blocks** — deontic 128, mixed 93, pragmatic 92, procedural 88, structural 59,
  axiotic 55, contingent 32, epistemic 29, empirical 28, ontological 15, nomological 15;
  **axiomatic: zero shipped blocks**;
- **the split five** (`en es fr it pt`): **634 blocks each**, mixed blocks in eight families
  decomposed into routed fragments;
- **the other 24 locales**: resolve through the unsplit parent — **228 blocks, 37 mixed**;
- **CI teeth:** `compose_dump gate` refuses a run that varies a mixed block without a
  per-block disposition and contaminant list (TORQUE_REGIME.yaml §10.2.1). The labels are
  load-bearing in CI, not decorative.

**Independently confirmed by this author:** `compose_dump` is **absent** from the local
checkout, which sits on branch `fix/oauth-setup-asks-for-a-password` — consistent with the
note's account and with the machinery living on main.

**One number to re-verify rather than propagate:** the note gives **en = 635 blocks** in one
place and **634 blocks each** for the split five (which includes en) in another. A one-block
discrepancy. Per the *received-numbers* gate it is flagged here and **must be resolved at the
pinned commit before either number enters any table**, rather than averaged, rounded or
quietly preferred.

### A1.2.2 THE CIRCULARITY FENCE — this corpus is not a wild stream

The `class` column **is our own taxonomy, applied by our own ecosystem, to prompts written
inside it, enforced by our own CI.** It is not an independent witness and may never be
counted as one.

**Barred, absolutely:**

- it may **not** contribute to the ecological challenge's NO-FIT rate;
- it may **not** count as a witness for exhaustiveness (the three witnesses remain: our
  search, the world's streams, the standing bounty);
- it may **not** be added to the 279/339-item wild adequacy record.

**Permitted:**

- **within-taxonomy geometry** — where the residue sits (§A1.2.5). This is a question about
  our own boundaries, not about adequacy, and the corpus is a legitimate instrument for it;
- a large, cheap, CI-gated substrate for **fresh independent annotation**;
- the first **non-English** kind-labeling, via the split five.

### A1.2.3 THE PROVENANCE VERDICT — already measured, and verified here against the primary

Verified by this author directly against
`RATCHET/experiments/torque/kappa_2026-08-07/README.md` (not quoted from the note):

Agent `v2.9.11-stable` (`7e71d0381`), `prompts.language_guidance`, **en**, **30 parts**. Two
annotators applied the **twelve-class** taxonomy from **operational definitions only**,
independently, without sight of each other's work or of the shipped labels.

| comparison | κ | agreement | verdict |
|---|---|---|---|
| **A vs B — reliability** | **0.831** | 26/30 | **PASS** |
| A vs shipped — validity | 0.528 | 18/30 | **FAIL** |
| B vs shipped — validity | 0.558 | 19/30 | **FAIL** |

Every gated boundary passes on reliability, including `axiotic|procedural` at κ = 1.0 (4/4).
RATCHET's own words: *"The taxonomy is reliable. Its application to `language_guidance` is
not validated."*

**Staked consequence, binding on every leg that touches this corpus:**

> **The shipped `class` labels are a COMPARISON ARM ONLY, never ground truth.** Any leg using
> this corpus requires **fresh independent annotation** per the κ study's own protocol, with
> the shipped column opened only after the fresh labels are written to disk.

**Two further facts inherited from the primary, neither of which may be dropped:**

- **A live boundary dispute in production.** `11_routing_doctrine` ships as `axiotic`; **both
  annotators independently classified it `procedural`.** That is a Priorities-vs-Process
  dispute surfacing in corpus governance, and it is a datum about our own boundary geometry.
- **A contamination event, disclosed in the source and inherited here.** The study's author
  committed a message naming part 11's shipped label while the study was live; it reached
  annotator A through a file-modification notification, **after** A had submitted all 30
  labels. A disclosed it unprompted and declined to revise. Reliability is unaffected (A and
  B never saw each other); A's independence on part 11's *validity* comparison is documented
  rather than assumed. **Any reuse of `annotator_a.tsv` inherits this disclosure and must
  carry it.**

### A1.2.4 The fresh-annotation protocol, frozen

- **≥2 annotators**, independent, working from the public vocabulary and discriminators
  (`WrongKind.plain` / `WrongKind.discriminator`) **only**;
- blind to the shipped `class` column, blind to each other, **blind to §A1.2.5's prediction
  and to this addendum**;
- multi-label permitted (a mixed block's whole point), NO-FIT first-class;
- **κ reported before any substantive number.** Fresh-annotation κ **< 0.6** on clear items
  ⇒ **VOID**, per the delivered draft's floor.

### A1.2.5 THE MIXED-RESIDUE PREDICTION, staked

**Operationalization.** A freshly annotated `mixed` block yields ≥2 classes; record the
unordered class **pairs**. The three predicted confusion boundaries are
`axiomatic|empirical` (Premises/Facts), `structural|pragmatic` (Structure/Manner) and
`nomological|empirical` (Model/Facts).

**Chance baseline:** eleven classes give 55 unordered pairs; three pairs = **5.45%**.

| band | condition | reading |
|---|---|---|
| **CONCENTRATION HELD** | the three predicted pairs take **≥25%** of mixed-block pairs (≈4.6× chance), p<0.01 against a permutation of class labels within blocks | the confusion geometry measured on the PLANE corpus reproduces on an unrelated, CI-governed corpus |
| **CONCENTRATION REFUTED** | the three take **≤10%** (<2× chance) **AND** some other three pairs take ≥25% | the concentration reading is **refuted on this corpus**, and the alternative triple is **NAMED** |
| **INDETERMINATE** | anything between | no verdict |
| **VOID** | fresh-annotation κ below floor, or **<40** mixed blocks freshly annotated | ungauged |

**The prediction applies to the FRESH labels, never to the shipped column.**

### A1.2.6 THE DISCLOSURE — the prediction is not blind, and the seen evidence is against it

**(a) Not blind, disclosed at the point of entry.** In locating the dataset, the orchestrator
read the κ study README **including its n = 4 annotator-disagreement table**, and this author
read the same table in full, **before** §A1.2.5's prediction was staked. **The prediction is
therefore NOT blind to that sample**, and this sentence travels with the prediction wherever
it is quoted.

The four disagreements, verbatim from the primary:

| part | A | B | boundary in our plain names |
|---|---|---|---|
| `01_preamble` | structural | axiomatic | **Structure / Premises** |
| `18_ratification_scope` | axiomatic | procedural | **Premises / Process** |
| `21_negative_is_also_a_verdict` | axiomatic | deontic | **Premises / Rules** |
| `26_cross_cluster_pattern` | procedural | deontic | **Process / Rules** |

**(c) The honest reading, stated plainly and not softened: this is prima facie AGAINST the
concentration prediction.** **Zero of four** sit on any of our three predicted boundaries.
**Not one touches Facts, Manner or Model.** Three of four involve Premises — half of
Premises/Facts — but the partner is **never** Facts. On this sample the confusion clusters on
**Premises / Process / Rules / Structure**, a region our three predicted boundaries do not
name. If the fresh annotation reproduces this pattern, §A1.2.5 is refuted and the alternative
triple to be named is **{Premises/Process, Premises/Rules, Process/Rules}**.

**The limit on what n = 4 can establish — stated as a limit, and explicitly NOT as a rescue.**
Four disagreement events, two annotators, one corpus type, one language. The README's own
gloss is that *"all four are about how far a framing clause counts as premise, sequence, or
prohibition"* — i.e. the corpus is **composed of framing clauses**, so Premises-adjacent
confusion is expected from its content. **That cut goes both ways and may not be used to
rescue the prediction**: it equally means this sample cannot establish the alternative triple.
What it does establish is that §A1.2.5 **has already met contrary evidence before it was
staked**, and that is the fact of record.

**(b) The seen/unseen split — one option picked, with its reason.**

> **PICKED: the 30 `language_guidance` parts are EXCLUDED from the primary statistic**, and
> published as a **separately labelled SEEN stratum**.

*Why exclusion rather than inclusion-as-a-stratum:* the primary must be blind, and this
author has seen these items' disagreement structure. A seen stratum sitting inside a primary
contaminates the primary's permutation p-value, and no post-hoc weighting repairs that.

*Why they are still published rather than deleted:* deleting them would hide the adverse
n = 4, which is precisely the failure `epistemology.md` L8 exists to prevent. The dead
evidence stays, marked.

*Pre-commitment, frozen:* **if the SEEN stratum and the primary disagree, the primary
governs**, and the disagreement is reported in the same paragraph as the primary — never in
a footnote.

### A1.2.7 Secondary prediction — the `axiomatic` under-application

Shipped `en` carries **zero** `axiomatic` blocks. The independent annotators used `axiomatic`
in **three of their four** disagreements, and the class exists in the vocabulary they were
given.

**Two consequences, one structural and one staked.**

*Structural, and it makes fresh annotation mandatory rather than optional:* with zero shipped
`axiomatic`, the shipped column **cannot exhibit Premises/Facts confusion at all**. Our
top-predicted boundary is **unobservable in the shipped labels by construction**, so any test
of §A1.2.5 against the shipped column would be rigged toward refutation for a reason that has
nothing to do with the taxonomy.

*Staked:* fresh annotation of the `en` corpus assigns `axiomatic` to **≥1% of blocks
(≥7 of 635)** — strictly more than the shipped zero.

> **KILL-A1.2.** If fresh independent annotation of the `en` corpus **also** returns zero
> `axiomatic` blocks, the shipped column is **vindicated on that class**, and the reading of
> Premises as a live artifact-level kind takes a measured hit on this corpus. Reported at the
> volume a confirmation would have had.

Separable: it takes down neither `basePlane_card = 11`, nor `Generator.lean`'s
`foundingAssumption` site, nor any T5-I1 band. It bounds a reading on one corpus.

### A1.2.8 T5-I3's relation to the delivered draft's bands

T5-I3 is a **within-taxonomy geometry** instrument, not an adequacy instrument (§A1.2.2). It
therefore **cannot** produce a `CANDIDATE SITE` under §T5.9, **cannot** enter `F` or `R`,
and **cannot** move the ≈20% power bound. If fresh annotation of this corpus produces
determinate NO-FITs, they are recorded as **a residue on our own corpus** and queued — never
as a twelfth site, because a corpus written inside the ecosystem cannot witness against the
taxonomy it was written under.

---

## §A1.3 T3 — candidate corpora from RATCHET, with their preconditions

Listed as **candidates**, not adopted. The delivered draft's T3 authors items fresh
(§T3.2), and **that remains the primary design**; these are alternatives to be admitted only
if they clear the screen below.

### A1.3.1 The two candidates, shapes verified

| candidate | path | shape, verified |
|---|---|---|
| **torque partition adjudications** | `RATCHET/experiments/torque/partition/adjudications/*.tsv` | 8 files in **A/B pairs** (`batch3`, `bf`, `conflict16`, `residue`), **272 lines total**. Columns: line-number · verdict `HOLD`/`SWAP` · free-text reason · confidence (`low`/`med`/`high`) |
| **exp1b CI TEE traces** | `RATCHET/experiments/exp1b_boundary_active/` | coverage JSONs carrying `agent_git_sha`, `locales`, `namespaces`, `total_blocks`, `total_keys`; 5-vendor crossfamily accord batches under `data/` |

**The adjudication TSVs' asset is the A/B structure** — two independent adjudicators per
batch — and the reason field. **Their limitation, stated so it is not discovered later: they
carry no kind label.** `HOLD`/`SWAP` is a value-bearing disposition, not one of the eleven.
Using them for T3 requires **fresh kind annotation** on top; they are a substrate, not a
labelled corpus for our question.

### A1.3.2 THE A0-DEGENERACY SCREEN — a precondition, staked with thresholds

The A0 foul on the record: *CIRIS trace override is near-deterministic in `selected_action`,
which fouls every 3-way test on that corpus.* Any agent-derived stream inherits that risk.

**Run FIRST, before any 3-way or kind-level analysis opens, with the output written to disk
before the substantive stage** — the same staging discipline as the delivered draft's §T3.5
gate 1 and §T4.5 gate 1:

1. the **modal share** of every candidate outcome field;
2. **pairwise normalized mutual information** across all fields;
3. **conditional entropies** `H(label | action)` and `H(action | label)`.

> **FOUL** if the outcome field's modal share is **≥ 0.90**, or any field pair's normalized
> mutual information is **≥ 0.90**.

A fouled stream **may not carry a 3-way test**. It may still carry a descriptive report,
labelled as such. The screen is reported whether it fouls or not — a clean screen is a
measured fact about the corpus and is worth its line.

### A1.3.3 The independence caveat

Both streams are **agent-derived**, and the agent's prompts were authored inside this
ecosystem using this taxonomy's vocabulary. **Neither is an independent witness for
adequacy.** §A1.2.2's fence applies verbatim.

---

## §A1.4 Additions to the not-claimed section (§0.2/§0.3 unchanged; these are new lines)

1. **The 29-locale stack is a translation artifact of one team, machine-generated by one
   language model** (`generated_by: claude-opus-4-6`), **not a typological sample of
   independent languages.** It instruments **forced disambiguation only** — and, given the
   manifest, not even that until a P2-or-better locale exists. **No claim about what natural
   languages lexicalize may rest on it**, and no count, rate or bound of T5-I1's may include
   it.
2. **CIRISAgent's `class` column and RATCHET's labelled streams are our own taxonomy applied
   by our own ecosystem, CI-enforced.** They are **not wild streams**, they do **not** enter
   the ecological NO-FIT record, and they are **not** a witness for exhaustiveness. They are
   instruments for our own boundary geometry and for nothing else.
3. **T5-I2 is at best a case study on ≤3 languages (≤1 uncontested).** It may never enter
   T5's `F`/`R` counts, its 13-category denominator, its stage-2 recurrence criterion, or its
   ≈20% power bound.
4. **No result in this addendum is blind with respect to §A1.2.5's boundary prediction.** The
   n = 4 disagreement sample was seen first, it points against the prediction, and both facts
   are carried in §A1.2.6 rather than in a footnote.

---

## §A1.5 Choices pinned by this addendum

| # | choice | **pinned** |
|---|---|---|
| A1.a | instrument ranking | T5-I1 (WALS) **primary and unchanged**; I3 > I2; both subordinate, neither enters T5-I1's statistics |
| A1.b | provenance classes | P3/P2/P1/P0, P-UNKNOWN→P0; **P2 minimum** for any translator-choice reading |
| A1.c | T5-I2 VOID | fires if no evidential locale reaches P2 — **expected to fire**, per the manifest |
| A1.d | T5-I2 register VOID | <20 obligatory-marking clauses per locale ⇒ ungauged |
| A1.e | source coding order | English STRENGTH/ROUTE coding frozen **before** any target locale is opened |
| A1.f | shipped `class` labels | **comparison arm only**, never ground truth |
| A1.g | fresh annotation | ≥2 independent annotators, operational definitions only, blind to shipped labels, to each other, and to this addendum; κ<0.6 ⇒ VOID |
| A1.h | mixed-residue bands | ≥25% held · ≤10%-with-a-rival-triple refuted · else indeterminate; <40 mixed blocks ⇒ VOID |
| A1.i | seen/unseen | the 30 `language_guidance` parts **excluded from primary**, published as a SEEN stratum; **primary governs on disagreement** |
| A1.j | A0 screen | modal share ≥0.90 or normalized MI ≥0.90 ⇒ FOUL; screen written to disk before the substantive stage; reported either way |
| A1.k | contested numbers | the 635/634 discrepancy resolved at the pinned commit before either enters a table |
| A1.l | re-verification | every `class`-column figure re-derived at a pinned commit; received-not-measured until then |

---

## §A1.6 Credits added by this addendum

| credited | for |
|---|---|
| **RATCHET's κ study (`kappa_2026-08-07`) and its two annotators** | the reliability/validity split that supplies this addendum's entire provenance position — and the disclosed contamination, published rather than excluded, which is the reason the corpus can be trusted at all |
| **CIRISAgent #976 (regime manifest v2) and #997 (`language_guidance` split)** | the `class` column and its CI teeth |
| **Alexandra Aikhenvald**, *Evidentiality* (2004) | the enumeration in §A1.1.2, which is owed verification against her survey before use |
| **the orchestrator** | the disclosure that the n = 4 sample preceded the boundary prediction — volunteered against the prediction's own interest, which is the only reason §A1.2.6 exists (misattributed to the steward in the first draft of this table; corrected) |

---

**Written before any leg ran. Additive to `RECOGNITION_PREREG.md`; no delivered band, kill,
VOID or prediction is altered by it. Pending steward review and freeze.**
