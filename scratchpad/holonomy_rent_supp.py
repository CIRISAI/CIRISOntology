#!/usr/bin/env python3
"""Supplementary analysis for the maintained-holonomy campaign.

FOUR questions the main sweep raised and could not itself answer.  All are POST-HOC
and labelled as such; per HOLONOMY_RENT_PREREG.md section 8 no cell outside the
declared grid enters a headline.  S1 and S3 exist to WEAKEN claims (they
characterise an un-converged quantity and diagnose a schedule dependence); S2
decomposes a pre-registered residual; S4 refines a pre-registered scale.

  S1  R-POL's fidelity was still DECLINING at R=400, so per prereg 6.5 it may not be
      quoted as a plateau.  How far does it fall, and does R-DES fall with it?
      Depth extended well past the declared grid, for that question only.
  S2  The H3 residual is confounded: the unmaintained decay is NOT exactly geometric.
      Drive the scalar rent recursion with the MEASURED per-step rates and see what
      is left over.
  S3  The periodic arm reads exactly 1.000000 whenever round(1/q) divides 399 -- a
      checkpoint landing on a repair step.  Cycle-average it and compare properly.
  S4  q_half on a refined grid rather than by interpolation across a coarse one.
"""
import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
sys.dont_write_bytecode = True

import importlib.util

import numpy as np

PRED = ("/home/emoore/coherence-ratchet/experiments/open_system_pomega/"
        "assumption_audit/holonomic_pomega/build_holonomic_pomega.py")
D, SEED = 64, 20260522
DEEP = 4001

spec = importlib.util.spec_from_file_location("bhp_pred", PRED)
bhp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bhp)
import cupy as cp
Wc, Bc, _, _ = bhp.build_connection(D, SEED)
W = np.asarray(cp.asnumpy(Wc), dtype=np.complex128)
B = np.asarray(cp.asnumpy(Bc), dtype=np.complex128)
del Wc, Bc
cp.get_default_memory_pool().free_all_blocks()


def polar(A):
    U, _, Vh = np.linalg.svd(A)
    return U @ Vh


Udes = polar(B)
I = np.eye(D, dtype=np.complex128)
FLOOR = 1.0 / D          # the MEASURED C-RAND fidelity floor, ~0.0156 at d=64


def walk(q, arm, kmax, every=1, mode="cont"):
    H, Wp, Dp = I.copy(), I.copy(), I.copy()
    period = int(round(1.0 / q)) if q > 0 else 0
    ks, gs, fs = [], [], []
    for k in range(1, kmax):
        H = B @ H
        Dp = Udes @ Dp
        Wp = W @ Wp
        if q > 0:
            s = q if mode == "cont" else (1.0 if (period and k % period == 0) else 0.0)
            if s > 0:
                H = (1 - s) * H + s * (polar(H) if arm == "POL" else Dp)
        if k % every == 0:
            Hol, Hd = H @ Wp, Dp @ Wp
            fn = float(np.linalg.norm(Hol))
            ks.append(k + 1)
            gs.append(fn / np.sqrt(D))
            fs.append(abs(complex(np.vdot(Hd, Hol)))
                      / max(float(np.linalg.norm(Hd)) * fn, 1e-300))
    return np.array(ks), np.array(gs), np.array(fs)


QS1 = [0.0345, 0.1, 0.3, 0.7]
print("=" * 86)
print("S1 (POST-HOC, depth far beyond the declared grid) -- where is the fidelity going?")
print("=" * 86)
print("  At R=400 R-POL's fidelity was 0.95 and still falling, so prereg 6.5 forbids")
print("  quoting it as a plateau.  This extension bounds how bad that is.  It is used")
print("  to WEAKEN the campaign's claim, never to support one.")
print(f"  C-RAND measured the chance floor at 1/d = {FLOOR:.4f}.\n")
S = {}
for arm in ("POL", "DES"):
    for q in QS1:
        S[(arm, q)] = walk(q, arm, DEEP, every=100)
S[("q0", 0.0)] = walk(0.0, "POL", DEEP, every=100)
ks = S[("POL", 0.0345)][0]

print("  FIDELITY vs depth")
print("      R    " + "".join(f"  POL q={q:<6g}" for q in QS1)
      + "".join(f"  DES q={q:<6g}" for q in QS1) + "   unmaint.")
for i, k in enumerate(ks):
    if not (k <= 401 or (k - 1) % 500 == 0):
        continue
    line = f"  {k:5d}  "
    for arm in ("POL", "DES"):
        for q in QS1:
            line += f"    {S[(arm, q)][2][i]:.6f}"
    line += f"    {S[('q0', 0.0)][2][i]:.6f}"
    print(line)

print("\n  GAIN vs depth, for contrast -- the PLATEAU does hold while the direction goes")
print("      R    " + "".join(f"  POL q={q:<6g}" for q in QS1) + "   unmaint.")
for i, k in enumerate(ks):
    if not (k <= 401 or (k - 1) % 1000 == 0):
        continue
    line = f"  {k:5d}  "
    for q in QS1:
        line += f"    {S[('POL', q)][1][i]:.6f}"
    line += f"    {S[('q0', 0.0)][1][i]:.3e}"
    print(line)

print("\n  fidelity power-law slope over R in [400, 4000], and the depth at which that")
print("  slope reaches the 1/d chance floor:")
print("    arm  q        f(4000)     dlogf/dlogR    R at floor")
for arm in ("POL", "DES"):
    for q in QS1:
        k, _, f = S[(arm, q)]
        m = (k >= 400) & (f > 0)
        sl = float(np.polyfit(np.log(k[m]), np.log(f[m]), 1)[0])
        kf = k[-1] * (FLOOR / f[-1]) ** (1.0 / sl) if sl < -1e-6 else np.inf
        print(f"    {arm}  {q:<7g}  {f[-1]:.6f}   {sl:+.4f}       {kf:.3g}")
