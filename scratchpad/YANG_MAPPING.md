# Yang et al. 2017 edit-intention taxonomy → CIRISOntology commitment-kind taxonomy

Source: Yang, Halfaker, Kraut, Hovy, "Identifying Semantic Edit Intentions from
Revisions in Wikipedia" (EMNLP 2017), repo `diyiy/Wiki_Semantic_Intention` (MIT
license), cloned to `scratchpad/yang_corpus/`. Definitions below are quoted from
the paper's Table 1, not reconstructed from memory.

**The axis distinction this note exists to keep visible.** Yang's taxonomy answers
*why did the editor make this edit?* (illocutionary purpose / intent). Ours answers
*what kind of thing changed?* (commitment-kind of the artifact site that varied —
`WrongKind`/`ChoiceKind` in `Core/WrongKind.lean`, generated from a speech-act model
in `Core/Generator.lean`). The two axes are not the same axis wearing different
names. A label can be tight enough in practice that its target content-kind is
almost always one thing (DETERMINATE), loose enough that the same intent produces
different content-kinds depending on what was actually written (PARTIAL), or
entirely off-axis — describing editor posture or platform workflow rather than any
commitment-kind of the article's content (ORTHOGONAL). All three occur below.

## 1. What was acquired

- Repo cloned shallow (`--depth 1`) into `scratchpad/yang_corpus/`, 8.8 MB `.git`,
  well under the size ceiling. No large binary data files beyond two `.jar`
  classifiers and a small XML config in `src/pred_src/`.
- **License: MIT** (`LICENSE`, copyright Diyi Yang & Aaron Halfaker). Reuse for
  mapping/validation work is unrestricted; attribution kept in this note and in
  any future citing artifact per the paper's own request.
- **The labeled data is `edit_intention_dataset.csv`** — two columns, `rev_id` and
  `labels` (comma-joined numeric codes when a revision carries more than one
  label). **This file holds ONLY revision IDs and label codes — no diff text.**
  Revision content must be fetched live from the Wikipedia API (the README points
  at `mwapi`/`revscoring` and `https://en.wikipedia.org/wiki/WP:Labels?diff=<rev_id>`).
  This is a real feasibility constraint, addressed in §4.
- `src/feat_src/` and `src/pred_src/` are Yang's own feature-extraction and
  classifier code (revscoring-based, Python 3.5, word2vec embeddings hosted
  off-repo) — not needed for our mapping use, kept for provenance only.

### Counts, measured directly from the CSV (not from the paper's rounded percentages)

| quantity | count |
|---|---|
| total rows (data rows, excl. header) | 7,169 |
| rows with a non-empty label field | **5,777** |
| rows with an empty label field | 1,392 |
| rows carrying exactly 1 label | 4,632 |
| rows carrying 2+ labels (multi-label) | 1,145 (889×2, 217×3, 33×4, 6×5) |
| total label *instances* (sum over multi-label rows) | **7,223** |

