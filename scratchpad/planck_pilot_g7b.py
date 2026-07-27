#!/usr/bin/env python3
"""
ARM G7b — the pump rate law as a forward prediction on real sky geometry.

Declared in PLANCK_PILOT_AMENDMENT_5.md section 2.1 before it was run.

WHY THIS ARM EXISTS.  `pump-curve` states the licensing conditions for a valve
prediction: the noise must be a SAME-ALPHABET per-cell channel, and the
binarization must be LUMPABLE with respect to it.  PREREG section 6.7's arm adds
continuous noise to a continuous field and binarizes afterwards, so
binarize(x+e) is not a function of binarize(x) and condition (b) fails.  This arm
reverses the order: the channel is applied to the ALREADY-BINARIZED slots, so the
alphabet IS the partition, lumpability is trivial, and `valve_needs_asymmetry`
applies.

THE LAW UNDER TEST — `pump-curve`'s, not this pilot's.  scratchpad/PUMP_RESULTS.md,
commit 2dc6cfc.  For three binary slots with sign-symmetric pair structure, a
per-cell channel of asymmetry a = p01 - p10 and strength s = (p01 + p10)/2:

    share = 18 r0^4 a^2 / [(1 + 2 r0)(1 + 3 r0)(1 - r0)],   r0 = (1 - 2 s)^2 rho

ZERO FREE PARAMETERS.  rho is MEASURED from the sky triples, not fitted.  The
equilateral templates E032, E064, E128 supply three values of rho the pump
campaign did not choose.  Only equilateral templates are used: the law assumes a
single r0, i.e. all three pair correlations equal, and the folded and squeezed
families do not have that.  Excluded by construction, not by result.

Scratchpad only.  No Lean, no Stance.lean, no audit, no `lake`.
"""
import json, os, sys, time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from planck_pilot import (load_planck, load_idx, Surrogates, share_2x2x2,  # noqa: E402
                          OUT, dump, null_shape)

TAGS = ["E032", "E064", "E128"]          # equilateral only — see the docstring
# (p01, p10) grid: asymmetry a = p01-p10, strength s = (p01+p10)/2.
# The SMALL-a rows are the primary comparison: `pump-curve`'s closed form is
# exact as a -> 0 and their correction coefficient c is DEFINED as
# lim_{a->0} delta/a^2, so a test at a = 0.2 tests the closed form plus an
# a^4 term neither campaign has measured.  Large a retained to reproduce the
# deviation curve, not to judge the law.
CHANNELS = [(0.01, 0.00), (0.02, 0.00), (0.03, 0.00), (0.05, 0.00),
            (0.10, 0.00), (0.20, 0.00),
            (0.05, 0.01), (0.10, 0.02), (0.20, 0.05),
            (0.10, 0.10), (0.20, 0.20)]   # the last two are SYMMETRIC: a = 0
N_REAL = 24                                # realisations per channel setting
N_FLOOR = 60                               # channel-free floor, same N

# `pump-curve`'s measured correction coefficient, PUMP_AMENDMENT_4 section 4.1,
# commit fbcb3ea, pump_correction_c.json.  exact = closed * (1 + c(r0) a^2 + ...).
# c is NOT constant: a basin near r0 ~ 0.36 rising steeply at high correlation.
PUMP_C_R0 = [0.04, 0.09, 0.16, 0.25, 0.36, 0.49, 0.64, 0.81]
PUMP_C = [4.53, 4.08, 3.62, 3.23, 3.01, 3.13, 4.42, 14.4]


def c_of_r0(r0):
    """Log-linear interpolation of pump-curve's c(r0).  Extrapolation is refused
    rather than guessed: outside the measured grid this returns None and the row
    is reported without a corrected prediction."""
    if r0 < PUMP_C_R0[0] or r0 > PUMP_C_R0[-1]:
        return None
    return float(np.interp(r0, PUMP_C_R0, PUMP_C))


def pump_law(rho, p01, p10):
    a = p01 - p10
    s = 0.5 * (p01 + p10)
    r0 = (1.0 - 2.0 * s) ** 2 * rho
    den = (1.0 + 2.0 * r0) * (1.0 + 3.0 * r0) * (1.0 - r0)
    closed = 18.0 * r0 ** 4 * a ** 2 / den
    c = c_of_r0(r0)
    corrected = closed * (1.0 + c * a * a) if c is not None else None
    return closed, r0, a, s, c, corrected


def table_from_bits(d1, d2, d3):
    idx = (d1.astype(np.int64) * 2 + d2) * 2 + d3
    return np.bincount(idx, minlength=8).astype(float).reshape(2, 2, 2)


def flip(d, p01, p10, rng):
    """Per-cell binary channel: 0 -> 1 with p01, 1 -> 0 with p10.  Independent
    across slots and across cells; same alphabet in and out."""
    u = rng.random(d.size)
    out = d.copy()
    z = d == 0
    out[z] = (u[z] < p01).astype(np.int8)
    o = ~z
    out[o] = (u[o] >= p10).astype(np.int8)
    return out


