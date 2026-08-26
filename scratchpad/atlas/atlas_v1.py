#!/usr/bin/env python3
"""Finite-model atlas v1 — instrument for ATLAS_V1_STAKES.md (staked first).

Part 1: deterministic sweep, 2x2 product space, ALL 256 maps. Verifies S1 exactly.
Part 2: stochastic common-driver family. Measures S2.
Part 3: the autonomy-memory-work frontier on the 2-bit repair model. Plots H1's data.
"""
import itertools, math
import numpy as np

def H(p):
    p = np.asarray(p, float); p = p[p > 1e-15]
    return float(-(p * np.log(p)).sum())

# ---------------- Part 1: deterministic sweep (S1) ----------------
STATES = list(itertools.product((0, 1), (0, 1)))
def closed(view, T):
    """Does view∘T factor through view? Exact, by fibers."""
    img = {}
    for s in STATES:
        v = view(s); w = view(T[s])
        if v in img and img[v] != w: return False
        img[v] = w
    return True
def is_product(T):
    fa = all(T[(a,0)][0] == T[(a,1)][0] for a in (0,1))
    gb = all(T[(0,b)][1] == T[(1,b)][1] for b in (0,1))
    return fa and gb

fst = lambda s: s[0]; snd = lambda s: s[1]; par = lambda s: s[0]^s[1]
n_maps = both_closed = product = agree = par_closed = 0
one_way = 0
for outs in itertools.product(STATES, repeat=4):
    T = dict(zip(STATES, outs)); n_maps += 1
    bc = closed(fst,T) and closed(snd,T); pr = is_product(T)
    both_closed += bc; product += pr; agree += (bc == pr)
    par_closed += closed(par,T)
    one_way += (closed(fst,T) and not closed(snd,T)) or (closed(snd,T) and not closed(fst,T))
print(f"PART 1 (S1): {n_maps} maps  both-closed={both_closed}  product={product}  agree={agree}/{n_maps}")
print(f"  S1 {'CONFIRMED EXACTLY' if agree==n_maps and both_closed==product else '*** VIOLATED — ATLAS CODE WRONG ***'}")
print(f"  extras: one-way-closed maps={one_way}, parity-view closed={par_closed}")

# ---------------- Part 2: common-driver family (S2) ----------------
def cmi(joint, X_ax, Y_ax, Z_ax):
    """I(X;Y|Z) from a joint array with named axes lists."""
    axes = list(range(joint.ndim))
    def marg(keep):
        drop = tuple(a for a in axes if a not in keep)
        return joint.sum(axis=drop) if drop else joint
    XZ = marg(sorted(X_ax+Z_ax)); YZ = marg(sorted(Y_ax+Z_ax))
    XYZ = marg(sorted(X_ax+Y_ax+Z_ax)); Z = marg(sorted(Z_ax)) if Z_ax else None
    hz = H(Z.ravel()) if Z_ax else 0.0
    return H(XZ.ravel()) + H(YZ.ravel()) - H(XYZ.ravel()) - hz

print("\nPART 2 (S2): common driver a'=a^n, b'=b^n, shared n~Bern(q); uniform inputs")
print(f"{'q':>6} {'I(B;A_next|A)':>14} {'I(A;B_next|B)':>14} {'I(A_n;B_n|A,B)':>15}")
for q in (0.1, 0.25, 0.5):
    # joint over (a, b, a', b'), axes 0..3
    J = np.zeros((2,2,2,2))
    for a,b in STATES:
        for n,pn in ((0,1-q),(1,q)):
            J[a,b,a^n,b^n] += 0.25*pn
    d_ba = cmi(J,[1],[2],[0])       # I(B_t ; A_{t+1} | A_t)
    d_ab = cmi(J,[0],[3],[1])       # I(A_t ; B_{t+1} | B_t)
    corr = cmi(J,[2],[3],[0,1])     # created correlation given the FULL input
    print(f"{q:6.2f} {d_ba:14.3e} {d_ab:14.3e} {corr:15.6f}")
