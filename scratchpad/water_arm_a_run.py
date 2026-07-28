#!/usr/bin/env python3
"""ARM A, THE RUN: the whole-only share against the three-body parameter lambda.

Scores P5' (`WATER_AMENDMENT_12.md` L5) on the lambda window that passes BOTH
pre-declared gates.  P5 as frozen is not scorable and K1 is UNGAUGED; that
adjudication is in amendment 12 and was written before this file computed
anything.

WHAT IS FIXED BEFORE THIS FILE RUNS, and where each was fixed:

  template   (2.86, 2.86, 4.50) A, tolerance 0.25 A -- mW's OWN measured g(r)
             first peak twice and its second shell once (`WATER_ARM_A_GATE.md`
             sec 3, recorded before any share existed).  g(r) is a PAIR quantity
             the instrument is blind to, so fixing a template from it is
             legitimate and is declared (`WATER_PREREG.md` sec 2.1).
  label      first-shell coordination thresholded at the integer n >= 5, r_cut =
             3.50 A = mW's own first minimum of g(r).  Never moved.
  gates      G-HOMOG and G-LABEL, thresholds fixed in amendment 12 L5
  ceiling    class-partitioned: r12 == r13 != r23, so orientations (12|3) and
             (13|2) coincide BY SYMMETRY.  Average the pair, then min against the
             third (AMENDMENT 7 G2).  Never min-of-three, never mean-of-three
  cap        on TRIANGLES (AMENDMENT 9 I2), with the S3 deviation of every capped
             table required to read exactly zero
  floors     N1a iid product -- theorem-pinned by `valve_from_nothing`, whose
             hypotheses were checked at source -- is the floor of record; N1b
             permutation gauges the finite-population term (AMENDMENT 4 D2)
  far arm    radius max(3 xi, 7.0 A) with xi MEASURED here, and UNGAUGED rather
             than passed if 3 xi > L/2 (AMENDMENT 10 J3)
  reporting  the primary is the floor-subtracted share with its empirical
             p-value; ceiling fractions are CONTEXT with their relative sd
             (AMENDMENT 3 C2), and BOTH denominators are named (`GATES.md`,
             named-denominator reporting) with the sharp fraction quoted only
             where the sharp cap clears the floor by the stated factor
"""
import argparse
import json
import sys

import numpy as np

sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")
import glass_share as GS   # noqa: E402
import water_arm_a as WA   # noqa: E402

LN2 = float(np.log(2.0))
# `GATES.md`, named-denominator reporting, AMENDED (glass, 4acfca8): a sharp
# ceiling fraction is quoted only where the sharp cap exceeds the reading's own
# floor by a stated factor; >= 100 is the comfortable bar.
SHARP_BAR = 100.0


def corr_length(r, g, rlo=4.0, rhi=None):
    """xi from the envelope of h(r) = g(r) - 1, which decays as exp(-r/xi)/r.

    A PAIR quantity, so measuring it is legitimate under sec 2.1 and is declared.
    Fitted on the extrema of r*h(r) beyond the first shell, which is where the
    Ornstein-Zernike form applies and where the first-peak amplitude does not
    dominate the fit.
    """
    r, g = np.asarray(r), np.asarray(g)
    rh = r * (g - 1.0)
    m = (r >= rlo) & (r <= (rhi if rhi else r[-1]))
    rr, y = r[m], rh[m]
    ext = [i for i in range(1, len(y) - 1)
           if (abs(y[i]) > abs(y[i - 1]) and abs(y[i]) > abs(y[i + 1]))]
    ext = [i for i in ext if abs(y[i]) > 1e-4]
    if len(ext) < 3:
        return float("nan"), 0
    sl = np.polyfit(rr[ext], np.log(np.abs(y[ext])), 1)[0]
    return (float(-1.0 / sl) if sl < 0 else float("nan")), len(ext)


def frames_for(path, stride, maxframes):
    fr = WA.read_dump(path)
    fr = fr[::stride]
    return fr[:maxframes] if maxframes else fr


