# -*- coding: utf-8 -*-
"""ARM D-fact (24) — the positive control's factContent half.  Each artifact is
matched to the D-rule half: it carries the same kind of applied conversion or
step, worked through to derived content, and that machinery is IDENTICAL across
the two versions.  What changes is a claim about the world stated elsewhere in
the document."""

ITEMS = [

# ---------------------------------------------------------------- policy (5)
dict(id="t3-Df-pol-01", arm="D-fact", domain="policy",
 before="""Kingsmere Borough Council — Market Stall Licensing Policy

The general market has been held on the same square since 1227, and the borough licenses each stall for a season at a time. An application is assessed against the four published headings and awarded points under each. The points are added and turned into a pitch group by dividing the sum by 8 and rounding down, so a trader holding 33 points falls in group 4 and one holding 17 points falls in group 2. Groups three and above are offered a pitch on the square as they fall vacant, in date order within the group. Traders below group three are offered a pitch on the adjoining street where one is free. Licences run from the first Monday in March and are not transferable between traders. The markets officer writes to every applicant with the group reached and the reasons for it.""",
 old="held on the same square since 1227",
 new="held on the same square since 1854",
 site="The change is in the opening sentence, in the statement about how long the market has been held on the square.",
 note="Only the date given for the market on the square changes; the assessment arithmetic and the two worked groups are identical between versions."),

dict(id="t3-Df-pol-02", arm="D-fact", domain="policy",
 before="""Harrowfield Water Authority — Reservoir Access Policy

The reservoir supplies drinking water to about 40,000 households in the district, and public access to the perimeter is managed under this policy. Access is permitted on the eastern shore path at all times and on the western shore path outside the wildfowl season. A permit application from an angling or sailing club is scored against the five published headings, and the total is turned into an access band by dividing by 6 and rounding down, so a club scoring 30 falls in band 5 and one scoring 20 falls in band 3. Bands four and above may apply for a keyed gate. The authority reviews permits every three years and consults the wildlife trust before renewing any permit on the western shore. Swimming is not permitted anywhere on the reservoir.""",
 old="about 40,000 households in the district",
 new="about 12,000 households in the district",
 site="The change is in the opening sentence, in the statement of how many households the reservoir supplies.",
 note="Only the number of households supplied changes; the permit arithmetic and the two worked bands are identical between versions."),

dict(id="t3-Df-pol-03", arm="D-fact", domain="policy",
 before="""Nettlebridge College — Placement Insurance Policy

The college has run the industrial placement scheme since 1998, and every student on a placement is covered under the college's own arrangements. A host employer is assessed before a student is placed, against the four headings on the standard sheet. The marks are added and turned into a cover class by dividing the total by 4 and rounding up, so a host scoring 14 takes class 4 and one scoring 6 takes class 2. Hosts in class three and above are covered without further reference to the insurer. Hosts below that are referred, and the placements office holds the student back until the referral is answered. The office keeps the assessment sheets for the length of the placement and for six years afterwards.""",
 old="run the industrial placement scheme since 1998",
 new="run the industrial placement scheme since 2014",
 site="The change is in the opening sentence, in the statement of how long the placement scheme has run.",
 note="Only the year the scheme began changes; the assessment arithmetic and the two worked cover classes are identical between versions."),

dict(id="t3-Df-pol-04", arm="D-fact", domain="policy",
 before="""Marlow Institute — Archive Access Policy

The collection holds 6,200 boxes and occupies two floors of the Fairhaven building. Readers apply for access by giving the archivist a written statement of the material they wish to consult. Each request is assessed against the three published headings and the marks are turned into a handling group by adding them and dividing by 2, rounding up, so a request marked seven in total falls in group 4 and one marked three falls in group 2. Groups three and above are consulted in the supervised room only. The archivist sets out the material in advance where the request is made five working days ahead. Photography without flash is permitted in the reading room for material in groups one and two.""",
 old="holds 6,200 boxes and occupies two floors",
 new="holds 3,100 boxes and occupies one floor",
 site="The change is in the opening sentence, in the statement of the size of the collection and the space it occupies.",
 note="Only the stated size of the collection changes; the assessment arithmetic and the two worked groups are identical between versions."),

dict(id="t3-Df-pol-05", arm="D-fact", domain="policy",
 before="""Bellhaven Leisure Centre — Pool Admission Policy

The main pool was opened in 1974 and is fed from the borough's own borehole, and admission to it is managed under this policy at all public session times. A swimmer wishing to use the fast lane completes the timed length assessment with a member of the poolside team. The recorded time is turned into a lane group by dividing 60 by the time in seconds and rounding down, so a length swum in 20 seconds gives group 3 and one swum in 30 seconds gives group 2. Groups two and above may use the fast lane during public sessions. The assessment is repeated on request and at least once a year for regular users. Lane ropes are set out for the first session of the day and taken in after the last.""",
 old="opened in 1974 and is fed from the borough's own borehole",
 new="opened in 1938 and is fed from the mains supply",
 site="The change is in the opening sentence, in the statement of when the main pool opened and where its water comes from.",
 note="Only the stated opening year and water source of the pool change; the assessment arithmetic and the two worked lane groups are identical between versions."),

# ---------------------------------------------------------------- config (5)
dict(id="t3-Df-cfg-01", arm="D-fact", domain="config",
 before="""# Colverton Beck gauging station — reading conversion
# The station stands 400 metres downstream of the road bridge.
station_id = "CV-208"
sample_seconds = 60
stage_zero_m = 0.318

# stage is turned into flow by the two values below
flow_coefficient = 3.10
flow_exponent = 1.50
# flow at the three notice heights, worked from the two values above
flow_at_0_50_m = 1.096
flow_at_1_00_m = 3.100
flow_at_2_00_m = 8.768

notice_height_m = 1.00
alarm_height_m = 2.00
telemetry_minutes = 15
operator = "Colverton catchment team\"""",
 old="stands 400 metres downstream of the road bridge",
 new="stands 1,900 metres upstream of the road bridge",
 site="The change is in the comment on the second line, which places the station relative to the road bridge.",
 note="Only the stated position of the station changes; the flow coefficient and the three worked flows are identical between versions."),

dict(id="t3-Df-cfg-02", arm="D-fact", domain="config",
 before="""# Weirbank roadside cabinet — index conversion
cabinet = "WB-5"
site_opened = 2009
averaging_minutes = 60
zero_check_hour = 3

# concentration is turned into an index number by the divisor below
ppb_per_index_point = 20
index_cap = 10
# index at three stored hourly means, worked from the divisor above
index_at_40_ppb = 2
index_at_120_ppb = 6
index_at_200_ppb = 10

advisory_index = 6
board_message_index = 8
feed_seconds = 900
retain_days = 400""",
 old="site_opened = 2009",
 new="site_opened = 1994",
 site="The change is in the third line, in the value given for the year the site opened.",
 note="Only the stated opening year of the site changes; the index divisor and the three worked index values are identical between versions."),

dict(id="t3-Df-cfg-03", arm="D-fact", domain="config",
 before="""# Colverton weighbridge — load cell conversion
# The bridge was relaid in 2018 and stands beside the west gate.
bridge_id = "WB-3"
cells = 4
settle_seconds = 8

# cell counts are turned into kilogrammes by the factor and tare below
kg_per_count = 0.500
tare_counts = 800
# kilogrammes at three stored count totals, worked from the two values above
kg_at_2800_counts = 1000.0
kg_at_6800_counts = 3000.0
kg_at_12800_counts = 6000.0

ticket_minimum_kg = 1000.0
axle_limit_kg = 11500.0
printer = "gate-1"
retain_days = 1825""",
 old="relaid in 2018 and stands beside the west gate",
 new="relaid in 2004 and stands beside the north gate",
 site="The change is in the comment on the second line, which gives the relaying year and the position of the bridge.",
 note="Only the stated relaying year and position change; the conversion factor and the three worked weights are identical between versions."),

dict(id="t3-Df-cfg-04", arm="D-fact", domain="config",
 before="""# Colverton glasshouse — soil moisture bench
# The glasshouse covers 1,800 square metres and is heated from the biomass boiler.
node_id = "GH-7"
adc_bits = 12
read_interval_seconds = 300

# raw counts are turned into percent by the two values below
counts_dry = 3000
counts_wet = 1000
# percent at three stored raw counts, worked from the two values above
percent_at_2600 = 20.0
percent_at_2000 = 50.0
percent_at_1400 = 80.0

irrigate_below_percent = 20.0
stop_above_percent = 50.0
valve_seconds = 45
alert_email = "glasshouse@colverton.example\"""",
 old="covers 1,800 square metres and is heated from the biomass boiler",
 new="covers 640 square metres and is heated from the mains gas boiler",
 site="The change is in the comment on the second line, which gives the area of the glasshouse and the boiler that heats it.",
 note="Only the stated area and heat source change; the anchor counts and the three worked percentages are identical between versions."),

dict(id="t3-Df-cfg-05", arm="D-fact", domain="config",
 before="""# Colverton depot forklift bay — charger stage bench
# The bay holds four trucks and is the only charging point on the site.
bay = "south"
pack_ah = 480
mains_amps = 32

# each stage runs for the previous stage length times the factor below
first_stage_minutes = 15
stage_factor = 2
# stage lengths in minutes, worked from the first stage and factor above
stage_bulk_minutes = 15
stage_absorb_minutes = 30
stage_equalise_minutes = 60
total_charge_minutes = 105

gas_extract_on = true
cover_interlock = true
log_path = "/var/log/colverton/charger.log\"""",
 old="holds four trucks and is the only charging point on the site",
 new="holds nine trucks and is one of three charging points on the site",
 site="The change is in the comment on the second line, which gives the capacity of the bay and how many charging points the site has.",
 note="Only the stated capacity and number of charging points change; the stage factor and the worked stage lengths are identical between versions."),
]

