# -*- coding: utf-8 -*-
"""ARM D-rule (24) — the positive control's appliedRule half.  The change is at
the applied-rule site, either flavour (A-type conversion or B-type step), same
domains and same recipe as arms A and B.  Paired against t3_items_Dfact.py."""

ITEMS = [

# ---------------------------------------------------------------- policy (5)
dict(id="t3-Dr-pol-01", arm="D-rule", domain="policy",
 before="""Kingsmere Borough Council — Resident Parking Permit Policy

A household applying for a second permit is assessed against the four published headings and awarded points under each. The points are added and turned into an award group by dividing the sum by 8 and rounding down, so a household holding 33 points falls in group 4 and one holding 17 points falls in group 2. Groups three and above are offered a second permit as bays fall vacant, in date order within the group. A household may hold no more than two permits in total, whatever group it reaches. Permits run for twelve months from the date of issue and are not transferable between vehicles without notice to the parking office. The office writes to every applicant with the group reached and the reasons for it, and a second officer will look at the assessment again on request.""",
 old="dividing the sum by 8 and rounding down, so a household holding 33 points falls in group 4 and one holding 17 points falls in group 2",
 new="dividing the sum by 5 and rounding down, so a household holding 33 points falls in group 6 and one holding 17 points falls in group 3",
 site="The change is in the second sentence, in the passage that turns a points sum into an award group.",
 note="Only the divisor applied to the points sum changes, together with the two worked groups stated in the same sentence."),

dict(id="t3-Dr-pol-02", arm="D-rule", domain="policy",
 before="""Nettlebridge College — Hardship Bursary Assessment Policy

A student applying to the hardship fund gives the college a statement of household income and of the number of dependants in the household. The assessed figure is worked out by taking the household income, subtracting 3,000 pounds for each dependant, and dividing what remains by twelve, so a household on 27,000 pounds with two dependants gives an assessed figure of 1,750 a month and one on 21,000 with one dependant gives 1,500. Assessed figures below 1,600 a month attract the full award and figures above that attract half. Awards are paid in three instalments across the year, and a student may ask for the first instalment early where the need is immediate. The bursary panel meets twice each term and its decisions are notified within ten working days of the meeting.""",
 old="subtracting 3,000 pounds for each dependant, and dividing what remains by twelve, so a household on 27,000 pounds with two dependants gives an assessed figure of 1,750 a month and one on 21,000 with one dependant gives 1,500",
 new="subtracting 3,600 pounds for each dependant, and dividing what remains by twelve, so a household on 27,000 pounds with two dependants gives an assessed figure of 1,650 a month and one on 21,000 with one dependant gives 1,450",
 site="The change is in the second sentence, in the passage that turns household income into an assessed monthly figure.",
 note="Only the allowance subtracted for each dependant changes, together with the two worked assessed figures stated in the same sentence."),

dict(id="t3-Dr-pol-03", arm="D-rule", domain="policy",
 before="""Kingsmere Borough Council — Highway Tree Inspection Policy

Every highway tree on the register is inspected on a cycle set by its condition group at the previous visit. A tree moves to the next visit by halving the interval each time its group worsens by one, so a tree in group one is seen every 48 months, a tree in group two every 24 months and a tree in group three every 12 months. The arboricultural officer sets the group at the close of each visit and enters it on the register the same week. Trees adjoining a school route are visited in term time so that any work can be planned for a holiday. Work arising from an inspection is ordered within ten working days where the officer marks it urgent. The register is published each spring with the ward and the species but without the group.""",
 old="halving the interval each time its group worsens by one, so a tree in group one is seen every 48 months, a tree in group two every 24 months and a tree in group three every 12 months",
 new="cutting the interval to a quarter each time its group worsens by one, so a tree in group one is seen every 48 months, a tree in group two every 12 months and a tree in group three every 3 months",
 site="The change is in the second sentence, in the passage that says how the visit interval moves as the group worsens.",
 note="Only the step by which the visit interval shortens changes, together with the three worked intervals stated in the same sentence."),

dict(id="t3-Dr-pol-04", arm="D-rule", domain="policy",
 before="""Marlow Institute — Equipment Loan Policy

Portable equipment is lent from the technical store for a fixed period against the borrower's staff number. A loan that is not returned by the due date moves to the overdue class after 7 days, and an overdue loan moves to the recovery class after a further 21 days, so a loan due on 1 October reaches the overdue class on 8 October and the recovery class on 29 October. Return at any point before recovery clears the loan and stops the count. The store manager writes to borrowers in the overdue class each Friday and passes the recovery class to the departmental administrator. Items in the recovery class are charged to the borrowing department at replacement value. Loans of more than four weeks are agreed in advance with the manager and are entered on the store list.""",
 old="moves to the overdue class after 7 days, and an overdue loan moves to the recovery class after a further 21 days, so a loan due on 1 October reaches the overdue class on 8 October and the recovery class on 29 October",
 new="moves to the overdue class after 3 days, and an overdue loan moves to the recovery class after a further 10 days, so a loan due on 1 October reaches the overdue class on 4 October and the recovery class on 14 October",
 site="The change is in the second sentence, in the passage that says how long a loan sits in each class before it moves on.",
 note="Only the two waiting periods that carry a loan from class to class change, together with the two worked dates stated in the same sentence."),

dict(id="t3-Dr-pol-05", arm="D-rule", domain="policy",
 before="""Harrowfield Water Authority — Bathing Water Classification Policy

Samples are drawn from each designated bathing water twenty times through the season and cultured at the regional laboratory. The season classification is worked out by taking the ninetieth percentile of the counts, dividing by 100, rounding up, and reading the answer against the class table where one or two gives excellent, three or four gives good, and five or more gives sufficient, so a percentile of 250 gives good and a percentile of 140 gives excellent. Classifications are published before the following season opens and are shown on the board at each access point. Where a sample is drawn during or shortly after heavy rain, the result is flagged on the sheet but is still counted. The authority reviews any water falling two classes in a season and reports the review to the regional board.""",
 old="dividing by 100, rounding up, and reading the answer against the class table where one or two gives excellent, three or four gives good, and five or more gives sufficient, so a percentile of 250 gives good and a percentile of 140 gives excellent",
 new="dividing by 50, rounding up, and reading the answer against the class table where one or two gives excellent, three or four gives good, and five or more gives sufficient, so a percentile of 250 gives sufficient and a percentile of 140 gives good",
 site="The change is in the second sentence, in the passage that turns a percentile count into a season classification.",
 note="Only the divisor applied to the percentile count changes, together with the two worked classifications stated in the same sentence."),

# ---------------------------------------------------------------- config (5)
dict(id="t3-Dr-cfg-01", arm="D-rule", domain="config",
 before="""# Eastgate pump station — wet well volume conversion
station = "EG-PS-04"
sample_seconds = 15
sensor = "ultrasonic"

# level is turned into stored volume by the area below
well_area_m2 = 6.0
invert_level_m = 0.15
# volume at three stored levels, worked from the area and invert above
volume_at_0_65_m = 3.0
volume_at_1_15_m = 6.0
volume_at_2_15_m = 12.0

start_pump_m3 = 6.0
stop_pump_m3 = 3.0
high_alarm_m3 = 12.0
telemetry_minutes = 5""",
 old="""well_area_m2 = 6.0
invert_level_m = 0.15
# volume at three stored levels, worked from the area and invert above
volume_at_0_65_m = 3.0
volume_at_1_15_m = 6.0
volume_at_2_15_m = 12.0""",
 new="""well_area_m2 = 9.5
invert_level_m = 0.15
# volume at three stored levels, worked from the area and invert above
volume_at_0_65_m = 4.75
volume_at_1_15_m = 9.5
volume_at_2_15_m = 19.0""",
 site="The change is in the six-line block that begins with the well area.",
 note="Only the area used to turn level into stored volume changes, together with the three worked volumes beneath it."),

dict(id="t3-Dr-cfg-02", arm="D-rule", domain="config",
 before="""# Calder district — alarm shelving bench
board = "intake-board"
poll_seconds = 10
operator_group = "duty"

# a shelved alarm loses weight by the factor below at each hour
shelf_start_weight = 100
weight_factor = 0.5
# weight after each of the first four hours, worked from the values above
weight_after_1h = 50
weight_after_2h = 25
weight_after_3h = 13
weight_after_4h = 6

unshelve_below = 6
audible_above = 50
retain_days = 30
theme = "high-contrast\"""",
 old="""weight_factor = 0.5
# weight after each of the first four hours, worked from the values above
weight_after_1h = 50
weight_after_2h = 25
weight_after_3h = 13
weight_after_4h = 6""",
 new="""weight_factor = 0.8
# weight after each of the first four hours, worked from the values above
weight_after_1h = 80
weight_after_2h = 64
weight_after_3h = 51
weight_after_4h = 41""",
 site="The change is in the six-line block that begins with the hourly weight factor.",
 note="Only the factor by which a shelved weight follows the previous hour changes, together with the four worked weights beneath it."),

dict(id="t3-Dr-cfg-03", arm="D-rule", domain="config",
 before="""# Bewick borehole — pressure to depth conversion
borehole = "BH-22"
sample_seconds = 60
transducer = "vented"

# pressure in kilopascals is turned into depth by the divisor below
kpa_per_metre = 9.81
sensor_offset_m = 0.00
# depth at three stored pressures, worked from the divisor and offset above
depth_at_98_1_kpa = 10.0
depth_at_196_2_kpa = 20.0
depth_at_294_3_kpa = 30.0

pump_on_depth_m = 20.0
pump_off_depth_m = 10.0
low_water_depth_m = 30.0
log_path = "/var/log/bewick/bh22.log\"""",
 old="""kpa_per_metre = 9.81
sensor_offset_m = 0.00
# depth at three stored pressures, worked from the divisor and offset above
depth_at_98_1_kpa = 10.0
depth_at_196_2_kpa = 20.0
depth_at_294_3_kpa = 30.0""",
 new="""kpa_per_metre = 12.26
sensor_offset_m = 0.00
# depth at three stored pressures, worked from the divisor and offset above
depth_at_98_1_kpa = 8.0
depth_at_196_2_kpa = 16.0
depth_at_294_3_kpa = 24.0""",
 site="The change is in the six-line block that begins with the kilopascals-per-metre divisor.",
 note="Only the divisor converting pressure to depth changes, together with the three worked depths beneath it."),

dict(id="t3-Dr-cfg-04", arm="D-rule", domain="config",
 before="""# Weirbank Surgery — appointment reminder ladder
channel = "sms"
sender = "Weirbank"
quiet_hours = "21:00-08:00"

# each reminder follows the previous one at the spacing below
first_reminder_days_before = 14
spacing_days = 6
# the reminder days before an appointment, worked from the values above
reminder_1_days_before = 14
reminder_2_days_before = 8
reminder_3_days_before = 2
reminder_count = 3

opt_out_keyword = "STOP"
max_per_patient_per_week = 3
log_path = "/var/log/weirbank/reminders.log\"""",
 old="""spacing_days = 6
# the reminder days before an appointment, worked from the values above
reminder_1_days_before = 14
reminder_2_days_before = 8
reminder_3_days_before = 2
reminder_count = 3""",
 new="""spacing_days = 5
# the reminder days before an appointment, worked from the values above
reminder_1_days_before = 14
reminder_2_days_before = 9
reminder_3_days_before = 4
reminder_count = 3""",
 site="The change is in the six-line block that begins with the reminder spacing.",
 note="Only the spacing at which each reminder follows the previous one changes, together with the reminder days and the count worked from it beneath."),

dict(id="t3-Dr-cfg-05", arm="D-rule", domain="config",
 before="""# Ardwick depot — gas detector bench
detector = "GD-11"
gas = "carbon monoxide"
sample_seconds = 5

# concentration is turned into an alarm level by the step below
ppm_per_level = 25
max_level = 4
# level at three stored concentrations, worked from the step above
level_at_25_ppm = 1
level_at_75_ppm = 3
level_at_100_ppm = 4

sounder_from_level = 2
extract_from_level = 3
evacuate_from_level = 4
retain_days = 365""",
 old="""ppm_per_level = 25
max_level = 4
# level at three stored concentrations, worked from the step above
level_at_25_ppm = 1
level_at_75_ppm = 3
level_at_100_ppm = 4""",
 new="""ppm_per_level = 50
max_level = 4
# level at three stored concentrations, worked from the step above
level_at_25_ppm = 1
level_at_75_ppm = 2
level_at_100_ppm = 2""",
 site="The change is in the six-line block that begins with the concentration step per alarm level.",
 note="Only the concentration step that turns a reading into an alarm level changes, together with the three worked levels beneath it."),
]

