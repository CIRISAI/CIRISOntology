# VALENCE — prior-art and mechanism sweep (filed 2026-08-20)

Scope: verification of the two staked faces; rival mechanisms; the mechanism-search verdict
(has anyone unified the split under a maintenance/thermodynamic asymmetry?); native-rated
dataset inventory; cost-of-destruction literature.

Method: web sweep, primary sources fetched and text-extracted where obtainable. Where a
paywall blocked the primary, that is stated rather than papered over. Numbers below are
quoted from the primary text unless marked SECONDARY.

**Headline verdict: CROWDED-ADJACENT.** The *pairing* of the two faces is already a named
model with both properties stated together (Unkelbach's Evaluative Information Ecology).
The Anna-Karenina mechanism for the differentiation face is already published (Alves/Koch/
Unkelbach's bounded-range argument, explicitly Tolstoy-framed in a 2023 follow-up). An
information-theoretic single-quantity version already exists (Garcia, Garas & Schweitzer
2012). **Nobody derives both faces from a maintenance/decay/thermodynamic asymmetry** — and
the leading incumbent (Rozin) states in print that its own unification fails. That is the
niche, and it is narrow.

---

## 1. VERIFICATION OF THE TWO FACES

### 1a. Face A — POSITIVE IS MORE FREQUENT (Pollyanna). VERIFIED, CONTESTED IN DEGREE.

**Boucher & Osgood 1969**, "The Pollyanna hypothesis", *Journal of Verbal Learning and
Verbal Behavior* 8(1):1–8.

**⚠ CORRECTION TO THE NOTE — LOAD-BEARING.** VALENCE_NOTE.md cites Boucher & Osgood for
"POSITIVE = FREQUENT BUT COARSE". They claim the opposite of the second half. Their thesis
is a universal tendency to use evaluatively positive words (E+) **"more frequently and
diversely"** than negative words (E−) — positive words are described as "more prevalent,
more meaningful, **more diversely used**, and more readily learned." Whatever B&O meant by
"diversely" (usage across contexts vs. distinct types is not disambiguated in the secondary
literature I could reach; the primary is paywalled at ScienceDirect), **the founding
Pollyanna paper asserts positive diversity, not positive coarseness.** The note currently
recruits B&O as support for a claim they contradict on its face. Any prereg must either
(i) read the 1969 primary and pin what "diversely" measures, or (ii) drop B&O from the
differentiation leg and cite them for frequency only. Do not carry this forward as written.

**Dodds et al. 2015**, "Human language reveals a universal positivity bias", *PNAS*
112(8):2389–2394. Verified from the PMC full text:
- 10 languages: English, Spanish, French, German, Brazilian Portuguese, Korean, Simplified
  Chinese, Russian, Indonesian, Arabic. 24 corpora (books, news, social media, web, TV/movie
  subtitles, music lyrics).
- 5,000–10,000 most frequent words per corpus; ~10,000 per language after merging.
- ~5 million individual human ratings, 50 ratings per word, 9-point scale.
- **Native speakers, region-restricted** (e.g. Portuguese rated by residents of Brazil).
  This matters for our gate 3 — labMT is NOT a translated lexicon.
- Frequency-dependence: they report α ~ −1×10⁻⁵, i.e. h_avg falls ~0.1 per 10,000 rank,
  and describe the happiness distribution as applying to "common words and rare words alike."

**The Garcia critique — read it, it is not a footnote.** Garcia, Garas & Schweitzer 2015,
*PNAS* 112(23):E2983. Three attacks, from the letter's own text:
1. **Measurement bias from the emoticon scale.** labMT used cartoon faces; a non-smiling
   face is perceived as slightly negative, inflating scores. Their test: LIWC's 399 function
   words should be neutral but score above 5 in labMT (Wilcoxon p<10⁻¹¹, **median = 5.25**).
2. **Positive shift vs. a reference lexicon.** labMT vs. Warriner & Kuperman: **median
   difference 0.28** (p<10⁻¹⁵) overall; on the **4,502-word intersection**, mean difference
   **0.07** (t-test p<10⁻¹⁵).
3. **Frequency independence is a rank-transform artifact.** Refitting h_avg = α·log(f) + β
   on actual Google Books frequencies (since 1990) instead of rank gives **significant,
   sizable dependence in four of six languages**; for English the happiness increase across
   the frequency range is **1.06** — far larger than under Dodds's rank fit. Conclusion:
   the reported "self-similarity" is "far from being universal."

**Dodds's reply** (arXiv:1505.06750, elaborated form of the PNAS letter) — verified from the
extracted text:
- LIWC function words are **not** emotionally neutral: of 450 matched function words, the
  top of the list includes "greatest" 7.26, "best" 7.18, "equality" 7.08; the bottom
  "worst" 2.10, "negative" 2.42, "cannot" 3.32. The gold standard is not gold.
- The labMT/WK histogram comparison is unsound (different words, frequency uncontrolled);
  they concede the intersection comparison is appropriate and that it gives 0.07.
- Reduced-major-axis regressions across labMT/ANEW/WK: β = 1.08, 1.07, 1.04 — WK looks
  *more* emotionally biased than labMT, not less.
- On frequency: they say they claimed "strongly" and "largely" independent, not independent;
  and that Garcia et al. "did not perform a reanalysis of our data — they instead carried
  out an analysis of a different, statistically improper data set and introduced a
  nonlinearity before performing linear regression" (word lists lacking ranks, uncontrolled
  missingness).

**Verdict on Face A.** The *existence* of a positivity frequency bias survives — it holds on
the 4,502-word intersection of two independently-built lexica at 0.07, in the direction
predicted, and Rozin's independent corpus counts (below) are not scale-artifacts at all.
What does **not** survive unqualified is (i) the magnitude, which is partly instrument, and
(ii) frequency-*independence*, which is a live methodological dispute turning on
rank-vs-log-frequency regression. **For our purposes this is the important part: any test we
run that regresses a valence quantity on frequency lands directly inside an unresolved
methods fight.** Pre-register the regression form (rank vs. log-f), justify it, and report
both. This is our own rule 3 (match the null to the generative structure) with a named
precedent for how it goes wrong.

**Rozin, Berman & Royzman 2010** independent corpus counts, from Leech/Rayson/Wilson's
100M-word spoken+written British English corpus (verified from the PDF):
- good **795** / bad **153** per million
- happy **117** / (unhappy 19 + sad 34 = **53**)
- pleasant **27** / (aversive <10 + unpleasant 13)
- beautiful **87** / ugly **14**
- clean **48** / (dirty 26 + unclean <10)
- pure **34** / (impure <10 + contaminated <10)
- sincere and its opposites: all below the corpus's 10/million reporting floor.
Caveat: "0" in that database means <10 per million, not zero. Seven hand-picked pairs, not
a sample.

### 1b. Face B — NEGATIVE IS MORE DIFFERENTIATED. VERIFIED, WITH A WEAK INSTRUMENT.

**Rozin, Berman & Royzman 2010**, "Biases in use of positive and negative words across
twenty natural languages", *Cognition & Emotion* 24(3):536–548. Verified from the PDF.

Their thesis sentence is exactly our two faces: *"Positive events are more common (more
tokens), but negative events are more differentiated (more types)."*

