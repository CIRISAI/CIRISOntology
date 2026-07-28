#!/usr/bin/env python3
"""ARM A, THE LOAD-BEARING CONTROL: data against N3 and N2 at MATCHED SIZE.

The deliverable of `WATER_PREREG.md` sec 5.1 is not the share.  It is the
DIFFERENCE `share(data) - share(N3)`, where N3 is an ensemble carrying water's
own `g(r)` and nothing else.  N3 will read nonzero, because a pair ensemble has
genuine triplet structure at liquid density (bounded form, AMENDMENT 8 W6:
Kirkwood superposition is violated at liquid density by an amount that vanishes
in the dilute limit), and that is the point.

Three ensembles, ONE pipeline, the SAME number of configurations, the SAME
template, the SAME tolerance, the SAME r_cut, the SAME triangle cap:

  DATA  mW at the state point named on the command line
  N3    the IBI pair-potential liquid whose g(r) is mW's own (`water_ibi.py`)
  N2    an ideal gas at mW's own mean number density -- no structure at all, and
        per AMENDMENT 10 J3 the primary fouling detector, because it is the one
        control with no correlation length to confound it

Every reading also carries N1a, the iid label floor on its OWN positions.  N1a is
an exact product state, so `Core/Valve.lean: valve_from_nothing` -- hypotheses
read at source, three `IsKernel` kernels and three `IsProb` cell states with the
input `prod3 p1 p2 p3` -- makes its true share exactly zero, and what it reads is
that ensemble's own finite-sample floor.

ERROR BARS.  The configuration bootstrap, taken independently within each
ensemble, because N3 and the data do NOT share configurations -- the label here
is a function of the positions, so glass's PAIRED bootstrap (its sec 2.1) is
unavailable and the difference does not get the benefit of a cancelling common
fluctuation.  That is a weaker instrument than glass had and it is declared, not
absorbed: `GLASS_PREREG.md` sec 6.1 measured the configuration bootstrap to
overstate a non-negative statistic near its boundary by about 2.2x, so a NULL is
additionally scored by an exact permutation test on ensemble membership.
"""
import argparse
import json
import sys

import numpy as np

sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")
import glass_share as GS   # noqa: E402
import water_arm_a as WA   # noqa: E402

LN2 = float(np.log(2.0))


def per_conf_tables(frames, tmpl, tol, rcut, cap, rng, ndraw=300):
    """Per-configuration 8-cell tables, plus the N1a iid floor pool."""
    tabs, counts, labs = [], [], []
    pool = np.zeros((ndraw, 8))
    for pos, L in frames:
        nb = WA.coordination(pos, L, rcut)
        lab = (nb >= 5).astype(np.int8)
        labs.append(float(lab.mean()))
        tri = WA.cap_triangles(GS.triangles(pos, L, tmpl, tol, rng), cap, rng)
        counts.append(len(tri))
        if not len(tri):
            tabs.append(np.zeros(8))
            continue
        tabs.append(GS.table_from_triples(tri, lab).ravel())
        li = (rng.random((ndraw, len(lab))) < lab.mean()).astype(np.int8)
        s = li[:, tri]
        idx = (s[:, :, 0] * 2 + s[:, :, 1]) * 2 + s[:, :, 2]
        for d in range(ndraw):
            pool[d] += np.bincount(idx[d], minlength=8)
    return np.array(tabs), pool, np.array(counts), float(np.mean(labs))


def summarise(tabs, pool, counts, p1, tmpl, rng, nboot=600):
    tab = tabs.sum(0).reshape(2, 2, 2)
    share = float(GS.share_2x2x2(tab))
    fl = np.array([GS.share_2x2x2(r.reshape(2, 2, 2)) for r in pool if r.sum()])
    ceil, orients, groups = WA.ceiling_classpartition(tab, tmpl)
    bs = []
    for _ in range(nboot):
        t = tabs[rng.integers(0, len(tabs), len(tabs))].sum(0)
        if t.sum():
            bs.append(GS.share_2x2x2(t.reshape(2, 2, 2)))
    n = float(tab.sum())
    return dict(share=share, n_triples=n, nconf=len(tabs), p1=p1,
                floor_median=float(np.median(fl)),
                floor_p99=float(np.percentile(fl, 99)),
                excess_over_floor=float(share - np.median(fl)),
                p_vs_floor=float((np.sum(fl >= share) + 1) / (len(fl) + 1)),
                ceiling=ceil, orientations=orients,
                ceiling_over_floor=float(ceil / max(np.median(fl), 1e-300)),
                cf_ln2=float(share / LN2),
                cf_sharp=float(share / ceil) if ceil > 0 else float("nan"),
                rel_sd_law=float(np.sqrt(2 + 8 * n * share) / (2 * n * share))
                if n * share > 0 else float("nan"),
                headroom=float(GS.share_headroom(tab)[1]),
                min_cell=float(tab.min()), occupancy=float((tab > 0).mean()),
                orbit_dev=float(WA.s3_deviation(tab, tmpl)),
                counts_mean=float(np.mean(counts)),
                boot_sd=float(np.std(bs)), boot=bs, table=tab.ravel().tolist())


