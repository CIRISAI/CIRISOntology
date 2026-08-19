import json, re, os

items = []

def add(id, kind, domain, amb, diff, before, old, new, site, note):
    assert before.count(old) == 1, (id, "span count", before.count(old))
    after = before.replace(old, new)
    items.append(dict(id=id, kind_target=kind, domain=domain, ambiguous_with=amb,
                      difficulty=diff, before=before, after=after,
                      variation_site=site, author_note=note, part="E2", batch=29,
                      _old=old, _new=new))

# 1 axiotic / minutes
add("e2b29-axiotic1", "axiotic", "minutes", None, "clear",
"""Tarn Head Slipway Users' Association — Minutes of the Winter Meeting

The harbourmaster's deputy reported that the February tide windows will again be short, and members agreed that loading order on the flat-bed barge should stand as before. Where the window will not hold everything waiting on the quay, mail sacks are taken ahead of livestock crates, and livestock crates ahead of builders' aggregate. Nothing is refused carriage on this account; anything left behind goes on the following sailing at no extra charge. The deputy noted that no member had been left waiting more than two sailings since October. The meeting also thanked the two members who repainted the tide board and agreed to buy a second mooring line before Easter.""",
"mail sacks are taken ahead of livestock crates, and livestock crates ahead of builders' aggregate",
"builders' aggregate is taken ahead of livestock crates, and livestock crates ahead of mail sacks",
"The change falls in the sentence describing loading on the flat-bed barge during a short tide window.",
"Reverses the loading precedence while every consignment remains carried, so only what-beats-what moves."),

# 2 deontic / manual
add("e2b29-deontic1", "deontic", "manual", None, "clear",
"""Glen Ardach Bothy Association — Warden's Manual, Section 6: Stove Ash

Ash accumulates faster in the shoulder seasons, when the stove is lit for warmth rather than cooking, and wardens should expect to clear the pan on most visits. Ash may be tipped on the scree slope below the gable once it has gone cold. Wardens are asked to note the date of clearing on the card behind the door so that the next visitor knows how long the pan has stood. The association supplies a galvanised pail and a short-handled scoop, both kept in the porch. Wardens who find the scoop missing should mention it in the visitors' book rather than improvising with the fire iron.""",
"Ash may be tipped on the scree slope below the gable once it has gone cold.",
"Ash must be carried out in the sealed tin and never tipped on the scree slope below the gable.",
"The change falls in the sentence dealing with disposal of cold ash.",
"Turns a permission into an obligation with a prohibition attached; the described activity is otherwise unchanged."),

# 3 pragmatic / bulletin HARD amb structural
add("e2b29-pragmatic1", "pragmatic", "bulletin", "structural", "hard",
"""Netherby Brass Band — Members' Bulletin, Third Quarter

Members are hereby advised that the Tuesday sectional will move to the chapel hall for six weeks from the fourteenth, the bandroom roof being under repair. Instruments may be left in the bandroom lockers as usual, but the librarian asks that parts for the contest set be taken home rather than stored loose. The percussion trailer will be towed to the chapel on the Monday evening and returned each Thursday. Anyone unable to reach the chapel hall by public transport should speak to the secretary, who is keeping a list of members willing to share a car. Subscriptions for the autumn term fall due at the end of the month.""",
"Members are hereby advised that",
"Quick note for everyone:",
"The change falls at the opening of the paragraph.",
"Shifts the register from formal circular to informal address while the announced content stays identical; tempting as an encoding change."),

# 4 ontological / catalogue HARD amb empirical
add("e2b29-ontological1", "ontological", "catalogue", "empirical", "hard",
"""County Herbarium — Accession Catalogue, Sheet 4417

Collected on the north face of Sheep Crag at 640 metres, in flush ground beside a spring, and pressed the same evening. The sheet is filed under Carex nigra, following the determination made when the material was first mounted. The label records a wet season and a single flowering culm; the collector's field notebook, held separately, gives the grid reference to eight figures. The sheet is in good order apart from foxing at the lower left corner, and has been rehoused in acid-free paper. Loans to visiting workers are handled through the curator, who asks for four weeks' notice and returns sheets by courier only.""",
"filed under Carex nigra",
"filed under Carex bigelowii",
"The change falls in the sentence giving the sheet's filing determination.",
"Reassigns the specimen's taxon; tempting as a factual correction because the surrounding text reads as field description."),

