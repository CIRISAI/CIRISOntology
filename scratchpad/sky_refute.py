"""Two checks of the convergent-art warning, run AFTER the main pilot.

C1. Is the order-3 whole-only share the same object as negentropy?  The total
    third-order negentropy (Jones & Sibson 1987 multivariate Edgeworth) is
        J3 = (1/12) zeta_ijk zeta_lmn A^il A^jm A^kn,      A = C^-1,
    a positive-definite quadratic form in the third cumulants.  The bridge is
        I  = (1/2) (A_1a A_2b A_3c zeta_abc)^2 / perm(A),
    a single squared LINEAR functional.  If they were the same object they would
    agree; if the share is only the pairwise-blind PART, J3 must stay positive on a
    field whose share is exactly zero.

C2. Static nonlinearity.  A one-sided clip is a monotone per-cell map.  Which route
    does it damage?
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, sky_pilot as sp

def J3(C, zeta):
    A = np.linalg.inv(np.asarray(C, float))
    return float(np.einsum('ijk,lmn,il,jm,kn->', zeta, zeta, A, A, A)) / 12.0

print("=" * 78)
print("C1  IS THE SHARE THE SAME OBJECT AS NEGENTROPY?  Exact lognormal, true share = 0")
print("=" * 78)
a = (0.5, 0.5, 0.5)
C0, _ = sp.latent_C_zeta(a, 0.0)
print(f"{'sigma_g':>8} {'1pt skew':>9} {'J3 (negentropy, Jones-Sibson)':>30} {'bridge (this pilot)':>21} {'ratio':>10}")
rows = []
for sig in [1.0, 0.5, 0.3, 0.1, 0.03, 0.01]:
    Cx = np.exp(sig**2 * C0) - 1.0
    Z = np.zeros((3, 3, 3))
    for i in range(3):
        for j in range(3):
            for k in range(3):
                Z[i, j, k] = (np.exp(sig**2*(C0[i,j]+C0[i,k]+C0[j,k]))
                              - np.exp(sig**2*C0[i,j]) - np.exp(sig**2*C0[i,k])
                              - np.exp(sig**2*C0[j,k]) + 2.0)
    j3, br = J3(Cx, Z), sp.route_B(Cx, Z)[0]
    sk = Z[0,0,0]/Cx[0,0]**1.5
    rows.append(dict(sigma_g=sig, skew=sk, J3=j3, bridge=br, ratio=br/j3))
    print(f"{sig:8.3f} {sk:9.4f} {j3:30.6e} {br:21.6e} {br/j3:10.3e}")
print("\n  TRUE share of every row above: 0 (exactly, by the pointwise-transform theorem,")
print("  verified at 1.3e-16 in the main run).  A quantity that equals the share must")
print("  therefore vanish here.")

print()
print("=" * 78)
print("C2  STATIC NONLINEARITY: which route does a one-sided clip damage?")
print("=" * 78)
xp, on_gpu = sp.get_xp(True)
N, L, R = 256, 1000.0, 8.0
kk = sp.kgrid(N, L, xp)
T = xp.asarray(sp.eh_nowiggle_T(kk.get() if hasattr(kk, 'get') else kk))
out = []
for q in [None, 0.99, 0.95, 0.90]:
    A_, B_, bits_diff, skews = [], [], [], []
    for rr in range(6):
        w = sp.white_noise(N, 20260725 + 1000*rr, xp)
        f = sp.make_field('gauss', 0.0, w, kk, T, 0.96, R, xp)
        s0, _ = sp.binarise(f, xp)
        if q is not None:
            thr = float(xp.quantile(f, q))
            f = xp.minimum(f, thr)          # one-sided clip: a MONOTONE per-cell map
        sb, _ = sp.binarise(f, xp)
        bits_diff.append(int((sb != s0).sum().get() if on_gpu else (sb != s0).sum()))
        v = float((f*f).mean()) - float(f.mean())**2
        skews.append(float(((f - f.mean())**3).mean()) / v**1.5)
        d1, d2 = sp.cfg_disp(4, 'T')
        A_.append(sp.share3_ref(sp.triple_hist_iso(sb, 4, 'T', xp)))
        Cm, Zm = sp.triple_cumulants(f, d1, d2, xp)
        B_.append(sp.route_B(Cm, Zm)[0])
        del f, sb, s0, w
        if on_gpu: xp.get_default_memory_pool().free_all_blocks()
    out.append(dict(clip=q, skew=float(np.mean(skews)),
                    bits_changed=int(max(bits_diff)),
                    A=float(np.mean(A_)), A_sem=float(np.std(A_, ddof=1)/np.sqrt(len(A_))),
                    B=float(np.mean(B_)), B_sem=float(np.std(B_, ddof=1)/np.sqrt(len(B_)))))
    o = out[-1]
    lab = 'unclipped' if q is None else f'clip at q={q}'
    print(f"  {lab:>14}: 1pt skew {o['skew']:+8.4f}  binary cells changed {o['bits_changed']:>9d}"
          f"  |  Route A {o['A']:.4e} +- {o['A_sem']:.1e}   Route B {o['B']:.4e} +- {o['B_sem']:.1e}")
b0 = out[0]
print("\n  ratio to the unclipped Gaussian (truth is UNCHANGED -- clipping is a per-cell map):")
for o in out[1:]:
    print(f"    clip q={o['clip']}:  Route A x{o['A']/b0['A']:6.3f}    Route B x{o['B']/b0['B']:9.1f}")
json.dump(dict(C1=rows, C2=out), open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
          'sky_refute.json'), 'w'), indent=1, default=float)
