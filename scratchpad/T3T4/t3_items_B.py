# -*- coding: utf-8 -*-
"""ARM B (30) — the ONLY change is a B-type applied step: the dynamics by which
a state evolves (a growth or decay step, a standing-change step, a recurrence).
The step is USED to derive content that appears in the artifact, and every
derived value moves with it inside one contiguous span."""

ITEMS = [

# ---------------------------------------------------------------- policy (6)
dict(id="t3-B-pol-01", arm="B", domain="policy",
 before="""Ravensworth Sports Club — Reserve Fund Policy

The club holds a reserve against the resurfacing of the outdoor courts, which the committee expects to fall due within the decade. The fund stands at 40,000 pounds at the start of the current year. The balance moves each year by drawing down a tenth of the opening balance for upkeep and adding nothing further, so the fund stands at 36,000 pounds after one year, 32,400 after two, and 29,160 after three. The treasurer reports the balance at each quarterly meeting and the committee reviews the drawdown at the annual general meeting. Money is moved from the reserve only on a resolution of the committee and only for work on the courts. Where a grant is received towards the resurfacing, it is held in a separate account and is not added to the reserve.""",
 old="drawing down a tenth of the opening balance for upkeep and adding nothing further, so the fund stands at 36,000 pounds after one year, 32,400 after two, and 29,160 after three",
 new="drawing down a fifth of the opening balance for upkeep and adding nothing further, so the fund stands at 32,000 pounds after one year, 25,600 after two, and 20,480 after three",
 site="The change is in the third sentence, in the passage that says how the balance moves from one year to the next.",
 note="Only the yearly drawdown step changes, together with the three projected balances worked from it in the same sentence."),

dict(id="t3-B-pol-02", arm="B", domain="policy",
 before="""Marlow Institute — Membership Standing Policy

A member in good standing whose subscription is unpaid on the renewal date moves to the holding class. A member in the holding class moves to the lapsed class after 90 days unless the subscription is paid, and a member in the lapsed class is removed from the register after a further 180 days, so a member whose renewal falls on 1 March reaches the lapsed class on 30 May and is removed on 26 November. Payment at any point before removal restores good standing from the date of payment. The membership secretary writes to members in the holding class once a month and to members in the lapsed class once a quarter. Members removed from the register may rejoin by fresh application and are not charged the arrears for the period during which they were off the register.""",
 old="moves to the lapsed class after 90 days unless the subscription is paid, and a member in the lapsed class is removed from the register after a further 180 days, so a member whose renewal falls on 1 March reaches the lapsed class on 30 May and is removed on 26 November",
 new="moves to the lapsed class after 60 days unless the subscription is paid, and a member in the lapsed class is removed from the register after a further 120 days, so a member whose renewal falls on 1 March reaches the lapsed class on 30 April and is removed on 28 August",
 site="The change is in the second sentence, in the passage that says how long a membership sits in each class before it moves on.",
 note="Only the two waiting periods that carry a membership from one class to the next change, together with the two worked dates in the same sentence."),

dict(id="t3-B-pol-03", arm="B", domain="policy",
 before="""Bramley Lane Allotments — Compost Bay Policy

The site keeps three bays in rotation and the working bay is turned into the next bay on a fixed cycle. A bay is turned every 14 days from the date it is first filled, and each bay is emptied to the seasoned heap after the fourth turn, so a bay filled on 1 April is turned on 15 April, 29 April, 13 May and 27 May. The rota for turning is drawn up by the site secretary in February and posted on the board by the store hut. Green waste from outside the site is not accepted into the bays, and holders are asked not to add turf or woody prunings thicker than a thumb. Holders who cannot take their turn arrange a swap with another holder and tell the secretary before the date falls due.""",
 old="turned every 14 days from the date it is first filled, and each bay is emptied to the seasoned heap after the fourth turn, so a bay filled on 1 April is turned on 15 April, 29 April, 13 May and 27 May",
 new="turned every 21 days from the date it is first filled, and each bay is emptied to the seasoned heap after the fourth turn, so a bay filled on 1 April is turned on 22 April, 13 May, 3 June and 24 June",
 site="The change is in the second sentence, in the passage that sets the turning cycle and lists the dates that follow from it.",
 note="Only the interval between one turn and the next changes, together with the four worked turning dates in the same sentence."),

dict(id="t3-B-pol-04", arm="B", domain="policy",
 before="""Harrowfield Water Authority — Standpipe Deposit Policy

A deposit of 1,000 pounds is taken at the counter when a standpipe is collected and is held against damage and non-return. The deposit is reduced for each full week the fitting is held beyond the agreed hire, by 10 per cent of the amount standing at the start of that week, so a deposit held one week over stands at 900 pounds, two weeks over at 810, and three weeks over at 729. The reduced amount is refunded within ten working days of return. A hirer may extend the agreed hire once by telephone before the end date, in which case no reduction is applied for the extended period. Deposits are not reduced where the depot has closed the counter for the whole of the week in question, and the district team confirms such closures in writing.""",
 old="by 10 per cent of the amount standing at the start of that week, so a deposit held one week over stands at 900 pounds, two weeks over at 810, and three weeks over at 729",
 new="by 20 per cent of the amount standing at the start of that week, so a deposit held one week over stands at 800 pounds, two weeks over at 640, and three weeks over at 512",
 site="The change is in the second sentence, in the passage that says how the held amount moves week by week.",
 note="Only the weekly reduction step changes, together with the three worked deposit amounts in the same sentence."),

dict(id="t3-B-pol-05", arm="B", domain="policy",
 before="""Weirbank Surgery — Complaint Handling Policy

A written complaint enters the log at stage one on the day it is opened. A complaint at stage one moves to stage two after 10 working days if no reply has gone out, and a complaint at stage two moves to the panel after a further 15 working days, so a complaint opened on Monday 1 June reaches stage two on 15 June and reaches the panel on 6 July. A reply at any point closes the complaint and stops the count. The practice manager reviews the log each Monday and lists complaints that are within two working days of a move. Complaints reaching the panel are heard at the next monthly meeting and the complainant is invited to attend. The log is kept for six years and is then destroyed under the retention schedule.""",
 old="moves to stage two after 10 working days if no reply has gone out, and a complaint at stage two moves to the panel after a further 15 working days, so a complaint opened on Monday 1 June reaches stage two on 15 June and reaches the panel on 6 July",
 new="moves to stage two after 5 working days if no reply has gone out, and a complaint at stage two moves to the panel after a further 25 working days, so a complaint opened on Monday 1 June reaches stage two on 8 June and reaches the panel on 13 July",
 site="The change is in the second sentence, in the passage that says how long a complaint sits at each stage before it moves on.",
 note="Only the two waiting periods that carry a complaint from stage to stage change, together with the two worked dates in the same sentence."),

dict(id="t3-B-pol-06", arm="B", domain="policy",
 before="""Fenwick Estate Community Shop — Chilled Stock Policy

Chilled lines are ordered on a fixed cycle so that the cabinet is filled without carrying more than two days of cover. An order is placed every 3 days and lands on the following morning, so an order placed on 2 March lands on 3 March, and the next orders are placed on 5, 8 and 11 March. The volunteer on the Tuesday shift checks the cabinet against the order sheet before the shop opens. Lines close to their date are marked down at midday and are moved to the front of the cabinet. Anything unsold at the close of the last day is taken to the community fridge in the hall. The cabinet temperature is read twice a day and noted on the sheet taped inside the door, and the sheet is changed at the start of each month.""",
 old="placed every 3 days and lands on the following morning, so an order placed on 2 March lands on 3 March, and the next orders are placed on 5, 8 and 11 March",
 new="placed every 5 days and lands on the following morning, so an order placed on 2 March lands on 3 March, and the next orders are placed on 7, 12 and 17 March",
 site="The change is in the second sentence, in the passage that sets the ordering cycle and lists the dates that follow from it.",
 note="Only the interval between one order and the next changes, together with the three worked ordering dates in the same sentence."),

# ---------------------------------------------------------------- config (6)
dict(id="t3-B-cfg-01", arm="B", domain="config",
 before="""# Ardwick depot file server — snapshot retention
volume = "depot-data"
snapshot_hour = 2
timezone = "Europe/London"

# snapshots thin out on the cadence below
keep_daily_days = 14
thin_factor = 2
# kept snapshot ages in days, worked from the cadence above
kept_age_1 = 14
kept_age_2 = 28
kept_age_3 = 56
kept_age_4 = 112
oldest_kept_days = 112

offsite_copy = true
verify_weekly = true
alert_channel = "depot-ops\"""",
 old="""thin_factor = 2
# kept snapshot ages in days, worked from the cadence above
kept_age_1 = 14
kept_age_2 = 28
kept_age_3 = 56
kept_age_4 = 112
oldest_kept_days = 112""",
 new="""thin_factor = 3
# kept snapshot ages in days, worked from the cadence above
kept_age_1 = 14
kept_age_2 = 42
kept_age_3 = 126
kept_age_4 = 378
oldest_kept_days = 378""",
 site="The change is in the seven-line block that begins with the thinning factor.",
 note="Only the factor by which one kept age follows the previous one changes, together with the four kept ages and the oldest kept age worked from it beneath."),

dict(id="t3-B-cfg-02", arm="B", domain="config",
 before="""# Marchgate telemetry uplink — send retry bench
endpoint = "https://uplink.marchgate.example/v2/ingest"
timeout_seconds = 20
max_attempts = 5

# the wait between attempts grows from the base by the multiplier below
base_wait_seconds = 2
wait_multiplier = 3
# waits before each attempt, worked from the base and multiplier above
wait_before_attempt_2 = 2
wait_before_attempt_3 = 6
wait_before_attempt_4 = 18
wait_before_attempt_5 = 54
total_wait_seconds = 80

jitter_fraction = 0.10
dead_letter_path = "/var/spool/marchgate/dead"
log_level = "info\"""",
 old="""wait_multiplier = 3
# waits before each attempt, worked from the base and multiplier above
wait_before_attempt_2 = 2
wait_before_attempt_3 = 6
wait_before_attempt_4 = 18
wait_before_attempt_5 = 54
total_wait_seconds = 80""",
 new="""wait_multiplier = 2
# waits before each attempt, worked from the base and multiplier above
wait_before_attempt_2 = 2
wait_before_attempt_3 = 4
wait_before_attempt_4 = 8
wait_before_attempt_5 = 16
total_wait_seconds = 30""",
 site="The change is in the seven-line block that begins with the wait multiplier.",
 note="Only the multiplier by which each wait follows the previous one changes, together with the four worked waits and their total beneath it."),

dict(id="t3-B-cfg-03", arm="B", domain="config",
 before="""# Bewick catchment portal — tile cache ageing
cache_root = "/srv/portal/tiles"
max_size_gb = 40
sweep_minutes = 30

# an entry lifetime shortens by the step below as a zoom level deepens
base_ttl_minutes = 960
ttl_step_divisor = 2
# lifetimes by zoom band, worked from the base and step above
ttl_zoom_10_minutes = 960
ttl_zoom_12_minutes = 480
ttl_zoom_14_minutes = 240
ttl_zoom_16_minutes = 120

stale_serve = true
purge_on_deploy = false
metrics_port = 9109""",
 old="""ttl_step_divisor = 2
# lifetimes by zoom band, worked from the base and step above
ttl_zoom_10_minutes = 960
ttl_zoom_12_minutes = 480
ttl_zoom_14_minutes = 240
ttl_zoom_16_minutes = 120""",
 new="""ttl_step_divisor = 4
# lifetimes by zoom band, worked from the base and step above
ttl_zoom_10_minutes = 960
ttl_zoom_12_minutes = 240
ttl_zoom_14_minutes = 60
ttl_zoom_16_minutes = 15""",
 site="The change is in the six-line block that begins with the lifetime step divisor.",
 note="Only the step by which a lifetime follows the previous band changes, together with the four worked lifetimes beneath it."),

dict(id="t3-B-cfg-04", arm="B", domain="config",
 before="""# Thornbury Academy — visits calendar reminder job
job_name = "visits-reminder"
timezone = "Europe/London"
run_hour = 7

# the job repeats on the day interval below, counted from the seed date
seed_date = "2026-03-02"
repeat_days = 7
# the next four run dates, worked from the seed and interval above
run_1 = "2026-03-09"
run_2 = "2026-03-16"
run_3 = "2026-03-23"
run_4 = "2026-03-30"

catch_up_missed = false
max_runtime_minutes = 10
notify = "office@thornbury.example\"""",
 old="""repeat_days = 7
# the next four run dates, worked from the seed and interval above
run_1 = "2026-03-09"
run_2 = "2026-03-16"
run_3 = "2026-03-23"
run_4 = "2026-03-30\"""",
 new="""repeat_days = 11
# the next four run dates, worked from the seed and interval above
run_1 = "2026-03-13"
run_2 = "2026-03-24"
run_3 = "2026-04-04"
run_4 = "2026-04-15\"""",
 site="The change is in the six-line block that begins with the repeat interval.",
 note="Only the interval on which the job repeats changes, together with the four run dates worked from it beneath."),

dict(id="t3-B-cfg-05", arm="B", domain="config",
 before="""# Calder district — inspection queue drain bench
queue = "inspection-intake"
workers = 6
shift_hours = 8

# the queue shortens by the amount below at each shift
drain_per_shift = 90
start_depth = 400
# projected depth at the end of each of the next four shifts
depth_after_shift_1 = 310
depth_after_shift_2 = 220
depth_after_shift_3 = 130
depth_after_shift_4 = 40

reassign_below = 40
page_above = 500
sample_minutes = 5
dashboard = "intake-board\"""",
 old="""drain_per_shift = 90
start_depth = 400
# projected depth at the end of each of the next four shifts
depth_after_shift_1 = 310
depth_after_shift_2 = 220
depth_after_shift_3 = 130
depth_after_shift_4 = 40""",
 new="""drain_per_shift = 55
start_depth = 400
# projected depth at the end of each of the next four shifts
depth_after_shift_1 = 345
depth_after_shift_2 = 290
depth_after_shift_3 = 235
depth_after_shift_4 = 180""",
 site="The change is in the seven-line block that begins with the per-shift drain amount.",
 note="Only the amount by which the queue shortens each shift changes, together with the four projected depths worked from it beneath."),

dict(id="t3-B-cfg-06", arm="B", domain="config",
 before="""# Ardwick forklift bay — charger stage bench
bay = "north"
pack_ah = 620
mains_amps = 32

# each stage runs for the previous stage length times the factor below
first_stage_minutes = 20
stage_factor = 2
# stage lengths in minutes, worked from the first stage and factor above
stage_bulk_minutes = 20
stage_absorb_minutes = 40
stage_equalise_minutes = 80
total_charge_minutes = 140

gas_extract_on = true
cover_interlock = true
log_path = "/var/log/ardwick/charger.log\"""",
 old="""stage_factor = 2
# stage lengths in minutes, worked from the first stage and factor above
stage_bulk_minutes = 20
stage_absorb_minutes = 40
stage_equalise_minutes = 80
total_charge_minutes = 140""",
 new="""stage_factor = 3
# stage lengths in minutes, worked from the first stage and factor above
stage_bulk_minutes = 20
stage_absorb_minutes = 60
stage_equalise_minutes = 180
total_charge_minutes = 260""",
 site="The change is in the six-line block that begins with the stage factor.",
 note="Only the factor by which each charging stage follows the previous one changes, together with the three stage lengths and the total worked from it beneath."),
]

