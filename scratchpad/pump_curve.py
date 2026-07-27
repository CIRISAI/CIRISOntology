#!/usr/bin/env python3
"""PUMP campaign instrument — the rate at which per-cell noise mints whole-only share.

Pre-registration: scratchpad/PUMP_PREREG.md (commit 64028fb), frozen before this
file was written.  Prior art: scratchpad/PUMP_PRIOR_ART.md (commit 8125797).

COORDINATES (prereg section 1).  A per-cell binary kernel is two numbers:
    p01 = P(read 0 | was 1)      p10 = P(read 1 | was 0)
    asymmetry  a = p01 - p10     strength  s = (p01 + p10)/2
    feasible   |a| <= 2*min(s, 1-s)
In the +-1 basis this is exactly `z -> kappa*z + b` with kappa = 1 - 2s, b = a,
which is the argument convention of qpu_habit_pipeline.apply_product_channel.

SOLVERS (prereg section 5.2).  At k = 3 two independent exact methods must agree
to 1e-12 nat on every configuration:
  * golden section on H(p + t*chi) along the parity-character line, the method of
    scratchpad/temporal-share/SHEARER_NUMERIC.py;
  * bisection on the stationarity condition p000*p011*p110*p101 =
    p001*p010*p100*p111, the method of qpu_habit_pipeline.pairwise_maxent_exact,
    IMPORTED rather than reimplemented.
At k >= 4 the certificate is two-sided: any theta gives a rigorous UPPER bound
log Z(theta) - theta.mu on the envelope entropy (Gibbs), and the fitted maxent
state's own entropy is a LOWER bound once its moment residual is discharged.
IPF is run alongside and reported as a third number, never as the answer.

Usage:  qenv/bin/python pump_curve.py <stage>
        stages: dye curveA curveB curveC dose qpu sampled coarse all
"""
import itertools
import json
import math
import os
import sys
import time

os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")

import numpy as np
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "temporal-share"))
import qpu_habit_pipeline as QP          # noqa: E402  (the repository's own solver)

LN2 = math.log(2.0)
SEED = 20260727

# pre-registered gates
SOLVER_BRACKET_K3 = 1e-12
SOLVER_BRACKET_KGE4 = 1e-6
OCCUPANCY_FLOOR = 1e-12
EXPANSION_VALID_A = 0.25
# AMENDMENT 1: the instrument's DEPTH, measured not assumed.  The k = 3 two-solver
# bracket came back at 6.6e-14 nat over 20000 random states (pump_dye.json), so a
# reading below 100x that is not resolved.  A reading below the depth is UNGAUGED
# -- not zero, not a detection (GATES.md reach 11).
SHARE_DEPTH = 1e-11


# ---------------------------------------------------------------------------
# entropy, channels, states
# ---------------------------------------------------------------------------

def entropy(p):
    q = np.asarray(p, dtype=float).ravel()
    nz = q > 0
    return float(-(q[nz] * np.log(q[nz])).sum())


def kernel(a, s):
    """The 2x2 per-cell kernel K[y, x] from (asymmetry, strength).

    Index 0 = bit value 0, index 1 = bit value 1.
    p01 = K[0, 1] = P(out 0 | in 1);  p10 = K[1, 0] = P(out 1 | in 0)."""
    p01 = s + a / 2.0
    p10 = s - a / 2.0
    if not (-1e-15 <= p01 <= 1 + 1e-15 and -1e-15 <= p10 <= 1 + 1e-15):
        raise ValueError(f"infeasible kernel a={a} s={s} -> p01={p01} p10={p10}")
    p01 = min(max(p01, 0.0), 1.0)
    p10 = min(max(p10, 0.0), 1.0)
    return np.array([[1.0 - p10, p01], [p10, 1.0 - p01]])


def apply_percell(p, kernels):
    """Push a k-slot state through one kernel per slot.  No kernel reads any slot
    but its own -- this is Core/Valve.lean's channel3, at general k."""
    out = np.asarray(p, dtype=float)
    k = out.ndim
    for q in range(k):
        out = np.moveaxis(np.tensordot(kernels[q], out, axes=([1], [q])), 0, q)
    return out


def repetition(k):
    """The k-slot repetition code: half on all-zeros, half on all-ones.
    Sign-symmetric, so whole-only share exactly zero (share_ferro at k = 3)."""
    p = np.zeros((2,) * k)
    p[(0,) * k] = 0.5
    p[(1,) * k] = 0.5
    return p


def ferro_mix(rho, k=3):
    """rho * repetition + (1-rho) * uniform.  Sign-symmetric at every rho, so
    share exactly zero; pair correlation <z_i z_j> = rho exactly."""
    return rho * repetition(k) + (1.0 - rho) * np.full((2,) * k, 2.0 ** (-k))


def parity_state():
    p = np.zeros((2, 2, 2))
    for x in itertools.product((0, 1), repeat=3):
        if sum(x) % 2 == 0:
            p[x] = 0.25
    return p


# ---------------------------------------------------------------------------
# k = 3: two independent exact solvers (prereg 5.2)
# ---------------------------------------------------------------------------

_BITS3 = np.array([[(i >> b) & 1 for b in (2, 1, 0)] for i in range(8)])
_CHI3 = np.array([1.0 if _BITS3[i].sum() % 2 == 0 else -1.0 for i in range(8)])


def _line(p8, c):
    """p + (c - c0) * chi / 8 -- the competitor line carrying p's pair data."""
    c0 = float(p8 @ _CHI3)
    return p8 + (c - c0) * _CHI3 / 8.0


def _feasible_c(p8):
    c0 = float(p8 @ _CHI3)
    A = 8.0 * p8 - c0 * _CHI3
    pos = _CHI3 > 0
    neg = _CHI3 < 0
    return float(np.max(-A[pos])), float(np.min(A[neg]))


def share3_golden(p, iters=200):
    """Golden section on H along the parity-character line (SHEARER_NUMERIC)."""
    p8 = np.asarray(p, dtype=float).ravel()
    lo, hi = _feasible_c(p8)
    gr = (math.sqrt(5.0) - 1.0) / 2.0
    a, b = lo, hi
    x1, x2 = b - gr * (b - a), a + gr * (b - a)
    f1, f2 = entropy(_line(p8, x1)), entropy(_line(p8, x2))
    for _ in range(iters):
        if f1 < f2:
            a, x1, f1 = x1, x2, f2
            x2 = a + gr * (b - a)
            f2 = entropy(_line(p8, x2))
        else:
            b, x2, f2 = x2, x1, f1
            x1 = b - gr * (b - a)
            f1 = entropy(_line(p8, x1))
        if b - a < 1e-15:
            break
    best = max(f1, f2, entropy(_line(p8, 0.5 * (a + b))))
    return best - entropy(p8)