ITEMS += [
# ------------------------------------------------------------------ code (5)
dict(id="t3-Df-code-01", arm="D-fact", domain="code",
 before='''"""Overdue charges for the Colverton library loan desk.

The desk has been open to the public since 1968.
"""

# a charge is worked from days overdue by the rate and cap below
PENCE_PER_DAY = 20
CAP_PENCE = 800
# charges for the three loans open at the desk, worked from the values above
CHARGE_LOAN_2210 = 100
CHARGE_LOAN_2265 = 400
CHARGE_LOAN_2288 = 800

DAYS_OVERDUE = {"2210": 5, "2265": 20, "2288": 61}


def charge_for(loan):
    return min(CAP_PENCE, PENCE_PER_DAY * DAYS_OVERDUE[loan])


def desk_charges():
    return {k: charge_for(k) for k in sorted(DAYS_OVERDUE)}''',
 old="open to the public since 1968",
 new="open to the public since 1991",
 site="The change is in the second line of the opening comment, in the statement of how long the desk has been open.",
 note="Only the year given for the desk opening changes; the daily rate and the three worked charges are identical between versions."),

dict(id="t3-Df-code-02", arm="D-fact", domain="code",
 before='''"""Trap index projection for the Colverton Beck eel counts."""

# The trap sits at the mill sluice, 2.4 km above the tidal limit.

# the index falls by the fraction below at each season
FALL_PER_SEASON = 0.20
START_INDEX = 500
# indices at the first four seasons, worked from the values above
INDEX_SEASON_1 = 400
INDEX_SEASON_2 = 320
INDEX_SEASON_3 = 256
INDEX_SEASON_4 = 204


def next_season(index):
    return int(index * (1 - FALL_PER_SEASON))


def projection(seasons):
    v, out = START_INDEX, []
    for _ in range(seasons):
        v = next_season(v)
        out.append(v)
    return out''',
 old="at the mill sluice, 2.4 km above the tidal limit",
 new="at the mill sluice, 8.1 km below the tidal limit",
 site="The change is in the comment that places the trap relative to the tidal limit.",
 note="Only the stated position of the trap changes; the seasonal fall and the four worked indices are identical between versions."),

dict(id="t3-Df-code-03", arm="D-fact", domain="code",
 before='''"""Pool hall submeter totals for the Colverton leisure centre.

The submeter was fitted by the contractor during the 2019 refurbishment.
"""

# a pulse count is turned into units by the factor below
KWH_PER_PULSE = 0.25
# units for the three months on file, worked from the factor above
UNITS_JANUARY = 20000
UNITS_FEBRUARY = 15000
UNITS_MARCH = 12500

PULSES = {"january": 80000, "february": 60000, "march": 50000}


def units_for(month):
    return int(KWH_PER_PULSE * PULSES[month])


def quarter_units():
    return {k: units_for(k) for k in PULSES}''',
 old="fitted by the contractor during the 2019 refurbishment",
 new="fitted by the contractor during the 2007 refurbishment",
 site="The change is in the second line of the opening comment, in the statement of when the submeter was fitted.",
 note="Only the year the submeter was fitted changes; the conversion factor and the three worked unit totals are identical between versions."),

dict(id="t3-Df-code-04", arm="D-fact", domain="code",
 before='''"""Residual projection for the Colverton service reservoir dosing sheet."""

# The bench comparator is the only one held at the works.

# the residual falls by the fraction below each day
LOSS_PER_DAY = 0.20
START_RESIDUAL = 0.60
# residuals at the first four days, worked from the values above
RESIDUAL_DAY_1 = 0.48
RESIDUAL_DAY_2 = 0.38
RESIDUAL_DAY_3 = 0.30
RESIDUAL_DAY_4 = 0.24


def next_day(mg):
    return round(mg * (1 - LOSS_PER_DAY), 2)


def week(days):
    v, out = START_RESIDUAL, []
    for _ in range(days):
        v = next_day(v)
        out.append(v)
    return out''',
 old="comparator is the only one held at the works",
 new="comparator is one of four held at the works",
 site="The change is in the comment about how many bench comparators the works holds.",
 note="Only the stated number of comparators changes; the daily loss and the four worked residuals are identical between versions."),

dict(id="t3-Df-code-05", arm="D-fact", domain="code",
 before='''"""Bat activity figures for the Colverton carr detector points.

The carr covers 62 hectares and is owned by the county wildlife trust.
"""

# a pass count is turned into an activity figure by the factor below
FIGURE_MULTIPLIER = 10
# figures for the three points on file, worked from the factor above
FIGURE_POINT_1 = 30
FIGURE_POINT_2 = 15
FIGURE_POINT_3 = 40

PASSES = {"1": (84, 28), "2": (45, 30), "3": (100, 25)}


def figure_for(point):
    passes, nights = PASSES[point]
    return int(passes / nights * FIGURE_MULTIPLIER)


def all_figures():
    return {k: figure_for(k) for k in sorted(PASSES)}''',
 old="covers 62 hectares and is owned by the county wildlife trust",
 new="covers 18 hectares and is owned by the parish council",
 site="The change is in the second line of the opening comment, in the statement of the area of the carr and who owns it.",
 note="Only the stated area and ownership change; the multiplier and the three worked activity figures are identical between versions."),

# ---------------------------------------------------------------- report (4)
dict(id="t3-Df-rep-01", arm="D-fact", domain="report",
 before="""Monitoring Note — Colverton Viaduct, Spans 1 and 2

The viaduct was opened in 1874 and is faced in local sandstone. Gauges were fixed to the lower flange at mid-span on both spans and read under a loaded test train run at walking pace. Microstrain readings were turned into stress by multiplying by an elastic constant of 205 kilonewtons per square millimetre and dividing by one thousand, so the 240 microstrain reading at span one gives 49.2 newtons per square millimetre and the 160 microstrain reading at span two gives 32.8. Both figures sit below the working limit for the section, which the design sheet gives as 120. Readings were repeated on the return run and agreed within four microstrain at every gauge. The gauges will stay in place until the next principal inspection.""",
 old="opened in 1874 and is faced in local sandstone",
 new="opened in 1902 and is faced in imported granite",
 site="The change is in the opening sentence, in the statement of when the viaduct opened and what it is faced in.",
 note="Only the stated opening year and facing change; the elastic constant and the two worked stresses are identical between versions."),

dict(id="t3-Df-rep-02", arm="D-fact", domain="report",
 before="""Footfall Note — Colverton Museum, Winter Quarter

The museum is the only accredited collection in the district. Beam counters at the two entrances were checked against a manual tally on three separate afternoons before the quarter opened. Counter totals were turned into visitor numbers by halving the beam count, to allow for entry and exit on the same beam, and then adding 4 in every hundred for pushchairs and wheelchairs passing as one, so the north door total of 30,000 beams gives 15,600 visitors and the south door total of 12,000 gives 6,240. The quarter total is the sum of the two doors. Counters were cleaned at the mid-quarter visit and the alignment was checked at the same time. The school group entrance is counted separately by the bookings desk.""",
 old="the only accredited collection in the district",
 new="one of three accredited collections in the district",
 site="The change is in the opening sentence, in the statement of how many accredited collections the district has.",
 note="Only the stated number of accredited collections changes; the counter conversion and the two worked visitor numbers are identical between versions."),

dict(id="t3-Df-rep-03", arm="D-fact", domain="report",
 before="""Bathing Water Note — Colverton Sands, Season Summary

The beach is 1,400 metres long and is backed by dunes. Samples were drawn twenty times through the season and cultured at the regional laboratory, with the sampling point held at the same marker on every visit. The season classification is worked out by taking the ninetieth percentile of the counts, dividing by 100, rounding up, and reading the answer against the class table where one or two gives excellent, three or four gives good, and five or more gives sufficient, so this season's percentile of 260 gives good. Two samples were drawn within a day of heavy rain and are flagged on the sheet. The classification will be shown on the board at each access point before the next season opens.""",
 old="beach is 1,400 metres long and is backed by dunes",
 new="beach is 3,000 metres long and is backed by a sea wall",
 site="The change is in the opening sentence, in the statement of the length of the beach and what backs it.",
 note="Only the stated length of the beach and what backs it change; the classification arithmetic and its worked answer are identical between versions."),

dict(id="t3-Df-rep-04", arm="D-fact", domain="report",
 before="""Fisheries Note — Colverton Mill Sluice, Five-Year Review

The mill has stood on the site since the sixteenth century. The trap at the sluice has been fished on the same nights each spring since the review period opened, with the same crew and the same gear. The run is falling at 15 per cent a year on the trap index, so the index of 360 counted this spring projects to 306 next spring, 260 the year after and 221 the year after that. The intervention threshold agreed with the trust is an index of 180, which on this projection is reached in the fifth year. Water temperature at first capture has been within a degree of the period mean in each of the five springs.""",
 old="mill has stood on the site since the sixteenth century",
 new="mill has stood on the site since the nineteenth century",
 site="The change is in the opening sentence, in the statement of how long the mill has stood on the site.",
 note="Only the stated age of the mill changes; the yearly fall and the three projected indices are identical between versions."),
]

