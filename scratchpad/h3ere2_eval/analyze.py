#!/usr/bin/env python3
"""h3ere2 verdict. Order-balanced scoring + paired sign test + length confound check."""
import json, sys, collections, math
from math import comb

def sign_test(w, l):
    n = w + l
    if n == 0: return 1.0
    p = sum(comb(n, i) for i in range(0, min(w, l) + 1)) * 2 / 2**n
    return min(1.0, p)

def main(judgefile, respfile=None):
    rows = [json.loads(l) for l in open(judgefile)]
    pairs = [r for r in rows if r.get("mode") == "pair"]
    print(f"judgments: {len(pairs)}\n")

    for cmp_ in ("CvB", "CvA"):
        sub = collections.defaultdict(dict)
        for r in pairs:
            if r["cmp"] == cmp_: sub[r["id"]][r["order"]] = r
        wins = collections.Counter(); flips = 0
        per_scr = collections.defaultdict(lambda: [0, 0])
        for iid, d in sub.items():
            if 0 not in d or 1 not in d: continue
            w0, w1 = d[0]["winner"], d[1]["winner"]
            if w0 is None or w1 is None: continue
            if w0 != w1:
                flips += 1; continue          # order-disagreement -> excluded, counted
            wins[w0] += 1
            s = d[0].get("scramble_id")
            if s is not None:
                per_scr[s][0] += (w0 == "C"); per_scr[s][1] += 1
        C = wins["C"]; O = sum(v for k, v in wins.items() if k != "C")
        dec = C + O; tot = dec + flips
        if tot == 0: continue
        rate = C / dec if dec else float("nan")
        p = sign_test(C, O)
        other = cmp_[-1]
        print(f"=== {cmp_[0]} vs {other} ===")
        print(f"  decisive={dec}  flips={flips} ({flips/tot:.3f} of {tot})")
        print(f"  C wins {C}, {other} wins {O}   ->  C win rate = {rate:.3f}")
        print(f"  paired sign test p = {p:.4f}")
        thr = 0.5 + 1.96 * math.sqrt(0.25 / dec) if dec else float("nan")
        print(f"  significance threshold at this n: {thr:.3f}")
        if cmp_ == "CvB":
            if p < 0.05 and rate > 0.5:
                print("  VERDICT: SUPPORTED - coupling contributes to response quality")
            else:
                print("  VERDICT: NOT SUPPORTED at n. Scope: rules out a LARGE effect")
                print("           (true win rate > ~0.61); CANNOT exclude a modest one")
                print("           (< 0.58 would need ~300-800 items). Does NOT falsify the")
                print("           engine, taxonomy, or classifier - only this pipeline's")
                print("           use of them for response generation.")
            if per_scr:
                print("  per-scramble C win rate:",
                      {k: round(v[0]/v[1], 2) for k, v in sorted(per_scr.items()) if v[1]})
        print()

    # ---- ADDENDUM J1: pre-registered stratified analysis --------------------
    # surface is near-collinear with stream, so a pooled win could be a stream effect.
    for key in ("stream", "surface"):
        strata = collections.defaultdict(lambda: collections.defaultdict(dict))
        for r in pairs:
            if r["cmp"] != "CvB": continue
            strata[r.get(key)][r["id"]][r["order"]] = r
        if len(strata) <= 1: continue
        print(f"STRATIFIED BY {key.upper()} (diagnostic, NOT confirmatory -- strata are underpowered):")
        for k, items in sorted(strata.items(), key=lambda x: str(x[0])):
            wins = collections.Counter(); fl = 0
            for iid, dd in items.items():
                if 0 not in dd or 1 not in dd: continue
                w0, w1 = dd[0]["winner"], dd[1]["winner"]
                if w0 is None or w1 is None: continue
                if w0 != w1: fl += 1; continue
                wins[w0] += 1
            C = wins["C"]; O = wins["B"]; dec = C + O
            if not dec: continue
            thr = 0.5 + 1.96 * math.sqrt(0.25 / dec)
            print(f"   {str(k):10s} decisive={dec:3d} flips={fl:3d}  C={C:3d} B={O:3d}  "
                  f"rate={C/dec:.3f}  p={sign_test(C,O):.4f}  (80%-power needs ~{0.5+2.8*math.sqrt(0.25/dec):.2f})")
        print()

    # length confound: does the longer response win, independent of arm?
    longer_won = tot_len = 0
    for r in pairs:
        if r.get("pick") not in ("1", "2"): continue
        if r["len1"] == r["len2"]: continue
        tot_len += 1
        longer = "1" if r["len1"] > r["len2"] else "2"
        longer_won += (r["pick"] == longer)
    if tot_len:
        lr = longer_won / tot_len
        p = sign_test(longer_won, tot_len - longer_won)
        print(f"LENGTH CONFOUND: judge picked the LONGER response {lr:.3f} of the time "
              f"(n={tot_len}, p={p:.4f})")
        print("  -> " + ("no length preference detected" if p >= 0.05 else
              "LENGTH-CONFOUNDED: judge prefers longer answers; a length-matched re-run is "
              "required before any verdict is issued"))

    if respfile:
        rows_r = [json.loads(l) for l in open(respfile)]
        print("\nPER-ARM (compute, verbosity, and PATH DEGENERACY -- prereg failure modes 1-3):")
        for a in sorted({r["arm"] for r in rows_r}):
            sub = [r for r in rows_r if r["arm"] == a]
            n = len(sub)
            chars = sum(r.get("resp_chars") or len(r.get("response") or "") for r in sub) / n
            ms = sum(r.get("gen_ms") or 0 for r in sub) / n
            toks = sum(r.get("gen_tokens") or 0 for r in sub) / n
            paths = {tuple(r["path"]) if isinstance(r.get("path"), list) else r.get("path")
                     for r in sub if r.get("path")}
            plens = sorted({r.get("path_len") for r in sub})
            print(f"  {a}: n={n:4d} chars={chars:6.0f} tokens={toks:5.0f} gen_ms={ms:7.0f} "
                  f"path_len={plens} DISTINCT PATHS={len(paths) if paths else 0}")
        cnt = collections.Counter(r["arm"] for r in rows_r)
        cpaths = {r["path"] for r in rows_r if r["arm"] == "C" and r.get("path")}
        if len(cpaths) <= 2:
            print(f"\n  ** DEGENERACY WARNING: arm C uses only {len(cpaths)} distinct path(s) across "
                  f"{cnt.get('C',0)} items. The treatment has that many levels, NOT one per item.")
            print("     Scope any verdict to 'fixed propagation order(s)', never to per-item reasoning.")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
