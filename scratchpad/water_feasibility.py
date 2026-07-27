#!/usr/bin/env python3
"""WATER campaign, stage 0: the ARITHMETIC THAT DECIDES FEASIBILITY.

Run BEFORE the pre-registration is written and BEFORE any water configuration
exists.  Nothing here reads water.  Everything here reads SYNTHETIC point
patterns built as deliberate brackets on water's oxygen sublattice, and its
only outputs are:

  (1) triples per configuration at the candidate templates  -> minimum N
  (2) the floor of the estimator vs configuration count     -> minimum n_conf
  (3) the ThirdCap per-orientation ceiling on the tables it produces
      (`CIRISOntology/Core/ThirdCap.lean`: `share_le_grouping_gaps`, whose
      MINIMUM over the three slot orientations is the honest data-computable
      denominator, and `share_le_log_two`, the universal one)
  (4) the occupancy reading of the eight-cell table under a water-like label
      composition

WHY SYNTHETIC, AND WHY TWO OF THEM.  Water's oxygen sublattice is OPEN: the
tetrahedral network gives a first-shell coordination near 4.5, where a hard
sphere fluid at the same number density gives ~10.  A single proxy would set
the triple count wrong by an order of magnitude and in an unknown direction,
so two are built to BRACKET it:

  * LDL-like proxy  -- a diamond (ice-Ic oxygen) network with Gaussian thermal
    displacement.  Coordination 4 by construction.  This is the LOW bracket on
    triple counts.
  * HDL-like proxy  -- the same network at liquid density with interstitials
    added, so first-shell coordination rises past 4.  This is the HIGH bracket.

Both are proxies for COUNTING, not for physics.  No share reported here is a
reading on water and none is a reading on anything at all: the labels are
drawn at random, so every share printed below is a FLOOR by construction
(`Core/Valve.lean`, `valve_from_nothing`: a product state has share exactly
zero, so what the estimator returns on one is its own finite-sample bias).

The estimator, the triangle enumerator and the headroom LP are imported from
the glass campaign's committed instrument (`glass_share.py`) rather than
re-written, per the brief.
"""
import argparse
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")
import glass_share as GS  # noqa: E402

LOG2 = float(np.log(2.0))

# Water's own numbers, from the literature, fixed here before any run.
RHO_LIQ = 0.03342      # oxygen number density of ambient liquid water, A^-3
RHO_ICE = 0.03068      # ice Ih / Ic oxygen number density, A^-3
R_OO_PEAK = 2.80       # first peak of g_OO, A
R_OO_MIN = 3.50        # first minimum of g_OO, A  (the coordination cutoff)
R_TET = 2.0 * R_OO_PEAK * np.sin(np.radians(109.47 / 2.0))   # 4.573 A


# ---------------------------------------------------------------------------
# the two bracketing synthetic point patterns
# ---------------------------------------------------------------------------

def diamond_lattice(ncell, a):
    """Oxygen positions of ice-Ic (diamond), ncell^3 cubic cells of side a."""
    basis = np.array([[0, 0, 0], [0, 2, 2], [2, 0, 2], [2, 2, 0],
                      [1, 1, 1], [1, 3, 3], [3, 1, 3], [3, 3, 1]]) / 4.0
    off = np.stack(np.meshgrid(*[np.arange(ncell)] * 3, indexing="ij"), -1)
    off = off.reshape(-1, 3).astype(float)
    pos = (off[:, None, :] + basis[None, :, :]).reshape(-1, 3) * a
    return pos, ncell * a


def ldl_proxy(ncell, sigma, rng):
    """LDL-like: diamond network at ice density, Gaussian thermal noise."""
    a = (8.0 / RHO_ICE) ** (1.0 / 3.0)
    pos, L = diamond_lattice(ncell, a)
    pos = pos + rng.normal(0.0, sigma, pos.shape)
    return np.mod(pos, L), L


