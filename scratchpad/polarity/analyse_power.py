"""POLARITY stage 4 — counts, P1, P4, and the UNDERPOWERED determination.

Per POLARITY_PREREG.md §3, the UNDERPOWERED condition is evaluated BEFORE any p-value is
read. This script therefore computes the permutation NULL distribution and the qualifying-
kind counts, and deliberately does NOT compute or print the observed statistic or any
p-value. Stage 5 (`analyse_p.py`) does that, and refuses to run without `power.json`.
"""
from __future__ import annotations
import collections, json, pathlib
import numpy as np

D = pathlib.Path("/home/emoore/CIRISOntology/scratchpad/polarity")
NPERM = 2000
SEED = 20260820

def load(p):
    return [json.loads(l) for l in open(p) if l.strip()]

def item_modal(votes):
    """Prereg §2: modal by plurality; ties -> AMBIGUOUS. EXECUTION_NOTE D8."""
    parsed = [v for v in votes if v in ("+", "-", "AMBIGUOUS")]
    if len(parsed) < 2:
        return None, parsed          # parse failure at item level
    c = collections.Counter(parsed).most_common()
    if len(c) > 1 and c[0][1] == c[1][1]:
        return "AMBIGUOUS", parsed   # tie -> AMBIGUOUS
    return c[0][0], parsed

def build():
    corpus = {r["id"]: r for r in load(D / "scoring_corpus.jsonl")}
    js = load(D / "polarity_judgments.jsonl")
    votes = collections.defaultdict(dict)
    err = collections.Counter(); calls = collections.Counter()
    for r in js:
        if "error" in r:
            err[r.get("model", "?")] += 1; calls[r.get("model", "?")] += 1; continue
        calls[r["model"]] += 1
        votes[r["id"]][r["model"]] = r.get("polarity")
        if r.get("polarity") is None:
            err[r["model"]] += 1
    scored = {}
    for iid, mv in votes.items():
        m, parsed = item_modal(list(mv.values()))
        scored[iid] = {"modal": m, "votes": mv, "n_parsed": len(parsed)}
    return corpus, scored, err, calls