def share3_root(p):
    """The repository's own bisection solver, imported not reimplemented."""
    return float(QP.share(np.asarray(p, dtype=float).reshape(2, 2, 2)))


def share3(p, gate=True):
    """Both solvers; they must agree to the pre-registered bracket."""
    g = share3_golden(p)
    r = share3_root(p)
    gap = abs(g - r)
    if gate and gap > SOLVER_BRACKET_K3:
        return float("nan"), gap
    return 0.5 * (g + r), gap


# ---------------------------------------------------------------------------
# k >= 3 general: pair-maxent by convex duality, with a two-sided certificate
# ---------------------------------------------------------------------------

def _features(k):
    """z_i for each slot and z_i z_j for each pair, as +-1 columns over 2^k cells."""
    cells = np.array(list(itertools.product((0, 1), repeat=k)))
    z = 1.0 - 2.0 * cells                              # (2^k, k)
    cols = [z[:, i] for i in range(k)]
    pairs = [(i, j) for i in range(k) for j in range(i + 1, k)]
    cols += [z[:, i] * z[:, j] for i, j in pairs]
    return np.array(cols).T                            # (2^k, k + C(k,2))


def _features_general(shape):
    """One-hot pair-marginal features for a general-alphabet product space:
    indicator(x_i = v) for v > 0, and indicator(x_i = v, x_j = w) for v, w > 0.
    Reduces to the +-1 construction on binary cells, and is what arm F needs."""
    k = len(shape)
    cells = np.array(list(itertools.product(*[range(L) for L in shape])))
    cols = []
    for i in range(k):
        for v in range(1, shape[i]):
            cols.append((cells[:, i] == v).astype(float))
    for i in range(k):
        for j in range(i + 1, k):
            for v in range(1, shape[i]):
                for w in range(1, shape[j]):
                    cols.append(((cells[:, i] == v) &
                                 (cells[:, j] == w)).astype(float))
    return np.array(cols).T


def share_dual_general(p, iters=4000):
    """Pair-maxent share on a general-alphabet product space, same two-sided
    certificate as `share_dual`.  Used only by arm F."""
    p = np.asarray(p, dtype=float)
    v = p.ravel()
    F = _features_general(p.shape)
    mu = F.T @ v

    def obj(th):
        e = F @ th
        m = e.max()
        w = np.exp(e - m)
        Z = w.sum()
        return m + math.log(Z) - th @ mu, F.T @ (w / Z) - mu

    res = minimize(obj, np.zeros(F.shape[1]), jac=True, method="L-BFGS-B",
                   options={"maxiter": iters, "ftol": 1e-18, "gtol": 1e-14})
    th = res.x
    for _ in range(80):
        e = F @ th
        m = e.max()
        w = np.exp(e - m)
        q = w / w.sum()
        g = F.T @ q - mu
        if np.abs(g).max() < 1e-14:
            break
        H = (F * q[:, None]).T @ F - np.outer(F.T @ q, F.T @ q)
        try:
            th = th - np.linalg.solve(H + 1e-12 * np.eye(H.shape[0]), g)
        except np.linalg.LinAlgError:
            break
    e = F @ th
    m = e.max()
    w = np.exp(e - m)
    Z = w.sum()
    q = w / Z
    Hp = entropy(v)
    upper = m + math.log(Z) - th @ mu - Hp
    lower = entropy(q) - Hp
    return {"share": float(0.5 * (upper + lower)),
            "share_upper": float(upper), "share_lower": float(lower),
            "bracket": float(abs(upper - lower)),
            "moment_resid": float(np.abs(F.T @ q - mu).max())}


def share_dual(p, iters=2000):
    """Pair-maxent share at general k, with a rigorous two-sided bracket.

    UPPER: for ANY theta, Gibbs gives H(q) <= log Z(theta) - theta.mu for every q
    carrying the observed pair moments mu.  The returned theta* therefore
    certifies an upper bound with no appeal to convergence.
    LOWER: the fitted state's own entropy, valid once its moment residual is
    discharged; the residual is reported, never assumed."""
    p = np.asarray(p, dtype=float)
    k = p.ndim
    v = p.ravel()
    F = _features(k)
    mu = F.T @ v

    def obj(th):
        e = F @ th
        m = e.max()
        Z = np.exp(e - m).sum()
        logZ = m + math.log(Z)
        q = np.exp(e - m) / Z
        return logZ - th @ mu, F.T @ q - mu

    res = minimize(obj, np.zeros(F.shape[1]), jac=True, method="L-BFGS-B",
                   options={"maxiter": iters, "ftol": 1e-18, "gtol": 1e-14})
    th = res.x
    # Newton polish.  The dual's Hessian is the feature covariance under q, which
    # is available in closed form, so the quasi-Newton stopping tolerance is not
    # the accuracy floor.  This was added after the k = 3 plumb line FIRED at
    # 7.1e-9 against a staked 1e-9 (pump_dye.json, first run) -- an instrument
    # failure, fixed and re-gated, with the firing kept in the record.
    for _ in range(60):
        e = F @ th
        m = e.max()
        w = np.exp(e - m)
        q = w / w.sum()
        g = F.T @ q - mu
        if np.abs(g).max() < 1e-15:
            break
        H = (F * q[:, None]).T @ F - np.outer(F.T @ q, F.T @ q)
        try:
            step = np.linalg.solve(H + 1e-14 * np.eye(H.shape[0]), g)
        except np.linalg.LinAlgError:
            break
        th = th - step
    e = F @ th
    m = e.max()
    Z = np.exp(e - m).sum()
    logZ = m + math.log(Z)
    q = np.exp(e - m) / Z
    resid = float(np.abs(F.T @ q - mu).max())
    Hp = entropy(v)
    upper = logZ - th @ mu - Hp
    lower = entropy(q) - Hp
    return {"share_upper": float(upper), "share_lower": float(lower),
            "bracket": float(abs(upper - lower)), "moment_resid": resid,
            "share": float(0.5 * (upper + lower))}


