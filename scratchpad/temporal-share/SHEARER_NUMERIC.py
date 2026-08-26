"""
Numerical verification for Core/Shearer.lean, run BEFORE the Lean was attempted.

Question every running campaign depends on: for THREE BINARY SLOTS, with NO
hypothesis on the pair marginals, is the whole-only share bounded by log 2?
The repository proved ATTAINMENT (share_parity = log 2) and a cap that
HYPOTHESISES a uniform pair marginal. The denominator the campaigns divide by
was therefore argued, not proved.

EXACT k=3 SOLVER (no IPF -- see memory note `ipf-sharek-boundary-drift`):
in the sign basis a three-bit state is

    p(x) = (1/8) * ( 1 + sum_i a_i s_i + sum_{i<j} b_ij s_i s_j + c s_1 s_2 s_3 )

with s_i = +-1. The six numbers a_i, b_ij are EXACTLY the pair-marginal data,
and c -- the triple correlator -- is the ONE free direction. So the pair
envelope is a one-parameter family, entropy is strictly concave along it, and
the max-entropy competitor is found by golden section on a scalar. Exact up to
the search tolerance; no iterative proportional fitting, no boundary drift.

Checks, on 1e6 random states drawn across four regimes:
  C1  share <= log 2                                    (THE TARGET)
  C2  share <= H(m12) + H(m3) - H(p)                    (the route's sharp form)
  C3  H(m12) + H(m3) - H(p) <= log 2                    (the route's closing step)
  C4  2*H(p) <= H(m12) + H(m13) + H(m23)                (Shearer at k=3, briefed route)
  C5  share <= (1/2)*sum H(m_ij) - H(p)                 (Shearer + envelope)
"""

import numpy as np

LOG2 = np.log(2.0)
TOL = 1e-9

# the eight cells, in the order (x1, x2, x3) with bit b -> sign 1 - 2b
BITS = np.array([[(i >> k) & 1 for k in (2, 1, 0)] for i in range(8)])
S = 1.0 - 2.0 * BITS                      # (8,3) signs
SIG = S[:, 0] * S[:, 1] * S[:, 2]         # (8,) triple sign
POS = SIG > 0
NEG = SIG < 0