ITEMS += [
# --------------------------------------------------------------- process (5)
dict(id="t3-Df-proc-01", arm="D-fact", domain="process",
 before="""Weld Inspection — Colverton Engineering, Fabrication Bay

The bay is the only one at the works fitted with an ultraviolet cabinet.

1. Clean the weld and the parent metal either side to bright metal for fifty millimetres.
2. Apply the penetrant and leave it for the dwell time printed on the tin.
3. Remove the excess, apply the developer, and read the weld after ten minutes.
4. Count the indications along the weld and note the length of each.
5. Turn the count into an acceptance class by dividing the number of indications by 3 and rounding up, so a weld with 7 indications takes class 3 and one with 2 indications takes class 1.
6. Accept welds in class one and two; refer class three and above to the welding engineer.
7. Photograph any weld referred to the engineer with the scale bar in frame.
8. Note the class, the count, and the reading time on the inspection sheet.
9. Clean the developer from the weld before the item leaves the bay.""",
 old="the only one at the works fitted with an ultraviolet cabinet",
 new="one of two at the works fitted with an ultraviolet cabinet",
 site="The change is in the line above the numbered steps, in the statement of how many bays have an ultraviolet cabinet.",
 note="Only the stated number of bays with a cabinet changes; the acceptance arithmetic and its two worked classes are identical between versions."),

dict(id="t3-Df-proc-02", arm="D-fact", domain="process",
 before="""Soil Sampling — Colverton Farm, Nutrient Round

The laboratory at Thirsk has held the scheme's accreditation since 2003.

1. Walk the field on a W pattern and take twenty-five cores to spade depth.
2. Combine the cores in the bucket and mix them thoroughly before bagging.
3. Label the bag with the field name, the date, and the sampling depth.
4. Send the bag to the laboratory with the submission sheet the same week.
5. Turn the returned milligrammes per litre into an index by dividing by 15 and rounding down, so a return of 46 gives index 3 and a return of 28 gives index 1.
6. Compare the index with the target for the crop in the coming rotation.
7. Note the index against the field on the nutrient plan.
8. Order lime where the pH returned is below the figure set for the soil type.
9. Repeat the round on the same fields in four years.""",
 old="held the scheme's accreditation since 2003",
 new="held the scheme's accreditation since 2016",
 site="The change is in the line above the numbered steps, in the statement of how long the laboratory has held accreditation.",
 note="Only the accreditation year changes; the index arithmetic and its two worked indices are identical between versions."),

dict(id="t3-Df-proc-03", arm="D-fact", domain="process",
 before="""Chlorine Dosing — Colverton Service Reservoir

The reservoir stands on the ridge above the village and was built in 1963.

1. Draw a sample from the outlet tapping and read the residual on the bench comparator.
2. Note the residual and the sample time on the dosing sheet.
3. Set the top-up dose from the residual, allowing for a loss of a fifth of the residual each day, so a reading of 0.50 falls to 0.40 after one day, 0.32 after two and 0.26 after three.
4. Confirm that the projected residual stays above the works minimum until the next visit.
5. Dose at the injection point with the pump set to the calculated rate.
6. Wait thirty minutes and draw a second sample from the same tapping.
7. Note the second reading beside the first on the dosing sheet.
8. Report any reading below the works minimum to the duty manager before leaving site.
9. Lock the kiosk and return the comparator to the van case.""",
 old="stands on the ridge above the village and was built in 1963",
 new="stands in the valley below the village and was built in 1937",
 site="The change is in the line above the numbered steps, in the statement of where the reservoir stands and when it was built.",
 note="Only the stated position and build year change; the daily loss step and its three worked residuals are identical between versions."),

dict(id="t3-Df-proc-04", arm="D-fact", domain="process",
 before="""Ladder Inspection — Colverton Depot, Access Equipment

The depot holds 46 ladders across the three yards.

1. Lay the ladder flat on the trestles in the inspection bay.
2. Check the stiles, the rungs, the feet and the tie rods against the illustrated sheet.
3. Mark the ladder with the coloured tag for the quarter just begun.
4. Set the next inspection by doubling the interval each time the ladder passes two rounds running, so a ladder starting on a 3-month interval moves to 6 months and then to 12 months.
5. Enter the new interval against the ladder number in the equipment register.
6. Withdraw any ladder that has not passed and move it to the quarantine rack.
7. Tell the depot manager the same day where a ladder is withdrawn.
8. Return passed ladders to the rack with the tag visible from the gangway.
9. Send the register extract to the safety officer at the end of each quarter.""",
 old="holds 46 ladders across the three yards",
 new="holds 112 ladders across the five yards",
 site="The change is in the line above the numbered steps, in the statement of how many ladders the depot holds and across how many yards.",
 note="Only the stated ladder and yard counts change; the interval step and its two worked intervals are identical between versions."),

dict(id="t3-Df-proc-05", arm="D-fact", domain="process",
 before="""Grain Intake Sampling — Colverton Store

The store was built in 1979 and holds 4,000 tonnes.

1. Draw three spear samples from different depths as the trailer tips.
2. Combine the three into one bag and shake it for a full minute.
3. Fill the meter cell to the mark and level it with the straight edge supplied.
4. Take three readings from the cell, emptying and refilling between each.
5. Turn the mean cell reading into moisture percent by adding 1.2 to the display figure, so a mean display of 13.8 gives 15.0 percent and a mean display of 17.3 gives 18.5 percent.
6. Note the moisture percent against the ticket number on the intake sheet.
7. Direct loads above sixteen percent to the drier rather than to the flat store.
8. Retain the combined bag for four weeks in case the load is queried.
9. Wipe the cell and the levelling edge before the next trailer is drawn.""",
 old="built in 1979 and holds 4,000 tonnes",
 new="built in 2011 and holds 9,500 tonnes",
 site="The change is in the line above the numbered steps, in the statement of when the store was built and how much it holds.",
 note="Only the stated build year and capacity change; the moisture adjustment and its two worked percentages are identical between versions."),
]