def hdl_proxy(ncell, sigma, rng):
    """HDL-like: the same network compressed to liquid density, plus
    interstitials placed in the network's own cavities, so the first-shell
    coordination rises past four exactly as the two-state picture says it
    does on the high-density side."""
    a = (8.0 / RHO_ICE) ** (1.0 / 3.0)
    pos, L = diamond_lattice(ncell, a)
    n_int = int(round(len(pos) * (RHO_LIQ / RHO_ICE - 1.0)))
    # cavity centres of the diamond lattice: the 'other' diamond sublattice,
    # displaced by a/2 along x -- the classic interstitial site.
    cav = pos + np.array([a / 2.0, 0.0, 0.0])
    sel = rng.choice(len(cav), size=n_int, replace=False)
    pos = np.concatenate([pos, cav[sel]], axis=0)
    scale = (len(pos) / (RHO_LIQ * L ** 3)) ** (1.0 / 3.0)
    L = L * scale
    pos = pos * scale
    pos = pos + rng.normal(0.0, sigma, pos.shape)
    return np.mod(pos, L), L


# ---------------------------------------------------------------------------
# the label: first-shell coordination number, thresholded at an integer
# ---------------------------------------------------------------------------

def coordination(pos, L, rcut):
    d = pos[:, None, :] - pos[None, :, :]
    d -= L * np.round(d / L)
    r2 = np.einsum("ijk,ijk->ij", d, d)
    np.fill_diagonal(r2, np.inf)
    return (r2 < rcut * rcut).sum(1)


# ---------------------------------------------------------------------------
# ThirdCap: the per-orientation ceilings, whose MINIMUM is the denominator
# ---------------------------------------------------------------------------

def thirdcap_ceilings(tab):
    """`Core/ThirdCap.lean` `share_le_grouping_gaps`, evaluated on a table.

        share <= H(marg_ab) + H(marg_c) - H(p)   for each of the three ways of
                                                 splitting {1,2,3} into a pair
                                                 and a singleton,

    and the honest data-computable ceiling is the MINIMUM of the three.  Never
    worse than `log 2` (`share_le_log_two`), and often far better.
    """
    p = np.asarray(tab, dtype=float)
    s = p.sum()
    if s <= 0:
        return dict(ceil_12_3=np.nan, ceil_13_2=np.nan, ceil_23_1=np.nan,
                    ceil_min=np.nan, ceil_log2=LOG2)
    p = p / s
    Hp = GS.entropy(p)
    out = {}
    for name, pair_ax, sing_ax in (("12_3", (2,), (0, 1)),
                                   ("13_2", (1,), (0, 2)),
                                   ("23_1", (0,), (1, 2))):
        out["ceil_" + name] = (GS.entropy(p.sum(axis=pair_ax))
                               + GS.entropy(p.sum(axis=sing_ax)) - Hp)
    out["ceil_min"] = float(min(out.values()))
    out["ceil_log2"] = LOG2
    return out


# ---------------------------------------------------------------------------
# the sweep
# ---------------------------------------------------------------------------

def templates():
    """The candidate templates, fixed here from water's published g_OO and
    from the tetrahedral angle -- both PAIR/single-molecule quantities the
    instrument is blind to by construction."""
    return {
        "tetrahedral": (R_OO_PEAK, R_OO_PEAK, R_TET),
        "equilateral_nn": (R_OO_PEAK, R_OO_PEAK, R_OO_PEAK),
        "interstitial": (R_OO_PEAK, 3.20, 3.20),
        "second_shell": (R_OO_PEAK, R_TET, R_TET),
        "far_null": (7.0, 7.0, 7.0),
    }


