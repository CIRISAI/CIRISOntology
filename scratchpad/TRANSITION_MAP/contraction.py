"""Contraction-map existence checker (arXiv:2409.17317 Thm 2.1, after Bao et al.).

An n-party candidate HEI  sum_{u<=M} S(I_u) >= sum_{v<=N} S(J_v)  is VALID iff there
is f : {0,1}^M -> {0,1}^N with d_H(x,x') >= d_H(f(x),f(x')) for all x,x', satisfying
the boundary conditions f(x_{A_i}) = y_{A_i} on the n+1 occurrence bitstrings
(the (n+1)-th party is the purifier, whose LHS bitstring is all-zero).

Key reduction: Hamming distance IS hypercube graph distance, so a map that does not
increase distance across EDGES cannot increase it along any geodesic. Contraction
therefore needs only M*2^(M-1) edge checks, and existence is a small CSP.
"""
import itertools, sys
from functools import lru_cache

def occ(term_sets, party):
    """occurrence bitstring: which terms contain this party"""
    return tuple(1 if party in T else 0 for T in term_sets)

def hd(a, b): return sum(x != y for x, y in zip(a, b))

def neighbours(x):
    for i in range(len(x)):
        y = list(x); y[i] ^= 1; yield tuple(y)

def exists_contraction(LHS, RHS, parties, verbose=False):
    """parties: list of party labels; the purifier must be included and appear in no
    LHS/RHS term (its bitstrings are all-zero)."""
    M, N = len(LHS), len(RHS)
    bc = {}
    for p in parties:
        x, y = occ(LHS, p), occ(RHS, p)
        if x in bc and bc[x] != y:
            return False, None, "boundary conditions inconsistent"
        bc[x] = y
    # sanity: boundary conditions must themselves be contracting
    for x1, y1 in bc.items():
        for x2, y2 in bc.items():
            if hd(y1, y2) > hd(x1, x2):
                return False, None, "boundary conditions already violate contraction"
    domain = list(itertools.product((0, 1), repeat=M))
    codomain = list(itertools.product((0, 1), repeat=N))
    free = [x for x in domain if x not in bc]
    assign = dict(bc)
    def ok(x, val):
        for y in neighbours(x):
            if y in assign and hd(val, assign[y]) > 1:
                return False
        return True
    def bt(i):
        if i == len(free): return True
        x = free[i]
        for val in codomain:
            if ok(x, val):
                assign[x] = val
                if bt(i + 1): return True
                del assign[x]
        return False
    if not bt(0):
        return False, None, "no contraction map"
    # full verification, not just edges, as an independent check of the reduction
    for a in domain:
        for b in domain:
            if hd(assign[a], assign[b]) > hd(a, b):
                return False, None, "EDGE REDUCTION FAILED — bug"
    return True, assign, "ok"

if __name__ == '__main__':
    A, B, C, O = 'A', 'B', 'C', 'O'
    print("=== CONTROL 1: MMI (must be VALID — the paper's star-graph example) ===")
    LHS = [{A,B}, {A,C}, {B,C}]
    RHS = [{A}, {B}, {C}, {A,B,C}]
    okk, f, msg = exists_contraction(LHS, RHS, [A,B,C,O])
    print(f"  MMI  M={len(LHS)} N={len(RHS)}  contraction map exists: {okk}  ({msg})")
    if f:
        for x in sorted(f): print(f"    f{x} = {f[x]}")

    print("\n=== CONTROL 2: MMI REVERSED (must be INVALID) ===")
    okk2, _, msg2 = exists_contraction(RHS, LHS, [A,B,C,O])
    print(f"  reversed  M={len(RHS)} N={len(LHS)}  contraction map exists: {okk2}  ({msg2})")

    print("\n=== CONTROL 3: subadditivity S(A)+S(B) >= S(AB) (VALID) ===")
    ok3, _, m3 = exists_contraction([{A},{B}], [{A,B}], [A,B,O])
    print(f"  SA: {ok3}  ({m3})")

    print("\n=== CONTROL 4: strong subadditivity S(AB)+S(BC) >= S(B)+S(ABC) (VALID) ===")
    ok4, _, m4 = exists_contraction([{A,B},{B,C}], [{B},{A,B,C}], [A,B,C,O])
    print(f"  SSA: {ok4}  ({m4})")

    gate = okk and (not okk2) and ok3 and ok4
    print(f"\nIMPLEMENTATION GATE: {'PASSES' if gate else 'FAILS — nothing downstream may be believed'}")
