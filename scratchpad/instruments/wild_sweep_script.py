#!/usr/bin/env python3
"""N4 — WILD SWEEP of the six v0b instruments, out-of-sample.

Runs empirical/deontic/epistemic/pragmatic/ontological/axiomatic over every
item in four wild/authored streams, compares fired-kind against panel-modal
(BASE condition, 3 judges) where available, and writes full JSON + a readable
markdown report. Pure stdlib, no network.
"""
from __future__ import annotations
import json, sys, collections

sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad/instruments")
import v0b  # noqa: E402

INSTRUMENTS = v0b.INSTRUMENTS  # {"empirical":..., "deontic":..., "epistemic":...,
                                #  "pragmatic":..., "ontological":..., "axiomatic":...}
PLAIN_TO_INTERNAL = v0b.PLAIN_TO_INTERNAL
INTERNAL_TO_PLAIN = {v: k for k, v in PLAIN_TO_INTERNAL.items()}

CORPUS_DIR = "/home/emoore/CIRISOntology/scratchpad/plane_corpus"

STREAMS = [
    # (label, corpus_file, list of judgment files feeding its panel-modal)
    ("eco_corpus", f"{CORPUS_DIR}/eco_corpus.jsonl", [f"{CORPUS_DIR}/eco_judgments.jsonl"]),
    ("eco_osm2", f"{CORPUS_DIR}/eco_osm2.jsonl", [f"{CORPUS_DIR}/eco2_judgments.jsonl"]),
    ("eco_wiki2", f"{CORPUS_DIR}/eco_wiki2.jsonl", [f"{CORPUS_DIR}/eco2_wiki_judgments.jsonl"]),
    ("part_d", f"{CORPUS_DIR}/part_d.jsonl", [f"{CORPUS_DIR}/partd_judgments.jsonl"]),
]

PART_D_TARGETS = {"empirical-report-07", "empirical-report-08",
                   "empirical-report-09", "empirical-report-11"}


def load_jsonl(path):
    out = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def panel_modal(judgment_files):
    """id -> (plain_label_or_None, vote_counter, n_votes, tie_bool).
    BASE condition only, kind field, plain names; ties -> None (excluded),
    labels not in PLAIN_TO_INTERNAL (e.g. stray/NO FIT) do not vote."""
    votes = collections.defaultdict(collections.Counter)
    for jf in judgment_files:
        for d in load_jsonl(jf):
            if d.get("condition") != "BASE":
                continue
            lab = d.get("kind")
            votes[d["id"]][lab] += 1  # count everything cast, including non-voting labels below
    modal = {}
    for id_, c in votes.items():
        valid = collections.Counter({k: n for k, n in c.items() if k in PLAIN_TO_INTERNAL})
        total_cast = sum(c.values())
        if not valid:
            modal[id_] = {"modal": None, "votes": dict(c), "n_cast": total_cast, "tie": False,
                          "note": "no vote fell inside the 12-kind taxonomy"}
            continue
        top = valid.most_common(2)
        tie = len(top) > 1 and top[0][1] == top[1][1]
        modal[id_] = {"modal": None if tie else top[0][0], "votes": dict(c),
                      "n_cast": total_cast, "tie": tie}
    return modal


