#!/usr/bin/env python3
"""Two-sided gauge for N2 (rent bracket + cycle-memory on QPU decay).

Model: per-slot survival lam (possibly a nonneg mixture of modes), deposit s0.
Ladder: P(k) = Pinf + (P0-Pinf)*prod(lam over k slots).  Bracket (GCOST 4.2):
R(p,C=2) in [s0eff*lam_fast^p, s0eff*lam_slow^p] +/- 3*sigma_shot.
Memory arm: |R(p,4)-R(p,2)| <= 3*sigma_diff.
Estimators are the frozen nonparametric ones (no curve fits):
  lam_fast = (P(1)-Pinf)/(P(0)-Pinf); lam_slow = ((P(32)-Pinf)/(P(16)-Pinf))^(1/16).
All readings at 4096-shot binomial noise."""
import numpy as np
rng = np.random.default_rng(20260826)
SHOTS, PINF = 4096, 0.015
KS, PS = [0,1,2,4,8,16,32], [2,4,8,16]

def shot(p): return rng.binomial(SHOTS, min(max(p,0),1))/SHOTS

def ladder(modes, w, s0):
    # P(k) for mixture: survival amplitude = sum w_j lam_j^k, thermal offset PINF
    return {k: PINF + (s0-PINF)*sum(wi*l**k for wi,l in zip(w,modes)) for k in KS}

def run_case(name, modes, w, s0, dose_lam=None, heat=0.0):
    """dose_lam: per-cycle survival override list per cycle (None = mixture);
       heat: deposit degradation per cycle (s0_eff*(1-heat*C))."""
    P = {k: shot(v) for k,v in ladder(modes,w,s0).items()}
    lam_f = (P[1]-PINF)/(P[0]-PINF)
    lam_s = ((P[32]-PINF)/(P[16]-PINF))**(1/16)
    s0e = shot(s0)
    sig = np.sqrt(0.25/SHOTS)
    ok_brk, ok_mem = True, True
    for p in PS:
        readings = {}
        for C in (2,4):
            s = s0*(1-heat*(C-1))
            if dose_lam is not None:
                surv = dose_lam[min(C-1,len(dose_lam)-1)]**p
            else:
                surv = sum(wi*l**p for wi,l in zip(w,modes))
            readings[C] = shot(PINF + (s-PINF)*surv)
        lo, hi = s0e*lam_f**p - 3*sig, s0e*lam_s**p + 3*sig
        # thermal-consistent bracket on the same scale as readings
        lo, hi = PINF + (s0e-PINF)*lam_f**p - 3*sig, PINF + (s0e-PINF)*lam_s**p + 3*sig
        if not (lo <= readings[2] <= hi): ok_brk = False
        if abs(readings[4]-readings[2]) > 3*sig*np.sqrt(2): ok_mem = False
    print(f"{name}: lam_fast={lam_f:.4f} lam_slow={lam_s:.4f} "
          f"bracket={'holds' if ok_brk else 'VIOLATION'} memory={'holds' if ok_mem else 'VIOLATION'}")
    return ok_brk, ok_mem

print("== N2 gauge: planted truth at 4096 shots, frozen estimators ==")
b1,m1 = run_case("PASS single-mode      ", [0.92],[1.0], 0.97)
b2,m2 = run_case("PASS two-mode mixture ", [0.85,0.97],[0.6,0.4], 0.97)
b3,m3 = run_case("FIRE out-of-bracket   ", [0.85,0.97],[0.6,0.4], 0.97, dose_lam=[0.70,0.70])
b4,m4 = run_case("FIRE cycle-memory heat", [0.92],[1.0], 0.97, heat=0.06)
assert b1 and m1 and b2 and m2, "pass side failed"
assert not b3, "bracket fire side failed to fire"
assert not m4, "memory fire side failed to fire"
print("gauge verdict: pass sides PASS inside bands; planted violations FIRE. Two-sided.")
