"""GAUGE TEST — analysis, per GAUGE_TEST_PREREG.md + EXECUTION_NOTE.md.

Two stages, mechanically ordered so the VOID determination cannot be read after the verdict:

  stage 1 (`void`)    loads ONLY arms A and C, computes pA, pC and the control test, writes
                      void.json. Arm B's judgment file is never opened.
  stage 2 (`verdict`) refuses to run without void.json; loads arm B, computes pB, the bands,
                      the secondary orphan tables and the kills, writes gauge_results.json.

No third-party dependencies: normal CDF from math.erf, exact binomial from math.comb.
"""
from __future__ import annotations
import collections, json, math, pathlib, sys

ROOT = pathlib.Path("/home/emoore/CIRISOntology/scratchpad/gaugetest")
PLAIN_ALL = ["Priorities", "Rules", "Manner", "Identity", "Confidence", "Facts",
             "Circumstances", "Process", "Model", "Structure", "Premises", "Record"]
REMOVED_PLAIN = {"A": None, "B": "Circumstances", "C": "Structure"}
TARGET_KEY = {"B": "contingent", "C": "structural"}   # authored kind_target of the removed kind


# ---------- shared machinery ----------

def modal_of(votes):
    """EXECUTION_NOTE G1/G3: plurality over PARSED votes; tie for top -> 'TIE';
    no parsed vote at all -> 'NOPARSE'."""
    if not votes:
        return "NOPARSE"
    c = collections.Counter(votes).most_common()
    if len(c) > 1 and c[0][1] == c[1][1]:
        return "TIE"
    return c[0][0]


def load_arm(arm):
    p = ROOT / f"judgments_{arm}.jsonl"
    votes = collections.defaultdict(list)
    rows = 0
    parse_fail = collections.Counter()
    offvocab = collections.Counter()
    cells = set()
    spend_tokens = collections.Counter()
    for l in open(p):
        r = json.loads(l)
        rows += 1
        cells.add((r["id"], r["model"]))
        spend_tokens[(r["model"], "in")] += r.get("in_tok", 0)
        spend_tokens[(r["model"], "out")] += r.get("out_tok", 0)
        k = r.get("kind")
        if not k:
            parse_fail[r["model"]] += 1
            continue
        k = k.strip()
        if k not in PLAIN_ALL and k != "NO FIT":
            offvocab[k] += 1
        if REMOVED_PLAIN[arm] and k == REMOVED_PLAIN[arm]:
            offvocab[f"[removed-label emitted] {k}"] += 1
        votes[r["id"]].append(k)
    modal = {i: modal_of(v) for i, v in votes.items()}
    return {"arm": arm, "rows": rows, "cells": len(cells), "votes": dict(votes),
            "modal": modal, "parse_fail": dict(parse_fail),
            "n_parse_fail": sum(parse_fail.values()),
            "offvocab": dict(offvocab), "tokens": {f"{m}|{d}": v for (m, d), v in spend_tokens.items()}}


def perturbation(arm_data, orig_modal, pop):
    """PRIMARY: fraction of the untouched population whose arm modal differs from the
    original 11-way modal. TIE and NOPARSE count as differing (G3)."""
    per = {}
    for i in pop:
        lab = arm_data["modal"].get(i, "MISSING")
        per[i] = (lab != orig_modal[i])
    x = sum(per.values())
    return x, len(pop), x / len(pop), per


def phi(z):
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def two_prop(x1, n1, x2, n2):
    """One-sided pooled two-proportion z test of H1: p1 > p2 (G4). Two-sided reported too."""
    p1, p2 = x1 / n1, x2 / n2
    pp = (x1 + x2) / (n1 + n2)
    se = math.sqrt(pp * (1 - pp) * (1 / n1 + 1 / n2)) if 0 < pp < 1 else 0.0
    if se == 0:
        return {"p1": p1, "p2": p2, "diff": p1 - p2, "z": float("nan"),
                "p_one_sided": 1.0 if p1 <= p2 else 0.0, "p_two_sided": 1.0 if p1 == p2 else 0.0,
                "note": "degenerate: pooled proportion is 0 or 1"}
    z = (p1 - p2) / se
    return {"p1": p1, "p2": p2, "diff": p1 - p2, "z": z,
            "p_one_sided": 1 - phi(z), "p_two_sided": 2 * (1 - phi(abs(z)))}


def mcnemar(per_x, per_a, pop):
    """Exact one-sided McNemar (sensitivity): H1 more perturbed in X than in A."""
    b = sum(1 for i in pop if per_x[i] and not per_a[i])
    c = sum(1 for i in pop if per_a[i] and not per_x[i])
    n = b + c
    if n == 0:
        return {"b": b, "c": c, "p_one_sided": 1.0, "note": "no discordant pairs"}
    p = sum(math.comb(n, k) for k in range(b, n + 1)) / (2 ** n)
    return {"b": b, "c": c, "p_one_sided": p}