def run_stream(label, corpus_path, judgment_files):
    items = load_jsonl(corpus_path)
    modal = panel_modal(judgment_files)
    per_item = []
    fire_counts = collections.Counter()
    axiomatic_firings = []
    agreement = {iname: collections.Counter() for iname in INSTRUMENTS}
    # agreement[iname]["agree"/"disagree"/"no_panel"] tallies, keyed against
    # whether THIS instrument's plain kind matches the panel modal.
    inst_plain = {iname: INTERNAL_TO_PLAIN[iname] for iname in INSTRUMENTS}

    for d in items:
        before, after = d["before"], d["after"]
        readings = {}
        for iname, fn in INSTRUMENTS.items():
            try:
                rd = fn(before, after)
            except Exception as e:  # pure-compute, should never happen; record if it does
                rd = {"kind": iname, "fired": False, "evidence": {},
                      "refused": True, "reason": f"EXCEPTION: {e!r}"}
            readings[iname] = rd
            if rd["fired"]:
                fire_counts[iname] += 1
                if iname == "axiomatic":
                    ev = rd["evidence"]
                    axiomatic_firings.append({
                        "id": d["id"], "stream": label,
                        "ripple": ev.get("ripple"),
                        "ripple_mentions": ev.get("ripple_mentions"),
                        "ripple_inherited": ev.get("ripple_inherited"),
                        "threshold": ev.get("threshold"),
                        "definitional": ev.get("definitional"),
                        "definitional_why": ev.get("definitional_why"),
                        "anchors": ev.get("anchors"),
                        "mode": ev.get("mode"),
                        "reason": rd["reason"],
                        "kind_target": d.get("kind_target"),
                    })

        pm = modal.get(d["id"])
        fired_plain = sorted(inst_plain[iname] for iname, rd in readings.items() if rd["fired"])
        for iname in INSTRUMENTS:
            fired = readings[iname]["fired"]
            plain = inst_plain[iname]
            if pm is None or pm.get("modal") is None:
                agreement[iname]["no_panel_or_tie"] += 1
            else:
                panel_lab = pm["modal"]
                if fired and panel_lab == plain:
                    agreement[iname]["true_positive"] += 1
                elif fired and panel_lab != plain:
                    agreement[iname]["false_positive"] += 1
                elif (not fired) and panel_lab == plain:
                    agreement[iname]["false_negative"] += 1
                else:
                    agreement[iname]["true_negative"] += 1

        per_item.append({
            "id": d["id"], "stream": label,
            "kind_target": d.get("kind_target"),
            "domain": d.get("domain"), "difficulty": d.get("difficulty"),
            "panel_modal": pm,
            "fired_instruments": fired_plain,
            "readings": readings,
        })

    # false-fire source breakdown: when instrument fires but panel modal disagrees,
    # which plain kind did the panel actually give it (diagnostic, matches v0b's
    # own bakeoff "top false-fire sources" column)
    false_fire_sources = {iname: collections.Counter() for iname in INSTRUMENTS}
    for it in per_item:
        pm = it["panel_modal"]
        if not pm or not pm.get("modal"):
            continue
        for iname in INSTRUMENTS:
            fired = it["readings"][iname]["fired"]
            plain = inst_plain[iname]
            if fired and pm["modal"] != plain:
                false_fire_sources[iname][pm["modal"]] += 1

    return {
        "label": label, "n_items": len(items),
        "fire_counts": dict(fire_counts),
        "fire_rate_pct": {k: round(100 * v / len(items), 1) for k, v in fire_counts.items()},
        "axiomatic_firings": axiomatic_firings,
        "agreement": {k: dict(v) for k, v in agreement.items()},
        "false_fire_sources": {k: dict(v) for k, v in false_fire_sources.items() if v},
        "items": per_item,
    }


def main():
    results = {}
    for label, corpus_path, jfiles in STREAMS:
        results[label] = run_stream(label, corpus_path, jfiles)

    # ---- overall axiomatic wild verdict
    total_items = sum(r["n_items"] for r in results.values())
    total_axiomatic_fires = sum(r["fire_counts"].get("axiomatic", 0) for r in results.values())
    wild_only_items = sum(r["n_items"] for k, r in results.items() if k != "part_d")
    wild_only_axiomatic = sum(r["fire_counts"].get("axiomatic", 0)
                              for k, r in results.items() if k != "part_d")

    # ---- part-D four absorbed items readout
    part_d_readout = {}
    part_d_items = {it["id"]: it for it in results["part_d"]["items"]}
    for tgt in sorted(PART_D_TARGETS):
        it = part_d_items.get(tgt)
        if it is None:
            part_d_readout[tgt] = {"error": "id not found in part_d.jsonl"}
            continue
        part_d_readout[tgt] = {
            "kind_target": it["kind_target"],
            "panel_modal": it["panel_modal"],
            "fired_instruments": it["fired_instruments"],
            "per_instrument_reason": {iname: it["readings"][iname]["reason"]
                                      for iname in INSTRUMENTS},
            "axiomatic_evidence": it["readings"]["axiomatic"]["evidence"],
            "empirical_evidence": it["readings"]["empirical"]["evidence"],
        }

    summary = {
        "staked_expectation": (
            "Wild Premises (axiomatic) should be RARE. The axiomatic instrument fires "
            "only on the conjunction definition-position AND ripple>=threshold. A high "
            "wild fire rate (esp. on prose news/wiki/OSM/fedreg text with no genuine "
            "definitional apparatus) would indicate the conjunction overfits the "
            "authored corpus; a low rate concentrated on config/code definition "
            "changes (where ripple is cheap to compute exactly) with prose staying "
            "near-silent would indicate the heuristic generalizes."
        ),
        "total_items": total_items,
        "total_axiomatic_fires": total_axiomatic_fires,
        "wild_streams_items": wild_only_items,
        "wild_streams_axiomatic_fires": wild_only_axiomatic,
        "wild_axiomatic_fire_rate": (wild_only_axiomatic / wild_only_items) if wild_only_items else None,
        "part_d_axiomatic_fires": results["part_d"]["fire_counts"].get("axiomatic", 0),
        "part_d_items": results["part_d"]["n_items"],
    }

    out = {"summary": summary, "streams": results, "part_d_target_readout": part_d_readout}

    out_json = "/home/emoore/CIRISOntology/scratchpad/instruments/wild_sweep.json"
    with open(out_json, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"wrote {out_json}")

    return out


if __name__ == "__main__":
    main()