def sign_rho(d1, d2, d3):
    """Pair correlation of the +-1 sign variables, and its three-way spread.
    The law assumes one rho; the spread is reported so the assumption is visible."""
    s1, s2, s3 = 2.0 * d1 - 1, 2.0 * d2 - 1, 2.0 * d3 - 1
    r = [float(np.mean(s1 * s2)), float(np.mean(s1 * s3)), float(np.mean(s2 * s3))]
    return float(np.mean(r)), r


def main():
    print("ARM G7b — pump rate law as a forward prediction", flush=True)
    _, Iinp, M, _ = load_planck()
    idx = load_idx("planck")
    surr = Surrogates(Iinp, 2048, 4096, "planck")
    del Iinp, M
    rng = np.random.default_rng(88001)
    out = {"law": "18 r0^4 a^2 / ((1+2r0)(1+3r0)(1-r0)), r0=(1-2s)^2 rho",
           "credit": "pump-curve, scratchpad/PUMP_RESULTS.md, commit 2dc6cfc",
           "templates": TAGS, "n_real": N_REAL, "rows": []}

    # one surrogate map -> binarized slots per template (sign-symmetric, share ~ 0)
    base = surr.s1(np.random.default_rng(88000))
    bits, rhos = {}, {}
    for t in TAGS:
        i1, i2, i3 = idx[t]
        x1, x2, x3 = base[i1], base[i2], base[i3]
        thr = float(np.median(np.concatenate([x1, x2, x3])))
        d = [(x >= thr).astype(np.int8) for x in (x1, x2, x3)]
        bits[t] = d
        rhos[t] = sign_rho(*d)
        print(f"  {t}: n={d[0].size}  rho={rhos[t][0]:.5f}  "
              f"per-pair {np.round(rhos[t][1],5)}", flush=True)
    out["rho"] = {t: {"mean": rhos[t][0], "per_pair": rhos[t][1]} for t in TAGS}

    # channel-free floor at the SAME N, from independent surrogate maps
    print("  floor (channel-free, same N)...", flush=True)
    fl = {t: [] for t in TAGS}
    for i, sd in enumerate(np.random.SeedSequence(88100).spawn(N_FLOOR)):
        m = surr.s1(np.random.default_rng(sd))
        for t in TAGS:
            i1, i2, i3 = idx[t]
            x1, x2, x3 = m[i1], m[i2], m[i3]
            thr = float(np.median(np.concatenate([x1, x2, x3])))
            dd = [(x >= thr).astype(np.int8) for x in (x1, x2, x3)]
            fl[t].append(share_2x2x2(table_from_bits(*dd)))
    out["floor"] = {t: null_shape(np.array(fl[t])) for t in TAGS}
    for t in TAGS:
        print(f"    {t}: floor median {out['floor'][t]['median']:.4e} "
              f"p99 {out['floor'][t]['p99']:.4e}", flush=True)

    t0 = time.time()
    for (p01, p10) in CHANNELS:
        for t in TAGS:
            d1, d2, d3 = bits[t]
            vals = []
            for _ in range(N_REAL):
                e1 = flip(d1, p01, p10, rng)
                e2 = flip(d2, p01, p10, rng)
                e3 = flip(d3, p01, p10, rng)
                vals.append(share_2x2x2(table_from_bits(e1, e2, e3)))
            v = np.array(vals)
            rho = rhos[t][0]
            closed, r0, a, s, cc, corrected = pump_law(rho, p01, p10)
            fmed = out["floor"][t]["median"]
            meas = float(np.median(v)) - fmed          # floor subtracted
            row = {"p01": p01, "p10": p10, "a": a, "s": s, "rho": rho, "r0": r0,
                   "template": t, "n": int(d1.size),
                   "measured_median_raw": float(np.median(v)),
                   "floor_median": fmed,
                   "measured_minus_floor": meas,
                   "predicted_closed": closed,
                   "c_of_r0": cc,
                   "predicted_corrected": corrected,
                   "ratio_vs_closed": (meas / closed) if closed > 0 else None,
                   "ratio_vs_corrected": (meas / corrected)
                   if (corrected and corrected > 0) else None,
                   "scatter": float(np.std(v, ddof=1)),
                   "sem": float(np.std(v, ddof=1) / np.sqrt(v.size))}
            out["rows"].append(row)
            r = row["ratio_vs_closed"]; rc = row["ratio_vs_corrected"]
            print(f"  a={a:+.3f} s={s:.3f} {t} rho={rho:.4f} r0={r0:.4f} "
                  f"c={('%.2f' % cc) if cc else ' n/a'} "
                  f"closed={closed:.4e} meas={meas:.4e} "
                  f"m/closed={('%.4f' % r) if r else 'n/a(a=0)'} "
                  f"m/corr={('%.4f' % rc) if rc else 'n/a'}",
                  flush=True)
    print(f"  {time.time()-t0:.0f}s", flush=True)
    dump("g7b_pump_law.json", out)
    return out


if __name__ == "__main__":
    main()
