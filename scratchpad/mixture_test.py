"""Is the ECA noise spike the PUBLISHED mixture mechanism?

Kahle, Olbrich, Jost & Ay (PRE 79, 026201, 2009) found a peak in exactly our
quantity, I^(k) = D(P||E_{k-1}) - D(P||E_k), as a function of coupling on tent-map
lattices, and diagnosed the mechanism:

  "the unordered state shows the same I vector as the region left of the peak, while
   the periodic sequences of course have I concentrated in I^(2) ... If the two types
   of sequences are mixed then higher order correlations appear, leading to the peak."

So: does a naive convex mixture of the deterministic distribution with the fully
noisy (uniform) one already reproduce the biphasic curve we report? If yes, our
"noise creates order-3" is mechanically the published mixture effect. If the real
noise curve differs from the mixture curve in shape, height or location, it is not.
"""
import sys, numpy as np
sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad')
import cupy as cp
import eca_spike as E
import eca_exact as X

LN2 = np.log(2.0)
NST = X.NST
bitidx = E.BITIDX if hasattr(E, 'BITIDX') else None


def share(p3):
    s, q, err, it = E.shareK3_batch(p3.reshape(1, 2, 2, 2))
    return float(cp.asnumpy(s)[0])


def bit_index():
    idx = cp.arange(NST, dtype=cp.int64)
    return [((idx >> j) & 1) for j in range(X.N_CELLS)]


BIT = bit_index()

# headline readings from ECA_SPIKE_RESULTS.md
#   rule 25  SPATIAL 1-2-14 -> slots (0, 1, 3)
#   rule 58  SPATIAL 1-1-15 -> slots (0, 1, 2)
#   rule 46  SPATIAL 1-2-14 -> slots (0, 1, 3)
CASES = [(25, (0, 1, 3), 'SPATIAL 1-2-14'),
         (58, (0, 1, 2), 'SPATIAL 1-1-15'),
         (46, (0, 1, 3), 'SPATIAL 1-2-14')]

PN = [0.0] + [2.0 ** (-k) for k in range(11, 0, -1)]  # 0, 1/2048 ... 1/2

print("Real noise sweep vs. convex-mixture surrogate, I_C^(3) in nats, exact\n")
for rule, (i, j, k), tag in CASES:
    # real: propagate with noise at each level
    real = []
    for p in PN:
        v, perm, idx = X.stationary(rule, p, 400)
        real.append(share(X.triple_from_v(v, i, j, k, BIT)))
    # mixture surrogate: the P_n=0 triple mixed with the P_n=1/2 triple
    v0, _, _ = X.stationary(rule, 0.0, 400)
    p_det = X.triple_from_v(v0, i, j, k, BIT)
    p_unif = cp.full((2, 2, 2), 0.125, dtype=cp.float64)
    mix = [share((1 - lam) * p_det + lam * p_unif) for lam in np.linspace(0, 1, 41)]

    r = np.array(real)
    m = np.array(mix)
    print(f"rule {rule:3d}  {tag}")
    print(f"   real   : det={r[0]:.6e}  peak={r.max():.6e} at P_n={PN[int(r.argmax())]:.3e}"
          f"  end={r[-1]:.3e}")
    print(f"   mixture: det={m[0]:.6e}  peak={m.max():.6e} at lam={np.linspace(0,1,41)[m.argmax()]:.3f}"
          f"  end={m[-1]:.3e}")
    print(f"   ratio real-peak / mixture-peak = {r.max()/max(m.max(),1e-300):.3g}")
    print()
