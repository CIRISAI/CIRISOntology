#!/usr/bin/env python3
"""Verifying the pump campaign's EXACT INTERIOR NULL before adopting it.

Their claim (AMENDMENT 10): on a NON-sign-symmetric input, minting by a per-cell
channel is NOT monotone in the channel asymmetry `a`.  It starts nonzero at
a = 0, FALLS as `a` rises, hits a machine-exact zero, and rises again -- the
channel's asymmetry cancelling the state's own -- with the null near the
magnetisation-preserving channel, a_null ~ 2ms = m(1-kappa).

This matters to GLASS_RESULTS.md sec 7a because it is the THIRD correction to the
same guidance and this one INVERTS a design instruction already written there
("bin at the median so d is small"): if the floor is non-monotone in `a`, then
neither "our channel is nearly symmetric" nor its reverse bounds it.

INPUT.  The maximum-entropy state with prescribed <sigma_i> = m and
<sigma_i sigma_j> = r -- the pair exponential family p ~ exp(h*sum(s) +
J*sum_{i<j} s_i s_j).  Being an exponential family in the pair statistics it IS
its own pair-maxent, so its share is exactly zero by construction rather than by
tuning.  Built at this campaign's own measured (m, r) = (0.553, 0.749) from the
r = 1.30, T = 0.44 template.

CHANNEL.  Per-cell, p(0->1) = s + a, p(1->0) = s - a: mean flip rate s,
asymmetry a.  a = 0 is unital.
"""
import sys

import numpy as np
from scipy.optimize import fsolve

sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")
import glass_share as GS   # noqa: E402

S = np.array([1.0, -1.0])


def state(h, J):
    p = np.zeros((2, 2, 2))
    for i in range(2):
        for j in range(2):
            for k in range(2):
                a, b, c = S[i], S[j], S[k]
                p[i, j, k] = np.exp(h * (a + b + c) + J * (a * b + a * c + b * c))
    return p / p.sum()


def moments(p):
    m = float((p.sum((1, 2)) * S).sum())
    r = float(np.einsum('abc,a,b->', p, S, S))
    return m, r


def build(m_t, r_t):
    f = lambda x: np.array(moments(state(*x))) - np.array([m_t, r_t])
    h, J = fsolve(f, [0.5, 0.5], full_output=False)
    return state(h, J), (h, J)


def push(p, s, a):
    K = np.array([[1 - (s + a), s + a], [s - a, 1 - (s - a)]])
    q = np.einsum('abc,ai,bj,ck->ijk', p, K, K, K)
    return q / q.sum()


m_t, r_t = 0.553, 0.749
p, (h, J) = build(m_t, r_t)
m, r = moments(p)
print(f"input: target (m,r)=({m_t},{r_t})  achieved ({m:.6f},{r:.6f})  h={h:.4f} J={J:.4f}")
print(f"       share of the input = {GS.share_2x2x2(p):.3e}   <- must be ~0 by construction")
print()
for s in (0.05, 0.10):
    print(f"=== mean flip rate s = {s} ===")
    print(f"  {'a':>8s} {'minted share':>14s}")
    # FULL range: the magnetisation-preserving channel balances flux
    # (1+m)(s+a) = (1-m)(s-a)  =>  a = -m*s, NEGATIVE in this convention.
    # An earlier version of this scan covered a >= 0 only and reported "no
    # interior null" -- the null was outside the window, not absent.
    grid = sorted(set(np.linspace(-s, s, 81).tolist()))
    vals = []
    for a in grid:
        v = GS.share_2x2x2(push(p, s, a))
        vals.append((a, v))
        print(f"  {a:8.4f} {v:14.4e}")
    lo = min(vals, key=lambda t: t[1])
    # refine around the minimum
    i = [v[0] for v in vals].index(lo[0])
    a0 = vals[max(i - 1, 0)][0]
    a1 = vals[min(i + 1, len(vals) - 1)][0]
    fine = np.linspace(a0, a1, 4001)
    fv = [(a, GS.share_2x2x2(push(p, s, a))) for a in fine]
    best = min(fv, key=lambda t: t[1])
    print(f"  -> minimum at a = {best[0]:.6f}, share = {best[1]:.3e}")
    print(f"     flux-balance prediction a = -m*s = {-m*s:.6f}   "
          f"ratio measured/predicted = {best[0]/(-m*s):.3f}")
    print(f"     their quoted form 2ms = {2*m*s:.6f} (sign/factor convention differs)")
    print(f"     monotone in a? {'NO' if best[1] < vals[0][1] and best[1] < vals[-1][1] else 'yes'}")
    print()
