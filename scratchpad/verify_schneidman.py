"""Verify: are Schneidman et al. (2003) Fig.1's four systems the same
measure-disagreement phenomenon we report on ECA rules 23/178/232 and 46?

Uses THIS repository's own instrument (the exact k=3 maxent solver in
eca_exact.share_exact) so the comparison is apples-to-apples.
"""
import sys, itertools, numpy as np
sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad')
import cupy as cp
import eca_spike as E

LN2 = np.log(2.0)


def share_exact(p3):
    """I_C^(3) in nats, via the repository's exact k=3 pairwise-maxent solver."""
    a = cp.asarray(np.asarray(p3, float).reshape(1, 2, 2, 2))
    share, q, err, it = E.shareK3_batch(a)
    assert float(cp.asnumpy(err).max()) < 1e-12, "maxent residual too large"
    return float(cp.asnumpy(share)[0])


def H(p):
    p = np.asarray(p, float).ravel()
    p = p[p > 0]
    return float(-(p * np.log(p)).sum())


def o_information(p3):
    """O-information for n=3 (Rosas et al. 2019), redundancy-positive.
    Omega = (n-2)H(X) + sum_j [H(X_j) - H(X_-j)]"""
    p3 = np.asarray(p3, float)
    Hall = H(p3)
    tot = (3 - 2) * Hall
    for j in range(3):
        axes = tuple(a for a in range(3) if a != j)
        Hj = H(p3.sum(axis=axes))            # marginal of variable j
        Hmj = H(p3.sum(axis=j))              # marginal of the other two
        tot += Hj - Hmj
    return tot


def co_information(p3):
    """Interaction information, redundancy-positive convention:
    I3 = sum_i S(x_i) - sum_{i<j} S(x_i,x_j) + S(x1,x2,x3)"""
    p3 = np.asarray(p3, float)
    s1 = sum(H(p3.sum(axis=tuple(a for a in range(3) if a != j))) for j in range(3))
    s2 = sum(H(p3.sum(axis=k)) for k in range(3))   # each pair marginal
    return s1 - s2 + H(p3)


def from_fn(fn):
    """sigma1,sigma2 uniform iid; sigma3 = fn(s1,s2)."""
    p = np.zeros((2, 2, 2))
    for a, b in itertools.product((0, 1), repeat=2):
        p[a, b, fn(a, b)] += 0.25
    return p


def fm():
    """Perfectly correlated ferromagnet: P(000)=P(111)=1/2.
    Schneidman's FM row (I = 2 bits, all pairwise MI = 1 bit)."""
    p = np.zeros((2, 2, 2))
    p[0, 0, 0] = 0.5
    p[1, 1, 1] = 0.5
    return p


def parity():
    p = np.zeros((2, 2, 2))
    for a, b in itertools.product((0, 1), repeat=2):
        p[a, b, a ^ b] = 0.25
    return p


cases = [
    ("AND", from_fn(lambda a, b: a & b)),
    ("OR",  from_fn(lambda a, b: a | b)),
    ("XOR", parity()),
    ("FM",  fm()),
]

print(f"{'system':6} {'I_C^(3) bits':>14} {'Omega bits':>12} {'co-info bits':>13}"
      f" {'Omega==co-info?':>16}")
for name, p in cases:
    ic3 = share_exact(p) / LN2
    om = o_information(p) / LN2
    ci = co_information(p) / LN2
    print(f"{name:6} {ic3:14.6f} {om:12.6f} {ci:13.6f} {str(abs(om-ci)<1e-12):>16}")

print()
print("Schneidman et al. 2003 Fig.1 published values (bits):")
print("  AND: I_C^(3)=0      I_C^(2)=0.8113  R(or I3) = -0.1887")
print("  OR : I_C^(3)=0      I_C^(2)=0.8113  R(or I3) = -0.1887")
print("  XOR: I_C^(3)=1      I_C^(2)=0       R(or I3) = -1")
print("  FM : I_C^(3)=0      I_C^(2)=2       R(or I3) = +1")

# The noise sweep of Fig.2: output noise on AND, i.e. flip sigma3 w.p. q.
print()
print("Fig.2 replication -- AND with output noise (flip sigma3 w.p. q):")
print(f"{'q':>8} {'I_C^(3) bits':>14} {'Omega bits':>12}")
base = from_fn(lambda a, b: a & b)
flip = np.zeros((2, 2, 2))
for q in [0.0, 1e-3, 1e-2, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5]:
    p = np.zeros((2, 2, 2))
    for a, b, c in itertools.product((0, 1), repeat=3):
        p[a, b, c] += base[a, b, c] * (1 - q)
        p[a, b, 1 - c] += base[a, b, c] * q
    print(f"{q:8.3f} {share_exact(p)/LN2:14.8f} {o_information(p)/LN2:12.6f}")