def run(proxy, ncell, sigma, nconf, tol, ndraw, rcut, seed, out):
    rng = np.random.default_rng(seed)
    tm = templates()
    build = ldl_proxy if proxy == "ldl" else hdl_proxy
    rec = {k: dict(counts=[], data_tabs=[], null=[]) for k in tm}
    coordstats = []
    t0 = time.time()
    for c in range(nconf):
        pos, L = build(ncell, sigma, rng)
        N = len(pos)
        nb = coordination(pos, L, rcut)
        lab = (nb >= 5).astype(np.int8)          # 0 = LDL-like, 1 = HDL-like
        coordstats.append((float(nb.mean()), float(lab.mean())))
        # ndraw permutation nulls for THIS configuration; each null draw takes
        # one relabelling from every configuration, so a null draw is a
        # full-ensemble reading, and it passes through the byte-identical
        # triple selection.  This is the floor construction the glass
        # campaign's own examination forced (GLASS_PREREG.md sec 4.1).
        lp = np.stack([rng.permutation(lab) for _ in range(ndraw)])
        for k, t in tm.items():
            tri = GS.triangles(pos, L, t, tol, rng)
            rec[k]["counts"].append(int(len(tri)))
            if len(tri) == 0:
                rec[k]["data_tabs"].append(np.zeros(8))
                rec[k]["null"].append(np.zeros((ndraw, 8)))
                continue
            rec[k]["data_tabs"].append(GS.table_from_triples(tri, lab).ravel())
            nt = np.zeros((ndraw, 8))
            s = lp[:, tri]                                    # (D, M, 3)
            idx = (s[:, :, 0] * 2 + s[:, :, 1]) * 2 + s[:, :, 2]
            for d in range(ndraw):
                nt[d] = np.bincount(idx[d], minlength=8)
            rec[k]["null"].append(nt)
        if c % 10 == 0:
            print(f"  conf {c}/{nconf}  N={N}  L={L:.2f}  "
                  f"<n>={np.mean([x[0] for x in coordstats]):.2f}  "
                  f"{time.time()-t0:.0f}s", flush=True)

    res = dict(proxy=proxy, ncell=ncell, N=int(N), L=float(L), sigma=sigma,
               nconf=nconf, tol=tol, rcut=rcut, ndraw=ndraw, seed=seed,
               coord_mean=float(np.mean([x[0] for x in coordstats])),
               p_hdl=float(np.mean([x[1] for x in coordstats])),
               templates={})
    for k, t in tm.items():
        cnt = np.array(rec[k]["counts"], dtype=float)
        dat = np.array(rec[k]["data_tabs"])
        nul = np.array(rec[k]["null"])                        # (nconf, D, 8)
        row = dict(template=list(t), count_mean=float(cnt.mean()),
                   count_min=int(cnt.min()), count_max=int(cnt.max()),
                   count_per_particle=float(cnt.mean() / N))
        # THE FLOOR LADDER: how the floor falls as configurations accumulate.
        ladder = {}
        for m in (1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000):
            if m > nconf:
                # extrapolate by pooling with replacement is NOT done; the
                # ladder simply stops where the data stops, and the report
                # says so.
                continue
            pooled = nul[:m].sum(0)                           # (D, 8)
            sh = np.array([GS.share_2x2x2(r.reshape(2, 2, 2))
                           for r in pooled if r.sum() > 0])
            if not len(sh):
                continue
            ladder[m] = dict(
                n_triples=float(cnt[:m].sum()),
                floor_median=float(np.median(sh)),
                floor_p99=float(np.percentile(sh, 99)),
                floor_mean=float(sh.mean()))
        row["floor_ladder"] = ladder
        tab = dat.sum(0).reshape(2, 2, 2)
        if tab.sum() > 0:
            row["occupancy"] = dict(
                min_cell=float(tab.min()), n_empty=int((tab == 0).sum()),
                occupancy=float((tab > 0).mean()),
                min_cell_per_conf=float(tab.min() / nconf),
                table=tab.ravel().tolist())
            row["ceilings"] = thirdcap_ceilings(tab)
            row["share_random_label"] = float(GS.share_2x2x2(tab))
            row["headroom"] = float(GS.share_headroom(tab)[1])
        res["templates"][k] = row
        print(f"  [{k}] {t}  triples/conf={row['count_mean']:.0f} "
              f"({row['count_per_particle']:.2f}/particle)", flush=True)
    json.dump(res, open(out, "w"), indent=1)
    print("wrote", out)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--proxy", default="hdl", choices=["ldl", "hdl"])
    ap.add_argument("--ncell", type=int, default=6)      # 8*n^3 sites
    ap.add_argument("--sigma", type=float, default=0.35)
    ap.add_argument("--nconf", type=int, default=60)
    ap.add_argument("--tol", type=float, default=0.15)
    ap.add_argument("--rcut", type=float, default=R_OO_MIN)
    ap.add_argument("--ndraw", type=int, default=200)
    ap.add_argument("--seed", type=int, default=20260727)
    ap.add_argument("--out", default="water_feasibility.json")
    a = ap.parse_args()
    run(a.proxy, a.ncell, a.sigma, a.nconf, a.tol, a.ndraw, a.rcut,
        a.seed, os.path.join("/home/emoore/CIRISOntology/scratchpad", a.out))


if __name__ == "__main__":
    main()
