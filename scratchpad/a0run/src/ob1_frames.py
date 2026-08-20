"""OB1 — frames, canonical clustering, discretizations, scrub, judge inputs.

OUTCOME-BLIND. sec 12 step 1: "Build frames; write A0_frames.json ... No labels touched."
Every pre-registered count is re-derived here and compared against the prereg's pinned
value; disagreements are written into the output as `mismatches` rather than smoothed.
"""
from __future__ import annotations
import json, sys, collections
sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad/a0run/src")
import a0lib as A

CLEAN_ACTIONS = {"SPEAK", "PONDER", "TASK_COMPLETE"}

PINNED = {  # what the prereg says these must come out at
    "FRAME-T": 2148, "FRAME-H": 1398, "FRAME-TL": 1885, "FRAME-HL": 1270,
    "FRAME-CP": 2662, "FRAME-4": 1154,
    "clusters/FRAME-T": 526, "clusters/FRAME-H": 410, "clusters/FRAME-TL": 480,
    "clusters/FRAME-HL": 378, "clusters/FRAME-CP": 580,
    "distinct/FRAME-T": 716, "distinct/FRAME-TL": 625, "distinct/FRAME-H": 408,
    "tier/full_traces": 2148, "tier/detailed": 1928, "tier/generic": 2389,
}


