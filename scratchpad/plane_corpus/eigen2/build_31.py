import json, re, os

items = []

def add(kind, dom, amb, diff, before, old, new, site, note, serial=1):
    assert before.count(old) == 1, (kind, "not unique")
    after = before.replace(old, new)
    items.append(dict(
        id=f"e2b31-{kind}{serial}", kind_target=kind, domain=dom,
        ambiguous_with=amb, difficulty=diff, before=before, after=after,
        variation_site=site, author_note=note, part="E2", batch=31))

# 1 axiotic / bulletin / hard
b = ("Lowfield Internal Drainage Board — Autumn Bulletin: Pump Attendance\n\n"
     "Attendants are reminded that the winter roster begins on the first Monday of November, with two "
     "attendants on call each night and a third on standby at the depot. All three callout points remain "
     "in service throughout the season and none has been withdrawn. Where two alarms sound together and "
     "only one attendant is free to travel, the sluice gauge at Marsh End is attended before the culvert "
     "screen at Ninefoot, and the culvert screen before the outfall marker on the tidal cut. An attendant "
     "who reaches a point and finds it sound should log the visit and go on to the next. Fuel dockets go "
     "to the depot clerk on the Friday.")
add("axiotic", "bulletin", "deontic", "hard", b,
    "the sluice gauge at Marsh End is attended before the culvert screen at Ninefoot, and the culvert screen before the outfall marker on the tidal cut",
    "the outfall marker on the tidal cut is attended before the culvert screen at Ninefoot, and the culvert screen before the sluice gauge at Marsh End",
    "The sentence covering two simultaneous alarms with one attendant available is altered.",
    "Every callout point stays in service and nothing becomes forbidden; only what yields to what under contention is reversed, dressed as a board instruction to tempt deontic.")

# 2 deontic / catalogue / clear
b = ("County Herbarium — Catalogue of the Tarred Cabinets, Section D\n\n"
     "Section D holds the coastal collections gathered on the north shore between 1904 and 1931, arranged "
     "by family and then by collector. Sheets are numbered in the top right corner in pencil; the paper "
     "labels are original and should not be lifted. Visiting students may photograph mounted sheets at the "
     "reading bench, provided no sheet leaves the bench and the cabinet door is closed between withdrawals. "
     "The curator holds the key to the two lower drawers, which contain the type material. Enquiries about "
     "loans go to the curator in writing, and a reply is usually sent within a fortnight of the enquiry "
     "reaching the office.")
add("deontic", "catalogue", None, "clear", b,
    "Visiting students may photograph mounted sheets at the reading bench",
    "Visiting students must not photograph mounted sheets at the reading bench",
    "The sentence about students and the reading bench is altered.",
    "A permission becomes a prohibition with no change to what the cabinets hold or how they are described.")

# 3 pragmatic / notice / clear
b = ("Bellmouth Ferry Service — Notice to Foot Passengers\n\n"
     "Passengers are hereby advised that the eight-fifteen sailing will not run on the second and fourth "
     "Wednesdays of the month while the slipway apron is relaid. A replacement minibus departs the harbour "
     "office at eight o'clock and reaches the far shore by the usual time. Tickets already purchased remain "
     "valid on the minibus and no refund need be sought. Passengers with pushchairs should board at the "
     "front door, where the step is lower. The works are expected to finish before the end of March, after "
     "which the ordinary timetable resumes without further notice being given at the office.")
add("pragmatic", "notice", None, "clear", b,
    "Passengers are hereby advised that",
    "We are just letting everyone know that",
    "The opening clause of the notice is altered.",
    "Register drops from formal to conversational while the sailing, the minibus and the dates stay identical.")

# 4 ontological / handbook / clear
b = ("Upland Bothy Association — Handbook, Entry 12: Glenmorrow\n\n"
     "Glenmorrow stands at the head of the western glen, an hour above the forestry gate, with a stone "
     "floor, two sleeping platforms and a chimney that draws well in a north wind. The building is held by "
     "the association as a bothy. Users carry out what they carry in; there is no warden and nothing is "
     "booked in advance. The roof was relaid in the year of the last survey and the gable repointed the "
     "following summer. Water comes from the burn thirty paces east of the door. The nearest telephone is "
     "at the forestry gate, and the track beyond it is unmetalled for two miles.")
add("ontological", "handbook", None, "clear", b,
    "as a bothy",
    "as a shared bunkhouse",
    "The sentence stating how the association holds the building is altered.",
    "The same stone building is reassigned to a different class of accommodation; usage terms, condition and location are untouched.")

