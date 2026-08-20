"""AN4 — the sec 6.2 tautology diagnostic. RUNS LAST (sec 12 step 11), after every band is
read, so it cannot influence them.

The banned threshold flags are run ONCE, as a labelled diagnostic, to measure how much of the
override is definitional. Pre-registered asymmetric consequence: at AUC >= 0.98, column 1's
INFERIOR verdict is downgraded to INFERIOR-BY-CONSTRUCTION and fires nothing; SUPERIOR and
PARITY stand and are strengthened.
"""
from __future__ import annotations
import collections, json, sys
import numpy as np
sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad/a0run/src")
import a0lib as A
import a0stat as S

FLAGS = ["entropy_passed", "coherence_passed", "optimization_veto_passed",
         "epistemic_humility_passed"]


def main():
    for m in ("AN1_cpfact.done", "AN2_col1.done", "AN3_cpkind.done"):
        if not A.has_marker(m):
            print("REFUSING: the tautology diagnostic runs LAST; missing", m)
            return 2
    fr = A.rjson("A0_frames.json")
    live = A.load_rows(allow_outcome=True, allow=FLAGS)
    byid = {r["t"]["id"]: r for r in live}
    ids = fr["frames"]["FRAME-H"]
    o = np.array([int(bool(byid[i]["t"].get(A.OUTCOME))) for i in ids])
    F = {}
    for f in FLAGS:
        F[f] = [(byid[i]["t"].get("conscience_result") or {}).get(f) for i in ids]
    const = {f: len({str(x) for x in v}) == 1 for f, v in F.items()}
    present = {f: sum(1 for x in v if x is not None) for f, v in F.items()}

    # joint score: number of flags failed (None counts as its own level)
    joint = ["|".join("T" if F[f][j] is True else "F" if F[f][j] is False else "-"
                      for f in FLAGS) for j in range(len(ids))]
    lv = sorted(set(joint))
    rate = {l: float(np.mean(o[[j for j in range(len(ids)) if joint[j] == l]]))
            for l in lv}
    score = [rate[joint[j]] for j in range(len(ids))]
    auc, tie = S.auc_tie_corrected(score, o)
    mi = S.mi_plugin(joint, o.tolist())

    per = {}
    for f in FLAGS:
        v = [1 if x is False else 0 if x is True else -1 for x in F[f]]
        if len(set(v)) > 1:
            a, t = S.auc_tie_corrected(v, o)
            per[f] = {"AUC": a, "tie_fraction": t, "MI_nats": S.mi_plugin(
                [str(x) for x in v], o.tolist()), "constant": const[f],
                "present": present[f]}
        else:
            per[f] = {"constant": True, "present": present[f], "AUC": None}

    res = {"frame": "FRAME-H", "N": len(ids),
           "joint_flag_AUC": auc, "tie_fraction": tie, "joint_MI_nats": mi,
           "joint_levels": dict(collections.Counter(joint)),
           "override_rate_by_level": rate,
           "per_flag": per,
           "pipeline_disclosure": "on FRAME-H entropy_passed is constant True by "
                                  "construction, so the diagnostic reduces to three flags "
                                  "of which two are themselves presence-conditioned "
                                  "(sec 3.10 / sec 6.2)",
           "AUC_ge_0.98": bool(auc >= 0.98),
           "consequence": ("column 1's INFERIOR verdict is downgraded to "
                           "INFERIOR-BY-CONSTRUCTION and fires nothing; SUPERIOR and PARITY "
                           "stand and are strengthened" if auc >= 0.98 else
                           "below 0.98: reported as context, changes nothing")}
    A.wjson("A0_tautology.json", res)
    print(json.dumps(res, indent=1, default=str))
    A.marker("AN4_taut.done", {"AUC": auc})
    return 0


if __name__ == "__main__":
    sys.exit(main())