print("  S2 reading: both closure defects ZERO while the channel creates correlation ->")
print("  the stochastic gap between mutual closure and productness IS common-driver correlation.")

print("\n  control: genuine one-way b'=b^(a&m), m~Bern(q), a'=a")
for q in (0.25, 0.5):
    J = np.zeros((2,2,2,2))
    for a,b in STATES:
        for m,pm in ((0,1-q),(1,q)):
            J[a,b,a,b^(a&m)] += 0.25*pm
    print(f"  q={q}: I(A;B_next|B)={cmi(J,[0],[3],[1]):.6f}  I(B;A_next|A)={cmi(J,[1],[2],[0]):.3e}")

# ---------------- Part 3: the H1 frontier ----------------
print("\nPART 3 (H1): 2-bit code {00,11}, iid flip eps, repair rate w -> nearest codeword")
print("  Delta_v = I(X_t; C_{t+1} | C_t) of UNREPAIRED chain at stationarity (uniform)")
print("  W* = min w such that stationary P(in code) >= 0.99")
print(f"{'eps':>6} {'Delta_v':>10} {'W*':>8} {'W*/Delta_v':>11}")
code = {(0,0),(1,1)}
def step_matrix(eps, w):
    P = np.zeros((4,4)); idx = {s:i for i,s in enumerate(STATES)}
    for s in STATES:
        for f1,p1 in ((0,1-eps),(1,eps)):
            for f2,p2 in ((0,1-eps),(1,eps)):
                t = (s[0]^f1, s[1]^f2); p = p1*p2
                if t in code:
                    P[idx[s], idx[t]] += p
                else:
                    # repair w.p. w: to nearest codeword (tie -> uniform over the two)
                    P[idx[s], idx[t]] += p*(1-w)
                    P[idx[s], idx[(0,0)]] += p*w*0.5
                    P[idx[s], idx[(1,1)]] += p*w*0.5
    return P, idx
def stationary(P):
    vals, vecs = np.linalg.eig(P.T)
    v = np.real(vecs[:, np.argmin(np.abs(vals-1))]); v = np.abs(v); return v/v.sum()
for eps in (0.02, 0.05, 0.1, 0.2):
    # Delta_v of unrepaired chain, stationary = uniform (bit-flip chain is doubly stochastic)
    P0,_ = step_matrix(eps, 0.0)
    J = np.zeros((4,2))   # (x_t, c_{t+1})
    for i,s in enumerate(STATES):
        for j,t in enumerate(STATES):
            J[i, 1 if t in code else 0] += 0.25*P0[i,j]
    # I(X;C'|C): split X axis by c(x)
    HC1 = H(J.sum(axis=0))
    Hjoint = H(J.ravel())
    # H(C'|C): group rows by code membership
    JC = np.zeros((2,2))
    for i,s in enumerate(STATES): JC[1 if s in code else 0] += J[i]
    d_v = (H(JC.sum(axis=1)) + HC1 - H(JC.ravel())) * 0 + (Hjoint*0)  # placeholder
    # compute properly: I(X;C'|C) = H(C'|C) - H(C'|X)
    HCp_given_C = H(JC.ravel()) - H(JC.sum(axis=1))
    HCp_given_X = H(J.ravel()) - H(J.sum(axis=1))
    d_v = HCp_given_C - HCp_given_X
    # W*
    ws = np.linspace(0,1,2001); wstar = None
    for w in ws:
        P,_ = step_matrix(eps, w); pi = stationary(P)
        if pi[0]+pi[3] >= 0.99: wstar = w; break
    print(f"{eps:6.2f} {d_v:10.5f} {'-' if wstar is None else f'{wstar:8.4f}'} "
          f"{'-' if wstar is None or d_v<1e-12 else f'{wstar/d_v:11.3f}'}")
print("  (frontier data only; any f(Delta) must be DERIVED before it is claimed)")