def perm_test(tabs_a, tabs_b, nperm=2000, rng=None):
    """Exact permutation test on ENSEMBLE MEMBERSHIP.

    Needs no error bar, which matters because the configuration bootstrap
    overstates the uncertainty of a non-negative statistic near its boundary
    (`GLASS_PREREG.md` sec 6.1, measured at ~2.2x).
    """
    na = len(tabs_a)
    allt = np.concatenate([tabs_a, tabs_b])
    obs = (GS.share_2x2x2(tabs_a.sum(0).reshape(2, 2, 2))
           - GS.share_2x2x2(tabs_b.sum(0).reshape(2, 2, 2)))
    cnt = 0
    for _ in range(nperm):
        idx = rng.permutation(len(allt))
        d = (GS.share_2x2x2(allt[idx[:na]].sum(0).reshape(2, 2, 2))
             - GS.share_2x2x2(allt[idx[na:]].sum(0).reshape(2, 2, 2)))
        if abs(d) >= abs(obs):
            cnt += 1
    return float(obs), float((cnt + 1) / (nperm + 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="/home/emoore/CIRISOntology/scratchpad/mw/mw_lam23.15.dump")
    ap.add_argument("--n3", default="/home/emoore/CIRISOntology/scratchpad/mw/ibi_n3.dump")
    ap.add_argument("--label", default="23.15")
    ap.add_argument("--cap", type=int, default=0)
    ap.add_argument("--nboot", type=int, default=600)
    ap.add_argument("--nperm", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=20260727)
    ap.add_argument("--out", default="/home/emoore/CIRISOntology/scratchpad/water_arm_a_null.json")
    a = ap.parse_args()

    rng = np.random.default_rng(a.seed)
    fd = WA.read_dump(a.data)
    f3 = WA.read_dump(a.n3)
    nconf = min(len(fd), len(f3))
    fd, f3 = fd[:nconf], f3[:nconf]
    n, L = len(fd[0][0]), fd[0][1]
    f2 = [(rng.random((n, 3)) * L, L) for _ in range(nconf)]
    print("matched at %d configurations, N=%d, L=%.3f A\n" % (nconf, n, L), flush=True)

    out = {"nconf": nconf, "N": n, "L": L, "data": a.data, "n3": a.n3, "cells": {}}
    for tname, tmpl in (("primary", WA.TMPL), ("far", WA.FAR)):
        res, tabs = {}, {}
        for name, fr in (("DATA", fd), ("N3_ibi", f3), ("N2_idealgas", f2)):
            tb, pool, cnt, p1 = per_conf_tables(fr, tmpl, WA.TOL, WA.RCUT,
                                                a.cap or None, rng)
            res[name] = summarise(tb, pool, cnt, p1, tmpl, rng, a.nboot)
            tabs[name] = tb
        # differences with independent configuration bootstraps
        for other in ("N3_ibi", "N2_idealgas"):
            bd = np.array(res["DATA"]["boot"])
            bo = np.array(res[other]["boot"])
            m = min(len(bd), len(bo))
            diff = bd[:m] - bo[:m]
            obs, p = perm_test(tabs["DATA"], tabs[other], a.nperm, rng)
            res["DATA"]["vs_" + other] = dict(
                excess=float(res["DATA"]["share"] - res[other]["share"]),
                boot_sd=float(np.std(diff)),
                z=float((res["DATA"]["share"] - res[other]["share"]) / max(np.std(diff), 1e-300)),
                perm_obs=obs, perm_p=p,
                excess_over_data=float((res["DATA"]["share"] - res[other]["share"])
                                       / max(res["DATA"]["share"], 1e-300)))
        for k in res:
            res[k].pop("boot", None)
        out["cells"][tname] = res

        print("--- %s template %s ---" % (tname, tmpl), flush=True)
        print("%-12s %9s %11s %11s %11s %7s %9s %8s"
              % ("ensemble", "p1", "N_tri", "share", "floor_med", "p", "ceiling", "orbit"),
              flush=True)
        for name in ("DATA", "N3_ibi", "N2_idealgas"):
            r = res[name]
            print("%-12s %9.4f %11.3e %11.4e %11.4e %7.4f %9.5f %8.1e"
                  % (name, r["p1"], r["n_triples"], r["share"], r["floor_median"],
                     r["p_vs_floor"], r["ceiling"], r["orbit_dev"]), flush=True)
        for other in ("N3_ibi", "N2_idealgas"):
            d = res["DATA"]["vs_" + other]
            print("   DATA - %-12s = %+11.4e +/- %.3e   z=%+6.2f   perm p=%.4f   (%.1f%% of data)"
                  % (other, d["excess"], d["boot_sd"], d["z"], d["perm_p"],
                     100 * d["excess_over_data"]), flush=True)
        print("", flush=True)
        json.dump(out, open(a.out, "w"))
    json.dump(out, open(a.out, "w"))
    print("wrote", a.out, flush=True)


if __name__ == "__main__":
    main()