def share_ipf(p, sweeps=5000, tol=1e-14):
    """IPF on all pair marginals -- reported as a third number, never the answer
    (memory: ipf-sharek-boundary-drift; IPF one-sidedly OVERSTATES near
    determinism, by five orders of magnitude in the stored case)."""
    p = np.asarray(p, dtype=float)
    k = p.ndim
    pairs = [(i, j) for i in range(k) for j in range(i + 1, k)]
    targets = [p.sum(axis=tuple(x for x in range(k) if x not in (i, j)))
               for i, j in pairs]
    q = np.full_like(p, 2.0 ** (-k))
    for sweep in range(sweeps):
        delta = 0.0
        for (i, j), t in zip(pairs, targets):
            cur = q.sum(axis=tuple(x for x in range(k) if x not in (i, j)))
            with np.errstate(divide="ignore", invalid="ignore"):
                ratio = np.where(cur > 0, t / np.where(cur > 0, cur, 1.0), 0.0)
            shape = [1] * k
            shape[i], shape[j] = 2, 2
            q = q * ratio.reshape(shape)
            delta = max(delta, float(np.abs(cur - t).max()))
        if delta < tol:
            break
    return float(entropy(q) - entropy(p)), sweep + 1


# ---------------------------------------------------------------------------
# the pre-registered closed form (prereg 4.3)
# ---------------------------------------------------------------------------

def closed_form_C(r0):
    """C(r0) = 18 r0^4 / [(1+2r0)(1+3r0)(1-r0)], the staked coefficient."""
    return 18.0 * r0 ** 4 / ((1 + 2 * r0) * (1 + 3 * r0) * (1 - r0))


def closed_form(a, s, rho=1.0):
    r0 = (1.0 - 2.0 * s) ** 2 * rho
    return closed_form_C(r0) * a * a


def min_cell(p):
    return float(np.asarray(p).min())


# ---------------------------------------------------------------------------
# stages
# ---------------------------------------------------------------------------

def stage_dye():
    """P-EVEN and the seven machine-checked plumb lines.  Run first; nothing
    downstream is reported if this fouls."""
    out = {"stage": "dye"}
    rng = np.random.default_rng(SEED)

    # --- plumb lines with exactly known answers -----------------------------
    plumb = []
    par = parity_state()
    plumb.append(("parity = ln2 (share_parity)", share3(par)[0], LN2))
    fer = repetition(3)
    plumb.append(("ferro = 0 (share_ferro)", share3(fer)[0], 0.0))
    plumb.append(("uniform = 0 (share_indep)", share3(np.full((2, 2, 2), .125))[0], 0.0))
    prod = np.einsum("i,j,k->ijk", [.3, .7], [.6, .4], [.15, .85])
    plumb.append(("product = 0 (share_prod3)", share3(prod)[0], 0.0))
    ss = rng.random(4)
    p_ss = np.zeros((2, 2, 2))
    for idx, cell in enumerate(itertools.product((0, 1), repeat=3)):
        anti = tuple(1 - c for c in cell)
        p_ss[cell] = ss[min(idx, 7 - idx)]
    p_ss /= p_ss.sum()
    plumb.append(("random sign-symmetric = 0", share3(p_ss)[0], 0.0))
    # damp^3 . ferro : machine-checked LOWER bound valve_upward_bound
    K = kernel(a=0.5, s=0.25)          # damp at gamma = 1/2 : p01=1/2, p10=0
    bulge = apply_percell(fer, [K] * 3)
    bulge_share, _ = share3(bulge)
    bound = LN2 + 0.75 * math.log(3) - (17 / 32) * math.log(17)
    out["plumb"] = [{"case": c, "measured": float(m), "expected": float(e),
                     "abs_err": float(abs(m - e))} for c, m, e in plumb]
    out["bulge"] = {"measured": float(bulge_share),
                    "valve_upward_bound": float(bound),
                    "obeys_bound": bool(bulge_share >= bound - 1e-12),
                    "cells": bulge.ravel().tolist()}
    out["plumb_worst"] = max(x["abs_err"] for x in out["plumb"])
    out["plumb_pass"] = bool(out["plumb_worst"] < 1e-12 and out["bulge"]["obeys_bound"])

    # --- P-EVEN : share(-a) == share(+a) exactly ----------------------------
    even = []
    for s in (0.02, 0.05, 0.1, 0.2, 0.3, 0.45):
        amax = 2 * min(s, 1 - s)
        for frac in (0.01, 0.1, 0.5, 0.9, 1.0):
            a = frac * amax
            pp = apply_percell(fer, [kernel(a, s)] * 3)
            pm = apply_percell(fer, [kernel(-a, s)] * 3)
            sp, gp = share3(pp)
            sm, gm = share3(pm)
            even.append({"s": s, "a": a, "share_plus": sp, "share_minus": sm,
                         "abs_diff": abs(sp - sm), "solver_gap": max(gp, gm)})
    out["p_even"] = even
    out["p_even_worst"] = max(e["abs_diff"] for e in even)
    out["p_even_pass"] = bool(out["p_even_worst"] < 1e-12)

    # --- solver agreement over random states (the bracket gate) -------------
    gaps = []
    for _ in range(20000):
        v = rng.dirichlet(np.full(8, rng.choice([0.05, 0.5, 3.0])))
        gaps.append(share3(v.reshape(2, 2, 2), gate=False)[1])
    out["solver_gap_max"] = float(np.max(gaps))
    out["solver_gap_p999"] = float(np.quantile(gaps, 0.999))
    out["solver_gate_pass"] = bool(out["solver_gap_max"] <= SOLVER_BRACKET_K3)

    # --- cap compliance -----------------------------------------------------
    caps = []
    for _ in range(20000):
        v = rng.dirichlet(np.full(8, rng.choice([0.05, 0.5, 3.0])))
        caps.append(share3(v.reshape(2, 2, 2), gate=False)[0])
    out["cap_max_share"] = float(np.max(caps))
    out["cap_pass"] = bool(out["cap_max_share"] <= LN2 + 1e-12)

    # --- the theorem-pinned mixture null: a = 0 at every strength -----------
    nul = []
    for s in np.linspace(0.001, 0.499, 60):
        for rho in (1.0, 0.6, 0.25):
            p = apply_percell(ferro_mix(rho), [kernel(0.0, s)] * 3)
            nul.append(abs(share3(p)[0]))
    out["mixture_null_max"] = float(np.max(nul))
    out["mixture_null_pass"] = bool(out["mixture_null_max"] < 1e-12)

    # --- dual solver vs the exact k=3 solver (plumb line for k>=4 machinery) -
    dual_err = []
    for _ in range(300):
        v = rng.dirichlet(np.full(8, rng.choice([0.5, 3.0])))
        p = v.reshape(2, 2, 2)
        d = share_dual(p)
        dual_err.append(abs(d["share"] - share3(p, gate=False)[0]))
    out["dual_vs_exact_max"] = float(np.max(dual_err))
    out["dual_pass"] = bool(out["dual_vs_exact_max"] < 1e-9)

    return out