# 5 epistemic / log / clear
b = ("Netherby Waterworks — Duty Log, 14 February\n\n"
     "Night duty. Pressure at the high reservoir fell by four metres between two and three in the morning "
     "and recovered when the booster was switched to the second pump. The fall was caused by an airlock in "
     "the rising main above the old crossing. No customer calls were taken overnight. The booster ran on "
     "the second pump until the morning shift, when the first pump was returned to service and held steady "
     "for two hours under observation. Chlorine residual was within band at every sample point. Handover to "
     "the day fitter at seven, with a note left on the board for the inspector.")
add("epistemic", "log", None, "clear", b,
    "was caused by an airlock",
    "was probably down to an airlock",
    "The sentence attributing the overnight pressure drop is altered.",
    "The stated cause is unchanged; only how firmly the log commits to it moves.")

# 6 empirical / policy / hard
b = ("Harbour Commissioners — Policy Statement on Night Movements\n\n"
     "This statement explains how the commissioners apply the existing controls on movements after dark and "
     "does not alter them. Byelaw 14, made in 1968 and confirmed by the department the following year, "
     "forbids vessels over twelve metres from entering the inner basin between sunset and sunrise without a "
     "pilot aboard. The commissioners will continue to publish the pilot roster a week in advance and to "
     "charge the standard boarding fee. Skippers who arrive after dark and cannot obtain a pilot should lie "
     "at the outer buoys until first light. Nothing here creates any new obligation on skippers or on the "
     "pilotage service.")
add("empirical", "policy", "deontic", "hard", b,
    "made in 1968 and confirmed by the department the following year",
    "made in 1974 and confirmed by the department the same year",
    "The clause describing the byelaw's making and confirmation is altered.",
    "What the byelaw forbids is word-for-word intact; only the historical claim about when it was made and confirmed moves, so the byelaw setting tempts deontic.")

# 7 contingent / report / clear
b = ("Estuary Bird Count — Report of the January Low-Water Count\n\n"
     "The count was made on the morning of the spring tide in fair visibility with a light southerly. "
     "Observers worked in two pairs, one on the saltings and one on the shingle spit. The main flock of "
     "waders was counted from the eastern hide as it lifted off the mud and settled again nearer the "
     "channel. Totals were reconciled at the boathouse over an hour and entered on the county form the same "
     "evening. No birds were ringed and no nets were set. The next count falls on the following spring "
     "tide, and the same pairs have offered to work it if the weather holds.")
add("contingent", "report", None, "clear", b,
    "eastern hide",
    "sea-wall hide",
    "The sentence describing where the main wader flock was counted is altered.",
    "An unbound detail of this occasion swaps to the other hide; no requirement, definition or claim about the birds changes.")

# 8 procedural / config / hard
b = ("Depot Weighbridge — Terminal Settings Sheet\n\n"
     "This sheet gives the settings applied to the weighbridge terminal after each power failure, taken "
     "from the fitter's card in the office drawer. The terminal is brought up as follows: the tare is "
     "cleared, then the ticket printer is put online, then the date and time are entered from the office "
     "clock, then the load cells are read once with the deck empty. Baud rate stays at nine thousand six "
     "hundred and the parity bit is left off. The office copy of this sheet is kept in the drawer with the "
     "fitter's card and is not to be amended by drivers.")
add("procedural", "config", "structural", "hard", b,
    "the tare is cleared, then the ticket printer is put online, then the date and time are entered from the office clock, then the load cells are read once with the deck empty",
    "the load cells are read once with the deck empty, then the date and time are entered from the office clock, then the ticket printer is put online, then the tare is cleared",
    "The bring-up sequence for the terminal is altered.",
    "The same four operations in a new order, sitting in a settings document so the encoding-focused neighbour tempts.")

# 9 nomological / process / clear
b = ("Allotment Society — Valuing Sheds on Transfer of a Plot\n\n"
     "When a plot changes hands the outgoing tenant may be paid for any shed, frame or water butt left "
     "standing. The site secretary inspects the items with one committee member present and lists them on "
     "the transfer sheet. Each item is then valued using the straight-line depreciation table printed at "
     "the back of the site book, taking the original cost from the tenant's receipt where one survives and "
     "the committee's estimate where it does not. The figure is shown to both tenants before signature. "
     "Payment passes directly between tenants; the society holds no money and takes no part in any dispute "
     "that follows.")
add("nomological", "process", None, "clear", b,
    "the straight-line depreciation table printed at",
    "the reducing-balance depreciation table printed at",
    "The clause naming what the listed items are valued by is altered.",
    "The inspection, the listing and the payment route are untouched; a different valuation scheme is applied to derive the figure.")

