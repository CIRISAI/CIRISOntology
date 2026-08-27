#!/usr/bin/env python3
"""QF-1 — the emptiness rung's first instrument (exact, no sampling): KCBS.

THE COVER LESSON, recorded: the C5 graph state's five stabilizer GENERATORS
are classically satisfiable (all-plus assignment gives every g_i = +1), so
that cover reads CF = 0 identically — the gauge caught the wrong cover before
any state was measured. The odd-cycle emptiness lives in the EXCLUSIVITY
cover: KCBS (Klyachko–Can–Binicioglu–Shumovsky 2008; Cabello–Severini–Winter
graph approach — the pentagon's Lovász theta is √5, and the SAME C5 whose
ring state is our Bell ceiling). Credit where the object lives.

Five qutrit projectors Pi_i = |v_i><v_i|, adjacent pairs orthogonal
(compatible); contexts C_i = {Pi_i, Pi_(i+1)}, outcomes: i fires / i+1 fires /
neither (exclusivity: both-fire has probability zero). Noncontextual facet:
Sum <Pi_i> <= 2; the KCBS state reads sqrt(5).
Family: rho(lam) = (1-lam)|psi><psi| + lam I/3.
DERIVED CROSSING (staked before the LP runs on the state):
Sum(lam) = (1-lam)sqrt5 + 5lam/3 = 2  =>  lam* = (sqrt5-2)/(sqrt5-5/3)."""
import numpy as np
from scipy.optimize import linprog

def kcbs_vectors():
    """The standard KCBS construction: v_i adjacent-orthogonal, symmetric
    around the axis n = (0,0,1); psi = n gives <Pi_i> = 1/sqrt5 each."""
    vs = []
    c = 1/5**0.25 / np.sqrt(1 + 1/np.sqrt(5))
    for i in range(5):
        phi = 4*np.pi*i/5
        v = np.array([np.cos(phi), np.sin(phi), 0.0])
        z = np.sqrt(1/np.sqrt(5))
        vi = np.array([np.sqrt(1-z*z)*np.cos(phi), np.sqrt(1-z*z)*np.sin(phi), z])
        vs.append(vi)
    return vs

VS = kcbs_vectors()
PSI = np.array([0.0, 0.0, 1.0])
CONTEXTS = [(i, (i+1) % 5) for i in range(5)]

def model_of(rho):
    """Per context: exact (P_i fires, P_j fires, neither). Adjacent projectors
    are orthogonal so the three outcomes are exhaustive and exclusive."""
    ev = [float(np.real(VS[i] @ rho @ VS[i])) for i in range(5)]
    out = []
    for i, j in CONTEXTS:
        out.append({(1, 0): ev[i], (0, 1): ev[j],
                    (0, 0): max(1.0 - ev[i] - ev[j], 0.0), (1, 1): 0.0})
    return out

def contextual_fraction(model):
    nG = 1 << 5                      # 0/1 assignment per projector
    rows, rhs = [], []
    for ci, (i, j) in enumerate(CONTEXTS):
        for outs, p in model[ci].items():
            row = np.zeros(nG)
            for g in range(nG):
                if (((g >> i) & 1), ((g >> j) & 1)) == outs: row[g] = 1.0
            rows.append(row); rhs.append(p)
    res = linprog(-np.ones(nG), A_ub=np.array(rows), b_ub=np.array(rhs),
                  bounds=[(0, None)]*nG, method='highs')
    assert res.status == 0, res.message
    return 1.0 + res.fun

def family_model(lam):
    rho = (1-lam)*np.outer(PSI, PSI) + lam*np.eye(3)/3
    return model_of(rho)

def classical_lift_model():
    """Fine's null through the same pipeline: a mixture of valid 0/1
    assignments (independent sets of the pentagon), read out per context."""
    assigns = [0b00000, 0b00101, 0b01010, 0b10100, 0b01001, 0b10010]
    out = []
    for i, j in CONTEXTS:
        d = {(1,0):0.0,(0,1):0.0,(0,0):0.0,(1,1):0.0}
        for g in assigns:
            d[(((g >> i) & 1), ((g >> j) & 1))] += 1/len(assigns)
        out.append(d)
    return out

def zero_point(tol=1e-5):
    lo, hi = 0.0, 1.0
    while hi - lo > tol:
        mid = 0.5*(lo+hi)
        if contextual_fraction(family_model(mid)) > 1e-9: lo = mid
        else: hi = mid
    return 0.5*(lo+hi)

if __name__ == "__main__":
    import json
    sum0 = sum(float(VS[i] @ PSI)**2 for i in range(5))
    derived = (np.sqrt(5)-2)/(np.sqrt(5)-5/3)
    out = {"sum_ev_at_0": sum0, "quantum_value_sqrt5": float(np.sqrt(5)),
           "Q1_classical_lift_CF": contextual_fraction(classical_lift_model()),
           "Q2_KCBS_CF": contextual_fraction(family_model(0.0)),
           "Q3_zero_point": zero_point(), "Q3_derived": float(derived)}
    out["Q3_gap"] = abs(out["Q3_zero_point"] - out["Q3_derived"])
    print(json.dumps(out, indent=2))