# --------------------------------------------------------------------------
# REVISION, made before any judgment was collected.  Five of the items above
# came out 0.84-0.96 similar in artifact text to their D-rule counterparts,
# because they were built by moving the change site within the same document.
# That is a tight matched control, but it also means a judge could meet the
# same document twice and answer the second showing by contrast with the first.
# The five are dropped and re-authored onto fresh subject matter, keeping the
# domain, the band, the recipe, and the unchanged applied-rule machinery.
# The originals are left visible above as the provenance of the revision.
# --------------------------------------------------------------------------
_DROP = {"t3-Df-rep-02", "t3-Df-proc-01", "t3-Df-proc-02",
         "t3-Df-proc-03", "t3-Df-proc-04"}
ITEMS = [i for i in ITEMS if i["id"] not in _DROP]

ITEMS += [
dict(id="t3-Df-rep-02", arm="D-fact", domain="report",
 before="""Car Park Note — Kingsmere Town Centre, Winter Quarter

The barrier at the entrance was replaced in 2015 and is maintained under contract. Beam counters on the entry and exit lanes were checked against a manual tally on three afternoons before the quarter opened. Entry beam totals were turned into vehicle counts by subtracting 6 in every hundred to allow for pedestrians crossing the lane, so the December total of 25,000 beams gives 23,500 vehicles and the January total of 18,000 gives 16,920. The two months together account for a little over half of the quarter. Counters were cleaned at the mid-quarter visit and the alignment was checked at the same time. Season ticket holders enter on a separate lane and are counted by the ticket system rather than by the beams.""",
 old="replaced in 2015 and is maintained under contract",
 new="replaced in 2003 and is maintained by the borough's own team",
 site="The change is in the opening sentence, in the statement of when the barrier was replaced and who maintains it.",
 note="Only the stated replacement year and maintainer change; the beam conversion and the two worked vehicle counts are identical between versions."),

dict(id="t3-Df-proc-01", arm="D-fact", domain="process",
 before="""Fire Door Inspection — Nettlebridge College, Lambert Building

The building has 62 fire doors on the three upper floors.

1. Take the illustrated sheet and the feeler gauges from the estates office.
2. Check each door for the certification label on the top edge of the leaf.
3. Measure the gap at the head and at both stiles with the gauges.
4. Turn the largest measured gap into a class by dividing the gap in millimetres by 2 and rounding up, so a gap of 5 millimetres gives class 3 and a gap of 2 gives class 1.
5. Accept doors in class one and two; list class three and above for the joiner.
6. Check that the closer pulls the door fully onto the latch from a half-open position.
7. Note the class, the largest gap, and the closer result against the door number.
8. Mark any door listed for the joiner with a numbered tag on the hinge side.
9. Return the sheet to the estates office at the end of the round.""",
 old="has 62 fire doors on the three upper floors",
 new="has 148 fire doors on the six upper floors",
 site="The change is in the line above the numbered steps, in the statement of how many fire doors the building has and on how many floors.",
 note="Only the stated door and floor counts change; the gap arithmetic and its two worked classes are identical between versions."),

dict(id="t3-Df-proc-02", arm="D-fact", domain="process",
 before="""Meter Reading Round — Harrowfield District, Eastern Walk

The district has 4,800 metered properties.

1. Draw the walk list and the handheld from the depot counter before eight.
2. Lift the chamber lid with the key and clear standing water from the dial face.
3. Read the black figures only and leave the red figures out of the entry.
4. Turn the dial units into litres by multiplying the reading by 1,000, so a reading of 47 gives 47,000 litres and a reading of 128 gives 128,000 litres.
5. Enter the litre figure against the property number on the handheld.
6. Photograph any dial that cannot be read cleanly and flag the property.
7. Replace the chamber lid and press it down until it seats flush with the path.
8. Report any chamber found flooded to the district team the same day.
9. Return the handheld to the docking cradle at the end of the walk.""",
 old="district has 4,800 metered properties",
 new="district has 11,200 metered properties",
 site="The change is in the line above the numbered steps, in the statement of how many metered properties the district has.",
 note="Only the stated number of metered properties changes; the dial conversion and its two worked litre figures are identical between versions."),

dict(id="t3-Df-proc-03", arm="D-fact", domain="process",
 before="""Boiler Water Testing — Colverton Laundry

The laundry has run on the same two boilers since 1996.

1. Draw a cooled sample from the blowdown line into the rinsed sample bottle.
2. Let the sample stand until it is at bench temperature before testing.
3. Add the indicator to the measured sample and swirl until the colour is even.
4. Titrate drop by drop, counting the drops until the colour turns.
5. Turn the drop count into hardness by multiplying the count by 10 to give parts per million, so a count of 7 gives 70 and a count of 12 gives 120.
6. Compare the hardness with the figure set in the water treatment schedule.
7. Adjust the softener regeneration where the hardness is above that figure.
8. Note the count, the hardness, and the sample time in the boiler book.
9. Rinse the bottle and the burette before the next sample is drawn.""",
 old="run on the same two boilers since 1996",
 new="run on the same two boilers since 2012",
 site="The change is in the line above the numbered steps, in the statement of how long the laundry has run on its present boilers.",
 note="Only the stated year changes; the hardness conversion and its two worked figures are identical between versions."),

dict(id="t3-Df-proc-04", arm="D-fact", domain="process",
 before="""Scaffold Tag Round — Corrie Viaduct Repaint

The site has 340 metres of scaffold standing at present.

1. Start at the west abutment and work along the standing scaffold in order.
2. Check the ties, the base plates, the boards and the guard rails at each bay.
3. Count the defects found in the bay and note the location of each.
4. Turn the count into a tag colour by counting 2 for each defect on a tie or a guard rail and 1 for any other, then taking green below 4, amber from 4 to 7, and red above 7, so a bay with two tie defects and one board defect scores 5 and takes amber.
5. Hang the tag for the colour reached at the bay access ladder.
6. Stop work in any bay taking a red tag and tell the scaffolder the same hour.
7. Note the bay number, the count, and the colour on the round sheet.
8. Repeat the round after any alteration to the standing scaffold.
9. File the round sheet with the site papers at the end of each week.""",
 old="has 340 metres of scaffold standing at present",
 new="has 810 metres of scaffold standing at present",
 site="The change is in the line above the numbered steps, in the statement of how much scaffold is standing on the site.",
 note="Only the stated length of standing scaffold changes; the tag arithmetic and its worked colour are identical between versions."),
]

