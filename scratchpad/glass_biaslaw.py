#!/usr/bin/env python3
"""Checking the water campaign's closed forms against my 400-resample measurements.

They offer two, and invite the check with "a disagreement means the resample is
wrong, not the theory".  Taking that seriously in both directions.

  VARIANCE LAW   rel_sd(ratio) = sqrt(2 + 8*N*share) / (2*N*share)
  BIAS LAW       rel_bias(ratio) ~ c / (N*share),  c = 0.2275 (median) or 0.5 (mean)

Also separates a confound they and I have both been carrying: the ratio has TWO
estimated quantities in it, and the closed forms above are written for the
numerator alone.  The ceiling I(pair;third) is itself a plug-in mutual
information with its own upward bias, which biases the RATIO downward.  This
script measures the share's bias and the ceiling's bias SEPARATELY at the same
planted states, so the ratio's bias can be attributed rather than fitted.
"""
import json
import sys

import numpy as np

sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")
import glass_share as GS   # noqa: E402
from glass_ratiogauge import H, ceiling, planted_state  # noqa: E402


def decompose(p, N, ndraw, rng):
    """Median bias of the share, of the ceiling, and of their ratio."""
    q = np.asarray(p, dtype=float).ravel(); q = q / q.sum()
    sh, cl, ra = np.empty(ndraw), np.empty(ndraw), np.empty(ndraw)
    for i in range(ndraw):
        c = rng.multinomial(N, q).reshape(2, 2, 2)
        sh[i] = GS.share_2x2x2(c)
        cl[i] = ceiling(c)
        ra[i] = sh[i] / cl[i] if cl[i] > 0 else np.nan
    return np.median(sh), np.median(cl), np.median(ra)


def main():
    rng = np.random.default_rng(4242)
    print("=" * 122)
    print("A. THE VARIANCE LAW  sqrt(2+8*N*share)/(2*N*share), against my eight real cells")
    print("=" * 122)
    G = json.load(open("/home/emoore/CIRISOntology/scratchpad/glass_ratiogauge.json"))
    print(f"{'cell':>18s} {'N*share':>10s} {'sd measured':>12s} {'sd law':>9s} "
          f"{'diff (pp)':>10s} {'bias meas':>10s} {'sd/bias':>8s} {'sqrt(Ns)':>9s}")
    rows = []
    for r in G["real_cells"]:
        Ns = r["N_eff"] * r["true_ratio"] * r["ceiling"]
        law = np.sqrt(2 + 8 * Ns) / (2 * Ns)
        rows.append((Ns, r["rel_sd"], law))
        print(f"{r['point'][-4:]+' r='+r['template'].split(':')[0]:>18s} {Ns:10.1f} "
              f"{100*r['rel_sd']:11.2f}% {100*law:8.2f}% "
              f"{100*(r['rel_sd']-law):+9.2f} {100*r['rel_bias']:+9.3f}% "
              f"{abs(r['rel_sd']/r['rel_bias']):8.1f} {np.sqrt(Ns):9.1f}")
    worst = max(abs(a - b) for _, a, b in rows)
    print(f"\n  worst |measured - law| = {100*worst:.2f} percentage points over 8 cells")

    print()
    print("=" * 122)
    print("B. THE BIAS, DECOMPOSED -- is the ratio's bias the SHARE's bias, or the "
          "CEILING's?")
    print("=" * 122)
    print(f"{'N*share':>9s} {'share bias':>11s} {'vs .2275/N':>11s} {'vs .5/N':>9s} "
          f"{'ceil bias':>10s} {'ceil rel':>9s} {'ratio bias':>11s} "
          f"{'share-ceil':>11s}")
    for rho, N in ((0.02, 10**6), (0.05, 10**6), (0.10, 10**6), (0.20, 10**6),
                   (0.10, 10**5), (0.40, 10**6)):
        p, s_true, c_true = planted_state(rho, 0.02)
        ms, mc, mr = decompose(p, N, 600, rng)
        Ns = N * s_true
        sb = (ms - s_true) / s_true                 # relative bias of the share
        cb = (mc - c_true) / c_true                 # relative bias of the ceiling
        rb = (mr - s_true / c_true) / (s_true / c_true)
        print(f"{Ns:9.1f} {100*sb:+10.3f}% {100*0.2275/Ns:10.3f}% "
              f"{100*0.5/Ns:8.3f}% {mc-c_true:+10.2e} {100*cb:+8.4f}% "
              f"{100*rb:+10.3f}% {100*(sb-cb):+10.3f}%")
    print("\n  'share-ceil' is the prediction rel_bias(ratio) = rel_bias(share) "
          "- rel_bias(ceiling);\n  compare it with 'ratio bias'.")


if __name__ == "__main__":
    main()
