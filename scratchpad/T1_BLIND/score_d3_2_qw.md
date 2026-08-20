# score_d3_2_qw.md — Qwen/Qwen3-235B-A22B-Instruct-2507

**STEP 1 — Extracted site list VERBATIM:**

S1. Referential content site (what referential is about: the context states)  
S2. Emotive content site (what emotive is about: the addresser's attitude)  
S3. Conative content site (what conative is about: the addressee's response)  
S4. Phatic content site (what phatic is about: the channel)  
S5. Metalingual content site (what metalingual is about: the code)  
S6. Poetic content site (what poetic is about: the message form)  
S7. Gap site for referential: accuracy of reference  
S8. Gap site for emotive: sincerity of expression  
S9. Gap site for conative: effectiveness on addressee  
S10. Gap site for phatic: channel availability  
S11. Gap site for metalingual: mutual understanding of code  
S12. Carrier site: encoding  
S13. Carrier site: presentation  
S14. Carrier site: instance token  

---

**STEP 2 — Routing each example change:**

E1 a report's stated measurement is changed from 4.2 to 4.9 → **S1**  
*(Change in factual content — referential content site)*

E2 "we conclude" becomes "we tentatively conclude"; the measurement is unchanged → **S2**  
*(Change in speaker attitude — emotive content site)*

E3 the formula converting the sensor reading into the reported value is changed; the reading is unchanged → **S5**  
*(Change in the code or interpretation rule — metalingual content site)*

E4 the standing assumption the report rests on ("readings are taken at sea level") is changed → **S7**  
*(Change in whether the reference matches facts — gap site for referential: accuracy of reference)*

E5 "operators may restart the process" becomes "operators must restart the process" → **S3**  
*(Change in intended addressee response — conative content site)*

E6 a policy's ranking of its goals is changed so that safety outranks throughput → **S2**  
*(Change in speaker's value stance — emotive content site)*

E7 two steps of a documented procedure are swapped → **S1**  
*(Change in the reported sequence of events — referential content site)*

E8 a document declares that a component previously called a draft now counts as ratified → **S14**  
*(Change in document status/token interpretation — carrier site: instance token)*

E9 the same table is moved from CSV to JSON; contents identical → **S12**  
*(Change in encoding format — carrier site: encoding)*

E10 a passage is rewritten from passive to active voice; content identical → **S13**  
*(Change in presentation style — carrier site: presentation)*

E11 the file recording the change is moved to a different directory; contents identical → **S14**  
*(Change in location of the instance — carrier site: instance token)*

---

**STEP 3 — Extras and summary:**

Extras (sites not routed to by any example):  
S6 (Poetic content site), S8 (Gap site for emotive), S9 (Gap site for conative), S10 (Gap site for phatic), S11 (Gap site for metalingual)

MATCHED=11 EXTRAS=5