def _fit_exponent(a_vals, d_vals):
    la, ld = np.log(np.asarray(a_vals)), np.log(np.asarray(d_vals))
    A = np.vstack([la, np.ones_like(la)]).T
    coef, res, *_ = np.linalg.lstsq(A, ld, rcond=None)
    pred = A @ coef
    dof = max(len(la) - 2, 1)
    sig = math.sqrt(float(((ld - pred) ** 2).sum()) / dof)
    cov = sig ** 2 * np.linalg.inv(A.T @ A)
    return float(coef[0]), float(math.sqrt(cov[0, 0])), float(np.abs(ld - pred).max())


def stage_curveA():
    """Arm A: ferro, the exponent and the coefficient against the closed form."""
    out = {"stage": "curveA", "rows": []}
    fer = repetition(3)
    s_grid = [0.005, 0.01, 0.02, 0.05, 0.075, 0.1, 0.15, 0.2, 0.25,
              0.3, 0.35, 0.4, 0.45, 0.475, 0.49]
    excluded = 0
    ungauged = []
    for s in s_grid:
        amax = 2 * min(s, 1 - s)
        # AMENDMENT 1 (see PUMP_AMENDMENT_1.md): the a-window is chosen per row,
        # PURELY FROM MEASURED VALUES and with no appeal to the prediction, so
        # that every point sits above the instrument's measured depth.  Start at
        # the top of the declared expansion band and walk down geometrically,
        # dropping points once the MEASURED share falls below SHARE_DEPTH.
        a_hi = min(EXPANSION_VALID_A, 0.5 * amax)
        av_all = np.geomspace(a_hi / 100.0, a_hi, 9)
        av, dv, gaps, occ = [], [], [], []
        for a in av_all:
            p = apply_percell(fer, [kernel(a, s)] * 3)
            mc = min_cell(p)
            if mc < OCCUPANCY_FLOOR:
                excluded += 1
                continue
            d, g = share3(p)
            if not (d > SHARE_DEPTH):
                continue                      # below the instrument's depth
            av.append(a); dv.append(d); gaps.append(g); occ.append(mc)
        av, dv = np.asarray(av), np.asarray(dv)
        ok = np.ones(len(av), dtype=bool)
        if len(av) < 4:
            ungauged.append({"s": s, "kappa": 1 - 2 * s,
                             "n_points_above_depth": int(len(av)),
                             "reason": "pump below the instrument's depth "
                                       f"({SHARE_DEPTH:.0e} nat) across the "
                                       "whole declared expansion band"})
            continue
        n, sn, maxres = _fit_exponent(av[ok], dv[ok])
        C_meas = float(dv[ok][0] / av[ok][0] ** 2)
        r0 = (1 - 2 * s) ** 2
        C_pred = closed_form_C(r0)
        out["rows"].append({
            "s": s, "kappa": 1 - 2 * s, "r0": r0, "a_max": amax,
            "n_points": int(ok.sum()),
            "a_vals": av[ok].tolist(),
            "share": dv[ok].tolist(),
            "exponent": n, "exponent_sd": sn, "loglog_max_resid": maxres,
            "C_measured": C_meas, "C_closed_form": C_pred,
            "C_ratio": C_meas / C_pred if C_pred > 0 else float("nan"),
            "solver_gap_max": float(np.nanmax(gaps)),
            "min_cell": float(np.min(occ))})
    out["excluded_by_occupancy"] = excluded
    out["ungauged_rows"] = ungauged

    # the full curve out to the feasibility boundary, exact solver only
    full = []
    for s in (0.05, 0.1, 0.2, 0.3, 0.4):
        amax = 2 * min(s, 1 - s)
        for frac in np.linspace(0.02, 1.0, 50):
            a = frac * amax
            p = apply_percell(fer, [kernel(a, s)] * 3)
            if min_cell(p) < OCCUPANCY_FLOOR:
                continue
            d, g = share3(p)
            full.append({"s": s, "a": float(a), "share": d,
                         "closed_form": closed_form(a, s),
                         "in_expansion_band": bool(a <= EXPANSION_VALID_A)})
    out["full_curve"] = full

    band = [r for r in out["rows"] if 0.1 <= (1 - 2 * r["s"]) <= 0.95]
    out["summary"] = {
        "exponent_min": min(r["exponent"] for r in out["rows"]),
        "exponent_max": max(r["exponent"] for r in out["rows"]),
        "C_ratio_min": min(r["C_ratio"] for r in band),
        "C_ratio_max": max(r["C_ratio"] for r in band),
        "P_EXP_pass": bool(all(1.90 <= r["exponent"] <= 2.10 for r in out["rows"])),
        "P_FORM_pass": bool(all(abs(r["C_ratio"] - 1) <= 0.02 for r in band)),
    }
    return out


def stage_curveB():
    """Arm B: the input pair-strength law.  Staked: C ∝ r0^4 at small r0."""
    out = {"stage": "curveB", "rows": []}
    for rho in [1.0, 0.9, 0.75, 0.6, 0.5, 0.4, 0.3, 0.25, 0.2, 0.15, 0.1, 0.05]:
        for s in (0.05, 0.1, 0.2, 0.3):
            base = ferro_mix(rho)
            pre = share3(base)[0]
            # AMENDMENT 1: measured-depth window, as in arm A
            a_hi = min(EXPANSION_VALID_A, min(s, 1 - s))
            av_all = np.geomspace(a_hi / 100.0, a_hi, 9)
            av, dv = [], []
            for a in av_all:
                p = apply_percell(base, [kernel(a, s)] * 3)
                if min_cell(p) < OCCUPANCY_FLOOR:
                    continue
                d = share3(p)[0]
                if not (d > SHARE_DEPTH):
                    continue
                av.append(a); dv.append(d)
            av, dv = np.asarray(av), np.asarray(dv)
            ok = np.ones(len(av), dtype=bool)
            if len(av) < 4:
                out.setdefault("ungauged_rows", []).append(
                    {"rho": rho, "s": s, "r0": (1 - 2 * s) ** 2 * rho,
                     "n_points_above_depth": int(len(av)),
                     "reason": "below the instrument's depth"})
                continue
            n, sn, _ = _fit_exponent(av[ok], dv[ok])
            C_meas = float(dv[ok][0] / av[ok][0] ** 2)
            r0 = (1 - 2 * s) ** 2 * rho
            out["rows"].append({
                "rho": rho, "s": s, "r0": r0, "share_input": pre,
                "exponent": n, "exponent_sd": sn,
                "C_measured": C_meas, "C_closed_form": closed_form_C(r0),
                "C_ratio": C_meas / closed_form_C(r0)})
    small = [r for r in out["rows"] if r["r0"] <= 0.2]
    if small:
        lr = np.log([r["r0"] for r in small])
        lc = np.log([r["C_measured"] for r in small])
        A = np.vstack([lr, np.ones_like(lr)]).T
        coef, *_ = np.linalg.lstsq(A, lc, rcond=None)
        out["r0_power_at_small_r0"] = float(coef[0])
    out["C_ratio_min"] = min(r["C_ratio"] for r in out["rows"])
    out["C_ratio_max"] = max(r["C_ratio"] for r in out["rows"])
    return out


