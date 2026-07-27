#!/usr/bin/env python3
"""STAGE A of the glass campaign: the temperature sweep, its controls, its
floors and the cheap gates.  Pre-registered in GLASS_PREREG.md.

The loop order is chosen so the expensive thing is done once.  Geometry --
the pair-distance matrix and the closed-triangle enumeration -- costs
everything; relabelling the found triples costs nothing.  So for each
configuration the triples are found ONCE and then read under every label
assignment the pre-registration calls for: the data's own species, the iid
product control, the permutation control, and (stage B) the pair-matched
surrogate.  Every control therefore passes through a BYTE-IDENTICAL template
selection, which is the only way the template-selection-minting hazard can be
gauged rather than argued.

No IPF anywhere in the primary reading: the 2x2x2 share is exact.
"""
import argparse
import json
import os
import sys
import time
import zlib

import numpy as np

sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")
import glass_share as GS  # noqa: E402

try:
    import cupy as cp
    XP = cp
    GPU = True
except Exception:                                     # pragma: no cover
    XP = np
    GPU = False


# ---------------------------------------------------------------------------
# geometry on the GPU
# ---------------------------------------------------------------------------

def pair_dist2(pos, L, chunk=512):
    """Squared minimum-image distances, (N, N) float32."""
    x = XP.asarray(pos, dtype=XP.float32)
    N = x.shape[0]
    out = XP.empty((N, N), dtype=XP.float32)
    Lf = XP.float32(L)
    for a in range(0, N, chunk):
        b = min(a + chunk, N)
        d = x[a:b, None, :] - x[None, :, :]
        d -= Lf * XP.round(d / Lf)
        out[a:b] = XP.sum(d * d, axis=2)
    return out


def _padded_from_bool(A):
    """(N, K) neighbour indices + validity mask from a boolean adjacency."""
    deg = A.sum(1)
    K = int(deg.max()) if int(deg.max()) > 0 else 1
    N = A.shape[0]
    order = XP.argsort(~A, axis=1, kind='stable')[:, :K].astype(XP.int32)
    rank = XP.arange(K, dtype=XP.int32)[None, :]
    M = rank < deg[:, None]
    return order, M, deg