# --------------------------------------------------------------------------
# SECOND REVISION, also before any judgment was collected.  A whole-corpus
# similarity sweep found two further items whose artifact text ran 0.79 and
# 0.95 similar to an ARM A item, because they had been built by re-siting the
# change in an artifact already used there.  Same objection, same remedy.
# Config items still run 0.65-0.67 against one another; that is the shared
# comment skeleton the recipe imposes on every config artifact in all four
# arms, not a re-used document, and it is left alone.
# --------------------------------------------------------------------------
_DROP2 = {"t3-Df-rep-01", "t3-Df-proc-05"}
ITEMS = [i for i in ITEMS if i["id"] not in _DROP2]

ITEMS += [
dict(id="t3-Df-rep-01", arm="D-fact", domain="report",
 before="""Ventilation Note — Colverton Archive Store, Lower Range

The store was fitted out in 1988 and is lit throughout by sealed units. Humidity was logged at four points across the lower range for a full year at hourly intervals. Logger counts were turned into relative humidity by multiplying by 0.25 and adding 10, so the mean count of 180 at the north wall gives 55 per cent and the mean count of 148 at the south wall gives 47 per cent. Both figures sit inside the band set out in the collection care plan. Loggers were checked against the reference hygrometer at the start and the end of the year and agreed within two per cent on both occasions. A fifth logger will be added at the door bay before the next heating season.""",
 old="fitted out in 1988 and is lit throughout by sealed units",
 new="fitted out in 2006 and is lit throughout by fibre optics",
 site="The change is in the opening sentence, in the statement of when the store was fitted out and how it is lit.",
 note="Only the stated fit-out year and lighting change; the humidity conversion and the two worked percentages are identical between versions."),

dict(id="t3-Df-proc-05", arm="D-fact", domain="process",
 before="""Livestock Weighing — Colverton Market, Sale Day

The market has been held on Tuesdays since the sale ring was rebuilt in 1988.

1. Check that the weigh crate is empty and that the display reads zero before the first lot.
2. Drive the lot into the crate and close the rear gate before taking the reading.
3. Wait for the display to settle and hold steady for three seconds.
4. Turn the display figure into a sale weight by subtracting 8 kilogrammes for the crate mat, so a display of 508 gives a sale weight of 500 and a display of 336 gives 328.
5. Call the sale weight to the clerk and confirm it against the lot card.
6. Open the front gate and move the lot on to the holding pen.
7. Re-zero the display between lots and note any drift on the sheet.
8. Report a drift above two kilogrammes to the market manager before the next lot.
9. Wash the crate down at the close of the sale.""",
 old="held on Tuesdays since the sale ring was rebuilt in 1988",
 new="held on Thursdays since the sale ring was rebuilt in 1964",
 site="The change is in the line above the numbered steps, in the statement of the market day and when the sale ring was rebuilt.",
 note="Only the stated market day and rebuilding year change; the crate-mat adjustment and its two worked sale weights are identical between versions."),
]

