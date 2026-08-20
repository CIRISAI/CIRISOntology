# score_d2_2_ds.md — deepseek-ai/DeepSeek-V3.1

STEP 1 — Derived site list verbatim:
S1: State-recognition content site (about world state)
S2: Transition-recognition content site (about transition)
S3: Constitution content site (about status)
S4: State-recognition gap site (information may be wrong)
S5: Transition-recognition gap site (transition may not be real)
S6: Encoding carrier site
S7: Presentation carrier site
S8: Instance token carrier site

STEP 2 — Routing for each example change:
E1: S1 (change in stated measurement relates to world state information)
E2: S4 (adding "tentatively" indicates uncertainty about information correctness)
E3: S4 (formula change introduces potential for wrong information from sensor reading)
E4: S4 (change in standing assumption affects information reliability about world state)
E5: S2 (change from "may" to "must" alters the transition requirement)
E6: S2 (change in goal ranking alters transition priorities/requirements)
E7: S2 (swapping procedure steps changes transition sequence)
E8: S3 (change in component status from draft to ratified is a constitutional change)
E9: S6 (CSV to JSON is an encoding change)
E10: S7 (passive to active voice is a presentation change)
E11: S8 (moving file to different directory is an instance token change)

STEP 3 — Extras and summary:
Extras: None (all sites used)
MATCHED=11 EXTRAS=0