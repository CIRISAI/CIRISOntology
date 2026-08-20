# T5-ATTEST — blocking pre-freeze tasks B1 and B2

**Discharges** `RECOGNITION_PREREG_A2.md` §A2.7 tasks **B1** (T5-ATTEST) and **B2** (row 1 value
inventories).
**Governed by** [D] §T5.2 (sample frame), §T5.3 (frozen table), §T5.4 (attestation requirement,
VOID-bearing), §T5.9 (bands); [A2] BLOCKER-7, BLOCKER-8, MAJOR-11, MAJOR-12, MAJOR-13, MINOR-7,
MINOR-8.

**Written 2026-08-20, before freeze, before any mapper ran.** No existing file was modified; no
git operation was performed.

---

## 0. Headline, stated first because it changes the freeze

**B1: 23 of 40 instances attest on their own named frame. 6 more attest only through a source the
frozen table does not name. 11 are DROPPED.** Ten of the eleven drops are substantive — the
primary source either has **no datapoint** for the named language, or **codes it against** the
row's own obligatory-marking selection criterion. The eleventh is row 10, dropped by its own
pre-flag exactly as predicted.

**Row 5 (alienable/inalienable possession) loses all three instances and the row dies.**

**The surviving denominator does not reach [D] §T5.9's `VOID — family` threshold on the named
frames alone.** Counting a category as surviving when it retains **≥2** instances (the reading
MAJOR-13's own row-14 rule licenses — *"row 14 runs on two languages and is marked as such"*),
`N = 9` on named frames, against a threshold of **10**. Admitting the six substitute sources
takes `N = 11` and the gate passes. **Whether T5 can run at all therefore now turns on a single
decision the orchestrator has to make: are the six substitutes admitted by amendment, or not?**
That decision is flagged, not taken here — see §2.3.

**B2: the provisional 5 / 3 / 2 = 10 pairs is CONFIRMED as data**, with all ten values named and
page-cited. Two discrepancies ride along: the registration's Turkish morpheme pair **`-mIş/-DIr`
is wrong** (it is `-mIş`/**`-DI`**, confirmed at three independent primaries), and **Cuzco Quechua
evidentials are *not obligatory*** on the designated primary's own testimony, which strikes at
row 1's selection criterion.

---

## 1. Method, and what "verified at the primary" means here

Everything below was fetched, not recalled. Three routes were used and are distinguished
throughout:

1. **WALS Online, live at `wals.info`.** Every coded value was read from the live datapoint page
   `https://wals.info/valuesets/{feature}-{walscode}`, which prints the feature, the chapter
   author, the value, the source references, and any glossed examples. Absences were confirmed by
   an HTTP **404** on that URL, not by silence in a mirror.
2. **The WALS CLDF release** (`cldf-datasets/wals`, `values.csv` 76,475 rows / `languages.csv`
   3,573 / `codes.csv` / `parameters.csv`) was pulled in bulk to enumerate *what else* is coded —
   which is how the replacement candidates in §2.4 were found. Every value quoted from it was then
   re-read live per (1). The mirror and the live site agreed in every case checked.
3. **Named survey literature**, reached at publisher-deposited metadata (Crossref, jbe-platform),
   author-hosted full text, or public-domain text. Where only page-level presence could be
   established and not the content of the claim, the row says so.

**Chapter-number check (the "received numbers are not measured numbers" gate).** All ten WALS
chapter numbers in the frozen table resolve, and their titles match the frozen table exactly:

| ch. | title as coded in WALS | frozen table agrees |
|---|---|---|
| 37A | Definite Articles | yes |
| 39A | Inclusive/Exclusive Distinction in Independent Pronouns | yes |
| 45A | Politeness Distinctions in Pronouns | yes |
| 55A | Numeral Classifiers | yes |
| 58A | Obligatory Possessive Inflection | yes |
| 59A | Possessive Classification | yes |
| 65A | Perfective/Imperfective Aspect | yes |
| 73A | The Optative | yes |
| 77A | Semantic Distinctions of Evidentiality | yes |
| 78A | Coding of Evidentiality | yes |

BLOCKER-7's parenthetical gloss of WALS 77A — *"a three-way presence/type contrast: no
grammatical evidentials / only indirect / both direct and indirect"* — is **verified exactly**
against 77A's coded value set.

**Frame classes used in the table below:**

- **WALS-primary** — a live WALS datapoint exists for this language on this feature.
- **survey-secondary** — no WALS chapter covers the category, or WALS has no datapoint for this
  language; the instance is attested at the survey source **named in the frozen table**.
  Disclosed per [D] §T5.2 as carrying a weaker independence guarantee.
- **SUBSTITUTE-REQUIRED** — the language is attested at a real primary, but **not at the source
  the frozen table names**. Admitting it requires a numbered amendment to the frame column. It is
  *not* counted as attested in the named-frame totals.
- **DROPPED** — VOID by [D] §T5.4.

---

## 2. B1 — THE ATTESTATION TABLE

One row per (category × language) instance. 40 instances (13 rows × 3 languages, plus row 10's
single named language).

### 2.1 Attested instances

| # | row / category | language | citation / datapoint verified at the primary | coded value or attested content | frame class |
|---|---|---|---|---|---|
| 1 | 1 Evidentiality | **Tuyuca** [tuy] | WALS **77A-tuy**, de Haan; refs **Barnes 1984**. Datapoint page carries two glossed examples (igt-1847 `mũtúru bɨsɨ-tɨ` 'The motor roared' (I heard it); igt-1848 `páaga punĩ-ga` 'My stomach hurts' (I feel it)). WALS ch. 77 body cites **Barnes 1984: 260** for the non-visual. | **Direct and indirect** | WALS-primary |
| 2 | 1 Evidentiality | **Tuyuca** [tuy] | WALS **78A-tuy**, de Haan; refs Barnes 1984 | **Part of the tense system** | WALS-primary |
| 3 | 1 Evidentiality | **Cuzco Quechua** [qcu] | **no WALS datapoint** (77A-qcu and 78A-qcu both 404). Attested at **Faller 2002: 14** (Stanford PhD, fetched in full from the author's own university page): the three focus enclitics *"the Direct -mi (allomorph -n), the Reportative -si (allomorph -s or -sis for some speakers in Cuzco), and the Conjectural -cha"* | three evidential enclitics; see §3.2 | **survey-secondary** (MAJOR-13's row-1 rule FIRED — see §4.1) |
| 4 | 1 Evidentiality | **Turkish** [tur] | WALS **77A-tur**, de Haan; refs **Aksu-Koç & Slobin 1986**. WALS ch. 77 ex. (8): `Ahmet gel-di` (witnessed) vs `Ahmet gel-miş` (unwitnessed) | **Direct and indirect** | WALS-primary |
| 5 | 1 Evidentiality | **Turkish** [tur] | WALS **78A-tur**; ch. 78 ex. (4), same morpheme pair | **Part of the tense system** | WALS-primary |
| 6 | 2 Perfective/imperfective | **Russian** [rus] | WALS **65A-rus**, Dahl & Velupillai; refs **Dahl 1985: 172** | **Grammatical marking** | WALS-primary |
| 7 | 2 Perfective/imperfective | **Mandarin** [mnd] | WALS **65A-mnd**, Dahl & Velupillai; refs **Dahl 1985: 180** | **Grammatical marking** | WALS-primary |
| 8 | 3 Optative | **Georgian** [geo] | WALS **73A-geo**, Dobrushina, van der Auwera & Goussev; refs **Hewitt 1995: 572**. Datapoint carries glossed example igt-1576 (`…mo-g-šl-od-e-t…` opt) | **Inflectional optative present** | WALS-primary |
| 9 | 3 Optative | **Ancient Greek** | **not a WALS language** (WALS codes only Greek (Modern), Cypriot, Greek Sign Language). Attested at **Smyth 1920, *A Greek Grammar for Colleges*, §1814 "Optative of Wish"**, read at Perseus: *"In independent sentences the optative without ἄν is used to express a wish referring to the future (negative μή)"*, with the named published example **Sophocles, *Ajax* 550** `ὦ παῖ, γένοιο πατρὸς εὐτυχέστερος` | inflectional optative present, wish use | **survey-secondary** (MAJOR-13's row-3 rule FIRED — see §4.2) |
| 10 | 4 Middle voice | **Classical Greek** | **Kemmer 1993**, Appendix B "Data Sources" **p. 271**: *"Greek, Classical: Smyth (1920), Wright (1912)"*; Index of Languages p. 297 lists ~20 loci. Example **p. 57, Table 6**: `péte-sthai` 'fly'. Inflectional middle described **p. 249** (`-mai` 1sg pres. middle ending) | middle voice present, inflectional MM | survey-secondary |
| 11 | 4 Middle voice | **Fula** | **Kemmer 1993**, App. B **p. 271**: *"Fula, Gombe dialect: Arnott (1970). Niger-Congo, West Atlantic"*; Index p. 297 (13 loci). Example **p. 26**: MM `-o`, RM `-(i)t-o`, `ndaar-t-o` 'look at oneself'; classified **two-form, "Dutch type"**. Corroborated in Kemmer's own source, **Arnott 1970: 179** (*"15 Active tenses, 14 Middle, and 13 Passive tenses"*) and **p. 189** (M-only radicals) | middle voice present, obligatory three-voice inflection | survey-secondary |
| 12 | 6 Inclusive/exclusive | **Tagalog** [tag] | WALS **39A-tag**, Cysouw; refs **Schachter & Otanes 1972: 88** | **Inclusive/exclusive** | WALS-primary |
| 13 | 7 Numeral classifiers | **Mandarin** [mnd] | WALS **55A-mnd**, Gil. ⚠ **datapoint carries NO source reference** | **Obligatory** | WALS-primary (weak — see §4.7) |
| 14 | 7 Numeral classifiers | **Japanese** [jpn] | WALS **55A-jpn**, Gil. ⚠ **datapoint carries NO source reference** | **Obligatory** | WALS-primary (weak — see §4.7) |
| 15 | 7 Numeral classifiers | **Yucatec** [yct] | WALS **55A-yct**, Gil; refs **Suárez 1983b: 88** | **Obligatory** | WALS-primary |
| 16 | 8 Egophoricity | **Kathmandu Newar** | **Hargreaves, David. "'Am I blue?': Privileged access constraints in Kathmandu Newar." Ch. 2, pp. 79–107** of Floyd, Norcliffe & San Roque (eds.) 2018, *Egophoricity* (TSL 118), DOI 10.1075/tsl.118.02har. TOC verified independently twice (jbe-platform chapter list; Crossref deposit) | conjunct/disjunct egophoric marking | survey-secondary |
| 17 | 11 Honorifics / social deixis | **Japanese** [jpn] | WALS **45A-jpn**, Helmbrecht; refs **Hinds 1986: 238–265**; datapoint carries an extensive Notes field enumerating `anata`, `anta`, `kimi`, `kisama`, `omae`, `o-taku` | **Pronouns avoided for politeness** | WALS-primary |
| 18 | 11 Honorifics / social deixis | **Korean** [kor] | WALS **45A-kor**, Helmbrecht; refs **Sohn 1999: 207f, 251f, 407–413**; Notes field enumerates `caki`, `caney`, `elusin`, `kutay`, `ne`, `tangsin`, `tayk` | **Pronouns avoided for politeness** | WALS-primary |
| 19 | 12 Mirativity | **Turkish** | **DeLancey 1997: 38**, morpheme **`-mIş`**; the flagship example `kız-ınız çok iyi piyano çal-iyor-muş` 'Your daughter plays piano very well!' (DeLancey 1997: 38, after Slobin & Aksu-Koç 1982: 197). Independently corroborated at **Faller 2002: 41 n. 2**: *"The suffix -mIş also has a mirative use"* | mirative use of `-mIş` | survey-secondary |
| 20 | 12 Mirativity | **Hare** | **DeLancey 1997: 38–40**, suffix **`-lõ`**; examples `júhye sa k'ínayeda lõ` 'I see there was a bear walking around here' (1997: 38), inference reading (1997: 39), compliment `deshı̃ta yedaníyie lõ` (1997: 40). Corroborated by DeLancey's own 2012 abstract, which names Hare (Athabaskan) as the exemplifying language | mirative `-lõ` | survey-secondary |
| 21 | 13 Associated motion | **Arrernte** | **Koch, Harold. "Associated motion in the Pama-Nyungan languages of Australia." Ch. 7, pp. 231–324** of Guillaume & Koch (eds.) 2021, *Associated Motion* (EALT 64). In-volume hits for "Arrernte"/"Mparntwe Arrernte"/"Arandic" at pp. 254, 257–268, 311–313, 324 — inside ch. 7. The volume's own Introduction states Koch compares Kaytetye with *"other Arandic languages, which… have played an important role in early studies of AM (Wilkins 1989, 1991)"* | associated motion present | survey-secondary |
| 22 | 13 Associated motion | **Cavineña** | Guillaume & Koch 2021, **Introduction p. 4, example (1)** — the volume's opening illustration of the category, citing Guillaume 2006/2008/2009, listing `ba-ti-` 'go and see O', `ba-na-` 'come and see O', `ba-aje-` 'see O while going', `ba-be-`, `ba-kena-`, `ba-dadi-`, `ba-tsa-`. Full 12-suffix paradigm at **Guillaume 2016: 88, Table 1** (open access, fetched in full); grammar locus **Guillaume 2008: 212–236** | associated motion, 12-suffix paradigm | survey-secondary |
| 23 | 13 Associated motion | **Cupeño** | Guillaume & Koch 2021, **Dryer ch. 13 "Associated motion in North America", pp. 485–526**; in-volume hits for "Cupeño" at pp. 492, 502, 505, 506, 516, and Dryer's reference list at p. 525 cites Hill's *A Grammar of Cupeño* | ⚠ **presence in the chapter verified; what Dryer SAYS about Cupeño is UNVERIFIED** (no snippet text available for this volume) | survey-secondary (**weak** — see §4.8) |
| 24 | 14 Definiteness | **Arabic (Modern Standard)** [ams] | WALS **37A-ams**, Dryer; refs **Cowan 1958: 9**. All **seven** Arabic varieties coded in 37A read the same value, so the instance is robust to which variety is pinned | **Definite affix** | WALS-primary |
| 25 | 14 Definiteness | **Hungarian** [hun] | WALS **37A-hun**, Dryer; refs **Kenesei et al. 1998: 94**, **Benkő & Imre 1972: 89–90** | **Definite word distinct from demonstrative** | WALS-primary |

Rows 1–5 above are the five WALS datapoints belonging to row 1's **three** language instances
(Tuyuca and Turkish each carry both a 77A and a 78A datapoint; Cuzco Quechua carries neither).

**Counting instances, not datapoints: 23 attested on their named frames** — 13 WALS-primary
(instances 1/2, 4/5, 6, 7, 8, 12, 13, 14, 15, 17, 18, 24, 25 → Tuyuca, Turkish, Russian, Mandarin-65A,
Georgian, Tagalog, Mandarin-55A, Japanese-55A, Yucatec, Japanese-45A, Korean, Arabic, Hungarian)
and 10 survey-secondary (Cuzco Quechua, Ancient Greek, Classical Greek, Fula, Kathmandu Newar,
Turkish-mirative, Hare, Arrernte, Cavineña, Cupeño).

### 2.2 Instances attested only through a source the frozen table does not name

These six are **real attestations at real primaries**, but the frozen frame column names a volume
that does not treat the language. Under [D] §T5.4 they are unfilled *as registered*; admitting
them is a frame amendment, not an author's fill-time choice.

| # | row | language | why the named frame fails | substitute verified at the primary |
|---|---|---|---|---|
| 26 | 8 Egophoricity | **Akhvakh** | **No chapter** in Floyd, Norcliffe & San Roque 2018. The 15-chapter TOC (verified twice, page ranges contiguous) has no Akhvakh chapter; Akhvakh is cited *inside* other chapters | **Creissels, Denis. 2008.** "Person variations in Akhvakh verb morphology: functional motivation and origin of an uncommon pattern." *STUF* **61(4): 309–325**, DOI 10.1524/stuf.2008.0027. Abstract fetched: the same endings encode 1st vs 2nd/3rd in declaratives and 2nd vs 1st/3rd in questions — the canonical egophoric alignment, restricted to the perfective positive |
| 27 | 8 Egophoricity | **Tsafiki** | **No chapter.** The volume's Barbacoan chapter is on the sister language **Cha'palaa** (Floyd, ch. 9, pp. 269–304). The Introduction's 154-item reference list contains no Dickinson/Tsafiki entry | **Dickinson, Connie. 2000.** "Mirativity in Tsafiki." *Studies in Language* **24(2): 379–422**, DOI 10.1075/sl.24.2.06dic; and **Dickinson 2002**, *Complex Predicates in Tsafiki*, PhD, Oregon. ⚠ bibliographic record verified; the content claim rests on this being the source two chapters of the volume cite for Tsafiki |
| 28 | 9 Switch-reference | **Amele** | **No chapter** in Haiman & Munro 1983. Verified independently by me at Crossref (20 deposited items, pp. i–337 contiguous): the Papuan chapters are Franklin on **Kewa** (39–50) and Longacre on **Wojokeso** (185–208) | **Roberts, John R. 1988.** "Amele switch-reference and the theory of grammar." *Linguistic Inquiry* **19(1): 45–63**; **Roberts 1987**, *Amele* (Croom Helm Descriptive Grammars) |
| 29 | 9 Switch-reference | **Choctaw** | **No chapter on Choctaw** in the 1983 volume. (Munro's own chapter, pp. 223–244, is the theoretical *"When 'same' is not 'not different'"*, and names no language in its title; whether Choctaw appears inside it is UNVERIFIED) | **Davies, William D. 1984.** "Choctaw Switch-Reference and Levels of Syntactic Representation." In *The Syntax of Native American Languages* (Syntax and Semantics 16), **pp. 123–147**, DOI 10.1163/9789004373129_006; **Broadwell 2006**, *A Choctaw Reference Grammar* |
| 30 | 9 Switch-reference | **Diyari** | **No chapter.** The volume's only Australian chapter is **Heath, "Referential tracking in Nunggubuyu", pp. 129–150** | **Austin, Peter. 1981.** "Switch-Reference in Australia." *Language* **57(2): 309–334**, DOI 10.2307/413693 (abstract fetched); **Austin 1981**, *A Grammar of Diyari, South Australia*, CUP |
| 31 | 12 Mirativity | **Magar** | **DeLancey 1997 does not treat Magar.** DeLancey's languages are Tibetan, Hare, Sunwar, Korean, Turkish, Kalasha — enumerated in Hill 2012: 413 (full text fetched), which places Magar in a separate, later bucket | **Grunow-Hårsta, Karen. 2007.** "Evidentiality and mirativity in Magar." *LTBA* **30(2): 151–194**, DOI 10.32655/ltba.30.2.06. ⚠ postdates DeLancey 1997; the specific Magar morphemes are UNVERIFIED |

### 2.3 DROPPED instances, with reasons

Eleven instances drop. **Ten are substantive failures**, not clerical gaps.

| # | row | language | reason | disposition rule |
|---|---|---|---|---|
| 32 | 2 Aspect | **Swahili** [swa] | WALS **65A-swa** = **"No grammatical marking"** (Dahl & Velupillai; refs Ashton 1947). The row selects for grammatically marked perfective/imperfective; the primary codes the language **against** it | [D] §T5.4 selection criterion |
| 33 | 3 Optative | **Turkish** [tur] | WALS **73A-tur** = **"Inflectional optative absent"** (Dobrushina, van der Auwera & Goussev; refs Lewis 1967, Kononov 1956). Verified live. The row's own declared frame codes Turkish as **lacking** the category | [D] §T5.4 selection criterion — **new, not anticipated by MAJOR-13** |
| 34 | 4 Middle voice | **Tamil** | **Not in Kemmer 1993.** "Tamil" occurs once in the volume, as the *subgroup label* for Kannada in App. B p. 271 (*"Dravidian, Tamil-Kannada"*). Independently, Asher 1982 (*Tamil*) and Schiffman 1999 (*Spoken Tamil*) return **0 hits** for "middle voice"; both call `koḷ`/`-koo` a **reflexive/self-benefactive auxiliary**, not a voice | [D] §T5.4 attestation requirement |
| 35 | 5 Possession | **Hawaiian** [haw] | **No WALS datapoint** in 58A or 59A (both 404) | [D] §T5.4 attestation requirement |
| 36 | 5 Possession | **Navajo** [nav] | **No WALS datapoint** in 58A or 59A (both 404) | [D] §T5.4 attestation requirement |
| 37 | 5 Possession | **Mixtec** | Only **Chalcatongo Mixtec** [mxc] is coded, and it reads **58A = "Absent"** (no obligatory possessive inflection) and **59A = "No possessive classification"** (Bickel & Nichols / Nichols & Bickel; refs Macaulay 1996) — the primary codes it **against** the row | [D] §T5.4 selection criterion |
| 38 | 6 Inclusive/exclusive | **Cherokee** [che] | **No WALS 39A datapoint.** The only Iroquoian language coded in 39A is **Oneida**, at *"'We' the same as 'I'"*. Cherokee's inclusive/exclusive contrast lives in the **pronominal prefixes**, but WALS 39A is defined on **independent pronouns**, so a grammar citation would attest a *different construction* than the frame defines | [D] §T5.4; frame-mismatch noted |
| 39 | 6 Inclusive/exclusive | **Quechua** | The frozen cell says only "Quechua". The **sole** Quechuan datapoint in 39A is **Imbabura**, coded **"No inclusive/exclusive"** (Cysouw; refs Cole 1982: 129). Cuzco Quechua has **no 39A datapoint**. Cuzco `-nchik`/`-yku` is verbal/possessive morphology, again not an independent pronoun | [D] §T5.4 selection criterion + underspecified cell |
| 40 | 10 Obviation | **Plains Cree** [cre] | **Pre-flagged in the frozen table itself**: essentially Algonquian-only, one family, fails the three-unrelated-families gate. Confirmed: WALS lists Plains Cree [cre] and Swampy Cree [cea] under family **Algic** | [D] §T5.3 pre-flag — **fired exactly as predicted** |
| 41 | 11 Honorifics | **Javanese** [jav] | **No WALS 45A datapoint** (404). Javanese speech levels are a canonical honorific system but WALS 45A codes only **pronouns**, and Javanese is uncoded | [D] §T5.4 attestation requirement |
| 42 | 14 Definiteness | **Persian** [prs] | WALS **37A-prs** = **"No definite, but indefinite article"** (Dryer; refs Rastorgueva 1964). **MAJOR-13 predicted this exactly.** Fails the obligatory-marking selection criterion | MAJOR-13's row-14 rule — **FIRED as written** |

### 2.4 The resulting `N`, under both readings the registration licenses

Per-row survival after attestation:

| row | category | attested on named frame | + substitutes | distinct top-level families among survivors |
|---|---|---|---|---|
| 1 | Evidentiality | **3** | 3 | Tucanoan · Quechuan · Altaic — **3** |
| 2 | Perfective/imperfective | 2 | 2 | Indo-European · Sino-Tibetan — 2 |
| 3 | Optative | 2 | 2 | Kartvelian · Indo-European — 2 |
| 4 | Middle voice | 2 | 2 | Indo-European · Niger-Congo — 2 |
| 5 | Possession | **0** | 0 | — **ROW DIES** |
| 6 | Inclusive/exclusive | **1** | 1 | Austronesian — 1 |
| 7 | Numeral classifiers | **3** | 3 | Sino-Tibetan · Japanese · Mayan — **3** |
| 8 | Egophoricity | 1 | **3** | Sino-Tibetan (+ Nakh-Daghestanian · Barbacoan) |
| 9 | Switch-reference | **0** | **3** | — (+ Trans-New Guinea · Muskogean · Pama-Nyungan) |
| 10 | Obviation | **0** | 0 | — **DROPPED by pre-flag** |
| 11 | Honorifics | 2 | 2 | Japanese · Korean — 2 |
| 12 | Mirativity | 2 | **3** | Altaic · Na-Dene (+ Sino-Tibetan) |
| 13 | Associated motion | **3** | 3 | Pama-Nyungan · Pano-Tacanan · Uto-Aztecan — **3** |
| 14 | Definiteness | 2 | 2 | Afro-Asiatic · Uralic — 2 |

**Strict reading** (a category survives [D] §T5.2's gate only with **three** instances in three
distinct top-level families):
- named frames only → **`N` = 3** (rows 1, 7, 13)
- substitutes admitted → **`N` = 6** (rows 1, 7, 8, 9, 12, 13)

**Lenient reading** (a category survives with **≥2** instances — the reading MAJOR-13's row-14
rule licenses when it says *"row 14 runs on two languages and is marked as such"*):
- named frames only → **`N` = 9** (rows 1, 2, 3, 4, 7, 11, 12, 13, 14)
- substitutes admitted → **`N` = 11** (add rows 8, 9)

[D] §T5.9's first band is **`VOID — family`: fewer than 10 categories surviving the
three-unrelated-families gate ⇒ no verdict.** Three of the four cells above are below 10.
**Only "lenient + substitutes admitted" clears it, at `N` = 11.**

⚠ **This is a registration tension, not an author's call, and it is left open deliberately.**
MINOR-8 restated PARTIAL, DEGENERATE and the power bound as functions of `N` but did **not**
restate the `VOID — family` threshold, which is still the absolute number **10**. MAJOR-13
simultaneously licenses two-language rows. The two rules cannot both bind as written. **Named in
§4.11 as an open design question owed a decision before freeze.**

### 2.5 Verified replacement candidates for the dead and wounded rows

Found in the WALS bulk data and re-verified live. **Offered, not adopted** — every one is a frame
amendment.

**Row 5 (dead) — a family-preserving repair exists.** All three registered families remain
available with real datapoints:

| family as registered | replacement | 58A | 59A | source |
|---|---|---|---|---|
| Austronesian | **Paamese** [pms] | **Exists** | **Three to five classes** | Crowley 1982 |
| Austronesian (alt.) | **Pohnpeian** [poh] | Absent | **Two classes** | Rehg 1981 |
| Na-Dene | **Slave** [sla] | Absent | **Three to five classes** | Rice 1989 |
| Oto-Manguean | **Chichimeca-Jonaz** [cjo] | — | **More than five classes** | Lastra de Suárez 1984 |

**Row 14 (Persian) — MAJOR-13's rule directs that a replacement "from a third family is sought".**
It exists many times over: 27 Indo-European languages carry a definite article in 37A. On the
least arbitrary rule available — *the nearest relative of the dropped language that satisfies the
criterion* — the replacement is **Kurdish (Central)** [krd], **"Definite affix"**, refs Abdulla &
McCarus 1967: 37, 121–122 and Blau 1980: 44, which keeps both Persian's **Iranian genus** and its
Indo-European family. Alternatives with equally good datapoints include Modern Greek, Albanian,
Romanian, Bulgarian, Icelandic, Oriya. **Recommended, not adopted** — the selection is a
registration decision.

**Row 4 (Tamil) — the Dravidian slot is rescuable within Kemmer herself.** Kemmer's sole Dravidian
language is **Kannada**, treated at **p. 199**: *"Kannada, it might be noted, has a two-form middle
system; the reflexive marker is the pronoun `tan-`"*, MM `-koLLu`, source Schiffman 1983. This
substitution stays inside the frozen frame source and preserves the family.

---

## 3. B2 — ROW 1 VALUE INVENTORIES, VERIFIED

**Status of the provisional counts before this task: NOT DATA** (BLOCKER-7, received-numbers
gate). **Status now: 5 / 3 / 2 = 10 pairs, CONFIRMED**, every value named and page-cited.

**Source actually used, and why.** BLOCKER-7 names **Aikhenvald 2004** as the value frame. The
book is **not readable from here** — Google Books volume `BQ9REAAAQBAJ` (*Evidentiality*, verified
by title) is a no-preview title returning page hits without text (Tuyuca at pp. 14, 86, 175, 350,
380, 436); no OA copy exists. **Barnes 1984** (IJAL 50(3): 255–271, DOI 10.1086/465835) is
paywalled, and the single OA copy advertised by OpenAlex (ICESI repository, handle 10906/115880)
is a **255-byte HTML redirect stub back to the paywalled DOI**, not a text.

Falling back to the most primary obtainable source as authorised: **Faller 2002** turns out to
attest **all three** languages directly from Barnes and Aksu-Koç & Slobin, with page citations —
so the inventories below rest on a peer-reviewed doctoral dissertation fetched **in full** from
the author's own institutional page, cross-checked against WALS chapter text.

### 3.1 Tuyuca — **5 values. CONFIRMED.**

**Faller 2002: 42** — *"According to Barnes, Tuyuca has **five** sets of evidential verbal
suffixes: Visual, Nonvisual, Apparent, Secondhand and Assumed."* Her footnote 4: *"All Tuyuca
examples are directly taken from **Barnes (1984: 257)**, including the explanatory contexts in
parentheses."*

The five, with forms, and with the canonical **minimal-pair set** — one sentence varying **only**
in the evidential, which is exactly the item form [D] §T5.4 requires:

| # | value | form | Barnes's example (Faller 2002: 42–43, ← Barnes 1984: 257f.) |
|---|---|---|---|
| 1 | **Visual** | `-wi` | `díiga apé-wi` 'He played soccer.' (I saw him play.) |
| 2 | **Nonvisual** | `-ti` | `díiga apé-ti` 'He played soccer.' (I heard the game and him, but didn't see it or him.) |
| 3 | **Apparent** | `-yi` | `díiga apé-yi` 'He played soccer.' (I have seen evidence that he played: his distinctive shoe print on the playing field. But I did not see him play.) |
| 4 | **Secondhand** | `-yigɨ` | `díiga apé-yigɨ` 'He played soccer.' (I obtained the information from someone else.) |
| 5 | **Assumed** | `-hĩyi` | `díiga apé-hĩyi` 'He played soccer.' (It is reasonable to assume that he did.) |

Barnes's own definitions, quoted by Faller: *"An apparent evidential is used when the speaker
draws conclusions from direct evidence"* (**Barnes 1984: 260**); *"An assumed evidential is used
when the speaker has prior knowledge about the state of things or about habitually general
behavior patterns"* (**Barnes 1984: 262**).

⚠ **Item-authoring hazard, newly surfaced — the paradigm has gaps.** Faller 2002: 42 n. 3: the
evidentials are **portmanteau** morphemes carrying tense, person, gender and number, and *"the
paradigm has gaps: there is no first person present tense Apparent, and there are no present tense
evidentials for Secondhand."* **A minimal pair must not be authored into a gap cell.** All five
examples above are past tense, third person masculine singular, which is a gap-free row.

### 3.2 Cuzco Quechua — **3 values. CONFIRMED — with the obligatoriness caveat.**

**Faller 2002: 14** — *"These evidential contrasts are primarily made by a subset of the focus
enclitics: the **Direct -mi** (allomorph `-n`), the **Reportative -si** (allomorph `-s` or `-sis`
for some speakers in Cuzco), and the **Conjectural -cha** encode the evidential values direct,
reportative and reasoning, respectively."*

| # | value | form | gloss |
|---|---|---|---|
| 1 | **Direct** | `-mi` / `-n` | speaker has the best possible grounds |
| 2 | **Reportative** | `-si` / `-s` (`-sis`) | speaker presents p on the basis that another took it to be fact |
| 3 | **Conjectural** | `-chá` | reasoning |

⚠ **The same sentence continues: *"The use of these evidentials is **not obligatory**, but I will
argue that their absence implicates that the speaker has direct information."*** Faller repeats
this at §1.2.6 ("No evidential") and at p. 152, where she offers the strongest available
softening: *"while it is true that evidentials are not obligatory, the fact that the absence of an
evidential enclitic implicates the evidential meaning of `-mi` makes the use of the other two
evidentials **quasi-obligatory** — that is, when the speaker has a source of information that is
not direct, they will usually use one of the other evidentials."* **See §4.3.**

Also recorded, because it bears on what counts as a value: Faller excludes the past-tense suffixes
`-rqa`/`-sqa` from the evidential inventory (pp. 14, §1.2.8, §4.4), holding that *"the tense
morphemes may not encode an evidential value at all."* Counting them would give 5, not 3; the
designated primary counts **3**.

### 3.3 Turkish — **2 values. CONFIRMED — and the registration names the wrong morpheme.**

**Faller 2002: 41–42** — *"According to Aksu-Koç and Slobin (1986), the past tense form **`-dI`
marks direct experience**, and the form **`-mIş` indirect experience**, where the indirect
experience suffix can convey both inference and hearsay."* And her summary: *"The mapping between
the Turkish evidentials onto evidential types is straightforward: `-dI` indicates **direct**, and
`-mIş` indicates **indirect**."* Footnote 1: *"Both `-dI` and `-mIş` can have various surface
realizations"* — hence the archiphoneme notation.

| # | value | form | gloss |
|---|---|---|---|
| 1 | **Direct / witnessed** | `-DI` | speaker witnessed the event; also generally familiar events (Aksu-Koç & Slobin 1986: 160) |
| 2 | **Indirect / non-firsthand** | `-mIş` | inference from a resultant state, or hearsay |

**Independently confirmed twice at WALS**, which is row 1's own primary frame:
- **WALS ch. 77, ex. (8)**: `Ahmet gel-di` (witnessed) vs `Ahmet gel-miş` (unwitnessed), citing Aksu-Koç & Slobin 1986.
- **WALS ch. 78, ex. (4)**: the same pair.

**See §4.4 — the frozen text's `-mIş/-DIr` is wrong.**

### 3.4 Recomputed pair, judgment and spend deltas

Judgments per minimal pair = **2 gloss conventions × 3 mapper families = 6** ([D] §T5.5).

**Row 1 alone:** 5 + 3 + 2 = **10 pairs = 60 judgments**. BLOCKER-7's arithmetic — *"+7 minimal
pairs → +42 judgments"* against a 3-pair baseline — **is confirmed correct**, and its `+42`
stands. BLOCKER-7's own estimate of the shape of the inventories (*"≈4–6 × 3"*) was right for
Tuyuca and wrong for both others; the verified spread is **5 / 3 / 2**.

**Whole-leg recount.** The registered base was **39 pairs** (13 × 3) **+ 7** (BLOCKER-7) = **46
pairs = 276 judgments**. After attestation:

| scenario | attested instances | pairs | judgments | Δ vs registered |
|---|---|---|---|---|
| **as registered** | 42 (assumed) | 46 | **276** | — |
| **substitutes admitted** | 29 | 10 (row 1) + 26 | **216** | **−10 pairs, −60 judgments** |
| **named frames only** | 23 | 10 (row 1) + 20 | **180** | **−16 pairs, −96 judgments** |

**T5-I1 spend line** (A2.5.2 line 5), at PLANE's measured **$0.000105/judgment**:

| component | registered | substitutes admitted | named frames only |
|---|---|---|---|
| base + BLOCKER-7 | 276 | 216 | 180 |
| MAJOR-12 tag-null | 54 | **36** ⚠ | **36** ⚠ |
| MAJOR-11 stage 2 (hard cap) | 54 | 54 | 54 |
| **total judgments** | **384** | **306** | **270** |
| **est. spend** | $0.05 | **$0.032** | **$0.028** |
| **CAP** | $0.50 | unchanged | unchanged |

The line comes in **under** its registered estimate in both scenarios; the $0.50 cap is untouched
and the global $6.00 cap is unaffected.

⚠ **The tag-null figure moved, and it is a design problem, not an arithmetic one.** MAJOR-12
specifies *"3 categories chosen in ascending category number from those with **≥3 obligatorily-
marked values** … × **3 languages** × 2 pair types × 3 mappers = 54"*. After attestation, the
categories that have **both** ≥3 values **and** 3 surviving language instances are **row 1** and
**row 7** — **two, not three**. MAJOR-12's control is **not constructible as written**. At two
categories the line is 2 × 3 × 2 × 3 = **36**. **Named in §4.10 as owed a decision.**

---

## 4. DISCREPANCIES — every place the primary disagreed with the registration

Received-numbers gate: **the source wins, and the discrepancy is recorded.** Eleven are recorded.
The three MAJOR-13 predicted are marked as such; **eight were not anticipated.**

### 4.1 Row 1, Cuzco Quechua — MAJOR-13's risk CONFIRMED, and it is worse than stated
MAJOR-13 wrote: *"ch. 77's text discusses Tuyuca and Turkish, not Cuzco Quechua."* Verified, and
stronger: the string **"Quechua" occurs ZERO times in the body of WALS chapter 77 and ZERO times
in chapter 78**, and **no Quechuan language of any variety** has a 77A or 78A datapoint except
**Huallaga** and **Imbabura** (both "Direct and indirect" / "Verbal affix or clitic"). Cuzco
Quechua itself has neither. **Disposition applied as written:** the instance is **secondary-frame
for presence as well as for values.**

### 4.2 Row 3, Ancient Greek — MAJOR-13's risk CONFIRMED, and understated
MAJOR-13 anticipated that WALS 73A might have *"no datapoint"* for Ancient Greek. In fact
**Ancient Greek is not a WALS language at all** — WALS codes only Greek (Modern) [grk], Cypriot
Greek, and Greek Sign Language. **Disposition applied as written:** secondary frame; attested at
Smyth 1920 §1814.

### 4.3 Row 1, Cuzco Quechua — the row's own selection criterion fails on the designated primary
Row 1 is registered as *"Evidentiality — source of knowing, **obligatory**"*. Faller 2002: 14, the
source the task designates: *"The use of these evidentials is **not obligatory**."* The strongest
available softening is her own **"quasi-obligatory"** (p. 152), and it covers only the two
non-direct enclitics. **This is not a fill-time judgment call.** Either row 1's criterion is
relaxed to "systematic" for this instance by amendment and the relaxation is disclosed, or the
instance drops on the criterion — in which case row 1 falls to **2** languages and stops being one
of the three rows that clears the strict family gate.

### 4.4 Row 1, Turkish — the registration names the wrong morpheme
§A2.7 task B2 names *"the standard Turkish grammars for **`-mIş`/`-DIr`**"*. `-DIr` is the
generalizing/assumptive copular suffix. The direct/witnessed past that contrasts with `-mIş` is
**`-DI`**. Confirmed at **three independent primaries**: Faller 2002: 41–42, WALS ch. 77 ex. (8),
WALS ch. 78 ex. (4) — all ultimately Aksu-Koç & Slobin 1986. **Correct to `-mIş`/`-DI`.**

### 4.5 Row 3, Turkish — NOT ANTICIPATED. The frame codes the language as lacking the category
WALS **73A-tur = "Inflectional optative absent"**. Row 3 samples Turkish *as an instance of* the
optative. MAJOR-13 flagged row 3's **Ancient Greek** cell as the risk and did not look at the
Turkish one. This is structurally identical to the Persian failure MAJOR-13 *did* catch, and it
was missed. The instance drops.

### 4.6 Row 5 — NOT ANTICIPATED. The row dies outright
Hawaiian and Navajo have **no 58A or 59A datapoint**; Chalcatongo Mixtec, the only coded Mixtec,
is coded **against** the row (58A "Absent", 59A "No possessive classification"). **0 of 3.** Row 5
was not on MAJOR-13's at-risk list. It is the single largest hit to `N` in this pass.

### 4.7 Row 7, Mandarin and Japanese — NOT ANTICIPATED. Datapoints with no source
WALS **55A-mnd** and **55A-jpn** (Gil) both carry the coded value "Obligatory" but **no References
section at all** on the live datapoint page — verified by direct fetch; contrast 55A-yct, which
carries Suárez 1983b: 88. They satisfy MAJOR-13's *"or a WALS datapoint"* limb but **not** its
*"named published example"* limb. Recorded as **WALS-primary (weak)**. This matters because row 7
is one of only three rows that clears the strict family gate.

### 4.8 Row 13, Cupeño — content unverified
Guillaume & Koch 2021 has **no Cupeño chapter**; Cupeño appears inside Dryer's ch. 13 (pp. 485–526)
at pp. 492, 502, 505, 506, 516. **Only the presence of the string is verified.** Whether Dryer
treats Cupeño as *having* associated motion or as a **negative** case is **UNVERIFIED**, and the
volume returns no snippet text. If row 13 is load-bearing — and under the strict reading it is one
of three surviving rows — **ch. 13 must be read directly before freeze.**

### 4.9 Rows 8, 9, 12, 13 — NOT ANTICIPATED. The named survey volumes do not contain most of the named languages
[D] §7 doubt 12 registered that the non-WALS categories carry a *weaker independence guarantee*.
The actual defect is different and larger: **the volumes largely do not treat the languages at
all.**

| row | named frame | languages actually treated as chapters |
|---|---|---|
| 8 | Floyd, Norcliffe & San Roque 2018 | Kathmandu Newar **yes**; Akhvakh **no**; Tsafiki **no** (the Barbacoan chapter is **Cha'palaa**) |
| 9 | Haiman & Munro 1983 | Amele **no**; Choctaw **no**; Diyari **no** — **0 of 3** |
| 12 | DeLancey 1997 | Turkish **yes**; Hare **yes**; Magar **no** |
| 13 | Guillaume & Koch 2021 | none as a chapter, but all three appear inside survey chapters |

**Row 9's frame fails completely.** Haiman & Munro 1983's 14 substantive chapters (verified
independently by me at Crossref, pp. 1–316 contiguous) cover Quechua, Huichol, Kewa, Maricopa,
Nunggubuyu, Wojokeso/Guanano, Lenakel, Northeast Caucasus, Kashaya and Central Yup'ik. The 1983
volume **predates the Amele description** — the canonical source is Roberts 1987/1988. **Citing
Haiman & Munro 1983 for Amele, Choctaw or Diyari would have been a fabricated citation**, and the
attestation column is what caught it.

### 4.10 MAJOR-12's tag-null control is not constructible as written
It requires **3** categories with ≥3 obligatorily-marked values **and** 3 language instances. After
attestation, **2** qualify (rows 1 and 7). Either the control runs on two categories (36
judgments), or its selection rule is relaxed by amendment. **Owed a decision.**

### 4.11 `VOID — family`'s threshold and MAJOR-13's two-language rule contradict each other
MINOR-8 made PARTIAL, DEGENERATE and the power bound functions of `N` but left `VOID — family` at
the absolute number **10**, while MAJOR-13 licenses rows that *"run on two languages"*. On named
frames `N` = 9 under the lenient reading and 3 under the strict one — **`VOID — family` fires in
three of the four cells**. **Owed a decision before freeze.** See §2.4.

### 4.12 Two family labels in the frozen table are genera, not families — MINOR-7's defect recurs
MINOR-7 corrected rows 5 and 12 from "Athabaskan" (a genus) to **Na-Dene**. The same defect
survives in two further cells, verified against `languages.csv`:

| frozen table says | WALS family | WALS genus |
|---|---|---|
| **Turkic** (Turkish, rows 1, 3, 12) | **Altaic** | Turkic |
| **Tacanan** (Cavineña, row 13) | **Pano-Tacanan** | Tacanan |

Two further cells differ in name only and are harmless: "Atlantic-Congo" (Swahili) is **Niger-Congo**
in WALS, and "Japonic" is **Japanese**. **No row loses its three-family independence under the
corrections** — Tucanoan/Quechuan/Altaic and Pama-Nyungan/Pano-Tacanan/Uto-Aztecan are still three
distinct families each. Recorded so that a scorer applying [D] §T5.2's *"family level, not genus"*
gate literally does not drop a row that should stand.

### 4.13 MAJOR-14's non-independence claim is CONFIRMED at the primary
MAJOR-14 asserted from memory that rows 1 and 12 share the Turkish morpheme `-mIş`. **Verified**:
Faller 2002: 41 n. 2 — *"The suffix `-mIş` also has a mirative use, and Aksu-Koç and Slobin (1986)
make a proposal to account for all three uses"* — and Hill 2012: 416 reproduces DeLancey 1997: 38's
mirative `-mIş` example. The **one-witness** rule stands, now on evidence rather than recall.

### 4.14 Two underspecified cells in the frozen table
Row 6 says only "Quechua" and row 14 only "Arabic"; row 5 says only "Mixtec". WALS codes 10
Quechua varieties, 21 Arabic varieties and 17 Mixtec varieties, and **the choice changes the
answer** for Quechua and Mixtec (§2.3 #37, #39). It does **not** for Arabic: all seven varieties
coded in 37A read "Definite affix", so instance #24 is robust. Cells should be pinned to a WALS
code at freeze.

---

## 5. What is owed before the freeze

1. **Decide §4.11** — the `VOID — family` threshold versus MAJOR-13's two-language rule. Nothing
   else in T5 can be scored until this is settled; on the strict reading the leg is already VOID.
2. **Decide §2.2** — admit the six substitute sources by amendment, or run without them. Named
   frames alone leave `N` = 9 and the leg VOID.
3. **Decide §4.3** — relax row 1's *obligatory* criterion to *systematic* for Cuzco Quechua and
   disclose it, or drop the instance.
4. **Correct `-mIş/-DIr` → `-mIş/-DI`** (§4.4).
5. **Decide row 5** — dead, or repaired with the verified replacements in §2.5.
6. **Decide row 14's replacement** — Kurdish (Central) is recommended on a stated rule; or run on
   two languages as MAJOR-13 permits.
7. **Read Dryer ch. 13 pp. 485–526 directly** for Cupeño (§4.8) — row 13 is otherwise carrying a
   surviving-row slot on an unverified claim.
8. **Decide §4.10** — MAJOR-12's tag-null control on two categories, or relax its selection rule.
9. **Pin the underspecified cells to WALS codes** (§4.14).
10. **Stage 2 is not attested.** MAJOR-11 caps recurrence at 3 categories × 3 further unrelated
    families = 54 judgments, but **no attestation exists for any stage-2 language**. That is a
    second T5-ATTEST pass, owed before stage 2 runs, not before freeze.

---

## Appendix — sources actually reached

**Live WALS** (`wals.info`): chapters 77, 78 (full body text); datapoints 77A/78A ×
{tuy, tur, qcu✗, qhu, qim}, 65A × {rus, mnd, swa}, 73A × {tur, geo, grk}, 58A/59A ×
{haw✗, nav✗, mxc}, 39A × {tag, che✗, qcu✗, qim, cre}, 55A × {mnd, jpn, yct}, 45A ×
{jpn, kor, jav✗}, 37A × {ams, aeg, hun, prs}. ✗ = verified 404.

**WALS CLDF release** (`cldf-datasets/wals`): `values.csv`, `languages.csv`, `codes.csv`,
`parameters.csv`.

**Full text fetched:** Faller, Martina T. 2002, *Semantics and Pragmatics of Evidentials in Cuzco
Quechua*, Stanford PhD (author's own university page). Hill, Nathan W. 2012, *"Mirativity" does
not exist* (SOAS eprints via Wayback). Guillaume & Koch 2021, Introduction ch. 1 (HAL via Wayback).
Guillaume 2016, *Associated motion in South America* (HAL via Wayback). Hengeveld &
Dall'Aglio Hattnher 2015, *Four types of evidentiality in the native languages of Brazil* (UvA-DARE).
Smyth 1920, *A Greek Grammar for Colleges* §1814 (Perseus).

**Publisher-deposited metadata:** Crossref TOCs for TSL 2 (Haiman & Munro 1983, 20 items) and
TSL 118 (Floyd et al. 2018, 20 items), both re-verified by me independently of the agents that
first reported them; Crossref/OpenAlex records for DeLancey 1997, Aikhenvald 2012, Barnes 1984,
Creissels 2008, Dickinson 2000, Davies 1984, Austin 1981, Grunow-Hårsta 2007, Guillaume & Koch 2021.

**Google Books search-inside** (page text): Kemmer 1993 (`mQv0QmkTHbMC`), Arnott 1970, Asher 1982,
Schiffman 1999. Page-hit only, no text: Guillaume & Koch 2021 (`k9whEAAAQBAJ`), Hill 2005.

**Reached and unusable:** Aikhenvald 2004 (`BQ9REAAAQBAJ`, no-preview: page hits only);
Barnes 1984 (paywalled; ICESI "OA" copy is a 255-byte redirect stub); *Oxford Handbook of
Evidentiality* figshare record (metadata only, no files); benjamins.com, degruyter.com,
annualreviews.org, sil.org (all 403).

**Not reached, and it matters:** Aikhenvald 2004 itself, and Barnes 1984 itself. Row 1's value
inventories rest on **Faller 2002's** page-cited report of Barnes and of Aksu-Koç & Slobin —
peer-reviewed and primary in its own right, but **one remove** from the two sources BLOCKER-7
names. If either count is to be quoted as read from Aikhenvald 2004, someone must open the book.
