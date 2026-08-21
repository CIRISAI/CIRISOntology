"""T4 — THE MANNER BOUNDARY TEST: item authoring.

Per RECOGNITION_PREREG.md §T4 (frozen) and RECOGNITION_PREREG_A2.md MAJOR-8/MAJOR-9.
72 items: arm M 24, arm C 24, arm P 24.

  M  the only change is how the passage is expressed (formality, voice, address,
     layout-of-expression). Content is held identical and is carried elsewhere in
     the document, named per item in `note`.
  C  matched control: a content change (a value, a date, a threshold, a permission)
     whose grounding is entirely inside the passage.
  P  manipulation check: a Premises- or Model-site change whose grounding lies
     OUTSIDE the passage; deciding what kind of change it is needs text the cut
     removes.

Each item declares `cut` as an exact substring of `before` (the CUT-A passage);
offsets are computed, never hand-written. Arm M additionally declares `cutb`
(the fragment one party holds), with `old_a`/`new_a` the portion of the change
that falls on that party's side, so the change straddles the division by
construction.

Emission only. All verification lives in check_t4.py, which reads the JSONL back.
"""
from __future__ import annotations
import json

ITEMS: list[dict] = []

# =============================================================== ARM M — policy
ITEMS += [
dict(id="t4-M01", arm="M", domain="policy", cutb_side="tail",
 before="""Ashcombe Trust — Volunteer Driver Scheme

Part 1. Every instruction in Part 3 is mandatory for volunteers who carry passengers, and the Trust treats a departure from any one of them as a matter for the scheme coordinator.

Part 2. Volunteers join the scheme after an interview with the coordinator and a check of their licence, which is repeated each year in the month the volunteer joined.

Part 3. Volunteers are asked to look over the tyres and lights before the first journey of the day, and to note what they find on the sheet kept in the glovebox. Where a defect appears, volunteers are asked to withdraw the vehicle and telephone the coordinator, who arranges a replacement from the pool.

Part 4. Fuel is drawn from the Trust account at the Bridge Street garage, and receipts are handed to the office within a week of the journey. The coordinator reviews the fuel account at the end of each quarter.""",
 old="""Volunteers are asked to look over the tyres and lights before the first journey of the day, and to note what they find on the sheet kept in the glovebox. Where a defect appears, volunteers are asked to withdraw the vehicle and telephone the coordinator, who arranges a replacement from the pool.""",
 new="""Look over the tyres and lights before the first journey of the day, and note what you find on the sheet kept in the glovebox. Where a defect appears, withdraw the vehicle and telephone the coordinator, who arranges a replacement from the pool.""",
 old_a="""Volunteers are asked to look over the tyres and lights before the first journey of the day, and to note what they find on the sheet kept in the glovebox. """,
 new_a="""Look over the tyres and lights before the first journey of the day, and note what you find on the sheet kept in the glovebox. """,
 cut="""Part 3. Volunteers are asked to look over the tyres and lights before the first journey of the day, and to note what they find on the sheet kept in the glovebox. Where a defect appears, volunteers are asked to withdraw the vehicle and telephone the coordinator, who arranges a replacement from the pool.""",
 site="Part 3, both sentences",
 note="Softened request form becomes direct address; the standing of the two instructions is stated in Part 1 (mandatory), so nothing the document says about the volunteer changes. CUT-B shows the coordinator half, which does not carry Part 1.",
 framing="The scheme issues this document in two halves and each party works only from its own; the half shown here is the one the coordinator keeps, beginning where the volunteer half ends."),

dict(id="t4-M02", arm="M", domain="policy", cutb_side="head",
 before="""Kelvin Docks Harbour Authority — Winter Berth Notice

Part 1. Berths on the inner basin are let by the season, and the season runs from the first Monday in November to the last Friday in March.

Part 2. A vessel left afloat over the season has a set of keys lodged with the harbour office, so that lines can be adjusted in heavy weather.

Part 3. You are responsible for the condition of your own lines and fenders, and you tell the office before any work is carried out on the pontoon. If your vessel is lifted out for the season, you clear the berth of gear within two days of the lift.

Part 4. The office holds a list of contractors who work in the basin, and any contractor is signed in at the gate before starting. This notice is addressed to berth holders on the inner basin and to nobody else; the outer basin is covered by a separate notice issued each October.""",
 old="""You are responsible for the condition of your own lines and fenders, and you tell the office before any work is carried out on the pontoon. If your vessel is lifted out for the season, you clear the berth of gear within two days of the lift.""",
 new="""Berth holders are responsible for the condition of their own lines and fenders, and the office is told before any work is carried out on the pontoon. If a vessel is lifted out for the season, the berth is cleared of gear within two days of the lift.""",
 old_a="""You are responsible for the condition of your own lines and fenders, and you tell the office before any work is carried out on the pontoon. """,
 new_a="""Berth holders are responsible for the condition of their own lines and fenders, and the office is told before any work is carried out on the pontoon. """,
 cut="""Part 3. You are responsible for the condition of your own lines and fenders, and you tell the office before any work is carried out on the pontoon. If your vessel is lifted out for the season, you clear the berth of gear within two days of the lift.""",
 site="Part 3, both sentences",
 note="Direct address becomes the impersonal form used by the rest of the document; who the notice speaks to is stated in Part 4, so the addressee does not change. CUT-B shows the opening half, which does not carry Part 4.",
 framing="The notice is split between the harbour office and the basin warden, each of whom holds one half; the half shown here is the office half, which stops where the warden half begins."),

dict(id="t4-M03", arm="M", domain="policy", cutb_side="tail",
 before="""Fernhill Academy — Trip Equipment Notice

Part 1. The contents of the day pack are settled by the governing body each September and are not varied by the staff leading a trip.

Part 2. Packs are issued from the sports store on the morning of the trip and returned to the same counter before the buses are released.

Part 3. Each pack holds a waterproof top, a spare pair of socks, a filled water bottle, a whistle on a lanyard and a printed card giving the school telephone number. Pupils who bring a waterproof top of their own still carry the one from the pack.

Part 4. Staff leading a trip carry a second pack holding a first aid kit and a charged handset. The store keeps a signing sheet for both kinds of pack and reconciles it the following morning.""",
 old="""Each pack holds a waterproof top, a spare pair of socks, a filled water bottle, a whistle on a lanyard and a printed card giving the school telephone number. Pupils who bring a waterproof top of their own still carry the one from the pack.""",
 new="""Each pack holds:

- a waterproof top
- a spare pair of socks
- a filled water bottle
- a whistle on a lanyard
- a printed card giving the school telephone number

Pupils who bring a waterproof top of their own still carry the one from the pack.""",
 old_a="""Each pack holds a waterproof top, a spare pair of socks, """,
 new_a="""Each pack holds:

- a waterproof top
- a spare pair of socks
""",
 cut="""Part 3. Each pack holds a waterproof top, a spare pair of socks, a filled water bottle, a whistle on a lanyard and a printed card giving the school telephone number. Pupils who bring a waterproof top of their own still carry the one from the pack.""",
 site="Part 3, both sentences",
 note="The same five items laid out down the page instead of across a sentence; every item word is carried over unchanged, and who settles the contents is stated in Part 1. CUT-B shows the second half, which does not carry Part 1.",
 framing="The notice is prepared jointly by the trips office and the sports store, which each keep one half; the half shown here is the store half, beginning where the trips office half ends."),

dict(id="t4-M04", arm="M", domain="policy", cutb_side="head",
 before="""Marlow District Council — Grit Bin Notice

Part 1. Bins stand at the sites shown on the map that accompanies this notice, and the map is redrawn every third year.

Part 2. Grit is taken from the bins by residents for use on the public highway and on footways, and not on private driveways.

Part 3. The bins are refilled between the middle of October and the end of November. They are looked at again after any period of snow lasting more than two days, and any bin found empty is refilled within four working days of the check.

Part 4. Bins are emptied, cleaned and stored over the summer. All of the work in Part 3 and in this Part is carried out by the highways team at the Fenn Lane depot, which also holds the map.""",
 old="""The bins are refilled between the middle of October and the end of November. They are looked at again after any period of snow lasting more than two days, and any bin found empty is refilled within four working days of the check.""",
 new="""The highways team refills the bins between the middle of October and the end of November. The team looks at them again after any period of snow lasting more than two days, and refills any bin found empty within four working days of the check.""",
 old_a="""The bins are refilled between the middle of October and the end of November. """,
 new_a="""The highways team refills the bins between the middle of October and the end of November. """,
 cut="""Part 3. The bins are refilled between the middle of October and the end of November. They are looked at again after any period of snow lasting more than two days, and any bin found empty is refilled within four working days of the check.""",
 site="Part 3, both sentences",
 note="Agentless voice becomes active voice naming the team; who does the work is stated in Part 4, so the document names the same doer either way. CUT-B shows the opening half, which does not carry Part 4.",
 framing="The notice is held in two halves, one by the depot and one by the district office, and each works only from its own; the half shown here is the depot half, which stops where the district office half begins."),

dict(id="t4-M05", arm="M", domain="policy", cutb_side="head",
 before="""Redhill Allotment Association — Plot Conditions

Part 1. Plots are let by the year from the first of January, and the letting is renewed by paying the fee before the last day of February.

Part 2. Tenants are invited to keep the paths on two sides of the plot cut to the width marked by the pegs, and to keep bonfires to the hours between four and seven in the evening. Where a plot is left untended for eight weeks in the growing season, tenants are invited to give the site secretary a date by which the plot returns to use.

Part 3. Water is drawn from the standpipes at the top and the bottom of the site, and hoses are not left running unattended.

Part 4. Every line of Part 2 is a condition of the tenancy, and the committee ends a tenancy on the site secretary report alone. The committee meets on the second Tuesday of each month.""",
 old="""Tenants are invited to keep the paths on two sides of the plot cut to the width marked by the pegs, and to keep bonfires to the hours between four and seven in the evening. Where a plot is left untended for eight weeks in the growing season, tenants are invited to give the site secretary a date by which the plot returns to use.""",
 new="""Tenants keep the paths on two sides of the plot cut to the width marked by the pegs, and keep bonfires to the hours between four and seven in the evening. Where a plot is left untended for eight weeks in the growing season, tenants give the site secretary a date by which the plot returns to use.""",
 old_a="""Tenants are invited to keep the paths on two sides of the plot cut to the width marked by the pegs, and to keep bonfires to the hours between four and seven in the evening. """,
 new_a="""Tenants keep the paths on two sides of the plot cut to the width marked by the pegs, and keep bonfires to the hours between four and seven in the evening. """,
 cut="""Part 2. Tenants are invited to keep the paths on two sides of the plot cut to the width marked by the pegs, and to keep bonfires to the hours between four and seven in the evening. Where a plot is left untended for eight weeks in the growing season, tenants are invited to give the site secretary a date by which the plot returns to use.""",
 site="Part 2, both sentences",
 note="An inviting form becomes the plain indicative used elsewhere; the standing of Part 2 is stated in Part 4 (a condition of the tenancy), so what binds the tenant does not change. CUT-B shows the opening half, which does not carry Part 4.",
 framing="The conditions are issued in two halves, one kept by the tenant and one by the site secretary; the half shown here is the tenant half, which stops where the secretary half begins."),
]

