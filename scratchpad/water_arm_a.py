#!/usr/bin/env python3
"""ARM A ANALYSIS: the whole-only share against the three-body parameter lambda.

Scores P5 and, if it fails, fires K1 (`WATER_PREREG.md` sec 4.3, sec 9).

EVERY DESIGN CHOICE HERE WAS FIXED BEFORE THIS FILE EXISTED, and each is cited:

  slot label     first-shell coordination number, thresholded at the INTEGER
                 n >= 5 (sec 2.1).  r_cut = 3.50 A is mW's OWN measured first
                 minimum of g(r), recorded in WATER_ARM_A_GATE.md sec 3 before
                 any share existed -- a pair quantity the instrument is blind to.
  template       tetrahedral, from mW's own measured g(r): (2.86, 2.86, 4.50),
                 its first peak twice and its second shell once (gate sec 3).
                 Tolerance 0.25 A, the pre-registered primary (sec 3).
  far arm        (7.0, 7.0, 7.0), checked against L/2 = 19.6 A per AMENDMENT 10.
  cap            on TRIANGLES, never on ordered triples (AMENDMENT 9), with the
                 S3 deviation of every capped table required to read exactly 0.
  ceiling        class-partitioned (AMENDMENT 7 G2): this template has r12 = r13
                 != r23, so orientations (12|3) and (13|2) coincide BY SYMMETRY
                 and (23|1) does not.  Average the pair, then min against the
                 third.  Never min-of-three (AMENDMENT 5), never mean-of-three
                 (AMENDMENT 7 G1: +16.77%, non-decaying).
  floors         N1a iid product control -- theorem-pinned by valve_from_nothing
                 -- is the floor of record; N1b permutation is NOT theorem-pinned
                 and gauges the finite-population term (AMENDMENT 4 D2).
  N2             ideal gas at matched density through the byte-identical
                 pipeline, the template-selection and filter minting gauge, and
                 per AMENDMENT 10 J3 the PRIMARY fouling detector.
  reporting      ceiling fractions are CONTEXT, quoted with their relative sd;
                 the primary is the floor-subtracted share with its empirical
                 p-value (AMENDMENT 3 C2).
"""
import argparse
import json
import os
import sys

import numpy as np

sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")
import glass_share as GS  # noqa: E402

RCUT = 3.50
TMPL = (2.86, 2.86, 4.50)
TOL = 0.25
FAR = (7.0, 7.0, 7.0)


def read_dump(path, max_frames=None):
    """LAMMPS custom dump -> list of (positions, L). Cubic box assumed."""
    frames, f = [], open(path)
    while True:
        line = f.readline()
        if not line:
            break
        if not line.startswith("ITEM: TIMESTEP"):
            continue
        f.readline()
        f.readline()
        n = int(f.readline())
        f.readline()
        lo, hi = map(float, f.readline().split()[:2])
        L = hi - lo
        f.readline()                      # y bounds
        f.readline()                      # z bounds
        f.readline()                      # ITEM: ATOMS id x y z
        pos = np.empty((n, 3))
        for i in range(n):
            p = f.readline().split()
            pos[int(p[0]) - 1] = (float(p[1]), float(p[2]), float(p[3]))
        frames.append((np.mod(pos - lo, L), L))
        if max_frames and len(frames) >= max_frames:
            break
    f.close()
    return frames


def coordination(pos, L, rcut):
    d = pos[:, None, :] - pos[None, :, :]
    d -= L * np.round(d / L)
    r2 = np.einsum("ijk,ijk->ij", d, d)
    np.fill_diagonal(r2, np.inf)
    return (r2 < rcut * rcut).sum(1)


def cap_triangles(tri, cap, rng):
    """AMENDMENT 9: subsample TRIANGLES and keep all their orderings, so slot
    exchangeability survives the cap exactly."""
    if cap is None or len(tri) == 0 or len(tri) <= cap:
        return tri
    key = np.sort(tri, axis=1)
    _, inv = np.unique(key, axis=0, return_inverse=True)
    ntri = inv.max() + 1
    per = len(tri) / ntri
    keep = int(max(1, min(ntri, np.floor(cap / per))))
    if keep >= ntri:
        return tri
    sel = np.zeros(ntri, bool)
    sel[rng.choice(ntri, size=keep, replace=False)] = True
    return tri[sel[inv]]


