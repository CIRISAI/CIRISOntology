"""OB2 — MC2, the dye test (docimasia). sec 8.2. OUTCOME-BLIND (gold kinds are the truth).

120 items = 10 per kind x 12 kinds, `difficulty == "clear"` preferred, seed 20260820,
rendered ON-MANIFOLD through the identical sec 5.2 template. Discharges V1.
"""
from __future__ import annotations
import collections, json, random, sys
sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad/a0run/src")
import a0lib as A
import a0judge as J


def pick_items():
    rows = [json.loads(l) for l in open(A.GOLD) if l.strip()]
    rng = random.Random(A.SEED)
    by = collections.defaultdict(list)
    for r in rows:
        by[r["kind_target"]].append(r)
    out = []
    for k in sorted(by):
        clear = [r for r in by[k] if r.get("difficulty") == "clear"]
        hard = [r for r in by[k] if r.get("difficulty") != "clear"]
        rng.shuffle(clear); rng.shuffle(hard)
        out.extend((clear + hard)[:10])
    return out


def render(item):
    """On-manifold: the identical sec 5.2 template, PROPOSED ACTION := SPEAK, the
    item's `after` as the stated reason, `variation_site` never shown."""
    return A.PROMPT_KIND.format(
        kinds=A.KIND_LINES, task_description=item["before"], thought_content="",
        selected_action="SPEAK",
        action_rationale="The revised text reads:\n" + item["after"])


def majority(labels):
    labels = [l for l in labels if l]
    if len(labels) < 2:
        return "NO MAJORITY"
    c = collections.Counter(labels).most_common()
    if len(c) == 1 or c[0][1] > c[1][1]:
        return c[0][0]
    return "NO MAJORITY"


def norm_kind(k):
    if not isinstance(k, str):
        return None
    k = k.strip().strip('".').title()
    if k.upper() in ("NO FIT", "NOFIT", "NO_FIT"):
        return "NO FIT"
    for v in A.KINDS12:
        if k.lower() == v.lower():
            return v
    return k if k else None


def macro_f1(gold, pred, classes):
    f1s = []
    for c in classes:
        tp = sum(1 for g, p in zip(gold, pred) if g == c and p == c)
        fp = sum(1 for g, p in zip(gold, pred) if g != c and p == c)
        fn = sum(1 for g, p in zip(gold, pred) if g == c and p != c)
        pr = tp / (tp + fp) if tp + fp else 0.0
        rc = tp / (tp + fn) if tp + fn else 0.0
        f1s.append(2 * pr * rc / (pr + rc) if pr + rc else 0.0)
    return sum(f1s) / len(f1s), dict(zip(classes, f1s))


def main():
    items = pick_items()
    jobs = [{"model": m, "text": render(it), "item_id": it["id"],
             "gold": A.PLAIN_OF[it["kind_target"]]}
            for it in items for m in J.MODELS]
    recs, stats = J.run_jobs(jobs, tag="MC2", workers=12)
    if stats.get("aborted"):
        return 3

    by_item = collections.defaultdict(dict)
    gold_of = {}
    for r in recs:
        j = J.parse_json(r.get("raw"))
        by_item[r["item_id"]][r["model"]] = norm_kind((j or {}).get("kind"))
        gold_of[r["item_id"]] = r["gold"]

    ids = sorted(by_item)
    gold = [gold_of[i] for i in ids]
    pred = [majority([by_item[i].get(m) for m in J.MODELS]) for i in ids]

    f1, per = macro_f1(gold, pred, A.KINDS12)

    # depth/surface balanced accuracy, and DEEP sensitivity
    gd = [A.is_deep(g) for g in gold]
    pd = [A.is_deep(p) for p in pred]           # None for NO FIT / NO MAJORITY
    sens_deep_n = sum(1 for g in gd if g == 1)
    sens_surf_n = sum(1 for g in gd if g == 0)
    sens_deep = sum(1 for g, p in zip(gd, pd) if g == 1 and p == 1) / max(1, sens_deep_n)
    sens_surf = sum(1 for g, p in zip(gd, pd) if g == 0 and p == 0) / max(1, sens_surf_n)
    ba = 0.5 * (sens_deep + sens_surf)

    # surface collapse (PLANE's "surface-4"; Record is its own level, sec 10.1)
    gs = [A.kind_m5(g) for g in gold]
    ps = [A.kind_m5(p) for p in pred]
    surf_acc = sum(1 for g, p in zip(gs, ps) if g is not None and g == p) / len(gs)

    conf = collections.Counter((g, p) for g, p in zip(gold, pred))
    boundaries = {f"{a}->{b}": conf.get((a, b), 0) for a, b in
                  [("Premises", "Facts"), ("Structure", "Manner"), ("Model", "Facts"),
                   ("Facts", "Premises"), ("Manner", "Structure"), ("Facts", "Model")]}

    v1 = (f1 >= 0.30) and (ba >= 0.60) and (sens_deep >= 0.40) and (surf_acc >= 0.60)
    res = {"n_items": len(ids), "macro_f1": f1, "per_kind_f1": per,
           "depth_surface_BA": ba, "sens_DEEP": sens_deep, "sens_SURFACE": sens_surf,
           "n_gold_deep": sens_deep_n, "n_gold_surface": sens_surf_n,
           "surface_collapse_acc": surf_acc,
           "no_majority": sum(1 for p in pred if p == "NO MAJORITY"),
           "no_fit": sum(1 for p in pred if p == "NO FIT"),
           "pred_dist": dict(collections.Counter(pred)),
           "plane_boundaries": boundaries,
           "confusion": {f"{g}|{p}": n for (g, p), n in sorted(conf.items())},
           "V1_PASS": bool(v1),
           "thresholds": {"macro_f1>=": 0.30, "BA>=": 0.60, "sens_DEEP>=": 0.40,
                          "surface>=": 0.60},
           "spend": stats}
    A.wjson("A0_mc2.json", res)
    print(json.dumps({k: v for k, v in res.items()
                      if k not in ("confusion", "per_kind_f1")}, indent=1))
    A.marker("OB2_mc2.done", {"V1_PASS": bool(v1), "macro_f1": f1,
                              "BA": ba, "sens_DEEP": sens_deep, "surf": surf_acc})
    return 0


if __name__ == "__main__":
    sys.exit(main())