# --------------------------------------------------------------------------
# THIRD REVISION, before any judgment was collected.  The remaining four
# cross-arm pairs at 0.61-0.67 were checked against the within-domain baseline
# rather than against a guessed threshold: median pairwise similarity inside a
# domain is 0.03-0.10 and the 90th percentile is 0.06-0.21, so 0.61+ is an
# order of magnitude out and is document reuse (same instrument, renamed site),
# not the recipe's shared skeleton.  All four are re-authored onto instruments
# that appear nowhere else in the corpus.
# --------------------------------------------------------------------------
_DROP3 = {"t3-Df-cfg-01", "t3-Df-cfg-02", "t3-Df-rep-04", "t3-Df-code-01"}
ITEMS = [i for i in ITEMS if i["id"] not in _DROP3]

ITEMS += [
dict(id="t3-Df-cfg-01", arm="D-fact", domain="config",
 before="""# Corrie Viaduct mast — wind speed conversion
# The mast stands on the south parapet and was erected in 1996.
mast_id = "CV-MAST-1"
sample_seconds = 10
gust_window_seconds = 3

# pulse counts are turned into metres per second by the two values below
ms_per_pulse = 0.25
zero_pulses = 2
# speeds at three stored pulse counts, worked from the two values above
ms_at_10_pulses = 2.0
ms_at_42_pulses = 10.0
ms_at_82_pulses = 20.0

work_stop_ms = 10.0
sheeting_stop_ms = 20.0
telemetry_minutes = 5
operator = "Corrie access team\"""",
 old="stands on the south parapet and was erected in 1996",
 new="stands on the north parapet and was erected in 1974",
 site="The change is in the comment on the second line, which places the mast and gives the year it was erected.",
 note="Only the stated position and year change; the pulse conversion and the three worked speeds are identical between versions."),

dict(id="t3-Df-cfg-02", arm="D-fact", domain="config",
 before="""# Colverton store hopper — level to tonnage bench
hopper = "H-2"
commissioned = 2011
sample_seconds = 30
echo_unit = "microseconds"

# echo time is turned into stored tonnes by the two values below
tonnes_per_1000_us = 4.0
empty_echo_us = 3000
# tonnes at three stored echo times, worked from the two values above
tonnes_at_2500_us = 2.0
tonnes_at_1500_us = 6.0
tonnes_at_500_us = 10.0

reorder_below_tonnes = 2.0
full_tonnes = 10.0
alert_email = "store@colverton.example"
retain_days = 730""",
 old="commissioned = 2011",
 new="commissioned = 1993",
 site="The change is in the third line, in the value given for the year the hopper was commissioned.",
 note="Only the stated commissioning year changes; the echo conversion and the three worked tonnages are identical between versions."),

dict(id="t3-Df-code-01", arm="D-fact", domain="code",
 before='''"""Admission bands for the Colverton Museum till.

The till was replaced in 2018 and prints a duplicate for the day book.
"""

# an age is turned into an admission band by the two cut points below
CHILD_UNDER = 16
CONCESSION_FROM = 65
# bands for the three ages on the day sheet, worked from the cut points above
BAND_AT_9 = "child"
BAND_AT_34 = "adult"
BAND_AT_71 = "concession"


def band_for(age):
    if age < CHILD_UNDER:
        return "child"
    if age >= CONCESSION_FROM:
        return "concession"
    return "adult"


def sheet_bands(ages):
    return [band_for(a) for a in ages]''',
 old="replaced in 2018 and prints a duplicate for the day book",
 new="replaced in 2005 and prints three copies for the day book",
 site="The change is in the second line of the opening comment, in the statement of when the till was replaced and what it prints.",
 note="Only the stated replacement year and printing behaviour change; the two cut points and the three worked bands are identical between versions."),

dict(id="t3-Df-rep-04", arm="D-fact", domain="report",
 before="""Roost Note — Colverton Church Tower, Swift Boxes

The tower was re-roofed in 1972 and the boxes were fitted at the same time. Occupied boxes were counted on four evenings in late June from the churchyard, with two observers working the north and south faces separately. Counts were turned into an occupancy index by dividing the occupied count by the number of boxes on that face and multiplying by 100, so the north face with 9 boxes occupied out of 20 gives an index of 45 and the south face with 6 out of 24 gives 25. Faces returning an index above forty are proposed for a second row of boxes next season. Weather was dry and still on all four evenings. The count follows the same layout as the previous two seasons so that the three can be read together.""",
 old="re-roofed in 1972 and the boxes were fitted at the same time",
 new="re-roofed in 2004 and the boxes were fitted ten years later",
 site="The change is in the opening sentence, in the statement of when the tower was re-roofed and when the boxes were fitted.",
 note="Only the stated re-roofing year and fitting date change; the occupancy conversion and the two worked indices are identical between versions."),
]