**Part 2 — the lexicalisation-gap counts (the actual numbers):**

| negative noun | languages with a synonym | languages with an antonym |
|---|---|---|
| murderer | 19/20 (95%) | 5/20 (25%) |
| accident | 18.5/19 (97%) | 8/19 (42%) |
| risk | 18/20 (90%) | 4/20 (20%) |
| sympathy | 15.5/19 (82%) | 4.5/19 (24%) |
| disgust(ing) | 19/20 (95%) | 4/20 (20%) |

- Across 20 languages × 5 target words = **100 possible word pairs, exactly ONE case** where
  the positive word existed and the negative did not.
- 13 of the 20 languages had a word for **all five** negative exemplars; **none** had a
  positive opposite to all five; only two had 4/5.
- English itself has no antonym for any of the five.

**Part 1 — markedness, across 7 adjective pairs × 20 languages:**
- Unique positive word present in **94.3%** (132/140) of cases vs. unique negative word in
  **77.1%**; χ²(1,279)=16.80, p<.001.
- Positive words negatable in **69.1%** vs. negative words in **42.9%**; χ²(1,239)=11.82,
  p<.001; holds 7/7 adjectives.
- Negation of a positive word yields the opposite (not neutral) valence in **82.7%** of
  cases vs. **36.9%** for negated negatives; χ²(1,140)=32.23, p<.001.
- Informants prefer "un-negative" to "un-positive" in **89.6%** (76/85, z=7.27, p<.001).
- Positive word usable across the whole dimension in **64.3%** vs. negative in **40.7%**;
  χ²(1,220)=3.781, p<.001.
- Positive-first in conjunctions **83.9%** (70/85, z=5.97, p<.001), 7/7 adjectives.
- All **35** directional predictions (5 per word × 7 words) came out in the predicted
  direction. English largest positive bias, Arabic smallest; all 20 in the same direction.

**INSTRUMENT WARNINGS (these are severe and must be inherited by any prereg):**
1. **N = 1 informant per language.** The authors say so. They ran 10 English informants to
   gauge within-language variance and found substantial disagreement on items 8 and 9 — so
   much that *"we decided not to count English as a clear example."* One informant per
   language is a single-rater instrument on a judgment task with demonstrated rater spread.
2. **Convenience sample, all at one university.** "The first 20 qualified informants we
   could find," all Penn students or employees, all fluent in English, all interviewed **in
   English**. Cross-linguistic conclusions from bilinguals interviewed in the metalanguage
   whose asymmetries generated the hypothesis is a circularity our gate 3 should catch.
