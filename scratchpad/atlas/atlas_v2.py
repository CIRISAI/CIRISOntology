#!/usr/bin/env python3
"""Finite-model atlas v2 — the transport layer. Instrument for ATLAS_V2_STAKES.md.

Stakes were committed to disk BEFORE this file existed. Parts map 1:1 onto them:

  PART 0  gates  D1, D2, gauge-invariance          (atlas's own kill)
  PART 1  the permutation family: D4, D5, D6, D7   (derived-in-prereg, verified)
  PART 2  the realizability reduction + the glued-view collapse
  PART 3  B(i), B(ii) — minimal counterexample search, ascending
  PART 4  B(iv) — the surviving bridge, and whether both hypotheses are load-bearing
  PART 5  B(v) lossy holonomy, B(vi) loop-transports-where-a-leg-does-not
  PART 6  B(vii) adiabatic scaling of the mode-sector closure defect
  PART 7  exhaustive exact-implication scan over the boolean features
"""
import itertools, math, sys
from collections import Counter

from atlas_v2_core import (H, cond_entropy, mediator, factors, compose_map,
                           apply_view, pcomp, pinv, ppow, cycle_type, Atlas,
                           closed, closure_defect, rate_map, perm_family,
                           build_view, build_reroot)

PASS, FAIL = "CONFIRMED", "*** VIOLATED — ATLAS CODE WRONG ***"
verdicts = {}


# ==================================================================== PART 0
print("=" * 78)
print("PART 0 — GATES (the atlas's own kill: D1, D2, gauge-invariance)")
print("=" * 78)

# --- D1: r_loop = id  =>  gamma_loop = id on range(q1).
# r_loop = id forces every r to be a bijection, so bijections are WLOG here.
# Enumerate r12, r23 over all bijections of a 4-element X; r31 is then forced.
X4 = list(range(4))
bij4 = list(itertools.permutations(X4))
views4_k2 = list(itertools.product(range(2), repeat=4))
n_d1 = n_d1_flat = n_d1_carry = 0
for r12 in bij4:
    for r23 in bij4:
        r13 = tuple(r23[r12[i]] for i in X4)
        r31 = pinv(r13)                      # forces r_loop = id
        for q1 in views4_k2:
            for q2 in views4_k2:
                for q3 in views4_k2:
                    A = Atlas(X4, q1, q2, q3, r12, r23, r31)
                    assert A.rloop == tuple(X4)
                    n_d1 += 1
                    if A.legs_ok:
                        n_d1_carry += 1
                        g = A.gloop
                        if all(g[f] == f for f in A.range1):
                            n_d1_flat += 1
ok_d1 = (n_d1_flat == n_d1_carry)
verdicts["D1"] = ok_d1
print(f"D1 flat-limit gate: |X|=4, k=2, all r12,r23 bijections (r31 forced), all views")
print(f"  models={n_d1}  transportable={n_d1_carry}  gamma_loop=id on range(q1): "
      f"{n_d1_flat}/{n_d1_carry}")
print(f"  D1 {PASS if ok_d1 else FAIL}")

# --- D2: mode-blind views + mode-only re-roots => gamma_loop = id on range(q1).
# X = M x S, |M|=2, |S|=3; views functions of s alone; r(m,s) = (sigma(m), s).
M, S = [0, 1], [0, 1, 2]
XM = [(m, s) for m in M for s in S]
idx = {x: i for i, x in enumerate(XM)}
def modeonly_reroot(sigma, rho=(0, 1, 2)):
    return tuple(idx[(sigma[m], rho[s])] for (m, s) in XM)
sigmas = [(0, 1), (1, 0)]
blind_views = [tuple(f[s] for (m, s) in XM) for f in itertools.product(range(2), repeat=3)]
n_d2 = n_d2_carry = n_d2_flat = 0
for s12, s23, s31 in itertools.product(sigmas, repeat=3):
    r12, r23, r31 = (modeonly_reroot(s) for s in (s12, s23, s31))
    for q1, q2, q3 in itertools.product(blind_views, repeat=3):
        A = Atlas(XM, q1, q2, q3, r12, r23, r31)
        n_d2 += 1
        if A.legs_ok:
            n_d2_carry += 1
            n_d2_flat += all(A.gloop[f] == f for f in A.range1)
