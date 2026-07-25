"""array_negentropy_cliptest.py — the readout-saturation exposure test.

Written AFTER the main run, in response to the sibling convergent-art check (commit e601aec,
CORRECTION 3): "The static-nonlinearity trap lands on route B, not route A ... Being
moment-native is the exposure, not the protection."

That correction is tested here directly on THIS pipeline and on the real CIRISArray kernel,
rather than assumed to transfer or assumed not to.  A one-sided readout clip at quantile q is
a per-channel monotone NON-STRICT map applied to the READOUT (the dynamics is untouched).  By
the transform theorem the true share is unchanged for a strictly monotone map; a clip is not
strictly monotone -- it creates a tie block -- so all three routes are being asked how they
behave under a coarse-graining they are all formally entitled to be changed by.

Three routes on identical data:
  (A) median-binarized shareK          -- array_cap_experiment
  (B) the bridge WITHOUT rank-Gaussianization (standardize only)
  (C) the bridge WITH rank-Gaussianization  -- this repository's instrument

Usage:  python3 array_negentropy_cliptest.py
"""
import sys, os, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import array_negentropy as AN
import array_cap_experiment as ACE


def routes(chans):
    """(C) rank-Gaussianized bridge, (B) standardize-only bridge, on cupy channels."""
    import cupy as cp
    g = [AN.gaussianize(c) for c in chans]
    M = AN.moment_tensor(*g)[None]
    C = np.array([[[1., M[0, 1, 1, 0], M[0, 1, 0, 1]],
                   [M[0, 1, 1, 0], 1., M[0, 0, 1, 1]],
                   [M[0, 1, 0, 1], M[0, 0, 1, 1], 1.]]])
    wC = float(AN.coord_deg3_closed(M, C)[0])
    g2 = [(c - c.mean()) / c.std() for c in chans]
    M2 = AN.moment_tensor(*g2)[None]
    C2 = np.array([[[1., M2[0, 1, 1, 0], M2[0, 1, 0, 1]],
                    [M2[0, 1, 1, 0], 1., M2[0, 0, 1, 1]],
                    [M2[0, 1, 0, 1], M2[0, 0, 1, 1], 1.]]])
    return wC, float(AN.coord_deg3_closed(M2, C2)[0])


def main():
    import cupy as cp
    drv = AN.Driver(8, 64)
    out = []
    for (kap, sig, bnd) in ((0.05, 1e-3, 'fold'), (0.05, 1e-3, 'clip')):
        R = drv.raw_states(kap, sig, bnd, 20260725, 2000, 64)
        print(f"\n=== kappa={kap} sigma={sig} {bnd} — one-sided readout clip at quantile q ===")
        print(" q      skew        (C) rank-route     ratio   (B) no-gauss      ratio   "
              "(A) binarized      ratio   tie_block")
        base = {}
        for q in (1.0, 0.99, 0.98, 0.95, 0.90, 0.80, 0.75):
            wc, wb, bs = [], [], []
            for t in range(24):
                ch = [R[t, 1].copy(), R[t + 1, 1].copy(), R[t + 2, 1].copy()]
                if q < 1.0:
                    for c in ch:
                        thr = cp.quantile(c.astype(cp.float64), q).astype(c.dtype)
                        cp.minimum(c, thr, out=c)
                a, b = routes(ch)
                wc.append(a); wb.append(b)
                if t < 8:
                    bs.append(ACE.analyze([cp.asnumpy(c).astype(np.float64) for c in ch],
                                          'bin', do_null=False)['share'])
            c0 = R[0, 1].astype(cp.float64)
            if q < 1.0:
                c0 = cp.minimum(c0, cp.quantile(c0, q))
            z0 = (c0 - c0.mean()) / c0.std()
            sk = float(cp.asnumpy((z0 ** 3).mean()))
            tie = 0.0 if q == 1.0 else round(1.0 - q, 4)
            sC = 0.5 * np.mean(wc) ** 2
            sB = 0.5 * np.mean(wb) ** 2
            sA = float(np.mean(bs))
            if q == 1.0:
                base = dict(C=sC, B=sB, A=sA)
            print(f" {q:<6} {sk:+.4f}     {sC:.4e}      {sC/base['C']:6.3f}   {sB:.4e}"
                  f"      {sB/base['B']:6.3f}   {sA:.4e}       {sA/base['A']:6.3f}   {tie:.3f}")
            out.append(dict(kappa=kap, sigma=sig, boundary=bnd, q=q, skew=sk,
                            s_rank=sC, s_nogauss=sB, s_binarized=sA,
                            r_rank=sC / base['C'], r_nogauss=sB / base['B'],
                            r_bin=sA / base['A'], tie_block=tie))
        del R
        cp.get_default_memory_pool().free_all_blocks()
    with open(os.path.join(HERE, 'array_negentropy_cliptest.json'), 'w') as f:
        json.dump(out, f, indent=1, default=float)
    print("\nThe pre-registered rail threshold (0.01) is exactly the guard against this "
          "channel:\nevery tie block above corresponds to a rail fraction of 1-q, so q < 0.99 "
          "is already\nexcluded by the rule frozen before the run.")


if __name__ == '__main__':
    main()
