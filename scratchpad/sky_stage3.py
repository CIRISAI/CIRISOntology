#!/usr/bin/env python3
"""
sky_stage3.py -- STAGE 3 controls, and the quantity G10's threshold is expressed in.

WHY THIS RUNS BEFORE G10 IS SCORED.  The pre-registration sets G10's bar at "10 % of the
SIGNAL".  The Patchy mocks carry gravity AND the pipeline's manufactured terms, so a mock
reading is not a floor measurement and cannot supply that denominator by itself.  The floor
is what the identical pipeline reads on a field with matched two-point structure and NO
gravitational higher-order structure -- i.e. the Gaussian control, which the prereg schedules
as Stage 3.  So Stage 2's verdict and Stage 3's control interlock, and the control runs first.

THE CONTROL.  A Gaussian field on the analysis grid with P(k) tuned so its post-pipeline
sigma at R = 15 matches the mocks', then POISSON-SAMPLED through the random catalogue so it
carries the same window, the same n-bar(z), the same fibre-collision weighting and the same
shot-noise level as a mock.  Its underlying field is Gaussian, hence sign-symmetric, so its
b = 2 whole-only share is EXACTLY zero by share_eq_zero_of_signSymmetric -- while at b >= 3
its connected information is NOT zero, because a binned Gaussian has a discretisation
artifact (SKY_PILOT_RESULTS.md section 3).  That artifact is precisely the bias the primary
statistic subtracts, so this control is the subtraction, not a null.

Note it is also the VALVE configuration: a per-cell stochastic channel (Poisson) acting on a
pair-structured field.  Core/Valve.lean says minting is possible there, and my own campaign
measured it.  The control therefore carries the shot-noise minting too, which is what makes
it the right floor.

BLINDING: reads Patchy randoms and the Stage 2 mock summaries only.  Never the real
catalogue.
"""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sky_realdata import F32, sky_to_cart, log                       # noqa: E402
from sky_stage2 import CapGeometry, RS, BS, _load_ascii, DATA        # noqa: E402
from sky_forecast import pk_lin                                      # noqa: E402
import tarfile                                                       # noqa: E402


def gaussian_delta(geo, amp, seed):
    """Gaussian field on the analysis grid with P(k) = amp * P_lin(k)."""
    g = geo.g
    rng = np.random.default_rng(seed)
    w = rng.standard_normal(g.N).astype(F32)
    k = np.sqrt(g.k2)
    P = (amp * pk_lin(np.maximum(k.astype(np.float64), 1e-6))).astype(np.float32)
    P[0, 0, 0] = 0.0
    Vcell = g.cell ** 3
    f = g.inv(g.fwd(w) * np.sqrt(np.maximum(P, 0.0) / Vcell).astype(np.float32)).astype(F32)
    del w, P, k
    return f


def sample_control(geo, ran_pos, ran_w, n_target, amp, seed):
    """Poisson-sample the randoms with (1 + delta_G): same window, same n-bar(z), same shot
    noise as a mock, with a GAUSSIAN underlying field."""
    g = geo.g
    dG = gaussian_delta(geo, amp, seed)
    idx = np.floor((ran_pos - g.lo) / g.cell).astype(np.int64)
    for i in range(3):
        np.clip(idx[:, i], 0, g.N[i] - 1, out=idx[:, i])
    lam = 1.0 + dG[idx[:, 0], idx[:, 1], idx[:, 2]]
    del dG, idx
    np.clip(lam, 0.0, None, out=lam)
    p = (n_target / max(float((lam * ran_w).sum()), 1e-30)) * lam * ran_w
    rng = np.random.default_rng(seed + 1)
    keep = rng.random(len(p)) < p
    del p, lam
    return ran_pos[keep], ran_w[keep]


def load_randoms(cap):
    p = f"{DATA}/Patchy-Mocks-Randoms-DR12{cap}-COMPSAM_V6C_x50.tar.gz"
    tf = tarfile.open(p, 'r|gz')
    m = next(iter(tf))
    raw = tf.extractfile(m).read()
    tf.close()
    a = _load_ascii(raw, 7)
    del raw
    sel = a[:, 5] > 0.5
    pos = sky_to_cart(a[sel, 0], a[sel, 1], a[sel, 2]).astype(np.float32)
    w = a[sel, 6].astype(np.float64)
    del a
    return pos, w


def run(cap, n_ctrl=32, seed0=20260726, out=None):
    st2 = json.load(open(f"{HERE}/sky_stage2_{cap}.json"))
    sig_target = {R: float(np.mean([r[str(R)]['sigma'] if str(R) in r else r[R]['sigma']
                                    for r in st2['res']])) for R in RS}
    ngal = None
    log(f"STAGE 3 CONTROL  cap={cap}  mocks' sigma: "
        + "  ".join(f"R={R:.0f}: {sig_target[R]:.4f}" for R in RS))
    geo = CapGeometry(cap)
    ran_pos, ran_w = load_randoms(cap)
    # galaxy count of one mock, to match the shot-noise level
    tf = tarfile.open(f"{DATA}/Patchy-Mocks-DR12{cap}-COMPSAM_V6C.tar.gz", 'r|gz')
    m = next(iter(tf)); raw = tf.extractfile(m).read(); tf.close()
    a = _load_ascii(raw, 8); del raw
    sel = a[:, 6] > 0.5
    ngal = float(a[sel, 7].sum()); del a
    log(f"  target weighted galaxy count = {ngal:.0f}; randoms = {len(ran_w)}")

    # --- tune the amplitude so the control's post-pipeline sigma matches the mocks' ---
    amp, R0 = 1.0, RS[0]
    for it in range(6):
        pos, w = sample_control(geo, ran_pos, ran_w, ngal, amp, seed0)
        r = geo.measure(pos, w, bs=[4], rs=[R0])
        s = r[R0]['sigma']
        log(f"  amp tune {it}: amp={amp:.4f} -> sigma={s:.4f} (target {sig_target[R0]:.4f})")
        del pos, w
        if abs(s / sig_target[R0] - 1) < 0.02:
            break
        amp *= (sig_target[R0] / s) ** 2
    log(f"  ADOPTED amp = {amp:.4f}")

    res = []
    t0 = time.time()
    for i in range(n_ctrl):
        pos, w = sample_control(geo, ran_pos, ran_w, ngal, amp, seed0 + 100 * (i + 1))
        r = geo.measure(pos, w, bs=BS, rs=RS)
        del pos, w
        res.append(r)
        if out and (len(res) % 4 == 0 or len(res) == n_ctrl):
            json.dump(dict(cap=cap, n=len(res), amp=amp, sigma_target=sig_target,
                           ngal=ngal, res=res), open(out, 'w'), default=float)
        if (i + 1) % 4 == 0:
            log(f"    control {i+1}/{n_ctrl}  {(time.time()-t0)/(i+1):.1f}s each")
    return geo, res, amp


if __name__ == '__main__':
    cap = sys.argv[1] if len(sys.argv) > 1 else 'SGC'
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 32
    op = sys.argv[3] if len(sys.argv) > 3 else f"{HERE}/sky_stage3_{cap}.json"
    run(cap, n, out=op)
