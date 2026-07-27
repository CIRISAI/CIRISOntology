#!/usr/bin/env python3
"""PIPELINE CALIBRATION -- the docimasia applied to the whole chain, not just the
estimator.

`glass_gate.py` examined the estimator on tables.  This examines the FULL chain:
real geometry, real template selection, real triple overlap, real pooling over
configurations, and the empirical null of `glass_run.tables_of_many`.

Three things are measured, and one candidate check was DISCARDED as vacuous
rather than banked:

  A. THE NULL'S SHAPE -- mean/median and p99/median of the control's share.
     The null is expected chi2_1-like (mean ~2.2x median, p99 ~14x median), and
     if it is, then p-values are the only permitted summary and a
     median-and-sigma z is forbidden (`share-null-is-chi2-shaped`).

  B. THE OVERLAP PENALTY -- the null median against 1/(2N).  This is the factor
     by which the naive multinomial floor understates the real one because
     enumerated triples share particles.

  C. THE DIFFERENCE TEST, which is what the campaign's verdict actually rests
     on.  Split one ensemble at random in half, read the share on each half, and
     score the difference against the configuration-level bootstrap error bar.
     The two halves are draws from the SAME distribution, so an honest error bar
     puts |z| <= 1.96 about 95% of the time.  If the bootstrap under-covers,
     every "5 sigma" in this campaign is inflated by a known factor and the
     kills K2 and P5 are unenforceable as written.

  DISCARDED: a Kolmogorov-Smirnov test on leave-one-out p-values.  It returned
  KS = 0.000 against a critical value of 0.124 -- perfectly uniform -- and that
  is because a leave-one-out p-value IS a rank, so its uniformity is a tautology
  and not evidence about the pipeline.  It is recorded here rather than quietly
  dropped.  (Its one useful by-product survives: the p-value that `glass_run.py`
  quotes is an EXACT rank test under exchangeability, not an asymptotic one.)

Runs on SYNTHETIC positions only.  No real configuration is read here.
"""
import argparse
import json
import sys
import time

import numpy as np

sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")
import glass_share as GS      # noqa: E402
import glass_run as GR        # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nconf", type=int, default=40)
    ap.add_argument("--K", type=int, default=120)
    ap.add_argument("--N", type=int, default=4096)
    ap.add_argument("--tol", type=float, default=0.10)
    ap.add_argument("--seed", type=int, default=20260727)
    ap.add_argument("--mode", default="ideal", choices=("ideal", "lj"))
    ap.add_argument("--nrep", type=int, default=60)
    ap.add_argument("--nboot", type=int, default=60)
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)
    L = (args.N / 1.2) ** (1 / 3)
    nB = int(round(0.2 * args.N))
    tmpls = [(r, r, r) for r in (1.07, 1.5, 3.0)]

    pos = (rng.random((args.nconf, args.N, 3)) - 0.5) * L
    if args.mode == "lj":
        # a crude excluded-volume point pattern, so the overlap structure of the
        # triples is at least qualitatively like a liquid's
        for c in range(args.nconf):
            for _ in range(30):
                d = pos[c][:, None, :] - pos[c][None, :, :]
                d -= L * np.round(d / L)
                r2 = np.einsum('ijk,ijk->ij', d, d)
                np.fill_diagonal(r2, 1e9)
                bad = r2 < 0.81
                f = (d * (bad / np.maximum(r2, 1e-6))[:, :, None]).sum(1)
                pos[c] += 0.02 * f
                pos[c] -= L * np.round(pos[c] / L)

    base = np.zeros(args.N, dtype=np.int8)
    base[:nB] = 1
    out = {}
    t0 = time.time()
    for t in tmpls:
        key = "%.2f" % t[0]
        percf = np.zeros((args.nconf, args.K, 8))
        counts = []
        for c in range(args.nconf):
            d2 = GR.pair_dist2(pos[c], L)
            tri = GR.triangles_from_d2(d2, t, args.tol, rng, cap=None)
            counts.append(int(tri.shape[0]))
            if tri.shape[0] == 0:
                continue
            labs = GR.XP.asarray(np.stack(
                [rng.permutation(base) for _ in range(args.K)]))
            percf[c] = GR.tables_of_many(tri, labs, 2)
            del d2, labs
        tabs = percf.sum(0)
        sh = np.array([GS.share_2x2x2(r.reshape(2, 2, 2)) for r in tabs])
        N = float(tabs[0].sum())

        # C. the difference test, on the quantity the verdict rests on
        zs, half = [], args.nconf // 2
        for _ in range(args.nrep):
            perm = rng.permutation(args.nconf)
            k = rng.integers(0, args.K)
            a, b = perm[:half], perm[half:2 * half]
            sa = GS.share_2x2x2(percf[a, k].sum(0).reshape(2, 2, 2))
            sb = GS.share_2x2x2(percf[b, k].sum(0).reshape(2, 2, 2))
            bo = []
            for _ in range(args.nboot):
                ia = a[rng.integers(0, half, half)]
                ib = b[rng.integers(0, half, half)]
                bo.append(GS.share_2x2x2(percf[ia, k].sum(0).reshape(2, 2, 2)) -
                          GS.share_2x2x2(percf[ib, k].sum(0).reshape(2, 2, 2)))
            sd = float(np.std(bo))
            if sd > 0:
                zs.append((sa - sb) / sd)
        zs = np.array(zs)
        out[key] = dict(
            n_triples=N, triples_per_conf=float(np.mean(counts)),
            share_median=float(np.median(sh)), share_mean=float(sh.mean()),
            share_p99=float(np.percentile(sh, 99)),
            mean_over_median=float(sh.mean() / np.median(sh)),
            p99_over_median=float(np.percentile(sh, 99) / np.median(sh)),
            inv2N=1.0 / (2 * N), overlap_penalty=float(np.median(sh) * 2 * N),
            z_sd=float(zs.std()), z_mean=float(zs.mean()),
            cover95=float((np.abs(zs) <= 1.96).mean()), n_rep=int(len(zs)))
        o = out[key]
        print(f"r={key}  Ntri={N:.3e}  med={o['share_median']:.3e}  "
              f"mean/med={o['mean_over_median']:.2f}  p99/med={o['p99_over_median']:.1f}  "
              f"overlap={o['overlap_penalty']:.1f}x  "
              f"z_sd={o['z_sd']:.2f} z_mean={o['z_mean']:+.2f} "
              f"cover95={o['cover95']:.2f}  [{time.time()-t0:.0f}s]", flush=True)
    out["_args"] = vars(args)
    json.dump(out, open("/home/emoore/CIRISOntology/scratchpad/glass_calib.json", "w"),
              indent=1)
    ok = all(0.80 <= v["cover95"] <= 1.0 and v["z_sd"] < 1.5
             for k, v in out.items() if k != "_args")
    print("\nCALIBRATION", "PASS" if ok else "FAIL (bootstrap error bar dishonest)")


if __name__ == "__main__":
    main()