ITEMS += [
# ------------------------------------------------------------------ code (6)
dict(id="t3-B-code-01", arm="B", domain="code",
 before='''"""Dye tracer readings at the Bewick outfall, stepped forward from the release."""

# the reading falls by the factor below at each ten-minute step
DECAY_PER_STEP = 0.50
START_READING = 640.0
# readings at the first four steps, worked from the factor and start above
READING_STEP_1 = 320.0
READING_STEP_2 = 160.0
READING_STEP_3 = 80.0
READING_STEP_4 = 40.0


def step_forward(reading):
    return reading * DECAY_PER_STEP


def series(n):
    r, out = START_READING, []
    for _ in range(n):
        r = step_forward(r)
        out.append(r)
    return out''',
 old='''DECAY_PER_STEP = 0.50
START_READING = 640.0
# readings at the first four steps, worked from the factor and start above
READING_STEP_1 = 320.0
READING_STEP_2 = 160.0
READING_STEP_3 = 80.0
READING_STEP_4 = 40.0''',
 new='''DECAY_PER_STEP = 0.25
START_READING = 640.0
# readings at the first four steps, worked from the factor and start above
READING_STEP_1 = 160.0
READING_STEP_2 = 40.0
READING_STEP_3 = 10.0
READING_STEP_4 = 2.5''',
 site="The change is in the seven-line block that begins with the per-step decay factor.",
 note="Only the factor by which a reading follows the previous one changes, together with the four worked readings beneath it."),

dict(id="t3-B-code-02", arm="B", domain="code",
 before='''"""Case standing for the Weirbank complaint log, stepped one day at a time."""

# the standing moves on when the day count passes the steps below
DAYS_TO_STAGE_TWO = 10
DAYS_TO_PANEL = 25
# standing after 8, 12 and 30 days, worked from the steps above
STANDING_AT_DAY_8 = "stage one"
STANDING_AT_DAY_12 = "stage two"
STANDING_AT_DAY_30 = "panel"


def standing_after(days):
    if days >= DAYS_TO_PANEL:
        return "panel"
    if days >= DAYS_TO_STAGE_TWO:
        return "stage two"
    return "stage one"


def walk(day_list):
    return [standing_after(d) for d in day_list]''',
 old='''DAYS_TO_STAGE_TWO = 10
DAYS_TO_PANEL = 25
# standing after 8, 12 and 30 days, worked from the steps above
STANDING_AT_DAY_8 = "stage one"
STANDING_AT_DAY_12 = "stage two"
STANDING_AT_DAY_30 = "panel"''',
 new='''DAYS_TO_STAGE_TWO = 4
DAYS_TO_PANEL = 11
# standing after 8, 12 and 30 days, worked from the steps above
STANDING_AT_DAY_8 = "stage two"
STANDING_AT_DAY_12 = "panel"
STANDING_AT_DAY_30 = "panel"''',
 site="The change is in the six-line block that begins with the first of the two day counts.",
 note="Only the day counts at which a case moves on change, together with the three worked standings beneath them."),

dict(id="t3-B-code-03", arm="B", domain="code",
 before='''"""Backwash timing for the Bellhaven plant panel."""

from datetime import datetime, timedelta

START = datetime(2026, 3, 2, 6, 0)
# each run follows the previous one by the gap below
GAP_HOURS = 84
RUNS = 4
# run times, worked from the start and gap above
RUN_1 = "2026-03-05 18:00"
RUN_2 = "2026-03-09 06:00"
RUN_3 = "2026-03-12 18:00"
RUN_4 = "2026-03-16 06:00"


def run_times():
    return [START + timedelta(hours=GAP_HOURS * (i + 1)) for i in range(RUNS)]''',
 old='''GAP_HOURS = 84
RUNS = 4
# run times, worked from the start and gap above
RUN_1 = "2026-03-05 18:00"
RUN_2 = "2026-03-09 06:00"
RUN_3 = "2026-03-12 18:00"
RUN_4 = "2026-03-16 06:00"''',
 new='''GAP_HOURS = 60
RUNS = 4
# run times, worked from the start and gap above
RUN_1 = "2026-03-04 18:00"
RUN_2 = "2026-03-07 06:00"
RUN_3 = "2026-03-09 18:00"
RUN_4 = "2026-03-12 06:00"''',
 site="The change is in the seven-line block that begins with the gap in hours.",
 note="Only the gap by which each run follows the previous one changes, together with the four run times worked from it beneath."),

dict(id="t3-B-code-04", arm="B", domain="code",
 before='''"""Colony counts at the Ryhope carr plots, stepped season by season."""

# the count grows by the factor below at each season
GROWTH_PER_SEASON = 1.5
START_COUNT = 64
# counts at the first four seasons, worked from the factor and start above
COUNT_SEASON_1 = 96
COUNT_SEASON_2 = 144
COUNT_SEASON_3 = 216
COUNT_SEASON_4 = 324


def next_season(count):
    return int(count * GROWTH_PER_SEASON)


def projection(seasons):
    c, out = START_COUNT, []
    for _ in range(seasons):
        c = next_season(c)
        out.append(c)
    return out''',
 old='''GROWTH_PER_SEASON = 1.5
START_COUNT = 64
# counts at the first four seasons, worked from the factor and start above
COUNT_SEASON_1 = 96
COUNT_SEASON_2 = 144
COUNT_SEASON_3 = 216
COUNT_SEASON_4 = 324''',
 new='''GROWTH_PER_SEASON = 1.25
START_COUNT = 64
# counts at the first four seasons, worked from the factor and start above
COUNT_SEASON_1 = 80
COUNT_SEASON_2 = 100
COUNT_SEASON_3 = 125
COUNT_SEASON_4 = 156''',
 site="The change is in the seven-line block that begins with the per-season growth factor.",
 note="Only the factor by which a season count follows the previous one changes, together with the four worked counts beneath it."),

dict(id="t3-B-code-05", arm="B", domain="code",
 before='''"""Uplink allowance for the Marchgate cabinets, refilled on a timer."""

# the allowance refills by the amount below each minute, up to the ceiling
REFILL_PER_MINUTE = 12
CEILING = 60
# allowance after 1, 3 and 5 minutes from empty, worked from the values above
ALLOWANCE_AT_1_MIN = 12
ALLOWANCE_AT_3_MIN = 36
ALLOWANCE_AT_5_MIN = 60


def allowance_after(minutes):
    return min(CEILING, REFILL_PER_MINUTE * minutes)


def timeline(minute_list):
    return [allowance_after(m) for m in minute_list]''',
 old='''REFILL_PER_MINUTE = 12
CEILING = 60
# allowance after 1, 3 and 5 minutes from empty, worked from the values above
ALLOWANCE_AT_1_MIN = 12
ALLOWANCE_AT_3_MIN = 36
ALLOWANCE_AT_5_MIN = 60''',
 new='''REFILL_PER_MINUTE = 25
CEILING = 60
# allowance after 1, 3 and 5 minutes from empty, worked from the values above
ALLOWANCE_AT_1_MIN = 25
ALLOWANCE_AT_3_MIN = 60
ALLOWANCE_AT_5_MIN = 60''',
 site="The change is in the six-line block that begins with the per-minute refill amount.",
 note="Only the amount by which the allowance refills each minute changes, together with the three worked allowances beneath it."),

dict(id="t3-B-code-06", arm="B", domain="code",
 before='''"""Bench anneal for the Harnbeck kiln controller."""

# the setpoint falls by the fraction below of the previous setpoint at each hold
COOL_FRACTION = 0.20
START_C = 1000
# setpoints at the first four holds, worked from the fraction and start above
HOLD_1_C = 800
HOLD_2_C = 640
HOLD_3_C = 512
HOLD_4_C = 409


def next_setpoint(c):
    return int(c * (1 - COOL_FRACTION))


def schedule(holds):
    c, out = START_C, []
    for _ in range(holds):
        c = next_setpoint(c)
        out.append(c)
    return out''',
 old='''COOL_FRACTION = 0.20
START_C = 1000
# setpoints at the first four holds, worked from the fraction and start above
HOLD_1_C = 800
HOLD_2_C = 640
HOLD_3_C = 512
HOLD_4_C = 409''',
 new='''COOL_FRACTION = 0.50
START_C = 1000
# setpoints at the first four holds, worked from the fraction and start above
HOLD_1_C = 500
HOLD_2_C = 250
HOLD_3_C = 125
HOLD_4_C = 62''',
 site="The change is in the seven-line block that begins with the cooling fraction.",
 note="Only the fraction by which a setpoint falls from the previous hold changes, together with the four worked setpoints beneath it."),

# ---------------------------------------------------------------- report (6)
dict(id="t3-B-rep-01", arm="B", domain="report",
 before="""Water Resources Note — Harrowfield Reservoir, Late Summer

The reservoir stood at 78 per cent of full capacity on 1 August, with inflow well below the seasonal mean and no rain of consequence forecast for the month. Storage falls by 4 percentage points a week under the present draw, so the projection carried in this note gives 74 per cent on 8 August, 70 per cent on 15 August and 66 per cent on 22 August. The drought plan's first trigger sits at 65 per cent, which on this projection is reached in the last days of the month. Compensation releases to the beck continue at the licensed rate. The catchment team reads the gauge daily and the figure is posted to the public page each morning. A further note will follow if the projection is overtaken by events.""",
 old="falls by 4 percentage points a week under the present draw, so the projection carried in this note gives 74 per cent on 8 August, 70 per cent on 15 August and 66 per cent on 22 August. The drought plan's first trigger sits at 65 per cent, which on this projection is reached in the last days of the month.",
 new="falls by 7 percentage points a week under the present draw, so the projection carried in this note gives 71 per cent on 8 August, 64 per cent on 15 August and 57 per cent on 22 August. The drought plan's first trigger sits at 65 per cent, which on this projection is reached in the second week of the month.",
 site="The change is in the second sentence and the sentence immediately after it, where the weekly movement in storage is given.",
 note="Only the weekly step by which storage falls changes, together with the three projected percentages and the trigger date worked from it in the following sentence."),

dict(id="t3-B-rep-02", arm="B", domain="report",
 before="""Survey Note — Corrie Millpond Silt Accumulation

Depth was probed on a fixed grid of twenty points in March and compared with the same grid probed three years ago. Silt is gaining on the pond floor at 30 millimetres a year across the grid mean, so the mean silt depth of 240 millimetres measured this March projects to 270 millimetres next March, 300 the year after and 330 the year after that. The desilting threshold agreed with the trust is 350 millimetres, which on this projection falls in the fourth year from now. Probing was done from the punt at low draw-down with a graduated rod, two readings at each point. The inlet corner is gaining faster than the grid mean and is shown separately on the plan attached to this note.""",
 old="at 30 millimetres a year across the grid mean, so the mean silt depth of 240 millimetres measured this March projects to 270 millimetres next March, 300 the year after and 330 the year after that. The desilting threshold agreed with the trust is 350 millimetres, which on this projection falls in the fourth year from now.",
 new="at 55 millimetres a year across the grid mean, so the mean silt depth of 240 millimetres measured this March projects to 295 millimetres next March, 350 the year after and 405 the year after that. The desilting threshold agreed with the trust is 350 millimetres, which on this projection falls in the second year from now.",
 site="The change is in the second sentence and the sentence immediately after it, where the yearly gain in silt depth is given.",
 note="Only the yearly step by which silt depth gains changes, together with the three projected depths and the threshold year worked from it in the following sentence."),

dict(id="t3-B-rep-03", arm="B", domain="report",
 before="""Livestock Note — Ardley Farm Suckler Herd

The herd stood at 120 cows at the October count, with 44 heifers held back and 38 cows drafted out over the year. The herd changes by a net gain of 5 per cent a year on the present replacement pattern, so the projection is 126 cows next October, 132 the year after and 139 the year after that. Housing at the north yard takes 140 head at the stocking density the assurance scheme requires, which on this projection is reached in the fourth year. Calving is tight, with 80 of the cows calving inside the first three weeks. Bull hire is booked for the same six-week window next season and the same two bulls have been asked for.""",
 old="by a net gain of 5 per cent a year on the present replacement pattern, so the projection is 126 cows next October, 132 the year after and 139 the year after that. Housing at the north yard takes 140 head at the stocking density the assurance scheme requires, which on this projection is reached in the fourth year.",
 new="by a net gain of 12 per cent a year on the present replacement pattern, so the projection is 134 cows next October, 150 the year after and 168 the year after that. Housing at the north yard takes 140 head at the stocking density the assurance scheme requires, which on this projection is reached in the second year.",
 site="The change is in the second sentence and the sentence immediately after it, where the yearly change in herd size is given.",
 note="Only the yearly step by which the herd changes size changes, together with the three projected herd sizes and the housing year worked from it in the following sentence."),

dict(id="t3-B-rep-04", arm="B", domain="report",
 before="""Waiting List Note — Nettlebridge Community Audiology

The list stood at 640 patients at the end of March, and the case mix has been steady across the quarter. Referrals arrive at about 90 a month and the clinic completes about 130 a month at current staffing, so the list shortens by 40 a month and stands at a projected 600 at the end of April, 560 at the end of May and 520 at the end of June. The target of 400 is reached in the sixth month on this projection. Two of the six rooms are shared with paediatrics on Tuesday afternoons, which is the binding constraint on the afternoon clinics. Non-attendance running at 9 per cent has been unchanged for three quarters. A further note follows at the half year.""",
 old="the clinic completes about 130 a month at current staffing, so the list shortens by 40 a month and stands at a projected 600 at the end of April, 560 at the end of May and 520 at the end of June. The target of 400 is reached in the sixth month on this projection.",
 new="the clinic completes about 170 a month at current staffing, so the list shortens by 80 a month and stands at a projected 560 at the end of April, 480 at the end of May and 400 at the end of June. The target of 400 is reached in the third month on this projection.",
 site="The change is in the second sentence and the sentence immediately after it, where the monthly movement in the list is given.",
 note="Only the monthly completion figure and the monthly step it sets change, together with the three projected list sizes and the target month worked from it in the following sentence."),

dict(id="t3-B-rep-05", arm="B", domain="report",
 before="""Operations Note — Marchgate Slow Sand Beds, Bed 2

The bed was returned to service on 4 May after scraping and the head loss was 120 millimetres at the first reading. Head loss builds at 45 millimetres a week at the present filtration rate, so the projection gives 165 millimetres on 11 May, 210 on 18 May and 255 on 25 May. The bed is taken out for scraping at 400 millimetres, which on this projection falls in the seventh week after return. Filtered water turbidity has held below the works target throughout. The sand depth after the last scrape is 640 millimetres, and two more scrapes can be taken before resanding is due.""",
 old="builds at 45 millimetres a week at the present filtration rate, so the projection gives 165 millimetres on 11 May, 210 on 18 May and 255 on 25 May. The bed is taken out for scraping at 400 millimetres, which on this projection falls in the seventh week after return.",
 new="builds at 90 millimetres a week at the present filtration rate, so the projection gives 210 millimetres on 11 May, 300 on 18 May and 390 on 25 May. The bed is taken out for scraping at 400 millimetres, which on this projection falls in the fourth week after return.",
 site="The change is in the second sentence and the sentence immediately after it, where the weekly build in head loss is given.",
 note="Only the weekly step by which head loss builds changes, together with the three projected head losses and the scraping week worked from it in the following sentence."),

dict(id="t3-B-rep-06", arm="B", domain="report",
 before="""Fleet Note — Ardwick Depot Light Vans

The eight light vans were bought together in 2022 and have run on the same round pattern since. Distance accrues at 1,500 miles a month across the fleet mean, so a van standing at 74,000 miles this month reaches 78,500 in three months, 83,000 in six and 87,500 in nine. The replacement point set by the workshop is 90,000 miles, which on this accrual falls in the eleventh month. Two vans are due for cambelt work before then and the workshop has quoted for both. Tyres are on a separate schedule tied to tread depth rather than distance. The depot manager reviews the fleet plan each quarter and reports to the operations board twice a year.""",
 old="at 1,500 miles a month across the fleet mean, so a van standing at 74,000 miles this month reaches 78,500 in three months, 83,000 in six and 87,500 in nine. The replacement point set by the workshop is 90,000 miles, which on this accrual falls in the eleventh month.",
 new="at 2,500 miles a month across the fleet mean, so a van standing at 74,000 miles this month reaches 81,500 in three months, 89,000 in six and 96,500 in nine. The replacement point set by the workshop is 90,000 miles, which on this accrual falls in the seventh month.",
 site="The change is in the second sentence and the sentence immediately after it, where the monthly accrual of distance is given.",
 note="Only the monthly step by which distance accrues changes, together with the three projected distances and the replacement month worked from it in the following sentence."),
]