The paper states its expanded corpus as 7,177 hand-labeled revisions; the local
release has 7,169 rows total, of which only 5,777 carry a label. **The cause of
the 1,392 blank rows is not documented in the repo and is reported as an open
data-quality note, not resolved by assumption** (per the discipline against
inventing a null one hasn't checked) — plausible causes include post-2017
Wikipedia revision deletion/oversight or an artifact of the public release, but
neither is verified here. All counts below use the 5,777 labeled rows only.

## 2. The 13(+1) labels, exactly as defined in the paper's Table 1

The paper calls this a "13-category taxonomy" — the 14th code, `other`, is the
explicit residual ("None of the above"), not a 14th substantive intention. README's
label→integer map (0–13) matches the CSV.

## 3. Mapping table

Verdict legend: **DETERMINATE** = one kind, reliably, given the label's own
operational definition. **PARTIAL** = kind depends on content; disambiguator
named. **ORTHOGONAL** = the label is about editor intent/posture or platform
workflow, not commitment-kind; the content touched could be any of our kinds and
inspecting the diff does not resolve it to one, because the defining feature of
the label sits off this axis entirely.

| label (code) | n | paper's definition | verdict | our kind(s) | rationale |
|---|---:|---|---|---|---|
| **fact-update** (1) | 374 | "Update numbers, dates, scores, episodes, status, etc. based on newly available information" | **DETERMINATE** | Facts | Textbook assertive-content edit — makes a checkable world-fact right. Matches `empirical`/Facts exactly; no boundary risk. |
| **elaboration** (8) | 859 | "Extend/add substantive new content; insert a fact or new meaningful assertion" | **DETERMINATE** | Facts | The paper's own wording ("insert a fact or new meaningful assertion") is Searle's assertive content, which `Generator.lean` maps to Facts by name (`factContent` site). Caveat: in principle "new content" could carry a directive or model-application sentence, but Wikipedia article prose is overwhelmingly assertive, so within this corpus the mapping holds without inspection. |
| **verifiability** (9) | 706 | "Add/modify references/citations; remove unverified text" | **DETERMINATE** | Confidence | This is the cleanest boundary-case confirmation in the set: adding a citation changes the *warrant* for a claim while the claim's content is untouched — exactly the Confidence/Facts split in `WrongKind.lean` ("the proposition can stay identical while warranted confidence changes"). "Remove unverified text" is verifiability-not-truth (Wikipedia's own WP:V framing), i.e. removal keyed on epistemic warrant, not on the assertion having been checked false — still Confidence, not Facts. |
| **disambiguation** (12) | 131 | "Relink from a disambiguation page to a specific page" | **DETERMINATE** | Identity | A declarative act — fixes what a term/link *counts as* referring to. Direct instance of Searle's declarations → Identity mapping in `Generator.lean` (`declarationContent` site). |
| **wikification** (5) | 2,407 | "Format text to meet style guidelines, e.g. add links or remove them where necessary" | **DETERMINATE** | Structure | Markup/link encoding changes, content/meaning invariant — the `encoding` site in `Generator.lean` ("serialization/encoding layer, form vs content") named almost verbatim. Largest single bucket in the corpus (33% of instances). |
| **copy-editing** (3) | 1,060 | "Rephrase; improve grammar, spelling, tone, or punctuation" | **DETERMINATE** | Manner | "Tone" is literally register. Textbook `pragmatic`/Manner: presentation wrapper, not content. |
| **clarification** (11) | 292 | "Specify or explain an existing fact or meaning by example or discussion without adding new information" | **DETERMINATE** | Manner | Definition explicitly excludes new content ("without adding new information") — presentation/explanation changes only, meaning held fixed. Same bucket as copy-editing. |
| **refactoring** (2) | 205 | "Restructure the article; move and rewrite content, without changing the meaning of it" | **PARTIAL** | Structure / Manner | The definition bundles two different sites in one label: "move... content" (reorganization, form-level, Structure) and "rewrite content" (wording-level, Manner). A given refactoring-labeled revision could be pure reorg, pure rewrite, or both — the diff disambiguates, the label alone does not. |
| **simplification** (7) | 329 | "Reduce the complexity or breadth of discussion; may remove information" | **PARTIAL** | Manner / Facts | "Reduce complexity" (simpler wording, same claims) is Manner; "may remove information" (fewer assertions survive) is Facts. The label does not distinguish which happened. |
| **point-of-view** (13) | 160 | "Rewrite using encyclopedic, neutral tone; remove bias; apply due weight" | **PARTIAL** | Manner / Confidence / Facts | Three sub-operations bundled: "neutral tone" is Manner (wording/register); "apply due weight" is Confidence (WP:DUE — calibrating how much credence a claim gets relative to its sourcing, i.e. a warrant operation); converting an unattributed assertion into an attributed opinion changes truth-conditions and is Facts. Needs the diff to resolve. |
| **counter-vandalism** (0) | 104 | "Revert or otherwise; remove vandalism" | **ORTHOGONAL** | — | Defined by editor posture (undoing bad faith), not by what kind of content was restored — could be Facts, Structure, Rules, anything, depending on what the reverted vandalism touched. This is the task brief's own paradigm case. |
| **vandalism** (6) | 140 | "Deliberately attempt to damage the article" | **ORTHOGONAL** | — | The mirror case: defined by malicious intent, not by damage mechanism (blanking reads as Structure-removal, false-info insertion reads as Facts, obscenity insertion reads as Manner-corruption — the *label* picks none of these, the intent axis does all the work). |
| **process** (10) | 420 | "Start/continue a wiki process workflow such as tagging an article with cleanup, merge or deletion notices" | **ORTHOGONAL** | — | **Name collision, not overlap**: Yang's "process" is Wikipedia's own administrative workflow (maintenance-tag invocation) — an act *about* the platform, not a claim, permission, or step-order *within* the article. Our `procedural`/Process kind means step-order in a process **description** (`stepOrder` site) — narrative encyclopedia articles essentially never carry that. If forced into our schema the tag-insertion mechanic reads closest to Structure (markup/template insertion), but the label's defining feature (workflow-invocation) is off-axis, so this is filed ORTHOGONAL rather than folded into Structure. |
| **other** (4) | 36 | "None of the above." | **N/A** | — | Residual by construction in their own scheme; excluded from validation counts (no positive expectation to test against). |

