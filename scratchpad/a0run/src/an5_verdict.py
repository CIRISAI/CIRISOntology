"""AN5 — the sec 10.3 conjunction, assembled mechanically.

Written BEFORE AN1/AN2/AN3 produce their bands, so the mapping from bands to verdicts is
fixed in code before the bands exist. Column 2's cell is read from CP-FACT (sec 1.3);
CP-KIND enters only as the mechanism reading and never as the kill trigger.
"""
from __future__ import annotations
import json, sys
sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad/a0run/src")
import a0lib as A

ROW = {
 1: ("first test PASSED. The wager stands, still a wager, with one confirmed prediction on "
     "real production data. Status does NOT move to measured on one corpus.",
     "gate passed; A1 proceeds"),
 2: ("KILL FIRES. 'the identity is decorative and dies.' Marked dead in Stance.lean with "
     "killedBy naming the prereg, kept in the record, marked dead.",
     "gate passed; A1 proceeds"),
 3: ("kill does NOT fire (its antecedent requires kind-readings to succeed). MIXED: the "
     "share supports the identity while its corollary is in tension with column 1.",
     "A0 kill fires; re-orientation wounded on the 3->1 DMA collapse only"),
 4: ("kill does NOT fire — the corpus is declared UNINFORMATIVE for the identity, because a "
     "share failure cannot be attributed when the instrument feeding column 1 "
     "under-performs.",
     "A0 kill fires; re-orientation wounded on the 3->1 DMA collapse only"),
 5: ("first test PASSED ON THE INSTRUMENT-FREE READING ONLY. The kind-shaped mechanism is "
     "UNGAUGED.",
     "NO VERDICT — the gate is ungauged, and an ungauged gate is not a passed gate"),
 6: ("kill does NOT fire: the conjunction's antecedent ('kind-readings succeed') is not "
     "merely false but UNMEASURED, and a conjunction with an unmeasured antecedent has no "
     "truth value. Reported as UNGAUGED-AND-NEGATIVE, and the failed share is reported as "
     "loudly as a detection.",
     "no verdict"),
 7: ("no kill in either column. The achieved half-width, the required I_L, and the next-size "
     "sample are named.", "no verdict"),
 8: ("no kill. The realised margins, the realised N_eff, the MDE and the maximum achievable "
     "share are all printed.", "per column 1"),
 9: ("no kill. The LP certificate's collapsed interval is printed.", "per column 1"),
 10: ("ungauged, reported as loudly as a detection", "per column 1"),
 11: ("as the matching INFERIOR row, except that the applied-branch column reads 'no verdict' "
      "and no A0 kill fires", "NO VERDICT"),
}


def classify(col1, col2):
    c1 = col1.upper(); c2 = col2.upper()
    if "INFERIOR-BY-CONSTRUCTION" in c1:
        return 11
    if "FOULED" in c2:
        return 9
    if c2.startswith("VOID"):
        return 10
    if "UNDERPOWERED" in c2:
        return 8
    if "UNDERPOWERED" in c1:
        return 7
    if c1.startswith("VOID") or c1.startswith("UNGAUGED"):
        return 5 if c2.startswith("CONCENTRATES") else 6
    if c1.startswith("INFERIOR"):
        return 3 if c2.startswith("CONCENTRATES") else 4
    if c1.startswith("SUPERIOR") or c1.startswith("PARITY"):
        return 1 if c2.startswith("CONCENTRATES") else 2
    return 7          # INCONCLUSIVE routes to the no-kill row


def main():
    cf = A.rjson("A0_cpfact.json")
    c1j = A.rjson("A0_col1.json")
    ck = A.rjson("A0_cpkind.json")
    panel = A.rjson("A0_panel.json")
    taut = A.rjson("A0_tautology.json")

    col2 = cf["BAND"]
    col1 = c1j["BAND"]
    # sec 10.1 wires V4 into column 1: the mandatory NO FIT / NO MAJORITY exclusion is
    # "gated by V4". A fired V4 therefore voids column 1 as well as CP-KIND.
    v4 = panel["gates"]["FRAME-H"]
    v4_tl = panel["gates"]["FRAME-TL"]
    if not v4["V4_PASS"]:
        col1_effective = "VOID (V4 — panel decisiveness)"
    else:
        col1_effective = col1
    if taut["AUC_ge_0.98"] and col1_effective.startswith("INFERIOR"):
        col1_effective = "INFERIOR-BY-CONSTRUCTION"

    row = classify(col1_effective, col2)
    out = {
        "column1_band_as_computed": col1,
        "column1_band_effective": col1_effective,
        "column1_V4_wiring": {
            "V4_FRAME_H": v4, "V4_FRAME_TL": v4_tl,
            "rule": "sec 10.1: 'NO FIT and NO MAJORITY rows are excluded from BOTH arms "
                    "identically; the exclusion count is reported and gated by V4.' A fired "
                    "V4 makes that mandatory exclusion inadmissible, so column 1 is VOID.",
            "disclosed_tension": "sec 10.3's column-1 VOID row enumerates '(any of V1, V2, "
                                 "V6, V7, V7b)' and does not list V4, while sec 10.1 wires "
                                 "V4 into column 1 through the exclusion gate and sec 9 "
                                 "states V4's consequence as a bare VOID. Both readings are "
                                 "reported; under EITHER of them the stance kill does not "
                                 "fire, because column 1's own band is read from the same "
                                 "panel that failed V4."},
        "column2_band_CP_FACT": col2,
        "mechanism_CP_KIND": ck["BAND_primary"],
        "row_10_3": row,
        "verdict_the_ledgers_third_name": ROW[row][0],
        "verdict_applied_branch": ROW[row][1],
        "two_faculty_scope": (
            "COLUMN 1 SCOPE, printed in the same sentence as the verdict per steward "
            "decision 3 (frozen at its default in sec 18): A0's legacy arm reaches TWO of "
            "the four consciences — entropy and coherence, the only pair simultaneously "
            "scorable anywhere in this corpus — on FRAME-H, which is itself exactly the "
            "frame where the entropy faculty did not fire. The 4->1 conscience collapse is "
            "UNTESTED HERE and is outside column 1's blast radius; the blast radius is the "
            "A8 re-orientation and the 3->1 DMA collapse arithmetic only."),
        "second_kill_untouched": (
            "The identity's second, independent kill — 'it dies on any substrate where the "
            "share and a frame-supplied Record reading are both measurable and decorrelate' "
            "— is NOT tested by A0 and is untouched by every outcome above."),
    }
    A.wjson("A0_verdict.json", out)
    print(json.dumps(out, indent=1, default=str))
    A.marker("AN5_verdict.done", {"row": row, "col1": col1_effective, "col2": col2})
    return 0


if __name__ == "__main__":
    sys.exit(main())
