# The 29-language labeled testbed (registered 2026-08-20, steward-disclosed)

The steward points out an asset the programme had not inventoried: the agent ecosystem
already carries the taxonomy's vocabulary across 29 languages, tested extensively by
RATCHET, with live labeled data in CI and locally.

## What exists, verified on disk

1. **The Greek spine.** RATCHET's public taxonomy page (docs/index.html) labels each of
   the eleven plain words with its philosophical name — the steward's "in the Greek":

   | plain | spine | | plain | spine |
   |---|---|---|---|---|
   | Facts | empirical | | Circumstances | contingent |
   | Rules | deontic | | Process | procedural |
   | Manner | pragmatic | | Structure | structural |
   | Identity | ontological | | Model | nomological |
   | Priorities | axiotic | | Premises | axiomatic |
   | Confidence | epistemic | | | |

   RATCHET#23 is adopted: plain words primary, the spine underneath for precision.
   (Observed, not over-read: the surface four all carry Greek-rooted names; the three
   Latin-rooted names — contingent, procedural, structural — are all deep-seven.)

2. **The 29-language prompt stack.** CIRISAgent ships its full reasoning stack — all 7
   DMA/conscience prompts — in English + 28 locales
   (`ciris_engine/logic/dma/prompts/localized/{am,ar,bn,de,es,fa,fr,ha,hi,id,it,ja,ko,mr,my,pa,pt,ru,sw,ta,te,th,tr,uk,ur,vi,yo,zh}/`),
   plus the accord in 29 locales (`ciris_engine/data/localized/`) and the polyglot weave
   ("woven from 15 languages by semantic weight" — three keys, reaching all four
   conscience faculties; RATCHET POLYGLOT_PROBLEM.md documents the confound structure).
   The historical commit is named: "PDMA v3.2: polyglot extraction + 28-locale fan-out."

3. **Labeled live data.** RATCHET's harness has line-level adjudications
   (experiments/torque/partition/adjudications/*.tsv, 272 lines, HOLD/SWAP with reasons
   and confidence), CI TEE traces (exp1b accord-batch JSONs, 5-vendor crossfamily), and
   the validation series with measured floors against human labels.

## What it is FOR (staked uses, each with its own gate)

- **T5 instrument (translation-forced disambiguation).** The 29 translations are a fossil
  record of decisions English left unmade: languages with obligatory grammatical marking
  (Turkish evidential -mIş; others in the set) FORCED their translators to disambiguate
  source-of-knowing where English "confidence" vocabulary is silent. Probe: extract how
  each locale's prompts render the Confidence/Model boundary vocabulary; where a grammar
  obligates evidential marking, the translation had to choose — the choices are data on
  whether SOURCE is inside Confidence or a distinct site. Cheap, in-hand, no new corpus.
  GATE: translations may be machine-produced or single-translator — provenance per locale
  must be established before any translator-choice is read as a native-speaker judgment.
- **A0-successor candidates.** RATCHET's TEE streams + adjudication TSVs are live labeled
  corpora unlike the fouled override corpus. GATE: check label/action degeneracy FIRST
  (the A0 foul: override near-deterministic in selected_action fouls every 3-way test).
- **Cross-linguistic gross-four replication.** If any locale's live traffic can be
  kind-labeled, the 91% surface-four claim gets its first non-English test.

## On anthropomorphism (steward's ruling, adopted with its discipline)

The steward: anthropomorphizing the universe is just another term for making it
understandable to us; we are humans, working mostly with human data, and the model doing
the work is assembled from human words in human orders. ADOPTED: human words are the
programme's instrument and its subject — the word-test method treats them as DATA, which
is the opposite of contamination. The discipline stays anyway, restated without apology:
the rename test and the blind panels exist so that when a warm old word survives, we know
the THEOREM earned it and not the warmth. Anthropomorphism as interface: yes, always.
Connotation as evidence: never. Both halves are the method.

## FOUND (2026-08-20, second pass): the categorization column itself

The steward's pointer ("research CI workflow on agent or ratchet") resolved it. The column
is **`class` in CIRISAgent's `compose_dump`** — every block of the agent's LLM-facing
corpus carries one of the Greek-spine labels or `mixed`:

    python3 -m ciris_engine.logic.utils.compose_dump dump --locales en

My earlier all-tree greps missed it because the local checkout sits on an old branch
(`fix/oauth-setup-asks-for-a-password`); the machinery lives on main from ~2.9.10
(#976 regime manifest v2, #997 language_guidance split). Verified live at origin/main
(2.9.28, scratch worktree):

- en: 635 blocks — deontic 128, mixed 93, pragmatic 92, procedural 88, structural 59,
  axiotic 55, contingent 32, epistemic 29, empirical 28, ontological 15, nomological 15.
  **axiomatic: zero shipped blocks** (the class exists — the κ annotators used it — but
  no shipped block carries it; noted, not over-read).
- The split five (en es fr it pt, RATCHET#19 / CIRISAgent#997): 634 blocks each, mixed
  blocks in eight families decomposed into routed fragments. The other 24 locales resolve
  through the unsplit parent: 228 blocks, 37 mixed.
- CI teeth: `compose_dump gate` REFUSES a run that varies a mixed block without a
  per-block disposition + contaminant list (TORQUE_REGIME.yaml §10.2.1) — the labels are
  load-bearing in CI, not decorative.

**The provenance verdict is already measured** (RATCHET kappa_2026-08-07, n=30
language_guidance parts): two independent annotators from operational definitions only —
**A-vs-B κ = 0.831 (reliability PASS)**, but **A-vs-shipped 0.528 / B-vs-shipped 0.558
(validity FAIL)**. RATCHET's own words: "The taxonomy is reliable. Its application to
`language_guidance` is not validated." So for our use: the CLASS VOCABULARY and the
independent annotator TSVs are well-provenanced; the SHIPPED labels are an unvalidated
convenience and must not be treated as ground truth. Any T5/corpus use goes through the
annotator-grade path (fresh independent labels, shipped column as a comparison arm), which
is exactly the prereg's provenance-gate shape.

Bonus finding for the record: both κ annotators independently re-labeled the shipped
`11_routing_doctrine` (shipped: axiotic) as **procedural** — a live example of a
kind-boundary dispute (Priorities-vs-Process) surfacing in production corpus governance.