def triangles_from_d2(d2, tmpl, tol, rng, cap=None):
    """Ordered vertex triples closing the template, from a distance matrix.

    Slot 1 is the apex: its two incident edges are (r12, r13); the remaining
    edge (r23) is a lookup.  For the equilateral template this returns each
    unordered triangle in all six orders, which is the symmetrization the
    template's own symmetry demands (GLASS_PREREG.md sec 3.3).
    """
    r12, r13, r23 = tmpl
    N = d2.shape[0]

    def shell(r):
        A = (d2 >= XP.float32((r - tol) ** 2)) & (d2 < XP.float32((r + tol) ** 2))
        XP.fill_diagonal(A, False)
        return A

    A12 = shell(r12)
    A13 = A12 if r13 == r12 else shell(r13)
    A23 = A12 if r23 == r12 else shell(r23)
    NB12, M12, _ = _padded_from_bool(A12)
    NB13, M13, _ = _padded_from_bool(A13)
    if NB12.shape[1] == 0 or NB13.shape[1] == 0:
        return XP.zeros((0, 3), dtype=XP.int32)
    ok = A23[NB12[:, :, None], NB13[:, None, :]]
    ok &= M12[:, :, None] & M13[:, None, :]
    ok &= (NB12[:, :, None] != NB13[:, None, :])
    ii, aa, bb = XP.nonzero(ok)
    tri = XP.stack([ii.astype(XP.int32), NB12[ii, aa], NB13[ii, bb]], axis=1)
    if cap is not None and tri.shape[0] > cap:
        # CAP TRIANGLES, NOT ORDERED TRIPLES.  Subsampling the ordered list with
        # rng.choice breaks the enumeration's symmetry -- and that symmetry is
        # the A PRIORI warrant for the orientation-class partition the sharp
        # ceiling depends on (GLASS_RESULTS.md sec 2.2b).  Measured: ordered
        # capping gives S3 deviations of 9e-3 to 2e-2 where triangle capping
        # gives EXACTLY 0.000e+00, at the same kept count.  Found by the water
        # campaign, which noticed that two conditions both campaigns had
        # adopted -- the count-matched cap and the a priori class partition --
        # are in direct conflict under ordered capping.
        #
        # Subsample the UNORDERED triangles; keep every ordering of each
        # selected one.  For a scalene template the orbit size is 1 and this
        # reduces to ordered capping, which is correct: no symmetry, nothing to
        # preserve.
        t = cp.asnumpy(tri) if GPU else np.asarray(tri)
        key = np.sort(t, axis=1)
        uniq, inv = np.unique(key, axis=0, return_inverse=True)
        mult = max(1, int(round(len(t) / len(uniq))))
        ntri = max(1, cap // mult)
        if ntri < len(uniq):
            keep = rng.choice(len(uniq), size=ntri, replace=False)
            mask = np.zeros(len(uniq), dtype=bool)
            mask[keep] = True
            tri = XP.asarray(t[mask[inv]])
    return tri


def table_of(tri, lab, nlab=2):
    """nlab^3 contingency table of slot labels over a triple list."""
    if tri.shape[0] == 0:
        return np.zeros((nlab,) * 3)
    s = lab[tri]
    idx = (s[:, 0].astype(XP.int64) * nlab + s[:, 1]) * nlab + s[:, 2]
    c = XP.bincount(idx, minlength=nlab ** 3)
    return (cp.asnumpy(c) if GPU else c).reshape((nlab,) * 3).astype(float)


def tables_of_many(tri, labs, nlab=2, chunk=32):
    """(D, nlab^3) tables for D label vectors over ONE triple list.

    WHY THIS EXISTS, and it is the single most important correction this
    campaign's own examination produced.  A multinomial resample of the pooled
    table at its raw triple count N is NOT the right floor here, and the
    ideal-gas control proved it: the enumerated triples SHARE PARTICLES -- at the
    nearest-neighbour template each particle sits in several of them -- so the
    effective independent count is far below N and the finite-sample bias is far
    above 1/(2N).  On a synthetic ideal gas the multinomial floor read 3.3e-6
    where the control's true spread was 1.5e-4, a factor of 45.  Had that floor
    been used, every reading in this campaign would have been quoted against a
    null 45 times too small.

    The floor is therefore the CONTROL ITSELF, drawn many times and pushed
    through the byte-identical triple selection: same configurations, same
    template, same tolerance, same cap, same triples -- only the labels change.
    That is the only construction in which the overlap structure of the triples
    is carried by the null as well as by the data.
    """
    D = labs.shape[0]
    if tri.shape[0] == 0:
        return np.zeros((D, nlab ** 3))
    out = XP.zeros((D, nlab ** 3), dtype=XP.float64)
    i0, i1, i2 = tri[:, 0], tri[:, 1], tri[:, 2]
    for a in range(0, D, chunk):
        b = min(a + chunk, D)
        s = labs[a:b]
        idx = ((s[:, i0].astype(XP.int64) * nlab + s[:, i1]) * nlab + s[:, i2])
        idx += XP.arange(b - a, dtype=XP.int64)[:, None] * (nlab ** 3)
        c = XP.bincount(idx.ravel(), minlength=(b - a) * nlab ** 3)
        out[a:b] = c.reshape(b - a, nlab ** 3).astype(XP.float64)
    return cp.asnumpy(out) if GPU else out


# ---------------------------------------------------------------------------
# floors and summaries
# ---------------------------------------------------------------------------

def multinomial_floor(p_model, N, ndraw, rng):
    """The naive floor, kept only as a DIAGNOSTIC and labelled as one.

    Multinomial resamples of a product model at the raw triple count.  It is
    reported beside the real floor so the gap between them -- the overlap
    penalty -- is visible in the record rather than argued about.
    """
    if N <= 0:
        return np.zeros(ndraw)
    q = np.asarray(p_model, dtype=float).ravel()
    q = q / q.sum()
    return np.array([GS.share_2x2x2(rng.multinomial(N, q).reshape(2, 2, 2))
                     for _ in range(ndraw)])


def product_model(tab):
    """The product of the table's own three single-slot marginals."""
    p = np.asarray(tab, dtype=float)
    p = p / p.sum()
    m = [p.sum(axis=tuple(j for j in range(3) if j != i)) for i in range(3)]
    return np.einsum('i,j,k->ijk', *m)


def summarize(tab, null, mfloor=None):
    """A reading against its EMPIRICAL null, with headroom and occupancy.

    `null` is the vector of control shares from `tables_of_many` -- the same
    triples, relabelled.  The null is chi2-shaped, so it is summarized by
    median / p99 / p-value and never by a median-and-sigma z
    (`share-null-is-chi2-shaped`; the Dalitz D7 near-miss).
    """
    n = float(tab.sum())
    s = GS.share_2x2x2(tab) if n > 0 else float('nan')
    _, head = GS.share_headroom(tab) if n > 0 else (0.0, float('nan'))
    null = np.asarray(null, dtype=float)
    out = dict(
        n_triples=n, share=s,
        null_median=float(np.median(null)), null_mean=float(null.mean()),
        null_p99=float(np.percentile(null, 99)), null_max=float(null.max()),
        null_sd=float(null.std()), n_null=int(len(null)),
        excess=s - float(np.median(null)),
        p_value=float((np.sum(null >= s) + 1) / (len(null) + 1)),
        headroom=head, headroom_ratio=(head / s if s > 0 else float('inf')),
        min_cell=float(tab.min()), occupancy=float((tab > 0).mean()),
        table=tab.ravel().tolist())
    if mfloor is not None and len(mfloor):
        out["multinomial_floor_median"] = float(np.median(mfloor))
        out["overlap_penalty"] = (float(np.median(null) / np.median(mfloor))
                                  if np.median(mfloor) > 0 else float('inf'))
    return out


# ---------------------------------------------------------------------------
# the sweep
# ---------------------------------------------------------------------------

def run_state_point(path, L, templates, tol, args, rng):
    """One state point.  Geometry once per configuration; every label
    assignment -- data, iid control, permutation control, and `ndraw` null draws
    of each -- reads the SAME triples."""
    z = np.load(path, allow_pickle=False)
    pos = z["inherent"] if args.inherent else z["positions"]
    typ = (z["types"] - z["types"].min()).astype(np.int8)      # -> {0, 1, ...}
    nconf = min(args.nconf, pos.shape[0]) if args.nconf else pos.shape[0]
    N = pos.shape[1]
    nlab = int(typ.max()) + 1
    merged = nlab > 2
    if merged:
        typ = (typ > 0).astype(np.int8)                        # merged binary arm
        nlab = 2
    pA = float((typ[:nconf] == 0).mean())
    D = args.ndraw

    data_tabs = {t: np.zeros((nconf, 8)) for t in templates}
    iid_tabs = {t: np.zeros((D, 8)) for t in templates}
    perm_tabs = {t: np.zeros((D, 8)) for t in templates}
    counts = {t: [] for t in templates}
    t0 = time.time()
    for c in range(nconf):
        d2 = pair_dist2(pos[c], L)
        lab_d = XP.asarray(typ[c])
        # D independent iid draws and D independent permutations, for THIS
        # configuration.  Draw d of the null pools draw d from every
        # configuration, so each null draw is a full-ensemble reading.
        li = XP.asarray((rng.random((D, N)) >= pA).astype(np.int8))
        lp = XP.asarray(np.stack([rng.permutation(typ[c]) for _ in range(D)]))
        for t in templates:
            tri = triangles_from_d2(d2, t, tol, rng, cap=args.cap)
            counts[t].append(int(tri.shape[0]))
            if tri.shape[0] == 0:
                continue
            data_tabs[t][c] = table_of(tri, lab_d, nlab).ravel()
            iid_tabs[t] += tables_of_many(tri, li, nlab)
            perm_tabs[t] += tables_of_many(tri, lp, nlab)
        del d2, li, lp
        if GPU and c % 25 == 0:
            cp.get_default_memory_pool().free_all_blocks()
        if c % 50 == 0:
            print(f"    conf {c}/{nconf}  {time.time()-t0:.1f}s", flush=True)
    return dict(data=data_tabs, iid=iid_tabs, perm=perm_tabs, counts=counts,
                pA=pA, nconf=nconf, merged=merged)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--points", default="KA_T0.44,KA_T0.50,KA_T0.56,KA_T0.64")
    ap.add_argument("--nconf", type=int, default=0)
    ap.add_argument("--cap", type=int, default=400000)
    ap.add_argument("--tol", type=float, default=0.10)
    ap.add_argument("--ndraw", type=int, default=200)
    ap.add_argument("--nboot", type=int, default=400)
    ap.add_argument("--inherent", action="store_true")
    ap.add_argument("--templates", default="")
    ap.add_argument("--seed", type=int, default=20260727)
    ap.add_argument("--out", default="glass_stageA.json")
    args = ap.parse_args()

    inv = json.load(open("/home/emoore/CIRISOntology/scratchpad/glass_inventory.json"))
    if args.templates:
        tmpls = [tuple(float(x) for x in g.split(':')) for g in args.templates.split(',')]
    else:
        # the pre-registered equilateral ladder (GLASS_PREREG.md sec 3.4).
        # 1.07 is the measured g_AA first peak and the primary rung; 0.89 is the
        # measured g_AB peak, in deliberately as the LP gate's stress test.
        tmpls = [(r, r, r) for r in
                 (0.89, 1.07, 1.3, 1.5, 1.8, 2.1, 2.5, 3.0, 4.0, 5.0, 6.0)]
    tmpls = [t if len(t) == 3 else (t[0],) * 3 for t in tmpls]

    results = {}
    for pt in args.points.split(','):
        path = f"/home/emoore/CIRISOntology/scratchpad/glass/compact/{pt}.npz"
        if not os.path.exists(path):
            print(f"SKIP {pt}: not present")
            continue
        if pt not in inv:
            print(f"SKIP {pt}: not in glass_inventory.json")
            continue
        L = inv[pt]["box"]
        print(f"\n=== {pt}  L={L:.4f} ===", flush=True)
        # STABLE per-point seed.  `hash()` on a str is salted per process, so
        # an earlier version of this line made every capped template
        # irreproducible between runs -- caught by comparing two Stage A runs,
        # which agreed to the last digit on the UNCAPPED templates and disagreed
        # on every capped one (GATES.md harvest: gate-log provenance).
        rng = np.random.default_rng(args.seed + zlib.crc32(pt.encode()) % 10000)
        S = run_state_point(path, L, tmpls, args.tol, args, rng)
        res = {}
        for t in tmpls:
            key = "%.3f:%.3f:%.3f" % t
            tab = S["data"][t].sum(0).reshape(2, 2, 2)
            n = int(tab.sum())
            if n == 0:
                res[key] = dict(empty=True)
                print(f"  {key}  EMPTY")
                continue
            null_iid = np.array([GS.share_2x2x2(r.reshape(2, 2, 2))
                                 for r in S["iid"][t] if r.sum() > 0])
            null_perm = np.array([GS.share_2x2x2(r.reshape(2, 2, 2))
                                  for r in S["perm"][t] if r.sum() > 0])
            mfl = multinomial_floor(product_model(tab), n, 50, rng)
            row = dict(data=summarize(tab, null_perm, mfl),
                       vs_iid=summarize(tab, null_iid))
            row["null_iid_median"] = float(np.median(null_iid))
            row["null_perm_median"] = float(np.median(null_perm))
            # configuration-level block bootstrap: the independent axis is the
            # configuration, never the pooled triple.
            arr = S["data"][t]
            bs = []
            for _ in range(args.nboot):
                tb = arr[rng.integers(0, len(arr), len(arr))].sum(0)
                if tb.sum() > 0:
                    bs.append(GS.share_2x2x2(tb.reshape(2, 2, 2)))
            row["boot_sd"] = float(np.std(bs)) if bs else float('nan')
            row["boot_lo"] = float(np.percentile(bs, 2.5)) if bs else float('nan')
            row["boot_hi"] = float(np.percentile(bs, 97.5)) if bs else float('nan')
            cc = S["counts"][t]
            row["counts_per_conf"] = dict(
                mean=float(np.mean(cc)), min=int(np.min(cc)), max=int(np.max(cc)),
                capped=int(sum(1 for m in cc if m >= args.cap)))
            res[key] = row
            d = row["data"]
            print(f"  {key}  N={d['n_triples']:.3e}  share={d['share']:.4e}  "
                  f"null={d['null_median']:.3e}  exc={d['excess']:+.4e}  "
                  f"p={d['p_value']:.4f}  head={d['headroom']:.3f}  "
                  f"minc={d['min_cell']:.0f}  bsd={row['boot_sd']:.2e}  "
                  f"ovl={d.get('overlap_penalty', float('nan')):.1f}x", flush=True)
        # write after EVERY state point.  The first version of this script
        # dumped only at the end and lost three completed state points to a
        # KeyError on the fourth.
        results[pt] = dict(L=L, nconf=S["nconf"], pA=S["pA"],
                           merged=S["merged"], templates=res,
                           per_conf_tables={"%.3f:%.3f:%.3f" % t:
                                            S["data"][t].tolist() for t in tmpls})
        json.dump(results, open(
            f"/home/emoore/CIRISOntology/scratchpad/{args.out}", "w"))
        print(f"  [checkpointed {pt}]", flush=True)
    results["_args"] = vars(args)
    json.dump(results, open(
        f"/home/emoore/CIRISOntology/scratchpad/{args.out}", "w"))
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
