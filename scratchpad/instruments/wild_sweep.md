# N4 — WILD SWEEP of the six v0b instruments, out-of-sample

Instruments: `empirical` (Facts), `deontic` (Rules), `epistemic` (Confidence),
`pragmatic` (Manner), `ontological` (Identity), `axiomatic` (Premises) — from
`/home/emoore/CIRISOntology/scratchpad/instruments/v0b.py`, called as
`fn(before, after)` per item, heuristic halves only, no retrieval/judges/network.

Corpora: `eco_corpus.jsonl` (170, streams fedreg/osm/github), `eco_osm2.jsonl`
(60), `eco_wiki2.jsonl` (49), `part_d.jsonl` (12 authored boundary items) — 291
items total, 279 of them genuinely WILD (`kind_target: "WILD"`), 12 authored.

Panel modal: BASE-condition `kind` field (plain names) from
`eco_judgments.jsonl` / `eco2_judgments.jsonl` / `eco2_wiki_judgments.jsonl` /
`partd_judgments.jsonl`, 3 judge models each. Ties (no unique top vote) and
votes outside the 12-kind taxonomy are excluded, same rule as `v0b.provisional_gold`.

Full data: `wild_sweep.json`. This file is the readable digest.

## Pre-registered expectation (stated before this run)

> Wild Premises should be RARE — the axiomatic conjunction (definition-position
> AND ripple>=2) firing at a high rate in the wild means it overfits the
> authored corpus; a low-and-sensible rate (config/code definition changes,
> little else) means it generalizes.

## 1. Fire-rate table (per stream, per instrument)

| stream | n | empirical | deontic | epistemic | pragmatic | ontological | **axiomatic** |
|---|---:|---:|---:|---:|---:|---:|---:|
| eco_corpus (fedreg+osm+github) | 170 | 20 (11.8%) | 25 (14.7%) | 0 | 0 | 0 | **0 (0.0%)** |
| eco_osm2 | 60 | 4 (6.7%) | 0 | 0 | 0 | 0 | **0 (0.0%)** |
| eco_wiki2 | 49 | 1 (2.0%) | 3 (6.1%) | 1 (2.0%) | 1 (2.0%) | 6 (12.2%) | **0 (0.0%)** |
| **wild subtotal** | **279** | 25 (9.0%) | 28 (10.0%) | 1 (0.4%) | 1 (0.4%) | 6 (2.2%) | **0 (0.0%)** |
| part_d (authored boundary) | 12 | 2 (16.7%) | 0 | 0 | 0 | 4 (33.3%) | **1 (8.3%)** |
| **all 291** | 291 | 27 (9.3%) | 28 (9.6%) | 1 (0.3%) | 1 (0.3%) | 10 (3.4%) | **1 (0.3%)** |

## 2. Axiomatic wild verdict: **GENERALIZES**, more strongly than staked

Zero axiomatic (Premises) fires across all 279 wild items, in every stream
(fedreg regulatory text, OSM tag diffs, GitHub diffs, OSM2, Wikipedia prose).
The pre-registered expectation allowed for a "low-and-sensible" rate
concentrated in config/code definitions; the observed rate is not merely low,
it is exactly zero on genuinely wild data. This is the strongest form of the
"generalizes" outcome, not a marginal pass — the definition-position AND
ripple>=threshold conjunction essentially never coincides by accident in real
text.

The only axiomatic firing anywhere in this sweep is on the **authored**
part-D boundary set (1/12, 8.3%), and — see anomaly below — it is a
**false positive** against unanimous panel judgment (panel said Identity
3/3, axiomatic instrument said Premises). So even the instrument's one
"successful" wild-adjacent firing is not a hit: it is exactly the kind of
spurious ripple-on-generic-vocabulary event the design note behind
`axiomatic()` warns about. Read together, the wild sweep does not just fail
to falsify "generalizes" — it suggests the more precise finding is
**"generalizes by staying silent, and its rare firings are unreliable."**

### 2a. Every axiomatic firing, verbatim (the complete set — n=1)