# =============================================================== ARM M — report
ITEMS += [
dict(id="t4-M06", arm="M", domain="report", cutb_side="tail",
 before="""Thornleigh Buildings — Roof Survey Summary

Section 1. Every finding below rests on a single visit made on 4 March and none of them has been checked against a second visit; the surveyor treats all of them as open until the follow-up in June.

Section 2. The covering on the north slope is a bitumen sheet laid in three widths, with the laps running down the fall.

Section 3. It appears that water has been entering at the ridge for some time, and the staining in the roof space seems to go back several winters. The daylight visible at the ridge line looks like the route, although the surveyor was not able to reach the ridge from inside.

Section 4. The gutters on both slopes were clear on the day of the visit. The downpipe at the east gable discharges to a gully that was running freely.""",
 old="""It appears that water has been entering at the ridge for some time, and the staining in the roof space seems to go back several winters. The daylight visible at the ridge line looks like the route, although the surveyor was not able to reach the ridge from inside.""",
 new="""Water has been entering at the ridge for some time, and the staining in the roof space goes back several winters. The daylight visible at the ridge line is the route, although the surveyor was not able to reach the ridge from inside.""",
 old_a="""It appears that water has been entering at the ridge for some time, and the staining in the roof space seems to go back several winters. """,
 new_a="""Water has been entering at the ridge for some time, and the staining in the roof space goes back several winters. """,
 cut="""Section 3. It appears that water has been entering at the ridge for some time, and the staining in the roof space seems to go back several winters. The daylight visible at the ridge line looks like the route, although the surveyor was not able to reach the ridge from inside.""",
 site="Section 3, both sentences",
 note="Qualified assertion becomes flat assertion; how far the findings are settled is stated in Section 1 (one visit, all open until June), so the standing of the survey does not change. CUT-B shows the second half, which does not carry Section 1.",
 framing="The summary is split between the surveyor and the managing agent, who each hold one half; the half shown here is the agent half, beginning where the surveyor half ends."),

dict(id="t4-M07", arm="M", domain="report", cutb_side="head",
 before="""Larkhill Community Transport — Quarterly Review

Section 1. The minibus covered 4,180 miles in the quarter, against 3,900 miles in the same quarter last year.

Section 2. Fuel was bought on eleven occasions, nine of them at the depot pump and two on the road.

Section 3. We looked at every journey sheet for the quarter and we found four sheets with no return time entered. We spoke to the three drivers concerned and we have asked the office to reissue the sheets in a larger size.

Section 4. The tyres were changed in the second month of the quarter. This review was written by the two committee members named below, and every line of it is theirs.""",
 old="""We looked at every journey sheet for the quarter and we found four sheets with no return time entered. We spoke to the three drivers concerned and we have asked the office to reissue the sheets in a larger size.""",
 new="""Every journey sheet for the quarter was looked at and four sheets were found with no return time entered. The three drivers concerned were spoken to, and the office has been asked to reissue the sheets in a larger size.""",
 old_a="""We looked at every journey sheet for the quarter and we found four sheets with no return time entered. """,
 new_a="""Every journey sheet for the quarter was looked at and four sheets were found with no return time entered. """,
 cut="""Section 3. We looked at every journey sheet for the quarter and we found four sheets with no return time entered. We spoke to the three drivers concerned and we have asked the office to reissue the sheets in a larger size.""",
 site="Section 3, both sentences",
 note="First person becomes the impersonal voice used elsewhere; who did the work and who speaks is stated in Section 4, so the authorship of the review does not change. CUT-B shows the opening half, which does not carry Section 4.",
 framing="The review is held in two halves, one by the committee and one by the transport office; the half shown here is the committee half, which stops where the office half begins."),

dict(id="t4-M08", arm="M", domain="report", cutb_side="tail",
 before="""Dunmore Mill — Boiler Readings Note

Section 1. The four readings below are taken straight from the meter and are given in the order the meter gives them; nothing has been added to them and nothing left out.

Section 2. The boiler ran on the low setting for the whole of the week under review, with one shutdown on the Wednesday for the annual valve check.

Section 3. Monday came in at 61 degrees, Tuesday at 63 degrees, Thursday at 60 degrees and Friday at 62 degrees. The Wednesday shutdown means there is no reading for that day.

Section 4. The gauge was compared against the hand thermometer at the start of the week and the two agreed to within a degree. No adjustment was made to the gauge during the week.""",
 old="""Monday came in at 61 degrees, Tuesday at 63 degrees, Thursday at 60 degrees and Friday at 62 degrees. The Wednesday shutdown means there is no reading for that day.""",
 new="""Monday    61 degrees
Tuesday   63 degrees
Thursday  60 degrees
Friday    62 degrees

The Wednesday shutdown means there is no reading for that day.""",
 old_a="""Monday came in at 61 degrees, Tuesday at 63 degrees, """,
 new_a="""Monday    61 degrees
Tuesday   63 degrees
""",
 cut="""Section 3. Monday came in at 61 degrees, Tuesday at 63 degrees, Thursday at 60 degrees and Friday at 62 degrees. The Wednesday shutdown means there is no reading for that day.""",
 site="Section 3, both sentences",
 note="The same four readings set down the page instead of across a sentence; every figure is carried over unchanged, and where the readings come from is stated in Section 1. CUT-B shows the second half, which does not carry Section 1.",
 framing="The note is divided between the shift engineer and the energy office, each working only from its own half; the half shown here is the energy office half, beginning where the shift engineer half ends."),

dict(id="t4-M09", arm="M", domain="report", cutb_side="head",
 before="""Baxter Fields Sports Club — Floodlight Note

Section 1. The lamps on the south pole were relamped in April, and the ones on the north pole in the same month two years before that.

Section 2. Burning hours are logged by the timer, which counts from the moment the contactor closes.

Section 3. The committee is of the view that the north pole lamps are close to the end of their life, and the committee considers that the drop in light on the near touchline follows from that. The committee holds that a relamp before the winter season is the cheaper course.

Section 4. A quotation was obtained from the contractor who did the April work. Every judgment in Section 3 is the committee's own, and the lighting contractor was not asked for a view on any of them.""",
 old="""The committee is of the view that the north pole lamps are close to the end of their life, and the committee considers that the drop in light on the near touchline follows from that. The committee holds that a relamp before the winter season is the cheaper course.""",
 new="""The north pole lamps are close to the end of their life, and the drop in light on the near touchline follows from that. A relamp before the winter season is the cheaper course.""",
 old_a="""The committee is of the view that the north pole lamps are close to the end of their life, and the committee considers that the drop in light on the near touchline follows from that. """,
 new_a="""The north pole lamps are close to the end of their life, and the drop in light on the near touchline follows from that. """,
 cut="""Section 3. The committee is of the view that the north pole lamps are close to the end of their life, and the committee considers that the drop in light on the near touchline follows from that. The committee holds that a relamp before the winter season is the cheaper course.""",
 site="Section 3, both sentences",
 note="Attributed judgment becomes plain assertion; whose judgment Section 3 carries is stated in Section 4, so the source of the view does not change. CUT-B shows the opening half, which does not carry Section 4.",
 framing="The note is kept in two halves, one by the club committee and one by the grounds contractor; the half shown here is the committee half, which stops where the contractor half begins."),

dict(id="t4-M10", arm="M", domain="report", cutb_side="tail",
 before="""Harburn Estates — Damp Note for Flat 6

Section 1. This note is written for the leaseholder of Flat 6 and for no other party; the freeholder receives a separate note covering the whole block.

Section 2. The meter was run along the party wall at three heights, and the highest reading of the three was at skirting level.

Section 3. Your kitchen wall carries the highest reading in the flat, and your extractor was not running when the meter was used. You dry that wall fastest by putting the extractor on a timer.

Section 4. The block was built with a solid wall on that side and there is no cavity to drain. The next visit falls due when the heating season ends.""",
 old="""Your kitchen wall carries the highest reading in the flat, and your extractor was not running when the meter was used. You dry that wall fastest by putting the extractor on a timer.""",
 new="""The kitchen wall carries the highest reading in the flat, and the extractor was not running when the meter was used. The wall dries fastest with the extractor on a timer.""",
 old_a="""Your kitchen wall carries the highest reading in the flat, and your extractor was not running when the meter was used. """,
 new_a="""The kitchen wall carries the highest reading in the flat, and the extractor was not running when the meter was used. """,
 cut="""Section 3. Your kitchen wall carries the highest reading in the flat, and your extractor was not running when the meter was used. You dry that wall fastest by putting the extractor on a timer.""",
 site="Section 3, both sentences",
 note="Direct address becomes the impersonal voice used elsewhere; who the note is written for is stated in Section 1, so the reader it speaks to does not change. CUT-B shows the second half, which does not carry Section 1.",
 framing="The note is issued in two halves, one to the leaseholder and one to the block surveyor; the half shown here is the surveyor half, beginning where the leaseholder half ends."),
]

# =============================================================== ARM M — config
ITEMS += [
dict(id="t4-M11", arm="M", domain="config", cutb_side="tail",
 before="""# Kirkwall gateway - edge node settings
# Every value in this file belongs to the network group; a change to any of
# them is agreed with that group first, whoever makes it.

[listener]
address = 10.4.19.7
port = 8443
backlog = 512

[timeouts]
# Kindly leave the two values below alone unless the network group has said
# otherwise, and do drop the group a note once you have changed them.
idle_seconds = 75
handshake_seconds = 12

[upstream]
pool = kirkwall-b
health_path = /alive
health_interval = 5
retry_limit = 2

[tls]
cert = /etc/kirkwall/edge.pem
key = /etc/kirkwall/edge.key
ciphers = modern""",
 old="""# Kindly leave the two values below alone unless the network group has said
# otherwise, and do drop the group a note once you have changed them.""",
 new="""# The two values below are changed only after the network group has said so.
# The group is told once the change is in.""",
 old_a="""# Kindly leave the two values below alone unless the network group has said
""",
 new_a="""# The two values below are changed only after the network group has said so.
""",
 cut="""[timeouts]
# Kindly leave the two values below alone unless the network group has said
# otherwise, and do drop the group a note once you have changed them.
idle_seconds = 75
handshake_seconds = 12""",
 site="the [timeouts] section, both comment lines",
 note="A polite request form becomes flat instruction; who owns the settings and what has to happen before a change is stated in the file header, so what the file requires of an editor does not change. CUT-B shows the second half, which does not carry the header.",
 framing="The file is maintained as two fragments owned by different groups and joined at deploy time; the fragment shown here is the second, beginning where the first one ends."),

dict(id="t4-M12", arm="M", domain="config", cutb_side="head",
 before="""# Ardenmoor data platform - collector settings
collector:
  interval_seconds: 30
  batch_size: 500
  retries: 3
  hosts:
    - alpha-01
    - alpha-02
    - beta-04
sink:
  kind: queue
  name: ardenmoor-main
  ack_timeout_seconds: 20
logging:
  level: info
  path: /var/log/ardenmoor/collector.log
# Every entry under sink is generated from the platform inventory and written
# back into this file by the generator, which owns all three of them.""",
 old="""  kind: queue
  name: ardenmoor-main
  ack_timeout_seconds: 20""",
 new="""  kind: "queue"
  name: "ardenmoor-main"
  ack_timeout_seconds: 20""",
 old_a="""  kind: queue
""",
 new_a="""  kind: "queue"
""",
 cut="""sink:
  kind: queue
  name: ardenmoor-main
  ack_timeout_seconds: 20
logging:
  level: info
  path: /var/log/ardenmoor/collector.log""",
 site="the sink block, all three lines",
 note="The same three settings written with quotation marks instead of bare; both spellings parse to the same values, and where the entries come from is stated in the trailing comment. A deliberately weak axis, kept because the frozen design names layout-of-expression. CUT-B shows the opening fragment, which does not carry the trailing comment.",
 framing="The file is assembled from two fragments held by different groups; the fragment shown here is the first, which stops where the second one begins."),

dict(id="t4-M13", arm="M", domain="config", cutb_side="head",
 before="""# Pelham gateway - rate settings
[window]
seconds = 60
max_calls = 240
burst = 30

[client]
# You set the two values below to match the plan the client has bought, and
# you raise a ticket with the desk when you want a plan that is not listed.
plan = standard
grace_calls = 15

[reporting]
interval_minutes = 5
sink = pelham-metrics
flush_on_exit = true

[audit]
path = /var/log/pelham/rate.log
rotate_mb = 64
keep_files = 7
# The two values in [client] are set by the desk from the signed order, and
# nobody outside the desk touches them.""",
 old="""# You set the two values below to match the plan the client has bought, and
# you raise a ticket with the desk when you want a plan that is not listed.""",
 new="""# The two values below match the plan the client has bought. A ticket goes to
# the desk when a plan that is not listed is wanted.""",
 old_a="""# You set the two values below to match the plan the client has bought, and
""",
 new_a="""# The two values below match the plan the client has bought. A ticket goes to
""",
 cut="""[client]
# You set the two values below to match the plan the client has bought, and
# you raise a ticket with the desk when you want a plan that is not listed.
plan = standard
grace_calls = 15""",
 site="the [client] section, both comment lines",
 note="Direct address becomes impersonal; who sets these two values is stated in the trailing comment, so the file names the same owner either way. CUT-B shows the opening fragment, which does not carry the trailing comment.",
 framing="The file is kept as two fragments, one held by the gateway team and one by the client desk; the fragment shown here is the gateway team fragment, which stops where the desk fragment begins."),

dict(id="t4-M14", arm="M", domain="config", cutb_side="tail",
 before="""# Ravensworth store - cache settings
# Every value below is a starting point taken from the vendor sheet. Each one
# is tuned on site after the first week and none of them is settled yet.
[cache]
size_mb = 512
ttl_seconds = 900
# It looks as though 900 is about right for most of the shelves here, and the
# eviction setting below seems to suit the mixed load we appear to be seeing.
eviction = lru
shard_count = 8

[disk]
path = /var/cache/ravensworth
reserve_mb = 2048
sync_interval_seconds = 30
scratch_path = /var/tmp/ravensworth
fsync_on_write = false

[shelves]
front_counter = 4
back_room = 3
cold_aisle = 1""",
 old="""# It looks as though 900 is about right for most of the shelves here, and the
# eviction setting below seems to suit the mixed load we appear to be seeing.""",
 new="""# 900 is right for most of the shelves here, and the eviction setting below
# suits the mixed load on this site.""",
 old_a="""# It looks as though 900 is about right for most of the shelves here, and the
""",
 new_a="""# 900 is right for most of the shelves here, and the eviction setting below
""",
 cut="""[cache]
size_mb = 512
ttl_seconds = 900
# It looks as though 900 is about right for most of the shelves here, and the
# eviction setting below seems to suit the mixed load we appear to be seeing.
eviction = lru
shard_count = 8""",
 site="the [cache] section, both comment lines",
 note="Qualified comment becomes flat comment; how settled the values are is stated in the file header (starting points, none settled), so how far the file commits to them does not change. CUT-B shows the second fragment, which does not carry the header.",
 framing="The file is joined from two fragments written by different shifts; the fragment shown here is the later one, beginning where the earlier fragment ends."),

dict(id="t4-M15", arm="M", domain="config", cutb_side="head",
 before="""# Calderbank portal - client messages
[routes]
not_found = /404
denied = /403
timeout = /504

[messages]
not_found = We are very sorry, but the page you asked for could not be found.
denied = We are afraid you do not have access to that page just at present.
timeout = The page took too long to load and we have stopped waiting for it.

[retry]
attempts = 3
backoff_seconds = 2
jitter_seconds = 1

[session]
idle_minutes = 20
cookie_name = calderbank_sid
secure_only = true
same_site = lax
# The text in [messages] is settled by the client desk and is shown to the
# visitor as it stands; none of it feeds the routing above.""",
 old="""not_found = We are very sorry, but the page you asked for could not be found.
denied = We are afraid you do not have access to that page just at present.""",
 new="""not_found = That page was not found.
denied = Access to that page is closed at present.""",
 old_a="""not_found = We are very sorry, but the page you asked for could not be found.
""",
 new_a="""not_found = That page was not found.
""",
 cut="""[messages]
not_found = We are very sorry, but the page you asked for could not be found.
denied = We are afraid you do not have access to that page just at present.
timeout = The page took too long to load and we have stopped waiting for it.""",
 site="the [messages] section, the first two entries",
 note="Two visitor-facing lines written short instead of long; each key names what its line conveys, and the trailing comment states that the text is settled by the desk and feeds nothing, so what the file does is untouched. CUT-B shows the opening fragment, which does not carry the trailing comment.",
 framing="The file is put together from two fragments owned by different desks; the fragment shown here is the first, which stops where the second one begins."),
]

