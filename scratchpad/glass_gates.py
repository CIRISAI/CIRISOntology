#!/usr/bin/env python3
"""G-BINMINT and the fine-geometry LP -- the two gates on the one coarse-graining
this design still has.

Pre-registered in GLASS_PREREG.md sec 5.2.  The species alphabet is atomic, so
the label carries no binning.  What DOES carry binning is the GEOMETRY: the
shell tolerance is a coarse-graining of a continuum, and merging fine radial
sub-bins is exactly the operation that mints share (Kahle, Olbrich, Jost & Ay,
PRE 79:026201).

THE FINE OBJECT.  Slot m carries the pair (species_m, radial sub-bin of ONE
incident edge), under the fixed assignment rule

    slot 1 <- edge(1,2),  slot 2 <- edge(2,3),  slot 3 <- edge(3,1),

so every edge is carried by exactly one slot and the three slots remain a
genuine 3-slot object.  Alphabet 2*b_r per slot.

  * THE PEDESTAL.  Take the fine table's pair-maxent, MERGE it to the analysis
    alphabet (sum out the radial sub-bin), and read the share of the merged
    distribution.  That number is share manufactured by the merge and by nothing
    else.  This is the sky campaign's own binmint construction
    (REFUTER_RESULTS.md sec A9a) ported to this alphabet.

  * THE FINE LP.  The exact range the COARSE share can occupy over every
    distribution carrying the FINE pair marginals -- `kappa_edge.py`'s
    `t_range_given_fine_marginals` ported here.  If the range collapses, the
    coarse reading was determined before three-way structure was consulted.

Both maxent solves are done TWICE, by IPF and by a dual/L-BFGS solve, and
disagreement above 1e-9 in H(Q) VOIDs the rung (GLASS_PREREG.md sec 5.5); IPF is
never used alone (`ipf-sharek-boundary-drift`).
"""
import argparse
import json
import os
import sys
import time

import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")
import glass_share as GS   # noqa: E402
import glass_run as GR     # noqa: E402

XP, GPU = GR.XP, GR.GPU


def pair_margs(P):
    return [P.sum(2), P.sum(1), P.sum(0)]


def ipf_maxent(P, iters=20000, tol=1e-14):
    """Maximum-entropy distribution carrying P's three pair marginals, by IPF."""
    tg = pair_margs(P / P.sum())
    n = P.shape[0]
    Q = np.ones_like(P, dtype=float) / P.size
    for it in range(iters):
        e = 0.0
        for ax, T in zip((2, 1, 0), tg):
            M = Q.sum(ax)
            R = np.divide(T, M, out=np.zeros_like(T), where=M > 0)
            Q = Q * np.expand_dims(R, ax)
            e = max(e, float(np.abs(M - T).max()))
        Q /= Q.sum()
        if e < tol:
            break
    return Q, it, e


def dual_maxent(P):
    """The same object by its DUAL: Q ~ exp(f12 + f13 + f23), minimising
    log Z(f) - <f, targets>.  An independent solver, so the bracket in
    GLASS_PREREG.md sec 5.5 is two-sided rather than one fitted answer."""
    P = P / P.sum()
    n = P.shape[0]
    t12, t13, t23 = pair_margs(P)

    def unpack(x):
        a = x[:n * n].reshape(n, n)
        b = x[n * n:2 * n * n].reshape(n, n)
        c = x[2 * n * n:].reshape(n, n)
        return a, b, c

    def obj(x):
        a, b, c = unpack(x)
        E = a[:, :, None] + b[:, None, :] + c[None, :, :]
        m = E.max()
        W = np.exp(E - m)
        Z = W.sum()
        f = np.log(Z) + m - (np.sum(a * t12) + np.sum(b * t13) + np.sum(c * t23))
        Q = W / Z
        g = np.concatenate([(Q.sum(2) - t12).ravel(), (Q.sum(1) - t13).ravel(),
                            (Q.sum(0) - t23).ravel()])
        return f, g

    r = minimize(obj, np.zeros(3 * n * n), jac=True, method='L-BFGS-B',
                 options=dict(maxiter=8000, ftol=1e-18, gtol=1e-14))
    a, b, c = unpack(r.x)
    E = a[:, :, None] + b[:, None, :] + c[None, :, :]
    W = np.exp(E - E.max())
    return W / W.sum(), r


def merge_species(Q, br):
    """Sum the radial sub-bin out of each slot: (2*br)^3 -> 2^3."""
    n = Q.shape[0]
    return Q.reshape(2, br, 2, br, 2, br).sum(axis=(1, 3, 5))