# --------------------------------------------------------------------------
# FOURTH REVISION, before any judgment was collected.  Lowering the sweep
# threshold to 0.45 surfaced two more reused instruments (a glasshouse moisture
# bench at 0.59 and a forklift charger bench at 0.46).  Same objection, same
# remedy; both re-authored onto instruments used nowhere else.
# --------------------------------------------------------------------------
_DROP4 = {"t3-Df-cfg-04", "t3-Df-cfg-05"}
ITEMS = [i for i in ITEMS if i["id"] not in _DROP4]

ITEMS += [
dict(id="t3-Df-cfg-04", arm="D-fact", domain="config",
 before="""# Colverton sluice — gate position bench
# The sluice was rebuilt in 1974 and is worked by hand from the walkway.
sluice_id = "CV-SL-1"
sample_seconds = 60
encoder_bits = 10

# encoder counts are turned into gate opening by the two values below
mm_per_count = 2.5
closed_counts = 40
# opening at three stored counts, worked from the two values above
mm_at_120_counts = 200.0
mm_at_240_counts = 500.0
mm_at_440_counts = 1000.0

notice_opening_mm = 500.0
full_opening_mm = 1000.0
telemetry_minutes = 15
operator = "Colverton catchment team\"""",
 old="rebuilt in 1974 and is worked by hand from the walkway",
 new="rebuilt in 2009 and is worked by motor from the control kiosk",
 site="The change is in the comment on the second line, which gives the year the sluice was rebuilt and how it is worked.",
 note="Only the stated rebuilding year and means of working change; the encoder conversion and the three worked openings are identical between versions."),

dict(id="t3-Df-cfg-05", arm="D-fact", domain="config",
 before="""# Colverton village hall — heating setback bench
# The hall seats 180 and was let for 92 events last year.
zone = "main hall"
sensor = "return-air"
sample_minutes = 5

# each setback step follows the previous one by the factor below
first_step_minutes = 30
step_factor = 2
# step lengths in minutes, worked from the first step and factor above
step_purge_minutes = 30
step_coast_minutes = 60
step_hold_minutes = 120
total_setback_minutes = 210

frost_protect_c = 5
occupied_c = 19
log_path = "/var/log/colverton/heating.log\"""",
 old="seats 180 and was let for 92 events last year",
 new="seats 340 and was let for 215 events last year",
 site="The change is in the comment on the second line, which gives the seating capacity of the hall and the number of lettings last year.",
 note="Only the stated capacity and letting count change; the setback factor and the worked step lengths are identical between versions."),
]

