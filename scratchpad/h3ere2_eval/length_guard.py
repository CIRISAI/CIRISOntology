#!/usr/bin/env python3
"""JUDGE_PROTOCOL section 5's length guard, as SPECIFIED rather than as approximated.

The protocol says: "Fit `choice ~ length_diff + arm` (logistic). If `length_diff` is
significant and `arm` is not, the comparison is reported as length-confounded and a
length-matched re-run is required before any verdict."

analyze.py only ever computed the MARGINAL "did the longer response win", never the joint
fit, so the conjunction the protocol actually stated has never been evaluated for any judge.
This runs it, plus a non-parametric length-matched subset that needs no model at all.

Coding, per judgment (one row per order, so each pair contributes two rows):
  y  = 1 if the judge picked slot 1, else 0
  x1 = (len1 - len2) / 1000, the length difference in the direction of the choice
  x2 = +1 if slot 1 holds the treatment arm C, -1 if slot 2 does
A positive x1 coefficient is a length preference; a positive x2 coefficient is a preference
for C that is NOT explained by length. Both are on the same scale (log-odds).

Usage: length_guard.py <pairs.jsonl> [label]
"""
import json, sys, collections, math


def logistic_fit(X, y, iters=200, ridge=1e-6):
    """Newton-Raphson. X includes the intercept column. Returns (beta, se)."""
    n, k = len(X), len(X[0])
    b = [0.0] * k
    for _ in range(iters):
        g = [0.0] * k
        H = [[ridge if i == j else 0.0 for j in range(k)] for i in range(k)]
        for xi, yi in zip(X, y):
            z = sum(bj * xj for bj, xj in zip(b, xi))
            p = 1.0 / (1.0 + math.exp(-max(-30.0, min(30.0, z))))
            w = p * (1.0 - p)
            for i in range(k):
                g[i] += (yi - p) * xi[i]
                for j in range(k):
                    H[i][j] += w * xi[i] * xi[j]
        # solve H d = g by Gauss-Jordan, carrying the inverse for standard errors
        A = [row[:] + [1.0 if i == j else 0.0 for j in range(k)] for i, row in enumerate(H)]
        for c in range(k):
            piv = max(range(c, k), key=lambda r: abs(A[r][c]))
            if abs(A[piv][c]) < 1e-12:
                return b, [float("nan")] * k
            A[c], A[piv] = A[piv], A[c]
            pv = A[c][c]
            A[c] = [v / pv for v in A[c]]
            for r in range(k):
                if r != c and A[r][c]:
                    f = A[r][c]
                    A[r] = [vr - f * vc for vr, vc in zip(A[r], A[c])]
        inv = [row[k:] for row in A]
        d = [sum(inv[i][j] * g[j] for j in range(k)) for i in range(k)]
        b = [bi + di for bi, di in zip(b, d)]
        if max(abs(di) for di in d) < 1e-9:
            break
    se = [math.sqrt(inv[i][i]) if inv[i][i] > 0 else float("nan") for i in range(k)]
    return b, se


def norm_p(z):
    return math.erfc(abs(z) / math.sqrt(2.0))


def sign_test(w, l):
    from math import comb
    n = w + l
    if n == 0:
        return 1.0
    return min(1.0, sum(comb(n, i) for i in range(0, min(w, l) + 1)) * 2 / 2 ** n)


def main(path, label=""):
    rows = [json.loads(l) for l in open(path)]
    pairs = [r for r in rows if r.get("mode") == "pair"]
    print(f"===== {label or path} =====")

    for cmp_ in ("CvB", "CvA"):
        sub = [r for r in pairs if r["cmp"] == cmp_ and r.get("pick") in ("1", "2")]
        if not sub:
            continue
        other = cmp_[-1]
        X, y = [], []
        for r in sub:
            # order 0 -> slot 1 holds C (judge.py builds (x, y) as (lo, hi) = (C, other))
            c_in_slot1 = (r["order"] == 0)
            X.append([1.0, (r["len1"] - r["len2"]) / 1000.0, 1.0 if c_in_slot1 else -1.0])
            y.append(1.0 if r["pick"] == "1" else 0.0)
        b, se = logistic_fit(X, y)
        names = ["intercept", "length_diff(/1k chars)", "arm(C in slot 1)"]
        print(f"  --- {cmp_[0]} vs {other}: logistic choice ~ length_diff + arm  (n={len(sub)} judgments) ---")
        for nm, bi, si in zip(names, b, se):
            z = bi / si if si and si == si else float("nan")
            print(f"      {nm:24s} beta={bi:+8.3f}  se={si:6.3f}  z={z:+6.2f}  p={norm_p(z):.4g}")
        lp, ap = norm_p(b[1] / se[1]), norm_p(b[2] / se[2])
        if lp < 0.05 and ap >= 0.05:
            print("      -> PROTOCOL SECTION 5 FIRES: length significant, arm NOT. "
                  "LENGTH-CONFOUNDED; a length-matched re-run is required before any verdict.")
        elif lp < 0.05 and ap < 0.05:
            print("      -> length IS significant but arm SURVIVES it. Not the protocol's "
                  "confound condition (which is conjunctive), but the length preference is real "
                  "and must be reported alongside the verdict.")
        else:
            print("      -> no significant length preference.")

        # Non-parametric, model-free: order-balanced outcome restricted to pairs where the
        # treatment arm C is the SHORTER response. If C still wins there, length is not doing it.
        byitem = collections.defaultdict(dict)
        for r in pairs:
            if r["cmp"] == cmp_:
                byitem[r["id"]][r["order"]] = r
        buckets = {"C shorter": [0, 0], "C longer": [0, 0]}
        for iid, d in byitem.items():
            if 0 not in d or 1 not in d:
                continue
            w0, w1 = d[0]["winner"], d[1]["winner"]
            if w0 is None or w1 is None or w0 != w1:
                continue
            # in order 0, slot1 = C, slot2 = other
            c_len, o_len = d[0]["len1"], d[0]["len2"]
            k = "C shorter" if c_len < o_len else "C longer"
            buckets[k][0] += (w0 == "C")
            buckets[k][1] += 1
        print(f"  --- {cmp_[0]} vs {other}: order-balanced decisive pairs, split by which arm is longer ---")
        for k, (c, n) in buckets.items():
            if n:
                print(f"      {k:10s} n={n:3d}  C wins {c:3d}  rate={c/n:.3f}  p={sign_test(c, n-c):.4f}")
            else:
                print(f"      {k:10s} n=  0")
        print()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "")
