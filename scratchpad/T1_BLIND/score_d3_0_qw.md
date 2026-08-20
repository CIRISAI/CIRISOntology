# score_d3_0_qw.md — Qwen/Qwen3-235B-A22B-Instruct-2507

**STEP 1 — Extracted Site List (VERBATIM):**

S1. State-recognition content site (what state-recognition is about: the state of the world)  
S2. Transition-recognition content site (what transition-recognition is about: the transition)  
S3. Constitution content site (what constitution is about: the status being made-so)  
S4. Gap site for state-recognition: accuracy of information about the state  
S5. Gap site for transition-recognition: correctness of assessment about the transition  
S6. Carrier site: encoding  
S7. Carrier site: presentation  
S8. Carrier site: instance token  

---

**STEP 2 — Routing the Eleven Example Changes:**

E1 a report's stated measurement is changed from 4.2 to 4.9  
→ **S1** (change in the reported state of the world; content of state-recognition)

E2 "we conclude" becomes "we tentatively conclude"; the measurement is unchanged  
→ **S7** (change in presentation style, hedging language; content identical, so carrier site)

E3 the formula converting the sensor reading into the reported value is changed; the reading is unchanged  
→ **S4** (this affects accuracy of information linking measurement to state; gap in state-recognition)

E4 the standing assumption the report rests on ("readings are taken at sea level") is changed  
→ **S4** (undermines or alters the basis for accurate state-recognition; affects gap via assumptions)

E5 "operators may restart the process" becomes "operators must restart the process"  
→ **S2** (shifts normative status of a transition; about what transition is required)

E6 a policy's ranking of its goals is changed so that safety outranks throughput  
→ **S5** (affects assessment of which transition is required; normative assessment)

E7 two steps of a documented procedure are swapped  
→ **S2** (alters the sequence of transitions; content of transition-recognition)

E8 a document declares that a component previously called a draft now counts as ratified  
→ **S3** (constitutes a status change via recognition; constitution makes it so)

E9 the same table is moved from CSV to JSON; contents identical  
→ **S6** (change in data encoding; carrier site)

E10 a passage is rewritten from passive to active voice; content identical  
→ **S7** (change in presentation; carrier site)

E11 the file recording the change is moved to a different directory; contents identical  
→ **S8** (change in instance token/location; carrier of the record)

---

**STEP 3 — Extras and Summary:**

Extras: **NONE**  
All 8 sites were used.

MATCHED=11 EXTRAS=0