# --------------------------------------------------------------------------
# FIFTH AND FINAL REVISION, before any judgment was collected.  t3-Df-rep-03
# carried the SAME rule sentence as t3-Dr-pol-05, where that sentence is what
# changes.  Two arms sharing one rule text is the one overlap that could let a
# judge read the D contrast off cross-item memory rather than off the change
# site, so the item is re-authored onto a different conversion.
# --------------------------------------------------------------------------
_DROP5 = {"t3-Df-rep-03"}
ITEMS = [i for i in ITEMS if i["id"] not in _DROP5]

ITEMS += [
dict(id="t3-Df-rep-03", arm="D-fact", domain="report",
 before="""Air Quality Note — Colverton High Street, Diffusion Tubes

The street was pedestrianised at its western end in 2011. Tubes were exposed at six points along the street and changed on the first working day of each month through the year. Laboratory returns were turned into an annual mean by averaging the twelve monthly figures and then multiplying by a bias adjustment of 0.83, so the western point with a raw mean of 40 micrograms per cubic metre gives 33.2 and the eastern point with a raw mean of 50 gives 41.5. The objective set in the borough's own plan is 40 micrograms per cubic metre. One tube was lost in August at the eastern point and that month has been left out of the average for that point. The tubes will be exposed again on the same six points next year.""",
 old="pedestrianised at its western end in 2011",
 new="pedestrianised at its eastern end in 1998",
 site="The change is in the opening sentence, in the statement of which end of the street was pedestrianised and when.",
 note="Only the stated end of the street and the year change; the bias adjustment and the two worked annual means are identical between versions."),
]
