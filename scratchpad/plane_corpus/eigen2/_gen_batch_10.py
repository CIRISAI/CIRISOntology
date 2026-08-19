import json, re, os

items = []

def add(idx, kind, domain, amb, diff, before, old, new, site, note):
    assert before.count(old) == 1, (idx, "not unique")
    after = before.replace(old, new)
    items.append(dict(id=idx, kind_target=kind, domain=domain, ambiguous_with=amb,
                      difficulty=diff, before=before, after=after,
                      variation_site=site, author_note=note, part="E2", batch=10))

add("e2b10-axiotic1", "axiotic", "handbook", None, "clear",
"""Fen Drainage Board — Pump Attendance Handbook, Section 6

Attendants on the night watch at the Marsh Lode station keep a standing order of care when two demands arrive together. Where the wet well is rising and the diesel day tank is low, the wet well is served first, and the day tank before the greasing round. Greasing is deferred until both are settled. The attendant enters the sequence in the watch book with times to the nearest five minutes, and the shift foreman initials it at handover. Nothing here alters what an attendant may or may not touch; the switchgear cabinet stays closed to all but the ticketed fitter, whatever the hour, and the board's telephone tree is unchanged.""",
"the wet well is served first, and the day tank before the greasing round",
"the day tank is served first, and the wet well before the greasing round",
"The change lies in the third sentence of the paragraph.",
"Reverses which competing demand is served ahead of which while every permitted action stays the same.")

add("e2b10-deontic1", "deontic", "log", None, "clear",
"""Harbour Slipway — Duty Log, February

Entries for the fortnight are copied from the gatehouse sheet. Tuesday: two trailers launched, both with winter permits shown. Wednesday: cradle inspected, chocks replaced. Thursday: the western slip closed for weed clearance from 0700. Standing instruction as printed at the head of the log: craft over six metres may not be launched single-handed and must have a second person on the warp. Friday: one refusal noted on that account, the owner advised to return with crew. Saturday: gate lamp replaced, bulb from the store. The keeper signs each week's block and forwards a copy to the harbour office by the following Monday.""",
"may not be launched single-handed and must have a second person on the warp",
"may be launched single-handed provided a warp is made fast to the bollard beforehand",
"The change lies in the sentence quoting the printed instruction.",
"Alters what is forbidden versus permitted for large craft, leaving all logged observations untouched.")

add("e2b10-pragmatic1", "pragmatic", "policy", None, "clear",
"""Almshouse Trust — Resident Correspondence Policy

The Trust writes to residents four times a year about repairs, the garden contract, the heating account, and the annual statement. Letters open with 'Dear Resident' and close with 'Yours faithfully, the Clerk to the Trustees'. The content follows the schedule agreed at the spring meeting: the same four headings, the same enclosure of the repairs timetable, and the same telephone number for the maintenance line. Copies go to the two visiting trustees. Where a resident has asked for large print, the office prints at fourteen point and posts rather than emails. Anything needing a decision by the resident carries a reply slip and a stamped envelope.""",
"'Dear Resident' and close with 'Yours faithfully, the Clerk to the Trustees'",
"'Hello there' and close with 'All the best, Marion in the office'",
"The change lies in the second sentence of the paragraph.",
"Shifts salutation and sign-off register while the letters carry exactly the same content.")

add("e2b10-ontological1", "ontological", "report", None, "clear",
"""County Herbarium — Accession Report, Sheet 4412

Sheet 4412 was gathered on the coastal shingle north of Ness Point in late June and mounted the following week. The collector's notes give a yellow-flowered crucifer, the stem bristly towards the base, pods with a long beak, growing above the strandline among sea kale and yellow horned-poppy. Measurements and the gathering date stand as written on the original label and have not been altered. The sheet is filed under Wild Turnip. Duplicate material went to the teaching cabinet under the same accession number with suffix B. The curator checked the mount for beetle damage and found none; the folder was returned to cabinet nine.""",
"The sheet is filed under Wild Turnip.",
"The sheet is filed under Sea Radish.",
"The change lies in the sentence naming the filing determination.",
"Reassigns what the specimen is taken to be, with every observation and measurement preserved.")