def main():
    bad = A.verify_pins()
    if bad:
        print("PIN MISMATCH", bad)
        return 2
    rows = A.load_rows()  # sealed
    n = len(rows)
    rec = []
    for r in rows:
        t, c = r["t"], r["c"]
        ts = t.get("thought_start") or {}
        cr = t.get("conscience_result") or {}
        act = t.get("selected_action")
        d = {
            "id": t["id"],
            "tier": t.get("trace_level"),
            "task_id_raw": t.get("task_id"),
            "cluster": A.canon_task_id(t.get("task_id"), t["id"]),
            "action": act if isinstance(act, str) and not A.is_corrupted(act) else None,
            "action_corrupt": A.is_corrupted(act),
            "lang": A.lang_of(t, c),
            "lang_regex": A.lang_regex(t),
            "lang_qa": (c.get("qa_language")
                        if isinstance(c.get("qa_language"), str)
                        and not A.is_corrupted(c.get("qa_language")) else None),
            "entropy_score": cr.get("entropy_score"),
            "coherence_score": cr.get("coherence_score"),
            "optveto": cr.get("optimization_veto_entropy_ratio"),
            "humility": cr.get("epistemic_humility_certainty"),
            "agent_version": c.get("agent_version"),
            "attestation": c.get("attestation_status"),
            "day": A.day_key(t.get("trace_id")),
            "task_class": c.get("task_class"),
            "cognitive_state": t.get("cognitive_state"),
            "thought_depth": t.get("thought_depth"),
            "qa_question_num": c.get("qa_question_num"),
            "tokens_total": t.get("tokens_total"),
            "llm_calls": t.get("llm_calls") if t.get("llm_calls") is not None else c.get("llm_calls"),
            "has_conflicts": ((t.get("dma_results") or {}).get("pdma") or {}).get("has_conflicts"),
            "fragility": (t.get("idma_result") or {}).get("fragility_flag"),
            "idma_phase": t.get("idma_phase"),
            "parent_thought_id": ts.get("parent_thought_id"),
            "thought_id": t.get("thought_id"),
        }
        # judge inputs (text tier only)
        if d["tier"] == "full_traces":
            td = ts.get("task_description") or ""
            tc = ts.get("thought_content") or ""
            ar = t.get("action_rationale") or ""
            tc_s, tc_n1, tc_s2 = A.scrub_text(tc)
            ar_s, ar_n1, ar_s2 = A.scrub_text(ar)
            d["s1_removed"] = ar_n1
            d["s2_hit"] = bool(ar_s2 or tc_s2)
            d["marker_in_tc"] = "[REDACTED-VERDICT-REFERENCE]" in tc_s
            d["prompt"] = A.PROMPT_KIND.format(
                kinds=A.KIND_LINES, task_description=td,
                thought_content=tc_s[:1500], selected_action=d["action"],
                action_rationale=ar_s)
            d["probe_prompt"] = A.PROMPT_PROBE.format(
                task_description=td, thought_content=tc_s[:1500],
                selected_action=d["action"], action_rationale=ar_s)
            d["mc1_prompt"] = A.PROMPT_MC1.format(
                task_description=td, thought_content=tc_s[:1500])
            d["norm_key"] = A.scrub_normalise(d["prompt"])
            d["raw_key"] = d["prompt"]
        rec.append(d)

    by_id = {d["id"]: d for d in rec}

    # ---- frames (sec 4) ------------------------------------------------------
    T = [d for d in rec if d["tier"] == "full_traces"]
    H = [d for d in T if d["entropy_score"] is not None and d["coherence_score"] is not None]
    # sec 4: FRAME-T AND language recoverable AND selected_action clean (not a scrub token)
    TL = [d for d in T if d["lang"] and d["action"] is not None]
    HL = [d for d in H if d["lang"]]
    CP = [d for d in rec if d["lang"] and d["action"] in CLEAN_ACTIONS]
    F4 = [d for d in T if all(d[k] is not None for k in
                              ("entropy_score", "coherence_score", "optveto", "humility"))]
    frames = {"FRAME-T": T, "FRAME-H": H, "FRAME-TL": TL, "FRAME-HL": HL,
              "FRAME-CP": CP, "FRAME-4": F4}

    tiers = collections.Counter(d["tier"] for d in rec)
    got = {f"tier/{k}": v for k, v in tiers.items()}
    for k, v in frames.items():
        got[k] = len(v)
        got["clusters/" + k] = len({d["cluster"] for d in v})
    for k in ("FRAME-T", "FRAME-TL", "FRAME-H"):
        got["distinct/" + k] = len({d["norm_key"] for d in frames[k]})

    mismatches = {k: {"pinned": PINNED[k], "measured": got.get(k)}
                  for k in PINNED if got.get(k) != PINNED[k]}

    # ---- distinct-input blocks on FRAME-T (sec 3.9) --------------------------
    blocks = collections.OrderedDict()
    for d in T:
        blocks.setdefault(d["norm_key"], []).append(d["id"])
    block_list = [{"bid": i, "ids": ids, "prompt": by_id[ids[0]]["prompt"],
                   "probe_prompt": by_id[ids[0]]["probe_prompt"]}
                  for i, (k, ids) in enumerate(blocks.items())]
    for b in block_list:
        for i in b["ids"]:
            by_id[i]["bid"] = b["bid"]

    # ---- language cross-check (sec 4.1) --------------------------------------
    both = [d for d in T if d["lang_regex"] and d["lang_qa"]]
    agree = sum(1 for d in both if d["lang_regex"] == d["lang_qa"])
    dual_ids = [d["id"] for d in both if d["lang_regex"] == d["lang_qa"]]
    zh_ids = [d["id"] for d in T if d["lang"] == "zh"]

    # ---- descriptive tables the results must carry ---------------------------
    desc = {
        "lang/FRAME-T": collections.Counter(d["lang"] for d in T),
        "lang/FRAME-CP": collections.Counter(d["lang"] for d in CP),
        "action/FRAME-T": collections.Counter(d["action"] for d in T),
        "action/FRAME-CP": collections.Counter(d["action"] for d in CP),
        "action_corrupt/FRAME-T": sum(1 for d in T if d["action_corrupt"]),
        "version/FRAME-CP": collections.Counter(d["agent_version"] for d in CP),
        "version/FRAME-TL": collections.Counter(d["agent_version"] for d in TL),
        "days/FRAME-T": collections.Counter(d["day"] for d in T),
        "s1_removed/FRAME-T": collections.Counter(d.get("s1_removed") for d in T),
        "s2_hit/FRAME-T": sum(1 for d in T if d.get("s2_hit")),
        "conflicts/FRAME-TL": collections.Counter(d["has_conflicts"] for d in TL),
        "fragility/FRAME-TL": collections.Counter(d["fragility"] for d in TL),
        "conflicts/FRAME-CP": collections.Counter(d["has_conflicts"] for d in CP),
        "fragility/FRAME-CP": collections.Counter(d["fragility"] for d in CP),
        "lang_dual_confirmed": {"n": len(both), "agree": agree},
        "cluster_lang_pure/FRAME-TL": sum(
            1 for cl, ds in _group(TL).items() if len({d["lang"] for d in ds}) > 1),
        "cluster_lang_pure/FRAME-CP": sum(
            1 for cl, ds in _group(CP).items() if len({d["lang"] for d in ds}) > 1),
        "cluster_ver_pure/FRAME-CP": sum(
            1 for cl, ds in _group(CP).items() if len({d["agent_version"] for d in ds}) > 1),
        "cluster_ver_pure/FRAME-TL": sum(
            1 for cl, ds in _group(TL).items() if len({d["agent_version"] for d in ds}) > 1),
    }

    A.wjson("A0_frames.json", {
        "n_rows": n, "measured": got, "pinned": PINNED, "mismatches": mismatches,
        "frames": {k: [d["id"] for d in v] for k, v in frames.items()},
        "desc": {k: (dict(v) if isinstance(v, collections.Counter) else v)
                 for k, v in desc.items()},
        "mc1_dual_ids": dual_ids, "mc1_zh_ids": zh_ids,
        "n_blocks_frame_t": len(block_list),
    })
    A.wjson("A0_rows.json", rec)
    with open(A.OUT / "A0_blocks.jsonl", "w") as f:
        for b in block_list:
            f.write(json.dumps(b) + "\n")

    print("measured:", json.dumps(got, indent=1))
    print("MISMATCHES:", json.dumps(mismatches, indent=1))
    A.marker("OB1_frames.done", {"measured": got, "mismatches": mismatches})
    return 0


def _group(rows):
    g = {}
    for d in rows:
        g.setdefault(d["cluster"], []).append(d)
    return g


if __name__ == "__main__":
    sys.exit(main())