# ================================================================= ARM M — code
ITEMS += [
dict(id="t4-M16", arm="M", domain="code", cutb_side="tail",
 before='''"""Connection pool for the Alderney feed.

Every borrow from this pool is matched by a release. The pool asserts the match
in debug builds and raises PoolLeak where it does not hold.
"""

_POOL = []
_MAX = 8


def borrow(timeout_seconds=5):
    if not _POOL:
        return _open_one(timeout_seconds)
    return _POOL.pop()


# Please remember to hand the connection back when you are finished with it,
# and please do try to hand it back before the timeout runs out.
def release(conn):
    if len(_POOL) < _MAX:
        _POOL.append(conn)
    else:
        conn.close()


def drain():
    while _POOL:
        _POOL.pop().close()


def size():
    return len(_POOL)


def spare():
    return _MAX - len(_POOL)


def is_full():
    return len(_POOL) >= _MAX''',
 old='''# Please remember to hand the connection back when you are finished with it,
# and please do try to hand it back before the timeout runs out.''',
 new='''# The connection is handed back once the caller has finished with it.
# The hand-back happens before the timeout runs out.''',
 old_a='''# Please remember to hand the connection back when you are finished with it,
''',
 new_a='''# The connection is handed back once the caller has finished with it.
''',
 cut='''# Please remember to hand the connection back when you are finished with it,
# and please do try to hand it back before the timeout runs out.
def release(conn):
    if len(_POOL) < _MAX:
        _POOL.append(conn)
    else:
        conn.close()''',
 site="the two comment lines above release, and release itself",
 note="A polite request becomes flat instruction; that every borrow is matched by a release, and what happens when it is not, is stated in the module docstring, so what the file requires of a caller is untouched. CUT-B shows the second fragment, which does not carry the docstring.",
 framing="The file is kept as two fragments merged at build time and owned by different teams; the fragment shown here is the second, beginning where the first one ends."),

dict(id="t4-M17", arm="M", domain="code", cutb_side="head",
 before='''from datetime import timedelta

_UNITS = {"s": 1, "m": 60, "h": 3600}


def parse_window(text):
    unit = text[-1]
    count = int(text[:-1])
    return timedelta(seconds=count * _UNITS[unit])


# You give this one a plain window such as 30m and you get back a timedelta.
# If you pass a unit that is not listed you get a KeyError, so you check first.
def window_seconds(text):
    return int(parse_window(text).total_seconds())


def clamp_window(text, lowest, highest):
    seconds = window_seconds(text)
    return max(lowest, min(highest, seconds))


# The two comment lines above are addressed to callers outside this package.
# Inside it the helpers are reached only from schedule.py, which checks first.''',
 old='''# You give this one a plain window such as 30m and you get back a timedelta.
# If you pass a unit that is not listed you get a KeyError, so you check first.''',
 new='''# This one takes a plain window such as 30m and gives back a timedelta.
# A unit that is not listed raises KeyError, so the caller checks first.''',
 old_a='''# You give this one a plain window such as 30m and you get back a timedelta.
''',
 new_a='''# This one takes a plain window such as 30m and gives back a timedelta.
''',
 cut='''# You give this one a plain window such as 30m and you get back a timedelta.
# If you pass a unit that is not listed you get a KeyError, so you check first.
def window_seconds(text):
    return int(parse_window(text).total_seconds())''',
 site="the two comment lines above window_seconds, and window_seconds itself",
 note="Direct address becomes impersonal; who the two comment lines speak to is stated in the trailing comment, so the reader they are aimed at does not change. CUT-B shows the opening fragment, which does not carry the trailing comment.",
 framing="The file is assembled from two fragments held by different teams; the fragment shown here is the first, which stops where the second one begins."),

dict(id="t4-M18", arm="M", domain="code", cutb_side="tail",
 before='''"""Bounds helpers for the Nettlefold sampler.

None of the comments in this file has been checked against the sampler. They
are notes left by whoever last touched the code and carry no more weight.
"""


def widen(low, high, factor):
    span = high - low
    pad = span * (factor - 1) / 2
    return low - pad, high + pad


# This probably holds for most inputs we see in practice, although nobody has
# gone through the small-span case with any care, so it seems safe enough here.
def tighten(low, high, factor):
    span = high - low
    pad = span * (1 - 1 / factor) / 2
    return low + pad, high - pad


def midpoint(low, high):
    return (low + high) / 2


def span(low, high):
    return high - low


def contains(low, high, value):
    return low <= value <= high


def clip(low, high, value):
    return max(low, min(high, value))''',
 old='''# This probably holds for most inputs we see in practice, although nobody has
# gone through the small-span case with any care, so it seems safe enough here.''',
 new='''# This holds for the inputs seen in practice, and the small-span case behaves
# the same way, so it is safe here.''',
 old_a='''# This probably holds for most inputs we see in practice, although nobody has
''',
 new_a='''# This holds for the inputs seen in practice, and the small-span case behaves
''',
 cut='''# This probably holds for most inputs we see in practice, although nobody has
# gone through the small-span case with any care, so it seems safe enough here.
def tighten(low, high, factor):
    span = high - low
    pad = span * (1 - 1 / factor) / 2
    return low + pad, high - pad''',
 site="the two comment lines above tighten, and tighten itself",
 note="Qualified comment becomes flat comment; how much weight any comment in the file carries is stated in the module docstring, so the standing of the note is untouched. CUT-B shows the second fragment, which does not carry the docstring.",
 framing="The file is merged from two fragments written by different maintainers; the fragment shown here is the second, beginning where the first one ends."),

dict(id="t4-M19", arm="M", domain="code", cutb_side="head",
 before='''import logging

log = logging.getLogger("hallam.sink")


def send(batch, sink):
    try:
        sink.write(batch)
    except TimeoutError:
        log.warning("Hmm, we could not get through to the sink just now, so we are having another go.")
        log.info("We are sorry to say that the batch has gone back on the queue for later.")
        return False
    return True


def send_all(batches, sink):
    sent = 0
    for b in batches:
        if send(b, sink):
            sent += 1
    return sent


def drop_stale(batches, cutoff):
    return [b for b in batches if b.stamp >= cutoff]


def split_batches(batches, limit):
    return [batches[i:i + limit] for i in range(0, len(batches), limit)]


def count_rows(batches):
    return sum(len(b.rows) for b in batches)


# Nothing reads the two log lines above except a person looking at the log file.
# The alerting keys off the counters in hallam.metrics and never off the text.''',
 old='''        log.warning("Hmm, we could not get through to the sink just now, so we are having another go.")
        log.info("We are sorry to say that the batch has gone back on the queue for later.")''',
 new='''        log.warning("sink unreachable; retrying")
        log.info("batch requeued")''',
 old_a='''        log.warning("Hmm, we could not get through to the sink just now, so we are having another go.")
''',
 new_a='''        log.warning("sink unreachable; retrying")
''',
 cut='''def send(batch, sink):
    try:
        sink.write(batch)
    except TimeoutError:
        log.warning("Hmm, we could not get through to the sink just now, so we are having another go.")
        log.info("We are sorry to say that the batch has gone back on the queue for later.")
        return False
    return True''',
 site="the body of send, both log lines",
 note="Two log lines written short instead of long; each says the same two things, and what reads them is stated in the trailing comment, so nothing downstream of the file changes. CUT-B shows the opening fragment, which does not carry the trailing comment.",
 framing="The file is put together from two fragments owned by different on-call teams; the fragment shown here is the first, which stops where the second one begins."),

dict(id="t4-M20", arm="M", domain="code", cutb_side="head",
 before='''def normalise(rows, width):
    out = []
    for r in rows:
        if len(r) > width:
            out.append(r[:width])
        else:
            out.append(r + " " * (width - len(r)))
    return out


# We clamp to the width here because the terminal wraps anything longer, and we
# would rather lose the tail than watch the table fall apart on a narrow screen.
def render(rows, width=80):
    return "\\n".join(normalise(rows, width))


def render_pairs(pairs, width=80):
    rows = [f"{k}: {v}" for k, v in pairs]
    return render(rows, width)


# The comment above was left by the two people named in AUTHORS who wrote this
# file, and it says what they decided; nobody else has touched it since.''',
 old='''# We clamp to the width here because the terminal wraps anything longer, and we
# would rather lose the tail than watch the table fall apart on a narrow screen.''',
 new='''# The width is clamped here because the terminal wraps anything longer, and
# losing the tail beats a table that falls apart on a narrow screen.''',
 old_a='''# We clamp to the width here because the terminal wraps anything longer, and we
''',
 new_a='''# The width is clamped here because the terminal wraps anything longer, and
''',
 cut='''# We clamp to the width here because the terminal wraps anything longer, and we
# would rather lose the tail than watch the table fall apart on a narrow screen.
def render(rows, width=80):
    return "\\n".join(normalise(rows, width))''',
 site="the two comment lines above render, and render itself",
 note="First person becomes impersonal; whose decision the comment carries is stated in the trailing comment, so the source of the choice does not change. CUT-B shows the opening fragment, which does not carry the trailing comment.",
 framing="The file is assembled from two fragments owned by different teams; the fragment shown here is the first, which stops where the second one begins."),
]

