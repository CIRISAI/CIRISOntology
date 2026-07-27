#!/usr/bin/env python3
"""WATER_AMENDMENT_1 A1: the test that refuted this campaign's own mechanism claim.

WHAT WAS CLAIMED.  `WATER_PREREG.md` sec 5.3 said the LP headroom collapses "when
the label composition becomes lopsided", and tied it to the ceiling collapse of
sec 5.4 as the same mechanism.

WHAT REFUTES IT.  The glass campaign measured, on 44 of its own real cells,
corr(log min(p,1-p), log headroom) = +0.209 -- weak and the wrong sign -- and
diagnosed near-emptiness of a CELL from geometry x species exclusion instead.
This script runs the same test on THIS campaign's own stage-0 data, which was
already on disk when the claim was written, and it refutes the claim harder:
lopsidedness correlates at -0.099 while min-cell fraction correlates at +0.863.

The decisive pair is inside one run at ONE composition (p1 = 0.091): the
tetrahedral template has min-cell fraction 1.08e-3 and headroom 0.0222, while
equilateral_nn has 5.00e-2 and 0.6555.  Same composition, 30x the headroom.

Reads only the committed stage-0 JSONs.  Computes no share and touches no water.
"""
import json

import numpy as np

RUNS = [("water_feas_hdl.json", "hdl_s35_t15"),
        ("water_feas_hdl_t25.json", "hdl_s35_t25"),
        ("water_feas_ldl_t25.json", "ldl_s35_t25"),
        ("water_feas_hdl_s20.json", "hdl_s20_t25")]
BASE = "/home/emoore/CIRISOntology/scratchpad/"


def collect():
    rows = []
    for fn, tag in RUNS:
        r = json.load(open(BASE + fn))
        p1 = r["p_hdl"]
        for k, v in r["templates"].items():
            o = v.get("occupancy")
            if not o:
                continue
            tab = np.array(o["table"], dtype=float)
            tot = tab.sum()
            if tot <= 0:
                continue
            # the product-model minimum cell: what the SINGLE-slot marginals alone
            # force the rarest cell to be.  This is the channel through which a
            # rare label starves a table, and it is what couples composition to
            # starvation without composition being the proximate driver.
            p = tab.reshape(2, 2, 2) / tot
            m = [p.sum(axis=tuple(j for j in range(3) if j != i)) for i in range(3)]
            rows.append(dict(
                tag=tag, tmpl=k, p1=p1, lop=min(p1, 1.0 - p1),
                head=v["headroom"], ceil=v["ceilings"]["ceil_min"],
                minfrac=tab.min() / tot,
                prodmin=float(np.einsum("i,j,k->ijk", *m).min()),
                mincell=tab.min(), tot=tot))
    return rows


def main():
    rows = collect()
    hdr = ("%-13s %-14s %6s %6s %8s %8s %9s %9s %8s"
           % ("run", "template", "p1", "lop", "headroom", "ceil_min",
              "minfrac", "prodmin", "mincell"))
    print(hdr)
    for d in rows:
        print("%-13s %-14s %6.3f %6.3f %8.4f %8.4f %9.2e %9.2e %8.0f"
              % (d["tag"], d["tmpl"], d["p1"], d["lop"], d["head"], d["ceil"],
                 d["minfrac"], d["prodmin"], d["mincell"]))

    L = np.log
    lop = L([d["lop"] for d in rows])
    head = L([max(d["head"], 1e-9) for d in rows])
    mf = L([max(d["minfrac"], 1e-12) for d in rows])
    pm = L([max(d["prodmin"], 1e-12) for d in rows])
    ceil = L([max(d["ceil"], 1e-9) for d in rows])

    def c(a, b):
        return float(np.corrcoef(a, b)[0, 1])

    print()
    print("n=%d  corr(log lopsidedness, log headroom)      = %+.3f"
          % (len(rows), c(lop, head)))
    print("      corr(log min-cell FRACTION, log headroom)  = %+.3f" % c(mf, head))
    print("      corr(log product-model min, log headroom)  = %+.3f" % c(pm, head))
    print("      corr(log lopsidedness, log ceil_min)       = %+.3f" % c(lop, ceil))
    print("      corr(log min-cell FRACTION, log ceil_min)  = %+.3f" % c(mf, ceil))
    print()
    print("VERDICT: lopsidedness does NOT drive the headroom collapse on this")
    print("campaign's own stage-0 data.  Cell starvation does.  The prereg's")
    print("mechanism claim is retracted in WATER_AMENDMENT_1.md sec A1; the gate")
    print("rules it was used to justify are unchanged, because P7 was stated as a")
    print("RATIO and never depended on the mechanism.")

    # the two-cell counter-example, printed explicitly because it is the argument
    print()
    print("THE FALSIFYING PAIR (one run, ONE composition, two templates):")
    for d in rows:
        if d["tag"] == "ldl_s35_t25" and d["tmpl"] in ("tetrahedral", "equilateral_nn"):
            print("  %-14s p1=%.3f  minfrac=%.2e  headroom=%.4f"
                  % (d["tmpl"], d["p1"], d["minfrac"], d["head"]))


if __name__ == "__main__":
    main()