ok_d2 = (n_d2_flat == n_d2_carry)
verdicts["D2"] = ok_d2
print(f"\nD2 mode-blind gate: mode-blind views + mode-only re-roots, |S|=3, k=2")
print(f"  models={n_d2}  transportable={n_d2_carry}  flat: {n_d2_flat}/{n_d2_carry}")
print(f"  D2 {PASS if ok_d2 else FAIL}")

# --- D2': the SAME family but with rho != id must NOT be flat in general.
# ASCENDING over |S| and k. (The first version of this probe was pinned at |S|=3,
# k=2 and returned NONE; that is a SIZE artifact, not a refutation — a nontrivial
# holonomy on a mode-blind view needs the re-root to permute q1's fibers, hence at
# least two fibers of EQUAL size, which a 2-colouring of 3 microstates cannot supply.)
found_d2p = None
for nS in (2, 3, 4):
    for kk in (2, 3):
        if kk > nS:
            continue
        XS = [(m, s) for m in (0, 1) for s in range(nS)]
        iS = {x: i for i, x in enumerate(XS)}
        blind = [tuple(f[s] for (m, s) in XS)
                 for f in itertools.product(range(kk), repeat=nS)]
        idS = tuple(range(nS))
        mo = lambda sg, rh=idS: tuple(iS[(sg[m], rh[s])] for (m, s) in XS)
        for r_ in itertools.permutations(range(nS)):
            if r_ == idS:
                continue
            r12, r23, r31 = mo((0, 1), r_), mo((0, 1)), mo((0, 1))
            for q1, q2, q3 in itertools.product(blind, repeat=3):
                A = Atlas(XS, q1, q2, q3, r12, r23, r31)
                if A.legs_ok and not A.held_loop():
                    found_d2p = dict(nS=nS, k=kk, rho=r_, q1=q1, q2=q2, q3=q3,
                                     support=A.curvature_support())
                    break
            if found_d2p: break
        if found_d2p: break
    if found_d2p: break
verdicts["D2p"] = found_d2p is not None
print(f"\nD2' fixed fibration does NOT imply flat when the re-root moves the base:")
print(f"  witness (rho, q1, q2, q3, support) = {found_d2p}")
print(f"  D2' {'CONFIRMED (state-dependence is not what unlocks curvature)' if found_d2p else FAIL}")

# --- gauge invariance of the holonomy class under relabelling readings per context
import random
random.seed(20260826)
gauge_ok = True
for _ in range(4000):
    q1, q2, q3 = (random.choice(views4_k2) for _ in range(3))
    r12, r23, r31 = (random.choice(bij4) for _ in range(3))
    A = Atlas(X4, q1, q2, q3, r12, r23, r31)
    if not A.legs_ok:
        continue
    lam = [random.choice(list(itertools.permutations(range(2)))) for _ in range(3)]
    B = Atlas(X4, tuple(lam[0][v] for v in q1), tuple(lam[1][v] for v in q2),
              tuple(lam[2][v] for v in q3), r12, r23, r31)
    if not B.legs_ok or B.held_loop() != A.held_loop() or \
       B.curvature_support() != A.curvature_support():
        gauge_ok = False
        break
verdicts["gauge"] = gauge_ok
print(f"\nGAUGE: relabelling each context's readings preserves flat/nonflat and support")
print(f"  {PASS if gauge_ok else FAIL} on 4000 random models")

if not (ok_d1 and ok_d2 and gauge_ok):
    print("\nGATES FAILED — everything below is VOID.")
    sys.exit(1)


# ==================================================================== PART 1
print()
print("=" * 78)
print("PART 1 — the permutation family: D4 (mode-sector formula), D5, D6, D7")
print("=" * 78)