add("e2b10-epistemic1", "epistemic", "config", "empirical", "hard",
"""Tide Gauge — Station Configuration Notes, Estuary Board

The instrument at the ferry hard reports every six minutes to the board's collector. Sensor height above the tide board is entered as 3.145 m and the datum offset as -0.271 m. Sampling is set to fifteen-second averaging with a spike filter at four standard deviations. The maintenance comment at the head of the file reads: the datum offset is thought to be good to about two centimetres, pending the next levelling run, so downstream users should treat it as provisional. Alarm thresholds stand as last season. The file is reloaded whenever the collector restarts, and a paper copy is kept in the office drawer.""",
"the datum offset is thought to be good to about two centimetres, pending the next levelling run, so downstream users should treat it as provisional",
"the datum offset is good to two centimetres, settled by the levelling run, and downstream users may take it as final",
"The change lies within the maintenance comment quoted in the file.",
"Hardens a hedge into a settled statement at the same stated tolerance; tempts empirical because a number sits in the span.")

add("e2b10-empirical1", "empirical", "process", None, "clear",
"""Parish Church Clock — Working Method for the Weekly Wind

Two people attend, one winding and one at the foot of the stair with the handset. The stair rises fifty-two steps from the vestry door to the ringing chamber, and a further ladder of nine rungs reaches the clock loft. The winder carries the crank on a shoulder strap and keeps one hand free on the rail. Lighting is by the fixed lamp, with torches carried as backup. The going train is wound first, then the striking train, and the hands are set only where the error exceeds one minute against the telephone signal. The loft door is locked on leaving and the key returned to the vestry board.""",
"fifty-two steps",
"seventy-one steps",
"The change lies in the second sentence of the paragraph.",
"Alters a stated count of the fabric while every instruction and its ordering stands.")

add("e2b10-contingent1", "contingent", "registry", "empirical", "hard",
"""Village Hall Bookings — Standing Register, Autumn Quarter

The register lists recurring hirers, the weekly slot each holds, and the room given them by the caretaker from whatever is free that term. The carpet bowls group meets on Tuesday evenings and is at present allocated the Green Room. The whist drive, the toddler group, and the choir take the remaining evenings on the same footing, the caretaker being free to move any group between rooms so long as the hirer is told a week ahead. Heating is charged at the flat quarterly figure whichever room is used. Keys are lifted from the hook board and signed out in the margin of this register.""",
"allocated the Green Room",
"allocated the Blue Room",
"The change lies in the second sentence of the paragraph.",
"Swaps which interchangeable room this term's slot happens to fall in; tempts empirical because it reads as a stated fact about the hall.")

add("e2b10-procedural1", "procedural", "minutes", None, "clear",
"""Silver Band Committee — Minutes of 3 October, Item 5: Hall Setup

The bandmaster reported on the setup routine for the winter concerts and the committee agreed the following. On arrival the chairs are set out to the marked floor plan, the stands are then placed and numbered, and the percussion is brought in from the van last. Lighting is checked once everything stands in position. Nothing changes as to who may drive the van, which stays restricted to named insured members, nor as to the hall's requirement that the fire exits be kept clear throughout. The treasurer noted no cost falling out of it. Agreed without dissent; the bandmaster to circulate a sheet before the first date.""",
"the chairs are set out to the marked floor plan, the stands are then placed and numbered, and the percussion is brought in from the van last",
"the percussion is brought in from the van first, the chairs are then set out to the marked floor plan, and the stands are placed and numbered last",
"The change lies in the second sentence of the paragraph.",
"Reorders the setup steps while every obligation and reported fact stands unchanged.")

add("e2b10-nomological1", "nomological", "manual", None, "clear",
"""Regional Seed Bank — Viability Estimation, Section 4

Each accession is retested on a fixed cycle and the outcome entered against its number. To fix the retest interval, the technician takes the current germination figure and works the expected storage life from the species constants tabulated in Appendix C, then sets the next test at half that span. Sample size is two hundred seeds where stock allows and one hundred otherwise. Nothing here touches the store conditions, which stay at minus twenty degrees and five per cent moisture, nor the requirement to regenerate any accession falling below eighty-five per cent of its original count. Outcomes go to the curator on the quarterly sheet, with a copy to the duplicate site.""",
"works the expected storage life from the species constants tabulated in Appendix C",
"works the expected storage life by fitting a straight line through the last three germination figures for that accession",
"The change lies in the second sentence of the paragraph.",
"Substitutes which derivation is applied to obtain the retest interval, leaving thresholds and obligations alone.")