# ============================================================== ARM M — process
ITEMS += [
dict(id="t4-M21", arm="M", domain="process", cutb_side="tail",
 before="""Ferrybridge Depot — Weekly Tank Check

Every step below is carried out in the order given and none of them is left out; the shift supervisor signs the sheet only when all eight have been done.

1. Open the compound gate and set the wheel chocks.
2. Read the level gauge on the north tank and note the figure on the sheet.
3. Read the level gauge on the south tank and note the figure on the sheet.
4. If either figure has moved by more than a tenth since last week, you are asked to telephone the duty engineer before going on.
5. Please look over the bund for standing water, and please note anything you find on the sheet.
6. Check that the two isolation valves turn freely by hand.
7. Close the compound gate and return the chocks to the rack.
8. Hand the sheet to the shift supervisor before leaving the site.""",
 old="""4. If either figure has moved by more than a tenth since last week, you are asked to telephone the duty engineer before going on.
5. Please look over the bund for standing water, and please note anything you find on the sheet.""",
 new="""4. If either figure has moved by more than a tenth since last week, telephone the duty engineer before going on.
5. Look over the bund for standing water and note anything you find on the sheet.""",
 old_a="""4. If either figure has moved by more than a tenth since last week, you are asked to telephone the duty engineer before going on.
""",
 new_a="""4. If either figure has moved by more than a tenth since last week, telephone the duty engineer before going on.
""",
 cut="""4. If either figure has moved by more than a tenth since last week, you are asked to telephone the duty engineer before going on.
5. Please look over the bund for standing water, and please note anything you find on the sheet.
6. Check that the two isolation valves turn freely by hand.""",
 site="steps 4 to 6",
 note="Softened request form becomes direct instruction; that every step is carried out and none left out is stated in the line above step 1, so what the round requires does not change. CUT-B shows the second half, which does not carry that line.",
 framing="The check is split between two people who each work from their own half of the card; the half shown here is the second, beginning where the first person hands over."),

dict(id="t4-M22", arm="M", domain="process", cutb_side="head",
 before="""Marlowe Bakery — Oven Changeover Card

1. Set the deck to the changeover temperature and wait for the lamp to go out.
2. Draw the trays out of the lower deck and stack them on the rack by the door.
3. You wipe the seals with the damp cloth and you check the hinge pins for play.
4. You set the timer to twenty minutes and you stay with the oven until it rings.
5. Load the trays for the next run into the upper deck.
6. Log the changeover time in the book at the end of the bench.
7. Return the cloth to the sink and the rack to the wall.

This card is written for the relief operator. The regular operator works from the wall chart instead, which carries the same seven steps in the same order.""",
 old="""3. You wipe the seals with the damp cloth and you check the hinge pins for play.
4. You set the timer to twenty minutes and you stay with the oven until it rings.""",
 new="""3. The seals are wiped with the damp cloth and the hinge pins checked for play.
4. The timer is set to twenty minutes and somebody stays with the oven until it rings.""",
 old_a="""3. You wipe the seals with the damp cloth and you check the hinge pins for play.
""",
 new_a="""3. The seals are wiped with the damp cloth and the hinge pins checked for play.
""",
 cut="""3. You wipe the seals with the damp cloth and you check the hinge pins for play.
4. You set the timer to twenty minutes and you stay with the oven until it rings.
5. Load the trays for the next run into the upper deck.""",
 site="steps 3 to 5",
 note="Direct address becomes impersonal; who the card is written for is stated in the closing line, so the person it speaks to does not change. CUT-B shows the opening half, which does not carry the closing line.",
 framing="The card is kept in two halves by the two bakers on the shift; the half shown here is the first baker half, which stops where the second baker half begins."),

dict(id="t4-M23", arm="M", domain="process", cutb_side="tail",
 before="""Kestrel Analytical — Sample Intake Round

Every step below is carried out by the intake technician on duty, and nobody else touches the samples between the door and the fridge.

1. Take the box from the courier and check the seal against the docket.
2. Open the box on the intake bench and lift out the racks.
3. The barcodes are scanned into the bench terminal and the docket number is entered beside them.
4. Any tube with a cracked cap is set aside on the amber tray and is not scanned.
5. The racks are carried to the fridge and placed on the shelf marked for the day.
6. Sign the docket and put it in the tray by the door.
7. Return the empty box to the courier point at the end of the round.""",
 old="""3. The barcodes are scanned into the bench terminal and the docket number is entered beside them.
4. Any tube with a cracked cap is set aside on the amber tray and is not scanned.
5. The racks are carried to the fridge and placed on the shelf marked for the day.""",
 new="""3. The technician scans the barcodes into the bench terminal and enters the docket number beside them.
4. The technician sets aside any tube with a cracked cap on the amber tray and leaves it unscanned.
5. The technician carries the racks to the fridge and places them on the shelf marked for the day.""",
 old_a="""3. The barcodes are scanned into the bench terminal and the docket number is entered beside them.
""",
 new_a="""3. The technician scans the barcodes into the bench terminal and enters the docket number beside them.
""",
 cut="""3. The barcodes are scanned into the bench terminal and the docket number is entered beside them.
4. Any tube with a cracked cap is set aside on the amber tray and is not scanned.
5. The racks are carried to the fridge and placed on the shelf marked for the day.""",
 site="steps 3 to 5",
 note="Agentless voice becomes active voice naming the doer; who carries out every step is stated in the line above step 1, so the round names the same person either way. CUT-B shows the second half, which does not carry that line.",
 framing="The round is divided between the intake bench and the fridge room, each holding its own half; the half shown here is the fridge room half, beginning where the bench half ends."),

dict(id="t4-M24", arm="M", domain="process", cutb_side="head",
 before="""Whitlock Print Room — Plate Wash Round

1. Put on the apron and the long gloves from the hook by the sink.
2. What happens next is that the wash tank is opened and the level of the solvent is looked at, so that the round does not begin with a tank too low to work in.
3. The way the plates are handled is that they are lifted from the rack one at a time and lowered into the tank by the edges, never by the face.
4. Set the timer for four minutes and stand clear of the tank.
5. Lift the plates out and stand them on the drainer in the same order.
6. Wipe the tank rim and close the lid.
7. Hang the apron and the gloves back on the hook.

The seven steps above are the whole of the round. The notice by the door gives the same seven and is the one the auditor works from.""",
 old="""2. What happens next is that the wash tank is opened and the level of the solvent is looked at, so that the round does not begin with a tank too low to work in.
3. The way the plates are handled is that they are lifted from the rack one at a time and lowered into the tank by the edges, never by the face.""",
 new="""2. Open the wash tank and look at the level of the solvent, so that the round does not begin with a tank too low to work in.
3. Lift the plates from the rack one at a time and lower them into the tank by the edges, never by the face.""",
 old_a="""2. What happens next is that the wash tank is opened and the level of the solvent is looked at, so that the round does not begin with a tank too low to work in.
""",
 new_a="""2. Open the wash tank and look at the level of the solvent, so that the round does not begin with a tank too low to work in.
""",
 cut="""2. What happens next is that the wash tank is opened and the level of the solvent is looked at, so that the round does not begin with a tank too low to work in.
3. The way the plates are handled is that they are lifted from the rack one at a time and lowered into the tank by the edges, never by the face.""",
 site="steps 2 and 3",
 note="Two steps written the long way round become two written short; the same seven steps are carried on the door notice, named in the closing line, so what the round consists of does not change. CUT-B shows the opening half, which does not carry the closing line.",
 framing="The round is worked by two people from two halves of the card; the half shown here is the first half, which stops where the second person takes over."),
]

# =============================================================== ARM C — policy
ITEMS += [
dict(id="t4-C01", arm="C", domain="policy",
 before="""Ravenglass Sports Trust — Pitch Booking Notice

Part 1. Pitches are let by the hour on weekday evenings and by the half-day at weekends, and the let takes in the changing rooms next to the pitch used.

Part 2. Bookings open twelve weeks ahead of the date wanted, and a booking is held for three days without payment. Where payment has not reached the office by the end of the third day, the booking is released and the slot goes back on the list.

Part 3. Clubs cancel through the office rather than through the groundsman, and a cancellation made more than a week ahead carries no charge.

Part 4. The floodlights are switched on by the groundsman at the start of the let and off at the end of it. Clubs are not given access to the switch room at any time.""",
 old="""twelve weeks ahead of the date wanted""",
 new="""eight weeks ahead of the date wanted""",
 cut="""Part 2. Bookings open twelve weeks ahead of the date wanted, and a booking is held for three days without payment. Where payment has not reached the office by the end of the third day, the booking is released and the slot goes back on the list.""",
 site="Part 2, first sentence",
 note="Rules-type: the window in which a booking can be opened. Both sentences of Part 2 state the window and what follows from it, so the passage grounds the change on its own."),

dict(id="t4-C02", arm="C", domain="policy",
 before="""Hollybank Community Hall — Key Holder Notice

Part 1. The hall is let to regular hirers by the season and to one-off hirers by the evening, and both kinds of hire are booked through the same office.

Part 2. Keys are cut for the hall only by the locksmith named on the office board, and a cut key is signed for at the counter.

Part 3. A key is issued to one named person for each regular hirer, and that person is the one who opens and closes the hall. Where the named person cannot attend, the key goes back to the office beforehand and is collected by whoever takes their place.

Part 4. Keys are handed back at the end of the season, and a hirer who does not hand a key back pays the cost of a lock change. The office keeps a list of who holds which key.""",
 old="""A key is issued to one named person for each regular hirer, and that person is the one who opens and closes the hall.""",
 new="""A key is issued to two named people for each regular hirer, and either of them opens and closes the hall.""",
 cut="""Part 3. A key is issued to one named person for each regular hirer, and that person is the one who opens and closes the hall. Where the named person cannot attend, the key goes back to the office beforehand and is collected by whoever takes their place.""",
 site="Part 3, first sentence",
 note="Rules-type: how many people hold a key for a hirer. Part 3 states the issue and what happens when the holder cannot attend, so the passage grounds the change on its own."),

dict(id="t4-C03", arm="C", domain="policy",
 before="""Dunbarrow Care Home — Visiting Notice

Part 1. Visitors sign in at the desk in the entrance hall and sign out again on leaving, and the book stays at the desk at all times.

Part 2. Visits take place in the day room, in the garden when the weather allows, or in a resident's own room where the resident asks for that.

Part 3. Visits are booked by six in the evening on the day before, and a booking covers up to two visitors at a time. Where more than two wish to come, the extra visitors are booked into a second slot on the same day.

Part 4. Children under twelve are accompanied by an adult throughout, and the home asks that dogs are left outside except for assistance dogs.""",
 old="""by six in the evening on the day before""",
 new="""by nine in the morning on the day of the visit""",
 cut="""Part 3. Visits are booked by six in the evening on the day before, and a booking covers up to two visitors at a time. Where more than two wish to come, the extra visitors are booked into a second slot on the same day.""",
 site="Part 3, first sentence",
 note="Rules-type: the cut-off by which a visit is booked. Part 3 carries the cut-off and the booking it governs, so the passage grounds the change on its own."),

dict(id="t4-C04", arm="C", domain="policy",
 before="""Whinfell Angling Club — Day Ticket Notice

Part 1. Day tickets are sold at the lodge from first light and at the tackle shop in the village during opening hours, and the price is the same at both.

Part 2. A day ticket covers the east bank only. The west bank is fished by season members, whose permits carry a photograph.

Part 3. The deposit on a lodge key is thirty pounds, and it comes back in full when the key is returned undamaged. A key that is not returned within a week of the ticket date is treated as lost and the deposit is kept.

Part 4. Fish are returned to the water alive, and keep nets are used only during a match. The bailiff walks both banks each morning.""",
 old="""thirty pounds""",
 new="""fifty pounds""",
 cut="""Part 3. The deposit on a lodge key is thirty pounds, and it comes back in full when the key is returned undamaged. A key that is not returned within a week of the ticket date is treated as lost and the deposit is kept.""",
 site="Part 3, first sentence",
 note="Facts-type: the sum held as a deposit. Part 3 states the sum, when it comes back and when it is kept, so the passage grounds the change on its own."),

dict(id="t4-C05", arm="C", domain="policy",
 before="""Stanbury Museum — Volunteer Stewarding Notice

Part 1. Stewards work in pairs on the ground floor and singly on the upper floor, and the rota is drawn up a month at a time.

Part 2. A steward opens the gallery at ten and closes it at five, and the keys are drawn from and returned to the front desk on each shift.

Part 3. Stewards take a break of thirty minutes on a full-day shift, and the break is covered by the reserve steward named on the rota. A half-day shift carries no break at all.

Part 4. Stewards wear the badge issued at induction and keep it visible while on the floor. A lost badge is replaced at the desk on the day it is missed.""",
 old="""a break of thirty minutes on a full-day shift""",
 new="""a break of forty-five minutes on a full-day shift""",
 cut="""Part 3. Stewards take a break of thirty minutes on a full-day shift, and the break is covered by the reserve steward named on the rota. A half-day shift carries no break at all.""",
 site="Part 3, first sentence",
 note="Facts-type: the length of the break on a full-day shift. Part 3 states the length, who covers it and the half-day case, so the passage grounds the change on its own."),
]