ITEMS += [
# --------------------------------------------------------------- process (6)
dict(id="t3-B-proc-01", arm="B", domain="process",
 before="""Kiln Cooling — Harnbeck Pottery, Biscuit Firing

1. Confirm that the peak has been held for the full thirty minutes before starting the cooling run.
2. Close the damper to a quarter and switch the controller to the cooling programme.
3. Step the setpoint down by 100 degrees every hour, so from a peak of 1,000 the setpoint reads 900 after one hour, 800 after two and 700 after three.
4. Watch the first hour for any sign that the elements are still driving the chamber.
5. Leave the spy holes plugged until the chamber falls below four hundred degrees.
6. Open the damper fully once the chamber is below two hundred and fifty degrees.
7. Leave the door shut overnight and open it no earlier than the following morning.
8. Unload with dry hands and stack the ware on the cooling bench, not the floor.
9. Note the peak, the hold and the unloading time in the firing book.""",
 old="down by 100 degrees every hour, so from a peak of 1,000 the setpoint reads 900 after one hour, 800 after two and 700 after three",
 new="down by 250 degrees every hour, so from a peak of 1,000 the setpoint reads 750 after one hour, 500 after two and 250 after three",
 site="The change is in step three, in the passage that sets how far the setpoint moves each hour.",
 note="Only the hourly step by which the setpoint falls changes, together with the three worked setpoints stated in the same step."),

dict(id="t3-B-proc-02", arm="B", domain="process",
 before="""Starter Maintenance — Bramley Lane Bakehouse

1. Take the starter from the retarder an hour before the first feed of the day.
2. Discard all but one hundred grammes of the starter into the waste pail.
3. Feed on a 12-hour cycle, so a starter fed at 06:00 is fed again at 18:00 and then at 06:00 the following morning, giving two feeds a day.
4. Add flour and water at equal weight to the retained starter and mix until no dry flour remains.
5. Mark the jar with a band at the level of the fresh mix.
6. Leave at bench temperature until the level has doubled and then return the jar to the retarder.
7. Note the rise time against the bench temperature in the bakehouse book.
8. Replace the jar and lid every fortnight and scald both before reuse.""",
 old="on a 12-hour cycle, so a starter fed at 06:00 is fed again at 18:00 and then at 06:00 the following morning, giving two feeds a day",
 new="on an 8-hour cycle, so a starter fed at 06:00 is fed again at 14:00 and then at 22:00 the same evening, giving three feeds a day",
 site="The change is in step three, in the passage that sets the feeding cycle and the times that follow from it.",
 note="Only the interval between one feed and the next changes, together with the worked feeding times and the daily count stated in the same step."),

dict(id="t3-B-proc-03", arm="B", domain="process",
 before="""Coating Cure — Corrie Viaduct Repaint, Panel Sequence

1. Check that the panel is dry and that the surface temperature is at least three degrees above dew point.
2. Apply the primer at the coverage marked on the tin and note the batch number.
3. Allow each coat to cure before the next is applied, on a 24-hour spacing, so a primer laid on 4 June takes its second coat on 5 June and its top coat on 6 June.
4. Sand lightly between coats with the grade named in the coating schedule.
5. Keep the sheeting closed while each coat cures and vent only at the ends.
6. Take the film thickness readings once the top coat has cured for a full day.
7. Move the sheeting to the next panel and begin again at the first step.
8. Note the batch numbers and the cure dates against the panel number on the inspection sheet.""",
 old="on a 24-hour spacing, so a primer laid on 4 June takes its second coat on 5 June and its top coat on 6 June",
 new="on a 72-hour spacing, so a primer laid on 4 June takes its second coat on 7 June and its top coat on 10 June",
 site="The change is in step three, in the passage that sets the spacing between coats and the dates that follow from it.",
 note="Only the spacing between one coat and the next changes, together with the two worked coating dates stated in the same step."),

dict(id="t3-B-proc-04", arm="B", domain="process",
 before="""Duty Roster Rotation — Bellhaven Leisure Centre

1. Draw the list of duty technicians in the order held by the centre manager.
2. Fix the first duty week to the week beginning 2 March.
3. Move the duty on by one name every 2 weeks, so the first name holds the weeks beginning 2 and 9 March, the second holds 16 and 23 March, and the third holds 30 March and 6 April.
4. Post the rota on the staff board four weeks ahead of the first date shown.
5. Arrange swaps directly between technicians and tell the manager before the Friday.
6. Carry the duty phone from the Monday handover until the following handover.
7. Note any call-out on the duty sheet with the time and the plant item.
8. Return the phone and the sheet to the office at the end of the duty.""",
 old="every 2 weeks, so the first name holds the weeks beginning 2 and 9 March, the second holds 16 and 23 March, and the third holds 30 March and 6 April",
 new="every 3 weeks, so the first name holds the weeks beginning 2, 9 and 16 March, the second holds 23 and 30 March and 6 April, and the third holds 13, 20 and 27 April",
 site="The change is in step three, in the passage that sets how often the duty moves on and lists the weeks that follow from it.",
 note="Only the interval at which the duty moves to the next name changes, together with the worked week beginnings stated in the same step."),

dict(id="t3-B-proc-05", arm="B", domain="process",
 before="""Fermentation Control — Weirbank Brewery, Bitter

1. Pitch at eighteen degrees and note the pitching gravity on the vessel card.
2. Hold at pitching temperature until the gravity has fallen by half.
3. Step the vessel temperature down by 2 degrees each day from that point, so a vessel at 18 reads 16 on the following day, 14 on the next and 12 on the third.
4. Take a gravity reading each morning before the temperature is stepped.
5. Hold at the final temperature for two full days before starting the chill.
6. Chill to four degrees over eight hours and leave to settle for a further day.
7. Rack to the conditioning tank, leaving the yeast bed undisturbed.
8. Note the pitching gravity, the final gravity, and the rack date on the vessel card.
9. Clean the vessel within the shift in which it is emptied.""",
 old="down by 2 degrees each day from that point, so a vessel at 18 reads 16 on the following day, 14 on the next and 12 on the third",
 new="down by 3 degrees each day from that point, so a vessel at 18 reads 15 on the following day, 12 on the next and 9 on the third",
 site="The change is in step three, in the passage that sets how far the vessel temperature moves each day.",
 note="Only the daily step by which the vessel temperature falls changes, together with the three worked temperatures stated in the same step."),

dict(id="t3-B-proc-06", arm="B", domain="process",
 before="""Backwash Scheduling — Bellhaven Pool Plant

1. Note the clean filter pressure after the first backwash of the season.
2. Run the plant and watch for the pressure to rise above the clean figure.
3. Set the interval between backwashes from the bather load, halving the interval each time the daily load doubles, so a load of 200 gives an interval of 16 days, a load of 400 gives 8 days and a load of 800 gives 4 days.
4. Enter the interval in the plant book and set the reminder on the panel.
5. Backwash before opening rather than during public session hours.
6. Run the reverse flow until the sight glass clears, normally four minutes.
7. Top up the pool to the tile line after each backwash.
8. Note the pressure before and after on the plant sheet.
9. Review the interval at the end of each month against the load actually seen.""",
 old="halving the interval each time the daily load doubles, so a load of 200 gives an interval of 16 days, a load of 400 gives 8 days and a load of 800 gives 4 days",
 new="quartering the interval each time the daily load doubles, so a load of 200 gives an interval of 16 days, a load of 400 gives 4 days and a load of 800 gives 1 day",
 site="The change is in step three, in the passage that sets how the interval moves as the load doubles.",
 note="Only the step by which the interval shortens as the load doubles changes, together with the three worked intervals stated in the same step."),
]