for n in (2, 3, 4):
    Xp, ip = perm_family(n)
    P = list(itertools.permutations(range(n)))
    ID = tuple(range(n))
    # gauge-fixed: a_i = id, b_i = beta_i ranges over P
    tot = ok_d4 = ok_d5 = ok_d6 = carry_ok = 0
    for betas in itertools.product(P, repeat=3):
        views = [build_view(Xp, ID, b) for b in betas]
        alphas = [pcomp(pinv(b), ID) for b in betas]      # alpha_i = (pi^1)^-1 pi^0
        for eps in itertools.product((0, 1), repeat=3):   # eps_12, eps_23, eps_31
            sig = [((1, 0) if e else (0, 1)) for e in eps]
            rr = [build_reroot(Xp, ip, s, ID) for s in sig]
            A = Atlas(Xp, views[0], views[1], views[2], rr[0], rr[1], rr[2])
            tot += 1
            # D5: carry on edge i->j exists iff alpha_i = alpha_j^{+-1} (rho = id)
            pred = []
            for (i, j, e) in ((0, 1, eps[0]), (1, 2, eps[1]), (2, 0, eps[2])):
                tgt = alphas[j] if e == 0 else pinv(alphas[j])
                pred.append(alphas[i] == tgt)
            got = [A.g12 is not None, A.g23 is not None, A.g31 is not None]
            ok_d5 += (pred == got)
            if not A.legs_ok:
                continue
            carry_ok += 1
            # D4: gamma_loop = a1 . alpha_1^-e31 alpha_3^-e23 alpha_2^-e12 . a1^-1
            core = pcomp(pcomp(ppow(alphas[0], -eps[2]), ppow(alphas[2], -eps[1])),
                         ppow(alphas[1], -eps[0]))
            predicted = core                     # a1 = id under the gauge
            actual = tuple(A.gloop[f] for f in range(n))
            ok_d4 += (actual == predicted)
            # D6: bijective re-roots => gamma_loop is a permutation
            ok_d6 += bool(A.gloop_is_perm())
    print(f"n={n}: models={tot}  transportable={carry_ok}"
          f"  D5 {ok_d5}/{tot}  D4 {ok_d4}/{carry_ok}  D6 {ok_d6}/{carry_ok}")
    verdicts[f"D4_n{n}"] = (ok_d4 == carry_ok)
    verdicts[f"D5_n{n}"] = (ok_d5 == tot)
    verdicts[f"D6_n{n}"] = (ok_d6 == carry_ok)

# D5 with rho free (the conjugacy condition proper), n = 3
n = 3
Xp, ip = perm_family(n)
P = list(itertools.permutations(range(n)))
ID = tuple(range(n))
tot = ok = 0
for betas in itertools.product(P, repeat=3):
    views = [build_view(Xp, ID, b) for b in betas]
    alphas = [pinv(b) for b in betas]
    for eps in itertools.product((0, 1), repeat=3):
        for rhos3 in itertools.product(P, repeat=3):
            sig = [((1, 0) if e else (0, 1)) for e in eps]
            rr = [build_reroot(Xp, ip, sig[t], rhos3[t]) for t in range(3)]
            A = Atlas(Xp, views[0], views[1], views[2], rr[0], rr[1], rr[2])
            pred = []
            for t, (i, j) in enumerate(((0, 1), (1, 2), (2, 0))):
                lhs = pcomp(pcomp(rhos3[t], alphas[i]), pinv(rhos3[t]))
                tgt = alphas[j] if eps[t] == 0 else pinv(alphas[j])
                pred.append(lhs == tgt)
            got = [A.g12 is not None, A.g23 is not None, A.g31 is not None]
            tot += 1
            ok += (pred == got)
print(f"D5 with rho free, n=3: {ok}/{tot} "
      f"{'CONFIRMED — transportability IS a conjugacy condition' if ok == tot else FAIL}")
verdicts["D5_rho_free"] = (ok == tot)

# D7: for the pure mode-advance dynamics, Closed q_i T  <=>  beta_i^2 = id
for n in (3, 4):
    Xp, ip = perm_family(n)
    P = list(itertools.permutations(range(n)))
    ID = tuple(range(n))
    Tmode = tuple(ip[(1 - m, s)] for (m, s) in Xp)
    ok = tot = 0
    for b in P:
        v = build_view(Xp, ID, b)
        tot += 1
        ok += (closed(v, Tmode) == (pcomp(b, b) == ID))
    print(f"D7 mode-advance closure, n={n}: {ok}/{tot} {PASS if ok == tot else FAIL}")
    verdicts[f"D7_n{n}"] = (ok == tot)


