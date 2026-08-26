#!/usr/bin/env python3
"""Atlas v2 core — primitives shared by atlas_v2.py and atlas_v2_addendum.py.

Split out of atlas_v2.py verbatim so the addendum can import them without
re-running the sweeps. No behaviour change.
"""
import itertools, math
from collections import Counter

# ---------------------------------------------------------------- primitives

def H(counts):
    """Entropy in nats of a multiset of counts."""
    n = sum(counts)
    return -sum((c / n) * math.log(c / n) for c in counts if c > 0)


def cond_entropy(u, w):
    """H(u|w) in nats, uniform measure on the index set. Zero iff u factors thru w."""
    n = len(u)
    joint = Counter(zip(w, u))
    marg = Counter(w)
    return H(list(joint.values())) - H(list(marg.values()))


def mediator(u, w):
    """The unique h with u = h o w on range(w), or None if u does not factor thru w."""
    h = {}
    for a, b in zip(w, u):
        if a in h:
            if h[a] != b:
                return None
        else:
            h[a] = b
    return h


def factors(u, w):
    return mediator(u, w) is not None


def compose_map(h, g):
    """h o g as a dict, on g's domain."""
    return {x: h[y] for x, y in g.items() if y in h}


def apply_view(q, r, X):
    """q o r as a tuple over X (q, r given as tuples indexed by state index)."""
    return tuple(q[r[i]] for i in range(len(X)))


# permutations as tuples: p[i] = image of i
def pcomp(p, q):
    return tuple(p[q[i]] for i in range(len(q)))


def pinv(p):
    out = [0] * len(p)
    for i, v in enumerate(p):
        out[v] = i
    return tuple(out)


def ppow(p, e):
    n = len(p)
    out = tuple(range(n))
    base = p if e >= 0 else pinv(p)
    for _ in range(abs(e)):
        out = pcomp(base, out)
    return out


def cycle_type(p):
    n = len(p)
    seen = [False] * n
    ct = []
    for i in range(n):
        if not seen[i]:
            L = 0
            j = i
            while not seen[j]:
                seen[j] = True
                j = p[j]
                L += 1
            ct.append(L)
    return tuple(sorted(ct))


# ------------------------------------------------- the atlas, pulled to root 1

class Atlas:
    """Three context-views over three roots, pulled back to root 1.

    Data as given: q1,q2,q3 (tuples over X), r12,r23,r31 (tuples over X).
    Derived:  qt2 = q2 o r12,  qt3 = q3 o r23 o r12,  rloop = r31 o r23 o r12.
    """

    def __init__(self, X, q1, q2, q3, r12, r23, r31):
        self.X, self.q1, self.q2, self.q3 = X, q1, q2, q3
        self.r12, self.r23, self.r31 = r12, r23, r31
        nX = len(X)
        self.r13 = tuple(r23[r12[i]] for i in range(nX))
        self.rloop = tuple(r31[self.r13[i]] for i in range(nX))
        self.qt2 = tuple(q2[r12[i]] for i in range(nX))
        self.qt3 = tuple(q3[self.r13[i]] for i in range(nX))
        self.qt1p = tuple(q1[self.rloop[i]] for i in range(nX))
        # carries: gamma_12 : F1 -> F2 with gamma o q1 = q2 o r12, etc.
        self.g12 = mediator(self.qt2, q1)
        self.g23 = mediator(self.qt3, self.qt2)
        self.g31 = mediator(self.qt1p, self.qt3)
        self.legs_ok = None not in (self.g12, self.g23, self.g31)
        self.gloop = None
        if self.legs_ok:
            self.gloop = compose_map(self.g31, compose_map(self.g23, self.g12))
        # loop-level carry, which may exist when a leg's does not
        self.gloop_direct = mediator(self.qt1p, q1)
        self.range1 = sorted(set(q1))

    # --- degree-0 (transport defects, nats) and degree-1 (curvature)
    def transport_defects(self):
        return (cond_entropy(self.qt2, self.q1),
                cond_entropy(self.qt3, self.qt2),
                cond_entropy(self.qt1p, self.qt3))

    def held_loop(self):
        """Held q1 rloop  <=>  zero curvature (D3)."""
        return self.qt1p == self.q1

    def curvature_support(self):
        """#readings moved by gamma_loop; requires the loop carry to exist."""
        g = self.gloop if self.legs_ok else self.gloop_direct
        if g is None:
            return None
        return sum(1 for f in self.range1 if g.get(f, f) != f)

    def gloop_is_perm(self):
        g = self.gloop if self.legs_ok else self.gloop_direct
        if g is None:
            return None
        img = [g[f] for f in self.range1 if f in g]
        return len(img) == len(self.range1) and len(set(img)) == len(self.range1)

    def glued(self):
        return tuple(zip(self.q1, self.qt2, self.qt3))


def closed(view, T):
    return factors(tuple(view[T[i]] for i in range(len(T))), view)


def closure_defect(view, T):
    return cond_entropy(tuple(view[T[i]] for i in range(len(T))), view)


def rate_map(view, T):
    return mediator(tuple(view[T[i]] for i in range(len(T))), view)



def perm_family(n):
    """X = M x S, |M|=2, |S|=n. q_i(m,s) = pi_i^m(s); F_i = S. Bijective views."""
    Xp = [(m, s) for m in (0, 1) for s in range(n)]
    ip = {x: i for i, x in enumerate(Xp)}
    return Xp, ip

def build_view(Xp, a, b):
    return tuple((a if m == 0 else b)[s] for (m, s) in Xp)

def build_reroot(Xp, ip, sigma, rho):
    return tuple(ip[(sigma[m], rho[s])] for (m, s) in Xp)

