"""Docimasia of arm G7b: does the instrument reproduce pump-curve's law on a
synthetic sign-symmetric triple where the law's hypotheses hold exactly?"""
import numpy as np, sys
sys.path.insert(0,"/home/emoore/CIRISOntology/scratchpad")
from planck_pilot_g7b import pump_law, table_from_bits, flip, sign_rho
from dalitz_share import share_2x2x2

rng=np.random.default_rng(5)
N=3_000_000
print(f"{'r_gauss':>8} {'rho':>8} {'p01':>6} {'p10':>6} {'a':>7} {'r0':>7} "
      f"{'pred':>11} {'meas':>11} {'ratio':>8}")
for rg in (0.30, 0.60, 0.85):
    C=np.full((3,3), rg); np.fill_diagonal(C,1.0)
    L=np.linalg.cholesky(C)
    g=(L @ rng.standard_normal((3,N)))
    d=[(x>=0).astype(np.int8) for x in g]          # split at 0 = symmetry centre
    rho,per=sign_rho(*d)
    base=share_2x2x2(table_from_bits(*d))
    # floor at the same N, channel-free
    fl=[]
    for _ in range(12):
        gg=(L @ rng.standard_normal((3,N)))
        dd=[(x>=0).astype(np.int8) for x in gg]
        fl.append(share_2x2x2(table_from_bits(*dd)))
    fmed=float(np.median(fl))
    print(f"  base share {base:.3e}, floor median {fmed:.3e}  rho={rho:.4f} "
          f"(per-pair spread {max(per)-min(per):.1e})")
    for (p01,p10) in ((0.05,0.0),(0.10,0.0),(0.20,0.0),(0.20,0.05),(0.10,0.10)):
        vals=[share_2x2x2(table_from_bits(flip(d[0],p01,p10,rng),
                                          flip(d[1],p01,p10,rng),
                                          flip(d[2],p01,p10,rng))) for _ in range(8)]
        meas=float(np.median(vals))-fmed
        pred,r0,a,s=pump_law(rho,p01,p10)
        rat = meas/pred if pred>0 else float('nan')
        print(f"{rg:8.2f} {rho:8.4f} {p01:6.2f} {p10:6.2f} {a:+7.3f} {r0:7.4f} "
              f"{pred:11.4e} {meas:11.4e} {rat:8.4f}")
