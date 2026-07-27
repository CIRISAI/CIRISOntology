#!/usr/bin/env python3
"""Verifying the pump campaign's STATE-AXIS law before adopting it.

Their correction: there are two pump axes, and the one governing a
non-sign-symmetric substrate is NOT the one they first described.

  channel axis  detuned CHANNEL, sign-symmetric input, needs an ASYMMETRIC
                channel, kappa^8 suppression, DIVERGES as noise -> 0.
  state axis    detuned STATE, non-sign-symmetric input, a UNITAL channel
                suffices, and the claimed law is

                    Delta = 8 d^2 k^6 (1-k^2) / [(1+2k^2)(1+3k^2)]

                which VANISHES as noise -> 0 and PEAKS at k ~ 0.80, i.e. s ~ 0.10.

Checked here rather than adopted on report, because it is about to be written
into GLASS_RESULTS.md sec 7a as guidance to whoever runs the Voronoi/q6 arm.

TEST STATE.  w on (0,0,0) and (1-w) on (1,1,1): perfectly agreeing bits, share
exactly zero, and sign-symmetric exactly at w = 1/2.  The detuning is d = w-1/2.
Channel: the binary symmetric channel, flip probability s, applied per cell --
UNITAL, i.e. exactly the innocent-looking kind, with k = 1-2s.
"""
import sys

import numpy as np

sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")
import glass_share as GS   # noqa: E402


def bsc_push(p, s):
    """Push a 2x2x2 state through three independent BSC(s) kernels."""
    K = np.array([[1 - s, s], [s, 1 - s]])
    q = np.einsum('abc,ai,bj,ck->ijk', p, K, K, K)
    return q / q.sum()


def state(w):
    p = np.zeros((2, 2, 2))
    p[0, 0, 0] = w
    p[1, 1, 1] = 1 - w
    return p


def law(d, k):
    return 8 * d**2 * k**6 * (1 - k**2) / ((1 + 2 * k**2) * (1 + 3 * k**2))


print("=" * 96)
print("1. THE INPUTS: share is exactly zero, and sign-symmetry holds only at w=1/2")
print("=" * 96)
for w in (0.5, 0.6, 0.8, 0.95):
    p = state(w)
    ss = max(abs(p[a, b, c] - p[1-a, 1-b, 1-c])
             for a in (0, 1) for b in (0, 1) for c in (0, 1))
    print(f"  w={w:.2f}  d={w-0.5:+.2f}  share={GS.share_2x2x2(p):.3e}  "
          f"max|p(s)-p(-s)|={ss:.3f}  {'SIGN-SYMMETRIC' if ss < 1e-12 else 'not sign-symmetric'}")

print()
print("=" * 96)
print("2. A UNITAL CHANNEL ON A SIGN-SYMMETRIC INPUT (w=1/2): must mint EXACTLY zero")
print("=" * 96)
worst = 0.0
for s in (0.01, 0.05, 0.10, 0.20, 0.30, 0.45):
    v = GS.share_2x2x2(bsc_push(state(0.5), s))
    worst = max(worst, v)
    print(f"  s={s:.2f}  share={v:.3e}")
print(f"  worst = {worst:.3e}   -> valve_needs_asymmetry holds where its hypothesis holds")

print()
print("=" * 96)
print("3. THE SAME UNITAL CHANNEL ON A NON-SIGN-SYMMETRIC INPUT: does it mint, and "
      "where does it peak?")
print("=" * 96)
for w in (0.6, 0.8):
    d = w - 0.5
    print(f"\n  w={w:.2f}  (detuning d={d:+.2f})")
    print(f"  {'s':>6s} {'kappa':>7s} {'measured':>11s} {'law':>11s} {'ratio':>8s}")
    best = (0, -1)
    for s in (0.001, 0.005, 0.01, 0.02, 0.05, 0.08, 0.10, 0.12, 0.15, 0.20,
              0.30, 0.40, 0.49):
        k = 1 - 2 * s
        m = GS.share_2x2x2(bsc_push(state(w), s))
        L = law(d, k)
        print(f"  {s:6.3f} {k:7.3f} {m:11.4e} {L:11.4e} {m/L if L > 0 else np.nan:8.3f}")
        if m > best[1]:
            best = (s, m)
    print(f"  -> measured peak at s = {best[0]:.3f} (kappa = {1-2*best[0]:.3f}), "
          f"share = {best[1]:.4e}")

print()
print("=" * 96)
print("4. THE QUADRATIC-IN-DETUNING CLAIM, at the peak")
print("=" * 96)
s0 = 0.10
for d in (0.01, 0.02, 0.05, 0.10, 0.20):
    m = GS.share_2x2x2(bsc_push(state(0.5 + d), s0))
    print(f"  d={d:5.2f}  share={m:.4e}   share/d^2={m/d**2:.4e}")
print("  (a constant share/d^2 column is the quadratic law)")