# ==================================================================== PART 2
print()
print("=" * 78)
print("PART 2 — realizability reduction, and what the GLUED VIEW actually carries")
print("=" * 78)
# Realizability: any (q1, qt2, qt3, rloop) is realized by r12=r23=id, r31=rloop.
X3 = list(range(3))
allmaps3 = list(itertools.product(X3, repeat=3))
allviews3 = list(itertools.product(range(2), repeat=3))
real_ok = True
for _ in range(3000):
    q1, qt2, qt3 = (random.choice(allviews3) for _ in range(3))
    rl = random.choice(allmaps3)
    A = Atlas(X3, q1, qt2, qt3, tuple(X3), tuple(X3), rl)
    if (A.qt2, A.qt3, A.rloop) != (qt2, qt3, rl):
        real_ok = False
        break
print(f"realizability of (q1,qt2,qt3,rloop) as a full 6-tuple atlas: "
      f"{PASS if real_ok else FAIL}")
verdicts["realizable"] = real_ok

# The glued view's information content, transportable vs obstructed.
same_when_ok = diff_when_ok = same_when_obs = strict_when_obs = 0
for q1, q2, q3 in itertools.product(allviews3, repeat=3):
    for rl in allmaps3:
        A = Atlas(X3, q1, q2, q3, tuple(X3), tuple(X3), rl)
        G = A.glued()
        same_partition = (cond_entropy(G, q1) == 0.0)
        if A.legs_ok:
            same_when_ok += same_partition
            diff_when_ok += (not same_partition)
        else:
            same_when_obs += same_partition
            strict_when_obs += (not same_partition)
print(f"transportable atlases: glued view has q1's fibers in {same_when_ok} models, "
      f"strictly finer in {diff_when_ok}")
print(f"obstructed atlases:    glued view has q1's fibers in {same_when_obs} models, "
      f"strictly finer in {strict_when_obs}")
verdicts["glue_collapse"] = (diff_when_ok == 0)
print("  => " + ("TRANSPORTABLE ATLAS: the glued view carries EXACTLY the base view. "
                 "All content is degree-1." if diff_when_ok == 0 else
                 "glued view can refine even when transportable (stake wrong)"))


# ==================================================================== PART 3
print()
print("=" * 78)
print("PART 3 — B(i) and B(ii): minimal counterexample search, ascending")
print("=" * 78)

def search_bridges(nX, k, want):
    """Exhaustive over (q1,qt2,qt3,rloop,T) at this size. want in {'i','ii'}.
    Returns the first (lexicographically smallest) witness, or None."""
    Xs = list(range(nX))
    views = list(itertools.product(range(k), repeat=nX))
    maps = list(itertools.product(Xs, repeat=nX))
    idn = tuple(Xs)
    for q1 in views:
        for qt2 in views:
            for qt3 in views:
                for rl in maps:
                    A = Atlas(Xs, q1, qt2, qt3, idn, idn, rl)
                    if not A.legs_ok:
                        continue
                    flat = A.held_loop()
                    if want == 'i' and not flat:
                        continue
                    if want == 'ii' and flat:
                        continue
                    G = A.glued()
                    for T in maps:
                        cg = closed(G, T)
                        c1 = closed(q1, T)
                        if want == 'i' and not (cg and c1):
                            # zero holonomy but the glued view is NOT closed
                            return dict(q1=q1, qt2=qt2, qt3=qt3, rloop=rl, T=T,
                                        support=A.curvature_support(),
                                        closedG=cg, closed1=c1,
                                        dG=closure_defect(G, T))
                        if want == 'ii' and cg and c1:
                            # nonzero holonomy but the glued view IS closed
                            return dict(q1=q1, qt2=qt2, qt3=qt3, rloop=rl, T=T,
                                        support=A.curvature_support(),
                                        closedG=cg, closed1=c1,
                                        dG=closure_defect(G, T))
    return None

for want, label in (('ii', 'B(ii)  nonzero holonomy => closure failure of the glued view'),
                    ('i',  'B(i)   zero holonomy => closure of the glued view')):
    hit = None
    for nX in (2, 3, 4):
        for k in (2, 3):
            if k > nX:
                continue
            hit = search_bridges(nX, k, want)
            if hit:
                print(f"\n{label}")
                print(f"  KILLED. Minimal counterexample at |X|={nX}, k={k}:")
                for key in ('q1', 'qt2', 'qt3', 'rloop', 'T'):
                    print(f"    {key:6s} = {hit[key]}")
                print(f"    curvature support = {hit['support']},  "
                      f"Closed(G,T) = {hit['closedG']},  Closed(q1,T) = {hit['closed1']},"
                      f"  Delta_G = {hit['dG']:.4f}")
                verdicts[f"B{want}"] = "KILLED"
                break
        if hit:
            break
    if not hit:
        print(f"\n{label}\n  NO COUNTEREXAMPLE up to |X|=4, k=3 — the bridge SURVIVES.")
        verdicts[f"B{want}"] = "SURVIVES"