def main():
    corpus, scored, err, calls = build()
    axis_items = [r for r in corpus.values() if r["axis_kind"] and r["axis_kind"] != "Record"]
    n_axis = len(axis_items)
    out = {"n_corpus_total": len(corpus), "n_axis_defined": n_axis,
           "n_record_unscored": sum(1 for r in corpus.values() if r["axis_kind"] == "Record")}

    # ---- parse rate (VOID §4: parse failure > 5%) ----
    tot_calls = sum(calls.values()); tot_err = sum(err.values())
    out["calls"] = dict(calls); out["parse_failures"] = dict(err)
    out["parse_failure_rate"] = tot_err / max(tot_calls, 1)
    out["parse_failure_rate_by_model"] = {m: err[m] / calls[m] for m in calls}
    out["item_level_parse_failures"] = sorted(i for i, s in scored.items() if s["modal"] is None)
    out["VOID_parse"] = out["parse_failure_rate"] > 0.05
    out["VOID_missing_items"] = sorted(r["id"] for r in axis_items if r["id"] not in scored)

    # ---- P1 / P4: ambiguity ----
    modal = {i: scored[i]["modal"] for i in scored}
    amb = [i for i in modal if modal[i] == "AMBIGUOUS"]
    sc = [i for i in modal if modal[i] in ("+", "-")]
    out["n_scored_items"] = len(modal)
    out["n_scoreable"] = len(sc)
    out["n_ambiguous"] = len(amb)
    out["P1_amb_rate_over_axis_defined"] = len(amb) / n_axis
    out["P1_amb_rate_over_272"] = (len(amb) + out["n_record_unscored"]) / len(corpus)
    out["VOID_lt150_scoreable"] = len(sc) < 150
    perk = collections.defaultdict(collections.Counter)
    for i, m in modal.items():
        perk[corpus[i]["axis_kind"]][m or "PARSEFAIL"] += 1
    out["P4_per_kind"] = {k: {"n": sum(c.values()), "plus": c["+"], "minus": c["-"],
                              "ambiguous": c["AMBIGUOUS"], "parsefail": c["PARSEFAIL"],
                              "amb_rate": c["AMBIGUOUS"] / max(sum(c.values()), 1)}
                          for k, c in sorted(perk.items())}
    out["P4_kinds_over_50pct_ambiguous"] = sorted(
        k for k, v in out["P4_per_kind"].items() if v["amb_rate"] > 0.50)

    # ---- P2 cell counts: scoreable AND carrying a usable BASE modal read ----
    def cells(exclude_conj=False):
        c = collections.defaultdict(lambda: collections.defaultdict(list))
        for i in sc:
            r = corpus[i]
            if exclude_conj and r["part"] == "CONJ":
                continue
            if r["base_modal"] is None:   # BASE tie / no BASE votes -> excluded
                continue
            c[r["axis_kind"]][modal[i]].append(r["base_modal"])
        return c
    for tag, exc in (("primary", False), ("no_conj", True)):
        c = cells(exc)
        q = sorted(k for k in c if len(c[k]["+"]) >= 8 and len(c[k]["-"]) >= 8)
        out[f"P2_cells_{tag}"] = {k: {"plus": len(c[k]["+"]), "minus": len(c[k]["-"])}
                                  for k in sorted(c)}
        out[f"P2_qualifying_kinds_{tag}"] = q
        out[f"P2_n_qualifying_{tag}"] = len(q)

    # ---- the permutation NULL (no observed statistic computed here) ----
    c = cells(False)
    q = out["P2_qualifying_kinds_primary"]
    rng = np.random.default_rng(SEED)
    def stat_from(assign):
        vals = []
        for k in q:
            lab = c[k]["+"] + c[k]["-"]
            idx = assign[k]
            npl = len(c[k]["+"])
            A = collections.Counter(lab[j] for j in idx[:npl])
            B = collections.Counter(lab[j] for j in idx[npl:])
            keys = set(A) | set(B)
            na, nb = max(sum(A.values()), 1), max(sum(B.values()), 1)
            vals.append(0.5 * sum(abs(A[x] / na - B[x] / nb) for x in keys))
        return float(np.mean(vals)) if vals else float("nan")
    null = []
    if q:
        for _ in range(NPERM):
            assign = {k: rng.permutation(len(c[k]["+"]) + len(c[k]["-"])) for k in q}
            null.append(stat_from(assign))
        null = np.array(null)
        np.save(D / "null_primary.npy", null)
        out["null_mean"] = float(null.mean()); out["null_sd"] = float(null.std(ddof=1))
        out["null_q"] = {p: float(np.quantile(null, p / 100)) for p in (1, 5, 50, 95, 99)}
        out["null_max"] = float(null.max())
    else:
        out["null_mean"] = out["null_sd"] = None

    # ---- UNDERPOWERED, per EXECUTION_NOTE D6 ----
    cond_a = out["P2_n_qualifying_primary"] < 4
    cond_b = (out["null_sd"] is not None and out["null_sd"] > (1.0 - out["null_mean"]))
    out["UNDERPOWERED_cond_a_fewer_than_4_kinds"] = bool(cond_a)
    out["UNDERPOWERED_cond_b_null_spread_exceeds_range"] = bool(cond_b)
    out["UNDERPOWERED"] = bool(cond_a or cond_b)

    (D / "power.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print("=== stage 4: counts, P1, P4, power. NO p-value computed here. ===")
    for k in ("n_corpus_total", "n_axis_defined", "n_record_unscored", "n_scored_items",
              "n_scoreable", "n_ambiguous", "parse_failure_rate", "VOID_parse",
              "VOID_lt150_scoreable", "P1_amb_rate_over_axis_defined", "P1_amb_rate_over_272",
              "P2_qualifying_kinds_primary", "P2_n_qualifying_primary",
              "P2_qualifying_kinds_no_conj", "null_mean", "null_sd",
              "UNDERPOWERED_cond_a_fewer_than_4_kinds",
              "UNDERPOWERED_cond_b_null_spread_exceeds_range", "UNDERPOWERED"):
        print(f"  {k}: {out[k]}")
    print("  P4 per-kind ambiguity:")
    for k, v in out["P4_per_kind"].items():
        print(f"    {k:14s} n={v['n']:3d}  + {v['plus']:3d}  - {v['minus']:3d}  "
              f"AMB {v['ambiguous']:3d} ({v['amb_rate']:.1%})  fail {v['parsefail']}")
    print("  P2 cells (primary):")
    for k, v in out["P2_cells_primary"].items():
        print(f"    {k:14s} +{v['plus']:3d} / -{v['minus']:3d}"
              + ("   <= QUALIFIES" if k in out["P2_qualifying_kinds_primary"] else ""))

if __name__ == "__main__":
    main()