def label_tau(frames, rcut):
    """Configuration-level decorrelation of the LABEL FIELD itself.

    The independent axis is the independent CONFIGURATION, never the pooled
    triple (`whole-only-null-autocorrelation`).  Measured on the label vector's
    own autocorrelation across frames, in units of frames.
    """
    labs = np.array([(WA.coordination(p, L, rcut) >= 5).astype(float)
                     for p, L in frames])
    labs -= labs.mean(1, keepdims=True)
    n = len(labs)
    ac = []
    for k in range(1, min(n // 3, 20)):
        num = np.mean([np.dot(labs[i], labs[i + k]) for i in range(n - k)])
        ac.append(num)
    a0 = np.mean([np.dot(labs[i], labs[i]) for i in range(n)])
    ac = np.array(ac) / a0
    tau = 1.0
    for v in ac:
        if v <= 0:
            break
        tau += 2 * v
    return float(tau), ac.tolist()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sweep", default="/home/emoore/CIRISOntology/scratchpad/water_mw_all.json")
    ap.add_argument("--gates", nargs="*", default=[
        "/home/emoore/CIRISOntology/scratchpad/water_mw_sweep_homog.json",
        "/home/emoore/CIRISOntology/scratchpad/water_mw_sweep_fill_homog.json",
        "/home/emoore/CIRISOntology/scratchpad/water_mw_sweep_up_homog.json"])
    ap.add_argument("--stride", type=int, default=1)
    ap.add_argument("--maxframes", type=int, default=0)
    ap.add_argument("--ndraw", type=int, default=300)
    ap.add_argument("--nboot", type=int, default=400)
    ap.add_argument("--cap", type=int, default=0, help="0 = auto count-match")
    ap.add_argument("--all", action="store_true", help="read gate-failing points too")
    ap.add_argument("--no-far", dest="no_far", action="store_true",
                    help="skip the far arm; it is established at floor elsewhere and its\n                         triangle count dominates the run time")
    ap.add_argument("--modes", default="full,matched")
    ap.add_argument("--seed", type=int, default=20260727)
    ap.add_argument("--out", default="/home/emoore/CIRISOntology/scratchpad/water_arm_a.json")
    a = ap.parse_args()

    sw = json.load(open(a.sweep))
    gates = {}
    for gf in a.gates:
        try:
            gates.update(json.load(open(gf)))
        except FileNotFoundError:
            pass
    lams = sorted(sw, key=float)
    read = [k for k in lams if a.all or gates.get(k, {}).get("verdict") == "PASS"]
    print("gate-passing lambda: %s\n" % read, flush=True)

    rng = np.random.default_rng(a.seed)
    frames = {k: frames_for(sw[k]["dump"], a.stride, a.maxframes) for k in read}

    # --- xi, tau and the count-match cap, all BEFORE any share ---
    pre = {}
    for k in read:
        xi, nx = corr_length(sw[k]["r"], sw[k]["g"])
        tau, ac = label_tau(frames[k][:60], WA.RCUT)
        L = frames[k][0][1]
        ntri = int(np.median([len(GS.triangles(p, LL, WA.TMPL, WA.TOL, rng))
                              for p, LL in frames[k][:12]]))
        pre[k] = dict(xi=xi, n_extrema=nx, tau_frames=tau, L=L,
                      r_far=max(3 * xi, 7.0) if np.isfinite(xi) else 7.0,
                      far_exists=bool(np.isfinite(xi) and 3 * xi <= 0.5 * L),
                      tri_per_conf=ntri, autocorr=ac[:6])
        print("  lam=%-6s xi=%5.2f A (%d extrema)  3xi=%5.2f  L/2=%5.2f  r_far=%5.2f  "
              "far_exists=%s  tau=%4.2f frames  tri/conf=%d"
              % (k, xi, nx, 3 * xi, 0.5 * L, pre[k]["r_far"],
                 pre[k]["far_exists"], tau, ntri), flush=True)

    cap = a.cap or int(min(pre[k]["tri_per_conf"] for k in read))
    print("\ncount-match cap (G-DOSE, on TRIANGLES): %d ordered triples/config\n" % cap,
          flush=True)

    res = {"cap": cap, "pre": pre, "stride": a.stride, "cells": {}}
    hdr = ("%6s %6s %8s %10s %10s %11s %7s %9s %9s %8s %8s %7s %6s"
           % ("lam", "p1", "N_tri", "share", "floor_med", "excess", "p",
              "ceil_sharp", "head", "CF_ln2%", "relsd%", "minc", "s3"))
    modes = [m for m in a.modes.split(",")]
    for tag, thecap in [x for x in (("full", None), ("matched", cap)) if x[0] in modes]:
        print("=== %s count ===\n%s" % (tag, hdr), flush=True)
        res["cells"][tag] = {}
        for k in read:
            r = WA.analyse(frames[k], WA.TMPL, WA.TOL, WA.RCUT, thecap,
                           a.ndraw, rng, nboot=a.nboot)
            rf = None
            if pre[k]["far_exists"] and not a.no_far:
                rr = pre[k]["r_far"]
                rf = WA.analyse(frames[k], (rr, rr, rr), WA.TOL, WA.RCUT, thecap,
                                a.ndraw, rng, nboot=50)
            r["far"] = rf
            r["far_radius"] = pre[k]["r_far"]
            r["far_exists"] = pre[k]["far_exists"]
            r["lam"] = float(k)
            r["rho"] = sw[k].get("rho_avg", sw[k]["rho"])
            r["press"] = sw[k].get("press")
            r["nconf"] = len(frames[k])
            r["cf_ln2"] = r["share"] / LN2
            r["ceiling_over_floor"] = r["ceiling"] / max(r["floor_median"], 1e-300)
            r["sharp_fraction_quotable"] = bool(r["ceiling_over_floor"] >= SHARP_BAR)
            r["ungauged_ceiling"] = bool(r["ceiling_over_floor"] < 10.0)
            res["cells"][tag][k] = r
            print("%6s %6.3f %8.2e %10.3e %10.3e %+11.3e %7.4f %9.4f %9.4f %8.4f %8.1f %7.0f %6.0e"
                  % (k, r["p1"], r["n_triples"], r["share"], r["floor_median"],
                     r["excess"], r["p_value"], r["ceiling"], r["headroom"],
                     100 * r["cf_ln2"], 100 * r["rel_sd_ratio"], r["min_cell"],
                     r["s3_worst"]), flush=True)
            json.dump(res, open(a.out, "w"))
        print("", flush=True)
    json.dump(res, open(a.out, "w"))
    print("wrote", a.out, flush=True)


if __name__ == "__main__":
    main()