# 5 epistemic / notice
add("e2b29-epistemic1", "epistemic", "notice", None, "clear",
"""Fenside Drainage Board — Notice to Occupiers, Mill Drove Culvert

Following the storm of the eleventh, the culvert beneath Mill Drove has been inspected from the downstream headwall. The inspector's report indicates that the invert is probably obstructed by silt and root material along the middle third of its length. Occupiers should expect standing water in the adjoining dyke after heavy rain until clearance work is carried out. A jetting contractor has been asked to quote, and the board expects work to begin before the end of the flood season. Access will be taken from the field gate on the south side, and the board will make good any rutting caused by plant crossing the headland.""",
"indicates that the invert is probably obstructed",
"establishes that the invert is obstructed",
"The change falls in the sentence reporting the inspector's finding about the invert.",
"Removes the hedge and raises certainty while the obstruction claim itself is unaltered."),

# 6 empirical / handbook
add("e2b29-empirical1", "empirical", "handbook", None, "clear",
"""Cairnwell Allotment Society — Plot Holders' Handbook, Water Supply

The society's supply comes from the bore at the top of the site and is pumped to the two header tanks behind the trading hut. In a dry August the bore yields about 300 litres an hour, which is why hosepipes are discouraged in the late afternoon when several plots draw at once. Watering cans may be filled at either tank without restriction. The pump is serviced each March and the filter cartridge changed at the same visit. Plot holders who find a tank empty should tell the site secretary rather than attempting to prime the pump themselves, as the foot valve is easily damaged.""",
"yields about 300 litres an hour",
"yields about 180 litres an hour",
"The change falls in the sentence describing the bore's dry-season output.",
"Alters a measured quantity about the world; permissions and procedures around it are untouched."),

# 7 contingent / log
add("e2b29-contingent1", "contingent", "log", None, "clear",
"""Sandhaven Depot — Vehicle Movements Log, Tuesday

The long-wheelbase van was signed out at 07:40 by the morning fitter and returned at 15:05 with the fuel card receipt clipped to the sheet. On return it was parked in bay four, the tailgate ramp folded and the battery isolator left on as usual. The tyre pressures were checked before departure and again on return, both within tolerance. A cracked nearside indicator lens was noted and a replacement ordered from the factor. The van is booked out again on Thursday for the coastal round, and the fitter has asked that the load bay be swept before then, the last run having carried loose grit.""",
"parked in bay four",
"parked in bay seven",
"The change falls in the sentence describing where the vehicle was left on return.",
"Swaps one unbound instance detail for another with no obligation, claim, or classification affected."),

# 8 procedural / policy
add("e2b29-procedural1", "procedural", "policy", None, "clear",
"""Wraycote Village Hall Committee — Closing Down the Hall

Whoever holds the key at the end of an evening booking works through the closing sequence on the laminated card by the meter cupboard. The steps run: drain the water heater, then switch off the immersion at the isolator, then take the meter reading and enter it in the book. After that the shutters are dropped, the fire door checked, and the alarm set from the lobby panel. The same sequence applies whether the hall has been used for a class or a private function. Anyone who cannot complete a step should leave a note in the book so that the caretaker can attend to it in the morning.""",
"drain the water heater, then switch off the immersion at the isolator, then take the meter reading",
"take the meter reading, then drain the water heater, then switch off the immersion at the isolator",
"The change falls in the sentence listing the closing sequence on the laminated card.",
"Reorders the steps of a task while every duty and every stated fact stays the same."),

# 9 nomological / report HARD amb axiomatic
add("e2b29-nomological1", "nomological", "report", "axiomatic", "hard",
"""Kirkbride Steam Winding Trust — Annual Report, Note 4: Plant Charges

The trust holds three items of restored plant on the asset schedule, all acquired second-hand and all in working order at the year end. The annual charge against each item is worked out on the straight-line basis over the remaining useful life. The resulting figures appear in the summary table and feed the reserve target agreed by the trustees in the spring. Two of the three items were revalued during the year after the boiler survey, and the surveyor's letter is held with the papers. The trustees note that the charge has no effect on the running account, which is kept on a cash footing throughout.""",
"worked out on the straight-line basis over the remaining useful life",
"worked out on the reducing-balance basis at twenty per cent of written-down value",
"The change falls in the sentence stating how the annual charge against each item is arrived at.",
"Switches which calculation scheme is applied to derive the figures; tempts axiomatic because the derived numbers downstream move."),