# The quantified form of B(ii): is there ANY nondecreasing f with Delta_G >= f(support)?
pairs = set()
Xs = list(range(3)); idn = tuple(Xs)
for q1, qt2, qt3 in itertools.product(list(itertools.product(range(2), repeat=3)), repeat=3):
    for rl in list(itertools.product(Xs, repeat=3)):
        A = Atlas(Xs, q1, qt2, qt3, idn, idn, rl)
        if not A.legs_ok:
            continue
        sup = A.curvature_support()
        G = A.glued()
        for T in itertools.product(Xs, repeat=3):
            pairs.add((sup, round(closure_defect(G, T), 12)))
mins = {}
for s, d in pairs:
    mins[s] = min(mins.get(s, 9e9), d)
print(f"\n  quantified envelope  min Delta_G by curvature support: "
      f"{ {s: round(v,6) for s, v in sorted(mins.items())} }")
print("  => any f with f(support>=1) > 0 is refuted iff min at support>=1 is 0.0")


# ==================================================================== PART 4
print()
print("=" * 78)
print("PART 4 — B(iv): curvature is an automorphism of the habit")
print("=" * 78)
# Exhaustive over the permutation family n=3 (rho free) x structured dynamics.
n = 3
Xp, ip = perm_family(n)
P = list(itertools.permutations(range(n)))
ID = tuple(range(n))
allS = list(itertools.product(range(n), repeat=n))     # all maps S->S (non-invertible too)

tested = held = 0
viol_eqv_closed = []
counter_no_eqv = None
counter_no_closed = None
stat = Counter()
for betas in itertools.product(P, repeat=3):
    views = [build_view(Xp, ID, b) for b in betas]
    for eps in itertools.product((0, 1), repeat=3):
        for rhos3 in itertools.product(P, repeat=3):
            sig = [((1, 0) if e else (0, 1)) for e in eps]
            rr = [build_reroot(Xp, ip, sig[t], rhos3[t]) for t in range(3)]
            A = Atlas(Xp, views[0], views[1], views[2], rr[0], rr[1], rr[2])
            if not A.legs_ok:
                continue
            for tau in ((0, 1), (1, 0)):
                for t0 in allS:
                    for t1 in allS:
                        T = tuple(ip[(tau[m], (t0 if m == 0 else t1)[s])] for (m, s) in Xp)
                        eqv = all(T[A.rloop[i]] == A.rloop[T[i]] for i in range(len(Xp)))
                        h = rate_map(A.q1, T)
                        c1 = h is not None
                        if not c1:
                            stat['not_closed'] += 1
                            if eqv and counter_no_closed is None:
                                # closure dropped: is the commutator still zero?
                                pass
                            continue
                        g = A.gloop
                        K = sum(1 for f in A.range1
                                if g[h[f]] != h[g[f]])
                        if eqv:
                            tested += 1
                            held += (K == 0)
                            if K != 0 and len(viol_eqv_closed) < 3:
                                viol_eqv_closed.append((betas, eps, rhos3, tau, t0, t1, K))
                            stat['eqv_closed'] += 1
                        else:
                            stat['noneqv_closed'] += 1
                            if K != 0 and counter_no_eqv is None:
                                counter_no_eqv = dict(betas=betas, eps=eps, rhos=rhos3,
                                                      tau=tau, t0=t0, t1=t1, K=K)
    # this sweep is large; the beta loop is the outer one, keep it whole
print(f"models with equivariance AND closure: {tested}")
print(f"  commutator [gamma_loop, h] = 0 on range(q1): {held}/{tested} "
      f"{PASS if held == tested else FAIL}")
verdicts["Biv"] = (held == tested and tested > 0)
if viol_eqv_closed:
    print(f"  VIOLATIONS: {viol_eqv_closed}")
print(f"  equivariance dropped, closure kept: {stat['noneqv_closed']} models; "
      f"first commutator violation: {counter_no_eqv}")
