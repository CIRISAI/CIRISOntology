#!/usr/bin/env python3
"""STAGE B: the pair-matched generative surrogate -- the load-bearing gate.

Pre-registered in GLASS_PREREG.md sec 4.4.

WHAT IT IS.  Hold the POSITIONS fixed -- so geometry, template, tolerance, box,
finite-size effects and the whole selection are byte-identical to the data --
and resample only the SPECIES, from the maximum-entropy distribution over
species assignments whose RADIAL SPECIES CORRELATION matches the data's.

On a fixed point pattern that distribution is an Ising model with radial
couplings,

    P(s) proportional to exp( sum_{i<j} J(r_ij) sigma_i sigma_j ),
    sigma = +-1,  composition conserved exactly,

fitted by iterative Boltzmann inversion on J(r) -- which is Shell's S_rel
programme (JCP 129:144108) used to BUILD the null rather than to fit a model,
and a g2-invariant construction in the species channel in the sense of Torquato
& Stillinger (PRE 68:041113).  It is the same object Reverse Monte Carlo
(McGreevy & Pusztai 1988) produces in the positional channel.

WHY IT IS THE RIGHT NULL AND NOT A ZERO.  This surrogate can and generally WILL
read a nonzero share: a pair ensemble has genuine triplet structure -- that is
the Kirkwood-superposition-violation physics Coslovich measured on this very
model.  The deliverable is the DIFFERENCE between the data and this, not the
data alone.

TWO THEOREMS THAT BEAR ON IT, stated so neither is tripped over:
  * an UNCONSTRAINED Ising model with no field is sign-symmetric, and
    `share_eq_zero_of_signSymmetric` would then make its share EXACTLY zero.
    Conserving the composition at 80:20 breaks that symmetry, which is why the
    surrogate is sampled with composition-conserving swap moves and not with a
    field.  The data carries the same exact-composition constraint, and the
    permutation control of sec 4.2 carries it too.
  * per-cell relabelling of a product state cannot create share
    (`valve_from_nothing`), which is what makes sec 4.1's control a floor and
    not a competitor.
"""
import argparse
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")
import glass_share as GS   # noqa: E402
import glass_run as GR     # noqa: E402

XP, GPU = GR.XP, GR.GPU


def neighbour_bins(pos, L, edges, kmax):
    """Padded neighbour indices and radial-bin indices within edges[-1]."""
    d2 = GR.pair_dist2(pos, L)
    r = XP.sqrt(d2)
    XP.fill_diagonal(r, XP.float32(1e9))
    A = r < XP.float32(edges[-1])
    deg = A.sum(1)
    K = min(int(deg.max()), kmax)
    order = XP.argsort(~A, axis=1, kind='stable')[:, :K].astype(XP.int32)
    rank = XP.arange(K, dtype=XP.int32)[None, :]
    M = rank < XP.minimum(deg, K)[:, None]
    rr = XP.take_along_axis(r, order, axis=1)
    b = XP.searchsorted(XP.asarray(edges, dtype=XP.float32), rr) - 1
    b = XP.clip(b, 0, len(edges) - 2)
    b = XP.where(M, b, len(edges) - 1)          # invalid -> a dead bin
    del d2, r, A
    return order, b.astype(XP.int32), M


def corr_by_bin(nb, bb, sig, nbin):
    """<sigma_i sigma_j> per radial bin and the pair count per bin."""
    s = sig[nb] * sig[:, None]
    w = XP.bincount(bb.ravel(), weights=s.ravel().astype(XP.float64),
                    minlength=nbin + 1)[:nbin]
    c = XP.bincount(bb.ravel(), minlength=nbin + 1)[:nbin].astype(XP.float64)
    return w, c