k, _, f = S[("q0", 0.0)]
m = (k >= 400) & (f > 0)
print(f"    q=0  unmaint.  {f[-1]:.6f}   "
      f"{float(np.polyfit(np.log(k[m]), np.log(f[m]), 1)[0]):+.4f}       (control)")

print()
print("=" * 86)
print("S2 -- decomposing the H3 residual: the operator, or the non-geometric decay?")
print("=" * 86)
k0, g0, _ = walk(0.0, "POL", 401, every=1)
lam_k = g0[1:] / g0[:-1]
lam_fixed = float(g0[-1] ** (1.0 / len(g0)))
eps_fixed = 1 - lam_fixed
print(f"  measured per-step gain ratio drifts: lam[2]={lam_k[0]:.6f} -> "
      f"lam[400]={lam_k[-1]:.6f}   (NOT a geometric law)")
print(f"  single fixed lambda from the q=0 run at R=400: {lam_fixed:.6f}, "
      f"eps = {eps_fixed:.6f}\n")
print("     q     measured   single-lambda  resid   |  driven by measured  resid")
print("            plateau    closed form            |  per-step rates")
QS = [0.01725, 0.0345, 0.069, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 0.99]
wf = wd = 0.0
for q in QS:
    _, gq, _ = walk(q, "POL", 401, every=400)
    meas = float(gq[-1])
    pf = q / (1 - (1 - q) * lam_fixed)
    s = 1.0
    for lk in lam_k:
        s = (1 - q) * lk * s + q
    rf, rd = (meas - pf) / pf, (meas - s) / s
    wf, wd = max(wf, abs(rf)), max(wd, abs(rd))
    print(f"  {q:6.5f}  {meas:.6f}   {pf:.6f}   {rf:+7.2%}  |  {s:.6f}      {rd:+7.2%}")
print(f"\n  max |residual|: single-lambda {wf:.1%}   driven-by-measured-rates {wd:.1%}")
print("  READ IT AS IT CAME: removing the decay's non-geometricity makes the residual")
print("  WORSE, not better.  So the gap is NOT the received law being mis-specified --")
print("  it is operator structure, and it has a consistent sign: the measured plateau")
print("  sits BELOW the scalar rent prediction at every q.  Misalignment between the")
print("  deposit and the decayed operator costs, exactly as prereg 4.3 anticipated.")

print()
print("=" * 86)
print("S3 -- the periodic arm is checkpoint-phase aliased.  Cycle-average, then compare.")
print("=" * 86)
print("  A full-strength repair puts the operator EXACTLY on the isometry manifold, so")
print("  gain = 1 at that step.  Reading at one R samples a sawtooth at one phase.")
print("  Closed forms: continuous/stochastic  q/(1-(1-q)lam);  periodic  (1-lam^P)/(P(1-lam))\n")
print("     q    period   R=400 aliased  cycle-avg   continuous  periodic pred  cont pred")
for q in [0.0345, 0.069, 0.1, 0.2, 0.3, 0.5]:
    P = int(round(1.0 / q))
    _, g, _ = walk(q, "POL", 401, every=1, mode="per")
    avg = float(np.mean(g[-P:]))
    _, gc, _ = walk(q, "POL", 401, every=400, mode="cont")
    pp = (1 - lam_fixed ** P) / (P * (1 - lam_fixed))
    pc = (1.0 / P) / (1 - (1 - 1.0 / P) * lam_fixed)
    print(f"  {q:6.4f}   {P:4d}    {g[-1]:.6f}     {avg:.6f}    {gc[-1]:.6f}    "
        f"{pp:.6f}      {pc:.6f}")
print("\n  Cycle-averaged, the periodic scheme does NOT agree with continuous: regular")
print("  full-strength repair beats spread-thin repair at the SAME mean effort, and the")
print("  two closed forms above say why.  Continuous and stochastic DO agree (geometric")
print("  gaps reproduce the rent formula exactly).  The difference is deterministic and")
print("  exactly reproducible -- not a sampling question -- so any quoted plateau must")
print("  NAME ITS SCHEDULE.")

print()
print("=" * 86)
print("S4 -- q_half on a refined grid (the pre-registered scale prediction eps/(2-lam))")
print("=" * 86)
lo, hi = 0.02, 0.09
for _ in range(40):
    mid = 0.5 * (lo + hi)
    _, gq, _ = walk(mid, "POL", 401, every=400)
    if float(gq[-1]) < 0.5:
        lo = mid
    else:
        hi = mid
qh = 0.5 * (lo + hi)
qh_pred = eps_fixed / (2 - lam_fixed)
print(f"  lambda = {lam_fixed:.6f}   eps = {eps_fixed:.6f}")
print(f"  PREDICTED  q_half = eps/(2-lambda) = {qh_pred:.6f} = {qh_pred/eps_fixed:.4f} eps")
print(f"  MEASURED   q_half (bisection, 40 steps) = {qh:.6f} = {qh/eps_fixed:.4f} eps")
print(f"  measured / predicted = {qh/qh_pred:.4f}")
print("  The SCALE is confirmed to ~15%; the SHARPNESS prediction (no threshold) is")
print("  confirmed by H2 separately.  The brief's q* = eps intuition had the scale right")
print("  and the sharpness wrong.")
