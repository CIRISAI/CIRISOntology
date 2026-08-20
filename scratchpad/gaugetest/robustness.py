"""GAUGE TEST — robustness cuts, all POST-HOC and labelled as such in the results document.
Run after analyse_gauge.py; writes robustness.json. Computes nothing that changes the frozen
primary — these exist to say how fragile or firm the primary's 13-vs-12-vs-4 arithmetic is.
"""
from __future__ import annotations
import collections, json, math, pathlib, sys

ROOT = pathlib.Path("/home/emoore/CIRISOntology/scratchpad/gaugetest")
sys.path.insert(0, str(ROOT))
from analyse_gauge import load_arm, two_prop, mcnemar, entropy_bits   # noqa: E402

LABELS = ["Priorities", "Rules", "Manner", "Identity", "Confidence", "Facts",
          "Circumstances", "Process", "Model", "Structure", "Premises", "Record"]
REM = {"A": None, "B": "Circumstances", "C": "Structure"}

o = json.load(open(ROOT / "originals.json"))
pop, om, ov = o["untouched"], o["modal"], o["votes"]
arms = {a: load_arm(a) for a in "ABC"}

orig_vote = {}
for l in open("/home/emoore/CIRISOntology/scratchpad/plane_corpus/full_judgments.jsonl"):
    r = json.loads(l)
    if r.get("condition") == "BASE" and r.get("kind"):
        orig_vote[(r["id"], r["model"])] = r["kind"].strip()
arm_vote = {}
for a in "ABC":
    v = {}
    for l in open(ROOT / f"judgments_{a}.jsonl"):
        r = json.loads(l)
        if r.get("kind"):
            v[(r["id"], r["model"])] = r["kind"].strip()
    arm_vote[a] = v

out = {"note": "ALL POST-HOC. The frozen primary is in gauge_results.json and is unaffected."}


def modal_perturb(ids, a):
    return sum(1 for i in ids if arms[a]["modal"].get(i) != om[i])


def vote_perturb(ids, a):
    S = set(ids)
    ks = [k for k in orig_vote if k[0] in S and k in arm_vote[a]]
    return sum(1 for k in ks if arm_vote[a][k] != orig_vote[k]), len(ks)


# --- R1: tie-tolerant modal (a tie whose top set still contains the original label is not a move)
def topset(votes):
    if not votes:
        return set()
    c = collections.Counter(votes)
    m = max(c.values())
    return {k for k, v in c.items() if v == m}


r1 = {}
per1 = {}
for a in "ABC":
    per1[a] = {i: om[i] not in topset(arms[a]["votes"].get(i, [])) for i in pop}
    r1[a] = {"x": sum(per1[a].values()), "n": len(pop), "p": sum(per1[a].values()) / len(pop)}
for a in "BC":
    r1[f"{a}_vs_A"] = {"test": two_prop(r1[a]["x"], len(pop), r1["A"]["x"], len(pop)),
                       "mcnemar": mcnemar(per1[a], per1["A"], pop)}
out["R1_tie_tolerant_modal"] = r1

# --- R2: vote level, paired by (item, model) against the SAME model's original BASE vote
r2 = {}
for a in "ABC":
    d, n = vote_perturb(pop, a)
    r2[a] = {"x": d, "n": n, "p": d / n}
for a in "BC":
    r2[f"{a}_vs_A"] = two_prop(r2[a]["x"], r2[a]["n"], r2["A"]["x"], r2["A"]["n"])
r2["B_vs_C"] = two_prop(r2["B"]["x"], r2["B"]["n"], r2["C"]["x"], r2["C"]["n"])
out["R2_vote_level"] = r2

# --- R3: STRICT subpopulation — no original vote for EITHER removed kind
strict = [i for i in pop if "Circumstances" not in ov[i] and "Structure" not in ov[i]]
r3 = {"n_items": len(strict),
      "excluded_for_a_minority_Circumstances_vote": sum(1 for i in pop if "Circumstances" in ov[i]),
      "excluded_for_a_minority_Structure_vote": sum(1 for i in pop if "Structure" in ov[i])}
for a in "ABC":
    r3[f"modal_{a}"] = {"x": modal_perturb(strict, a), "p": modal_perturb(strict, a) / len(strict)}
    d, n = vote_perturb(strict, a)
    r3[f"vote_{a}"] = {"x": d, "n": n, "p": d / n}
for a in "BC":
    r3[f"modal_{a}_vs_A"] = two_prop(modal_perturb(strict, a), len(strict),
                                     modal_perturb(strict, "A"), len(strict))
    r3[f"vote_{a}_vs_A"] = two_prop(r3[f"vote_{a}"]["x"], r3[f"vote_{a}"]["n"],
                                    r3["vote_A"]["x"], r3["vote_A"]["n"])
r3["vote_B_vs_C"] = two_prop(r3["vote_B"]["x"], r3["vote_B"]["n"],
                             r3["vote_C"]["x"], r3["vote_C"]["n"])
out["R3_strict_subpopulation"] = r3

# --- R4: B vs C head to head on the frozen primary
per = {a: {i: arms[a]["modal"].get(i) != om[i] for i in pop} for a in "ABC"}
out["R4_B_vs_C_primary"] = {"two_prop": two_prop(13, len(pop), 12, len(pop)),
                            "mcnemar": mcnemar(per["B"], per["C"], pop),
                            "moved_in_B": sorted(i for i in pop if per["B"][i]),
                            "moved_in_C": sorted(i for i in pop if per["C"][i]),
                            "moved_in_both": sorted(i for i in pop if per["B"][i] and per["C"][i]),
                            "moved_in_A": sorted(i for i in pop if per["A"][i])}

# --- R5: where the removed kind's VOTES went, corpus-wide (all 248 items)
dist = {}
for a in "ABC":
    c = collections.Counter()
    for l in open(ROOT / f"judgments_{a}.jsonl"):
        r = json.loads(l)
        if r.get("kind"):
            c[r["kind"].strip()] += 1
    dist[a] = dict(c)
r5 = {"distribution": dist, "delta_vs_A": {}}
for a in "BC":
    freed = dist["A"].get(REM[a], 0)
    delta = {k: dist[a].get(k, 0) - dist["A"].get(k, 0) for k in LABELS}
    gains = {k: v for k, v in delta.items() if v > 0 and k != REM[a]}
    top = max(gains.items(), key=lambda kv: kv[1]) if gains else (None, 0)
    r5["delta_vs_A"][a] = {"removed": REM[a], "votes_freed": freed, "delta": delta,
                           "top_gainer": top[0], "top_gain": top[1],
                           "top_gainer_share_of_freed": (top[1] / freed) if freed else None,
                           "n_kinds_gaining": len(gains)}
out["R5_vote_redistribution"] = r5

# --- R6: composition of the primary perturbations
out["R6_composition"] = {a: {"genuine_relabel": sum(1 for i in pop
                                                    if arms[a]["modal"].get(i) not in (om[i], "TIE", "NOPARSE")),
                             "tie": sum(1 for i in pop if arms[a]["modal"].get(i) in ("TIE", "NOPARSE"))}
                         for a in "ABC"}

json.dump(out, open(ROOT / "robustness.json", "w"), indent=1)
print("wrote", ROOT / "robustness.json")
for k in ("R1_tie_tolerant_modal", "R2_vote_level", "R3_strict_subpopulation"):
    print(k, json.dumps({kk: vv for kk, vv in out[k].items()
                         if not isinstance(vv, dict) or "p" in vv or "diff" in vv})[:600])