# =============================================================== ARM C — report
ITEMS += [
dict(id="t4-C06", arm="C", domain="report",
 before="""Brackenhurst Depot — Fuel Line Note

Section 1. The line from the bulk tank to the pump island was walked on 12 May in dry weather, with the pumps shut down for the visit.

Section 2. The line runs in a shallow trench for most of its length and comes above ground at the island end.

Section 3. The wet patch found on the walk sits four metres from the tank end of the trench, and the ground there was damp to a depth of a spade's blade. Nothing was seen at the island end, which was dry along its whole run.

Section 4. The pumps were run for ten minutes at the end of the visit and the meter agreed with the tank dip to within two litres.""",
 old="""four metres from the tank end of the trench""",
 new="""nineteen metres from the tank end of the trench""",
 cut="""Section 3. The wet patch found on the walk sits four metres from the tank end of the trench, and the ground there was damp to a depth of a spade's blade. Nothing was seen at the island end, which was dry along its whole run.""",
 site="Section 3, first sentence",
 note="Facts-type: where along the trench the wet patch sits. Section 3 gives the position, the depth and the state of the other end, so the passage grounds the change on its own."),

dict(id="t4-C07", arm="C", domain="report",
 before="""Netherby Library — Stock Check Note

Section 1. The check covered the lending shelves on the ground floor and was done over two evenings after closing.

Section 2. Items were counted by shelf and the count was entered on the tally sheet at the end of each bay.

Section 3. Four items on the large print shelves could not be found against the tally, and all four had been borrowed and returned within the last month. Two of the four were found the next morning on the returns trolley.

Section 4. The upper floor was not part of this check. The next check falls due at the end of the financial year.""",
 old="""Four items on the large print shelves could not be found against the tally, and all four had been borrowed and returned within the last month. Two of the four were found the next morning on the returns trolley.""",
 new="""Nine items on the large print shelves could not be found against the tally, and all nine had been borrowed and returned within the last month. Two of the nine were found the next morning on the returns trolley.""",
 cut="""Section 3. Four items on the large print shelves could not be found against the tally, and all four had been borrowed and returned within the last month. Two of the four were found the next morning on the returns trolley.""",
 site="Section 3, both sentences",
 note="Facts-type: how many items were missing against the tally. Section 3 carries the count, what was known about the items and how many turned up, so the passage grounds the change on its own."),

dict(id="t4-C08", arm="C", domain="report",
 before="""Culross Hall — Boiler Service Note

Section 1. The boiler was looked at by the service engineer on his half-yearly visit, with the system cold.

Section 2. The expansion vessel holds its charge and the pressure gauge reads a little over one bar on a cold system.

Section 3. The burner was last stripped and cleaned in April, and the hours counter has run four hundred hours since then. The flame picture was even across the head on the day of the visit.

Section 4. The flue was swept from the boiler end and the sweepings were bagged and taken away. No further work was left open.""",
 old="""last stripped and cleaned in April, and the hours counter has run four hundred hours since then""",
 new="""last stripped and cleaned in September, and the hours counter has run nine hundred hours since then""",
 cut="""Section 3. The burner was last stripped and cleaned in April, and the hours counter has run four hundred hours since then. The flame picture was even across the head on the day of the visit.""",
 site="Section 3, first sentence",
 note="Facts-type: when the burner was last cleaned and how many hours have run since. Section 3 carries both figures together, so the passage grounds the change on its own."),

dict(id="t4-C09", arm="C", domain="report",
 before="""Aldersgate Practice — Waiting Room Note

Section 1. The count below was taken on four Tuesdays in the same month, between eight in the morning and noon.

Section 2. Patients were counted as they were called rather than as they arrived, so a patient who left before being called is not in the count.

Section 3. The busiest hour of the four mornings was the one from nine to ten, which took 41 patients across the four days. The quietest was the one from eleven to noon, at 17 patients.

Section 4. The counter was the same member of the desk staff on each morning. No count was taken in the afternoon.""",
 old="""the one from nine to ten, which took 41 patients across the four days. The quietest was the one from eleven to noon, at 17 patients""",
 new="""the one from eight to nine, which took 52 patients across the four days. The quietest was the one from eleven to noon, at 12 patients""",
 cut="""Section 3. The busiest hour of the four mornings was the one from nine to ten, which took 41 patients across the four days. The quietest was the one from eleven to noon, at 17 patients.""",
 site="Section 3, both sentences",
 note="Facts-type: which hour was busiest and the two counts. Section 3 names both hours and both figures, so the passage grounds the change on its own."),

dict(id="t4-C10", arm="C", domain="report",
 before="""Pennfield Estate — Gutter Note for Block C

Section 1. The gutters were looked at from a ladder at four points and from the ground along the rest of the run.

Section 2. The run is cast iron on the front elevation and plastic on the rear, and the two meet at the north corner.

Section 3. The downpipe at the east gable is blocked at the shoe and water stands in the gutter above it after rain. The downpipe at the west gable was running clear on the day of the visit.

Section 4. No work was carried out during the visit. A quotation for clearing has been asked for from the contractor.""",
 old="""The downpipe at the east gable is blocked at the shoe and water stands in the gutter above it after rain. The downpipe at the west gable was running clear""",
 new="""The downpipe at the west gable is blocked at the shoe and water stands in the gutter above it after rain. The downpipe at the east gable was running clear""",
 cut="""Section 3. The downpipe at the east gable is blocked at the shoe and water stands in the gutter above it after rain. The downpipe at the west gable was running clear on the day of the visit.""",
 site="Section 3, both sentences",
 note="Facts-type: which of the two downpipes is blocked. Section 3 names both gables and the state of each, so the passage grounds the change on its own."),
]

# =============================================================== ARM C — config
ITEMS += [
dict(id="t4-C11", arm="C", domain="config",
 before="""# Baswick relay - transport settings
[socket]
bind = 0.0.0.0
port = 9210
backlog = 256

[timeouts]
# The idle timeout is three times the longest run seen on this link, and the
# handshake timeout is a quarter of the idle one.
idle_seconds = 60
handshake_seconds = 15

[peers]
primary = baswick-a
secondary = baswick-b
probe_seconds = 10

[queue]
max_items = 5000
spill_path = /var/spool/baswick
drain_on_stop = true

[audit]
path = /var/log/baswick/relay.log
rotate_mb = 32
keep_files = 10

[limits]
max_frame_bytes = 65536
max_open_sockets = 64""",
 old="""idle_seconds = 60
handshake_seconds = 15""",
 new="""idle_seconds = 120
handshake_seconds = 30""",
 cut="""[timeouts]
# The idle timeout is three times the longest run seen on this link, and the
# handshake timeout is a quarter of the idle one.
idle_seconds = 60
handshake_seconds = 15""",
 site="the [timeouts] section, both settings",
 note="Facts-type: the two timeout values. The comment inside the section states how the two are related, and the pair still stands in that relation, so the passage grounds the change on its own."),

dict(id="t4-C12", arm="C", domain="config",
 before="""# Tarnbeck ingest - reader settings
reader:
  poll_seconds: 15
  window_size: 200
source:
  # The reader takes from the first host that answers, tried in the order
  # listed, and the order below is the one the desk asked for.
  hosts:
    - tarn-a
    - tarn-b
    - tarn-c
  port: 7440
store:
  path: /var/lib/tarnbeck
  keep_days: 30
alerts:
  email: desk@tarnbeck.example
  threshold_lag_seconds: 90
  quiet_hours: none
retry:
  attempts: 4
  backoff_seconds: 8
  give_up_after_minutes: 20
audit:
  path: /var/log/tarnbeck/reader.log
  keep_days: 45""",
 old="""    - tarn-a
    - tarn-b
    - tarn-c""",
 new="""    - tarn-c
    - tarn-a
    - tarn-b""",
 cut="""source:
  # The reader takes from the first host that answers, tried in the order
  # listed, and the order below is the one the desk asked for.
  hosts:
    - tarn-a
    - tarn-b
    - tarn-c
  port: 7440""",
 site="the source block, the three host entries",
 note="Facts-type: which host is tried first. The comment inside the block states that the order is the order tried, so the passage grounds the change on its own."),

dict(id="t4-C13", arm="C", domain="config",
 before="""# Colwick portal - session settings
[server]
listen = 127.0.0.1
port = 8080
workers = 4

[session]
# Cookies are marked secure because the portal is reached over TLS at the edge,
# and the two settings below follow the pattern used by the other portals.
secure_only = true
same_site = lax
idle_minutes = 20

[static]
root = /srv/colwick/public
cache_seconds = 600
gzip = on

[health]
path = /healthz
interval_seconds = 30
timeout_seconds = 3

[upload]
max_bytes = 8388608
temp_dir = /var/tmp/colwick
allowed_types = pdf,png,jpg
[mail]
relay = mail.colwick.example
from_address = portal@colwick.example""",
 old="""same_site = lax
idle_minutes = 20""",
 new="""same_site = strict
idle_minutes = 45""",
 cut="""[session]
# Cookies are marked secure because the portal is reached over TLS at the edge,
# and the two settings below follow the pattern used by the other portals.
secure_only = true
same_site = lax
idle_minutes = 20""",
 site="the [session] section, the last two settings",
 note="Facts-type: the same-site setting and the idle window. The comment inside the section covers both, so the passage grounds the change on its own."),

dict(id="t4-C14", arm="C", domain="config",
 before="""# Rushmere archive - sweep settings
[source]
root = /srv/rushmere/incoming
pattern = *.tar.gz
min_age_minutes = 30

[target]
# Sweeps land in the month folder under the root named here, and the checksum
# file is written beside the archive it belongs to.
root = /srv/rushmere/archive
checksum = sha256
verify_after_write = true

[schedule]
hour = 2
minute = 15
weekday = daily

[retention]
keep_months = 84
prune_on_sunday = true
dry_run = false

[notify]
mailbox = archive@rushmere.example
on_success = false
on_failure = true
[limits]
max_parallel_sweeps = 2
bandwidth_mb_per_second = 40""",
 old="""root = /srv/rushmere/archive
checksum = sha256""",
 new="""root = /mnt/vault/rushmere
checksum = sha512""",
 cut="""[target]
# Sweeps land in the month folder under the root named here, and the checksum
# file is written beside the archive it belongs to.
root = /srv/rushmere/archive
checksum = sha256
verify_after_write = true""",
 site="the [target] section, the root and checksum settings",
 note="Facts-type: where sweeps land and which checksum is written. The comment inside the section states what both settings do, so the passage grounds the change on its own."),

dict(id="t4-C15", arm="C", domain="config",
 before="""# Ilkeston counter - queue settings
[queue]
# The counter takes one ticket at a time. The limit below counts the people
# waiting, not the number served in an hour.
max_waiting = 40
warn_at = 30

[display]
board_rows = 8
refresh_seconds = 5
show_average_wait = true

[hours]
open = 0900
close = 1630
break_start = 1300
break_end = 1330

[audit]
path = /var/log/ilkeston/queue.log
keep_days = 90
include_ticket_text = false

[printer]
device = /dev/usb/lp0
ticket_width_mm = 58""",
 old="""max_waiting = 40
warn_at = 30""",
 new="""max_waiting = 25
warn_at = 20""",
 cut="""[queue]
# The counter takes one ticket at a time. The limit below counts the people
# waiting, not the number served in an hour.
max_waiting = 40
warn_at = 30""",
 site="the [queue] section, both settings",
 note="Facts-type: how many people the queue holds and where the warning falls. The comment inside the section says what the limit counts, so the passage grounds the change on its own."),
]

