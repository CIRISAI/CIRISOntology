# score_d2_2_qw.md — Qwen/Qwen3-235B-A22B-Instruct-2507

**STEP 1 — Extracted Site List (VERBATIM):**

S1. "State-recognition content site (about world state)"  
S2. "Transition-recognition content site (about transition)"  
S3. "Constitution content site (about status)"  
S4. "State-recognition gap site (information may be wrong)"  
S5. "Transition-recognition gap site (transition may not be real)"  
S6. "Encoding carrier site"  
S7. "Presentation carrier site"  
S8. "Instance token carrier site"

---

**STEP 2 — Routing Each Example Change:**

E1 a report's stated measurement is changed from 4.2 to 4.9  
→ **S1** (This is a change in the reported world state; fits state-recognition content)

E2 "we conclude" becomes "we tentatively conclude"; the measurement is unchanged  
→ **S4** (Epistemic hedge added; reflects uncertainty in recognition — "information may be wrong" — gap in state-recognition)

E3 the formula converting the sensor reading into the reported value is changed; the reading is unchanged  
→ **S6** (Change in encoding of data — how raw input becomes output; encoding carrier site)

E4 the standing assumption the report rests on ("readings are taken at sea level") is changed  
→ **S4** (Undermines reliability of state-recognition; affects whether information is correct — gap site)

E5 "operators may restart the process" becomes "operators must restart the process"  
→ **S2** (Change in transition availability/requirement — directly about a transition being mandatory; transition-recognition content)

E6 a policy's ranking of its goals is changed so that safety outranks throughput  
→ **S5** (Shift in what constitutes a valid or required transition; affects transition legitimacy — transition-recognition gap: "transition may not be real" if not aligned with current norms)

E7 two steps of a documented procedure are swapped  
→ **S2** (Alters transition order — procedural change affecting transition logic — transition-recognition content)

E8 a document declares that a component previously called a draft now counts as ratified  
→ **S3** (Constitution: status is brought into being by recognition — "draft" to "ratified" is a constituted status change)

E9 the same table is moved from CSV to JSON; contents identical  
→ **S6** (Change in encoding format — encoding carrier site)

E10 a passage is rewritten from passive to active voice; content identical  
→ **S7** (Change in presentation style — presentation carrier site)

E11 the file recording the change is moved to a different directory; contents identical  
→ **S8** (Change in instance token location — the physical or logical token carrying the content; instance token carrier site)

---

**STEP 3 — Extras and Summary:**

Extras (sites not routed to by any example):  
- **S5** was used (E6)  
- All sites S1 through S8 were used.

Wait: let's verify usage:

- S1 → E1  
- S2 → E5, E7 → AMBIGUOUS(S2) for two examples? No — each example routes independently.

But the question is: which site would you route *each* example to — so multiple examples can map to same site.

We check which sites were **not** used by any example:

- S1: E1 → used  
- S2: E5, E7 → used  
- S3: E8 → used  
- S4: E2, E4 → used  
- S5: E6 → used  
- S6: E3, E9 → used  
- S7: E10 → used  
- S8: E11 → used  

All 8 sites are used.

Thus:

**MATCHED=11 EXTRAS=0**