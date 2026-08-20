"""OB5 — the adversarial leak probe's CALLS. sec 6.5. OUTCOME-BLIND.

The panel is turned against the sec 6.3 scrub: same three models, same scrubbed inputs, same
distinct-input caching, one different question. The probe's SCORE is computed here (panel-mean
confidence signed by `overridden`); its AUC against the true override — gate V7b — is an
outcome-crossing computation and is discharged in the analysis stage (AMENDMENTS A0-NOTE-1).
"""
from __future__ import annotations
import collections, json, sys
sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad/a0run/src")
import a0lib as A
import a0judge as J


def main():
    blocks = [json.loads(l) for l in open(A.OUT / "A0_blocks.jsonl")]
    jobs = [{"model": m, "text": b["probe_prompt"], "bid": b["bid"]}
            for b in blocks for m in J.MODELS]
    recs, stats = J.run_jobs(jobs, tag="PROBE", workers=16, progress_every=200)
    if stats.get("aborted"):
        return 3

    per = collections.defaultdict(dict)
    cues = collections.defaultdict(list)
    for r in recs:
        j = J.parse_json(r.get("raw")) or {}
        ov, cf = j.get("overridden"), j.get("confidence")
        if isinstance(ov, str):
            ov = ov.strip().lower() in ("true", "yes", "1")
        try:
            cf = float(cf)
        except (TypeError, ValueError):
            cf = None
        if isinstance(ov, bool) and cf is not None:
            per[r["bid"]][r["model"]] = (1.0 if ov else -1.0) * max(0.0, min(1.0, cf))
            if ov and j.get("cue"):
                cues[r["bid"]].append(str(j["cue"])[:200])

    out = []
    for b in blocks:
        v = [per[b["bid"]].get(m) for m in J.MODELS]
        v = [x for x in v if x is not None]
        out.append({"bid": b["bid"], "n_models": len(v),
                    "score": (sum(v) / len(v)) if v else None,
                    "cues": cues.get(b["bid"], [])})
    A.wjson("A0_probe_scores.json",
            {"n_blocks": len(out), "parsed_full": sum(1 for r in out if r["n_models"] == 3),
             "scores": out, "spend": stats})
    print(f"probe: {len(out)} blocks, {sum(1 for r in out if r['n_models']==3)} with all "
          f"three models parsed; spend {stats}")
    A.marker("OB5_probe.done", {"n_blocks": len(out), "spend": stats})
    return 0


if __name__ == "__main__":
    sys.exit(main())
