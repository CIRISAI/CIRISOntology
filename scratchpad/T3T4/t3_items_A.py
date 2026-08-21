# -*- coding: utf-8 -*-
"""ARM A (30) — the ONLY change is an A-type applied conversion: the mapping
from evidence/observation to conclusion.  The mapping is USED to derive content
that appears in the artifact, and every derived value moves with it inside one
contiguous span."""

ITEMS = [

# ---------------------------------------------------------------- policy (6)
dict(id="t3-A-pol-01", arm="A", domain="policy",
 before="""Fennimore Trust — Small Grants Assessment Policy

Applications to the small grants fund are read by two assessors working independently, each of whom marks the application against the four published headings. Marks under each heading run from nought to ten, and the two sheets are added together to give a raw total out of eighty. The raw total is turned into an award band by dividing it by 4 and rounding down to the nearest whole number, so an application scoring 46 sits in band 11 and an application scoring 58 sits in band 14. Bands of twelve and above are put to the awards meeting; the remainder are answered by letter within ten working days. Where the two assessors differ by more than fifteen marks on the raw total, a third assessor reads the application and the middle sheet of the three is used. The awards meeting sits on the first Thursday of each quarter and may hold an application over to the following quarter once.""",
 old="dividing it by 4 and rounding down to the nearest whole number, so an application scoring 46 sits in band 11 and an application scoring 58 sits in band 14",
 new="dividing it by 5 and rounding down to the nearest whole number, so an application scoring 46 sits in band 9 and an application scoring 58 sits in band 11",
 site="The change is in the third sentence, in the passage that turns a raw total into an award band.",
 note="Only the arithmetic that converts a raw total into a band changes, together with the two worked bands stated in the same sentence; both worked bands are recomputed under the later arithmetic."),

dict(id="t3-A-pol-02", arm="A", domain="policy",
 before="""Calder District Council — Food Hygiene Grading Policy

Officers inspect food businesses against the three headings on the national sheet and award demerit points under each. The points are added to give a shop total, which is then turned into a public letter grade: the total is divided by 10 and rounded up, and the answer is read off the letter table where one gives A, two gives B, three gives C and four or more gives D. A shop carrying 24 demerit points therefore takes grade C, and one carrying 8 points takes grade A. Grades are published within twenty-eight days of the visit and are displayed at the entrance to the shop. A proprietor may ask for a re-visit once the matters raised have been dealt with, and the re-visit is charged at the published rate. Where a shop is closed voluntarily during the visit, no grade is published until the re-visit has taken place.""",
 old="divided by 10 and rounded up, and the answer is read off the letter table where one gives A, two gives B, three gives C and four or more gives D. A shop carrying 24 demerit points therefore takes grade C, and one carrying 8 points takes grade A.",
 new="divided by 6 and rounded up, and the answer is read off the letter table where one gives A, two gives B, three gives C and four or more gives D. A shop carrying 24 demerit points therefore takes grade D, and one carrying 8 points takes grade B.",
 site="The change is in the third sentence, in the passage that turns a demerit total into a published letter grade.",
 note="Only the divisor applied to the demerit total changes, together with the two worked grades that follow from it in the same passage."),

dict(id="t3-A-pol-03", arm="A", domain="policy",
 before="""Wexbury Borough Council — Noise Assessment Policy

Where a complaint about amplified music is made, an officer takes a reading at the boundary of the complainant's dwelling with a class one meter over a period of five minutes. The reading is converted to an assessment level by subtracting the background level measured earlier the same evening and adding a correction of 4 decibels for tonal content, so a reading of 62 against a background of 45 gives an assessment level of 21, and a reading of 55 against the same background gives 14. Assessment levels of twenty and above are dealt with by notice; levels below twenty are dealt with by letter in the first instance. Officers carry a calibrator and check the meter before and after each visit, noting both checks on the visit sheet. Readings taken during rainfall are set aside and the visit is repeated on a dry evening within the following fortnight.""",
 old="adding a correction of 4 decibels for tonal content, so a reading of 62 against a background of 45 gives an assessment level of 21, and a reading of 55 against the same background gives 14",
 new="adding a correction of 9 decibels for tonal content, so a reading of 62 against a background of 45 gives an assessment level of 26, and a reading of 55 against the same background gives 19",
 site="The change is in the second sentence, in the passage that converts a meter reading into an assessment level.",
 note="Only the tonal correction applied to the reading changes, together with the two worked assessment levels stated in the same sentence."),

dict(id="t3-A-pol-04", arm="A", domain="policy",
 before="""Baxendale Engineering — Apprentice Assessment Policy

Each apprentice is observed at the bench on eight set tasks during the second year, and the supervising engineer marks every task as met, partly met, or not met. The marks are turned into a stage number by counting 2 for each task met and 1 for each task partly met, then halving the total and rounding down, so an apprentice with five met and two partly met reaches stage 6, while one with three met and three partly met reaches stage 4. Stage five is the threshold for entry to the third year. Observations are spread across at least four separate weeks so that a single poor week does not decide the outcome. The supervising engineer keeps the marked sheets in the workshop file and gives the apprentice a copy at the end of each observed week. An apprentice below the threshold repeats the second year in part, on a plan agreed with the training officer.""",
 old="counting 2 for each task met and 1 for each task partly met, then halving the total and rounding down, so an apprentice with five met and two partly met reaches stage 6, while one with three met and three partly met reaches stage 4",
 new="counting 3 for each task met and 2 for each task partly met, then halving the total and rounding down, so an apprentice with five met and two partly met reaches stage 9, while one with three met and three partly met reaches stage 7",
 site="The change is in the second sentence, in the passage that turns bench observations into a stage number.",
 note="Only the weights applied to observed tasks change, together with the two worked stage numbers that follow from them in the same sentence."),

dict(id="t3-A-pol-05", arm="A", domain="policy",
 before="""Ardley Housing Partnership — Allocation Assessment Policy

An application to the housing list is assessed against the six published headings, and points are awarded under each by the assessment team. The points from all six headings are added and the sum is turned into a lettered group by taking the square root of the total, rounding down, and reading the answer against the group table, so an application holding 49 points falls in group 7 and one holding 20 points falls in group 4. Groups six and above are offered properties as they become free, in date order within the group. Applications are reassessed every twelve months, or sooner where the household writes in with a change of address, household size, or medical need. The team writes to every applicant with the group reached and the reasons for it. An applicant may ask for the assessment to be looked at again by a second officer within twenty-eight days of that letter.""",
 old="taking the square root of the total, rounding down, and reading the answer against the group table, so an application holding 49 points falls in group 7 and one holding 20 points falls in group 4",
 new="dividing the total by 6, rounding down, and reading the answer against the group table, so an application holding 49 points falls in group 8 and one holding 20 points falls in group 3",
 site="The change is in the second sentence, in the passage that turns a points sum into a lettered group.",
 note="Only the arithmetic that turns a points sum into a group changes, together with the two worked groups stated in the same sentence."),

dict(id="t3-A-pol-06", arm="A", domain="policy",
 before="""Harnbeck Museum — Object Condition Assessment Policy

Every object coming into the store is examined by a conservator against five headings, each marked from one to four, where four is the soundest. The five marks are turned into a handling class by adding them, subtracting 5, and then dividing by 3 and rounding up, so an object marked four across the board reaches class 5, and one marked two across the board reaches class 2. Objects in class four and above may be handled by trained volunteers; objects below that are handled by conservation staff only. The examination is repeated whenever an object is taken out for display and whenever it returns to the store. Conservators write the marks on the object sheet in pencil and initial the entry. Where an object cannot be examined without disturbing an existing mount, the examination is deferred and the sheet is annotated to that effect.""",
 old="adding them, subtracting 5, and then dividing by 3 and rounding up, so an object marked four across the board reaches class 5, and one marked two across the board reaches class 2",
 new="adding them, subtracting 4, and then dividing by 2 and rounding up, so an object marked four across the board reaches class 8, and one marked two across the board reaches class 3",
 site="The change is in the second sentence, in the passage that turns five condition marks into a handling class.",
 note="Only the arithmetic that turns five marks into a handling class changes, together with the two worked classes stated in the same sentence."),

# ---------------------------------------------------------------- config (6)
dict(id="t3-A-cfg-01", arm="A", domain="config",
 before="""# Bewick Beck gauging station — reading conversion
station_id = "BW-114"
sample_seconds = 60
stage_zero_m = 0.412

# stage is turned into flow by the two values below
flow_coefficient = 2.65
flow_exponent = 1.50
# flow at the three notice heights, worked from the two values above
flow_at_0_50_m = 0.937
flow_at_1_00_m = 2.650
flow_at_2_00_m = 7.495

notice_height_m = 1.00
alarm_height_m = 2.00
telemetry_minutes = 15
operator = "Bewick catchment team\"""",
 old="""flow_coefficient = 2.65
flow_exponent = 1.50
# flow at the three notice heights, worked from the two values above
flow_at_0_50_m = 0.937
flow_at_1_00_m = 2.650
flow_at_2_00_m = 7.495""",
 new="""flow_coefficient = 4.20
flow_exponent = 1.50
# flow at the three notice heights, worked from the two values above
flow_at_0_50_m = 1.485
flow_at_1_00_m = 4.200
flow_at_2_00_m = 11.879""",
 site="The change is in the six-line block that begins with the flow coefficient.",
 note="Only the coefficient that converts stage to flow changes, together with the three worked flows immediately beneath it, which are recomputed under the later coefficient."),

dict(id="t3-A-cfg-02", arm="A", domain="config",
 before="""# Marchgate intake — turbidity sensor conversion
sensor_tag = "TB-07"
sample_seconds = 30
warmup_seconds = 120

# volts are turned into turbidity units by the slope and offset below
volts_to_ntu_slope = 40.0
volts_to_ntu_offset = -2.0
# unit values at the three cut points, worked from the two values above
ntu_at_0_25_v = 8.0
ntu_at_0_50_v = 18.0
ntu_at_1_00_v = 38.0

advisory_ntu = 18.0
shutdown_ntu = 38.0
log_path = "/var/log/marchgate/turbidity.log"
retain_days = 90""",
 old="""volts_to_ntu_slope = 40.0
volts_to_ntu_offset = -2.0
# unit values at the three cut points, worked from the two values above
ntu_at_0_25_v = 8.0
ntu_at_0_50_v = 18.0
ntu_at_1_00_v = 38.0""",
 new="""volts_to_ntu_slope = 25.0
volts_to_ntu_offset = -2.0
# unit values at the three cut points, worked from the two values above
ntu_at_0_25_v = 4.25
ntu_at_0_50_v = 10.5
ntu_at_1_00_v = 23.0""",
 site="The change is in the six-line block that begins with the volts-to-units slope.",
 note="Only the slope converting sensor volts to turbidity units changes, together with the three worked unit values beneath it."),

dict(id="t3-A-cfg-03", arm="A", domain="config",
 before="""# Ryhope glasshouse — soil moisture bench
node_id = "GH-3"
adc_bits = 12
read_interval_seconds = 300

# raw counts are turned into percent by the two values below
counts_dry = 3200
counts_wet = 1200
# percent at three stored raw counts, worked from the two values above
percent_at_2800 = 20.0
percent_at_2200 = 50.0
percent_at_1600 = 80.0

irrigate_below_percent = 20.0
stop_above_percent = 50.0
valve_seconds = 45
alert_email = "glasshouse@ryhope.example\"""",
 old="""counts_dry = 3200
counts_wet = 1200
# percent at three stored raw counts, worked from the two values above
percent_at_2800 = 20.0
percent_at_2200 = 50.0
percent_at_1600 = 80.0""",
 new="""counts_dry = 3600
counts_wet = 1200
# percent at three stored raw counts, worked from the two values above
percent_at_2800 = 33.3
percent_at_2200 = 58.3
percent_at_1600 = 83.3""",
 site="The change is in the six-line block that begins with the dry-end count.",
 note="Only the dry-end anchor count changes, together with the three worked moisture percentages beneath it, which are recomputed against the later anchor."),

dict(id="t3-A-cfg-04", arm="A", domain="config",
 before="""# Fenwick roadside cabinet — index conversion
cabinet = "FW-2"
averaging_minutes = 60
zero_check_hour = 3

# concentration is turned into an index number by the divisor below
ppb_per_index_point = 16
index_cap = 10
# index at three stored hourly means, worked from the divisor above
index_at_32_ppb = 2
index_at_96_ppb = 6
index_at_160_ppb = 10

advisory_index = 6
board_message_index = 8
feed_seconds = 900
retain_days = 400""",
 old="""ppb_per_index_point = 16
index_cap = 10
# index at three stored hourly means, worked from the divisor above
index_at_32_ppb = 2
index_at_96_ppb = 6
index_at_160_ppb = 10""",
 new="""ppb_per_index_point = 32
index_cap = 10
# index at three stored hourly means, worked from the divisor above
index_at_32_ppb = 1
index_at_96_ppb = 3
index_at_160_ppb = 5""",
 site="The change is in the six-line block that begins with the concentration-per-index-point divisor.",
 note="Only the divisor converting concentration to an index number changes, together with the three worked index values beneath it."),

dict(id="t3-A-cfg-05", arm="A", domain="config",
 before="""# Ardwick weighbridge — load cell conversion
bridge_id = "WB-1"
cells = 4
settle_seconds = 8

# cell counts are turned into kilogrammes by the factor and tare below
kg_per_count = 0.250
tare_counts = 1600
# kilogrammes at three stored count totals, worked from the two values above
kg_at_4000_counts = 600.0
kg_at_9600_counts = 2000.0
kg_at_20000_counts = 4600.0

ticket_minimum_kg = 600.0
axle_limit_kg = 11500.0
printer = "gate-2"
retain_days = 1825""",
 old="""kg_per_count = 0.250
tare_counts = 1600
# kilogrammes at three stored count totals, worked from the two values above
kg_at_4000_counts = 600.0
kg_at_9600_counts = 2000.0
kg_at_20000_counts = 4600.0""",
 new="""kg_per_count = 0.400
tare_counts = 1600
# kilogrammes at three stored count totals, worked from the two values above
kg_at_4000_counts = 960.0
kg_at_9600_counts = 3200.0
kg_at_20000_counts = 7360.0""",
 site="The change is in the six-line block that begins with the kilogrammes-per-count factor.",
 note="Only the factor converting cell counts to kilogrammes changes, together with the three worked weights beneath it."),

dict(id="t3-A-cfg-06", arm="A", domain="config",
 before="""# Thornbury sports hall — lighting bench
controller = "LX-9"
poll_seconds = 20
fade_seconds = 6

# measured lux is turned into a dimming step by the divisor and floor below
lux_per_step = 50
step_floor = 1
# steps at three stored readings, worked from the two values above
step_at_100_lux = 2
step_at_400_lux = 8
step_at_750_lux = 15

hold_step = 8
night_step = 2
sensor_height_m = 7.5
zone = "main court\"""",
 old="""lux_per_step = 50
step_floor = 1
# steps at three stored readings, worked from the two values above
step_at_100_lux = 2
step_at_400_lux = 8
step_at_750_lux = 15""",
 new="""lux_per_step = 125
step_floor = 1
# steps at three stored readings, worked from the two values above
step_at_100_lux = 1
step_at_400_lux = 3
step_at_750_lux = 6""",
 site="The change is in the six-line block that begins with the lux-per-step divisor.",
 note="Only the divisor converting measured lux to a dimming step changes, together with the three worked steps beneath it."),
]

