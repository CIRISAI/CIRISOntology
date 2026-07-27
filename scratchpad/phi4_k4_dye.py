"""K4's GAUGE GATE — can the mixture null manufacture the structure it is meant to gauge?

GATES.md, family 3 (mixture / manufacture): "a gauge gate: the mixture null must be able to
*manufacture* the data's generative structure, or it gauges nothing."  K4 on the ridge peak
returns a mixture share 200x BELOW the measured share, with the fit degenerating to a single
component (mu -> 0).  Two readings of that are possible and they are opposite:

  (a) the ridge is genuinely NOT a latent-binary-mode mixture, or
  (b) the fit is broken and K4 gauges nothing.

This file decides between them by planting states the null SHOULD recover:

  D1  a state drawn from the mixture family itself, at several (w, mu).  If the fit cannot
      recover its own family, K4 is void and reading (b) holds.
  D2  the ridge's own measured pair marginals with a planted two-component structure of
      the size the ridge actually carries -- i.e. the same test at the RIGHT amplitude,
      because a null that recovers big structure and misses small structure is no gauge at
      the size that matters.
  D3  a pure single-copula state (mu = 0 truth): the fit must return share ~ the copula's,
      which is the null's own floor.

Nothing here is fitted to a result.  It is a dye test, and it either licenses K4's reading
or voids it.
"""
import sys, os, math, json
import numpy as np
from scipy import special
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from phi4_fastcop import cells_vec
from phi4_k4 import mixture_fast
from ising_field import share3


def plant(a0, rho, w, mu):
    m = w * cells_vec(a0 - mu, *rho) + (1 - w) * cells_vec(a0 + mu, *rho)
    return m / m.sum()


print("=" * 92)
print("K4 GAUGE GATE — plant, then ask the null to recover")
print("=" * 92)

rng = np.random.default_rng(4242)

print("\nD1 — states drawn from the mixture family itself")
print(f"  {'w':>6s} {'mu':>6s} {'true share':>13s} {'fitted share':>13s} {'ratio':>7s} "
      f"{'fit rms':>10s} {'w_hat':>7s} {'mu_hat':>7s}")
a0 = np.array([0.0, 0.0, 0.0])
rho = [0.35, 0.20, 0.35]
worst = 0.0
for w in (0.5, 0.3):
    for mu in (0.05, 0.15, 0.4, 1.0):
        p = plant(a0, rho, w, mu)
        st = float(share3(p)[0])
        m, prm, rms = mixture_fast(p)
        sm = float(share3(m)[0])
        rat = sm / st if st > 0 else float('nan')
        if st > 1e-9:
            worst = max(worst, abs(rat - 1))
        print(f"  {w:6.2f} {mu:6.2f} {st:13.4e} {sm:13.4e} {rat:7.3f} {rms:10.2e} "
              f"{prm['w']:7.3f} {prm['mu']:7.3f}")

print("\nD2 — the SAME test at the ridge's own marginals and its own amplitude.")
print("     a0 and rho are taken from the measured L=16 peak state; mu is tuned so the")
print("     planted share matches the measured share (3.3e-05 nats).  This asks whether")
print("     the null can gauge structure OF THE SIZE ACTUALLY PRESENT.")
rows = json.load(open('phi4_ridge.json'))
r0 = [r for r in rows if r['L'] == 16 and abs(r['u'] - 1.4994) < 1e-3][0]
cnt = np.asarray(r0['counts']['theta0']['colin-r'], float).sum(axis=0)
pm = cnt / cnt.sum()
import phi4_ridge as P
_, prm0 = P.fit_copula(pm)
a_m = np.array(prm0['a']); rho_m = prm0['rho']
print(f"  measured state: a = {np.round(a_m,4)}  rho = {np.round(rho_m,4)}  "
      f"share = {float(share3(pm)[0]):.4e}")
print(f"  {'mu':>6s} {'true share':>13s} {'fitted share':>13s} {'ratio':>7s} {'fit rms':>10s}")
for mu in (0.01, 0.02, 0.05, 0.1, 0.3):
    p = plant(a_m, rho_m, 0.5, mu)
    st = float(share3(p)[0])
    m, prm, rms = mixture_fast(p)
    sm = float(share3(m)[0])
    print(f"  {mu:6.3f} {st:13.4e} {sm:13.4e} {sm/st if st>0 else float('nan'):7.3f} "
          f"{rms:10.2e}")

print("\nD3 — a pure single-copula state (truth mu = 0): the fit must return the copula's")
print("     own share, i.e. the null's floor, and must NOT invent a mixture.")
p = cells_vec(a_m, *rho_m); p = p / p.sum()
st = float(share3(p)[0])
m, prm, rms = mixture_fast(p)
print(f"  true {st:.4e}   fitted {float(share3(m)[0]):.4e}   "
      f"w_hat {prm['w']:.3f}  mu_hat {prm['mu']:.4f}  rms {rms:.2e}")

print("\n" + "=" * 92)
print(f"  D1 worst |ratio - 1| over the planted family: {worst:.3f}")
print("  If D1 and D2 recover their plants, K4's reading on the data stands and the ridge")
print("  is NOT a latent-binary-mode mixture.  If they do not, K4 GAUGES NOTHING here and")
print("  its verdict on the data must be withdrawn as UNGAUGED.")
print("=" * 92)
