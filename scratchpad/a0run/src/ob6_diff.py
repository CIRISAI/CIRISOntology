"""OB6 — the declared secondary: the diff arm. sec 3.6, sec 5.4. OUTCOME-BLIND.

NEVER KILL-BEARING under any outcome. The heuristic diff instruments were validated on
before/after pairs of ONE artifact; a chain pair here is thought-to-thought, which is a
different object, and the parent is not uniquely identified because `thought_id` is truncated
and collides. Both facts are carried in the output.
"""
from __future__ import annotations
import collections, json, sys
sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad/a0run/src")
sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")
import a0lib as A
from instruments import v0c, v0d


def main():
    live = A.load_rows()          # sealed
    T = [r["t"] for r in live]
    text = {}
    by_tid = collections.defaultdict(list)
    for t in T:
        ts = t.get("thought_start") or {}
        tc = ts.get("thought_content")
        if t.get("trace_level") == "full_traces" and tc:
            text[t["id"]] = tc
        if t.get("thought_id"):
            by_tid[t["thought_id"]].append(t["id"])

    have_parent = [t for t in T if t.get("trace_level") == "full_traces"
                   and (t.get("thought_start") or {}).get("parent_thought_id")]
    named = [t for t in have_parent
             if (t["thought_start"]["parent_thought_id"]) in by_tid]
    readable = [t for t in named
                if any(i in text for i in by_tid[t["thought_start"]["parent_thought_id"]])]

    pairs, dropped = [], 0
    for t in readable:
        pid = t["thought_start"]["parent_thought_id"]
        cands = [i for i in by_tid[pid] if i in text and i < t["id"]]
        if not cands:
            dropped += 1
            continue
        pairs.append((max(cands), t["id"]))

    fr = A.rjson("A0_frames.json")
    rows = {d["id"]: d for d in A.rjson("A0_rows.json")}
    kinds = {json.loads(l)["bid"]: json.loads(l)["majority"]
             for l in open(A.OUT / "A0_kinds.jsonl")} \
        if (A.OUT / "A0_kinds.jsonl").exists() else {}

    fired = collections.Counter()
    per_row = {}
    for p, c in pairs:
        b, a = text[p][:4000], text[c][:4000]
        f = []
        try:
            if v0d.axiotic(b, a, judge=None).get("fired"):
                f.append("Priorities")
        except Exception:
            pass
        try:
            if v0d.nomological(b, a, judge=None).get("fired"):
                f.append("Model")
        except Exception:
            pass
        for nm, fn in v0c.INSTRUMENTS_V2.items():
            try:
                if fn(b, a).get("fired"):
                    f.append(A.PLAIN_OF.get(nm, nm))
            except Exception:
                pass
        for x in f:
            fired[x] += 1
        per_row[c] = f

    both = [(c, per_row[c], kinds.get(rows[c]["bid"]))
            for p, c in pairs if kinds.get(rows[c].get("bid")) is not None]
    agree = sum(1 for c, f, k in both if k in f)
    agree_m5 = sum(1 for c, f, k in both
                   if A.kind_m5(k) in {A.kind_m5(x) for x in f if A.kind_m5(x)})
    multi = sum(1 for c, f, k in both if len(f) > 1)
    silent = sum(1 for c, f, k in both if not f)

    out = {"rows_with_parent_id": len(have_parent),
           "parent_named_in_corpus": len(named),
           "parent_with_readable_thought_content": len(readable),
           "pairs_resolved": len(pairs), "pairs_dropped": dropped,
           "prereg_pinned": {"1012": len(have_parent) == 1012,
                             "903": len(named) == 903, "868": len(readable) == 868},
           "instrument_fire_counts": dict(fired),
           "n_fired_any": sum(1 for f in per_row.values() if f),
           "coverage_of_FRAME_T": len(pairs) / len(fr["frames"]["FRAME-T"]),
           "panel_comparison": {"n_compared": len(both),
                                "instrument_names_panel_kind_12way": agree,
                                "rate_12way": agree / len(both) if both else None,
                                "agrees_on_surface_collapse": agree_m5,
                                "rate_surface_collapse": agree_m5 / len(both) if both else None,
                                "n_multi_fire": multi, "n_silent": silent},
           "caveats": ["the pair is thought-to-thought, NOT artifact-before-to-after: a "
                       "different object from what the instruments were validated on "
                       "(sec 3.6)",
                       "thought_id is truncated and collides (926 values name more than one "
                       "row); the parent is the largest id strictly below the child with "
                       "readable content, per the sec 3.6 pinned rule",
                       "NOT KILL-BEARING under any outcome (sec 5.4)"]}
    A.wjson("A0_diffarm.json", out)
    print(json.dumps(out, indent=1, default=str))
    A.marker("OB6_diff.done", {"pairs": len(pairs)})
    return 0


if __name__ == "__main__":
    sys.exit(main())