ITEMS += [
# ------------------------------------------------------------------ code (6)
dict(id="t3-A-code-01", arm="A", domain="code",
 before='''"""Sound level banding for the Wexbury visit sheets."""

# a measured level is turned into a band by the offset and width below
BAND_OFFSET_DB = 40
BAND_WIDTH_DB = 5
# bands for the three levels held on the sheet, worked from the two values above
BAND_AT_52_DB = 3
BAND_AT_63_DB = 5
BAND_AT_71_DB = 7


def band_for(level_db):
    if level_db <= BAND_OFFSET_DB:
        return 0
    return int((level_db - BAND_OFFSET_DB) // BAND_WIDTH_DB) + 1


def sheet_bands(levels):
    return [band_for(v) for v in levels]''',
 old='''BAND_OFFSET_DB = 40
BAND_WIDTH_DB = 5
# bands for the three levels held on the sheet, worked from the two values above
BAND_AT_52_DB = 3
BAND_AT_63_DB = 5
BAND_AT_71_DB = 7''',
 new='''BAND_OFFSET_DB = 40
BAND_WIDTH_DB = 8
# bands for the three levels held on the sheet, worked from the two values above
BAND_AT_52_DB = 2
BAND_AT_63_DB = 3
BAND_AT_71_DB = 4''',
 site="The change is in the six-line block that begins with the band offset near the top of the file.",
 note="Only the band width applied to a measured level changes, together with the three worked bands beneath it, which are recomputed under the later width."),

dict(id="t3-A-code-02", arm="A", domain="code",
 before='''"""Millivolt readings from the Harnbeck bench probe, turned into pH."""

# a probe reading is turned into pH by the pair below
MV_AT_PH7 = 0.0
MV_PER_PH = -59.0
# pH for the three stored bench readings, worked from the pair above
PH_AT_MINUS_118_MV = 9.0
PH_AT_ZERO_MV = 7.0
PH_AT_177_MV = 4.0


def ph_from_mv(mv):
    return round(7.0 + (mv - MV_AT_PH7) / MV_PER_PH, 2)


def bench_series(readings):
    return [ph_from_mv(mv) for mv in readings]''',
 old='''MV_PER_PH = -59.0
# pH for the three stored bench readings, worked from the pair above
PH_AT_MINUS_118_MV = 9.0
PH_AT_ZERO_MV = 7.0
PH_AT_177_MV = 4.0''',
 new='''MV_PER_PH = -29.5
# pH for the three stored bench readings, worked from the pair above
PH_AT_MINUS_118_MV = 11.0
PH_AT_ZERO_MV = 7.0
PH_AT_177_MV = 1.0''',
 site="The change is in the five-line block that begins with the millivolts-per-pH constant.",
 note="Only the millivolts-per-pH constant changes, together with the three worked pH values beneath it."),

dict(id="t3-A-code-03", arm="A", domain="code",
 before='''"""Pulse totals from the Eastgate meter, turned into litres."""

# pulses are turned into litres by the factor and offset below
LITRES_PER_PULSE = 0.5
OFFSET_PULSES = 20
# litres for the three totals held in the daily file, worked from the values above
LITRES_AT_120_PULSES = 50.0
LITRES_AT_520_PULSES = 250.0
LITRES_AT_1020_PULSES = 500.0


def litres_for(pulses):
    return (pulses - OFFSET_PULSES) * LITRES_PER_PULSE


def daily_totals(counts):
    return [litres_for(c) for c in counts]''',
 old='''LITRES_PER_PULSE = 0.5
OFFSET_PULSES = 20
# litres for the three totals held in the daily file, worked from the values above
LITRES_AT_120_PULSES = 50.0
LITRES_AT_520_PULSES = 250.0
LITRES_AT_1020_PULSES = 500.0''',
 new='''LITRES_PER_PULSE = 0.2
OFFSET_PULSES = 20
# litres for the three totals held in the daily file, worked from the values above
LITRES_AT_120_PULSES = 20.0
LITRES_AT_520_PULSES = 100.0
LITRES_AT_1020_PULSES = 200.0''',
 site="The change is in the six-line block that begins with the litres-per-pulse factor.",
 note="Only the litres-per-pulse factor changes, together with the three worked litre totals beneath it."),

dict(id="t3-A-code-04", arm="A", domain="code",
 before='''"""Site visit scores from the Calder sheets, turned into a written class."""

# a summed sheet score is turned into a class by the two cut points below
CLASS_B_ABOVE = 12
CLASS_C_ABOVE = 24
# classes for the three totals kept on file, worked from the cut points above
CLASS_AT_9 = "A"
CLASS_AT_18 = "B"
CLASS_AT_30 = "C"


def class_for(total):
    if total > CLASS_C_ABOVE:
        return "C"
    if total > CLASS_B_ABOVE:
        return "B"
    return "A"


def file_classes(totals):
    return [class_for(t) for t in totals]''',
 old='''CLASS_B_ABOVE = 12
CLASS_C_ABOVE = 24
# classes for the three totals kept on file, worked from the cut points above
CLASS_AT_9 = "A"
CLASS_AT_18 = "B"
CLASS_AT_30 = "C"''',
 new='''CLASS_B_ABOVE = 6
CLASS_C_ABOVE = 15
# classes for the three totals kept on file, worked from the cut points above
CLASS_AT_9 = "B"
CLASS_AT_18 = "C"
CLASS_AT_30 = "C"''',
 site="The change is in the six-line block that begins with the first of the two cut points.",
 note="Only the two cut points applied to a summed sheet score change, together with the worked classes beneath them, which are recomputed under the later cut points."),

dict(id="t3-A-code-05", arm="A", domain="code",
 before='''"""Resistance readings from the Bewick store probe, turned into moisture percent."""

import math

# resistance in kilohms is turned into percent by the pair below
LOG_SLOPE = -6.0
LOG_INTERCEPT = 26.0
# percent for the three stored probe readings, worked from the pair above
PERCENT_AT_10_KOHM = 20.0
PERCENT_AT_100_KOHM = 14.0
PERCENT_AT_1000_KOHM = 8.0


def percent_for(kohm):
    return round(LOG_INTERCEPT + LOG_SLOPE * math.log10(kohm), 1)


def store_series(readings):
    return [percent_for(r) for r in readings]''',
 old='''LOG_SLOPE = -6.0
LOG_INTERCEPT = 26.0
# percent for the three stored probe readings, worked from the pair above
PERCENT_AT_10_KOHM = 20.0
PERCENT_AT_100_KOHM = 14.0
PERCENT_AT_1000_KOHM = 8.0''',
 new='''LOG_SLOPE = -4.0
LOG_INTERCEPT = 26.0
# percent for the three stored probe readings, worked from the pair above
PERCENT_AT_10_KOHM = 22.0
PERCENT_AT_100_KOHM = 18.0
PERCENT_AT_1000_KOHM = 14.0''',
 site="The change is in the six-line block that begins with the log slope.",
 note="Only the slope converting probe resistance to moisture percent changes, together with the three worked percentages beneath it."),

dict(id="t3-A-code-06", arm="A", domain="code",
 before='''"""Returned questionnaire sheets from the Ravensworth survey, turned into an index."""

# answers are turned into an index by the weight and base below
WEIGHT_PER_AGREE = 4
INDEX_BASE = 10
# index for the three returned sheets, worked from the weight and base above
INDEX_SHEET_11 = 26
INDEX_SHEET_12 = 38
INDEX_SHEET_13 = 18

AGREE_COUNTS = {"11": 4, "12": 7, "13": 2}


def index_for(sheet):
    return INDEX_BASE + WEIGHT_PER_AGREE * AGREE_COUNTS[sheet]


def all_indices():
    return {k: index_for(k) for k in sorted(AGREE_COUNTS)}''',
 old='''WEIGHT_PER_AGREE = 4
INDEX_BASE = 10
# index for the three returned sheets, worked from the weight and base above
INDEX_SHEET_11 = 26
INDEX_SHEET_12 = 38
INDEX_SHEET_13 = 18''',
 new='''WEIGHT_PER_AGREE = 7
INDEX_BASE = 10
# index for the three returned sheets, worked from the weight and base above
INDEX_SHEET_11 = 38
INDEX_SHEET_12 = 59
INDEX_SHEET_13 = 24''',
 site="The change is in the six-line block that begins with the weight given to each agreeing answer.",
 note="Only the weight given to an agreeing answer changes, together with the three worked sheet indices beneath it."),

# ---------------------------------------------------------------- report (6)
dict(id="t3-A-rep-01", arm="A", domain="report",
 before="""Bat Activity Survey — Ryhope Carr, Summer Season

Detectors were left at six points along the carr from the last week of May until the second week of August, and recordings were checked by two workers against the reference library. Passes were counted for each point and converted to an activity figure by dividing the pass count by the number of detector nights and then multiplying by 10, so point three with 84 passes over 28 nights returns an activity figure of 30, and point five with 45 passes over 30 nights returns 15. Points returning an activity figure above twenty are treated as main commuting lines and are shown on the plan attached to this note. Weather was settled through June and broken through July, and four nights were lost to heavy rain at point two. The survey follows the same layout as the previous season so that the two can be read side by side.""",
 old="dividing the pass count by the number of detector nights and then multiplying by 10, so point three with 84 passes over 28 nights returns an activity figure of 30, and point five with 45 passes over 30 nights returns 15",
 new="dividing the pass count by the number of detector nights and then multiplying by 4, so point three with 84 passes over 28 nights returns an activity figure of 12, and point five with 45 passes over 30 nights returns 6",
 site="The change is in the second sentence, in the passage that converts pass counts into an activity figure.",
 note="Only the multiplier applied to the nightly pass rate changes, together with the two worked activity figures stated in the same sentence."),

dict(id="t3-A-rep-02", arm="A", domain="report",
 before="""Monitoring Note — Corrie Viaduct, Spans 3 and 4

Gauges were fixed to the lower flange at mid-span on both spans and read under a loaded test train run at walking pace. Microstrain readings were turned into stress by multiplying by an elastic constant of 205 kilonewtons per square millimetre and dividing by one thousand, so the 260 microstrain reading at span three gives 53.3 newtons per square millimetre and the 180 microstrain reading at span four gives 36.9. Both figures sit below the working limit for the section, which the design sheet gives as 120. Readings were repeated on the return run and agreed within four microstrain at every gauge. The gauges will stay in place until the next principal inspection so that the same points can be read again under a comparable load.""",
 old="multiplying by an elastic constant of 205 kilonewtons per square millimetre and dividing by one thousand, so the 260 microstrain reading at span three gives 53.3 newtons per square millimetre and the 180 microstrain reading at span four gives 36.9",
 new="multiplying by an elastic constant of 70 kilonewtons per square millimetre and dividing by one thousand, so the 260 microstrain reading at span three gives 18.2 newtons per square millimetre and the 180 microstrain reading at span four gives 12.6",
 site="The change is in the second sentence, in the passage that converts microstrain into stress.",
 note="Only the elastic constant applied to the gauge readings changes, together with the two worked stresses stated in the same sentence."),

dict(id="t3-A-rep-03", arm="A", domain="report",
 before="""Laboratory Note — Marchgate Intake, Phosphate Determination

Samples were drawn from the intake on three mornings and read on the bench spectrophotometer at 880 nanometres against a reagent blank. Absorbance was turned into concentration by multiplying by 1.60 and expressing the answer in milligrammes per litre, so the Tuesday absorbance of 0.150 gives 0.240, the Wednesday absorbance of 0.075 gives 0.120, and the Thursday absorbance of 0.300 gives 0.480. The bench standard was read at the start and the end of each run and agreed within two parts in a hundred. Samples were held at four degrees and read within six hours of drawing. The Thursday sample was drawn after two days of rain, which the catchment team expects to lift the reading.""",
 old="multiplying by 1.60 and expressing the answer in milligrammes per litre, so the Tuesday absorbance of 0.150 gives 0.240, the Wednesday absorbance of 0.075 gives 0.120, and the Thursday absorbance of 0.300 gives 0.480",
 new="multiplying by 2.00 and expressing the answer in milligrammes per litre, so the Tuesday absorbance of 0.150 gives 0.300, the Wednesday absorbance of 0.075 gives 0.150, and the Thursday absorbance of 0.300 gives 0.600",
 site="The change is in the second sentence, in the passage that converts absorbance into concentration.",
 note="Only the multiplier applied to absorbance changes, together with the three worked concentrations stated in the same sentence."),

dict(id="t3-A-rep-04", arm="A", domain="report",
 before="""Traffic Count Note — Bramley Lane, Spring Week

Two pneumatic tubes were laid across the carriageway north of the junction and left in place for seven days. Axle hits were logged in fifteen-minute bins and turned into vehicle counts by dividing the axle total by two and then subtracting 5 in every hundred to allow for multi-axle goods traffic, so the Tuesday total of 8,400 axle hits gives 3,990 vehicles and the Sunday total of 3,200 gives 1,520. The weekday daily mean over the five working days was close to the figure counted on the same length three years ago. One tube was struck by a mower on the Thursday morning and was replaced within the hour; the affected bin has been left out of the daily totals.""",
 old="dividing the axle total by two and then subtracting 5 in every hundred to allow for multi-axle goods traffic, so the Tuesday total of 8,400 axle hits gives 3,990 vehicles and the Sunday total of 3,200 gives 1,520",
 new="dividing the axle total by two and then subtracting 20 in every hundred to allow for multi-axle goods traffic, so the Tuesday total of 8,400 axle hits gives 3,360 vehicles and the Sunday total of 3,200 gives 1,280",
 site="The change is in the second sentence, in the passage that turns axle hits into vehicle counts.",
 note="Only the goods-traffic allowance applied to the halved axle total changes, together with the two worked vehicle counts stated in the same sentence."),

dict(id="t3-A-rep-05", arm="A", domain="report",
 before="""Rain Gauge Note — Fenwick Estate Roof Station

The tipping bucket at the roof station was checked against a measured pour on the first of the month and the tip counter was read at nine each morning. Tip counts were turned into depth by multiplying by 0.20 millimetres per tip, so the 65 tips logged on the wettest morning give 13.0 millimetres and the 18 tips logged on the eleventh give 3.6 millimetres. The monthly total came to 71.4 millimetres over 357 tips. The funnel was cleared of moss at the mid-month visit and the counter was not disturbed. Readings from the fourteenth are shown separately because the gauge was shaded by scaffolding for two days while the parapet was repaired.""",
 old="multiplying by 0.20 millimetres per tip, so the 65 tips logged on the wettest morning give 13.0 millimetres and the 18 tips logged on the eleventh give 3.6 millimetres. The monthly total came to 71.4 millimetres over 357 tips.",
 new="multiplying by 0.50 millimetres per tip, so the 65 tips logged on the wettest morning give 32.5 millimetres and the 18 tips logged on the eleventh give 9.0 millimetres. The monthly total came to 178.5 millimetres over 357 tips.",
 site="The change is in the second sentence and the sentence immediately after it, where tip counts are turned into a depth.",
 note="Only the depth allowed per tip changes, together with the two daily depths and the monthly total worked from it in the following sentence."),

dict(id="t3-A-rep-06", arm="A", domain="report",
 before="""Timber Inspection Note — Bellhaven Roof Trusses

Readings were taken with a two-pin meter at twelve points along the tie beams, with the pins driven to a depth of twenty millimetres. Meter readings were turned into moisture percent by subtracting a temperature correction of 1 percent for every five degrees below twenty, so the reading of 22 taken at ten degrees gives 20 percent and the reading of 16 taken at five degrees gives 13 percent. Values above eighteen percent are treated as damp for the purposes of the repair schedule. The loft was unheated at the time of the visit and the outside air was near freezing. A second set of readings is planned for the same points in late summer so that the two seasons can be compared.""",
 old="subtracting a temperature correction of 1 percent for every five degrees below twenty, so the reading of 22 taken at ten degrees gives 20 percent and the reading of 16 taken at five degrees gives 13 percent",
 new="subtracting a temperature correction of 2 percent for every five degrees below twenty, so the reading of 22 taken at ten degrees gives 18 percent and the reading of 16 taken at five degrees gives 10 percent",
 site="The change is in the second sentence, in the passage that turns a meter reading into moisture percent.",
 note="Only the temperature correction applied to the meter reading changes, together with the two worked moisture percentages stated in the same sentence."),
]