```
id:                 ontological-registry-07  (part_d, authored — NOT wild)
kind_target:        ontological
panel modal:        Identity (3/3 unanimous: Llama-4-Scout, gemma-3-27b, gpt-oss-120b)
instrument verdict: FIRED (Premises) — a false positive against the panel

evidence.definitional:      true
evidence.definitional_why:  pattern 'For the purposes of'
evidence.ripple:             3
evidence.ripple_mentions:    3
evidence.ripple_inherited:   0
evidence.threshold:          2
evidence.anchors:            ["carried", "county", "list", "population"]
evidence.mode:               prose

reason: "changed span sits in a definition/assumption position (pattern 'For
         the purposes of') and 3 downstream segments depend on it"

text (before -> after, changed span only):
  "...the population is carried under the genus Ranunculus, following..."
  "...the population is carried under the genus Ficaria, following..."
```

**Why this is a false positive, not a genuine Premises event:** the sentence
carries the classic definitional cue ("For the purposes of this list, the
population is carried under the genus X") and the anchor set (`carried`,
`county`, `list`, `population`) hits three other segments — but those are
generic document-scaffolding words in a registry document that is *about* a
population and a list, not genuine downstream dependents of the genus term.
The actual content of the edit is a straightforward taxonomic reclassification
(Ranunculus -> Ficaria), which all three judges independently and unanimously
called Identity. This is a textbook case of the definitional-position
detector correctly recognizing prose that IS structured as a definition,
while the ripple counter over-credits topical vocabulary overlap as
dependency. No wild item produced this failure mode; it took the harder,
adversarially-authored boundary corpus to find it.

## 3. Agreement matrix: instrument vs panel-modal, per stream

TP = instrument fired AND panel modal equals that instrument's plain kind.
FP = instrument fired AND panel modal is a different kind.
FN = instrument silent AND panel modal equals that instrument's plain kind.
TN = instrument silent AND panel modal is a different kind.
"no panel" = item excluded (panel tie, or all 3 votes fell outside the
12-kind taxonomy) — not scored either way, same exclusion rule as
`v0b.provisional_gold`.

### eco_corpus (n=170, valid panel=148, excluded=22 ties/off-taxonomy)

| instrument | fires | TP | FP | FN | TN | false-fire sources |
|---|---:|---:|---:|---:|---:|---|
| empirical | 20 | 1 | 15 | 44 | 88 | Rules:13, Identity:2 |
| deontic | 25 | 25 | 0 | 44 | 79 | — |
| epistemic | 0 | 0 | 0 | 0 | 148 | — |
| pragmatic | 0 | 0 | 0 | 11 | 137 | — |
| ontological | 0 | 0 | 0 | 11 | 137 | — |
| **axiomatic** | **0** | 0 | 0 | 0 | 148 | — |

Note: `deontic` is perfect-precision here (25/25 fires all agree with panel
Rules) on a stream dominated by fedreg regulatory-permission text — expected
given the domain. `empirical`'s false fires are concentrated on Rules (13):
value substitutions inside regulatory clauses that the panel reads as
rule-content changes rather than fact changes — a genuine Facts/Rules
boundary confusion in regulatory prose, consistent with `v0b`'s own
documented suppressor list not fully covering fedreg-style permission counts.

### eco_osm2 (n=60, valid panel=53, excluded=7)

| instrument | fires | TP | FP | FN | TN | false-fire sources |
|---|---:|---:|---:|---:|---:|---|
| empirical | 4 | 3 | 0 | 27 | 23 | — |
| deontic | 0 | 0 | 0 | 3 | 50 | — |
| epistemic | 0 | 0 | 0 | 0 | 53 | — |
| pragmatic | 0 | 0 | 0 | 4 | 49 | — |
| ontological | 0 | 0 | 0 | 14 | 39 | — |
| **axiomatic** | **0** | 0 | 0 | 0 | 53 | — |

`empirical` is precision-1.0 on OSM tag diffs (3/4 TP, 0 FP; one fire has no
scored panel item). Every other instrument stays silent — OSM key=value tag
diffs give the deontic/pragmatic/ontological heuristics almost nothing to
grab (recall gap is real: e.g. ontological FN=14, ontological never fires),
but importantly none of them false-fire either.