# ================================================================= ARM C — code
ITEMS += [
dict(id="t4-C16", arm="C", domain="code",
 before='''"""Batch sizing for the Rothley uploader."""

_MAX_ROWS = 500
_MAX_BYTES = 262144


def chunk(rows):
    out, cur, size = [], [], 0
    for r in rows:
        # A chunk closes when either limit is reached. The row that would cross
        # a limit starts the next chunk instead of ending this one.
        if len(cur) >= _MAX_ROWS or size + len(r) > _MAX_BYTES:
            out.append(cur)
            cur, size = [], 0
        cur.append(r)
        size += len(r)
    if cur:
        out.append(cur)
    return out


def chunk_count(rows):
    return len(chunk(rows))

def largest_chunk(rows):
    return max((len(c) for c in chunk(rows)), default=0)

def fits(row):
    return len(row) <= _MAX_BYTES

def total_bytes(rows):
    return sum(len(r) for r in rows)


def would_split(rows):
    return total_bytes(rows) > _MAX_BYTES or len(rows) > _MAX_ROWS


def describe(rows):
    return f"{len(rows)} rows in {chunk_count(rows)} chunks"''',
 old='''        # A chunk closes when either limit is reached. The row that would cross
        # a limit starts the next chunk instead of ending this one.
        if len(cur) >= _MAX_ROWS or size + len(r) > _MAX_BYTES:''',
 new='''        # A chunk closes only when both limits are reached. The row that would
        # cross both starts the next chunk instead of ending this one.
        if len(cur) >= _MAX_ROWS and size + len(r) > _MAX_BYTES:''',
 cut='''    for r in rows:
        # A chunk closes when either limit is reached. The row that would cross
        # a limit starts the next chunk instead of ending this one.
        if len(cur) >= _MAX_ROWS or size + len(r) > _MAX_BYTES:
            out.append(cur)
            cur, size = [], 0
        cur.append(r)
        size += len(r)''',
 site="the body of chunk, the comment and the test below it",
 note="Rules-type: the test that closes a chunk. The comment and the test sit together inside the function and agree with each other after the change, so the passage grounds it on its own."),

dict(id="t4-C17", arm="C", domain="code",
 before='''"""Counting helpers for the Marsden desk."""

from collections import Counter


def tally(entries):
    return Counter(e.label for e in entries)

def summarise(counts, top=5):
    """Give back the entries with the highest counts.

    The number given back is the top argument. Ties are broken by the entry
    text, so that two runs over the same input agree.
    """
    pairs = sorted(((v, k) for k, v in counts.items()), reverse=True)
    return [k for _, k in pairs[:top]]


def share(counts, label):
    total = sum(counts.values())
    return counts.get(label, 0) / total if total else 0.0

def labels(entries):
    return sorted({e.label for e in entries})

def busiest(counts):
    return summarise(counts, top=1)[0] if counts else None

def total(counts):
    return sum(counts.values())

def rarest(counts):
    return min(counts, key=counts.get) if counts else None

def above(counts, floor):
    return {k: v for k, v in counts.items() if v >= floor}


def as_lines(counts):
    return [f"{k} {v}" for k, v in sorted(counts.items())]''',
 old='''def summarise(counts, top=5):''',
 new='''def summarise(counts, top=25):''',
 cut='''def summarise(counts, top=5):
    """Give back the entries with the highest counts.

    The number given back is the top argument. Ties are broken by the entry
    text, so that two runs over the same input agree.
    """
    pairs = sorted(((v, k) for k, v in counts.items()), reverse=True)
    return [k for _, k in pairs[:top]]''',
 site="the first line of summarise",
 note="Facts-type: how many entries come back when the caller names none. The docstring inside the function says the number is the top argument, so the passage grounds the change on its own."),

dict(id="t4-C18", arm="C", domain="code",
 before='''"""Window helpers for the Coleford sampler."""


def in_window(reading, floor, ceiling):
    # A reading counts when it sits inside the pair of limits passed in, with
    # the floor included and the ceiling left out.
    return floor <= reading < ceiling


def count_in_window(readings, floor, ceiling):
    return sum(1 for r in readings if in_window(r, floor, ceiling))


def first_in_window(readings, floor, ceiling):
    for r in readings:
        if in_window(r, floor, ceiling):
            return r
    return None


def window_span(floor, ceiling):
    return ceiling - floor


def midpoint(floor, ceiling):
    return (floor + ceiling) / 2''',
 old='''    # A reading counts when it sits inside the pair of limits passed in, with
    # the floor included and the ceiling left out.
    return floor <= reading < ceiling''',
 new='''    # A reading counts when it sits inside the pair of limits passed in, with
    # the floor left out and the ceiling included.
    return floor < reading <= ceiling''',
 cut='''def in_window(reading, floor, ceiling):
    # A reading counts when it sits inside the pair of limits passed in, with
    # the floor included and the ceiling left out.
    return floor <= reading < ceiling''',
 site="the body of in_window, the comment and the line below it",
 note="Rules-type: which of the two limits a reading may sit on. The comment and the test sit together inside the function and agree with each other after the change, so the passage grounds it on its own."),

dict(id="t4-C19", arm="C", domain="code",
 before='''"""Retry helper for the Tenbury feed."""

from time import sleep


def with_retry(fn, attempts=3, pause_seconds=2):
    # The call is tried up to the number of attempts named here, with a fixed
    # pause between tries. A KeyError is passed straight back to the caller.
    for n in range(attempts):
        try:
            return fn()
        except KeyError:
            raise
        except OSError:
            if n == attempts - 1:
                raise
            sleep(pause_seconds)


def try_once(fn):
    return with_retry(fn, attempts=1)


def patient(fn):
    return with_retry(fn, attempts=10, pause_seconds=30)


def name_of(fn):
    return getattr(fn, "__name__", "anonymous")


def quick(fn):
    return with_retry(fn, attempts=2, pause_seconds=1)


def describe(attempts, pause_seconds):
    return f"{attempts} tries, {pause_seconds}s apart"''',
 old='''def with_retry(fn, attempts=3, pause_seconds=2):''',
 new='''def with_retry(fn, attempts=6, pause_seconds=5):''',
 cut='''def with_retry(fn, attempts=3, pause_seconds=2):
    # The call is tried up to the number of attempts named here, with a fixed
    # pause between tries. A KeyError is passed straight back to the caller.
    for n in range(attempts):
        try:
            return fn()''',
 site="the first line of with_retry",
 note="Facts-type: how many tries and how long a pause the caller gets by default. The comment inside the function names both, so the passage grounds the change on its own."),

dict(id="t4-C20", arm="C", domain="code",
 before='''"""Lookup helpers for the Wrenbury table."""


def lookup(table, name):
    # A name that is not in the table gives back None. The caller decides what
    # an absent name means.
    if name not in table:
        return None
    return table[name]


def lookup_many(table, names):
    return [lookup(table, n) for n in names]


def known(table, name):
    return name in table


def merge(left, right):
    out = dict(left)
    out.update(right)
    return out

def names(table):
    return sorted(table)


def without(table, name):
    out = dict(table)
    out.pop(name, None)
    return out


def counts(table):
    return {k: len(v) for k, v in table.items()}


def describe(table):
    return f"{len(table)} entries"''',
 old='''    # A name that is not in the table gives back None. The caller decides what
    # an absent name means.
    if name not in table:
        return None''',
 new='''    # A name that is not in the table raises KeyError. The caller catches it
    # wherever an absent name is allowed.
    if name not in table:
        raise KeyError(name)''',
 cut='''def lookup(table, name):
    # A name that is not in the table gives back None. The caller decides what
    # an absent name means.
    if name not in table:
        return None
    return table[name]''',
 site="the body of lookup, the comment and the two lines below it",
 note="Rules-type: what a name that is missing from the table gives the caller. The comment and the branch sit together inside the function and agree with each other after the change, so the passage grounds it on its own."),
]

# ============================================================== ARM C — process
ITEMS += [
dict(id="t4-C21", arm="C", domain="process",
 before="""Southwold Hatchery — Morning Tank Round

1. Unlock the shed and switch on the overhead lights.
2. Read the thermometer on each of the four tanks and note the figures on the board.
3. Where a tank reads above sixteen degrees, open the chiller valve a quarter turn and note the time on the board.
4. Feed each tank from the hopper marked with its number, one scoop to each tank.
5. Skim the surface of each tank with the long net and empty the net into the waste bin.
6. Check the outflow screens for weed and clear anything that is caught.
7. Lock the shed and hang the key on the hook in the office.""",
 old="""above sixteen degrees, open the chiller valve a quarter turn""",
 new="""above nineteen degrees, open the chiller valve a half turn""",
 cut="""3. Where a tank reads above sixteen degrees, open the chiller valve a quarter turn and note the time on the board.
4. Feed each tank from the hopper marked with its number, one scoop to each tank.""",
 site="steps 3 to 5",
 note="Rules-type: the reading at which the valve is opened, and how far. Step 3 carries the reading, the action and the note that follows it, so the passage grounds the change on its own."),

dict(id="t4-C22", arm="C", domain="process",
 before="""Ledbury Cellars — Cask Racking Round

1. Bring the empty casks up from the cold store and stand them by the bench.
2. Draw a sample from the settling tank and hold it against the window light.
3. Where the sample is clear, rack two litres into each cask and stopper it by hand.
4. Where the sample is cloudy, leave the tank a further day and stop the round here.
5. Label each stoppered cask with the tank number and the day of the round.
6. Roll the stoppered casks to the cold store and stand them upright.
7. Rinse the sample glass and hang it back over the bench.
8. Enter the tank number and the cask count in the cellar book.
9. Sweep the bench area and put the empty pallets by the door for collection.""",
 old="""rack two litres into each cask and stopper it by hand""",
 new="""rack five litres into each cask and stopper it by machine""",
 cut="""3. Where the sample is clear, rack two litres into each cask and stopper it by hand.
4. Where the sample is cloudy, leave the tank a further day and stop the round here.
5. Label each stoppered cask with the tank number and the day of the round.""",
 site="steps 3 to 5",
 note="Facts-type: how much goes into each cask and how it is stoppered. Step 3 states the condition and the action together, so the passage grounds the change on its own."),

dict(id="t4-C23", arm="C", domain="process",
 before="""Halstead Clinic — Instrument Return Round

1. Collect the trays from the two treatment rooms at the end of the list.
2. Count the instruments on each tray against the card taped to the tray.
3. Any instrument that is missing from a tray is put on the amber shelf and the shelf card is marked.
4. Instruments from the amber shelf are chased at the end of the following list.
5. Wipe each tray down and stack the trays by the hatch.
6. Pass the trays through the hatch to the sterile room in tray order.
7. Hang the tray cards on the rail beside the hatch.
8. Wipe the hatch rim and the trolley handles with the blue cloth.
9. Take the blue cloth to the laundry bin on the way out of the room.""",
 old="""is put on the amber shelf and the shelf card is marked.
4. Instruments from the amber shelf are chased at the end of the following list.""",
 new="""is written on the hatch board and the board is dated.
4. Instruments on the hatch board are chased at the end of the following list.""",
 cut="""3. Any instrument that is missing from a tray is put on the amber shelf and the shelf card is marked.
4. Instruments from the amber shelf are chased at the end of the following list.
5. Wipe each tray down and stack the trays by the hatch.""",
 site="steps 3 and 4",
 note="Rules-type: where a missing instrument is noted and where it is chased from. Steps 3 and 4 name the same place twice inside the passage and agree after the change, so the passage grounds it on its own."),

dict(id="t4-C24", arm="C", domain="process",
 before="""Barrow Foundry — Furnace Shutdown Round

1. Stop the charge feed and let the last charge run through.
2. Close the gas valve at the wall and note the meter reading on the sheet.
3. Leave the extraction running for twenty minutes after the valve is closed.
4. Rake the hearth clear once the extraction has stopped and bag the sweepings.
5. Check the door seals and the sight glass while the hearth is cool.
6. Drop the shutter and padlock it to the floor ring.
7. Hand the sheet with the meter reading to the shift office.
8. Return the rake and the bagging tools to the rack by the door.
9. Switch off the bay lights and sign out at the gatehouse.""",
 old="""running for twenty minutes after the valve is closed""",
 new="""running for ninety minutes after the valve is closed""",
 cut="""3. Leave the extraction running for twenty minutes after the valve is closed.
4. Rake the hearth clear once the extraction has stopped and bag the sweepings.
5. Check the door seals and the sight glass while the hearth is cool.""",
 site="step 3",
 note="Facts-type: how long the extraction runs on after the valve closes. Step 3 states the interval and step 4 turns on it, both inside the passage, so it grounds the change on its own."),
]

# =============================================================== ARM P — policy
ITEMS += [
dict(id="t4-P01", arm="P", domain="policy",
 before="""Kelso Village Hall — Charges Notice

Part 1. The sums in Part 3 are worked out from the whole-evening rate, which is the basis the trustees settled on for the current year. The hourly rate is kept in the ledger for comparison only, and a standard evening priced from it comes to sixty pounds.

Part 2. The hall is let to village organisations, to households in the parish and to outside hirers, and all three are charged from the same basis.

Part 3. A standard evening let is charged at ninety pounds, and a let that runs past midnight is charged at that sum with a half again. A let cancelled inside a week is charged at half of the sum that would have been due. A let of the small room only is charged at a third of the sum due for the whole hall.

Part 4. Payment falls due within a month of the let. The treasurer issues one invoice for each let and does not carry a balance from one let to the next.""",
 old="""charged at ninety pounds""",
 new="""charged at sixty pounds""",
 cut="""Part 3. A standard evening let is charged at ninety pounds, and a let that runs past midnight is charged at that sum with a half again. A let cancelled inside a week is charged at half of the sum that would have been due. A let of the small room only is charged at a third of the sum due for the whole hall.""",
 site="Part 3, first sentence",
 note="Premises-site: Part 1 names the two rates the hall can price from and gives the hourly figure as sixty. Moving Part 3 to that figure moves the notice onto the other basis. Part 1 lies outside the passage, so the change reads as a bare sum without it."),

dict(id="t4-P02", arm="P", domain="policy",
 before="""Ardleigh Trust — Travel Grant Notice

Part 1. A household income for this notice is the income of the applicant and any partner before tax and before housing costs. Where housing costs are taken off first, the same households come out about four thousand pounds lower.

Part 2. Applications are made on the form issued by the trust and are considered at the meeting following receipt, whoever makes them.

Part 3. A grant is paid where household income is below twenty-two thousand pounds in the year before the application. Where income is at or above that sum, no grant is paid and the applicant is told in writing. The sum is checked against the payslips sent in with the form.

Part 4. A grant is paid once in any twelve-month period. The trust keeps the forms for six years and then destroys them.""",
 old="""below twenty-two thousand pounds""",
 new="""below eighteen thousand pounds""",
 cut="""Part 3. A grant is paid where household income is below twenty-two thousand pounds in the year before the application. Where income is at or above that sum, no grant is paid and the applicant is told in writing. The sum is checked against the payslips sent in with the form.""",
 site="Part 3, first sentence",
 note="Premises-site: Part 1 defines what income means here and states the four thousand pound gap between the two ways of counting it. Moving the line by that gap moves the notice onto the other definition. Part 1 lies outside the passage."),

dict(id="t4-P03", arm="P", domain="policy",
 before="""Marrick District — Skip Placement Notice

Part 1. The distances in Part 3 follow the county standard of 2019, which measures from the kerb line. The standard of 2011 measured from the building line and gave distances two metres shorter throughout.

Part 2. A skip is placed on the public highway only under a permit, and the permit names the street and the dates.

Part 3. A skip stands no closer than six metres to a junction and no closer than four metres to a crossing. Where neither distance can be kept, the skip goes on private ground instead. The distances are measured along the kerb and not across it.

Part 4. Lamps are fitted at both ends of a skip between dusk and dawn. The permit holder is the one who fits them.""",
 old="""no closer than six metres to a junction and no closer than four metres to a crossing""",
 new="""no closer than four metres to a junction and no closer than two metres to a crossing""",
 cut="""Part 3. A skip stands no closer than six metres to a junction and no closer than four metres to a crossing. Where neither distance can be kept, the skip goes on private ground instead. The distances are measured along the kerb and not across it.""",
 site="Part 3, first sentence",
 note="Premises-site: Part 1 names the two county standards and the two-metre gap between them. Shortening both distances by that gap moves the notice onto the earlier standard. Part 1 lies outside the passage."),

dict(id="t4-P04", arm="P", domain="policy",
 before="""Thirlwood Angling Trust — Membership Notice

Part 1. The bands in Part 3 are the four bands of the national scheme. The trust ran its own scheme until last year, which had three bands and put the middle two of the national four together.

Part 2. Members join at the annual meeting or by post at any time, and a member joining by post is placed in a band by the secretary.

Part 3. Members are placed in Band A, Band B, Band C or Band D by the water they fish and the days they fish it. A member who fishes two waters is placed in the higher of the two bands. A member who fishes no water in a year keeps the band last held.

Part 4. Bands are reviewed each January. A member who changes water tells the secretary within a month of the change.""",
 old="""in Band A, Band B, Band C or Band D""",
 new="""in Band A, Band B or Band C""",
 cut="""Part 3. Members are placed in Band A, Band B, Band C or Band D by the water they fish and the days they fish it. A member who fishes two waters is placed in the higher of the two bands. A member who fishes no water in a year keeps the band last held.""",
 site="Part 3, first sentence",
 note="Model-site: Part 1 names the two schemes and says the trust's own had three bands where the national has four. Dropping to three bands moves the notice back onto the trust's scheme. Part 1 lies outside the passage."),

dict(id="t4-P05", arm="P", domain="policy",
 before="""Netherfield Depot — Claims Notice

Part 1. The counts of days in Part 3 are working days, with the depot shutdown week counted as working. Counting that week as closed moves each of them on by five days.

Part 2. A claim is made on the form at the goods counter, and the form is stamped by the counter clerk on the day it is handed in.

Part 3. A claim is made within twenty working days of the delivery, and a claim about a short delivery is made within ten. A claim handed in later than that is not considered. The stamped date on the form is the date that counts.

Part 4. Claims are settled by credit against the next invoice. The counter keeps the stamped forms for two years.""",
 old="""within twenty working days of the delivery, and a claim about a short delivery is made within ten""",
 new="""within twenty-five working days of the delivery, and a claim about a short delivery is made within fifteen""",
 cut="""Part 3. A claim is made within twenty working days of the delivery, and a claim about a short delivery is made within ten. A claim handed in later than that is not considered. The stamped date on the form is the date that counts.""",
 site="Part 3, first sentence",
 note="Premises-site: Part 1 states how days are counted and the five-day gap between the two ways of counting them. Moving both counts by that gap moves the notice onto the other way. Part 1 lies outside the passage."),
]