def entropy_bits(counts):
    n = sum(counts.values())
    if n == 0:
        return 0.0
    return -sum((v / n) * math.log2(v / n) for v in counts.values() if v > 0)


# ---------- stage 1: VOID, computed from arms A and C only ----------

def stage_void():
    orig = json.load(open(ROOT / "originals.json"))
    pop = orig["untouched"]
    om = orig["modal"]
    A, C = load_arm("A"), load_arm("C")
    xA, nA, pA, perA = perturbation(A, om, pop)
    xC, nC, pC, perC = perturbation(C, om, pop)
    ctrl = two_prop(xC, nC, xA, nA)
    mc = mcnemar(perC, perA, pop)

    protocol = {}
    for d in (A, C):
        rate = d["n_parse_fail"] / max(d["rows"], 1)
        protocol[d["arm"]] = {"rows": d["rows"], "cells": d["cells"],
                              "parse_failures": d["n_parse_fail"], "parse_fail_rate": rate,
                              "over_5pct_VOID": rate > 0.05,
                              "offvocab": d["offvocab"],
                              "ties": sum(1 for i in pop if d["modal"].get(i) == "TIE"),
                              "noparse_items": sum(1 for i in pop if d["modal"].get(i) == "NOPARSE"),
                              "missing_items": sum(1 for i in pop if i not in d["modal"])}
    void_stat = ctrl["p_one_sided"] >= 0.05
    void_protocol = any(v["over_5pct_VOID"] for v in protocol.values())
    out = {"stage": "void", "n_untouched": len(pop),
           "pA": {"x": xA, "n": nA, "p": pA}, "pC": {"x": xC, "n": nC, "p": pC},
           "control_test_C_vs_A": ctrl, "mcnemar_C_vs_A": mc,
           "protocol_checks": protocol,
           "VOID_statistical": void_stat, "VOID_protocol": void_protocol,
           "VOID": bool(void_stat or void_protocol),
           "determination": ("VOID — the control failed; no verdict may be read in either direction"
                             if (void_stat or void_protocol) else
                             "NOT VOID — removing a genuine kind (Structure) perturbs the other "
                             "ten significantly more than a re-run does; the instrument resolves")}
    json.dump(out, open(ROOT / "void.json", "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "protocol_checks"}, indent=1))
    print("wrote", ROOT / "void.json")


# ---------- stage 2: verdict + secondary ----------

def stage_verdict():
    vp = ROOT / "void.json"
    if not vp.exists():
        sys.exit("REFUSING: void.json absent. The VOID determination is computed first, "
                 "from arms A and C only. Run --stage void.")
    void = json.load(open(vp))
    orig = json.load(open(ROOT / "originals.json"))
    pop = orig["untouched"]
    om = orig["modal"]
    A, B, C = load_arm("A"), load_arm("B"), load_arm("C")
    xA, nA, pA, perA = perturbation(A, om, pop)
    xB, nB, pB, perB = perturbation(B, om, pop)
    xC, nC, pC, perC = perturbation(C, om, pop)

    treat = two_prop(xB, nB, xA, nA)
    ctrl = void["control_test_C_vs_A"]
    half = (pC - pA) / 2.0
    cond_ns = treat["p_one_sided"] >= 0.05          # B not significantly above A
    cond_half = (pB - pA) < half                    # B costs less than half of C

    if void["VOID"]:
        verdict = "VOID / UNDERPOWERED — no verdict"
    elif cond_ns and cond_half:
        verdict = "GAUGE CONFIRMED"
    elif (not cond_ns) and (not cond_half):
        verdict = "NOT GAUGE — K-G1 FIRES"
    else:
        verdict = "AMBIGUOUS"

    # --- sensitivity: arm ties dropped pairwise ---
    def paired_drop(dx, da):
        keep = [i for i in pop
                if dx["modal"].get(i) not in ("TIE", "NOPARSE", None)
                and da["modal"].get(i) not in ("TIE", "NOPARSE", None)]
        x1 = sum(1 for i in keep if dx["modal"][i] != om[i])
        x2 = sum(1 for i in keep if da["modal"][i] != om[i])
        return {"n": len(keep), "x_treat": x1, "x_base": x2,
                "p_treat": x1 / len(keep), "p_base": x2 / len(keep),
                "test": two_prop(x1, len(keep), x2, len(keep))}
    sens = {"B_vs_A": paired_drop(B, A), "C_vs_A": paired_drop(C, A)}

    # --- SECONDARY: where the orphans go ---
    tgt = orig["kind_target"]
    orphans = {}
    for arm, data in (("B", B), ("C", C)):
        ids_target = [i for i in tgt if tgt[i] == TARGET_KEY[arm]]
        dist = collections.Counter(data["modal"].get(i, "MISSING") for i in ids_target)
        ids_modal = [i for i in tgt if om[i] == REMOVED_PLAIN[arm]]
        dist_modal = collections.Counter(data["modal"].get(i, "MISSING") for i in ids_modal)
        orphans[arm] = {
            "removed": REMOVED_PLAIN[arm],
            "primary_population": "authored kind_target",
            "n": len(ids_target),
            "distribution": dict(dist.most_common()),
            "entropy_bits": entropy_bits(dist),
            "entropy_normalised": entropy_bits(dist) / math.log2(11),
            "top": dist.most_common(1)[0] if dist else None,
            "top_share": (dist.most_common(1)[0][1] / len(ids_target)) if ids_target else 0.0,
            "sensitivity_modal_orphans": {"n": len(ids_modal),
                                          "distribution": dict(dist_modal.most_common()),
                                          "entropy_bits": entropy_bits(dist_modal)},
            "original_modal_distribution": dict(
                collections.Counter(om[i] for i in ids_target).most_common()),
        }

    # K-G2, per EXECUTION_NOTE G7b
    hB, hC = orphans["B"]["entropy_bits"], orphans["C"]["entropy_bits"]
    tB, tC = orphans["B"]["top_share"], orphans["C"]["top_share"]
    topB = orphans["B"]["top"][0] if orphans["B"]["top"] else None
    concentrated = (hB <= hC) and (tB >= tC)
    kg2 = concentrated and (topB != "Facts")
    staked_secondary = {
        "structure_concentrates_on_Manner": orphans["C"]["top"][0] if orphans["C"]["top"] else None,
        "circumstances_scatters_or_Facts": topB,
        "B_at_least_as_concentrated_as_C": concentrated,
        "K_G2_FIRES": bool(kg2),
        "note": ("concentrated but on Facts — the prereg's own staked destination, so K-G2 does "
                 "not fire; reported as adverse-leaning" if (concentrated and topB == "Facts") else ""),
    }

    out = {"stage": "verdict",
           "VOID_determination_read_from": str(vp), "VOID": void["VOID"],
           "void_determination_text": void["determination"],
           "n_untouched": len(pop),
           "pA": pA, "pB": pB, "pC": pC,
           "counts": {"xA": xA, "xB": xB, "xC": xC, "n": nA},
           "treatment_test_B_vs_A": treat, "control_test_C_vs_A": ctrl,
           "mcnemar_B_vs_A": mcnemar(perB, perA, pop),
           "mcnemar_C_vs_A": void["mcnemar_C_vs_A"],
           "half_of_control": half,
           "band_conditions": {"B_not_significantly_above_A": cond_ns,
                               "B_minus_A_below_half_of_C_minus_A": cond_half},
           "VERDICT": verdict,
           "K_G1_FIRES": verdict.startswith("NOT GAUGE"),
           "sensitivity_ties_dropped": sens,
           "orphans": orphans, "secondary": staked_secondary,
           "arm_protocol": {a: {"rows": d["rows"], "cells": d["cells"],
                                "parse_failures": d["n_parse_fail"],
                                "parse_fail_rate": d["n_parse_fail"] / max(d["rows"], 1),
                                "offvocab": d["offvocab"],
                                "ties_in_pop": sum(1 for i in pop if d["modal"].get(i) == "TIE"),
                                "noparse_in_pop": sum(1 for i in pop if d["modal"].get(i) == "NOPARSE"),
                                "modal_distribution": dict(collections.Counter(
                                    d["modal"].get(i, "MISSING") for i in pop).most_common())}
                           for a, d in (("A", A), ("B", B), ("C", C))},
           }
    # where the untouched population moved, per arm (diagnostic, no verdict)
    out["movement"] = {}
    for arm, data in (("A", A), ("B", B), ("C", C)):
        mv = collections.Counter()
        for i in pop:
            lab = data["modal"].get(i, "MISSING")
            if lab != om[i]:
                mv[f"{om[i]} -> {lab}"] += 1
        out["movement"][arm] = dict(mv.most_common())
    json.dump(out, open(ROOT / "gauge_results.json", "w"), indent=1)
    print(json.dumps({k: out[k] for k in
                      ("pA", "pB", "pC", "counts", "treatment_test_B_vs_A", "control_test_C_vs_A",
                       "half_of_control", "band_conditions", "VERDICT", "K_G1_FIRES",
                       "secondary", "sensitivity_ties_dropped")}, indent=1))
    print("\nORPHANS:", json.dumps(out["orphans"], indent=1))
    print("wrote", ROOT / "gauge_results.json")


if __name__ == "__main__":
    stage = sys.argv[1] if len(sys.argv) > 1 else "both"
    if stage in ("void", "both"):
        stage_void()
    if stage in ("verdict", "both"):
        stage_verdict()
