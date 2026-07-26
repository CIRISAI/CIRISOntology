"""array_negentropy_size.py — the finite-size / window-drift check of ADDENDUM2 sec 2.

Pre-registered in ARRAY_NEGENTROPY_PREREG_ADDENDUM2.md (b611a5b) before this file existed.
Discriminator: s3 is quadratic in a moment and its estimator bias falls as 1/T (subtracted),
so drift in s3 that is NOT tracked by drift in kappa_111 or rho_pair is an estimator /
finite-size effect on the share quantity, not dynamics.  Bar: <10% over the 16x range in T.
"""
import sys, os, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import array_negentropy as AN

def reading_at(rows, cols, kap, sig, bnd, slots, settle=2000, nframes=128, seed=20260725):
    drv = AN.Driver(rows, cols)
    G, rails, cr = drv.run(kap, sig, bnd, seed, settle, nframes)
    r = AN.reading(G, slots)
    C = np.array(r['C_mean']); mx = max(abs(C[0,1]), abs(C[0,2]), abs(C[1,2]))
    del G
    import cupy as cp; cp.get_default_memory_pool().free_all_blocks()
    return dict(T=drv.T, s_deb=r['s_deb'], kappa111=r['kappa111'], rho=float(mx),
                z=r['z'], rail=float(rails[:, :, 0].max()))

SPECS = [('T3d1 @ k=0.05 (OUTSIDE regime)', 0.05, 1e-3, [(0,1),(1,1),(2,1)]),
         ('S3   @ k=0.16 (inside)',         0.16, 1e-3, [(0,0),(0,1),(0,2)]),
         ('C3   @ k=0.14 (inside)',         0.14, 1e-3, [(0,0),(1,1),(2,2)]),
         ('T3d4 @ k=0.05 (inside, tail)',   0.05, 1e-3, [(0,1),(4,1),(8,1)])]

def main():
    out = []
    for (lab, kap, sig, slots) in SPECS:
        print(f"\n=== {lab} ===")
        print("   n_oss       T      s3          ratio    kappa_111   ratio    max|rho|   z")
        base = None
        for (rows, cols) in ((2, 64), (8, 64), (32, 64)):
            r = reading_at(rows, cols, kap, sig, 'fold', slots)
            if base is None: base = r
            print(f"   {rows*cols:<7} {r['T']:>7}  {r['s_deb']:+.4e}  {r['s_deb']/base['s_deb']:6.3f}"
                  f"   {r['kappa111']:+.5f}   {r['kappa111']/base['kappa111']:6.3f}   "
                  f"{r['rho']:.4f}   {r['z']:+8.1f}")
            r.update(label=lab, kappa=kap, sigma=sig, n_oss=rows*cols); out.append(r)
        sub = [x for x in out if x['label'] == lab]
        d = abs(sub[-1]['s_deb'] - sub[0]['s_deb']) / max(abs(sub[0]['s_deb']), 1e-300)
        dk = abs(sub[-1]['kappa111'] - sub[0]['kappa111']) / max(abs(sub[0]['kappa111']), 1e-300)
        dr = abs(sub[-1]['rho'] - sub[0]['rho']) / max(sub[0]['rho'], 1e-300)
        print(f"   drift over 16x in T:  s3 {d*100:+.1f}%   kappa_111 {dk*100:+.1f}%   "
              f"rho {dr*100:+.1f}%   -> {'STABLE' if d < 0.10 else 'SIZE-DEPENDENT'}"
              f" ({'tracked by the moments' if d <= 2.2*dk + 0.02 else 'NOT tracked by the moments'})")
    with open(os.path.join(HERE, 'array_negentropy_size.json'), 'w') as f:
        json.dump(out, f, indent=1, default=float)

if __name__ == '__main__':
    main()