def stage_curveC():
    """Arm C: k-scaling on the repetition code, k = 3..7, dual certificate.

    AMENDMENT 2 (see PUMP_AMENDMENT_1.md section 2).  The first run of this arm
    returned exponent ~0.005 at k >= 4, which is not a pump measurement: it is a
    CONSTANT baseline swamping the a-dependence.  Diagnosed, and it is a real
    property of the model rather than an instrument fault:

      share(repetition(k)) = 0 exactly at every k (checked, <= 5e-14), but the
      UNITAL (a = 0, flip-covariant) channel mints STRICTLY POSITIVE share from
      it at k >= 4 -- 0.0132 nat at k=4, s=0.1, on an output verified
      sign-symmetric to 7e-18.

    `Core/SignSymmetry.share_eq_zero_of_signSymmetric` is a THREE-SLOT theorem,
    and `valve_needs_asymmetry` inherits that restriction.  Sign symmetry kills
    ODD-order structure; at four slots and up the EVEN orders survive it, exactly
    as this programme's own SPIKE_SURVEY recorded numerically (order 4 at 0.169
    nats while the odd orders sat at 1.7e-13).  So at k >= 4 there are two
    separate things to measure and the first run conflated them:

      B_k(s)        the SYMMETRIC BASELINE: what unital noise alone mints
      D_k(a,s)      the ASYMMETRY-DRIVEN EXCESS, share(a,s) - B_k(s)

    D is the pump.  B is a new object this campaign did not expect to exist."""
    out = {"stage": "curveC", "rows": [], "baseline": []}

    # --- B_k(s): the symmetric baseline, measured on its own ----------------
    for k in (3, 4, 5, 6, 7):
        base = repetition(k)
        d_in = share_dual(base)
        for s in (0.02, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4):
            p = apply_percell(base, [kernel(0.0, s)] * k)
            d = share_dual(p)
            flip = p[tuple(slice(None, None, -1) for _ in range(k))]
            out["baseline"].append({
                "k": k, "s": s, "kappa": 1 - 2 * s,
                "share_input": d_in["share"],
                "B": d["share"], "bracket": d["bracket"],
                "signsym_err": float(np.abs(p - flip).max()),
                "cap_k_minus_2_ln2": (k - 2) * LN2,
                "ceiling_fraction": d["share"] / ((k - 2) * LN2)})

    # --- D_k(a,s): the excess above the symmetric baseline -------------------
    for k in (3, 4, 5, 6, 7):
        base = repetition(k)
        for s in (0.05, 0.1, 0.2, 0.3):
            B = share_dual(apply_percell(base, [kernel(0.0, s)] * k))["share"]
            a_hi = min(EXPANSION_VALID_A, min(s, 1 - s))
            av_all = np.geomspace(a_hi / 50.0, a_hi, 9)
            av, dv, brackets, resids = [], [], [], []
            for a in av_all:
                p = apply_percell(base, [kernel(a, s)] * k)
                if min_cell(p) < OCCUPANCY_FLOOR:
                    continue
                d = share_dual(p)
                excess = d["share"] - B
                if not (excess > SHARE_DEPTH):
                    continue
                av.append(a); dv.append(excess)
                brackets.append(d["bracket"]); resids.append(d["moment_resid"])
            if len(av) < 4:
                continue
            av, dv = np.asarray(av), np.asarray(dv)
            n, sn, _ = _fit_exponent(av, dv)
            C_meas = float(dv[0] / av[0] ** 2)
            row = {"k": k, "s": s, "B_symmetric_baseline": B,
                   "exponent": n, "exponent_sd": sn, "n_points": len(av),
                   "C_measured": C_meas,
                   "a_vals": av.tolist(), "excess": dv.tolist(),
                   "bracket_max": float(np.max(brackets)),
                   "moment_resid_max": float(np.max(resids)),
                   "bracket_pass": bool(np.max(brackets) <= SOLVER_BRACKET_KGE4)}
            if k == 3:
                p = apply_percell(base, [kernel(av[0], s)] * 3)
                row["C_exact_k3"] = float(share3(p)[0] / av[0] ** 2)
                row["C_closed_form"] = closed_form_C((1 - 2 * s) ** 2)
                row["C_ratio_vs_closed_form"] = (row["C_exact_k3"]
                                                 / row["C_closed_form"])
                ipf, sweeps = share_ipf(p)
                row["ipf_share"] = ipf
                row["exact_share"] = float(share3(p)[0])
                row["ipf_minus_exact"] = ipf - float(share3(p)[0])
                row["ipf_sweeps"] = sweeps
            out["rows"].append(row)

    growth = {}
    for s in (0.05, 0.1, 0.2, 0.3):
        rows = sorted([r for r in out["rows"] if r["s"] == s], key=lambda r: r["k"])
        if len(rows) >= 3:
            lk = np.log([r["k"] for r in rows])
            lc = np.log([r["C_measured"] for r in rows])
            A = np.vstack([lk, np.ones_like(lk)]).T
            coef, *_ = np.linalg.lstsq(A, lc, rcond=None)
            growth[str(s)] = {"power_in_k": float(coef[0]),
                              "C_by_k": {str(r["k"]): r["C_measured"] for r in rows}}
        brows = sorted([r for r in out["baseline"] if r["s"] == s],
                       key=lambda r: r["k"])
        brows = [r for r in brows if r["B"] > SHARE_DEPTH]
        if len(brows) >= 3:
            lk = np.log([r["k"] for r in brows])
            lb = np.log([r["B"] for r in brows])
            A = np.vstack([lk, np.ones_like(lk)]).T
            coef, *_ = np.linalg.lstsq(A, lb, rcond=None)
            growth.setdefault(str(s), {})["baseline_power_in_k"] = float(coef[0])
            growth[str(s)]["B_by_k"] = {str(r["k"]): r["B"] for r in brows}
            growth[str(s)]["ceilfrac_by_k"] = {
                str(r["k"]): r["ceiling_fraction"] for r in brows}
    out["k_growth"] = growth
    out["exponent_range"] = [min(r["exponent"] for r in out["rows"]),
                             max(r["exponent"] for r in out["rows"])]
    out["P_EXP_pass_all_k"] = bool(all(1.90 <= r["exponent"] <= 2.10
                                       for r in out["rows"]))
    return out


