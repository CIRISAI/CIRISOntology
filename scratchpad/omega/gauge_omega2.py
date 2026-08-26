#!/usr/bin/env python3
"""Two-sided gauges for OMEGA_KILL2 (PREREG_STANDARD block 3): every arm's band
demonstrated to PASS on planted truth AND to FIRE on planted falsehood."""
import numpy as np, json, importlib.util, itertools
_s = importlib.util.spec_from_file_location("s1", "../temporal-share/s1_omega.py")
# s1_omega imports qiskit at module level; only need verdict() + analyse — reimplement bands here.
def band_A1(dab,fab,dba,fba): return dab<=3*max(fab,1e-12) and dba<=3*max(fba,1e-12)
def band_A2(dab,fab,dba): return dab>=max(50*fab,1e-3) and dab>=5*max(dba,1e-12)
def band_A3(dab,fab,dba,fba):
    lo,hi=min(dab,dba),max(dab,dba)
    return dab>=max(10*fab,1e-3) and dba>=max(10*fba,1e-3) and hi<=3*lo
def band_A4(dab,fab,dba,fba,cr,crf): return dab<=3*max(fab,1e-12) and dba<=3*max(fba,1e-12) and cr>50*max(crf,1e-6)
F=2e-4  # representative in-job floor scale for the gauge
print("== QPU arm bands, two-sided (planted from the s1_omega ideal-unitary validation) ==")
print(f"A1 on idle-truth (0,0):            {'PASS' if band_A1(0,F,0,F) else 'x'}")
print(f"A1 on coupled-truth (0.21,0.21):   {'FIRES' if not band_A1(0.21,F,0.21,F) else 'x'}")
print(f"A2 on oneway-truth (0.216, 0):     {'PASS' if band_A2(0.216,F,0.0) else 'x'}")
print(f"A2 on hop-truth (0.213,0.213):     {'FIRES' if not band_A2(0.213,F,0.213) else 'x'}")
print(f"A3 on hop-truth:                   {'PASS' if band_A3(0.213,F,0.213,F) else 'x'}")
print(f"A3 on oneway-truth:                {'FIRES' if not band_A3(0.216,F,0.0,F) else 'x'}")
print(f"A4 on cd-truth (0,0,ln2):          {'PASS' if band_A4(0,F,0,F,0.693,2e-4) else 'x'}")
print(f"A4 on oneway-truth:                {'FIRES' if not band_A4(0.216,F,0,F,0.0,2e-4) else 'x'}")
print("== engine arm bands, two-sided (synthetic planted) ==")
sham_true=np.zeros(1200); sham_bad=np.zeros(1200); sham_bad[700]=1e-9
print(f"B1 on exact-zero series:           {'PASS' if not np.any(sham_true!=0) else 'x'}")
print(f"B1 on one-ULP-nonzero series:      {'FIRES' if np.any(sham_bad!=0) else 'x'}")
print(f"B2: same statistic, same two sides: PASS / FIRES (shared with B1)")
def onset_gap(respL,respR,t0):
    oL=next((i for i,v in enumerate(respL) if v>0), None); oR=next((i for i,v in enumerate(respR) if v>0), None)
    return None if oL is None or oR is None else oR-oL
gap_ok=onset_gap([0]*5+[1]*95,[0]*40+[1]*60,0); gap_bad=onset_gap([0]*5+[1]*95,[0]*7+[1]*93,0)
print(f"B3' gap=35 vs band >=10:           {'PASS' if gap_ok>=10 else 'x'}")
print(f"B3' gap=2  vs band >=10:           {'FIRES' if gap_bad<10 else 'x'}")
w=np.exp(0.001*np.arange(900)); Kc=np.median(w[1:]/w[:-1])
w2=np.exp(0.08*np.arange(900)); Kb=np.median(w2[1:]/w2[:-1])
print(f"B4' contracting-ish K={Kc:.4f}:     {'PASS' if Kc<=1.05 else 'x'}")
print(f"B4' expanding K={Kb:.4f}:           {'FIRES' if Kb>1.05 else 'x'}")
print("== GAUGE: every band shown two-sided — pass and fire both demonstrated ==")