# =============================================================== ARM P — report
ITEMS += [
dict(id="t4-P06", arm="P", domain="report",
 before="""Cawthorne Mail Order — Quarterly Dispatch Note

Section 1. The counts in Section 3 are gross of returns, which is how the warehouse system reports them. Net of returns they run about a fifth lower across every line.

Section 2. The quarter ran from the first Monday in April to the last Friday in June, with the bank holidays counted as working days.

Section 3. The warehouse dispatched 1,240 parcels in the quarter, of which 310 went to addresses outside the county. The busiest week took 148 parcels. Parcels going outside the county go by the overnight service where the address allows it.

Section 4. Two of the thirteen weeks were shortened by the van contract change. The contractor was the same in both halves of the quarter.""",
 old="""dispatched 1,240 parcels in the quarter, of which 310 went to addresses outside the county. The busiest week took 148 parcels""",
 new="""dispatched 992 parcels in the quarter, of which 248 went to addresses outside the county. The busiest week took 118 parcels""",
 cut="""Section 3. The warehouse dispatched 1,240 parcels in the quarter, of which 310 went to addresses outside the county. The busiest week took 148 parcels. Parcels going outside the county go by the overnight service where the address allows it.""",
 site="Section 3, both sentences",
 note="Premises-site: Section 1 says the counts are gross of returns and puts the net figures a fifth lower. Dropping every figure by a fifth moves the note onto the net basis. Section 1 lies outside the passage."),

dict(id="t4-P07", arm="P", domain="report",
 before="""Hartsmere Leisure — Attendance Note

Section 1. A visit in Section 3 is one person coming through the door, which is what the turnstile counts. Counting a visit as a booked slot instead gives roughly half the number, since most slots are booked in pairs.

Section 2. The turnstile was in service throughout the month and was compared against the door count on two evenings.

Section 3. The centre took 3,420 visits in the month, of which 1,180 were on the two weekend days. The quietest weekday took 74 visits. The weekend days are the busiest at the pool as well as at the hall, and the pattern held in every week.

Section 4. The pool was closed for two days in the middle of the month. No allowance for that has been made in any figure above.""",
 old="""took 3,420 visits in the month, of which 1,180 were on the two weekend days. The quietest weekday took 74 visits""",
 new="""took 1,710 visits in the month, of which 590 were on the two weekend days. The quietest weekday took 37 visits""",
 cut="""Section 3. The centre took 3,420 visits in the month, of which 1,180 were on the two weekend days. The quietest weekday took 74 visits. The weekend days are the busiest at the pool as well as at the hall, and the pattern held in every week.""",
 site="Section 3, both sentences",
 note="Premises-site: Section 1 defines a visit and says the other definition halves the count. Halving every figure moves the note onto that definition. Section 1 lies outside the passage."),

dict(id="t4-P08", arm="P", domain="report",
 before="""Ravensdale Practice — Waiting Time Note

Section 1. The figures in Section 3 are means, taken over every patient seen in the month. The medians run about three minutes lower in every month of the year.

Section 2. Waiting is counted from the appointment time, not from arrival, so a patient who arrives early is not counted as waiting longer.

Section 3. The wait in January was 14 minutes and the wait in February was 12 minutes. March came in at 15 minutes, the highest of the three. The wait was measured to the nearest minute in all three months.

Section 4. The same two consulting rooms were in use in all three months. One clinician was absent for a fortnight in February.""",
 old="""in January was 14 minutes and the wait in February was 12 minutes. March came in at 15 minutes""",
 new="""in January was 11 minutes and the wait in February was 9 minutes. March came in at 12 minutes""",
 cut="""Section 3. The wait in January was 14 minutes and the wait in February was 12 minutes. March came in at 15 minutes, the highest of the three. The wait was measured to the nearest minute in all three months.""",
 site="Section 3, both sentences",
 note="Premises-site: Section 1 says the figures are means and puts the medians three minutes lower. Dropping all three by three moves the note onto the median. Section 1 lies outside the passage."),

dict(id="t4-P09", arm="P", domain="report",
 before="""Bardsey School — Roll Note

Section 1. The totals in Section 3 take in the annexe, which the authority counts as part of the school. Leaving the annexe out takes about forty off each total.

Section 2. The roll was taken on the first Thursday of each term, which is the day the authority names for the return.

Section 3. The autumn roll was 612 and the spring roll was 604. The summer roll was 598, the lowest of the three terms. The autumn figure is the one the authority uses for funding and the one sent on the return.

Section 4. Two classes moved between buildings during the spring term. The move did not change the number on the roll.""",
 old="""roll was 612 and the spring roll was 604. The summer roll was 598""",
 new="""roll was 572 and the spring roll was 564. The summer roll was 558""",
 cut="""Section 3. The autumn roll was 612 and the spring roll was 604. The summer roll was 598, the lowest of the three terms. The autumn figure is the one the authority uses for funding and the one sent on the return.""",
 site="Section 3, both sentences",
 note="Premises-site: Section 1 says the totals take in the annexe and puts the annexe at about forty. Dropping every total by forty moves the note onto the roll without it. Section 1 lies outside the passage."),

dict(id="t4-P10", arm="P", domain="report",
 before="""Tarnside Water — Sample Note

Section 1. The dates in Section 3 are the dates each sample was drawn at the intake. The dates the samples reached the laboratory run two days later in every case.

Section 2. Samples are drawn by the district technician on a Monday and carried by the Wednesday van, which is why the two sets of dates differ.

Section 3. The first sample is dated 4 June, the second 11 June and the third 18 June. All three were drawn at the same point on the intake screen. Each sample was drawn into a one-litre bottle and sealed at the intake.

Section 4. The laboratory reported on all three together at the end of the month. No sample was held over.""",
 old="""dated 4 June, the second 11 June and the third 18 June""",
 new="""dated 6 June, the second 13 June and the third 20 June""",
 cut="""Section 3. The first sample is dated 4 June, the second 11 June and the third 18 June. All three were drawn at the same point on the intake screen. Each sample was drawn into a one-litre bottle and sealed at the intake.""",
 site="Section 3, first sentence",
 note="Premises-site: Section 1 says which of the two dates the note carries and puts the other two days later. Moving all three on by two days moves the note onto the laboratory date. Section 1 lies outside the passage."),
]

# =============================================================== ARM P — config
ITEMS += [
dict(id="t4-P11", arm="P", domain="config",
 before="""# Harbury edge - transport settings
# The timeouts below are three times the upstream p99, which is 400 ms on this
# link. Under the degraded-mode p99 of 900 ms the same working gives 2700.
[socket]
bind = 0.0.0.0
port = 9440
backlog = 256
[timeouts]
# Each setting here is a wait in milliseconds and applies to every peer alike.
request_ms = 1200
connect_ms = 600
read_ms = 1200
write_ms = 1200
idle_ms = 2400
[peers]
primary = harbury-a
secondary = harbury-b
probe_seconds = 10""",
 old="""request_ms = 1200
connect_ms = 600
read_ms = 1200
write_ms = 1200
idle_ms = 2400""",
 new="""request_ms = 2700
connect_ms = 1350
read_ms = 2700
write_ms = 2700
idle_ms = 5400""",
 cut="""[timeouts]
# Each setting here is a wait in milliseconds and applies to every peer alike.
request_ms = 1200
connect_ms = 600
read_ms = 1200
write_ms = 1200
idle_ms = 2400""",
 site="the [timeouts] section, all five settings",
 note="Premises-site: the header names the upstream p99 the timeouts are worked out from and gives the figure the other one yields. Moving every setting onto that figure moves the file onto the degraded-mode p99. The header lies outside the passage."),

dict(id="t4-P12", arm="P", domain="config",
 before="""# Sedgewick render - worker settings
# The counts below are set for the eight-core boxes the pool runs on today.
# On the thirty-two-core boxes the same working gives four times each count.
[server]
listen = 0.0.0.0
port = 8300
[workers]
# The three settings under the count follow it and are never set on their own.
count = 8
queue_depth = 32
prefetch = 16
max_inflight = 64
[paths]
scratch = /var/tmp/sedgewick
output = /srv/sedgewick/out""",
 old="""count = 8
queue_depth = 32
prefetch = 16
max_inflight = 64""",
 new="""count = 32
queue_depth = 128
prefetch = 64
max_inflight = 256""",
 cut="""[workers]
# The three settings under the count follow it and are never set on their own.
count = 8
queue_depth = 32
prefetch = 16
max_inflight = 64""",
 site="the [workers] section, all four settings",
 note="Premises-site: the header names the machine the counts are set for and states the multiplier for the other machine. Multiplying every count by four moves the file onto that machine. The header lies outside the passage."),

dict(id="t4-P13", arm="P", domain="config",
 before="""# Whitmoor archive - retention settings
# The keeps below follow the standard schedule, which is the one the office
# adopted. The extended schedule keeps everything four times as long.
[source]
root = /srv/whitmoor/incoming
pattern = *.tar.gz
[retention]
# Each keep is counted in days from the day the file lands in the archive.
keep_days = 90
keep_index_days = 180
keep_manifest_days = 360
prune_batch = 500
[notify]
mailbox = archive@whitmoor.example
on_failure = true""",
 old="""keep_days = 90
keep_index_days = 180
keep_manifest_days = 360""",
 new="""keep_days = 360
keep_index_days = 720
keep_manifest_days = 1440""",
 cut="""[retention]
# Each keep is counted in days from the day the file lands in the archive.
keep_days = 90
keep_index_days = 180
keep_manifest_days = 360
prune_batch = 500""",
 site="the [retention] section, the three keep settings",
 note="Model-site: the header names the two schedules and the factor between them. Multiplying every keep by four moves the file onto the extended schedule. The header lies outside the passage."),

dict(id="t4-P14", arm="P", domain="config",
 before="""# Glenmark feed - reader settings
# The hosts below are the primary site, which is the site the reader runs at.
# The failover site carries the same three in the same order under gm-b names.
reader:
  poll_seconds: 15
  window_size: 200
source:
  # The reader tries the hosts in the order they are written here.
  hosts:
    - gm-a-01
    - gm-a-02
    - gm-a-03
  port: 7440
store:
  path: /var/lib/glenmark
  keep_days: 30""",
 old="""    - gm-a-01
    - gm-a-02
    - gm-a-03""",
 new="""    - gm-b-01
    - gm-b-02
    - gm-b-03""",
 cut="""source:
  # The reader tries the hosts in the order they are written here.
  hosts:
    - gm-a-01
    - gm-a-02
    - gm-a-03
  port: 7440""",
 site="the source block, the three host entries",
 note="Premises-site: the header names which site the host list belongs to and states that the other site carries the same three under different names. Swapping the names moves the file onto the failover site. The header lies outside the passage."),

dict(id="t4-P15", arm="P", domain="config",
 before="""# Barrowfield glasshouse - vent settings
# The thresholds below are the summer profile, which is the one loaded now.
# The winter profile is the same shape with every threshold a fifth higher.
[sensors]
inside = t-in-01
outside = t-out-01
[thresholds]
# Each threshold is a temperature taken at the inside sensor named above.
vent_open_c = 20
vent_shut_c = 15
alarm_high_c = 30
alarm_low_c = 5
[fans]
speed_percent = 60
run_minutes = 15""",
 old="""vent_open_c = 20
vent_shut_c = 15
alarm_high_c = 30
alarm_low_c = 5""",
 new="""vent_open_c = 24
vent_shut_c = 18
alarm_high_c = 36
alarm_low_c = 6""",
 cut="""[thresholds]
# Each threshold is a temperature taken at the inside sensor named above.
vent_open_c = 20
vent_shut_c = 15
alarm_high_c = 30
alarm_low_c = 5""",
 site="the [thresholds] section, all four settings",
 note="Premises-site: the header names which profile is loaded and states the factor between the two. Raising every threshold by that factor moves the file onto the winter profile. The header lies outside the passage."),
]