3. **Non-independent languages.** The authors concede it in footnote 2: "the 20 languages
   are related to some extent, but we treat them as independent for the purpose of computing
   and interpreting the chi-square." Every χ² above is therefore anticonservative by an
   unknown factor. This is *our* enumerated-count-is-not-effective-count problem in a
   different substrate (cf. `enumerated-count-is-not-effective-count`,
   `occupancy-must-be-measured`). A phylogenetically-controlled redo is an open target.
4. **Stimuli hand-picked from English to exhibit the effect.** "Selected by convenience,
   with the proviso that we knew in advance for all cases that the positive asymmetries we
   were exploring were present for these words in English." They partially defend this with
   a post-hoc check on the 120 most common British English adjectives, but it is a
   post-hoc check.

**Schrauf & Sánchez 2004**, "The Preponderance of Negative Emotion Words in the Emotion
Lexicon: A Cross-generational and Cross-linguistic Study", *J. Multilingual and
Multicultural Development*. SECONDARY (abstract-level): free-listed "working emotion
vocabulary" runs approximately **50% negative / 30% positive / 20% neutral**; no significant
Spanish-vs-English difference (Mexico City and Chicago samples); held across young (~20) and
older (~65) groups, with older participants showing more diversity and less overlap. Their
proffered mechanism is affect-as-information (negative affect → detailed systematic
processing; positive affect → heuristic schema-based processing), i.e. a *processing*
account, not a structural one.

**Averill 1975/1980**, *A Semantic Atlas of Emotional Concepts* and "On the Paucity of
Positive Emotions". SECONDARY: ~**558** words with emotional connotation catalogued; the
50/30/20 split above is the figure that propagates from this line. I could not obtain the
primary; the Springer chapter is paywalled and the exact unpleasant/pleasant breakdown in
Averill's own tables is **NOT VERIFIED** here. Do not cite a specific Averill percentage
without pulling the book. What is verifiable: Carlson (1967) content-analysed psychology
textbooks and found roughly **twice** as much space on negative as positive emotions — a
fact about psychologists, not about the lexicon.

**Rozin's own basic-emotion count**: of the "standard" six basic emotions, **four are
negative** (anger, disgust, fear, sadness), **one positive** (happiness), one unvalenced
(surprise).

**Verdict on Face B.** The direction is robust and replicated across independent lines
(lexicalisation gaps, markedness, free-listing, emotion taxonomies). The *quantitative*
cross-linguistic claim rests on a single-informant, convenience-sampled, English-mediated,
phylogenetically-uncorrected instrument. Face B is a solid qualitative fact and a weak
quantitative one. **A ratio-based stake (frequency ratio vs. type ratio) cannot be built on
Rozin's numbers.** It needs a corpus-and-norms instrument built for the purpose.

---

## 2. RIVAL MECHANISMS

| Rival | Claim | Covers A? | Covers B? | One principle? | Proximity to ours | What separates ours empirically |
|---|---|---|---|---|---|---|
| **Unkelbach EvIE** (2019) | Evaluative Information Ecology: positivity prevalence + negativity diversity are two structural properties of the information ecology | YES | YES | **NO** — two posited properties | **VERY HIGH** (identical explanandum, both faces already paired) | Ours claims one asymmetry *generates* both; EvIE posits both. A joint quantitative constraint linking the two magnitudes is ours, not theirs. |
| **Alves/Koch/Unkelbach bounded range** (2016–2018) | For evaluative dimensions (temperature, taste, nutrition), one positive band is flanked by two negative spectra — *too much* and *too little*. Hence more ways to be bad. Density hypothesis: positive information clusters more tightly | NO (predicts negative *more* common if anything) | YES | Yes, for B alone | **HIGH** on B; this *is* an Anna Karenina argument, and the group later frames it as Tolstoy explicitly ("The Convergence of Positivity: Are Happy People All Alike?", *J. Happiness Studies* 2023) | Geometry alone predicts many bad states but not that we mostly *occupy* the good one. Ours says occupancy is bought — so ours predicts the frequency face should track a *maintenance* covariate (upkeep intensity), theirs predicts it tracks nothing. |
| **Communicative efficiency school** (Zipf meaning-frequency law; Piantadosi/Tily/Gibson; Garcia/Garas/Schweitzer 2012) | Word length and frequency are set by average information content; **"negative words contain more information than positive words, as the informativeness of a word increases uniformly with its valence decrease"** (Garcia et al. 2012, English/German/Spanish, three affective lexica) | YES | YES (as informativeness) | **Nearly** — one measured quantity, both faces on the same axis | **HIGH** on ambition | Efficiency *describes* the frequency–informativeness coupling; it does not say why valence sits on that axis at all. Ours predicts the coupling's *sign and origin*. Also: Dodds et al. reject Garcia's use of Piantadosi's formula as a misapplication — the incumbent's flagship result is itself contested. |
| **Frijda hedonic asymmetry** (1988, "The Laws of Emotion") | *"Pleasure is always contingent upon change and disappears with continuous satisfaction"* — pain persists under continued adversity because adversity keeps violating goals | NO | NO | n/a | **VERY HIGH conceptually — this is the nearest miss in the whole sweep.** It is `rent_holds` / `unpaid_decays` stated for affect: the positive state must be continuously re-paid or it evaporates; the negative state is self-sustaining | Frijda is about hedonic *experience over time*, never about lexicon structure. Nobody has bridged it. **Bridging it is the specific contribution available to us — and it means Frijda must be cited as antecedent, not discovered.** |
| **Rozin's own two-mechanism account** (2010) | Face A from world-event frequency plus linguistic efficiency; Face B from **response-option count** — negative events afford attack/withdraw/freeze, positive events afford only approach | YES | YES | **NO, and they say so** | HIGH (it is the incumbent) | See below — this is the opening. |
| **Peeters' informational negativity** (1971, 1991) | Negative events are rarer, hence carry more informational value; people expect positive and compensate with sensitivity to negative | YES | partly | Rate-based | MEDIUM | Same objection as efficiency: description, not derivation. |
| **Affect-as-information** (Schwarz/Clore, via Schrauf) | Negative affect → systematic detailed processing → finer labels; positive → heuristic | NO | YES | No | LOW-MEDIUM | Processing-side; predicts nothing about frequency. |
| **Freyer et al. 2026 formal account** | *Personality and Social Psychology Review*, "Valence Asymmetry in Cognition — A Formal Account" (preprint 10.31234/osf.io/qz2rt). Formalizes and **contrasts** the intrapsychic/phylogenetic vs. ecological/ontogenetic perspectives with an explicit parameter set; relabels the effect *valence-driven* vs. *distinctiveness-driven*; flags that some explanations rest on "implicit yet critical assumptions such as the probability of having contact with stimuli" | — | — | Explicitly a *framework for testing*, not a unification | **HIGH as a competitor for the formalization slot** | Note what it names: **contact probability** as the hidden assumption. Our valve's "building needs contact" is the same variable arriving from the other side. If we formalize, we are formalizing into a space that was mapped in 2026 and we must cite it. |