# 10 structural / config
add("e2b29-structural1", "structural", "config", None, "clear",
"""Estuary Tide Board — Display Feed Settings

The board pulls its readings from the gauge file every ten minutes and renders the next four high waters in the top panel. Each line of the gauge file carries a timestamp, a height in metres, and a quality flag, with the fields separated by a vertical bar. Blank lines are skipped and any line whose quality flag is not the letter G is ignored. The display dims between 23:00 and 06:00 and reverts to full brightness on the hour. If the feed is more than forty minutes stale the panel shows the last good reading with a dash in place of the height, and the warden is sent a text message.""",
"the fields separated by a vertical bar",
"the fields separated by a tab character",
"The change falls in the sentence describing the layout of a line in the gauge file.",
"Alters the delimiter used in the encoding; a human reads the same content but a parser does not."),

# 11 axiomatic / process
add("e2b29-axiomatic1", "axiomatic", "process", None, "clear",
"""Marrick Seed Bank — Handling of Incoming Accessions

Throughout this document a working day means Monday to Friday, excluding bank holidays. Incoming accessions are quarantined for five working days before germination testing, and the viability certificate is issued within ten working days of the test. Donors are told the expected certificate date at the point of deposit, and the drying room booking is made against the same count. Where a consignment arrives split across two deliveries, the count begins from the later one. The technician logs each deposit against the donor reference and files the packet slip with the quarantine sheet, which is checked by a second technician before the packet leaves the cold store.""",
"a working day means Monday to Friday, excluding bank holidays",
"a working day means any day on which the cold store is staffed, including Saturdays",
"The change falls in the opening sentence of the paragraph.",
"Redefines a term that every downstream count composes over, so the quarantine and certificate dates all shift."),

# 12 deontic extra / registry
add("e2b29-deontic2", "deontic", "registry", None, "clear",
"""Ellerby Common Grazing Register — Transfers of Stint

Transfers of stint between registered graziers are entered by the clerk on receipt of the signed transfer form and the current year's fee. The form need not be countersigned by a second grazier. Entries are made in ink in the bound register, with the date of receipt in the left margin, and a copy of the form is filed in the transfer folder. The clerk reads the register aloud at the spring meeting so that any error may be picked up while the parties are present. A grazier who disputes an entry may write to the chair within twenty-eight days of that meeting.""",
"The form need not be countersigned by a second grazier.",
"The form must be countersigned by a second grazier and by the chair.",
"The change falls in the sentence about signatures on the transfer form.",
"Converts an explicit exemption into a requirement; the filing and reading practices are unchanged."),

BAD = ["priority","priorities","rule","rules","identity","premise","premises","structure",
       "structural","manner","confidence","circumstance","circumstances","process","model","record"]

problems = []
for it in items:
    b, a = it["before"], it["after"]
    assert b != a
    # contiguous span check
    p = 0
    while p < min(len(b), len(a)) and b[p] == a[p]:
        p += 1
    s = 0
    while s < min(len(b), len(a)) - p and b[len(b)-1-s] == a[len(a)-1-s]:
        s += 1
    db, da = b[p:len(b)-s], a[p:len(a)-s]
    if "\n" in db or "\n" in da:
        problems.append(f"{it['id']}: newline in span")
    wc = len(b.split())
    if not (85 <= wc <= 150):
        problems.append(f"{it['id']}: wordcount {wc}")
    if b.count(it["_old"]) != 1:
        problems.append(f"{it['id']}: span not unique")
    span = (db + " " + da).lower()
    for w in BAD:
        if re.search(r"\b" + w + r"\b", span):
            problems.append(f"{it['id']}: leak word '{w}' in changed span")
    print(it["id"], wc, "| DIFF:", repr(db), "->", repr(da))

print("PROBLEMS:", problems)
if not problems:
    out = "/home/emoore/CIRISOntology/scratchpad/plane_corpus/eigen2/batch_29.jsonl"
    with open(out, "w") as f:
        for it in items:
            d = {k: v for k, v in it.items() if not k.startswith("_")}
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    print("wrote", out, len(items))