ITEMS += [
# ------------------------------------------------------------------ code (5)
dict(id="t3-Dr-code-01", arm="D-rule", domain="code",
 before='''"""Overdue charges for the Nettlebridge College loan desk."""

# a charge is worked from days overdue by the rate and cap below
PENCE_PER_DAY = 15
CAP_PENCE = 900
# charges for the three loans open at the desk, worked from the values above
CHARGE_LOAN_4471 = 90
CHARGE_LOAN_4512 = 450
CHARGE_LOAN_4530 = 900

DAYS_OVERDUE = {"4471": 6, "4512": 30, "4530": 74}


def charge_for(loan):
    return min(CAP_PENCE, PENCE_PER_DAY * DAYS_OVERDUE[loan])


def desk_charges():
    return {k: charge_for(k) for k in sorted(DAYS_OVERDUE)}''',
 old='''PENCE_PER_DAY = 15
CAP_PENCE = 900
# charges for the three loans open at the desk, worked from the values above
CHARGE_LOAN_4471 = 90
CHARGE_LOAN_4512 = 450
CHARGE_LOAN_4530 = 900''',
 new='''PENCE_PER_DAY = 25
CAP_PENCE = 900
# charges for the three loans open at the desk, worked from the values above
CHARGE_LOAN_4471 = 150
CHARGE_LOAN_4512 = 750
CHARGE_LOAN_4530 = 900''',
 site="The change is in the six-line block that begins with the daily rate.",
 note="Only the daily rate applied to days overdue changes, together with the three worked charges beneath it."),

dict(id="t3-Dr-code-02", arm="D-rule", domain="code",
 before='''"""Settling column readings for the Marchgate laboratory bench."""

# the suspended figure falls by the fraction below at each half hour
SETTLE_FRACTION = 0.40
START_MG_PER_L = 500.0
# readings at the first four half hours, worked from the values above
READING_0H5 = 300.0
READING_1H0 = 180.0
READING_1H5 = 108.0
READING_2H0 = 64.8


def next_reading(mg):
    return round(mg * (1 - SETTLE_FRACTION), 1)


def column(steps):
    v, out = START_MG_PER_L, []
    for _ in range(steps):
        v = next_reading(v)
        out.append(v)
    return out''',
 old='''SETTLE_FRACTION = 0.40
START_MG_PER_L = 500.0
# readings at the first four half hours, worked from the values above
READING_0H5 = 300.0
READING_1H0 = 180.0
READING_1H5 = 108.0
READING_2H0 = 64.8''',
 new='''SETTLE_FRACTION = 0.20
START_MG_PER_L = 500.0
# readings at the first four half hours, worked from the values above
READING_0H5 = 400.0
READING_1H0 = 320.0
READING_1H5 = 256.0
READING_2H0 = 204.8''',
 site="The change is in the seven-line block that begins with the settling fraction.",
 note="Only the fraction by which a reading follows the previous half hour changes, together with the four worked readings beneath it."),

dict(id="t3-Dr-code-03", arm="D-rule", domain="code",
 before='''"""Module marks for the Marlow Institute board sheet, turned into a letter."""

# a mark is turned into a letter by the two cut points below
LETTER_B_FROM = 60
LETTER_A_FROM = 70
# letters for the three marks on the sheet, worked from the cut points above
LETTER_AT_58 = "C"
LETTER_AT_64 = "B"
LETTER_AT_72 = "A"


def letter_for(mark):
    if mark >= LETTER_A_FROM:
        return "A"
    if mark >= LETTER_B_FROM:
        return "B"
    return "C"


def sheet_letters(marks):
    return [letter_for(m) for m in marks]''',
 old='''LETTER_B_FROM = 60
LETTER_A_FROM = 70
# letters for the three marks on the sheet, worked from the cut points above
LETTER_AT_58 = "C"
LETTER_AT_64 = "B"
LETTER_AT_72 = "A"''',
 new='''LETTER_B_FROM = 50
LETTER_A_FROM = 62
# letters for the three marks on the sheet, worked from the cut points above
LETTER_AT_58 = "B"
LETTER_AT_64 = "A"
LETTER_AT_72 = "A"''',
 site="The change is in the six-line block that begins with the first of the two cut points.",
 note="Only the cut points applied to a module mark change, together with the worked letters beneath them."),

dict(id="t3-Dr-code-04", arm="D-rule", domain="code",
 before='''"""Cleaning rota generation for the Fenwick Estate community shop."""

from datetime import date, timedelta

FIRST = date(2026, 3, 2)
# each turn follows the previous one by the gap below
GAP_DAYS = 7
TURNS = 4
# turn dates, worked from the first date and gap above
TURN_1 = "2026-03-09"
TURN_2 = "2026-03-16"
TURN_3 = "2026-03-23"
TURN_4 = "2026-03-30"


def turn_dates():
    return [(FIRST + timedelta(days=GAP_DAYS * (i + 1))).isoformat() for i in range(TURNS)]''',
 old='''GAP_DAYS = 7
TURNS = 4
# turn dates, worked from the first date and gap above
TURN_1 = "2026-03-09"
TURN_2 = "2026-03-16"
TURN_3 = "2026-03-23"
TURN_4 = "2026-03-30"''',
 new='''GAP_DAYS = 10
TURNS = 4
# turn dates, worked from the first date and gap above
TURN_1 = "2026-03-12"
TURN_2 = "2026-03-22"
TURN_3 = "2026-04-01"
TURN_4 = "2026-04-11"''',
 site="The change is in the seven-line block that begins with the gap in days.",
 note="Only the gap by which each turn follows the previous one changes, together with the four turn dates worked from it beneath."),

dict(id="t3-Dr-code-05", arm="D-rule", domain="code",
 before='''"""Exposure figures for the Corrie Viaduct working platform."""

# air temperature and wind are turned into an exposure figure by the pair below
WIND_WEIGHT = 0.5
BASE_OFFSET = 2
# figures for the three sets of readings on file, worked from the pair above
FIGURE_AT_6C_20KMH = -6
FIGURE_AT_2C_30KMH = -15
FIGURE_AT_0C_40KMH = -22

READINGS = [(6, 20), (2, 30), (0, 40)]


def figure_for(temp_c, wind_kmh):
    return int(temp_c - WIND_WEIGHT * wind_kmh - BASE_OFFSET)


def platform_figures():
    return [figure_for(t, w) for t, w in READINGS]''',
 old='''WIND_WEIGHT = 0.5
BASE_OFFSET = 2
# figures for the three sets of readings on file, worked from the pair above
FIGURE_AT_6C_20KMH = -6
FIGURE_AT_2C_30KMH = -15
FIGURE_AT_0C_40KMH = -22''',
 new='''WIND_WEIGHT = 0.2
BASE_OFFSET = 2
# figures for the three sets of readings on file, worked from the pair above
FIGURE_AT_6C_20KMH = 0
FIGURE_AT_2C_30KMH = -6
FIGURE_AT_0C_40KMH = -10''',
 site="The change is in the six-line block that begins with the wind weight.",
 note="Only the weight given to wind speed changes, together with the three worked exposure figures beneath it."),

# ---------------------------------------------------------------- report (5)
dict(id="t3-Dr-rep-01", arm="D-rule", domain="report",
 before="""Sound Insulation Test Note — Ravensworth Trust, Blocks 4 and 5

Airborne testing was carried out between the paired living rooms on the second floor of each block, with the source room dosed by a dodecahedron loudspeaker at two positions. The level difference at each third-octave band was turned into a single rating by taking the mean of the sixteen bands and subtracting a correction of 3 decibels for room volume, so block four with a band mean of 55 gives a rating of 52 and block five with a band mean of 49 gives 46. Ratings of forty-five and above meet the standard set in the trust's own specification. Background levels were at least ten decibels below the receiving level in every band. Reverberation was measured in the receiving room at both loudspeaker positions and the two agreed closely.""",
 old="subtracting a correction of 3 decibels for room volume, so block four with a band mean of 55 gives a rating of 52 and block five with a band mean of 49 gives 46",
 new="subtracting a correction of 8 decibels for room volume, so block four with a band mean of 55 gives a rating of 47 and block five with a band mean of 49 gives 41",
 site="The change is in the second sentence, in the passage that turns a band mean into a single rating.",
 note="Only the room-volume correction applied to the band mean changes, together with the two worked ratings stated in the same sentence."),

dict(id="t3-Dr-rep-02", arm="D-rule", domain="report",
 before="""Peat Depth Note — Ryhope Moss, Restoration Block C

Depths were probed on a hundred-metre grid across the restoration block and compared with the baseline probed at the time the dams were built. Peat is gaining across the block at 8 millimetres a year on the grid mean, so the mean depth of 1,240 millimetres probed this summer projects to 1,248 millimetres next summer, 1,256 the year after and 1,264 the year after that. The restoration target of 1,300 millimetres is reached in the eighth year on this projection. Probing was done with a graduated rod to refusal, three readings within a metre at each grid point. Pool cover across the block has continued to spread and is mapped separately from the aerial survey flown in June.""",
 old="at 8 millimetres a year on the grid mean, so the mean depth of 1,240 millimetres probed this summer projects to 1,248 millimetres next summer, 1,256 the year after and 1,264 the year after that. The restoration target of 1,300 millimetres is reached in the eighth year on this projection.",
 new="at 20 millimetres a year on the grid mean, so the mean depth of 1,240 millimetres probed this summer projects to 1,260 millimetres next summer, 1,280 the year after and 1,300 the year after that. The restoration target of 1,300 millimetres is reached in the third year on this projection.",
 site="The change is in the second sentence and the sentence immediately after it, where the yearly gain in depth is given.",
 note="Only the yearly step by which peat depth gains changes, together with the three projected depths and the target year worked from it in the following sentence."),

dict(id="t3-Dr-rep-03", arm="D-rule", domain="report",
 before="""Footfall Note — Harnbeck Museum, Winter Quarter

Beam counters at the two entrances were checked against a manual tally on three separate afternoons before the quarter opened. Counter totals were turned into visitor numbers by halving the beam count, to allow for entry and exit on the same beam, and then adding 4 in every hundred for pushchairs and wheelchairs passing as one, so the west door total of 40,000 beams gives 20,800 visitors and the east door total of 15,000 gives 7,800. The quarter total is the sum of the two doors. Counters were cleaned at the mid-quarter visit and the alignment was checked at the same time. The school group entrance is counted separately by the bookings desk and is not included in these figures.""",
 old="then adding 4 in every hundred for pushchairs and wheelchairs passing as one, so the west door total of 40,000 beams gives 20,800 visitors and the east door total of 15,000 gives 7,800",
 new="then adding 12 in every hundred for pushchairs and wheelchairs passing as one, so the west door total of 40,000 beams gives 22,400 visitors and the east door total of 15,000 gives 8,400",
 site="The change is in the second sentence, in the passage that turns a beam count into a visitor number.",
 note="Only the allowance added to the halved beam count changes, together with the two worked visitor numbers stated in the same sentence."),

dict(id="t3-Dr-rep-04", arm="D-rule", domain="report",
 before="""Fisheries Note — Bewick Beck Eel Trap, Five-Year Review

The trap at the mill sluice has been fished on the same nights each spring since the review period opened, with the same crew and the same gear. The run is falling at 15 per cent a year on the trap index, so the index of 400 counted this spring projects to 340 next spring, 289 the year after and 246 the year after that. The intervention threshold agreed with the trust is an index of 200, which on this projection is reached in the fifth year. Water temperature at first capture has been within a degree of the period mean in each of the five springs. The sluice gate was rehung in the second year of the period and has not been altered since.""",
 old="falling at 15 per cent a year on the trap index, so the index of 400 counted this spring projects to 340 next spring, 289 the year after and 246 the year after that. The intervention threshold agreed with the trust is an index of 200, which on this projection is reached in the fifth year.",
 new="falling at 30 per cent a year on the trap index, so the index of 400 counted this spring projects to 280 next spring, 196 the year after and 137 the year after that. The intervention threshold agreed with the trust is an index of 200, which on this projection is reached in the second year.",
 site="The change is in the second sentence and the sentence immediately after it, where the yearly fall in the index is given.",
 note="Only the yearly step by which the index falls changes, together with the three projected indices and the threshold year worked from it in the following sentence."),

dict(id="t3-Dr-rep-05", arm="D-rule", domain="report",
 before="""Energy Note — Bellhaven Leisure Centre, Pool Hall Submeter

The submeter on the pool hall circuit gives a pulse output that is logged by the building panel at fifteen-minute intervals. Pulse counts were turned into units by multiplying by 0.5 kilowatt hours per pulse, so the January count of 96,000 pulses gives 48,000 units and the February count of 72,000 gives 36,000 units. The two months together account for a little under half of the centre's winter consumption. The meter was read manually at the start and end of each month and the manual reading agreed with the logged total on both occasions. A second submeter is to be fitted on the changing block circuit before the next heating season.""",
 old="multiplying by 0.5 kilowatt hours per pulse, so the January count of 96,000 pulses gives 48,000 units and the February count of 72,000 gives 36,000 units",
 new="multiplying by 0.2 kilowatt hours per pulse, so the January count of 96,000 pulses gives 19,200 units and the February count of 72,000 gives 14,400 units",
 site="The change is in the second sentence, in the passage that turns a pulse count into units.",
 note="Only the units allowed per pulse change, together with the two worked unit totals stated in the same sentence."),
]