# 10 structural / registry / clear
b = ("Parish Burial Registry — Transcription Conventions\n\n"
     "The working transcript of the older registry is kept as a plain text file on the volunteer's machine "
     "and copied to the parish office each quarter. One grave occupies one line. Each line carries the plot "
     "reference, the surname, the forename, the year of interment and the transcriber's initials, separated "
     "by a comma, with no space after the separator. Where the stone is unreadable a single question mark "
     "stands in for the missing field. Nothing is abbreviated except the initials. The office copy is "
     "printed once a year and bound; the printed copy has never yet been used to settle a query.")
add("structural", "registry", None, "clear", b,
    "by a comma, with no space after the separator",
    "by a vertical bar, with no space after the separator",
    "The clause describing how the fields on a line are divided is altered.",
    "The same five fields in the same order, differently delimited: meaning-preserving to a reader, decisive for anything parsing the file.")

# 11 axiomatic / minutes / clear
b = ("Village Hall Committee — Minutes of the March Meeting, Item 5\n\n"
     "Item 5. The booking schedule. The treasurer noted that several parts of the schedule count in days: "
     "the fourteen days of notice for a cancellation, the seven days allowed for payment of the deposit, "
     "and the three days within which a key must be returned. The committee agreed that throughout the "
     "schedule a working day means Monday to Friday, excluding bank holidays. The secretary will reissue "
     "the schedule with the wording set out at the head of it rather than in a footnote, so that hirers "
     "meet it before the counted periods. Carried, four in favour, none against, one abstention.")
add("axiomatic", "minutes", None, "clear", b,
    "a working day means Monday to Friday, excluding bank holidays",
    "a working day means Monday to Saturday, excluding bank holidays",
    "The agreed wording at the end of the treasurer's item is altered.",
    "A defined term that three counted periods compose over is widened, so every deadline in the schedule shifts without any of them being edited.")

# 12 deontic (extra) / manual / clear
b = ("Town Brass Band — Members' Manual, Section 3: Sectionals\n\n"
     "Sectionals are held on Tuesday evenings in the band room, cornets first and lower brass after the "
     "break, and run from the first week of September to the contest weekend in May. Section leaders must "
     "attend every sectional and account to the bandmaster for any absence. Players are asked to bring "
     "their own pencils and to mark parts lightly. The band room is opened at half past six and locked at "
     "half past nine by whoever holds the key that week. Music stands are counted back onto the rack at the "
     "end of the evening.")
add("deontic", "manual", None, "clear", b,
    "Section leaders must attend every sectional and account to the bandmaster for any absence",
    "Section leaders may attend sectionals as their other commitments allow, and need not tell the bandmaster of an absence",
    "The sentence about section leaders and attendance is altered.",
    "A duty is downgraded to a bare permission; timings, venue and everything else in the section stand.", 2)

BANNED = {"priority","priorities","rule","rules","identity","premise","premises","structure",
          "structural","manner","confidence","circumstance","circumstances","process","model","record"}

problems = []
for it in items:
    b, a = it["before"], it["after"]
    if b == a: problems.append(it["id"] + ": identical")
    n = 0
    while n < min(len(b), len(a)) and b[n] == a[n]: n += 1
    m = 0
    while m < min(len(b), len(a)) - n and b[len(b)-1-m] == a[len(a)-1-m]: m += 1
    ob, oa = b[n:len(b)-m], a[n:len(a)-m]
    if not ob or not oa: problems.append(it["id"] + ": empty span")
    if "\n" in ob or "\n" in oa: problems.append(it["id"] + ": newline in span")
    if b.count(ob) != 1: problems.append(f"{it['id']}: span occurs {b.count(ob)}x")
    wc = len(b.split())
    if not (85 <= wc <= 150): problems.append(f"{it['id']}: wc {wc}")
    for w in re.findall(r"[a-z]+", (ob + " " + oa).lower()):
        if w in BANNED: problems.append(f"{it['id']}: banned word {w}")
    it["_wc"] = wc

print(problems)
for it in items: print(it["id"], it["domain"], it["_wc"])
if not problems:
    for it in items: it.pop("_wc")
    p = "/home/emoore/CIRISOntology/scratchpad/plane_corpus/eigen2/batch_31.jsonl"
    with open(p, "w") as f:
        for it in items: f.write(json.dumps(it, ensure_ascii=False) + "\n")
    print("WROTE", p, len(items))
