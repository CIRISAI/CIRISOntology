#!/usr/bin/env python3
"""ARM B: the Kob-Andersen PAIR-POTENTIAL baseline, read with THIS campaign's
coordination-number label on the glass campaign's own configurations.

PRE-REGISTERED as P6 (`WATER_PREREG.md` sec 4.3) and extended to P8 by
`WATER_AMENDMENT_1.md` A4, which glass staked BEFORE seeing any coordination
reading, making it an advance prediction under `epistemology.md` rule 6:

  P6  the Kob-Andersen mixture, read with the SAME coordination label through
      the SAME instrument across its own supercooling ladder, shows NO interior
      peak of the P1/P2 kind.
  P8  it reads MONOTONE in T, agreeing with glass's SPECIES reading in both
      monotonicity and sign.  A PASS is agreement.  An interior peak is a real
      disagreement between two labels on byte-identical configurations and is
      CHASED, not explained away.

THE THREE CONDITIONS `WATER_AMENDMENT_1.md` A3 attached, all honoured:
  1. read `glass/compact/*.npz`, never the tarballs -- the compact files carry
     positions, inherent structures and types only, and the dynamical
     propensities are discarded at ingestion.  For a deflation control that is a
     feature: a static-order baseline must have no dynamical label near it;
  2. take the count-matched cap 1300, ON TRIANGLES (A3(2) as superseded by
     AMENDMENT 9 I2), because glass's raw triple counts RISE with temperature --
     the same direction a floor artifact would take;
  3. seed every RNG and record the seed.

THE r_cut PROBLEM, declared HERE and BEFORE any reading, because
`WATER_AMENDMENT_12.md` L3 makes it predictable rather than a surprise.  The
`n >= 5` threshold was fixed for WATER, where the tetrahedral network puts ~4-5
neighbours in the first shell.  Kob-Andersen is a dense pair-potential liquid at
rho = 1.2 sigma^-3, so its own first shell holds ~12, and the label would
SATURATE exactly as it does on every homogeneous pair-potential liquid in arm A.
Two r_cut are therefore declared in advance, and BOTH are reported:

  B-own      r_cut = KA's OWN measured first minimum of g(r).  This is the
             campaign's own rule (`WATER_PREREG.md` sec 2.1) transferred
             literally.  PREDICTED, before the run, to be LABEL-DEGENERATE
             (p1 > 0.98).  If it is, that is not a failure of arm B -- it is arm
             B independently reproducing arm A's finding on a different
             substrate, a different code and a different potential.
  B-matched  r_cut set so that the IDEAL-GAS coordination at KA's density equals
             the ideal-gas coordination at mW's density and r_cut = 3.50 A,
             namely 5.99.  This matches what the LABEL can resolve rather than
             what the geometry is called, and it is the only version in which
             P6/P8 are scorable at all.

POLARITY (G-POL, sec 5.5): a PASS of P6 is NO interior maximum; a PASS of P8 is
monotone in T with glass's sign.  Declared before the numbers exist.
"""
import argparse
import json
import sys

import numpy as np

sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")
import glass_share as GS   # noqa: E402
import water_arm_a as WA   # noqa: E402

LN2 = float(np.log(2.0))
TEMPS = ["0.44", "0.50", "0.56", "0.64"]
TEMPLATES = {"1.30": (1.30, 1.30, 1.30), "1.50": (1.50, 1.50, 1.50),
             "far_5.00": (5.00, 5.00, 5.00)}
TOL = 0.10                      # glass's own tolerance, inherited
CAP = 1300                      # AMENDMENT 1 A3(2), on TRIANGLES per AMENDMENT 9