### The single most useful sentence in the incumbent literature

Rozin, Berman & Royzman 2010, Discussion, verbatim:

> *"The frequency account is not at all adequate to account for the negative bias in nouns.
> An inverse frequency account would hold that because certain negative events (e.g.,
> murder) are rare, we are more inclined to have a word to designate the event. But this
> account will not work for the negative bias we describe for all five nouns: for example,
> while murder is rare, so is saving a life; and sympathy is at least as common as the
> shared joy of another person."*

**The incumbent's own verdict is that its unification fails.** Rozin needs two mechanisms
(world-frequency + efficiency for A; response-option count and "greater significance" for B)
and cannot get one. That is the honest shape of the niche: not empty, but with a hole the
incumbents have marked themselves.

### A rival result our reading must survive, not cite

**Jackson, Lindquist, Drabble, Atkinson & Watts 2022**, "Valence-dependent mutation in
lexical evolution", *Nature Human Behaviour* (PMID 36443501). Cognate replacement rates for
200 concepts on an Indo-European tree spanning 6–10 millennia: **negative valence correlates
with faster cognate replacement**, holding when frequency of use is controlled. Most robust
for **adjectives** (dirty/clean, bad/good); does not consistently reach significance for
verbs; **never** for nouns. Behavioural experiments show individuals are more likely to
replace words for negative concepts. Mechanism offered: micro-level guided variation driving
macro-level mutation (a euphemism-treadmill-shaped account).

Why this matters to us both ways:
- **It reads as a maintenance signature.** The positive lexicon is the stable one; the
  negative lexicon turns over. That is `rent_holds` vs. `unpaid_decays` in a 10,000-year
  substrate, with frequency controlled — which kills the obvious confound.
- **But it is a residual, and rule 6 forbids counting it as support.** It was measured before
  our reading existed and explained by an unrelated mechanism. If we want it, we must stake a
  *forward* prediction it does not already make — e.g. that replacement rate tracks a
  maintenance covariate independent of valence, or that the part-of-speech profile
  (adjectives yes, nouns never) is forced rather than incidental. The noun null is awkward
  for us: Rozin's Face B is carried *by nouns*, and Jackson's dynamics effect is *absent* in
  nouns. Any unification owes an account of that dissociation.

### A finding that cuts against a naive form of our reading

Polysemy is *not* aligned the way "positive = coarse" would want. The literature reports
that **negative words are more polysemous than positive words, and relatively neutral words
more polysemous than evaluatively extreme words** (line traced to "Some hypotheses concerning
the evolution of polysemous words", *J. Psycholinguistic Research*; SECONDARY, primary not
obtained). Meanwhile Zipf's meaning-frequency law says frequent words carry more senses. So
if positive words are more frequent, the meaning-frequency law predicts them to be *more*
polysemous, and the valence-polysemy literature says they are *less*. **Do not operationalize
"coarse" as polysemy.** Type-count per valence band and within-band embedding dispersion are
the safe operationalizations; senses-per-word is a trap that lands on the wrong side of two
different laws at once.