def stage_dose():
    """Dose-vs-rate (GATES.md reach 7): is the per-step minted share step-count
    invariant, or is it a transient?  The fixed point of any per-cell channel is
    a product state (share exactly zero), so a bulge is REQUIRED by the existing
    theorems.  Characterise it."""
    out = {"stage": "dose", "traj": []}
    fer = repetition(3)
    for s_step, a_frac in [(0.02, 1.0), (0.02, 0.5), (0.05, 1.0), (0.05, 0.5),
                           (0.01, 1.0), (0.1, 1.0)]:
        a = a_frac * 2 * min(s_step, 1 - s_step)
        K = kernel(a, s_step)
        p = fer.copy()
        row = {"s_step": s_step, "a_frac": a_frac, "a_step": a, "steps": []}
        for n in range(1, 121):
            p = apply_percell(p, [K] * 3)
            d, _ = share3(p)
            # the effective single-shot channel after n steps
            Kn = np.linalg.matrix_power(K, n)
            a_eff = Kn[0, 1] - Kn[1, 0]
            s_eff = 0.5 * (Kn[0, 1] + Kn[1, 0])
            row["steps"].append({"n": n, "share": d, "a_eff": float(a_eff),
                                 "s_eff": float(s_eff),
                                 "per_step": d / n,
                                 "closed_form_at_eff": closed_form(a_eff, s_eff)})
        sh = [x["share"] for x in row["steps"]]
        row["peak_share"] = float(max(sh))
        row["peak_step"] = int(np.argmax(sh) + 1)
        row["final_share"] = float(sh[-1])
        pk = row["steps"][row["peak_step"] - 1]
        row["peak_a_eff"] = pk["a_eff"]
        row["peak_kappa_eff"] = float(1 - 2 * pk["s_eff"])
        out["traj"].append(row)

    # the composition check: n steps of K is one step of K^n, so the whole
    # trajectory must be ONE curve in the effective coordinates
    dev = []
    for row in out["traj"]:
        for st in row["steps"]:
            if st["a_eff"] <= EXPANSION_VALID_A and st["share"] > 1e-13:
                p = apply_percell(fer, [kernel(st["a_eff"], st["s_eff"])] * 3)
                one, _ = share3(p)
                dev.append(abs(one - st["share"]))
    out["composition_max_dev"] = float(max(dev)) if dev else None
    out["composition_pass"] = bool(dev and max(dev) < 1e-12)
    return out


def stage_qpu():
    """P-QPU: the hardware cross-check.  Blinding declared ABSENT in the prereg
    -- run 3's bulge is already published."""
    ts = os.path.join(HERE, "temporal-share")
    verdict = json.load(open(os.path.join(ts, "qpu_sector_verdict_C_"
                                          "d9in8jrjf64c739fprqg.json")))
    raw = json.load(open(os.path.join(ts, "qpu_habit_C_"
                                      "d9in8jrjf64c739fprqg.json")))
    fz = raw["freeze"]
    recs = {r["tag"]: r for r in raw["records"]}
    sets = []
    for pre in ("C9", "C0"):
        sets.append(QP.assignment_matrices(
            QP.counts_to_p(recs[f"{pre}|cal|000|0"]["counts"]).ravel(),
            QP.counts_to_p(recs[f"{pre}|cal|111|0"]["counts"]).ravel()))
    amats = [(sets[0][q] + sets[1][q]) / 2 for q in range(3)]

    def corr(tag):
        pc = QP.correct_readout(QP.counts_to_p(recs[tag]["counts"]), amats)
        pc = np.clip(pc, 0, None)
        return pc / pc.sum()

    # p_exc exactly as the published analysis derived it
    sat = fz["delays_sat_us"]
    p1_sat = []
    for t in sat:
        pc = corr(f"C2|exc|ZZZ|{t}")
        p1_sat.append([float(pc.sum(axis=tuple(x for x in range(3) if x != q))[1])
                       for q in range(3)])
    pexc = [min(p1_sat[-1][q], 0.2) for q in range(3)]

    kap = np.array(verdict["kappa"])
    meas = verdict["ferro_share"]
    published_pred = verdict["ferro_pred"]
    delays = fz["delays_ferro_us"]

    rows = []
    for i, t in enumerate(delays):
        k_q = kap[i]
        b_q = [(1 - k_q[q]) * (1 - 2 * pexc[q]) for q in range(3)]
        # our own exact reconstruction, same measured inputs as the published run
        M = QP.moments(repetition(3))
        M2 = QP.apply_product_channel(M, k_q, np.array(b_q))
        p = QP.dist_from_moments(M2)
        ours = float(QP.share(p)) if p.min() >= 0 else float("nan")
        ours_gold = share3_golden(np.clip(p, 0, None) / np.clip(p, 0, None).sum())
        a_q = b_q
        s_q = [(1 - k_q[q]) / 2 for q in range(3)]
        a_bar = float(np.mean(a_q))
        s_bar = float(np.mean(s_q))
        rows.append({
            "t_us": t, "kappa": k_q.tolist(), "p_exc": pexc,
            "a_per_qubit": [float(x) for x in a_q],
            "s_per_qubit": [float(x) for x in s_q],
            "a_mean": a_bar, "s_mean": s_bar,
            "kappa_mean": float(np.mean(k_q)),
            "alpha_ratio": [float(1 - 2 * pq) for pq in pexc],
            "share_measured": meas[i],
            "share_published_pred": published_pred[i],
            "share_ours_exact": ours,
            "share_ours_golden": float(ours_gold),
            "share_closed_form": closed_form(a_bar, s_bar),
            "in_expansion_band": bool(a_bar <= EXPANSION_VALID_A)})

    rel = [abs(r["share_ours_exact"] - r["share_published_pred"]) /
           max(r["share_published_pred"], 1e-12) for r in rows[1:]]
    out = {"stage": "qpu", "rows": rows,
           "p_exc": pexc,
           "alpha_ratio": [float(1 - 2 * pq) for pq in pexc],
           "QPU1_max_rel_dev_vs_published": float(max(rel)),
           "QPU1_pass": bool(max(rel) <= 0.01)}
    band = [r for r in rows if r["in_expansion_band"] and r["share_measured"] > 1e-4]
    if band:
        ratios = [r["share_measured"] / r["share_closed_form"] for r in band]
        out["QPU2_ratios"] = ratios
        out["QPU2_min"] = float(min(ratios))
        out["QPU2_max"] = float(max(ratios))
        out["QPU2_pass"] = bool(0.5 <= min(ratios) and max(ratios) <= 2.0)
        out["QPU2_n_points"] = len(band)
    return out