ITEMS += [
# --------------------------------------------------------------- process (6)
dict(id="t3-A-proc-01", arm="A", domain="process",
 before="""Dairy Tank Dip — Ardley Farm, Morning Collection

1. Switch off the agitator and wait four minutes for the surface to settle.
2. Wipe the dipstick with the cloth kept in the parlour and lower it square to the tank floor.
3. Read the wetted length to the nearest millimetre and note it on the collection sheet.
4. Turn the dip into litres by multiplying the wetted length in millimetres by 9.4, so a dip of 300 gives 2,820 litres and a dip of 145 gives 1,363 litres.
5. Enter the litre figure against the tank number and initial the entry.
6. Rinse the dipstick under the tap and return it to the wall clip.
7. Restart the agitator before the tanker arrives.
8. Give the top copy of the sheet to the driver and keep the carbon in the parlour file.""",
 old="multiplying the wetted length in millimetres by 9.4, so a dip of 300 gives 2,820 litres and a dip of 145 gives 1,363 litres",
 new="multiplying the wetted length in millimetres by 6.0, so a dip of 300 gives 1,800 litres and a dip of 145 gives 870 litres",
 site="The change is in step four, in the passage that turns a dip into litres.",
 note="Only the multiplier applied to the wetted length changes, together with the two worked litre figures stated in the same step."),

dict(id="t3-A-proc-02", arm="A", domain="process",
 before="""Cube Test — Baxendale Site Laboratory

1. Take the cube from the curing tank and wipe the bearing faces dry.
2. Weigh the cube and note the mass on the test sheet.
3. Centre the cube in the machine so that the trowelled face is vertical.
4. Load at the steady rate marked on the dial until the cube fails, and note the peak load in kilonewtons.
5. Turn the peak load into a strength figure by dividing by 22.5 to give newtons per square millimetre, so a peak of 675 kilonewtons gives 30.0 and a peak of 900 gives 40.0.
6. Compare the strength figure with the grade called for on the pour sheet.
7. Photograph the failed cube from two sides and file the images against the pour number.
8. Clear the platens of debris before the next cube is placed.
9. Sign the test sheet and pass it to the site engineer the same day.""",
 old="dividing by 22.5 to give newtons per square millimetre, so a peak of 675 kilonewtons gives 30.0 and a peak of 900 gives 40.0",
 new="dividing by 45.0 to give newtons per square millimetre, so a peak of 675 kilonewtons gives 15.0 and a peak of 900 gives 20.0",
 site="The change is in step five, in the passage that turns a peak load into a strength figure.",
 note="Only the divisor applied to the peak load changes, together with the two worked strength figures stated in the same step."),

dict(id="t3-A-proc-03", arm="A", domain="process",
 before="""Audiometry Screening — Nettlebridge Occupational Health

1. Seat the worker in the booth and fit the headset with the red cup on the right ear.
2. Explain the response button and run two practice tones before the test proper.
3. Test each ear at the six standard frequencies and note the threshold in decibels.
4. Add the thresholds at one, two, three and four kilohertz for each ear separately.
5. Turn the sum into a category by dividing by 10 and rounding down, so a sum of 95 gives category 9 and a sum of 42 gives category 4.
6. Compare the category with the entry from the previous year held in the worker's health file.
7. Refer any worker whose category has moved by two or more to the occupational physician.
8. Print the audiogram and give a copy to the worker before they leave the booth.
9. Clean the cups with the wipes provided and leave the booth door open between appointments.""",
 old="dividing by 10 and rounding down, so a sum of 95 gives category 9 and a sum of 42 gives category 4",
 new="dividing by 25 and rounding down, so a sum of 95 gives category 3 and a sum of 42 gives category 1",
 site="The change is in step five, in the passage that turns a threshold sum into a category.",
 note="Only the divisor applied to the threshold sum changes, together with the two worked categories stated in the same step."),

dict(id="t3-A-proc-04", arm="A", domain="process",
 before="""Fuel Tank Dip — Ardwick Depot, Weekly Reconciliation

1. Lock the pump out at the isolator before opening the fill point cover.
2. Lower the dip tape until it touches the tank floor and hold it for five seconds.
3. Withdraw the tape and read the wetted mark to the nearest five millimetres.
4. Turn the dip into litres by multiplying the wetted height in centimetres by 118, so a dip of 60 centimetres gives 7,080 litres and a dip of 25 gives 2,950 litres.
5. Compare the litre figure with the pump totaliser reading taken at the same time.
6. Note both figures and the difference between them on the weekly sheet.
7. Report any difference above two hundred litres to the depot manager the same day.
8. Refit the fill point cover and restore the pump at the isolator.
9. File the weekly sheet in the depot binder with the delivery notes for the same week.""",
 old="multiplying the wetted height in centimetres by 118, so a dip of 60 centimetres gives 7,080 litres and a dip of 25 gives 2,950 litres",
 new="multiplying the wetted height in centimetres by 145, so a dip of 60 centimetres gives 8,700 litres and a dip of 25 gives 3,625 litres",
 site="The change is in step four, in the passage that turns a dip into litres.",
 note="Only the multiplier applied to the wetted height changes, together with the two worked litre figures stated in the same step."),

dict(id="t3-A-proc-05", arm="A", domain="process",
 before="""Grain Intake Sampling — Bewick Store

1. Draw three spear samples from different depths as the trailer tips.
2. Combine the three into one bag and shake it for a full minute.
3. Fill the meter cell to the mark and level it with the straight edge supplied.
4. Take three readings from the cell, emptying and refilling between each.
5. Turn the mean cell reading into moisture percent by adding 1.2 to the display figure, so a mean display of 13.8 gives 15.0 percent and a mean display of 17.3 gives 18.5 percent.
6. Note the moisture percent against the ticket number on the intake sheet.
7. Direct loads above sixteen percent to the drier rather than to the flat store.
8. Retain the combined bag for four weeks in case the load is queried.
9. Wipe the cell and the levelling edge before the next trailer is drawn.""",
 old="adding 1.2 to the display figure, so a mean display of 13.8 gives 15.0 percent and a mean display of 17.3 gives 18.5 percent",
 new="subtracting 0.4 from the display figure, so a mean display of 13.8 gives 13.4 percent and a mean display of 17.3 gives 16.9 percent",
 site="The change is in step five, in the passage that turns a mean cell reading into moisture percent.",
 note="Only the adjustment applied to the display figure changes, together with the two worked moisture percentages stated in the same step."),

dict(id="t3-A-proc-06", arm="A", domain="process",
 before="""Coating Thickness Check — Corrie Viaduct Repaint

1. Set the gauge on the calibration shim supplied with the instrument and confirm that it reads the shim value.
2. Take ten readings on each marked panel, spaced at least fifty millimetres apart.
3. Discard the highest and the lowest of the ten and take the mean of the remaining eight.
4. Turn the mean gauge figure into dry film thickness by multiplying by 0.85, so a mean of 240 microns gives 204 microns and a mean of 180 gives 153 microns.
5. Compare the dry film thickness with the figure called for in the coating schedule.
6. Mark any panel below the schedule figure with chalk for a further coat.
7. Note the panel number, the mean, and the dry film thickness on the inspection sheet.
8. Return the gauge and the shim to the case at the end of each shift.
9. Send the inspection sheet to the contract engineer at the end of each week.""",
 old="multiplying by 0.85, so a mean of 240 microns gives 204 microns and a mean of 180 gives 153 microns",
 new="multiplying by 0.60, so a mean of 240 microns gives 144 microns and a mean of 180 gives 108 microns",
 site="The change is in step four, in the passage that turns a mean gauge figure into dry film thickness.",
 note="Only the factor applied to the mean gauge figure changes, together with the two worked thicknesses stated in the same step."),
]
