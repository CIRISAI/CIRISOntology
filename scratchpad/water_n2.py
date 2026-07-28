#!/usr/bin/env python3
"""N2, THE IDEAL-GAS CONTROL, MEASURED AS A DISTRIBUTION AND NOT AS ONE DRAW.

WHY THIS FILE EXISTS, recorded rather than smoothed over.  The arm A docimasia
first measured the ideal-gas share at four sample sizes -- ONE realisation each
-- saw it fail to fall as 1/N, and provisionally read that as a PEDESTAL: share
minted by template selection plus the coordination filter, which would not fall
with N and would have fired `WATER_PREREG.md` sec 8 outcome (j).  The mechanism
check (W7c) then read the SAME template at the SAME sample size and got
6.4e-05 against 2.0e-04, p = 0.26 against p = 0.045.  Two draws, a factor of
three apart.

That is the campaign's own memory firing on the campaign: the share null is
chi-squared-shaped, so a single draw is not a measurement of it, and
`GATES.md` (Dalitz D7) keeps the anchor -- a single draw of a chi-squared-shaped
null read 2.9e-4 and would have fired a kill; over 200 draws it was flat.

THE TEST DONE PROPERLY.  At each sample size, M INDEPENDENT ideal-gas ensembles
are drawn and the share of each is computed, giving the DISTRIBUTION of the N2
reading.  Beside it, and on the SAME positions, the N1a label floor: labels drawn
iid Bernoulli at the ensemble's own composition.  N1a is an exact product state,
so `Core/Valve.lean: valve_from_nothing` -- hypotheses checked at source: three
`IsKernel` kernels, three `IsProb` cell states, input `prod3 p1 p2 p3` -- makes
its true share exactly zero.

THE QUESTION, and the two answers it can give:

  * if the N2 distribution sits ON the N1a distribution, then template selection
    and the coordination filter mint NOTHING, the pre-registered floor of record
    stands, and outcome (j) does not fire;
  * if N2 sits systematically ABOVE N1a and the gap does not fall with N, the gap
    is a genuine minting pedestal and must be subtracted from every reading.

Polarity is declared before the run in both directions, per sec 5.5 G-POL.
"""
import argparse
import json
import sys

import numpy as np

sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")
import glass_share as GS   # noqa: E402
import water_arm_a as WA   # noqa: E402


def one_ensemble(n, L, nconf, tmpl, tol, rcut, rng):
    """One ideal-gas ensemble: its N2 share, its N1a floor draw, its N_tri."""
    tab = np.zeros(8)
    tab_iid = np.zeros(8)
    ntri = 0
    labs = []
    for _ in range(nconf):
        pos = rng.random((n, 3)) * L
        nb = WA.coordination(pos, L, rcut)
        lab = (nb >= 5).astype(np.int8)
        labs.append(lab.mean())
        tri = GS.triangles(pos, L, tmpl, tol, rng)
        if not len(tri):
            continue
        ntri += len(tri)
        tab += GS.table_from_triples(tri, lab).ravel()
        li = (rng.random(n) < lab.mean()).astype(np.int8)
        tab_iid += GS.table_from_triples(tri, li).ravel()
    if tab.sum() == 0:
        return None
    return (float(GS.share_2x2x2(tab.reshape(2, 2, 2))),
            float(GS.share_2x2x2(tab_iid.reshape(2, 2, 2))),
            ntri, float(np.mean(labs)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=2000)
    ap.add_argument("--L", type=float, default=39.1507)
    ap.add_argument("--nconf", default="5,12,25,50")
    ap.add_argument("--m", type=int, default=40)
    ap.add_argument("--tmpl", default="2.86,2.86,4.50")
    ap.add_argument("--seed", type=int, default=20260727)
    ap.add_argument("--out", default="/home/emoore/CIRISOntology/scratchpad/water_n2.json")
    a = ap.parse_args()
    tmpl = tuple(float(x) for x in a.tmpl.split(","))
    rng = np.random.default_rng(a.seed)
    res = {"template": tmpl, "n": a.n, "L": a.L, "m": a.m, "rows": []}
    print("N2 ideal-gas control as a DISTRIBUTION.  template=%s  M=%d ensembles each\n"
          % (tmpl, a.m), flush=True)
    print("%6s %9s %5s | %11s %11s %11s | %11s %11s | %8s %7s"
          % ("nconf", "N_tri", "p1", "N2 med", "N2 p90", "N2 p99",
             "N1a med", "N1a p99", "med rat", "p(N2>N1a)"), flush=True)
    for nconf in [int(x) for x in a.nconf.split(",")]:
        m = a.m if nconf <= 25 else max(12, a.m // 3)
        rows = [one_ensemble(a.n, a.L, nconf, tmpl, 0.25, WA.RCUT, rng)
                for _ in range(m)]
        rows = [r for r in rows if r]
        s2 = np.array([r[0] for r in rows])
        s1 = np.array([r[1] for r in rows])
        ntri = float(np.mean([r[2] for r in rows]))
        p1 = float(np.mean([r[3] for r in rows]))
        # exact rank test: how often does an independent N1a draw beat an N2 draw
        pgt = float((s2[:, None] > s1[None, :]).mean())
        row = dict(nconf=nconf, m=len(rows), N_tri=ntri, p1=p1,
                   n2_median=float(np.median(s2)), n2_p90=float(np.percentile(s2, 90)),
                   n2_p99=float(np.percentile(s2, 99)),
                   n1a_median=float(np.median(s1)), n1a_p99=float(np.percentile(s1, 99)),
                   median_ratio=float(np.median(s2) / max(np.median(s1), 1e-300)),
                   frac_n2_above_n1a=pgt,
                   n2_times_Ntri=float(np.median(s2) * ntri),
                   n1a_times_Ntri=float(np.median(s1) * ntri))
        res["rows"].append(row)
        print("%6d %9.0f %5.3f | %11.4e %11.4e %11.4e | %11.4e %11.4e | %8.3f %7.3f"
              % (nconf, ntri, p1, row["n2_median"], row["n2_p90"], row["n2_p99"],
                 row["n1a_median"], row["n1a_p99"], row["median_ratio"], pgt),
              flush=True)
    r = res["rows"]
    sN = [x["n2_times_Ntri"] for x in r]
    slope = float(np.polyfit(np.log([x["N_tri"] for x in r]),
                             np.log([max(x["n2_median"], 1e-30) for x in r]), 1)[0])
    res["n2_median_times_Ntri"] = sN
    res["n2_loglog_slope"] = slope
    res["verdict"] = ("N2 AT FLOOR — no pedestal" if slope < -0.7 and
                      max(x["median_ratio"] for x in r) < 3.0
                      else "N2 ABOVE FLOOR — pedestal, outcome (j) territory")
    print("\n  N2 median x N_tri (flat => a 1/N floor): %s"
          % ["%.3f" % x for x in sN], flush=True)
    print("  N2 median log-log slope in N_tri: %+.3f  (a floor gives -1)" % slope, flush=True)
    print("\n  VERDICT: %s" % res["verdict"], flush=True)
    json.dump(res, open(a.out, "w"), indent=1)
    print("\nwrote", a.out, flush=True)


if __name__ == "__main__":
    main()