def stage_sampled():
    """Arm G: the sampled arm, so GATES reaches 1 and 9 are not simply skipped.
    Separates the VALVE (moves the true share of an exact distribution) from
    FINITE-N MINTING (leaves the true share at zero and moves the estimator)."""
    rng = np.random.default_rng(SEED + 1)
    out = {"stage": "sampled", "rows": []}
    fer = repetition(3)
    for s in (0.1, 0.25):
        for a_frac, label in ((0.0, "a=0 TRUE ZERO (estimator bias only)"),
                              (0.5, "a=half-max (valve + bias)"),
                              (1.0, "a=max (valve + bias)")):
            a = a_frac * 2 * min(s, 1 - s)
            p = apply_percell(fer, [kernel(a, s)] * 3)
            truth, _ = share3(p)
            for N in (100, 1000, 10000, 100000, 1000000):
                est = []
                for _ in range(200):
                    c = rng.multinomial(N, p.ravel()) / N
                    est.append(share3_root(c.reshape(2, 2, 2)))
                est = np.asarray(est)
                out["rows"].append({
                    "s": s, "a": float(a), "arm": label, "N": N,
                    "true_share": truth,
                    "est_median": float(np.median(est)),
                    "est_mean": float(est.mean()),
                    "est_q05": float(np.quantile(est, 0.05)),
                    "est_q95": float(np.quantile(est, 0.95)),
                    "bias": float(np.median(est) - truth),
                    "floor_over_truth": (float(np.median(est) / truth)
                                         if truth > 0 else None),
                    "chi2_prediction_(cells-1)/2N": 7.0 / (2 * N)})
    return out