def orbit_perms(tmpl):
    """The slot permutations the TEMPLATE's own geometry makes symmetries.

    AMENDMENT 9 I2 requires the capped table's invariance to read exactly zero,
    and AMENDMENT 7 G2's class partition rests on the same group.  The group is
    the template's, not S3: for `(r12, r13, r23)` a transposition of two slots is
    a symmetry exactly when it leaves the multiset of edge lengths fixed.  Only
    an EQUILATERAL template has full S3; the primary tetrahedral template
    `(2.86, 2.86, 4.50)` has the single 2<->3 transposition and nothing else.

    Requiring full S3 of an isoceles template is requiring a symmetry it does not
    have, and reading the resulting nonzero number as a defect is a gate pointed
    at the wrong object (`GATES.md` reach 8; `GATE_PROPOSAL_PROXY.md`).
    """
    r12, r13, r23 = tmpl
    out = []
    # axes are (slot1, slot2, slot3).  swapping slots i,j swaps the two edges
    # incident on the third slot.
    if r12 == r13:                       # slots 2,3 exchangeable
        out.append((0, 2, 1))
    if r12 == r23:                       # slots 1,3 exchangeable
        out.append((2, 1, 0))
    if r13 == r23:                       # slots 1,2 exchangeable
        out.append((1, 0, 2))
    if r12 == r13 == r23:                # full S3: add the two 3-cycles
        out += [(1, 2, 0), (2, 0, 1)]
    return out


def s3_deviation(tab, tmpl=None):
    """Worst relative deviation of the table from the template's OWN symmetries.

    `tmpl=None` keeps the old full-S3 behaviour and is retained only so the
    number it produced stays reproducible; it is not the gate.
    """
    t = np.asarray(tab, float)
    if t.sum() <= 0:
        return np.nan
    t = t / t.sum()
    perms = (orbit_perms(tmpl) if tmpl is not None
             else [(0, 2, 1), (1, 0, 2), (2, 1, 0), (1, 2, 0), (2, 0, 1)])
    if not perms:
        return 0.0
    return float(max(np.abs(t - np.transpose(t, p)).max() / max(t.max(), 1e-300)
                     for p in perms))


def orientations(tab):
    p = np.asarray(tab, float)
    p = p / p.sum()
    Hp = GS.entropy(p)
    return np.array([GS.entropy(p.sum(axis=ax)) + GS.entropy(p.sum(axis=sa)) - Hp
                     for ax, sa in (((2,), (0, 1)), ((1,), (0, 2)), ((0,), (1, 2)))])


def ceiling_classpartition(tab, tmpl):
    """AMENDMENT 7 G2. Classes fixed A PRIORI from the edge lengths -- never
    from observing that two estimates are close."""
    r12, r13, r23 = tmpl
    o = orientations(tab)
    groups = []
    # orientation i is "pair (jk) against slot i"; equal edges => equal classes
    if r12 == r13:
        groups.append([0, 1]); groups.append([2])
    elif r12 == r23:
        groups.append([0, 2]); groups.append([1])
    elif r13 == r23:
        groups.append([1, 2]); groups.append([0])
    else:
        groups = [[0], [1], [2]]
    return float(min(o[g].mean() for g in groups)), o.tolist(), groups