### eco_wiki2 (n=49, valid panel=44, excluded=5)

| instrument | fires | TP | FP | FN | TN | false-fire sources |
|---|---:|---:|---:|---:|---:|---|
| empirical | 1 | 1 | 0 | 15 | 28 | — |
| deontic | 3 | 0 | 2 | 0 | 42 | Facts:1, Manner:1 |
| epistemic | 1 | 1 | 0 | 0 | 43 | — |
| pragmatic | 1 | 1 | 0 | 19 | 24 | — |
| ontological | 6 | 0 | 5 | 5 | 34 | Circumstances:1, Facts:2, Manner:2 |
| **axiomatic** | **0** | 0 | 0 | 0 | 44 | — |

The weakest stream for precision: `ontological` fires 6 times and agrees with
the panel 0 times (5 FP + 1 unscored) — free-running Wikipedia prose has
plenty of is-a-shaped sentences that are not, in the panel's reading, Identity
edits. `deontic` is also mostly wrong here (0/3 correct). Both stay well
short of axiomatic's zero-false-fire record; the axiomatic instrument is the
*cleanest* instrument on this stream by construction (silence has no FP cost),
but is also the only one to record zero true positives too — trivially, since
recall is 0/0 (no wiki2 item has panel modal Premises).

### part_d (n=12, valid panel=12, excluded=0) — authored, not wild

| instrument | fires | TP | FP | FN | TN | false-fire sources |
|---|---:|---:|---:|---:|---:|---|
| empirical | 2 | 0 | 2 | 2 | 8 | Rules:2 |
| deontic | 0 | 0 | 0 | 5 | 7 | — |
| epistemic | 0 | 0 | 0 | 0 | 12 | — |
| pragmatic | 0 | 0 | 0 | 0 | 12 | — |
| ontological | 4 | 3 | 1 | 2 | 6 | Facts:1 |
| **axiomatic** | **1** | 0 | 1 | 0 | 11 | Identity:1 |

The one place axiomatic fires at all, it is a false positive (detailed in
§2a). `empirical` also underperforms here (0/2 TP) — see §4, both empirical
false fires are on the two boundary items the panel absorbed into Rules.
`ontological` performs best (3/4 TP) — it is exactly what correctly catches
the two Identity-absorbed empirical-target items (§4).

## 4. Part-D four absorbed items (empirical-report-07, -08, -09, -11)

These four were authored with `kind_target: empirical` but the panel's BASE
modal absorbed them elsewhere — into Rules (07, 08) or Identity (09, 11),
never into Facts. Per-instrument readout:

### empirical-report-07 — byelaw light-hours sentence
Panel modal: **Rules** (3/3). Change: "between sunset and sunrise" ->
"at all times when afloat" (byelaw scope, author's note: describes what the
byelaw requires, provision itself unchanged).
- `empirical`: silent — "no checkable value substituted in the changed span"
  (the substitution is a phrase, not a value token the instrument's
  value-extractor resolves).
- `deontic`: silent — "no obligation/permission/prohibition altered."
- `epistemic`/`pragmatic`/`ontological`: silent, no relevant cue.
- `axiomatic`: **near-miss**, does NOT fire — "definition position but ripple
  1 < 2 — low dependency, route toward Facts (empirical)." Definitional cue
  matched on the phrase "all times"; ripple=1 (anchor "harbour").
- **No instrument agrees with the panel's Rules call on this item.**

### empirical-report-08 — flammable-store checking interval
Panel modal: **Rules** (2/3, one Facts). Change: "every fortnight" -> "every
week" (report's claim about what the site manual states, author's note: the
manual itself is untouched).
- `empirical`: silent — "no checkable value substituted."
- `deontic`: silent — "no obligation/permission/prohibition altered."
- `axiomatic`: silent — "changed span is not in a definition/assumption
  position (ripple would be 4)."
- All others silent.
- **No instrument agrees with the panel's Rules-majority call.**

