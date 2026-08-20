"""OB3 — MC1, the context manipulation check. sec 8.1. OUTCOME-BLIND.

150 rows drawn at random without replacement from the 1,334 dual-source-confirmed rows with
`random.Random(20260820)`, stratified to the realised am/es/en proportions, plus a declared
uncontrolled 50-row `zh` leg. Discharges V2.
"""
from __future__ import annotations
import collections, json, random, sys
sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad/a0run/src")
import a0lib as A
import a0judge as J
import a0stat as S


def norm_lang(v):
    if not isinstance(v, str):
        return None
    v = v.strip().strip('".').lower()
    v = "".join(ch for ch in v if ch.isalpha() or ch == "-")
    if not v:
        return None
    return v.split("-")[0][:2]


def majority(labels):
    labels = [l for l in labels if l]
    if len(labels) < 2:
        return None
    c = collections.Counter(labels).most_common()
    if len(c) == 1 or c[0][1] > c[1][1]:
        return c[0][0]
    return None


def main():
    fr = A.rjson("A0_frames.json")
    rows = {d["id"]: d for d in A.rjson("A0_rows.json")}
    dual = fr["mc1_dual_ids"]
    zh = fr["mc1_zh_ids"]
    rng = random.Random(A.SEED)

    # stratify 150 to the realised am/es/en proportions (largest remainder)
    by = collections.defaultdict(list)
    for i in dual:
        by[rows[i]["lang"]].append(i)
    langs = sorted(by)
    exact = {L: 150 * len(by[L]) / len(dual) for L in langs}
    take = {L: int(exact[L]) for L in langs}
    rem = sorted(langs, key=lambda L: -(exact[L] - take[L]))
    for L in rem[:150 - sum(take.values())]:
        take[L] += 1
    gate_ids = []
    for L in langs:
        gate_ids.extend(rng.sample(sorted(by[L]), take[L]))
    zh_ids = rng.sample(sorted(zh), 50)

    jobs = ([{"model": m, "text": rows[i]["mc1_prompt"], "row": i,
              "truth": rows[i]["lang"], "leg": "gate"}
             for i in gate_ids for m in J.MODELS] +
            [{"model": m, "text": rows[i]["mc1_prompt"], "row": i,
              "truth": "zh", "leg": "zh"}
             for i in zh_ids for m in J.MODELS])
    recs, stats = J.run_jobs(jobs, tag="MC1", workers=12)
    if stats.get("aborted"):
        return 3

    per = collections.defaultdict(dict)
    meta = {}
    for r in recs:
        j = J.parse_json(r.get("raw"))
        per[r["row"]][r["model"]] = norm_lang((j or {}).get("lang"))
        meta[r["row"]] = (r["truth"], r["leg"])

    def score(ids):
        ok = 0; got = []
        for i in ids:
            mj = majority([per[i].get(m) for m in J.MODELS])
            got.append(mj)
            if mj == meta[i][0]:
                ok += 1
        return ok, got

    ok_g, got_g = score(gate_ids)
    ok_z, got_z = score(zh_ids)
    lb = S.clopper_pearson_lower(ok_g, len(gate_ids), 0.05)
    v2 = lb > 0.80

    res = {"gate_n": len(gate_ids), "gate_strata": take,
           "gate_agree": ok_g, "gate_rate": ok_g / len(gate_ids),
           "gate_CP_lower_95": lb, "V2_PASS": bool(v2),
           "threshold": "CP lower bound > 0.80 (>= 129/150)",
           "zh_n": len(zh_ids), "zh_agree": ok_z, "zh_rate": ok_z / len(zh_ids),
           "zh_note": "declared uncontrolled leg: zh ground truth is single-source "
                      "(regex only); it cannot fire the gate (sec 8.1)",
           "gate_pred_dist": dict(collections.Counter(got_g)),
           "zh_pred_dist": dict(collections.Counter(got_z)),
           "per_truth": {L: {"n": sum(1 for i in gate_ids if meta[i][0] == L),
                             "ok": sum(1 for i in gate_ids
                                       if meta[i][0] == L and
                                       majority([per[i].get(m) for m in J.MODELS]) == L)}
                         for L in langs},
           "spend": stats}
    A.wjson("A0_mc1.json", res)
    print(json.dumps({k: v for k, v in res.items() if k != "spend"}, indent=1))
    A.marker("OB3_mc1.done", {"V2_PASS": bool(v2), "lb": lb, "agree": ok_g})
    return 0


if __name__ == "__main__":
    sys.exit(main())