def fine_lp(P, br):
    """Exact range of the COARSE parity coordinate over every distribution
    carrying P's FINE pair marginals.  Linear objective, linear equalities."""
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix
    n = P.shape[0]
    P = P / P.sum()
    # the coarse parity character, lifted to the fine alphabet
    chi = np.array([[[1., -1.], [-1., 1.]], [[-1., 1.], [1., -1.]]])
    T = np.repeat(np.repeat(np.repeat(chi, br, 0), br, 1), br, 2).ravel()
    rows, cols, vals, rhs, r = [], [], [], [], 0
    for (i, j) in ((0, 1), (0, 2), (1, 2)):
        M = P.sum(3 - i - j)
        k = 3 - i - j
        for a in range(n):
            for c_ in range(n):
                idx = [0, 0, 0]
                for m in range(n):
                    idx[i], idx[j], idx[k] = a, c_, m
                    rows.append(r)
                    cols.append((idx[0] * n + idx[1]) * n + idx[2])
                    vals.append(1.0)
                rhs.append(M[a, c_])
                r += 1
    A = coo_matrix((vals, (rows, cols)), shape=(r, n ** 3))
    out = {}
    for sense, tag in ((1.0, 'min'), (-1.0, 'max')):
        res = linprog(sense * T, A_eq=A, b_eq=np.array(rhs), bounds=(0, None),
                      method='highs')
        out[tag] = float(sense * res.fun) if res.success else float('nan')
        out[tag + '_ok'] = bool(res.success)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--points", default="KA_T0.44,KA_T0.50,KA_T0.56,KA_T0.64")
    ap.add_argument("--nconf", type=int, default=150)
    ap.add_argument("--templates", default="1.07,1.30,1.50,1.80,3.00")
    ap.add_argument("--br", default="2,3,4")
    ap.add_argument("--tol", type=float, default=0.10)
    ap.add_argument("--cap", type=int, default=25000)
    ap.add_argument("--seed", type=int, default=20260727)
    ap.add_argument("--out", default="glass_gates.json")
    args = ap.parse_args()

    inv = json.load(open("/home/emoore/CIRISOntology/scratchpad/glass_inventory.json"))
    tmpls = [(float(x),) * 3 for x in args.templates.split(',')]
    brs = [int(x) for x in args.br.split(',')]
    out = {}

    for pt in args.points.split(','):
        path = f"/home/emoore/CIRISOntology/scratchpad/glass/compact/{pt}.npz"
        if not os.path.exists(path):
            print(f"SKIP {pt}")
            continue
        rng = np.random.default_rng(args.seed + 7)
        z = np.load(path, allow_pickle=False)
        L = inv[pt]["box"]
        pos, typ = z["positions"][:args.nconf], z["types"][:args.nconf]
        C, N = typ.shape
        lab = (typ != typ.min()).astype(np.int8)
        print(f"\n=== {pt}  gates  C={C} ===", flush=True)
        rows = {}
        t0 = time.time()
        for t in tmpls:
            for br in brs:
                nfine = 2 * br
                fine = np.zeros((nfine, nfine, nfine))
                for c in range(C):
                    d2 = GR.pair_dist2(pos[c], L)
                    tri = GR.triangles_from_d2(d2, t, args.tol, rng, cap=args.cap)
                    if tri.shape[0] == 0:
                        del d2
                        continue
                    # the three edge lengths, sub-binned within the shell
                    e = []
                    for (u, v) in ((0, 1), (1, 2), (2, 0)):
                        rr = XP.sqrt(d2[tri[:, u], tri[:, v]])
                        q = XP.clip(((rr - (t[0] - args.tol)) /
                                     (2 * args.tol) * br).astype(XP.int32), 0, br - 1)
                        e.append(q)
                    s = XP.asarray(lab[c])[tri]
                    slot = [s[:, m].astype(XP.int32) * br + e[m] for m in range(3)]
                    idx = (slot[0] * nfine + slot[1]) * nfine + slot[2]
                    cnt = XP.bincount(idx, minlength=nfine ** 3)
                    fine += (GR.cp.asnumpy(cnt) if GPU else cnt).reshape(
                        (nfine,) * 3).astype(float)
                    del d2
                n = float(fine.sum())
                if n == 0:
                    continue
                coarse = merge_species(fine / n, br)
                s_data = GS.share_2x2x2(coarse)
                Qi, it, err = ipf_maxent(fine / n)
                Qd, r_ = dual_maxent(fine / n)
                Hi, Hd = GS.entropy(Qi.ravel()), GS.entropy(Qd.ravel())
                ped_i = GS.share_2x2x2(merge_species(Qi, br))
                ped_d = GS.share_2x2x2(merge_species(Qd, br))
                occ = float((fine > 0).mean())
                key = f"{t[0]:.2f}|b{br}"
                rows[key] = dict(
                    n_triples=n, share_coarse=float(s_data),
                    pedestal_ipf=float(ped_i), pedestal_dual=float(ped_d),
                    pedestal_frac=float(ped_d / s_data) if s_data > 0 else float('nan'),
                    H_ipf=float(Hi), H_dual=float(Hd), dH=float(abs(Hi - Hd)),
                    ipf_iters=int(it), ipf_err=float(err),
                    cert_ok=bool(abs(Hi - Hd) < 1e-9),
                    occupancy=occ, min_cell=float(fine.min()))
                if br == brs[-1] and occ > 0.3:
                    try:
                        rows[key]["fine_lp"] = fine_lp(fine / n, br)
                    except Exception as exc:            # pragma: no cover
                        rows[key]["fine_lp_error"] = str(exc)
                r = rows[key]
                print(f"  {key}  N={n:.3e} share={s_data:.4e} "
                      f"ped={ped_d:.4e} ({100*r['pedestal_frac']:.1f}%) "
                      f"dH={r['dH']:.2e} occ={occ:.2f} "
                      f"[{time.time()-t0:.0f}s]", flush=True)
        out[pt] = rows
    out["_args"] = vars(args)
    json.dump(out, open(f"/home/emoore/CIRISOntology/scratchpad/{args.out}", "w"),
              indent=1)
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
