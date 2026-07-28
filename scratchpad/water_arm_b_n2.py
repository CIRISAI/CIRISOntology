#!/usr/bin/env python3
"""ARM B's OWN N2 CONTROL — required before any arm B reading means anything.

`WATER_AMENDMENT_10.md` J3 makes the ideal gas the PRIMARY fouling detector, and
`water_arm_a_null.py` measured that on THIS design it does not read floor: at the
water template the ideal gas mints 22x more whole-only share than mW carries,
because the three slots' coordination cutoff spheres overlap and a particle in
their triple intersection is counted by all three at once (`WATER_RESULTS.md`
sec 2.4, sec 3.4).

Arm B's B_matched variant uses `r_cut = 1.0599 sigma` at templates of side 1.30
and 1.50 sigma.  Both are below `2 r_cut = 2.12 sigma`, so **the same minting
channel is open**, and an arm B reading quoted against a LABEL floor would be
quoted against the wrong null for exactly the reason arm A's was.

This file reads the byte-identical pipeline on `glass/compact/SYNTH_ideal.npz` --
the glass campaign's OWN ideal-gas control at its own density -- so the
comparison is against a null built by the campaign whose configurations these
are, and not against one this campaign generated for itself.

POLARITY, declared: a PASS is the ideal gas reading AT OR BELOW its own floor.
Anything above it is the minting pedestal, and any arm B reading below the
pedestal is VOID by `WATER_PREREG.md` sec 5.2's own rule.
"""
import argparse
import json
import sys

import numpy as np

sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")
import water_arm_a as WA   # noqa: E402
import water_arm_b as WB   # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nconf", type=int, default=40)
    ap.add_argument("--ndraw", type=int, default=200)
    ap.add_argument("--seed", type=int, default=20260727)
    ap.add_argument("--out", default="/home/emoore/CIRISOntology/scratchpad/water_arm_b_n2.json")
    a = ap.parse_args()
    rng = np.random.default_rng(a.seed)

    b = json.load(open("/home/emoore/CIRISOntology/scratchpad/water_arm_b.json"))
    L = b["L"]
    d = np.load("glass/compact/SYNTH_ideal.npz")
    P = d["positions"][:a.nconf].astype(np.float64)
    frames = [(np.mod(p - p.min(), L), L) for p in P]

    out = {"L": L, "nconf": len(frames), "rcut_own": b["rcut_own"],
           "rcut_matched": b["rcut_matched"], "cells": {}}
    print("arm B N2: glass's own SYNTH_ideal, %d configs, L=%.4f\n" % (len(frames), L),
          flush=True)
    print("%9s %9s %6s %10s %11s %11s %8s %9s %7s"
          % ("variant", "template", "p1", "N_tri", "share", "floor_med", "p",
             "ceiling", "minc"), flush=True)
    for vname, rcut in (("B_own", b["rcut_own"]), ("B_matched", b["rcut_matched"])):
        out["cells"][vname] = {}
        tmpls = ({"1.30": WB.TEMPLATES["1.30"]} if vname == "B_own" else WB.TEMPLATES)
        for tname, tmpl in tmpls.items():
            r = WA.analyse(frames, tmpl, WB.TOL, rcut, WB.CAP, a.ndraw, rng, nboot=200)
            r["rcut"] = rcut
            out["cells"][vname][tname] = r
            print("%9s %9s %6.3f %10.3e %11.4e %11.4e %8.4f %9.5f %7.0f"
                  % (vname, tname, r["p1"], r["n_triples"], r["share"],
                     r["floor_median"], r["p_value"], r["ceiling"], r["min_cell"]),
                  flush=True)
            json.dump(out, open(a.out, "w"))
    json.dump(out, open(a.out, "w"))
    print("\nwrote", a.out, flush=True)


if __name__ == "__main__":
    main()