print("  => equivariance is LOAD-BEARING" if counter_no_eqv else
      "  => equivariance was NOT needed (bridge is stronger than staked)")
verdicts["Biv_eqv_loadbearing"] = counter_no_eqv is not None


# ==================================================================== PART 5
print()
print("=" * 78)
print("PART 5 — B(v) lossy holonomy;  B(vi) loop transports where a leg does not")
print("=" * 78)
lossy = None
for nX in (2, 3, 4):
    Xs = list(range(nX)); idn = tuple(Xs)
    kk = 2 if nX == 2 else 3
    for k in range(2, min(kk, nX) + 1):
        views = list(itertools.product(range(k), repeat=nX))
        maps = list(itertools.product(Xs, repeat=nX))
        for q1 in views:
            for qt2 in views:
                for qt3 in views:
                    for rl in maps:
                        A = Atlas(Xs, q1, qt2, qt3, idn, idn, rl)
                        if not A.legs_ok:
                            continue
                        if A.gloop_is_perm() is False:
                            lossy = dict(nX=nX, k=k, q1=q1, qt2=qt2, qt3=qt3, rloop=rl,
                                         gloop={f: A.gloop[f] for f in A.range1},
                                         range1=A.range1)
                            break
                    if lossy: break
                if lossy: break
            if lossy: break
        if lossy: break
    if lossy: break
print(f"B(v) lossy holonomy: {'WITNESS' if lossy else 'NONE up to |X|=4'}")
if lossy:
    print(f"  |X|={lossy['nX']}, k={lossy['k']}: q1={lossy['q1']} qt2={lossy['qt2']} "
          f"qt3={lossy['qt3']} rloop={lossy['rloop']}")
    print(f"  range(q1)={lossy['range1']}  gamma_loop={lossy['gloop']}  (non-injective)")
    print("  => irreversible transport gives a COLLAPSING holonomy: the loop returns "
          "fewer distinctions than it took.")
verdicts["Bv"] = "WITNESS" if lossy else "NONE"

# B(vi): loop-level carry exists while a leg's does not
Xs = list(range(3)); idn = tuple(Xs)
views3 = list(itertools.product(range(2), repeat=3))
maps3 = list(itertools.product(Xs, repeat=3))
n_obs = n_loop_ok = 0
first_vi = None
for q1, qt2, qt3 in itertools.product(views3, repeat=3):
    for rl in maps3:
        A = Atlas(Xs, q1, qt2, qt3, idn, idn, rl)
        if A.legs_ok:
            continue
        n_obs += 1
        if A.gloop_direct is not None:
            n_loop_ok += 1
            if first_vi is None and not A.held_loop():
                first_vi = dict(q1=q1, qt2=qt2, qt3=qt3, rloop=rl,
                                legs=(A.g12 is not None, A.g23 is not None,
                                      A.g31 is not None),
                                gloop=A.gloop_direct)
print(f"\nB(vi) obstructed atlases: {n_obs}; loop-level carry nevertheless exists in "
      f"{n_loop_ok} ({100*n_loop_ok/max(n_obs,1):.1f}%)")
print(f"  first NON-FLAT such atlas: {first_vi}")
verdicts["Bvi"] = n_loop_ok > 0


# ==================================================================== PART 6
print()
print("=" * 78)
print("PART 6 — B(vii): adiabatic scaling of the mode-sector closure defect")
print("=" * 78)
# Stochastic slow mode: T flips the mode w.p. p, microstate held. n = 3,
# view q(m,s) = pi^m(s) with beta a 3-cycle (maximally state-dependent).
n = 3
Xp, ip = perm_family(n)
beta = (1, 2, 0)
v = build_view(Xp, (0, 1, 2), beta)
print(f"  view: q(0,s)=s, q(1,s)=beta(s), beta={beta} (3-cycle, beta^2 != id)")
print(f"{'p':>8} {'Delta_v (nats)':>16} {'Delta/p':>12}")
for p in (0.0, 0.001, 0.01, 0.05, 0.1, 0.25, 0.5):
    # joint over (v_t, v_{t+1}) under uniform state, mode flips w.p. p
    joint = Counter()
    for i, (m, s) in enumerate(Xp):
        for mm, pr in ((m, 1 - p), (1 - m, p)):
            if pr <= 0:
                continue
            joint[(v[i], v[ip[(mm, s)]])] += pr
    tot = sum(joint.values())
    pj = [c / tot for c in joint.values()]
    marg = Counter()
    for (a, b), c in joint.items():
        marg[a] += c
    pm = [c / tot for c in marg.values()]
    d = -sum(x * math.log(x) for x in pj if x > 0) + sum(x * math.log(x) for x in pm if x > 0)
    print(f"{p:8.3f} {d:16.6f} {('-' if p == 0 else f'{d/p:12.4f}')}")