def mc_sweeps(nb, bb, J, sig, listA, listB, nsweep, nbin):
    """Composition-conserving Metropolis (Kawasaki) on the species labels.

    One A/B swap per configuration per step, vectorised across configurations,
    so every chain is a STRICTLY SEQUENTIAL single-swap chain: there is no
    parallel-update approximation and nothing to defend about detailed balance.

    Swapping i (species +1) with j (species -1) flips both, so
        dlogW = -2*sigma_i*h_i - 2*sigma_j*h_j + 4*J_ij*sigma_i*sigma_j,
    with h_i = sum_k J(r_ik) sigma_k over i's neighbours.

    Two implementation points that are worth 15x and were found by timing rather
    than by guessing.  (1) The A and B particle INDEX LISTS are carried and
    swapped, so every proposal is a genuine A/B exchange; drawing two particles
    uniformly would waste 84% of proposals at 80:20 composition.  (2) The random
    numbers are drawn on the device.  The step is kernel-launch bound, and a
    host-side draw per step costs more than the physics.
    """
    C, N = sig.shape
    K = nb.shape[2]
    Jp = XP.concatenate([J, XP.zeros(1, dtype=XP.float64)])   # dead bin -> 0
    rows = XP.arange(C)
    nA, nB = listA.shape[1], listB.shape[1]
    # FLAT views.  Two-index advanced indexing on a (C, N, K) array goes through
    # cupy's multi-array indexing path and dominated the step time at 8 ms;
    # collapsing (config, particle) into one axis and taking along it is the
    # same arithmetic and measured several times faster.
    nbf = nb.reshape(C * N, K)
    bbf = bb.reshape(C * N, K)
    sigf = sig.reshape(C * N)
    off = rows * N
    for _ in range(nsweep * nB):
        sa = XP.random.randint(0, nA, C)
        sb = XP.random.randint(0, nB, C)
        pi, pj = listA[rows, sa], listB[rows, sb]
        fi, fj = off + pi, off + pj
        nbi, nbj = nbf[fi], nbf[fj]                    # (C, K)
        Ji, Jj = Jp[bbf[fi]], Jp[bbf[fj]]              # (C, K)
        hi = XP.sum(Ji * sigf[off[:, None] + nbi], axis=1)
        hj = XP.sum(Jj * sigf[off[:, None] + nbj], axis=1)
        Jij = XP.sum(XP.where(nbi == pj[:, None], Ji, 0.0), axis=1)
        d = -2.0 * hi + 2.0 * hj - 4.0 * Jij
        acc = XP.random.random(C) < XP.exp(XP.minimum(d, 0.0))
        sigf[fi] = XP.where(acc, -1.0, 1.0)
        sigf[fj] = XP.where(acc, 1.0, -1.0)
        listA[rows, sa] = XP.where(acc, pj, pi)
        listB[rows, sb] = XP.where(acc, pi, pj)
    return sigf.reshape(C, N), listA, listB


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--points", default="KA_T0.44,KA_T0.50,KA_T0.56,KA_T0.64")
    ap.add_argument("--nconf", type=int, default=100)
    ap.add_argument("--kmax", type=int, default=90)
    ap.add_argument("--rcut", type=float, default=2.5)
    ap.add_argument("--dbin", type=float, default=0.10)
    ap.add_argument("--ibi", type=int, default=25)
    ap.add_argument("--alpha", type=float, default=0.5)
    ap.add_argument("--eqsweep", type=int, default=6)
    ap.add_argument("--nrep", type=int, default=40)
    ap.add_argument("--repsweep", type=int, default=3)
    ap.add_argument("--tol", type=float, default=0.10)
    ap.add_argument("--cap", type=int, default=25000)
    ap.add_argument("--templates", default="1.07,1.30,1.50,1.80,2.10,3.00")
    ap.add_argument("--minpairs", type=int, default=20000)
    ap.add_argument("--nmeas", type=int, default=3)
    ap.add_argument("--sens", type=float, default=0.0,
                    help="deliberately DE-converge J by this fraction of the\n                         final residual, to convert the surrogate's\n                         residual pair mismatch into a quoted\n                         systematic on the excess rather than a hope")
    ap.add_argument("--seed", type=int, default=20260727)
    ap.add_argument("--out", default="glass_stageB.json")
    args = ap.parse_args()

    inv = json.load(open("/home/emoore/CIRISOntology/scratchpad/glass_inventory.json"))
    edges = np.arange(0.0, args.rcut + 1e-9, args.dbin)
    nbin = len(edges) - 1
    tmpls = [(float(x),) * 3 for x in args.templates.split(',')]
    out = {}

    for pt in args.points.split(','):
        path = f"/home/emoore/CIRISOntology/scratchpad/glass/compact/{pt}.npz"
        if not os.path.exists(path):
            print(f"SKIP {pt}")
            continue
        rng = np.random.default_rng(args.seed + abs(hash(pt)) % 9973)
        z = np.load(path, allow_pickle=False)
        L = inv[pt]["box"]
        pos = z["positions"][:args.nconf]
        typ = z["types"][:args.nconf]
        C, N = typ.shape
        sig0 = XP.asarray(np.where(typ == typ.min(), 1.0, -1.0))
        print(f"\n=== {pt}  surrogate  C={C} N={N} bins={nbin} ===", flush=True)

        t0 = time.time()
        nb = XP.zeros((C, N, args.kmax), dtype=XP.int32)
        bb = XP.zeros((C, N, args.kmax), dtype=XP.int32)
        K = args.kmax
        for c in range(C):
            o, b, _ = neighbour_bins(pos[c], L, edges, args.kmax)
            k = o.shape[1]
            K = min(K, k)
            nb[c, :, :k], bb[c, :, :k] = o, b
            bb[c, :, k:] = nbin                       # dead bin
        nb, bb = nb[:, :, :K], bb[:, :, :K]
        print(f"  neighbour lists K={K}  [{time.time()-t0:.1f}s]", flush=True)

        # target: <sigma sigma> per radial bin, from the data's own labels
        wt = XP.zeros(nbin, dtype=XP.float64)
        ct = XP.zeros(nbin, dtype=XP.float64)
        for c in range(C):
            w, n = corr_by_bin(nb[c], bb[c], sig0[c], nbin)
            wt += w
            ct += n
        Ctarget = wt / XP.maximum(ct, 1.0)
        # a bin with a handful of pairs has a target of +-1 and is pure noise;
        # it is not fitted and its coupling stays exactly zero.
        live = (ct >= args.minpairs)
        print(f"  live bins {int(live.sum())}/{nbin} "
              f"(>= {args.minpairs} pairs)", flush=True)

        # IBI
        J = XP.zeros(nbin, dtype=XP.float64)
        nBp = int((typ[0] != typ.min()).sum())
        lb = np.stack([rng.permutation(N)[:nBp] for _ in range(C)])
        listB = XP.asarray(lb.astype(np.int32))
        listA = XP.asarray(np.stack([np.setdiff1d(np.arange(N), lb[c])
                                     for c in range(C)]).astype(np.int32))
        sig = XP.ones((C, N), dtype=XP.float64)
        sig[XP.arange(C)[:, None], listB] = -1.0
        hist = []
        Jprev = Cprev = None
        for it in range(args.ibi):
            sig, listA, listB = mc_sweeps(nb, bb, J, sig, listA, listB,
                                          args.eqsweep, nbin)
            # AVERAGE the model correlation over several decorrelated snapshots.
            # A single snapshot's per-bin noise is comparable to the residual we
            # are trying to drive down, so a single-snapshot update chases noise
            # -- which is exactly what a per-bin secant step was measured to do
            # (it gave rms 0.059 at iteration 13 where a plain fixed step gave
            # 0.058 at iteration 11: no improvement, recorded rather than kept).
            Cm = XP.zeros(nbin, dtype=XP.float64)
            for _m in range(args.nmeas):
                if _m:
                    sig, listA, listB = mc_sweeps(nb, bb, J, sig, listA, listB,
                                                  1, nbin)
                wm = XP.zeros(nbin, dtype=XP.float64)
                cm = XP.zeros(nbin, dtype=XP.float64)
                for c in range(C):
                    w, n = corr_by_bin(nb[c], bb[c], sig[c], nbin)
                    wm += w
                    cm += n
                Cm += (wm / XP.maximum(cm, 1.0)) / args.nmeas
            err = XP.where(live, Ctarget - Cm, 0.0)
            Jprev, Cprev = J, Cm
            J = J + XP.where(live, args.alpha * err, 0.0)
            rms = float(XP.sqrt(XP.mean(err[live] ** 2)))
            mx = float(XP.max(XP.abs(err[live])))
            hist.append(dict(it=it, rms=rms, max=mx))
            if it % 5 == 0 or it == args.ibi - 1:
                print(f"  IBI {it:3d}  rms={rms:.5f}  max={mx:.5f}  "
                      f"[{time.time()-t0:.0f}s]", flush=True)

        final_rms, final_max = hist[-1]['rms'], hist[-1]['max']
        if args.sens:
            # push J AWAY from its fit by a controlled amount, so the change in
            # the surrogate's share per unit of pair mismatch is MEASURED
            J = J * (1.0 - args.sens)

        # replicas, read through the byte-identical template pipeline
        rows = {}
        tri_cache = {}
        for c in range(C):
            d2 = GR.pair_dist2(pos[c], L)
            for t in tmpls:
                tri_cache[(c, t)] = GR.triangles_from_d2(d2, t, args.tol, rng,
                                                         cap=args.cap)
            del d2
        tabs = {t: np.zeros((args.nrep, 8)) for t in tmpls}
        dtab = {t: np.zeros(8) for t in tmpls}
        for c in range(C):
            for t in tmpls:
                tri = tri_cache[(c, t)]
                if tri.shape[0]:
                    dtab[t] += GR.table_of(tri, XP.asarray(
                        (typ[c] != typ[c].min()).astype(np.int8)), 2).ravel()
        for rep in range(args.nrep):
            sig, listA, listB = mc_sweeps(nb, bb, J, sig, listA, listB,
                                          args.repsweep, nbin)
            lab = ((sig < 0).astype(XP.int8))
            for c in range(C):
                for t in tmpls:
                    tri = tri_cache[(c, t)]
                    if tri.shape[0]:
                        tabs[t][rep] += GR.table_of(tri, lab[c], 2).ravel()
            if rep % 10 == 0:
                print(f"  replica {rep}/{args.nrep}  [{time.time()-t0:.0f}s]",
                      flush=True)

        for t in tmpls:
            key = "%.3f:%.3f:%.3f" % t
            sd = GS.share_2x2x2(dtab[t].reshape(2, 2, 2))
            ss = np.array([GS.share_2x2x2(r.reshape(2, 2, 2))
                           for r in tabs[t] if r.sum() > 0])
            rows[key] = dict(
                n_triples=float(dtab[t].sum()), share_data=float(sd),
                surrogate_median=float(np.median(ss)),
                surrogate_mean=float(ss.mean()), surrogate_sd=float(ss.std()),
                surrogate_p99=float(np.percentile(ss, 99)),
                surrogate_max=float(ss.max()), n_rep=int(len(ss)),
                excess=float(sd - np.median(ss)),
                p_value=float((np.sum(ss >= sd) + 1) / (len(ss) + 1)))
            r = rows[key]
            print(f"  {key}  data={sd:.4e}  surr={r['surrogate_median']:.4e}"
                  f" +- {r['surrogate_sd']:.2e}  exc={r['excess']:+.4e}  "
                  f"p={r['p_value']:.4f}", flush=True)

        out[pt] = dict(templates=rows, nconf=C, K=int(K),
                       final_rms=final_rms, final_max=final_max,
                       n_live_bins=int(live.sum()), sens=args.sens,
                       J=[float(x) for x in (GR.cp.asnumpy(J) if GPU else J)],
                       edges=edges.tolist(),
                       Ctarget=[float(x) for x in (GR.cp.asnumpy(Ctarget) if GPU else Ctarget)],
                       ibi_history=hist)
        del nb, bb, sig, sig0, tri_cache
        if GPU:
            GR.cp.get_default_memory_pool().free_all_blocks()

    out["_args"] = vars(args)
    json.dump(out, open(f"/home/emoore/CIRISOntology/scratchpad/{args.out}", "w"))
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
