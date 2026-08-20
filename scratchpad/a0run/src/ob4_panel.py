"""OB4 — the main judging pass. sec 5.2/5.3, sec 3.9. OUTCOME-BLIND.

One call per distinct scrub-normalised judge input (716 on FRAME-T), broadcast to every row
in the block. Majority of three, no tie-break, NO MAJORITY is a label.
Discharges V3 (coverage), V4 (decisiveness), V15 (repeat-block support).
"""
from __future__ import annotations
import collections, json, sys
sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad/a0run/src")
import a0lib as A
import a0judge as J
from ob2_mc2 import norm_kind, majority

VALID = set(A.KINDS12) | {"NO FIT"}


def kappa(x, y):
    labs = sorted(set(x) | set(y))
    n = len(x)
    if n == 0:
        return float("nan")
    po = sum(1 for a, b in zip(x, y) if a == b) / n
    cx = collections.Counter(x); cy = collections.Counter(y)
    pe = sum((cx[l] / n) * (cy[l] / n) for l in labs)
    return (po - pe) / (1 - pe) if pe < 1 else float("nan")


def main():
    blocks = [json.loads(l) for l in open(A.OUT / "A0_blocks.jsonl")]
    fr = A.rjson("A0_frames.json")
    rows = {d["id"]: d for d in A.rjson("A0_rows.json")}

    jobs = [{"model": m, "text": b["prompt"], "bid": b["bid"]}
            for b in blocks for m in J.MODELS]
    recs, stats = J.run_jobs(jobs, tag="KIND", workers=16, progress_every=200)
    if stats.get("aborted"):
        return 3

    per = collections.defaultdict(dict)
    raw_ok = collections.defaultdict(dict)
    for r in recs:
        j = J.parse_json(r.get("raw"))
        k = norm_kind((j or {}).get("kind"))
        k = k if k in VALID else None
        per[r["bid"]][r["model"]] = k
        raw_ok[r["bid"]][r["model"]] = k is not None

    bids = sorted(per)
    maj = {}
    for b in bids:
        labs = [per[b].get(m) for m in J.MODELS]
        maj[b] = majority(labs) if all(l is not None for l in labs) else \
            (majority(labs) if sum(l is not None for l in labs) >= 2 else None)

    # ---- V3 coverage, V4 decisiveness, V15 support, per judged frame ---------
    def frame_blocks(name):
        return sorted({rows[i]["bid"] for i in fr["frames"][name]})

    gates = {}
    for fname in ("FRAME-T", "FRAME-TL", "FRAME-H"):
        fb = frame_blocks(fname)
        full = [b for b in fb if all(raw_ok[b].get(m) for m in J.MODELS)]
        nofit = sum(1 for b in fb if maj.get(b) == "NO FIT")
        nomaj = sum(1 for b in fb if maj.get(b) in (None, "NO MAJORITY"))
        gates[fname] = {
            "distinct_inputs": len(fb),
            "V3_coverage": len(full) / len(fb),
            "V3_PASS": len(full) / len(fb) >= 0.90,
            "V3_caveat_band": 0.90 <= len(full) / len(fb) < 0.95,
            "NO_FIT": nofit, "NO_MAJORITY": nomaj,
            "V4_frac": (nofit + nomaj) / len(fb),
            "V4_PASS": (nofit + nomaj) / len(fb) <= 0.10,
            "V15_PASS": len(fb) >= 300,
        }

    # ---- agreement, both bases (sec 5.3, b11) --------------------------------
    def agr(bs):
        trip = sum(1 for b in bs if len({per[b].get(m) for m in J.MODELS}) == 1)
        return trip / len(bs) if bs else float("nan")

    fbT = frame_blocks("FRAME-T")
    rowbids = [rows[i]["bid"] for i in fr["frames"]["FRAME-T"]]
    kap = {}
    for i in range(3):
        for j2 in range(i + 1, 3):
            m1, m2 = J.MODELS[i], J.MODELS[j2]
            x = [per[b].get(m1) or "NONE" for b in fbT]
            y = [per[b].get(m2) or "NONE" for b in fbT]
            kap[f"{m1.split('/')[-1]}|{m2.split('/')[-1]}"] = kappa(x, y)

    panel = {
        "n_blocks": len(bids),
        "gates": gates,
        "three_way_agreement_distinct": agr(fbT),
        "three_way_agreement_rows": agr(rowbids),
        "kappa_pairwise_distinct": kap,
        "per_model_dist_distinct": {m.split("/")[-1]: dict(collections.Counter(
            per[b].get(m) for b in fbT)) for m in J.MODELS},
        "majority_dist_distinct": dict(collections.Counter(maj.get(b) for b in fbT)),
        "majority_dist_rows_FRAME_TL": dict(collections.Counter(
            maj.get(rows[i]["bid"]) for i in fr["frames"]["FRAME-TL"])),
        "spend": stats,
    }
    A.wjson("A0_panel.json", panel)
    with open(A.OUT / "A0_kinds.jsonl", "w") as f:
        for b in bids:
            f.write(json.dumps({"bid": b, "majority": maj.get(b),
                                "per_model": {m.split("/")[-1]: per[b].get(m)
                                              for m in J.MODELS}}) + "\n")
    print(json.dumps({k: v for k, v in panel.items()
                      if k not in ("per_model_dist_distinct", "spend")}, indent=1))
    A.marker("OB4_panel.done", {"gates": gates})
    return 0


if __name__ == "__main__":
    sys.exit(main())