---

## 3. MECHANISM SEARCH — VERDICT

**Has anyone derived or linked the frequency-vs-differentiation split to a
maintenance/thermodynamic/entropy asymmetry? NO. Not one paper found.**

Searched combinations, all negative for the specific link:
- "Anna Karenina principle" + language / lexicon / entropy → the principle is applied to
  science success (Grinchenko/Bornmann arXiv:1104.0807), ecology, patient-experience NLP
  sentiment; **not** to lexical valence structure. The nearest is Alves's Tolstoy framing of
  the *similarity* asymmetry, which is the diversity face only.
- "negativity bias" + thermodynamics / entropy / free energy → nothing. Evolutionary
  threat-asymmetry accounts dominate; the free-energy/allostasis literature (Friston, Barrett)
  touches maintenance but never valence *lexicon* structure. "Natural Language Syntax Complies
  with the Free-Energy Principle" (arXiv:2210.15098) is syntax, not valence.
- "Pollyanna" + information theory → **Garcia, Garas & Schweitzer 2012** is the only real
  hit, and it is information-theoretic, not thermodynamic. Abstract verbatim: *"words with a
  positive emotional content are more frequently used… We also find that negative words
  contain more information than positive words, as the informativeness of a word increases
  uniformly with its valence decrease."* Three affective lexica, English/German/Spanish.
  **This is the closest published thing to "one quantity, both faces."**
- markedness + information theory → Horn's division of pragmatic labour and the classic
  result that only one of two subcontraries lexicalises, always the positive value (no *nall,
  *nand, *nalways). Elegant, and it is a *communicative*-economy account, not a maintenance one.
- Frijda / hedonic asymmetry → the closest *conceptual* antecedent, unbridged (see table).
- Breithaupt → *The Narrative Brain* (Yale UP) and the large retelling experiments: retellings
  preserve a story's degree of happiness/sadness as an "anchor of stability" even as coherence
  degrades. Adjacent and interesting (emotional content is the maintained invariant under
  transmission) but not a valence-asymmetry mechanism.

**Nearest misses, ranked:**
1. **Frijda's law of hedonic asymmetry (1988).** Semantically nearest. "Pleasure is contingent
   upon change and disappears with continuous satisfaction" is the rent clause for affect.
   Missing: any connection to lexicon.
2. **Garcia et al. 2012.** Structurally nearest. One measured quantity spanning both faces.
   Missing: a generative principle, and its formula application is disputed by Dodds et al.
3. **Alves/Koch/Unkelbach bounded range.** Mechanistically nearest for face B, and already
   Anna-Karenina in substance. Missing: face A, which its geometry arguably predicts backwards.
4. **Freyer et al. 2026.** Nearest in *form* — it is the formalization move, made this year,
   and it independently identifies contact probability as a load-bearing hidden assumption.

**What this means for the stance.** The claim "the ledger reading unifies the two faces" is
**not clear ground**. The two faces are already paired (EvIE), the AK mechanism is already
published (Alves), and the one-quantity version already exists (Garcia 2012). What is
genuinely unclaimed is a *derivation* — one asymmetry (free decay / paid upkeep /
contact-gated building) from which both faces follow with a **joint quantitative constraint**,
plus a **dissociation kill**. Absent that constraint, the contribution reduces to renaming
Rozin's two mechanisms with our vocabulary, which is not a contribution. Compare
`unconditional-statement-failure`: substance would survive, warrant would fail.

---

## 4. DATASET INVENTORY (for a future test)

**Gate reminder (note §3): never test on a lexicon whose valence was assigned BY TRANSLATION
from English.** Marked below. Verification column says whether I confirmed provenance from a
primary/publisher source in this sweep or am relaying a secondary description.