def analyse(frames, tmpl, tol, rcut, cap, ndraw, rng, nboot=400):
    per_conf, counts, labs = [], [], []
    iid_pool = np.zeros((ndraw, 8))
    perm_pool = np.zeros((ndraw, 8))
    s3s = []
    for pos, L in frames:
        nb = coordination(pos, L, rcut)
        lab = (nb >= 5).astype(np.int8)
        labs.append(lab.mean())
        tri = cap_triangles(GS.triangles(pos, L, tmpl, tol, rng), cap, rng)
        counts.append(len(tri))
        if len(tri) == 0:
            per_conf.append(np.zeros(8))
            continue
        t = GS.table_from_triples(tri, lab)
        s3s.append(s3_deviation(t, tmpl))
        per_conf.append(t.ravel())
        p1 = float(lab.mean())
        li = (rng.random((ndraw, len(lab))) < p1).astype(np.int8)   # N1a
        lp = np.stack([rng.permutation(lab) for _ in range(ndraw)])  # N1b
        for pool, LB in ((iid_pool, li), (perm_pool, lp)):
            s = LB[:, tri]
            idx = (s[:, :, 0] * 2 + s[:, :, 1]) * 2 + s[:, :, 2]
            for d in range(ndraw):
                pool[d] += np.bincount(idx[d], minlength=8)
    per_conf = np.array(per_conf)
    tab = per_conf.sum(0).reshape(2, 2, 2)
    if tab.sum() == 0:
        return dict(empty=True)
    share = GS.share_2x2x2(tab)
    fl_iid = np.array([GS.share_2x2x2(r.reshape(2, 2, 2)) for r in iid_pool if r.sum()])
    fl_prm = np.array([GS.share_2x2x2(r.reshape(2, 2, 2)) for r in perm_pool if r.sum()])
    ceil, orients, groups = ceiling_classpartition(tab, tmpl)
    bs = []
    for _ in range(nboot):
        tb = per_conf[rng.integers(0, len(per_conf), len(per_conf))].sum(0)
        if tb.sum():
            bs.append(GS.share_2x2x2(tb.reshape(2, 2, 2)))
    n = float(tab.sum())
    return dict(
        n_triples=n, nconf=len(frames), share=float(share),
        p1=float(np.mean(labs)), m=float(1 - 2 * np.mean(labs)),
        floor_median=float(np.median(fl_iid)), floor_p99=float(np.percentile(fl_iid, 99)),
        excess=float(share - np.median(fl_iid)),
        p_value=float((np.sum(fl_iid >= share) + 1) / (len(fl_iid) + 1)),
        perm_median=float(np.median(fl_prm)),
        finite_pop_gauge=float(np.median(fl_prm) - np.median(fl_iid)),
        ceiling=ceil, orientations=orients, classes=[list(map(int, g)) for g in groups],
        ceiling_fraction=float(share / ceil) if ceil > 0 else float("nan"),
        rel_sd_ratio=float(np.sqrt(2 + 8 * n * share) / (2 * n * share)) if n * share > 0 else float("nan"),
        headroom=float(GS.share_headroom(tab)[1]),
        min_cell=float(tab.min()), occupancy=float((tab > 0).mean()),
        counts_mean=float(np.mean(counts)), s3_worst=float(np.max(s3s)) if s3s else float("nan"),
        boot_sd=float(np.std(bs)) if bs else float("nan"),
        table=tab.ravel().tolist())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sweep", default="/home/emoore/CIRISOntology/scratchpad/water_mw_sweep.json")
    ap.add_argument("--cap", type=int, default=0)
    ap.add_argument("--ndraw", type=int, default=200)
    ap.add_argument("--maxframes", type=int, default=0)
    ap.add_argument("--seed", type=int, default=20260727)
    ap.add_argument("--out", default="/home/emoore/CIRISOntology/scratchpad/water_arm_a.json")
    a = ap.parse_args()
    sw = json.load(open(a.sweep))
    rng = np.random.default_rng(a.seed)
    res = {}
    lams = sorted(sw, key=float)
    # count-matching cap: the minimum triple count across the sweep (G-DOSE)
    print("lam    rho     p1      Ntri     share      floor_med   excess     p      "
          "ceil     CF%     relsd  head    minc  s3", flush=True)
    for k in lams:
        fr = read_dump(sw[k]["dump"], a.maxframes or None)
        r = analyse(fr, TMPL, TOL, RCUT, a.cap or None, a.ndraw, rng)
        r["rho"] = sw[k]["rho"]; r["lam"] = float(k)
        rf = analyse(fr, FAR, TOL, RCUT, a.cap or None, a.ndraw, rng)
        r["far"] = rf
        res[k] = r
        print("%6.2f %6.3f %6.3f %8.2e %10.3e %10.3e %+10.3e %6.4f %7.4f %6.3f %6.1f%% "
              "%6.3f %6.0f %.0e"
              % (float(k), r["rho"], r["p1"], r["n_triples"], r["share"],
                 r["floor_median"], r["excess"], r["p_value"], r["ceiling"],
                 100 * r["ceiling_fraction"], 100 * r["rel_sd_ratio"],
                 r["headroom"], r["min_cell"], r["s3_worst"]), flush=True)
        json.dump(res, open(a.out, "w"))
    print("\nwrote", a.out, flush=True)


if __name__ == "__main__":
    main()
