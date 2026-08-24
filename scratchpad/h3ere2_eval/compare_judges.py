#!/usr/bin/env python3
"""Inter-judge agreement for the K2 split-verdict provision (JUDGE_PROTOCOL section 3:
"Inter-judge agreement is reported. A verdict claimed by only one judge is reported as
SPLIT, not as a win.")

Written BEFORE any second-judge calibration number was read. Does not modify or re-score
anything: it reads two `judge.py pairs` outputs and applies the SAME order-balanced rule
analyze.py applies, then compares the two judges item by item.

Usage: compare_judges.py <primary_pairs.jsonl> <second_pairs.jsonl> [label1] [label2]
"""
import json, sys, collections
from math import comb


def sign_test(w, l):
    n = w + l
    if n == 0:
        return 1.0
    return min(1.0, sum(comb(n, i) for i in range(0, min(w, l) + 1)) * 2 / 2 ** n)


def decisions(path, cmp_):
    """Order-balanced per-item outcome, identical to analyze.py's rule:
    a pair is decisive only when the SAME arm wins in BOTH orders; otherwise it is a flip."""
    sub = collections.defaultdict(dict)
    for l in open(path):
        r = json.loads(l)
        if r.get("mode") == "pair" and r["cmp"] == cmp_:
            sub[r["id"]][r["order"]] = r
    out = {}
    for iid, d in sub.items():
        if 0 not in d or 1 not in d:
            continue
        w0, w1 = d[0]["winner"], d[1]["winner"]
        if w0 is None or w1 is None:
            continue
        out[iid] = w0 if w0 == w1 else "FLIP"
    return out


def kappa(pairs):
    """Cohen's kappa over whatever category set actually occurs."""
    n = len(pairs)
    if not n:
        return float("nan")
    cats = sorted({x for p in pairs for x in p})
    obs = sum(a == b for a, b in pairs) / n
    m1 = collections.Counter(a for a, _ in pairs)
    m2 = collections.Counter(b for _, b in pairs)
    exp = sum((m1[c] / n) * (m2[c] / n) for c in cats)
    return (obs - exp) / (1 - exp) if exp < 1 else float("nan")


def rate(dec):
    C = sum(v == "C" for v in dec.values())
    O = sum(v not in ("C", "FLIP") for v in dec.values())
    F = sum(v == "FLIP" for v in dec.values())
    return C, O, F


def main(f1, f2, n1="primary", n2="second"):
    for cmp_ in ("CvB", "CvA"):
        d1, d2 = decisions(f1, cmp_), decisions(f2, cmp_)
        both = sorted(set(d1) & set(d2))
        other = cmp_[-1]
        print(f"=== {cmp_[0]} vs {other} ===")
        for nm, d in ((n1, d1), (n2, d2)):
            C, O, F = rate(d)
            dec = C + O
            r = C / dec if dec else float("nan")
            print(f"  {nm:>10s}: decisive={dec:3d} flips={F:3d}  C={C:3d} {other}={O:3d}  "
                  f"rate={r:.3f}  p={sign_test(C, O):.4f}")

        # 3-category agreement (C / other / FLIP) over every item BOTH judges scored
        p3 = [(d1[i], d2[i]) for i in both]
        a3 = sum(a == b for a, b in p3) / len(p3) if p3 else float("nan")
        # 2-category agreement, restricted to items DECISIVE FOR BOTH judges
        p2 = [(a, b) for a, b in p3 if a != "FLIP" and b != "FLIP"]
        a2 = sum(a == b for a, b in p2) / len(p2) if p2 else float("nan")
        print(f"  inter-judge, 3-way (C/{other}/FLIP), n={len(p3)}: "
              f"raw={a3:.3f}  kappa={kappa(p3):.3f}")
        print(f"  inter-judge, both-decisive only,  n={len(p2)}: "
              f"raw={a2:.3f}  kappa={kappa(p2):.3f}")

        # where they part company
        cm = collections.Counter(p3)
        print("  confusion (primary -> second):",
              {f"{a}->{b}": c for (a, b), c in sorted(cm.items(), key=lambda x: -x[1])})
        print()


if __name__ == "__main__":
    main(*sys.argv[1:])