### English
| Resource | Size | Provenance | Verified | Notes |
|---|---|---|---|---|
| Warriner, Kuperman & Brysbaert 2013 | **13,915** lemmas, VAD, 1–9 | Native English, crowdsourced; ~11,826 lemmas drawn from movie-subtitle corpus | YES (primary + Dodds reply) | 14–20 raters/word (fewer than labMT's 50). Lemmas, not tokens — a mismatch with token-frequency lists that Dodds explicitly flags. |
| NRC VAD Lexicon **v2** (Mohammad 2025, arXiv:2503.23547) | **55,133** entries = 44,928 unigrams + 10,205 MWEs | Native English human ratings | YES | Largest English VAD resource. Free for research. |
| labMT (Dodds et al. 2015), English slice | ~10,222 words | Native, 50 raters/word, 9-pt emoticon scale | YES | **Instrument caveat:** the emoticon scale is the object of Garcia's bias charge. |
| ANEW (Bradley & Lang) | 1,034 words | Native English | SECONDARY | Small; the ancestor of most translated sets. |
| LIWC function-word list | 399–450 matched | expert-constructed | YES | **Not neutral** — Dodds shows "greatest" 7.26 / "worst" 2.10. Do not use as a neutrality control. |

### Multilingual, NATIVE-RATED (usable)
| Language | Resource | Size | Verified |
|---|---|---|---|
| 10 languages (en, es, fr, de, pt-BR, ko, zh, ru, id, ar) | **labMT / Dodds et al. 2015** | ~10,000 words each, 50 native raters/word | YES — PNAS states native speakers, region-restricted |
| Spanish | **Stadthagen-González et al. 2016/17**, "Norms of valence and arousal for 14,031 Spanish words", *Behav Res* | **14,031**, valence+arousal | YES (publisher record) — native-generated, not an ANEW translation |
| German | BAWL-R (Võ et al. 2009) | ~2,900 | SECONDARY |
| Dutch | Moors et al. 2013 | **4,300**, VAD + AoA | SECONDARY |
| Polish | Imbir, ANPW_R 2016 (*Front. Psychol.*) | **4,900**, VAD + origin/significance/concreteness/imageability/AoA | SECONDARY; ANPW 2015 predecessor = 1,586 |
| Chinese (simplified) | Valence+arousal for **11,310** simplified Chinese words, *Behav Res* 2021 | 11,310 | SECONDARY |
| Chinese | ANCW (2023, *Behav Res*) | 4,030 | SECONDARY |
| French | Monnier & Syssau 2014 | — | SECONDARY |
| Croatian | Ćoso et al. 2019 | — | SECONDARY |
| Indonesian | Sianipar et al. 2016 | — | SECONDARY |
| Turkish | Torkamani-Azar et al. 2019 | — | SECONDARY |
| Greek | Vaiouli, Panteli & Panayiotou 2021 | — | SECONDARY |

### FLAGGED — translation-derived, UNUSABLE for the gate as primary evidence
| Resource | Why |
|---|---|
| Redondo et al. 2007 (Spanish) | Spanish **translation equivalents** of ANEW's 1,034 items. Use Stadthagen-González instead. |
| Montefinese et al. 2014 (Italian) | ANEW adaptation |
| Soares et al. 2012 (European Portuguese) | ANEW adaptation |
| "Mexican Spanish adaptation for ANEW" (*Behav Res* 2025) | adaptation by name |
| Buechel et al. 2020, "Learning and Evaluating Emotion Lexicons for 91 Languages" | **Machine-derived**, not human-rated. Coverage is seductive; provenance disqualifies it for a gate that turns on native judgment. |
| NRC translated emotion lexicons | machine-translated from English |

**Provenance is not binary — a third category matters.** "Adaptation" papers often *re-rate*
the translated items with native speakers. That is not the same as a native-*generated* item
set: the item list still inherits English lexicalisation, which is precisely the variable
Face B is about. For a differentiation test, a re-rated translation is **still unusable**,
because the type-count is the measurement and the type-list came from English. For a
*frequency* test, a re-rated translation is merely weak. State which of the two you are
running before you pick a lexicon.

### Frequency lists
| Resource | Coverage | License | Notes |
|---|---|---|---|
| SUBTLEX family (Brysbaert et al., crr.ugent.be) | US, UK, NL, DE, CH, ESP, PL, PT, GR, IT | redistributable with credit | SUBTLEX-US: ~74,286 letter-strings from ~30M words / 8,388 films and episodes (SECONDARY figure) |
| OPUS **OpenSubtitles 2018** | 60+ languages | attribution to OpenSubtitles | Packaged in `wordfreq` (rspeer) alongside SUBTLEX |
| Hermit Dave OpenSubtitles lists | 61 frequency lists | CC | convenient, lower provenance |
| Google Books Ngrams | many | free | the corpus Garcia et al. used for the log-f refit |
| Leech, Rayson & Wilson (BNC-derived) | British English, 100M words | — | Rozin's source; **reporting floor at 10/million** — anything rarer reads as 0 |

**A dependency to disclose, not discover later.** Warriner's lemma list is drawn from
subtitles, and SUBTLEX is a subtitle corpus. Pairing them is *not* two independent
instruments for gate 4 (≥2 corpora × ≥2 lexicons). Cross the register: pair a subtitle-sourced
lexicon with a books/news frequency list and vice versa, and report the crossing explicitly.

### Zipfian handling (note gate 2)
- Rank statistics, not means on raw frequencies.
- **Disclose the tied fraction** — corpora with reporting floors (Leech et al.'s 10/million)
  manufacture massive ties at the bottom, exactly where the rare negative types live. This is
  the same shape as `share-null-is-chi2-shaped` and our disclosure rule 4.
- Pre-register rank-vs-log-f regression form. Report both. Garcia/Dodds is the cautionary case.

---

## 5. THE COST QUESTION — destruction vs. neglect

Our model's staked question: does targeted unbuilding cost more than letting decay run?
("hate is paid, neutrality is free").

**Information-theoretic / thermodynamic — the strongest formal support.**
- **Landauer**: erasing a bit has a minimum thermodynamic cost (kT ln 2). Relaxation toward
  equilibrium requires no work. This is the formal statement of the staked asymmetry:
  *going to equilibrium is free; putting a system into a specified state is paid.*
- **Weak vs. strong erasure** (Norton and successors; "The Simply Uninformed Thermodynamics of
  Erasure", *Philosophy of Physics* / arXiv:2502.18231): phase-space analysis recovers **no
  minimum entropy cost for weak erasure** and a **positive minimum for strong erasure**. This
  is a sharper distinction than Landauer alone and it maps cleanly onto our poles —
  *randomize* (cheap, ≈ neutrality) vs. *drive to a specified target* (paid, ≈ hate).
- Refinements worth knowing: the dominant entropy cost at molecular scale is suppressing
  thermal fluctuation (noise), not the logical operation; dissipated heat at fixed erasure
  fidelity is controlled by the overlap of the initial state with the slowest relaxation mode.
  The second is directly analogous to our maintained-holonomy result — **cost depends on the
  structure you are acting against, not on the act alone.**
- **Anti-support to keep honest:** "Information erasure without an energy cost" and
  Maxwell's-demon reanalyses ("foiled by the entropy cost of measurement, not erasure")
  show the Landauer bound is neither unconditional nor uncontested. Do not cite Landauer as
  settled physics in support of a values claim.

**The sharpest form of the model's own answer, from our own record.** Our maintained-holonomy
campaign found that a repair holds a structure's identity **only if it knows the design**
(fidelity 0.9909 flat vs. power-law collapse to chance) — see `holonomy-is-maintainable`,
`gain-plateau-is-not-maintenance`. The dual is immediate and testable: **targeted unbuilding
must also know the design.** Undirected noise merely randomizes (cheap, and it is exactly
neutrality); destroying a *specific* pattern requires paying for the information that
identifies it. **That gives "hate is paid" a mechanism rather than a metaphor, and it is
symmetric with a result we already own.** This is the most promising formal handle found in
the sweep and it needs no new physics.

**Biological / ecological.**
- Jones et al. 2018, "Restoration and repair of Earth's damaged ecosystems", *Proc. R. Soc. B*
  285:20172577 — meta-analysis: **active restoration did not produce faster or more complete
  recovery than simply ending the disturbance**; recovery rates slow with time since
  disturbance ended. Read carefully, this is *awkward* for the "building needs contact" leg:
  the contact-gated intervention did not beat passive recovery. It is a datum about
  *rebuilding*, not destroying, but the valve claim should not be advertised as if ecology
  supports it.

**Organizational / political — names the distinction, does not price it.**
- The policy literature cleanly separates **active dismantling** ("deliberate, rapid, and
  highly visible rollback driven by political choice rather than fiscal necessity"; mechanisms:
  staff elimination, regulatory degradation, disarticulation of inter-institutional
  coordination) from **policy drift/decay** (policies designed for today fitting tomorrow only
  imperfectly). See the *Policy and Society* 2026 pieces on termination and dismantling and
  "Dismantling Policies and Eroding Administrative Capacities" (Penn State, 2026).
- This is our three poles under other names — dismantling (−), drift (0), maintenance (+) —
  but the literature is descriptive/typological. **No cost comparison between deliberate
  dismantling and drift was found.** If someone has priced it, this sweep did not find them.

**Overall verdict on the cost question: OPEN, with one strong formal handle.** The
weak-vs-strong erasure distinction plus our own design-knowing-repair result give a
principled, already-half-owned route to "targeted unbuilding is paid, neglect is free."
Nothing in the organizational or biological literature prices it. Nothing in the psychology
of valence has asked the question at all.

---

## 6. WHAT A PREREG WOULD HAVE TO DO (consequences of this sweep)

1. **Drop or re-source Boucher & Osgood on the differentiation leg.** They claim positive
   diversity. Verify the primary or cite them for frequency only. (§1a)
2. **Cite Frijda as antecedent, not as discovery.** The hedonic-asymmetry law is our rent
   clause for affect, published 1988.
3. **Cite Unkelbach's EvIE as the incumbent that already pairs both faces**, and Alves's
   bounded-range as the incumbent Anna-Karenina mechanism. Claiming an open niche over these
   would be false.
4. **Engage Garcia et al. 2012 head-on.** It is the existing one-quantity account. Our reading
   must either subsume it or predict where it fails.
5. **Cite Freyer et al. 2026.** The formalization slot was occupied this year, and it
   independently names contact probability — our valve's variable.
6. **The contribution must be a joint constraint plus a dissociation kill,** not a re-labelling.
   The kill the note already gestures at (the two biases dissociating where the ledger says
   they must co-occur) is the right shape; it needs a number and a pre-registered band.
   Nothing here is support until a forward prediction confirms (rule 6).
7. **Do not operationalize "coarse" as polysemy.** (§2, final subsection)
8. **Rozin's numbers cannot carry a ratio stake** — N=1 per language, non-independent
   languages, English-generated stimuli. Build the instrument. (§1b)
9. **Owed to Jackson et al. 2022:** an account of why the valence-mutation effect is carried by
   adjectives and absent in nouns, when Face B is carried by nouns.

---

## 7. SOURCES

- Boucher & Osgood 1969, *J. Verbal Learning & Verbal Behavior* 8(1):1–8 — https://www.sciencedirect.com/science/article/abs/pii/S0022537169800022 (primary paywalled; claim relayed SECONDARY)
- Dodds et al. 2015, *PNAS* 112(8):2389–2394 — https://pmc.ncbi.nlm.nih.gov/articles/PMC4345622/
- Garcia, Garas & Schweitzer 2015, *PNAS* 112(23):E2983 — https://www.sg.ethz.ch/publications/2015/garcia2015the-language-dependent-relationship/PNAS-2015-Garcia-E2983.pdf
- Dodds et al. 2015 reply — https://arxiv.org/pdf/1505.06750
- Garcia, Garas & Schweitzer 2012, *EPJ Data Science* 1:3 — https://arxiv.org/abs/1110.4123
- Rozin, Berman & Royzman 2010, *Cognition & Emotion* 24(3):536–548 — https://bpb-us-w2.wpmucdn.com/web.sas.upenn.edu/dist/7/206/files/2016/09/PositiveWordBiasesCE2010-1sug059.pdf
- Unkelbach et al. 2019, *European Review of Social Psychology* 30(1) — https://www.tandfonline.com/doi/abs/10.1080/10463283.2019.1688474
- Unkelbach, Alves & Koch 2020, *Adv. Exp. Soc. Psych.* — https://www.sciencedirect.com/science/chapter/bookseries/abs/pii/S0065260120300150
- Koch, Alves, Krüger & Unkelbach 2016, *JEP:LMC* — https://www.apa.org/pubs/journals/features/xlm-xlm0000243.pdf
- Alves, Koch & Unkelbach 2017, *Trends in Cognitive Sciences* — https://www.sciencedirect.com/science/article/abs/pii/S1364661316302054
- Alves et al. 2023, *J. Happiness Studies* — https://link.springer.com/article/10.1007/s10902-023-00631-9
- Freyer, Unkelbach, Wiedenroth, Alves, Knischewski & Leising 2026, *PSPR* — https://journals.sagepub.com/doi/10.1177/10888683251407820 ; preprint https://osf.io/preprints/psyarxiv/qz2rt
- Weitzel & Unkelbach 2026, *EJSP* — https://onlinelibrary.wiley.com/doi/full/10.1002/ejsp.70070 (paywalled here)
- Jackson, Lindquist, Drabble, Atkinson & Watts 2022, *Nature Human Behaviour* — https://pubmed.ncbi.nlm.nih.gov/36443501/ ; PDF https://static1.squarespace.com/static/5d8c8bd71a675f210c9996e6/t/6386272cecbe7753b19fee69/1669736240811/s41562-022-01483-8.pdf
- Frijda 1988, "The Laws of Emotion" — https://www.academia.edu/6827184/The_Laws_of_Emotion ; https://en.wikipedia.org/wiki/Hedonic_asymmetry
- Schrauf & Sánchez 2004, *JMMD* — https://eric.ed.gov/?id=EJ885202
- Averill, *A Semantic Atlas of Emotional Concepts* (1975); "On the Paucity of Positive Emotions" — https://link.springer.com/chapter/10.1007/978-1-4684-3782-9_2 (paywalled; counts NOT verified)
- Horn, negation & markedness — https://plato.stanford.edu/entries/negation/ ; https://saltconf.github.io/salt33/materials/horn.pdf
- Piantadosi, Tily & Gibson 2011, *PNAS* — https://www.pnas.org/doi/10.1073/pnas.1012551108
- Warriner, Kuperman & Brysbaert 2013 — https://link.springer.com/article/10.3758/s13428-012-0314-x
- NRC VAD v2 — https://arxiv.org/abs/2503.23547
- Stadthagen-González et al., 14,031 Spanish words — https://link.springer.com/article/10.3758/s13428-015-0700-2
- Imbir, ANPW_R — https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2016.01081/full
- Valence/arousal, 11,310 Chinese words — https://link.springer.com/article/10.3758/s13428-021-01607-4
- SUBTLEX — http://crr.ugent.be/programs-data/subtitle-frequencies ; wordfreq — https://github.com/rspeer/wordfreq
- Jones et al. 2018, *Proc. R. Soc. B* 285:20172577 — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5832705/
- Erasure thermodynamics — https://arxiv.org/pdf/2502.18231 ; https://philosophyofphysics.lse.ac.uk/articles/10.31389/pop.154
- Breithaupt, *The Narrative Brain* — https://yalebooks.yale.edu/book/9780300273809/the-narrative-brain/
- Policy dismantling vs. decay — https://academic.oup.com/policyandsociety/advance-article/doi/10.1093/polsoc/puag006/8527840
