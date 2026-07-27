#!/usr/bin/env python3
"""THE CAP-SUBSAMPLING VARIANCE -- a hole in the null, found by re-running.

Two Stage A runs, differing only in the per-state-point RNG (an unstable
`hash()` seed, now fixed), agreed TO THE LAST DIGIT on the templates whose
triples were not capped and disagreed on EVERY capped one.  That is a diagnosis:

    the empirical null of `glass_run.tables_of_many` holds the TRIPLE SELECTION
    fixed and varies only the labels, so it carries the label noise and the
    triple-overlap structure -- but NOT the variance introduced by the cap's
    random subsampling of the enumerated triples.

For an uncapped template that hole is empty and the null is complete.  For a
capped one it is not, and the p-value is under-stated by however much the
subsampling moves the reading.  This script MEASURES that, by re-reading the
same configurations under several independent cap draws and reporting the
spread of the reading beside the spread of the null.

Nothing here is a new physical measurement; it is a gauge on the instrument.
"""
import argparse
import json
import sys

import numpy as np

sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")
import glass_share as GS   # noqa: E402
import glass_run as GR     # noqa: E402

XP = GR.XP


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--point", default="KA_T0.44")
    ap.add_argument("--nconf", type=int, default=150)
    ap.add_argument("--nseed", type=int, default=8)
    ap.add_argument("--ndraw", type=int, default=60)
    ap.add_argument("--cap", type=int, default=25000)
    ap.add_argument("--tol", type=float, default=0.10)
    ap.add_argument("--templates", default="1.30,1.50,1.80,3.00,5.00,6.00")
    ap.add_argument("--out", default="glass_capnoise.json")
    args = ap.parse_args()

    inv = json.load(open("/home/emoore/CIRISOntology/scratchpad/glass_inventory.json"))
    L = inv[args.point]["box"]
    z = np.load(f"/home/emoore/CIRISOntology/scratchpad/glass/compact/{args.point}.npz",
                allow_pickle=False)
    pos, typ = z["positions"][:args.nconf], z["types"][:args.nconf]
    lab = (typ != typ.min()).astype(np.int8)
    tmpls = [(float(x),) * 3 for x in args.templates.split(',')]
    out = {}

    for t in tmpls:
        shares, nulls, ns, capped = [], [], [], 0
        for s in range(args.nseed):
            rng = np.random.default_rng(90000 + s)
            tab = np.zeros(8)
            ntab = np.zeros((args.ndraw, 8))
            tot = 0
            for c in range(args.nconf):
                d2 = GR.pair_dist2(pos[c], L)
                tri = GR.triangles_from_d2(d2, t, args.tol, rng, cap=args.cap)
                m = int(tri.shape[0])
                tot += m
                if m >= args.cap:
                    capped += 1
                if m:
                    tab += GR.table_of(tri, XP.asarray(lab[c]), 2).ravel()
                    lp = XP.asarray(np.stack(
                        [rng.permutation(lab[c]) for _ in range(args.ndraw)]))
                    ntab += GR.tables_of_many(tri, lp, 2)
                del d2
            shares.append(GS.share_2x2x2(tab.reshape(2, 2, 2)))
            nulls.append(float(np.median(
                [GS.share_2x2x2(r.reshape(2, 2, 2)) for r in ntab])))
            ns.append(tot)
        sh, nu = np.array(shares), np.array(nulls)
        key = "%.2f" % t[0]
        out[key] = dict(
            shares=sh.tolist(), nulls=nu.tolist(), n=ns,
            share_mean=float(sh.mean()), share_sd=float(sh.std()),
            null_median_mean=float(nu.mean()),
            cap_sd_over_null=float(sh.std() / nu.mean()) if nu.mean() > 0 else float('nan'),
            was_capped=bool(capped > 0),
            capped_frac=float(capped / (args.nseed * args.nconf)))
        o = out[key]
        print(f"r={key}  capped={o['was_capped']}({o['capped_frac']:.2f})  "
              f"share={o['share_mean']:.4e} +- {o['share_sd']:.2e}  "
              f"null_med={o['null_median_mean']:.3e}  "
              f"cap_sd/null={o['cap_sd_over_null']:.2f}", flush=True)

    out["_args"] = vars(args)
    json.dump(out, open(f"/home/emoore/CIRISOntology/scratchpad/{args.out}", "w"),
              indent=1)
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
