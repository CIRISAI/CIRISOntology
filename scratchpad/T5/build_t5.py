#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Author the T5 minimal-pair corpus (34 pairs) and the MAJOR-12 tag-null control (12 items).

Governed by RECOGNITION_PREREG.md §T5.3-§T5.5, RECOGNITION_PREREG_A2.md BLOCKER-7 /
MAJOR-12 / MAJOR-13, RECOGNITION_PREREG_A3.md (lenient + substitutes, corrections),
and T5_ATTEST.md §2/§3 as the source of truth for surviving instances and citations.
"""
import json, os

BASE = "/home/emoore/CIRISOntology/scratchpad/T5"

# ---------------------------------------------------------------------------
# Fixed, kind-neutral tag vocabulary. One prefix per category; the value set per
# category is closed and declared here. No value is a kind name.
# ---------------------------------------------------------------------------
TAG_VOCAB = {
    "evidentiality":            ("EVID",   ["visual", "nonvisual", "apparent", "secondhand",
                                            "assumed", "direct", "reportative", "conjectural",
                                            "indirect"]),
    "perfective/imperfective":  ("ASPECT", ["bounded", "unbounded"]),
    "optative":                 ("MOOD",   ["statement", "wish"]),
    "middle voice":             ("VOICE",  ["active", "middle"]),
    "numeral classifiers":      ("CLF",    ["long-thin", "chunk", "small-animal",
                                            "large-animal", "animate", "inanimate"]),
    "egophoricity":             ("EGO",    ["self", "other"]),
    "switch-reference":         ("REF",    ["same-subject", "different-subject"]),
    "honorifics":               ("HON",    ["plain", "exalted"]),
    "mirativity":               ("MIR",    ["expected", "surprise"]),
    "associated motion":        ("MOTION", ["go-and-do", "come-and-do", "do-while-going"]),
    "definiteness":             ("DEF",    ["definite", "indefinite"]),
}

# ---------------------------------------------------------------------------
# One preamble per category, identical across every item of that category.
# The preamble is the only field licensed to use linguistic meta-vocabulary.
# ---------------------------------------------------------------------------
PREAMBLE = {
"evidentiality":
 "CATEGORY NOTE. In this language every finite clause must also mark how the speaker came "
 "to know what the clause says: by seeing it, by hearing or otherwise sensing it without "
 "seeing it, by finding traces of it afterwards, by being told it by someone else, or by "
 "supposing it from what is generally so. The bracketed tag in the passage below names "
 "which of those the marked clause carries. The tag is not part of the sentence's wording; "
 "it stands in for a suffix the language attaches to the verb and that a speaker cannot "
 "leave off.",
"perfective/imperfective":
 "CATEGORY NOTE. In this language every finite verb must also mark whether the event is "
 "presented as a single completed whole with its endpoint included, or as ongoing, "
 "repeated, or viewed from inside without its endpoint. The bracketed tag in the passage "
 "below names which of the two the marked clause carries. The tag is not part of the "
 "sentence's wording; it stands in for a verbal marking a speaker cannot leave off.",
"optative":
 "CATEGORY NOTE. In this language the verb carries a distinct inflected form used to "
 "express a wish about how things should turn out, alongside the ordinary form used to "
 "state how things are or were. The bracketed tag in the passage below names which of the "
 "two forms the marked clause carries. The tag is not part of the sentence's wording; it "
 "stands in for an inflection on the verb, not for an added word.",
"middle voice":
 "CATEGORY NOTE. In this language the verb must take one of a set of endings that mark "
 "whether the subject simply acts on something else, or is itself the seat of the event -- "
 "acting on itself, acting for its own benefit, or undergoing the event in its own body. "
 "The bracketed tag in the passage below names which ending the marked clause carries. The "
 "tag is not part of the sentence's wording; it stands in for the verb's own inflection.",
"numeral classifiers":
 "CATEGORY NOTE. In this language a noun cannot be counted with a bare numeral. A counting "
 "word must stand between the numeral and the noun, drawn from a closed set and chosen "
 "according to what sort of thing is being counted -- its shape, whether it is alive, or "
 "the class it is taken to belong to. The bracketed tag in the passage below names which "
 "counting word the phrase carries. The tag is not part of the sentence's wording; it "
 "stands in for a word a speaker cannot leave out of a count phrase.",
"egophoricity":
 "CATEGORY NOTE. In this language the verb must mark whether the speaker is the "
 "participant with privileged access to the event -- the one who brought it about "
 "deliberately, or whose own inner condition is being described -- or whether the event "
 "belongs to someone else's access instead. The bracketed tag in the passage below names "
 "which of the two the marked clause carries. The tag is not part of the sentence's "
 "wording; it stands in for a verbal ending a speaker cannot leave off.",
"switch-reference":
 "CATEGORY NOTE. In this language a non-final clause in a chain must carry a marker saying "
 "whether the subject of the following clause is the same participant as its own subject "
 "or a different one. The bracketed tag in the passage below names which of the two the "
 "marked clause carries. The tag is not part of the sentence's wording; it stands in for a "
 "suffix on the non-final verb that a speaker cannot leave off.",
"honorifics":
 "CATEGORY NOTE. In this language a speaker cannot address or refer to another person "
 "without choosing a form that encodes that person's social standing relative to the "
 "speaker. Plain forms are used downward and among intimates; elevated forms, including "
 "the avoidance of a direct second-person word in favour of a title, are used upward. The "
 "bracketed tag in the passage below names which level the marked clause carries. The tag "
 "is not part of the sentence's wording; it stands in for that obligatory choice.",
"mirativity":
 "CATEGORY NOTE. In this language the verb must mark whether what is said fits what the "
 "speaker already held to be so, or whether it is newly come upon and runs against what "
 "the speaker had been supposing up to that moment. The bracketed tag in the passage below "
 "names which of the two the marked clause carries. The tag is not part of the sentence's "
 "wording; it stands in for a verbal marking a speaker cannot leave off.",
"associated motion":
 "CATEGORY NOTE. In this language a verb must also mark the travel that goes with the "
 "event it names: whether the participant went somewhere and then did it, came somewhere "
 "and then did it, or did it while travelling. The bracketed tag in the passage below "
 "names which of those the marked clause carries. The tag is not part of the sentence's "
 "wording; it stands in for a suffix on the verb, not for an added phrase.",
"definiteness":
 "CATEGORY NOTE. In this language a noun phrase must be marked for whether the thing it "
 "names is one the hearer is expected to be able to pick out already, or one being brought "
 "in as new. The bracketed tag in the passage below names which of the two the marked "
 "phrase carries. The tag is not part of the sentence's wording; it stands in for an affix "
 "or particle the language attaches to the noun phrase.",
}

# ---------------------------------------------------------------------------
# Citations, copied from T5_ATTEST.md's verified column (one per instance).
# ---------------------------------------------------------------------------
CIT = {
"tuyuca":
 "WALS 77A-tuy and 78A-tuy (de Haan; refs Barnes 1984); datapoint examples igt-1847 "
 "'The motor roared' (heard it) and igt-1848 'My stomach hurts' (feel it). Five-value "
 "minimal set at Faller 2002: 42-43, taken directly from Barnes 1984: 257f. "
 "(diiga ape-wi / -ti / -yi / -yigi / -hiyi 'He played soccer'); Barnes 1984: 260 "
 "(apparent), 262 (assumed). Frame class WALS-primary for presence, Faller 2002 for "
 "values (secondary, BLOCKER-7).",
"cuzco quechua":
 "No WALS datapoint (77A-qcu and 78A-qcu both verified 404). Faller 2002: 14: the Direct "
 "-mi (allomorph -n), the Reportative -si (-s / -sis), the Conjectural -cha. Frame class "
 "survey-secondary, MAJOR-13's row-1 rule fired. Obligatoriness relaxed to SYSTEMATIC for "
 "this instance per A3.3 (Faller 2002: 14 'not obligatory', 152 'quasi-obligatory').",
"turkish-evid":
 "WALS 77A-tur (de Haan; refs Aksu-Koc & Slobin 1986), ch. 77 ex. (8) 'Ahmet gel-di' "
 "(witnessed) vs 'Ahmet gel-mis' (unwitnessed); WALS 78A-tur, ch. 78 ex. (4), same "
 "morpheme pair; Faller 2002: 41-42. Morpheme pair corrected to -DI / -mIs per A3.4 (1).",
"russian":
 "WALS 65A-rus (Dahl & Velupillai; refs Dahl 1985: 172), coded 'Grammatical marking'. "
 "Frame class WALS-primary.",
"mandarin-aspect":
 "WALS 65A-mnd (Dahl & Velupillai; refs Dahl 1985: 180), coded 'Grammatical marking'. "
 "Frame class WALS-primary.",
"georgian":
 "WALS 73A-geo (Dobrushina, van der Auwera & Goussev; refs Hewitt 1995: 572), coded "
 "'Inflectional optative present'; datapoint carries glossed example igt-1576 "
 "(mo-g-sl-od-e-t, optative). Frame class WALS-primary.",
"ancient greek":
 "Not a WALS language (WALS codes only Greek (Modern), Cypriot Greek, Greek Sign "
 "Language). Attested at Smyth 1920, A Greek Grammar for Colleges, section 1814 'Optative "
 "of Wish', read at Perseus: 'In independent sentences the optative without an is used to "
 "express a wish referring to the future (negative me)', with the named published example "
 "Sophocles, Ajax 550, 'o pai, genoio patros eutuchesteros'. Frame class survey-secondary, "
 "MAJOR-13's row-3 rule fired.",
"classical greek":
 "Kemmer 1993, Appendix B 'Data Sources' p. 271 ('Greek, Classical: Smyth (1920), Wright "
 "(1912)'); Index of Languages p. 297 (~20 loci); inflectional middle described p. 249 "
 "(-mai 1sg present middle ending); example p. 57, Table 6, 'pete-sthai' 'fly'. Frame "
 "class survey-secondary.",
"fula":
 "Kemmer 1993, Appendix B p. 271 ('Fula, Gombe dialect: Arnott (1970). Niger-Congo, West "
 "Atlantic'); Index p. 297 (13 loci); example p. 26, middle marker -o, RM -(i)t-o, "
 "'ndaar-t-o' 'look at oneself', classified two-form 'Dutch type'. Corroborated in "
 "Kemmer's own source, Arnott 1970: 179 ('15 Active tenses, 14 Middle, and 13 Passive "
 "tenses') and p. 189 (middle-only radicals). Frame class survey-secondary.",
"mandarin-clf":
 "WALS 55A-mnd (Gil), coded 'Obligatory'. The live datapoint page carries NO References "
 "section; frame class WALS-primary (weak), per T5_ATTEST section 4.7.",
"japanese-clf":
 "WALS 55A-jpn (Gil), coded 'Obligatory'. The live datapoint page carries NO References "
 "section; frame class WALS-primary (weak), per T5_ATTEST section 4.7.",
"yucatec":
 "WALS 55A-yct (Gil; refs Suarez 1983b: 88), coded 'Obligatory'. Frame class WALS-primary.",
"kathmandu newar":
 "Hargreaves, David. \"'Am I blue?': Privileged access constraints in Kathmandu Newar.\" "
 "Ch. 2, pp. 79-107 of Floyd, Norcliffe & San Roque (eds.) 2018, Egophoricity (TSL 118), "
 "DOI 10.1075/tsl.118.02har. Table of contents verified independently twice. Frame class "
 "survey-secondary.",
"akhvakh":
 "SUBSTITUTE-SECONDARY, admitted by A3.1. The named frame (Floyd, Norcliffe & San Roque "
 "2018) has no Akhvakh chapter. Attested at Creissels, Denis. 2008. 'Person variations in "
 "Akhvakh verb morphology: functional motivation and origin of an uncommon pattern.' STUF "
 "61(4): 309-325, DOI 10.1524/stuf.2008.0027: the same endings encode 1st vs 2nd/3rd in "
 "declaratives and 2nd vs 1st/3rd in questions, restricted to the perfective positive.",
"tsafiki":
 "SUBSTITUTE-SECONDARY, admitted by A3.1. The named frame's Barbacoan chapter is on the "
 "sister language Cha'palaa. Attested at Dickinson, Connie. 2000. 'Mirativity in Tsafiki.' "
 "Studies in Language 24(2): 379-422, DOI 10.1075/sl.24.2.06dic; and Dickinson 2002, "
 "Complex Predicates in Tsafiki, PhD, Oregon. Bibliographic record verified; the content "
 "claim rests on this being the source the volume's chapters cite for Tsafiki.",
"amele":
 "SUBSTITUTE-SECONDARY, admitted by A3.1. Haiman & Munro 1983 has no Amele chapter (the "
 "volume's Papuan chapters are Kewa and Wojokeso) and predates the Amele description. "
 "Attested at Roberts, John R. 1988. 'Amele switch-reference and the theory of grammar.' "
 "Linguistic Inquiry 19(1): 45-63; and Roberts 1987, Amele (Croom Helm Descriptive "
 "Grammars).",
"choctaw":
 "SUBSTITUTE-SECONDARY, admitted by A3.1. Haiman & Munro 1983 has no Choctaw chapter. "
 "Attested at Davies, William D. 1984. 'Choctaw Switch-Reference and Levels of Syntactic "
 "Representation.' In The Syntax of Native American Languages (Syntax and Semantics 16), "
 "pp. 123-147, DOI 10.1163/9789004373129_006; and Broadwell 2006, A Choctaw Reference "
 "Grammar.",
"diyari":
 "SUBSTITUTE-SECONDARY, admitted by A3.1. Haiman & Munro 1983's only Australian chapter is "
 "Heath on Nunggubuyu. Attested at Austin, Peter. 1981. 'Switch-Reference in Australia.' "
 "Language 57(2): 309-334, DOI 10.2307/413693; and Austin 1981, A Grammar of Diyari, South "
 "Australia (CUP).",
"japanese-hon":
 "WALS 45A-jpn (Helmbrecht; refs Hinds 1986: 238-265), coded 'Pronouns avoided for "
 "politeness'; the datapoint's Notes field enumerates anata, anta, kimi, kisama, omae, "
 "o-taku. Frame class WALS-primary.",
"korean":
 "WALS 45A-kor (Helmbrecht; refs Sohn 1999: 207f, 251f, 407-413), coded 'Pronouns avoided "
 "for politeness'; the datapoint's Notes field enumerates caki, caney, elusin, kutay, ne, "
 "tangsin, tayk. Frame class WALS-primary.",
"turkish-mir":
 "DeLancey 1997: 38, morpheme -mIs; flagship example 'kiz-iniz cok iyi piyano cal-iyor-mus' "
 "'Your daughter plays piano very well!' (after Slobin & Aksu-Koc 1982: 197). "
 "Independently corroborated at Faller 2002: 41 n. 2. Frame class survey-secondary. NOT "
 "INDEPENDENT of the row 1 Turkish instance: the two share the morpheme -mIs (MAJOR-14, "
 "confirmed at the primary in T5_ATTEST section 4.13); a site supported by both counts as "
 "ONE witness.",
"hare":
 "DeLancey 1997: 38-40, suffix -lo; examples 'juhye sa k'inayeda lo' 'I see there was a "
 "bear walking around here' (1997: 38), the inference reading (1997: 39), and the "
 "compliment 'deshita yedaniyie lo' (1997: 40). Corroborated by DeLancey's own 2012 "
 "abstract, which names Hare as the exemplifying language. Frame class survey-secondary.",
"magar":
 "SUBSTITUTE-SECONDARY, admitted by A3.1. DeLancey 1997 does not treat Magar (his "
 "languages are Tibetan, Hare, Sunwar, Korean, Turkish, Kalasha, enumerated at Hill 2012: "
 "413). Attested at Grunow-Harsta, Karen. 2007. 'Evidentiality and mirativity in Magar.' "
 "LTBA 30(2): 151-194, DOI 10.32655/ltba.30.2.06. The specific Magar morphemes are "
 "UNVERIFIED at the primary (T5_ATTEST section 2.2 #31).",
"arrernte":
 "Koch, Harold. 'Associated motion in the Pama-Nyungan languages of Australia.' Ch. 7, pp. "
 "231-324 of Guillaume & Koch (eds.) 2021, Associated Motion (EALT 64). In-volume hits for "
 "Arrernte / Mparntwe Arrernte / Arandic at pp. 254, 257-268, 311-313, 324, inside ch. 7. "
 "Frame class survey-secondary.",
"cavinena":
 "Guillaume & Koch 2021, Introduction p. 4, example (1), the volume's opening illustration "
 "of the category: ba-ti- 'go and see O', ba-na- 'come and see O', ba-aje- 'see O while "
 "going', ba-be-, ba-kena-, ba-dadi-, ba-tsa-. Full twelve-suffix paradigm at Guillaume "
 "2016: 88, Table 1 (open access, fetched in full); grammar locus Guillaume 2008: 212-236. "
 "Frame class survey-secondary.",
"arabic":
 "WALS 37A-ams (Modern Standard Arabic; Dryer; refs Cowan 1958: 9), coded 'Definite "
 "affix'. All seven Arabic varieties coded in 37A read the same value, so the instance is "
 "robust to which variety is pinned. Frame class WALS-primary.",
"hungarian":
 "WALS 37A-hun (Dryer; refs Kenesei et al. 1998: 94; Benko & Imre 1972: 89-90), coded "
 "'Definite word distinct from demonstrative'. Frame class WALS-primary.",
}

# ---------------------------------------------------------------------------
# THE 34 MINIMAL PAIRS
# Each entry: id, row, category, language, value, cit_key, tagT (template with
# {TAG}), tb/ta (tag values), nb/na (GLOSS-N before / after), site, fid.
# ---------------------------------------------------------------------------
def P(**kw):
    return kw

# --- row 1, Evidentiality: one pair per value per language (BLOCKER-7) -------
TUY_T = ("The field by the landing was in use again yesterday afternoon. The eldest of "
         "the three brothers played in the game there {TAG}. The field is free again "
         "from Saturday.")
def tuy_n(clause):
    return ("The field by the landing was in use again yesterday afternoon. " + clause +
            " The field is free again from Saturday.")
TUY_N = {
 "visual":     tuy_n("The eldest of the three brothers played in the game there; I watched "
                     "the whole of it from the bank."),
 "nonvisual":  tuy_n("The eldest of the three brothers played in the game there; I could "
                     "hear the game and his voice from the path, but I never saw the field."),
 "apparent":   tuy_n("The eldest of the three brothers played in the game there; afterwards "
                     "I found his shoe prints all over the near end of the field, though I "
                     "did not see him play."),
 "secondhand": tuy_n("The eldest of the three brothers played in the game there; one of the "
                     "women at the landing told me so."),
 "assumed":    tuy_n("The eldest of the three brothers played in the game there; he never "
                     "misses a game on that field, so he will have been in it."),
}
TUY_SITE = ("Only the marked clause's account of how the speaker came to know that the "
            "brother played changes; the surrounding sentences are held.")

TUY2_T = ("The outboard on the far bank ran for most of the night {TAG}. The fuel drum at "
          "the store is down to the last of it.")
TUY2_N = {
 "visual":    "The outboard on the far bank ran for most of the night; I watched it from "
              "the window. The fuel drum at the store is down to the last of it.",
 "nonvisual": "The outboard on the far bank ran for most of the night; I could hear it from "
              "the house but never saw the boat. The fuel drum at the store is down to the "
              "last of it.",
}
TUY2_SITE = ("Only the marked clause's account of how the speaker came to know that the "
             "outboard ran changes; the surrounding sentence is held.")

QCU_T = ("The mill at the top of the road shut early on Tuesday {TAG}. Anyone with grain "
         "waiting there will need to come back on Thursday. The gate on the lower path "
         "stays open as usual.")
def qcu_n(clause):
    return (clause + " Anyone with grain waiting there will need to come back on Thursday. "
            "The gate on the lower path stays open as usual.")
QCU_N = {
 "direct":      qcu_n("The mill at the top of the road shut early on Tuesday; I was standing "
                      "at the gate when they closed it."),
 "reportative": qcu_n("The mill at the top of the road shut early on Tuesday; that is what "
                      "the woman who keeps the gate says."),
 "conjectural": qcu_n("The mill at the top of the road shut early on Tuesday; the yard was "
                      "empty by mid-afternoon, so it must have."),
}
QCU_SITE = ("Only the marked clause's account of how the speaker came to know that the mill "
            "shut early changes; the surrounding sentences are held.")

QCU2_T = ("The road above the bridge was blocked on Tuesday morning {TAG}. Carts are going "
          "round by the lower track until it is cleared.")
QCU2_N = {
 "direct":      "The road above the bridge was blocked on Tuesday morning; I saw the stones "
                "down across it myself. Carts are going round by the lower track until it "
                "is cleared.",
 "reportative": "The road above the bridge was blocked on Tuesday morning; that is what the "
                "carter says. Carts are going round by the lower track until it is cleared.",
}
QCU2_SITE = ("Only the marked clause's account of how the speaker came to know that the road "
             "was blocked changes; the surrounding sentence is held.")

TURA_T = ("The inspector came on the morning bus {TAG}. The site office will stay open "
          "until the visit is finished.")
TURA_N = {
 "direct":   "The inspector came on the morning bus; I met the bus myself. The site office "
             "will stay open until the visit is finished.",
 "indirect": "The inspector came on the morning bus, by all accounts. The site office will "
             "stay open until the visit is finished.",
}
TURB_T = ("The teacher came back to the village last night {TAG}. Lessons start again on "
          "Monday at the usual hour.")
TURB_N = {
 "direct":   "The teacher came back to the village last night; I saw her get down from the "
             "truck. Lessons start again on Monday at the usual hour.",
 "indirect": "The teacher came back to the village last night, from what people are saying. "
             "Lessons start again on Monday at the usual hour.",
}
TUR_SITE = ("Only the marked clause's account of how the speaker came to know of the arrival "
            "changes; the surrounding sentence is held.")

ITEMS = [
 P(id="t5-r01-tuy-visual", row=1, cat="evidentiality", lang="Tuyuca", value="visual",
   cit="tuyuca", tmpl=TUY2_T, tb="nonvisual", ta="visual",
   nb=TUY2_N["nonvisual"], na=TUY2_N["visual"], site=TUY2_SITE,
   fid="A second Tuyuca scenario is used for this pair so that it is not the byte-inverse of "
       "t5-r01-tuy-assumed on one text. It stays in the register of the WALS datapoint's own "
       "example igt-1847, 'The motor roared' (I heard it), and in the gap-free past-3sg row "
       "per A3.4 (2); the river framing is invented."),
 P(id="t5-r01-tuy-nonvisual", row=1, cat="evidentiality", lang="Tuyuca", value="nonvisual",
   cit="tuyuca", tmpl=TUY_T, tb="visual", ta="nonvisual",
   nb=TUY_N["visual"], na=TUY_N["nonvisual"], site=TUY_SITE,
   fid="As t5-r01-tuy-visual. The GLOSS-N wording follows Barnes's parenthetical context "
       "'I heard the game and him, but didn't see it or him' (Faller 2002: 42)."),
 P(id="t5-r01-tuy-apparent", row=1, cat="evidentiality", lang="Tuyuca", value="apparent",
   cit="tuyuca", tmpl=TUY_T, tb="visual", ta="apparent",
   nb=TUY_N["visual"], na=TUY_N["apparent"], site=TUY_SITE,
   fid="As t5-r01-tuy-visual. The GLOSS-N wording follows Barnes's parenthetical context "
       "'his distinctive shoe print on the playing field' (Faller 2002: 42)."),
 P(id="t5-r01-tuy-secondhand", row=1, cat="evidentiality", lang="Tuyuca", value="secondhand",
   cit="tuyuca", tmpl=TUY_T, tb="visual", ta="secondhand",
   nb=TUY_N["visual"], na=TUY_N["secondhand"], site=TUY_SITE,
   fid="As t5-r01-tuy-visual. GLOSS-N follows 'I obtained the information from someone "
       "else' (Faller 2002: 42)."),
 P(id="t5-r01-tuy-assumed", row=1, cat="evidentiality", lang="Tuyuca", value="assumed",
   cit="tuyuca", tmpl=TUY_T, tb="visual", ta="assumed",
   nb=TUY_N["visual"], na=TUY_N["assumed"], site=TUY_SITE,
   fid="As t5-r01-tuy-visual. GLOSS-N follows 'It is reasonable to assume that he did' "
       "(Faller 2002: 43) and Barnes 1984: 262 on prior knowledge of habitual behaviour."),

 P(id="t5-r01-qcu-direct", row=1, cat="evidentiality", lang="Cuzco Quechua", value="direct",
   cit="cuzco quechua", tmpl=QCU2_T, tb="reportative", ta="direct",
   nb=QCU2_N["reportative"], na=QCU2_N["direct"], site=QCU2_SITE,
   fid="INVENTED SCENARIO. Faller 2002 attests the three enclitics and their values but "
       "supplies no example domain that was carried into this item; the road scenario is "
       "invented and mundane. A second scenario is used for this pair so that it is not the "
       "byte-inverse of t5-r01-qcu-conjectural on one text. Marking is SYSTEMATIC, not "
       "obligatory, per A3.3."),
 P(id="t5-r01-qcu-reportative", row=1, cat="evidentiality", lang="Cuzco Quechua",
   value="reportative", cit="cuzco quechua", tmpl=QCU_T, tb="direct", ta="reportative",
   nb=QCU_N["direct"], na=QCU_N["reportative"], site=QCU_SITE,
   fid="INVENTED SCENARIO, as t5-r01-qcu-direct. GLOSS-N follows Faller's gloss of -si, "
       "'the speaker presents p on the basis that another took it to be fact'."),
 P(id="t5-r01-qcu-conjectural", row=1, cat="evidentiality", lang="Cuzco Quechua",
   value="conjectural", cit="cuzco quechua", tmpl=QCU_T, tb="direct", ta="conjectural",
   nb=QCU_N["direct"], na=QCU_N["conjectural"], site=QCU_SITE,
   fid="INVENTED SCENARIO, as t5-r01-qcu-direct. GLOSS-N follows Faller's gloss of -cha, "
       "'reasoning'."),

 P(id="t5-r01-tur-direct", row=1, cat="evidentiality", lang="Turkish", value="direct",
   cit="turkish-evid", tmpl=TURA_T, tb="indirect", ta="direct",
   nb=TURA_N["indirect"], na=TURA_N["direct"], site=TUR_SITE,
   fid="Content stays in the attested come/arrive domain (WALS ch. 77 ex. (8) 'Ahmet "
       "gel-di' / 'Ahmet gel-mis'); the inspector framing is invented."),
 P(id="t5-r01-tur-indirect", row=1, cat="evidentiality", lang="Turkish", value="indirect",
   cit="turkish-evid", tmpl=TURB_T, tb="direct", ta="indirect",
   nb=TURB_N["direct"], na=TURB_N["indirect"], site=TUR_SITE,
   fid="A second come/arrive scenario is used so that the two Turkish pairs are not exact "
       "inverses of one another on one text; the teacher framing is invented."),

 # --- row 2, Perfective / imperfective aspect -------------------------------
 P(id="t5-r02-rus", row=2, cat="perfective/imperfective", lang="Russian", value=None,
   cit="russian",
   tmpl="The long fence along the yard needed attention. He painted it on Saturday {TAG}. "
        "The paint store on the corner is closed until the tenth.",
   tb="unbounded", ta="bounded",
   nb="The long fence along the yard needed attention. He was painting it right through "
      "Saturday. The paint store on the corner is closed until the tenth.",
   na="The long fence along the yard needed attention. He painted the whole of it on "
      "Saturday and finished. The paint store on the corner is closed until the tenth.",
   site="Only the marked clause's presentation of the painting -- under way, or carried to "
        "its endpoint -- changes; the surrounding sentences are held.",
   fid="INVENTED SCENARIO. WALS 65A-rus codes the category as grammatically marked and "
       "cites Dahl 1985: 172 but the datapoint carries no glossed example; the fence "
       "scenario is invented and mundane."),
 P(id="t5-r02-mnd", row=2, cat="perfective/imperfective", lang="Mandarin", value=None,
   cit="mandarin-aspect",
   tmpl="The letter to the supplier was overdue. She wrote it yesterday {TAG}. Anyone with "
        "additions should speak to her before the post goes out.",
   tb="unbounded", ta="bounded",
   nb="The letter to the supplier was overdue. She was writing it through yesterday. Anyone "
      "with additions should speak to her before the post goes out.",
   na="The letter to the supplier was overdue. She wrote it right out yesterday and it is "
      "done. Anyone with additions should speak to her before the post goes out.",
   site="Only the marked clause's presentation of the writing -- under way, or carried to "
        "its endpoint -- changes; the surrounding sentences are held.",
   fid="INVENTED SCENARIO. WALS 65A-mnd codes the category as grammatically marked and "
       "cites Dahl 1985: 180 but the datapoint carries no glossed example."),

 # --- row 3, Optative -------------------------------------------------------
 P(id="t5-r03-geo", row=3, cat="optative", lang="Georgian", value=None, cit="georgian",
   tmpl="This is the closing line of the letter to the departing steward. You find the new "
        "post easier than this one {TAG}. The household will send word at the end of the "
        "month.",
   tb="statement", ta="wish",
   nb="This is the closing line of the letter to the departing steward. You find the new "
      "post easier than this one. The household will send word at the end of the month.",
   na="This is the closing line of the letter to the departing steward. May you find the "
      "new post easier than this one. The household will send word at the end of the month.",
   site="Only the marked clause changes between saying how things stand and voicing a wish "
        "about how they should turn out; the surrounding sentences are held.",
   fid="INVENTED SCENARIO. WALS 73A-geo carries glossed example igt-1576 "
       "(mo-g-sl-od-e-t, optative) but its content was not obtainable from the attestation "
       "record, so the farewell scenario is invented and mundane."),
 P(id="t5-r03-grc", row=3, cat="optative", lang="Ancient Greek", value=None,
   cit="ancient greek",
   tmpl="These are the words a father speaks to his young son before he goes. You are more "
        "fortunate than your father {TAG}. The household will keep the small room ready for "
        "him.",
   tb="statement", ta="wish",
   nb="These are the words a father speaks to his young son before he goes. You are more "
      "fortunate than your father. The household will keep the small room ready for him.",
   na="These are the words a father speaks to his young son before he goes. May you be more "
      "fortunate than your father. The household will keep the small room ready for him.",
   site="Only the marked clause changes between saying how things stand and voicing a wish "
        "about how they should turn out; the surrounding sentences are held.",
   fid="Content is the named published example itself, Sophocles, Ajax 550, a father's wish "
       "that his son fare better than he did (Smyth 1920 section 1814); only the framing "
       "sentences around it are invented."),

 # --- row 4, Middle voice ---------------------------------------------------
 P(id="t5-r04-grc", row=4, cat="middle voice", lang="Classical Greek", value=None,
   cit="classical greek",
   tmpl="From the morning notice at the training ground. Before the third hour he prepares "
        "{TAG}. The gate is shut at the fourth hour and is not opened again.",
   tb="active", ta="middle",
   nb="From the morning notice at the training ground. Before the third hour he prepares "
      "the gear for the others. The gate is shut at the fourth hour and is not opened again.",
   na="From the morning notice at the training ground. Before the third hour he prepares "
      "himself. The gate is shut at the fourth hour and is not opened again.",
   site="Only the marked clause changes between the subject acting on something else and "
        "the subject being the seat of the event; the surrounding sentences are held.",
   fid="COMPROMISE. Kemmer 1993 attests the inflectional middle for Classical Greek (p. 249, "
       "-mai) and gives 'pete-sthai' 'fly' at p. 57, but 'fly' is middle-only and admits no "
       "active/middle minimal pair; a self-preparation verb is used instead, which is "
       "Kemmer's own middle semantic type. The training-ground scenario is invented."),
 P(id="t5-r04-ful", row=4, cat="middle voice", lang="Fula", value=None, cit="fula",
   tmpl="Note left at the water point. At first light he looks {TAG}. The pump handle is "
        "stiff until the sun is up.",
   tb="active", ta="middle",
   nb="Note left at the water point. At first light he looks the animals over. The pump "
      "handle is stiff until the sun is up.",
   na="Note left at the water point. At first light he looks himself over. The pump handle "
      "is stiff until the sun is up.",
   site="Only the marked clause changes between the subject acting on something else and "
        "the subject being the seat of the event; the surrounding sentences are held.",
   fid="Content keeps Kemmer's own attested Fula example verb, 'ndaar-t-o' 'look at oneself' "
       "(Kemmer 1993: 26); the water-point framing is invented."),

 # --- row 7, Numeral classifiers -------------------------------------------
 P(id="t5-r07-mnd", row=7, cat="numeral classifiers", lang="Mandarin", value=None,
   cit="mandarin-clf",
   tmpl="Two {TAG} fish came in with the morning delivery. They are on the middle shelf "
        "until the kitchen collects them. Nothing else is expected before Friday.",
   tb="long-thin", ta="chunk",
   nb="Two whole fish came in with the morning delivery. They are on the middle shelf until "
      "the kitchen collects them. Nothing else is expected before Friday.",
   na="Two cuts of fish came in with the morning delivery. They are on the middle shelf "
      "until the kitchen collects them. Nothing else is expected before Friday.",
   site="Only the counting word in the first sentence changes; the surrounding sentences "
        "are held.",
   fid="INVENTED SCENARIO. WALS 55A-mnd codes the category 'Obligatory' but carries no "
       "source reference and no glossed example at all (T5_ATTEST section 4.7); the choice "
       "of counting words and the delivery scenario are both invented."),
 P(id="t5-r07-jpn", row=7, cat="numeral classifiers", lang="Japanese", value=None,
   cit="japanese-clf",
   tmpl="Two {TAG} dogs were brought to the gate this morning. The keeper has put them in "
        "the far pen. They will be moved once the paperwork comes through.",
   tb="small-animal", ta="large-animal",
   nb="Two small dogs were brought to the gate this morning. The keeper has put them in the "
      "far pen. They will be moved once the paperwork comes through.",
   na="Two large dogs were brought to the gate this morning. The keeper has put them in the "
      "far pen. They will be moved once the paperwork comes through.",
   site="Only the counting word in the first sentence changes; the surrounding sentences "
        "are held.",
   fid="INVENTED SCENARIO. WALS 55A-jpn codes the category 'Obligatory' but carries no "
       "source reference and no glossed example (T5_ATTEST section 4.7); the choice of "
       "counting words and the kennel scenario are both invented."),
 P(id="t5-r07-yct", row=7, cat="numeral classifiers", lang="Yucatec", value=None,
   cit="yucatec",
   tmpl="Two {TAG} birds were brought to the stall at first light. The price is chalked on "
        "the board by the scales. Nothing is held back for the afternoon.",
   tb="animate", ta="inanimate",
   nb="Two live birds were brought to the stall at first light. The price is chalked on the "
      "board by the scales. Nothing is held back for the afternoon.",
   na="Two birds already plucked for the pot were brought to the stall at first light. The "
      "price is chalked on the board by the scales. Nothing is held back for the afternoon.",
   site="Only the counting word in the first sentence changes; the surrounding sentences "
        "are held.",
   fid="INVENTED SCENARIO. WALS 55A-yct codes the category 'Obligatory' and cites Suarez "
       "1983b: 88, but the datapoint carries no glossed example; the animate/inanimate "
       "contrast and the market scenario are supplied by the author."),

 # --- row 8, Egophoricity ---------------------------------------------------
 P(id="t5-r08-new", row=8, cat="egophoricity", lang="Kathmandu Newar", value=None,
   cit="kathmandu newar",
   tmpl="Transcript from the front desk. The ache in the left shoulder began before first "
        "light {TAG}. The nurse has written the hour on the sheet and the doctor will look "
        "at it after rounds.",
   tb="self", ta="other",
   nb="Transcript from the front desk. My left shoulder began aching before first light. "
      "The nurse has written the hour on the sheet and the doctor will look at it after "
      "rounds.",
   na="Transcript from the front desk. His left shoulder began aching before first light. "
      "The nurse has written the hour on the sheet and the doctor will look at it after "
      "rounds.",
   site="Only the marked clause changes between the speaker being the one with access to "
        "the condition described and someone else being that one; the surrounding sentences "
        "are held.",
   fid="Content is in Hargreaves's own domain for this instance -- privileged access to an "
       "inner condition, the chapter's own subject -- but the clinic scenario is invented."),
 P(id="t5-r08-akv", row=8, cat="egophoricity", lang="Akhvakh", value=None, cit="akhvakh",
   tmpl="Note left on the workshop bench. The gate was latched last night {TAG}. Nothing "
        "else was touched and the key is back in the tin.",
   tb="self", ta="other",
   nb="Note left on the workshop bench. I latched the gate last night. Nothing else was "
      "touched and the key is back in the tin.",
   na="Note left on the workshop bench. Someone else latched the gate last night. Nothing "
      "else was touched and the key is back in the tin.",
   site="Only the marked clause changes between the speaker being the one who brought the "
        "event about and someone else being that one; the surrounding sentences are held.",
   fid="INVENTED SCENARIO, but authored into the cell Creissels 2008 attests the contrast "
       "for: a positive perfective declarative. The workshop framing is invented."),
 P(id="t5-r08-tsa", row=8, cat="egophoricity", lang="Tsafiki", value=None, cit="tsafiki",
   tmpl="Transcript, second day. The canoe was pulled up above the flood line {TAG}. The "
        "rope is tied to the same post as before.",
   tb="self", ta="other",
   nb="Transcript, second day. I pulled the canoe up above the flood line. The rope is tied "
      "to the same post as before.",
   na="Transcript, second day. He pulled the canoe up above the flood line. The rope is "
      "tied to the same post as before.",
   site="Only the marked clause changes between the speaker being the one who brought the "
        "event about and someone else being that one; the surrounding sentences are held.",
   fid="INVENTED SCENARIO. The Tsafiki instance is a substitute source whose content claim "
       "rests on Dickinson 2000/2002 being what the named volume cites for the language; no "
       "example domain was carried into the item."),

 # --- row 9, Switch-reference -----------------------------------------------
 P(id="t5-r09-ame", row=9, cat="switch-reference", lang="Amele", value=None, cit="amele",
   tmpl="The pig broke out of the pen before dawn {TAG} and went down to the river. The "
        "fence at the low corner has been mended since, and the gate is kept barred at "
        "night.",
   tb="same-subject", ta="different-subject",
   nb="The pig broke out of the pen before dawn and went down to the river itself. The "
      "fence at the low corner has been mended since, and the gate is kept barred at night.",
   na="The pig broke out of the pen before dawn and the men went down to the river after "
      "it. The fence at the low corner has been mended since, and the gate is kept barred "
      "at night.",
   site="Only the marked clause's statement about whether the next clause has the same "
        "subject changes; the surrounding sentences are held.",
   fid="Content stays in the pig-and-men domain of Roberts's canonical Amele example; the "
       "fence framing is invented."),
 P(id="t5-r09-cho", row=9, cat="switch-reference", lang="Choctaw", value=None, cit="choctaw",
   tmpl="The driver signed the sheet at the desk {TAG} and then went round to the side "
        "door. The bill is on the spike by the till.",
   tb="same-subject", ta="different-subject",
   nb="The driver signed the sheet at the desk and then went round to the side door "
      "himself. The bill is on the spike by the till.",
   na="The driver signed the sheet at the desk and then the storekeeper went round to the "
      "side door. The bill is on the spike by the till.",
   site="Only the marked clause's statement about whether the next clause has the same "
        "subject changes; the surrounding sentence is held.",
   fid="INVENTED SCENARIO. The Choctaw instance is a substitute source (Davies 1984); no "
       "example domain was carried into the item."),
 P(id="t5-r09-diy", row=9, cat="switch-reference", lang="Diyari", value=None, cit="diyari",
   tmpl="The old man got up from the fire {TAG} and walked out to the waterhole. The billy "
        "was left on the coals and the dogs stayed where they were.",
   tb="same-subject", ta="different-subject",
   nb="The old man got up from the fire and walked out to the waterhole himself. The billy "
      "was left on the coals and the dogs stayed where they were.",
   na="The old man got up from the fire and the boy walked out to the waterhole. The billy "
      "was left on the coals and the dogs stayed where they were.",
   site="Only the marked clause's statement about whether the next clause has the same "
        "subject changes; the surrounding sentence is held.",
   fid="INVENTED SCENARIO. The Diyari instance is a substitute source (Austin 1981); no "
       "example domain was carried into the item."),

 # --- row 11, Honorifics / social deixis ------------------------------------
 P(id="t5-r11-jpn", row=11, cat="honorifics", lang="Japanese", value=None, cit="japanese-hon",
   tmpl="Message left at the desk. Come to the third floor before the meeting begins {TAG}. "
        "The room has been changed to the one at the end of the corridor.",
   tb="plain", ta="exalted",
   nb="Message left at the desk. You are asked to come to the third floor before the "
      "meeting begins. The room has been changed to the one at the end of the corridor.",
   na="Message left at the desk. The section head is asked to come to the third floor "
      "before the meeting begins. The room has been changed to the one at the end of the "
      "corridor.",
   site="Only the form used to address the reader changes between a plain one and an "
        "elevated one; the request itself and the surrounding sentence are held.",
   fid="Content follows the coded value itself -- WALS 45A-jpn is 'Pronouns avoided for "
       "politeness', so the elevated version replaces the second-person word with a title. "
       "The office scenario is invented."),
 P(id="t5-r11-kor", row=11, cat="honorifics", lang="Korean", value=None, cit="korean",
   tmpl="Notice pinned by the stairs. Bring the signed form to the office by Friday {TAG}. "
        "Forms left after Friday will be held until the following week.",
   tb="plain", ta="exalted",
   nb="Notice pinned by the stairs. You are asked to bring the signed form to the office "
      "by Friday. Forms left after Friday will be held until the following week.",
   na="Notice pinned by the stairs. The teacher is asked to bring the signed form to the "
      "office by Friday. Forms left after Friday will be held until the following week.",
   site="Only the form used to address the reader changes between a plain one and an "
        "elevated one; the request itself and the surrounding sentence are held.",
   fid="Content follows the coded value itself -- WALS 45A-kor is 'Pronouns avoided for "
       "politeness'. The school scenario is invented."),

 # --- row 12, Mirativity ----------------------------------------------------
 P(id="t5-r12-tur", row=12, cat="mirativity", lang="Turkish", value=None, cit="turkish-mir",
   tmpl="Note passed along at the recital. Your daughter plays the piano very well {TAG}. "
        "The second half begins in ten minutes.",
   tb="expected", ta="surprise",
   nb="Note passed along at the recital. Your daughter plays the piano very well, as I have "
      "always said. The second half begins in ten minutes.",
   na="Note passed along at the recital. Your daughter plays the piano very well -- I had "
      "no idea! The second half begins in ten minutes.",
   site="Only the marked clause changes between fitting what the speaker already held and "
        "running against it; the surrounding sentence is held.",
   fid="Content is DeLancey's own flagship example, 'Your daughter plays piano very well!' "
       "(1997: 38); the recital framing is invented."),
 P(id="t5-r12-har", row=12, cat="mirativity", lang="Hare", value=None, cit="hare",
   tmpl="Note left at the trail head. A bear has been walking about here {TAG}. The bins at "
        "the second camp are to be kept shut from now on.",
   tb="expected", ta="surprise",
   nb="Note left at the trail head. A bear has been walking about here, as one does every "
      "year at this season. The bins at the second camp are to be kept shut from now on.",
   na="Note left at the trail head. So a bear has been walking about here after all. The "
      "bins at the second camp are to be kept shut from now on.",
   site="Only the marked clause changes between fitting what the speaker already held and "
        "running against it; the surrounding sentence is held.",
   fid="Content is DeLancey's own Hare example, 'I see there was a bear walking around "
       "here' (1997: 38); the trail-head framing is invented."),
 P(id="t5-r12-mgp", row=12, cat="mirativity", lang="Magar", value=None, cit="magar",
   tmpl="Note from the upper field. The spring above the terrace is running again {TAG}. "
        "The channel to the lower plots has been opened.",
   tb="expected", ta="surprise",
   nb="Note from the upper field. The spring above the terrace is running again, just as it "
      "does after the first rains. The channel to the lower plots has been opened.",
   na="Note from the upper field. So the spring above the terrace is running again -- it "
      "had been dry for two seasons. The channel to the lower plots has been opened.",
   site="Only the marked clause changes between fitting what the speaker already held and "
        "running against it; the surrounding sentence is held.",
   fid="INVENTED SCENARIO. The Magar instance is a substitute source whose specific "
       "morphemes are UNVERIFIED at the primary (T5_ATTEST section 2.2 #31); no example "
       "domain was carried into the item."),

 # --- row 13, Associated motion --------------------------------------------
 P(id="t5-r13-aer", row=13, cat="associated motion", lang="Arrernte", value=None,
   cit="arrernte",
   tmpl="Note left at the camp. She gathered the wood by the creek {TAG}. The fire will be "
        "banked before dark as usual.",
   tb="come-and-do", ta="do-while-going",
   nb="Note left at the camp. She came in to the creek and gathered the wood there. The "
      "fire will be banked before dark as usual.",
   na="Note left at the camp. She gathered the wood by the creek as she went along. The "
      "fire will be banked before dark as usual.",
   site="Only the marked clause's account of the travel that went with the gathering "
        "changes; the surrounding sentence is held.",
   fid="INVENTED SCENARIO. Koch's chapter is attested for Arrernte by in-volume page "
       "location only; no glossed example was obtainable, so the camp scenario is invented."),
 P(id="t5-r13-cav", row=13, cat="associated motion", lang="Cavinena", value=None,
   cit="cavinena",
   tmpl="Note for the second boat. He checked the trap at the bend {TAG}. The line above "
        "the falls has not been touched since Tuesday.",
   tb="go-and-do", ta="do-while-going",
   nb="Note for the second boat. He went out to the bend and checked the trap there. The "
      "line above the falls has not been touched since Tuesday.",
   na="Note for the second boat. He checked the trap at the bend as he went past on his "
      "way. The line above the falls has not been touched since Tuesday.",
   site="Only the marked clause's account of the travel that went with the checking "
        "changes; the surrounding sentence is held.",
   fid="Content follows the attested Cavinena paradigm directly: ba-ti- 'go and see O' "
       "against ba-aje- 'see O while going' (Guillaume & Koch 2021: 4, ex. 1), rendered as "
       "checking rather than seeing; the river framing is invented."),

 # --- row 14, Definiteness --------------------------------------------------
 P(id="t5-r14-ara", row=14, cat="definiteness", lang="Arabic (Modern Standard)", value=None,
   cit="arabic",
   tmpl="Notice at the yard gate. Bring {TAG} key to the office before you leave. The "
        "office closes at six and does not open again until Monday.",
   tb="definite", ta="indefinite",
   nb="Notice at the yard gate. Bring the key to the office before you leave. The office "
      "closes at six and does not open again until Monday.",
   na="Notice at the yard gate. Bring a key to the office before you leave. The office "
      "closes at six and does not open again until Monday.",
   site="Only the marking on the noun phrase in the second sentence changes; the "
        "surrounding sentences are held.",
   fid="INVENTED SCENARIO. WALS 37A-ams codes 'Definite affix' and cites Cowan 1958: 9 but "
       "carries no glossed example; the yard scenario is invented."),
 P(id="t5-r14-hun", row=14, cat="definiteness", lang="Hungarian", value=None, cit="hungarian",
   tmpl="Message for the caretaker. {TAG} ladder has been left against the wall of the "
        "shed. Please put it back in the store before the rain comes.",
   tb="definite", ta="indefinite",
   nb="Message for the caretaker. The ladder has been left against the wall of the shed. "
      "Please put it back in the store before the rain comes.",
   na="Message for the caretaker. A ladder has been left against the wall of the shed. "
      "Please put it back in the store before the rain comes.",
   site="Only the marking on the noun phrase in the second sentence changes; the "
        "surrounding sentences are held.",
   fid="INVENTED SCENARIO. WALS 37A-hun codes 'Definite word distinct from demonstrative' "
       "and cites Kenesei et al. 1998: 94 but carries no glossed example."),
]

# ---------------------------------------------------------------------------
# THE 12 TAG-NULL CONTROL ITEMS (MAJOR-12), rows 1 and 7 only, 3 languages each
#   pair type alpha -- tag byte-identical, surrounding text reworded
#   pair type beta  -- tag moves to another value of the same category, text held
# ---------------------------------------------------------------------------
ALPHA_SITE = ("The bracketed tag is held byte-identical while the surrounding sentences are "
              "reworded to say the same thing in different words.")
BETA_SITE = ("The bracketed tag moves to a different value of the same category while every "
             "other byte of the passage is held.")

TAGNULL = [
 P(id="tn-r01-tuy-alpha", row=1, cat="evidentiality", lang="Tuyuca", pair_type="alpha",
   before="The rain held off until the evening [EVID:visual]. The path along the bank is "
          "passable again.",
   after="It did not rain until the evening [EVID:visual]. The bank path can be walked "
         "again.",
   tb="visual", ta="visual", site=ALPHA_SITE),
 P(id="tn-r01-tuy-beta", row=1, cat="evidentiality", lang="Tuyuca", pair_type="beta",
   tmpl="The nets were taken up before the water rose {TAG}. They are stacked under the "
        "shelter by the steps.",
   tb="nonvisual", ta="apparent", site=BETA_SITE),
 P(id="tn-r01-qcu-alpha", row=1, cat="evidentiality", lang="Cuzco Quechua", pair_type="alpha",
   before="The bread came out of the oven late this morning [EVID:direct]. There is enough "
          "for every house on the row.",
   after="This morning the bread was late out of the oven [EVID:direct]. Every house on the "
         "row can be supplied.",
   tb="direct", ta="direct", site=ALPHA_SITE),
 P(id="tn-r01-qcu-beta", row=1, cat="evidentiality", lang="Cuzco Quechua", pair_type="beta",
   tmpl="The upper channel was cleared on Monday {TAG}. Water reached the last plot by "
        "evening.",
   tb="reportative", ta="conjectural", site=BETA_SITE),
 P(id="tn-r01-tur-alpha", row=1, cat="evidentiality", lang="Turkish", pair_type="alpha",
   before="The bell was rung twice at noon [EVID:direct]. The gate was opened straight "
          "after.",
   after="At noon the bell rang twice [EVID:direct]. Straight after that, the gate was "
         "opened.",
   tb="direct", ta="direct", site=ALPHA_SITE),
 P(id="tn-r01-tur-beta", row=1, cat="evidentiality", lang="Turkish", pair_type="beta",
   tmpl="The cart left the yard before the rain {TAG}. It is due back the day after "
        "tomorrow.",
   tb="direct", ta="indirect", site=BETA_SITE),

 P(id="tn-r07-mnd-alpha", row=7, cat="numeral classifiers", lang="Mandarin",
   pair_type="alpha",
   before="Three [CLF:long-thin] ropes were issued to the second team. They are signed for "
          "on the sheet by the door.",
   after="The second team was issued three [CLF:long-thin] ropes. The sheet by the door "
         "carries the signature.",
   tb="long-thin", ta="long-thin", site=ALPHA_SITE),
 P(id="tn-r07-mnd-beta", row=7, cat="numeral classifiers", lang="Mandarin", pair_type="beta",
   tmpl="Four {TAG} fish are held back for the evening service. The rest go out with the "
        "midday tray.",
   tb="long-thin", ta="chunk", site=BETA_SITE),
 P(id="tn-r07-jpn-alpha", row=7, cat="numeral classifiers", lang="Japanese",
   pair_type="alpha",
   before="Two [CLF:small-animal] rabbits were handed in at the gate. The keeper has them "
          "in the near hutch.",
   after="At the gate, two [CLF:small-animal] rabbits were handed in. The keeper is holding "
         "them in the near hutch.",
   tb="small-animal", ta="small-animal", site=ALPHA_SITE),
 P(id="tn-r07-jpn-beta", row=7, cat="numeral classifiers", lang="Japanese", pair_type="beta",
   tmpl="Six {TAG} animals went out on the morning van. The sheet is with the driver.",
   tb="small-animal", ta="large-animal", site=BETA_SITE),
 P(id="tn-r07-yct-alpha", row=7, cat="numeral classifiers", lang="Yucatec",
   pair_type="alpha",
   before="Five [CLF:animate] birds were brought to the stall at first light. The price is "
          "chalked on the board.",
   after="At first light, five [CLF:animate] birds arrived at the stall. The board carries "
         "the chalked price.",
   tb="animate", ta="animate", site=ALPHA_SITE),
 P(id="tn-r07-yct-beta", row=7, cat="numeral classifiers", lang="Yucatec", pair_type="beta",
   tmpl="Two {TAG} birds are set aside for the Thursday order. Everything else on the stall "
        "is for today.",
   tb="animate", ta="inanimate", site=BETA_SITE),
]

# ---------------------------------------------------------------------------
# Emit
# ---------------------------------------------------------------------------
def tag(cat, value):
    prefix, vocab = TAG_VOCAB[cat]
    assert value in vocab, (cat, value)
    return "[%s:%s]" % (prefix, value)

def main():
    rows = []
    for it in ITEMS:
        tb, ta = tag(it["cat"], it["tb"]), tag(it["cat"], it["ta"])
        assert it["tmpl"].count("{TAG}") == 1, it["id"]
        rows.append({
            "id": it["id"],
            "row": it["row"],
            "category": it["cat"],
            "language": it["lang"],
            "value": it["value"],
            "citation": CIT[it["cit"]],
            "glossN_before": it["nb"],
            "glossN_after": it["na"],
            "glossT_before": it["tmpl"].replace("{TAG}", tb),
            "glossT_after": it["tmpl"].replace("{TAG}", ta),
            "tag_before": tb,
            "tag_after": ta,
            "category_preamble": PREAMBLE[it["cat"]],
            "variation_site": it["site"],
            "fidelity_note": it["fid"],
        })
    with open(os.path.join(BASE, "t5_items.jsonl"), "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    tn = []
    for it in TAGNULL:
        tb, ta = tag(it["cat"], it["tb"]), tag(it["cat"], it["ta"])
        if it["pair_type"] == "beta":
            assert it["tmpl"].count("{TAG}") == 1, it["id"]
            before = it["tmpl"].replace("{TAG}", tb)
            after = it["tmpl"].replace("{TAG}", ta)
        else:
            before, after = it["before"], it["after"]
        tn.append({
            "id": it["id"],
            "row": it["row"],
            "category": it["cat"],
            "language": it["lang"],
            "pair_type": it["pair_type"],
            "before": before,
            "after": after,
            "tag_before": tb,
            "tag_after": ta,
            "category_preamble": PREAMBLE[it["cat"]],
            "variation_site": it["site"],
        })
    with open(os.path.join(BASE, "t5_tagnull.jsonl"), "w") as f:
        for r in tn:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print("wrote %d pairs, %d tag-null items" % (len(rows), len(tn)))

if __name__ == "__main__":
    main()