# ================================================================= ARM P — code
ITEMS += [
dict(id="t4-P16", arm="P", domain="code",
 before='''"""Batch sizing for the Cawley feed.

Every size below is worked out for rows of at most 2 KiB, which is the shape
the feed has had since the schema change. Before that change rows ran to 8 KiB
and the same working gave a quarter of these numbers.
"""

_MAX_ROWS = 2000
_MAX_BYTES = 4194304
_FLUSH_ROWS = 500


def chunk(rows):
    out, cur = [], []
    for r in rows:
        if len(cur) >= _MAX_ROWS:
            out.append(cur)
            cur = []
        cur.append(r)
    if cur:
        out.append(cur)
    return out

def flush_due(pending):
    return len(pending) >= _FLUSH_ROWS''',
 old='''_MAX_ROWS = 2000
_MAX_BYTES = 4194304
_FLUSH_ROWS = 500''',
 new='''_MAX_ROWS = 500
_MAX_BYTES = 1048576
_FLUSH_ROWS = 125''',
 cut='''_MAX_ROWS = 2000
_MAX_BYTES = 4194304
_FLUSH_ROWS = 500


def chunk(rows):
    out, cur = [], []
    for r in rows:
        if len(cur) >= _MAX_ROWS:
            out.append(cur)
            cur = []
        cur.append(r)''',
 site="the three module constants and the loop below them",
 note="Premises-site: the docstring names the row size the numbers are worked out for and states that the other row size gives a quarter of them. Quartering all three moves the file onto the pre-change feed. The docstring lies outside the passage."),

dict(id="t4-P17", arm="P", domain="code",
 before='''"""Rate helpers for the Denby meter.

The meter in service emits once an hour, so every rate below is per hour to
match it. The older meter emitted once a minute, where the same rates come out
at one sixtieth of these.
"""

_SECONDS = 3600
_WARN_RATE = 120
_TRIP_RATE = 360


def rate(count, seconds):
    # The count is divided by the seconds constant here and by nothing else.
    return count * _SECONDS / seconds

def warn(count, seconds):
    return rate(count, seconds) >= _WARN_RATE

def trip(count, seconds):
    return rate(count, seconds) >= _TRIP_RATE''',
 old='''_SECONDS = 3600
_WARN_RATE = 120
_TRIP_RATE = 360''',
 new='''_SECONDS = 60
_WARN_RATE = 2
_TRIP_RATE = 6''',
 cut='''_SECONDS = 3600
_WARN_RATE = 120
_TRIP_RATE = 360


def rate(count, seconds):
    # The count is divided by the seconds constant here and by nothing else.
    return count * _SECONDS / seconds''',
 site="the three module constants and the helper below them",
 note="Premises-site: the docstring names which meter the rates match and states the sixtieth between the two. Dividing all three by sixty moves the file onto the older meter. The docstring lies outside the passage."),

dict(id="t4-P18", arm="P", domain="code",
 before='''"""Window test for the Fenwick sampler.

The sampler in service emits readings at the limits as well as between them,
so the window takes both limits in. The older sampler emitted only between the
limits, and the window left both of them out.
"""


def in_window(reading, floor, ceiling):
    # A reading that sits on one of the limits is decided by the next line alone.
    return floor <= reading <= ceiling

def count_in(readings, floor, ceiling):
    return sum(1 for r in readings if in_window(r, floor, ceiling))

def first_in(readings, floor, ceiling):
    for r in readings:
        if in_window(r, floor, ceiling):
            return r
    return None''',
 old='''    return floor <= reading <= ceiling''',
 new='''    return floor < reading < ceiling''',
 cut='''def in_window(reading, floor, ceiling):
    # A reading that sits on one of the limits is decided by the next line alone.
    return floor <= reading <= ceiling

def count_in(readings, floor, ceiling):
    return sum(1 for r in readings if in_window(r, floor, ceiling))''',
 site="the body of in_window and the helper below it",
 note="Model-site: the docstring names which sampler the test is written for and states what the other one needs. Leaving both limits out moves the file onto the older sampler. The docstring lies outside the passage."),

dict(id="t4-P19", arm="P", domain="code",
 before='''"""Fee bands for the Ashfold counter.

The bands below follow the tariff of 2019, which is the one in force at the
counter. The tariff of 2015 had the same shape with every band five pounds
lower than the one beside it here.
"""

_BANDS = [(0, 12), (100, 24), (500, 48)]


def fee(amount):
    out = _BANDS[0][1]
    for floor, band in _BANDS:
        if amount >= floor:
            out = band
    return out

def bands():
    return list(_BANDS)''',
 old='''_BANDS = [(0, 12), (100, 24), (500, 48)]''',
 new='''_BANDS = [(0, 7), (100, 19), (500, 43)]''',
 cut='''_BANDS = [(0, 12), (100, 24), (500, 48)]


def fee(amount):
    out = _BANDS[0][1]
    for floor, band in _BANDS:
        if amount >= floor:
            out = band
    return out''',
 site="the band table and the function below it",
 note="Premises-site: the docstring names which tariff the table follows and states the five pound gap to the other one. Taking five off every band moves the file onto the earlier tariff. The docstring lies outside the passage."),

dict(id="t4-P20", arm="P", domain="code",
 before='''"""Opening hours for the Netherton depot.

Every hour below is on the depot clock, which runs on local time all year. The
gate system runs on the other clock, where the same hours come out one earlier
between the last Sunday in March and the last Sunday in October.
"""

OPEN_HOUR = 7
CLOSE_HOUR = 19
LAST_LOAD_HOUR = 18


def is_open(hour):
    # The two hours below are read here and in the helper under this one.
    return OPEN_HOUR <= hour < CLOSE_HOUR

def accepts_load(hour):
    return is_open(hour) and hour < LAST_LOAD_HOUR''',
 old='''OPEN_HOUR = 7
CLOSE_HOUR = 19
LAST_LOAD_HOUR = 18''',
 new='''OPEN_HOUR = 6
CLOSE_HOUR = 18
LAST_LOAD_HOUR = 17''',
 cut='''OPEN_HOUR = 7
CLOSE_HOUR = 19
LAST_LOAD_HOUR = 18


def is_open(hour):
    # The two hours below are read here and in the helper under this one.
    return OPEN_HOUR <= hour < CLOSE_HOUR''',
 site="the three module constants and the helper below them",
 note="Premises-site: the docstring names which clock the hours are on and states the hour between the two. Taking an hour off all three moves the file onto the gate clock. The docstring lies outside the passage."),
]

# ============================================================== ARM P — process
ITEMS += [
dict(id="t4-P21", arm="P", domain="process",
 before="""Cranleigh Works — Line Purge Round

The times below are counted from the moment the pump starts. Counted from the moment the valve opens instead, each of them is two minutes shorter.

1. Check that the drain tray is empty and in place under the line.
2. Start the pump and open the valve at the head of the line.
3. Run the purge for twelve minutes and watch the sight glass throughout.
4. Close the valve and let the pump run on for four minutes.
5. Stop the pump and drain the tray into the waste drum standing by the bench.
6. Wipe the sight glass and log the purge in the book by the door.
7. Return the drum to the store and sign the tag on the store rail.""",
 old="""Run the purge for twelve minutes and watch the sight glass throughout.
4. Close the valve and let the pump run on for four minutes.""",
 new="""Run the purge for ten minutes and watch the sight glass throughout.
4. Close the valve and let the pump run on for two minutes.""",
 cut="""3. Run the purge for twelve minutes and watch the sight glass throughout.
4. Close the valve and let the pump run on for four minutes.
5. Stop the pump and drain the tray into the waste drum standing by the bench.""",
 site="steps 3 to 5",
 note="Premises-site: the line above step 1 states which moment the times are counted from and the two minutes between the two ways of counting. Taking two minutes off both moves the round onto the other one. That line lies outside the passage."),

dict(id="t4-P22", arm="P", domain="process",
 before="""Loxley Gauge Room — Block Check Round

The tolerances below are the ones the vendor publishes. The house tolerances are half as wide, and they are the ones the auditor works to.

1. Take the block set from the cabinet and let it stand for an hour.
2. Wipe each block with the lint-free cloth before it is measured.
3. Measure the hundred-millimetre block and accept it within four tenths of a micron.
4. Measure the fifty-millimetre block and accept it within two tenths of a micron.
5. Note both readings on the card and initial the card at the foot.
6. Return the set to the cabinet and close the cabinet door.
7. Hand the card to the gauge room supervisor before leaving.""",
 old="""and accept it within four tenths of a micron.
4. Measure the fifty-millimetre block and accept it within two tenths of a micron.""",
 new="""and accept it within two tenths of a micron.
4. Measure the fifty-millimetre block and accept it within one tenth of a micron.""",
 cut="""3. Measure the hundred-millimetre block and accept it within four tenths of a micron.
4. Measure the fifty-millimetre block and accept it within two tenths of a micron.
5. Note both readings on the card and initial the card at the foot.""",
 site="steps 3 to 5",
 note="Premises-site: the line above step 1 names whose tolerances the round carries and states that the other set is half as wide. Halving both moves the round onto the house set. That line lies outside the passage."),

dict(id="t4-P23", arm="P", domain="process",
 before="""Marchford Dairy — Starter Batch Round

The quantities below are for the twenty-litre batch, which is the one made on weekdays. The forty-litre weekend batch doubles every one of them.

1. Sterilise the vat and the paddle and stand both on the drainer.
2. Draw the milk into the vat and bring it to the set temperature.
3. Add three scoops of starter and stir for two minutes by the clock.
4. Add one scoop of the second culture and stir for a further minute.
5. Cover the vat and leave it for the ripening time given on the card.
6. Draw a sample from the vat and check it against the card.
7. Log the batch number and the time in the book by the door.""",
 old="""Add three scoops of starter and stir for two minutes by the clock.
4. Add one scoop of the second culture and stir for a further minute.""",
 new="""Add six scoops of starter and stir for two minutes by the clock.
4. Add two scoops of the second culture and stir for a further minute.""",
 cut="""3. Add three scoops of starter and stir for two minutes by the clock.
4. Add one scoop of the second culture and stir for a further minute.
5. Cover the vat and leave it for the ripening time given on the card.""",
 site="steps 3 to 5",
 note="Premises-site: the line above step 1 names which batch the quantities are for and states that the other batch doubles them. Doubling both moves the round onto the weekend batch. That line lies outside the passage."),

dict(id="t4-P24", arm="P", domain="process",
 before="""Ryhall Kiln — Firing Watch Round

The readings below are in degrees Celsius, which is what the new gauges show. The older gauges on the second kiln show Fahrenheit, where the same three points come out at one hundred and forty, three hundred and two, and five hundred.

1. Open the book at the page for the day and enter the start time.
2. Read the front gauge every half hour and enter the figure in the book.
3. Where the front gauge passes sixty degrees, open the damper one notch.
4. Where it passes one hundred and fifty degrees, shut the vent and log the time.
5. Where it passes two hundred and sixty degrees, call the kiln supervisor and stand clear of the kiln door until the supervisor arrives.
6. Enter the peak reading at the foot of the page at the end of the watch.
7. Close the book and hang it on the hook by the kiln door.""",
 old="""passes sixty degrees, open the damper one notch.
4. Where it passes one hundred and fifty degrees, shut the vent and log the time.
5. Where it passes two hundred and sixty degrees, call the kiln supervisor and stand clear of the kiln door until the supervisor arrives.""",
 new="""passes one hundred and forty degrees, open the damper one notch.
4. Where it passes three hundred and two degrees, shut the vent and log the time.
5. Where it passes five hundred degrees, call the kiln supervisor and stand clear of the kiln door until the supervisor arrives.""",
 cut="""3. Where the front gauge passes sixty degrees, open the damper one notch.
4. Where it passes one hundred and fifty degrees, shut the vent and log the time.
5. Where it passes two hundred and sixty degrees, call the kiln supervisor and stand clear of the kiln door until the supervisor arrives.""",
 site="steps 3 to 5",
 note="Premises-site: the line above step 1 names which scale the readings are on and gives the three matching points on the other scale. Moving all three onto those points moves the round onto the older gauges. That line lies outside the passage."),
]