### empirical-report-09 — churchyard tree species
Panel modal: **Identity** (2/3, one Facts). Change: "an English oak" -> "a
sycamore" (field misidentification correction).
- `ontological`: **FIRES**, and agrees — "category reassigned: english oak
  measured three girth chest height -> sycamore measured three girth chest
  height."
- `empirical`: silent — "no checkable value substituted" (the extractor does
  not treat a bare noun swap as a value).
- All others silent.
- **`ontological` alone matches the panel here.**

### empirical-report-11 — corner-unit shop type
Panel modal: **Identity** (2/3, one Facts). Change: "a pharmacy" -> "a
barber's" (street-walkabout observation correction).
- `ontological`: **FIRES**, and agrees — "category reassigned: pharmacy open
  six days awning newly recovered -> open six days awning newly recovered."
- `empirical`: silent — same reason as -09.
- All others silent.
- **`ontological` alone matches the panel here.**

**Reading:** the panel's absorption pattern is coherent and the instruments
partially track it. The two tree/shop items (09, 11) are genuinely is-a
reclassifications and `ontological` catches both cleanly — the "empirical"
label these items were authored under looks like an authoring miss corrected
by the panel and confirmed by an independent instrument. The two byelaw/manual
items (07, 08) are genuinely harder: the panel reads them as Rules because the
sentence describes what a rule requires/states, but no instrument — including
`deontic` — recognizes them as such, because the actual edited tokens are a
temporal-scope phrase and a frequency phrase, not a modal verb or permission
word the deontic heuristic watches for. This is a real coverage gap, but it
is a **miss (false negative), not a false alarm** — consistent with, not
contrary to, the "axiomatic overfitting" question this sweep was staked
against, and worth flagging to whoever owns `deontic`/`empirical` scope next
(the fix is watching temporal/frequency phrases embedded in a
requires/states clause, not a ripple change).

## 5. Anomalies

1. **The only axiomatic firing outside the training-adjacent authored corpus
   is a false positive** (§2a) — reinforces the "generalizes, and treat any
   rare firing with suspicion" reading rather than a clean validation.
2. **`empirical` vs `deontic` boundary confusion in fedreg text**: 13 of
   `empirical`'s 15 false fires in eco_corpus are cases the panel calls
   Rules — regulatory value changes (thresholds, counts) inside permission
   clauses that the current suppressor list (`_config_key` permission-key
   check is config-mode only) does not catch in prose fedreg text.
3. **`ontological` over-fires on eco_wiki2** (6 fires, 5 FP, 0 TP, 1
   unscored) — free Wikipedia prose has abundant is-a-shaped sentences
   (renamings, appositions) that the panel does not read as Identity changes;
   worth a closer look if `ontological` gets tuned next, independent of the
   axiomatic question this task was staked on.
4. **part_d empirical-report-07/-08 have no matching instrument at all**
   (§4) — a real recall gap for `deontic`/`empirical` on
   requires/states-governed temporal and frequency phrases, flagged but out
   of this task's scope (axiomatic was the staked target).
5. No instrument threw an exception or produced an unexpected `refused` on
   any of the 291 items; every REFUSED reading elsewhere in the corpus was
   the expected `identical-input` or `empty-baseline` case (none occurred in
   this sweep — all 291 before/after pairs differ and are non-empty).

## Method notes

- Pure local compute: `v0b.py`'s six instrument functions called directly,
  `fn(before, after)`, stdlib only (`difflib`, `json`, `re`, `collections`).
- Panel modal computed independently per corpus file against its own matched
  judgments file (not `v0b.provisional_gold`, which is wired to
  `corpus_full.jsonl`/`full_judgments.jsonl` — a different, larger corpus not
  in scope for this task).
- Tie/off-taxonomy exclusion rule matches `v0b.provisional_gold` exactly:
  count only `condition == "BASE"` votes whose `kind` is one of the 12 plain
  taxonomy names; a tied top count excludes the item from scoring.
- `part_d` is reported separately from the three wild streams throughout
  because it is explicitly the *authored* boundary corpus (12 items,
  `difficulty: hard`, deliberately ambiguous) — folding it into the "wild"
  fire-rate would understate how clean the wild-only zero-fire result is.
