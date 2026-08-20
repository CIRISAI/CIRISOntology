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