def entropy(p):
    """Row-wise entropy of a (N,m) array of states."""
    p = np.asarray(p, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        t = np.where(p > 0, p * np.log(np.where(p > 0, p, 1.0)), 0.0)
    return -t.sum(axis=-1)


def pair_marg(P, i, j):
    """(N,4) marginals on slots i, j."""
    idx = BITS[:, i] * 2 + BITS[:, j]
    out = np.zeros((P.shape[0], 4))
    for cell in range(8):
        out[:, idx[cell]] += P[:, cell]
    return out


def single_marg(P, i):
    out = np.zeros((P.shape[0], 2))
    for cell in range(8):
        out[:, BITS[cell, i]] += P[:, cell]
    return out


def envelope_family(P):
    """p_c = (A + c*SIG)/8 carries P's pair marginals for every feasible c."""
    c0 = P @ SIG                                        # (N,) triple correlator
    A = 8.0 * P - c0[:, None] * SIG[None, :]            # (N,8)
    lo = np.max(-A[:, POS], axis=1)
    hi = np.min(A[:, NEG], axis=1)
    return A, c0, lo, hi


def _H_at(A, c):
    return entropy((A + c[:, None] * SIG[None, :]) / 8.0)


def max_entropy_in_envelope(P, iters=90):
    """Max entropy over the pair envelope, batched golden section."""
    A, c0, lo, hi = envelope_family(P)
    assert np.all(lo <= c0 + 1e-9) and np.all(c0 <= hi + 1e-9)
    gr = (np.sqrt(5.0) - 1.0) / 2.0
    a, b = lo.copy(), hi.copy()
    x1 = b - gr * (b - a)
    x2 = a + gr * (b - a)
    f1, f2 = _H_at(A, x1), _H_at(A, x2)
    for _ in range(iters):
        left = f1 < f2
        # branch where the maximum is to the right of x1
        a = np.where(left, x1, a)
        b = np.where(left, b, x2)
        nx1 = np.where(left, x2, b - gr * (b - a))
        nx2 = np.where(left, a + gr * (b - a), x1)
        nf1 = np.where(left, f2, np.nan)
        nf2 = np.where(left, np.nan, f1)
        need1 = ~left
        need2 = left
        if need1.any():
            nf1 = np.where(need1, _H_at(A, nx1), nf1)
        if need2.any():
            nf2 = np.where(need2, _H_at(A, nx2), nf2)
        x1, x2, f1, f2 = nx1, nx2, nf1, nf2
        if np.max(b - a) < 1e-14:
            break
    cands = np.stack([f1, f2, _H_at(A, lo), _H_at(A, hi), _H_at(A, c0),
                      _H_at(A, 0.5 * (a + b))], axis=1)
    return cands.max(axis=1)


def draw(regime, rng, n):
    if regime == "flat":
        return rng.dirichlet(np.ones(8), size=n)
    if regime == "sparse":
        return rng.dirichlet(np.full(8, 0.05), size=n)
    if regime == "spiky":
        return rng.dirichlet(np.full(8, 0.005), size=n)
    if regime == "support":
        # uniform on a random subset -- the deterministic corners, where the
        # extremal states (parity among them) live
        P = np.zeros((n, 8))
        k = rng.integers(1, 9, size=n)
        for r in range(n):
            idx = rng.choice(8, size=k[r], replace=False)
            P[r, idx] = 1.0 / k[r]
        return P
    raise ValueError(regime)


def main():
    rng = np.random.default_rng(20260727)
    regimes = ["flat", "sparse", "spiky", "support"]
    n_per, chunk = 250_000, 25_000

    keys = ("C1", "C2", "C3", "C4", "C5")
    worst = {k: -np.inf for k in keys}
    fails = {k: 0 for k in keys}
    best_share, best_p = -np.inf, None

    for regime in regimes:
        done = 0
        while done < n_per:
            n = min(chunk, n_per - done)
            done += n
            P = draw(regime, rng, n)
            Hp = entropy(P)
            Hmax = max_entropy_in_envelope(P)
            share = Hmax - Hp

            H12 = entropy(pair_marg(P, 0, 1))
            H13 = entropy(pair_marg(P, 0, 2))
            H23 = entropy(pair_marg(P, 1, 2))
            H3 = entropy(single_marg(P, 2))

            gap = H12 + H3 - Hp
            shear = 0.5 * (H12 + H13 + H23)

            v = {
                "C1": share - LOG2,
                "C2": share - gap,
                "C3": gap - LOG2,
                "C4": Hp - shear,
                "C5": share - (shear - Hp),
            }
            for k in keys:
                worst[k] = max(worst[k], float(v[k].max()))
                fails[k] += int((v[k] > TOL).sum())
            j = int(np.argmax(share))
            if share[j] > best_share:
                best_share, best_p = float(share[j]), P[j].copy()

    print(f"log 2 = {LOG2:.12f}")
    print(f"states tested: {len(regimes) * n_per}")
    print()
    labels = {
        "C1": "share <= log 2                        [THE TARGET]",
        "C2": "share <= H(m12)+H(m3)-H(p)            [route, sharp form]",
        "C3": "H(m12)+H(m3)-H(p) <= log 2            [route, closing step]",
        "C4": "2H(p) <= H(m12)+H(m13)+H(m23)         [Shearer at k=3]",
        "C5": "share <= (1/2)sum H(m_ij) - H(p)      [Shearer + envelope]",
    }
    for k in keys:
        status = "HOLDS" if fails[k] == 0 else f"VIOLATED x{fails[k]}"
        print(f"  {k}  {labels[k]}")
        print(f"      worst excess = {worst[k]:+.3e}   {status}")
    print()
    print(f"largest share seen: {best_share:.12f}   (log 2 = {LOG2:.12f}, "
          f"deficit {LOG2 - best_share:.3e})")
    print(f"  at p = {np.round(best_p, 6)}")

    # the two exhibited states, as a ruler
    parity = np.array([0.25 if BITS[i].sum() % 2 == 0 else 0.0 for i in range(8)])
    print()
    sh_par = float((max_entropy_in_envelope(parity[None]) - entropy(parity[None]))[0])
    unif = np.full(8, 0.125)
    sh_uni = float((max_entropy_in_envelope(unif[None]) - entropy(unif[None]))[0])
    print(f"parity  state: share = {sh_par:.12f}   (log 2 - share = {LOG2 - sh_par:+.3e})")
    print(f"uniform state: share = {sh_uni:.12f}")


if __name__ == "__main__":
    main()