add("e2b10-structural1", "structural", "bulletin", "pragmatic", "hard",
"""Ferry Service — Weekly Sailings Bulletin

The bulletin is posted to the pier board each Friday and read onto the answering machine. Departures from the north slip on weekdays are listed as 07:15; 09:45; 12:30; 15:10; 17:40, with the return workings on the line beneath in the same fashion. Sailings marked with an asterisk run on request only and need a call to the office before noon. Tidal restriction applies on the two lowest springs of the month, when the first departure is held until the flood makes. Fares stand as advertised in the spring leaflet. Passengers are asked to be at the slip ten minutes before the advertised time.""",
"07:15; 09:45; 12:30; 15:10; 17:40",
"0715, 0945, 1230, 1510, 1740",
"The change lies in the second sentence of the paragraph.",
"Changes the delimiter and time encoding only; tempts pragmatic because it reads as a presentational tidy-up.")

add("e2b10-axiomatic1", "axiomatic", "catalogue", None, "clear",
"""Museum of Rural Life — Catalogue Conventions, Preface

Throughout this catalogue, a group of objects acquired together and used together is counted as a single entry and given one accession number, with parts told apart by letter suffix. The running totals in each section, the insurance schedule, the shelf labels, and the annual return to the county all follow from that reckoning. Sections are ordered by trade: dairy, harness, hedging, thatch. Photographs are filed to the accession number and not numbered separately. Where provenance is unknown the entry says so plainly rather than guessing at a farm. The preface is reprinted unaltered in each edition unless the trustees direct otherwise at the November meeting.""",
"a group of objects acquired together and used together is counted as a single entry and given one accession number, with parts told apart by letter suffix",
"each object is counted as its own entry and given its own accession number, whether or not it was acquired and used alongside others",
"The change lies in the first sentence of the paragraph.",
"Redefines the counting unit that totals, labels, and the county return all compose over, so the effect ripples.")

add("e2b10-empirical2", "empirical", "notice", None, "clear",
"""Bothy Association — Notice Posted Inside the Door

This shelter is kept up by volunteers and left unlocked all year. The nearest road end lies four miles to the north-west by the stalkers' path, and the burn below the shelter is the only water; boil it. There is no warden here and no telephone signal at the door. Users are asked to carry out all rubbish, to leave dry kindling for the next party, and on no account to burn the fittings. Work parties come twice a year, in April and October, and notice of these is put up at the estate office. Numbers should be kept to six or fewer, and the sleeping platform is not for storage.""",
"four miles to the north-west",
"nine miles to the north-west",
"The change lies in the second sentence of the paragraph.",
"Alters a stated distance about the surrounding ground; no instruction or permission moves.")

BANNED = ["priority","priorities","rule","rules","identity","premise","premises","structure",
          "structural","manner","confidence","circumstance","circumstances","process","model","record"]

problems = []
for it in items:
    b, a = it["before"], it["after"]
    assert b != a
    p = 0
    while p < len(b) and p < len(a) and b[p] == a[p]:
        p += 1
    s = 0
    while s < len(b)-p and s < len(a)-p and b[len(b)-1-s] == a[len(a)-1-s]:
        s += 1
    ob, oa = b[p:len(b)-s], a[p:len(a)-s]
    if "\n" in ob or "\n" in oa:
        problems.append(it["id"]+": newline in span")
    if b.count(ob) != 1:
        problems.append(it["id"]+": span not unique (%d)" % b.count(ob))
    wc = len(b.split())
    if not (85 <= wc <= 150):
        problems.append("%s: wordcount %d" % (it["id"], wc))
    for w in BANNED:
        if re.search(r"\b"+w+r"\b", (ob+" "+oa).lower()):
            problems.append("%s: banned word %s in span" % (it["id"], w))
    print(it["id"], wc, repr(ob[:40]))

print("PROBLEMS:", problems)
if not problems:
    with open("/home/emoore/CIRISOntology/scratchpad/plane_corpus/eigen2/batch_10.jsonl","w") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False)+"\n")
    print("written", len(items))