def stage_coarse():
    """Arm F, EXPLORATORY and separable: a four-letter per-cell channel followed
    by binarization.  This CROSSES the alphabet boundary Core/Valve.lean does not
    cover.  It cannot feed the primary law whatever it finds (prereg section 2)."""
    rng = np.random.default_rng(SEED + 2)
    out = {"stage": "coarse", "note": "EXPLORATORY: alphabet-reducing, outside "
           "Core/Valve.lean's proved scope. Separable verdict.", "rows": []}
    # a 4-letter repetition-style input: all three cells carry the same letter
    for L in (4,):
        base = np.zeros((L,) * 3)
        for v in range(L):
            base[v, v, v] = 1.0 / L
        for s in (0.05, 0.1, 0.2, 0.3):
            for a_frac in (0.0, 0.25, 0.5, 0.75, 1.0):
                # asymmetric L-letter channel: drift toward letter 0 with
                # asymmetry a, symmetric mixing with strength s
                K = np.full((L, L), 0.0)
                for x in range(L):
                    stay = 1.0 - 2 * s
                    K[:, x] = 2 * s / L
                    K[x, x] += stay
                    # asymmetry: bleed a_frac*s of the weight to letter 0
                    bleed = a_frac * s
                    if x != 0:
                        K[:, x] *= (1 - bleed)
                        K[0, x] += bleed
                K = K / K.sum(axis=0, keepdims=True)
                p = apply_percell(base, [K] * 3)
                # binarize: letters {0,1} -> 0, {2,3} -> 1
                b = np.zeros((2, 2, 2))
                for cell in itertools.product(range(L), repeat=3):
                    b[tuple(0 if c < L // 2 else 1 for c in cell)] += p[cell]
                sh_fine_pairs = share_dual_general(p)
                sh_bin, _ = share3(b)
                out["rows"].append({
                    "L": L, "s": s, "a_frac": a_frac,
                    "share_after_binarize": sh_bin,
                    "share_fine_alphabet": sh_fine_pairs["share"],
                    "fine_bracket": sh_fine_pairs["bracket"],
                    "min_cell_binary": min_cell(b)})
    # ARM F DYE TEST.  The abscissa above parametrizes the FINE channel, and a
    # non-lumpable fine channel induces no well-defined binary per-cell channel,
    # so an exponent read against it is not directly comparable to arm A's.  The
    # dye: a LUMPABLE fine channel -- one that acts identically within each block
    # of the partition -- DOES induce an exact binary per-cell channel with known
    # (a, s).  If the instrument reads exponent 2 there and not-2 on the
    # non-lumpable family, the difference is the coarse-graining, not the probe.
    dye = []
    for s in (0.1, 0.2):
        for a in np.geomspace(2e-3, 0.2, 7):
            Kb = kernel(a, s)                       # the induced binary channel
            L = 4
            K = np.zeros((L, L))
            for x in range(L):
                for y in range(L):
                    # act on the BLOCK label with Kb, spread uniformly inside
                    K[y, x] = Kb[y // 2, x // 2] * 0.5
            base = np.zeros((L,) * 3)
            for v in range(L):
                base[v, v, v] = 1.0 / L
            p = apply_percell(base, [K] * 3)
            b = np.zeros((2, 2, 2))
            for cell in itertools.product(range(L), repeat=3):
                b[tuple(c // 2 for c in cell)] += p[cell]
            sh, _ = share3(b)
            if sh > SHARE_DEPTH:
                dye.append({"s": s, "a_induced": float(a), "share": sh,
                            "closed_form": closed_form(a, s)})
    out["dye_lumpable"] = dye
    for s in (0.1, 0.2):
        rows = [r for r in dye if r["s"] == s]
        if len(rows) >= 4:
            la = np.log([r["a_induced"] for r in rows])
            ld = np.log([r["share"] for r in rows])
            A = np.vstack([la, np.ones_like(la)]).T
            coef, *_ = np.linalg.lstsq(A, ld, rcond=None)
            out.setdefault("dye_lumpable_exponent", {})[str(s)] = float(coef[0])
            out.setdefault("dye_lumpable_C_ratio", {})[str(s)] = float(
                rows[0]["share"] / rows[0]["closed_form"])

    # does the binarized reading still go as a^2?
    for s in (0.1, 0.2):
        rows = [r for r in out["rows"] if r["s"] == s and r["a_frac"] > 0]
        if len(rows) >= 3:
            la = np.log([r["a_frac"] for r in rows])
            ld = np.log([max(r["share_after_binarize"], 1e-300) for r in rows])
            A = np.vstack([la, np.ones_like(la)]).T
            coef, *_ = np.linalg.lstsq(A, ld, rcond=None)
            out.setdefault("binarized_exponent", {})[str(s)] = float(coef[0])
    return out


STAGES = {"dye": stage_dye, "curveA": stage_curveA, "curveB": stage_curveB,
          "curveC": stage_curveC, "dose": stage_dose, "qpu": stage_qpu,
          "sampled": stage_sampled, "coarse": stage_coarse}


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    names = list(STAGES) if which == "all" else [which]
    for nm in names:
        t0 = time.time()
        res = STAGES[nm]()
        res["seed"] = SEED
        res["wall_s"] = round(time.time() - t0, 2)
        path = os.path.join(HERE, f"pump_{nm}.json")
        json.dump(res, open(path, "w"), indent=1)
        print(f"[{nm}] {res['wall_s']}s -> {path}")
        for key in sorted(res):
            v = res[key]
            if isinstance(v, (int, float, bool, str)) or (
                    isinstance(v, dict) and len(json.dumps(v)) < 600):
                print(f"    {key} = {v}")
        sys.stdout.flush()


if __name__ == "__main__":
    main()


# ---------------------------------------------------------------------------
# THE DOWNSTREAM ENTRY POINT — send this, not a number.
#
# Written after three campaigns each received a NUMBER from this campaign that
# was conditioned on a substrate property their own systems set and mine did
# not: which axis governs (is the input sign-symmetric?), the magnetisation m,
# and the estimator floor.  Each time the number was right for my substrate and
# wrong or unusable for theirs.  `water`'s diagnosis, adopted: a floor is a
# property of the RECIPIENT'S sampling geometry, not of the sender's
# derivation, so it cannot be supplied from outside -- send the instrument,
# which carries the substrate parameter by construction, never the number,
# which assumes it.
#
# Usage:
#     from pump_curve import substrate_report
#     substrate_report(m=0.55, r=0.75, s=0.10, N=4_000_000)
# ---------------------------------------------------------------------------

def substrate_report(m, r, s, N=None, verbose=True):
    """Which axis governs YOUR substrate, and what it implies. All exact.

    m : per-slot magnetisation <z> of your binarized table (0 = sign-symmetric)
    r : pair moment <z_i z_j> of your table -- the RAW moment, not a Pearson
        correlation. If your marginals are not 50/50 they differ:
        <z_i z_j> = rho_pearson * (1 - m**2) + m**2
    s : per-cell noise strength (p01 + p10)/2 of your channel; kappa = 1 - 2s
    N : your sample size, if you want the usability threshold. Use your OWN
        MEASURED floor if you have one -- 0.227/N is a BENCHMARK for
        independent tuples and under-reads by 2-42x on real geometries."""
    from scipy.optimize import brentq, minimize_scalar
    out = {"m": m, "r": r, "s": s, "kappa": 1 - 2 * s}

    def _st(mm, rr, cc):
        p = [(1 + 3*mm + 3*rr + cc)/8, (1 + mm - rr - cc)/8,
             (1 - mm - rr + cc)/8, (1 - 3*mm + 3*rr - cc)/8]
        q = np.zeros((2, 2, 2))
        for x in itertools.product((0, 1), repeat=3):
            q[x] = p[sum(x)]
        return q

    def _zero_share(mm, rr):
        f = lambda c: (math.log(max((1+3*mm+3*rr+c)/8, 1e-300))
                       + 3*math.log(max((1-mm-rr+c)/8, 1e-300))
                       - 3*math.log(max((1+mm-rr-c)/8, 1e-300))
                       - math.log(max((1-3*mm+3*rr-c)/8, 1e-300)))
        lo, hi = -0.999, 0.999
        while f(lo) > 0: lo += 0.005
        while f(hi) < 0: hi -= 0.005
        return _st(mm, rr, brentq(f, lo, hi, xtol=1e-16))

    sign_symmetric = abs(m) < 1e-12
    out["axis"] = "CHANNEL" if sign_symmetric else "STATE"
    p0 = _zero_share(m, r)
    out["input_share"] = share3(p0, gate=False)[0]

    if sign_symmetric:
        r0 = (1 - 2*s)**2 * r
        out["r0"] = r0
        out["C_channel_axis"] = closed_form_C(r0)
        out["law"] = "share = C * a^2, C = 18 r0^4/[(1+2r0)(1+3r0)(1-r0)]"
        out["floor_at_a0"] = 0.0
        out["a_null"] = None
        out["note"] = ("a = 0 mints EXACTLY zero (valve_needs_asymmetry, and it "
                       "needs BOTH three slots and this sign-symmetry). The "
                       "closed form is a leading quadratic: coefficient exact "
                       "as a->0, VALUE within 2% only for a <~ 0.07.")
    else:
        out["floor_at_a0"] = share3(apply_percell(p0, [kernel(0.0, s)]*3),
                                    gate=False)[0]
        amax = 2 * min(s, 1 - s) * 0.999
        g = lambda a: share3(apply_percell(p0, [kernel(a, s)]*3), gate=False)[0]
        res = minimize_scalar(g, bounds=(-amax, amax), method="bounded",
                              options={"xatol": 1e-12})
        out["a_null"] = float(res.x)
        out["a_null_approx_2ms"] = 2 * m * s
        out["share_at_null"] = float(res.fun)
        out["note"] = ("A UNITAL channel already mints here -- a = 0 is NOT a "
                       "null. The floor is NON-MONOTONE in a: it falls from "
                       "a = 0 to an exact zero at a_null (the magnetisation-"
                       "preserving channel), then rises. Neither 'our channel "
                       "is symmetric' nor its converse is a bound.")

    if N is not None:
        out["N"] = N
        out["naive_floor_0.227_over_N"] = 0.227 / N
        out["WARNING"] = ("0.227/N holds only for INDEPENDENT tuples. Measured "
                          "overhead on real geometries: 1.0x (iid), 1.9x, "
                          "5.8-7.9x, 45x. USE YOUR OWN MEASURED FLOOR.")
        if not sign_symmetric and out["floor_at_a0"] > 0:
            # K must be the SMALL-m constant, not floor/m^2 at the caller's own
            # m: the floor is quadratic in m only below m ~ 0.05 and saturates
            # above it, so evaluating K at a large m under-reads it and inflates
            # the threshold. Probe at m = 1e-3 with the caller's r and s.
            probe = 1e-3
            K = share3(apply_percell(_zero_share(probe, r), [kernel(0.0, s)]*3),
                       gate=False)[0] / probe**2
            out["K_at_your_r_and_s"] = K
            out["K_local_at_your_m"] = out["floor_at_a0"] / (m*m)
            out["m_threshold_vs_naive"] = math.sqrt((0.227/N) / K)
            out["threshold_note"] = ("below this m the state-axis floor sits "
                                     "beneath the NAIVE estimator floor; "
                                     "recompute against your measured floor, "
                                     "which is 2-42x higher.")
    if verbose:
        for k, v in out.items():
            print(f"  {k} = {v}")
    return out