print("  (adiabatic limit p=0 must read exactly 0; the leading behaviour is the finding)")


# ==================================================================== PART 7
print()
print("=" * 78)
print("PART 7 — exhaustive exact-implication scan over the boolean features")
print("=" * 78)
n = 3
Xp, ip = perm_family(n)
P = list(itertools.permutations(range(n)))
ID = tuple(range(n))
rows = []
for betas in itertools.product(P, repeat=3):
    views = [build_view(Xp, ID, b) for b in betas]
    for eps in itertools.product((0, 1), repeat=3):
        for rhos3 in itertools.product(P, repeat=3):
            sig = [((1, 0) if e else (0, 1)) for e in eps]
            rr = [build_reroot(Xp, ip, sig[t], rhos3[t]) for t in range(3)]
            A = Atlas(Xp, views[0], views[1], views[2], rr[0], rr[1], rr[2])
            if not A.legs_ok:
                continue
            SD = any(b != ID for b in betas)
            MO = all(r == ID for r in rhos3)
            HOL = not A.held_loop()
            for tau in ((0, 1), (1, 0)):
                for t0 in (ID, (1, 2, 0), (0, 0, 0)):
                    for t1 in (ID, (1, 2, 0), (0, 0, 0)):
                        T = tuple(ip[(tau[m], (t0 if m == 0 else t1)[s])] for (m, s) in Xp)
                        h = rate_map(A.q1, T)
                        G = A.glued()
                        rows.append(dict(
                            HOL=HOL, SD=SD, MODEONLY=MO,
                            EQV=all(T[A.rloop[i]] == A.rloop[T[i]] for i in range(len(Xp))),
                            C1=h is not None,
                            HELD1=tuple(A.q1[T[i]] for i in range(len(Xp))) == A.q1,
                            CG=closed(G, T),
                            PERM=bool(A.gloop_is_perm()),
                            COMM=(h is not None and
                                  all(A.gloop[h[f]] == h[A.gloop[f]] for f in A.range1)),
                        ))
feats = ['HOL', 'SD', 'MODEONLY', 'EQV', 'C1', 'HELD1', 'CG', 'PERM', 'COMM']
print(f"models scanned: {len(rows)}")
lits = [(f, s) for f in feats for s in (True, False)]
survivors = []
for (fa, sa) in lits:
    for (fb, sb) in lits:
        if fa == fb:
            continue
        ante = [r for r in rows if r[fa] == sa]
        if not ante:
            continue
        if all(r[fb] == sb for r in ante):
            survivors.append((f"{'' if sa else '¬'}{fa}", f"{'' if sb else '¬'}{fb}",
                              len(ante)))
print("exact single-antecedent implications (over transportable models):")
for a, b, n_ in sorted(survivors):
    print(f"  {a:10s} => {b:10s}   (support {n_})")
# pair antecedents, reported only when neither half alone suffices
singles = {(a, b) for a, b, _ in survivors}
pair_sv = []
for (fa, sa), (fb, sb) in itertools.combinations(lits, 2):
    if fa == fb:
        continue
    ante = [r for r in rows if r[fa] == sa and r[fb] == sb]
    if len(ante) < 20:
        continue
    for (fc, sc) in lits:
        if fc in (fa, fb):
            continue
        A_ = f"{'' if sa else '¬'}{fa}"; B_ = f"{'' if sb else '¬'}{fb}"
        C_ = f"{'' if sc else '¬'}{fc}"
        if (A_, C_) in singles or (B_, C_) in singles:
            continue
        if all(r[fc] == sc for r in ante):
            pair_sv.append((A_, B_, C_, len(ante)))
print("exact two-antecedent implications (neither half alone suffices):")
for a, b, c, n_ in sorted(pair_sv):
    print(f"  {a} & {b:10s} => {c:10s}   (support {n_})")

print()
print("=" * 78)
print("VERDICTS:", verdicts)