Row sum check: 374+859+706+131+2407+1060+292+205+329+160+104+140+420+36 = 7,223,
matching the measured total label-instance count in §1.

## 4. Feasibility verdict

**5 of our 12 kinds get a DETERMINATE external-validation pool from this corpus;
7 get none.**

| our kind | DETERMINATE label-instances available | PARTIAL pool that could add more | notes |
|---|---:|---|---|
| Structure | **2,407** (wikification) | + up to 205 (refactoring, reorg half) | by far the largest, cleanest pool |
| Manner | **1,352** (copy-editing 1,060 + clarification 292) | + up to 694 (refactoring/simplification/POV, wording half of each) | largest after Structure |
| Facts | **1,233** (fact-update 374 + elaboration 859) | + up to 489 (simplification/POV, content-removal half) | strong |
| Confidence | **706** (verifiability) | + up to 160 (POV, due-weight half) | solid, single clean source |
| Identity | **131** (disambiguation) | — | small but unambiguous, single-purpose |
| Priorities, Rules, Circumstances, Process (ours), Model, Premises, Record | **0** | **0** | see below |

**Why seven kinds get nothing here.** This is a structural fact about the domain,
not a defect in Yang's taxonomy or ours: encyclopedia article prose is almost
entirely assertive (Searle's sense). It essentially never contains directives
(no Rules — that needs policy-page text, not article text), preference rankings
over outcomes (no Priorities), explicit step-ordered procedures (no Process in
*our* sense — see the `process` name-collision row above), applied-inference-rule
content (no Model), founding-assumption/decomposition-premise content (no
Premises — that varies *across* annotation harnesses, not within Wikipedia
articles), or a frame-relation to a record's provability (no Record — closest
near-miss is `counter-vandalism`/`vandalism`, restoring/damaging prior state, but
that is a stretch not claimed here). `Circumstances` is out of scope by
construction in our own taxonomy (the unchosen/luck marker), so its absence here
is expected, not a gap.

**Usable design, if this validation is run.** DETERMINATE rows are ready-made
stratified samples: draw N per target kind from {wikification→Structure,
copy-editing+clarification→Manner, fact-update+elaboration→Facts,
verifiability→Confidence, disambiguation→Identity}, fetch each revision's diff via
the Wikipedia API by `rev_id` (mwapi, per the README — **not included locally,
this is the binding feasibility gate**), run our own kind-classifier/panel on the
diff blind to Yang's label, and score agreement. This is a genuine external check
because Yang's annotators worked from a different question (intent) using a
different guideline, on a domain (Wikipedia) our own ecological study's
Wikipedia stream never reached (`ECOLOGICAL_RESULTS.md`: "Wikipedia DEFERRED —
sustained API 429s") — so this corpus is a live, unblocked substitute path into
the one stream the internal ecological run could not complete, at costs of (a)
needing live API fetch per item, a small fraction of which may 404 on
old/deleted/oversighted revisions, and (b) PARTIAL-row items (694 label-instances,
~12% of the labeled pool) needing manual content inspection before they can
serve, since the label alone does not fix a kind.

**What this corpus cannot validate at all**, regardless of budget: the 7 kinds
with zero DETERMINATE or PARTIAL coverage above. Confirming those needs a
different domain — policy/regulatory text (Rules, matching the internal
ecological run's Federal Register stream, which already scored Rules 93%),
procedural/instructional text (Process), or something with an explicit reasoning
chain (Model, Premises) — not Wikipedia article-edit intent labels.