ITEMS += [
# --------------------------------------------------------------- process (4)
dict(id="t3-Dr-proc-01", arm="D-rule", domain="process",
 before="""Weld Inspection — Baxendale Engineering, Fabrication Bay

1. Clean the weld and the parent metal either side to bright metal for fifty millimetres.
2. Apply the penetrant and leave it for the dwell time printed on the tin.
3. Remove the excess, apply the developer, and read the weld after ten minutes.
4. Count the indications along the weld and note the length of each.
5. Turn the count into an acceptance class by dividing the number of indications by 3 and rounding up, so a weld with 7 indications takes class 3 and one with 2 indications takes class 1.
6. Accept welds in class one and two; refer class three and above to the welding engineer.
7. Photograph any weld referred to the engineer with the scale bar in frame.
8. Note the class, the count, and the reading time on the inspection sheet.
9. Clean the developer from the weld before the item leaves the bay.""",
 old="dividing the number of indications by 3 and rounding up, so a weld with 7 indications takes class 3 and one with 2 indications takes class 1",
 new="dividing the number of indications by 6 and rounding up, so a weld with 7 indications takes class 2 and one with 2 indications takes class 1",
 site="The change is in step five, in the passage that turns a count of indications into an acceptance class.",
 note="Only the divisor applied to the count of indications changes, together with the worked classes stated in the same step."),

dict(id="t3-Dr-proc-02", arm="D-rule", domain="process",
 before="""Chlorine Dosing — Marchgate Service Reservoir

1. Draw a sample from the outlet tapping and read the residual on the bench comparator.
2. Note the residual and the sample time on the dosing sheet.
3. Set the top-up dose from the residual, allowing for a loss of a fifth of the residual each day, so a reading of 0.50 falls to 0.40 after one day, 0.32 after two and 0.26 after three.
4. Confirm that the projected residual stays above the works minimum until the next visit.
5. Dose at the injection point with the pump set to the calculated rate.
6. Wait thirty minutes and draw a second sample from the same tapping.
7. Note the second reading beside the first on the dosing sheet.
8. Report any reading below the works minimum to the duty manager before leaving site.
9. Lock the kiosk and return the comparator to the van case.""",
 old="allowing for a loss of a fifth of the residual each day, so a reading of 0.50 falls to 0.40 after one day, 0.32 after two and 0.26 after three",
 new="allowing for a loss of a half of the residual each day, so a reading of 0.50 falls to 0.25 after one day, 0.13 after two and 0.06 after three",
 site="The change is in step three, in the passage that says how the residual moves from one day to the next.",
 note="Only the daily loss step applied to the residual changes, together with the three worked residuals stated in the same step."),

dict(id="t3-Dr-proc-03", arm="D-rule", domain="process",
 before="""Soil Sampling — Ardley Farm, Nutrient Round

1. Walk the field on a W pattern and take twenty-five cores to spade depth.
2. Combine the cores in the bucket and mix them thoroughly before bagging.
3. Label the bag with the field name, the date, and the sampling depth.
4. Send the bag to the laboratory with the submission sheet the same week.
5. Turn the returned milligrammes per litre into an index by dividing by 15 and rounding down, so a return of 46 gives index 3 and a return of 28 gives index 1.
6. Compare the index with the target for the crop in the coming rotation.
7. Note the index against the field on the nutrient plan.
8. Order lime where the pH returned is below the figure set for the soil type.
9. Repeat the round on the same fields in four years.""",
 old="dividing by 15 and rounding down, so a return of 46 gives index 3 and a return of 28 gives index 1",
 new="dividing by 9 and rounding down, so a return of 46 gives index 5 and a return of 28 gives index 3",
 site="The change is in step five, in the passage that turns a laboratory return into an index.",
 note="Only the divisor applied to the laboratory return changes, together with the two worked indices stated in the same step."),

dict(id="t3-Dr-proc-04", arm="D-rule", domain="process",
 before="""Ladder Inspection — Ardwick Depot, Access Equipment

1. Lay the ladder flat on the trestles in the inspection bay.
2. Check the stiles, the rungs, the feet and the tie rods against the illustrated sheet.
3. Mark the ladder with the coloured tag for the quarter just begun.
4. Set the next inspection by doubling the interval each time the ladder passes two rounds running, so a ladder starting on a 3-month interval moves to 6 months and then to 12 months.
5. Enter the new interval against the ladder number in the equipment register.
6. Withdraw any ladder that has not passed and move it to the quarantine rack.
7. Tell the depot manager the same day where a ladder is withdrawn.
8. Return passed ladders to the rack with the tag visible from the gangway.
9. Send the register extract to the safety officer at the end of each quarter.""",
 old="doubling the interval each time the ladder passes two rounds running, so a ladder starting on a 3-month interval moves to 6 months and then to 12 months",
 new="adding two months to the interval each time the ladder passes two rounds running, so a ladder starting on a 3-month interval moves to 5 months and then to 7 months",
 site="The change is in step four, in the passage that says how the inspection interval moves after a pass.",
 note="Only the step by which the inspection interval lengthens changes, together with the two worked intervals stated in the same step."),
]