def gr(pos, L, rmax, nbins=200):
    d = pos[:, None, :] - pos[None, :, :]
    d -= L * np.round(d / L)
    r = np.sqrt(np.einsum("ijk,ijk->ij", d, d))
    r = r[np.triu_indices(len(pos), 1)]
    h, e = np.histogram(r[r < rmax], bins=nbins, range=(0, rmax))
    rc = 0.5 * (e[1:] + e[:-1])
    shell = (4.0 / 3.0) * np.pi * (e[1:] ** 3 - e[:-1] ** 3)
    n = len(pos)
    return rc, h / (shell * 0.5 * n * (n - 1) / L ** 3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nconf", type=int, default=80)
    ap.add_argument("--ndraw", type=int, default=300)
    ap.add_argument("--nboot", type=int, default=400)
    ap.add_argument("--seed", type=int, default=20260727)
    ap.add_argument("--out", default="/home/emoore/CIRISOntology/scratchpad/water_arm_b.json")
    a = ap.parse_args()
    rng = np.random.default_rng(a.seed)

    # --- r_cut, both versions, fixed from g(r) BEFORE any share ---
    d = np.load("glass/compact/KA_T0.64.npz")
    pos0 = d["positions"][0].astype(np.float64)
    L = float(pos0.max() - pos0.min())
    L = round(L, 4)
    n = pos0.shape[0]
    rho = n / L ** 3
    rc, g = gr(np.mod(pos0 - pos0.min(), L), L, 3.0)
    pk = int(np.argmax(g))
    mn = pk + int(np.argmin(g[pk:pk + 60]))
    rcut_own = float(rc[mn])
    rcut_matched = float((5.99 * 3.0 / (4.0 * np.pi * rho)) ** (1.0 / 3.0))
    print("Kob-Andersen: N=%d  L=%.4f  rho=%.4f sigma^-3" % (n, L, rho), flush=True)
    print("  g(r) first peak %.3f, first minimum %.3f -> r_cut(B-own) = %.4f"
          % (rc[pk], rc[mn], rcut_own), flush=True)
    print("  ideal-gas-matched r_cut (n_ideal = 5.99, as mW at 3.50 A) = %.4f\n"
          % rcut_matched, flush=True)

    out = {"L": L, "N": n, "rho": rho, "nconf": a.nconf, "cap": CAP, "tol": TOL,
           "rcut_own": rcut_own, "rcut_matched": rcut_matched,
           "gr_first_peak": float(rc[pk]), "gr_first_min": float(rc[mn]),
           "cells": {}}

    # B_own is PREDICTED above to be label-degenerate.  A degenerate label
    # collapses the table whatever the geometry, so it is run at ONE template;
    # three copies of the same collapse would buy nothing and this box is shared.
    plan = {"B_own": {"1.30": TEMPLATES["1.30"]}, "B_matched": TEMPLATES}
    for vname, rcut in (("B_own", rcut_own), ("B_matched", rcut_matched)):
        out["cells"][vname] = {}
        print("=== %s   r_cut = %.4f ===" % (vname, rcut), flush=True)
        print("%9s %6s %6s %10s %11s %11s %8s %9s %9s %7s"
              % ("template", "T", "p1", "N_tri", "share", "floor_med", "p",
                 "ceiling", "headroom", "minc"), flush=True)
        for tname, tmpl in plan[vname].items():
            out["cells"][vname][tname] = {}
            for T in TEMPS:
                dd = np.load("glass/compact/KA_T%s.npz" % T)
                P = dd["positions"][:a.nconf].astype(np.float64)
                frames = [(np.mod(p - p.min(), L), L) for p in P]
                r = WA.analyse(frames, tmpl, TOL, rcut, CAP, a.ndraw, rng,
                               nboot=a.nboot)
                r["T"] = float(T)
                r["rcut"] = rcut
                r["ceiling_over_floor"] = r["ceiling"] / max(r["floor_median"], 1e-300)
                r["label_degenerate"] = bool(r["p1"] > 0.98 or r["p1"] < 0.02)
                r["cf_ln2"] = r["share"] / LN2
                out["cells"][vname][tname][T] = r
                print("%9s %6s %6.3f %10.3e %11.4e %11.4e %8.4f %9.5f %9.4f %7.0f"
                      % (tname, T, r["p1"], r["n_triples"], r["share"],
                         r["floor_median"], r["p_value"], r["ceiling"],
                         r["headroom"], r["min_cell"]), flush=True)
                json.dump(out, open(a.out, "w"))
        print("", flush=True)
    json.dump(out, open(a.out, "w"))
    print("wrote", a.out, flush=True)


if __name__ == "__main__":
    main()
