#!/usr/bin/env python3
"""
Dalitz campaign — the whole-only share of (x, y, c): two binarised Dalitz
coordinates and the CP tag.

Pre-registered in scratchpad/DALITZ_PREREG.md (commit 53db89d), committed before
this file existed. Every threshold, cut, null, dye test and kill below is the one
written there.

Scratchpad only. No Lean, no Stance.lean, no audit.
"""
import json, sys, os, time
import numpy as np

NAT = 1.0
M_K = 493.677
M_PI = 139.57039
M_B = 5279.34
M_D0 = 1864.84

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dalitz", "data")

# ---------------------------------------------------------------------------
# 1. THE ESTIMATOR — exact 1-D k=3 solver (PREREG section 5). No IPF, anywhere.
# ---------------------------------------------------------------------------

SIGMA = np.array([[[1., -1.], [-1., 1.]], [[-1., 1.], [1., -1.]]])  # (-1)^(i+j+k)


def entropy(p):
    p = np.asarray(p, dtype=float).ravel()
    q = p[p > 0]
    return float(-np.sum(q * np.log(q)))


def share_2x2x2(p, tol=1e-15):
    """Whole-only share of a 2x2x2 table, exactly.

    The distributions carrying all three pair marginals of `p` are exactly the
    one-parameter family p + delta*SIGMA, since sum_k SIGMA[i,j,k] = 0 for every
    pair.  Entropy is strictly concave along it, so the pair-maxent is the unique
    root of dH/ddelta = -sum(SIGMA * log(p+delta*SIGMA)).  Bisection to machine
    precision; no iterative proportional fitting is used at any point.
    """
    p = np.asarray(p, dtype=float).reshape(2, 2, 2)
    s = p.sum()
    if s <= 0:
        return float("nan")
    p = p / s
    pos, neg = p[SIGMA > 0], p[SIGMA < 0]
    lo, hi = -pos.min(), neg.min()          # feasible delta interval
    if hi - lo < tol:
        return 0.0

    def g(d):
        q = p + d * SIGMA
        q = np.clip(q, 1e-300, None)
        return float(-np.sum(SIGMA * np.log(q)))

    a, b = lo + (hi - lo) * 1e-12, hi - (hi - lo) * 1e-12
    ga, gb = g(a), g(b)
    if ga < 0:        # maximiser at the lower edge
        return max(0.0, entropy(p + a * SIGMA) - entropy(p))
    if gb > 0:
        return max(0.0, entropy(p + b * SIGMA) - entropy(p))
    for _ in range(200):
        m = 0.5 * (a + b)
        if g(m) > 0:
            a = m
        else:
            b = m
    d = 0.5 * (a + b)
    return max(0.0, entropy(p + d * SIGMA) - entropy(p))


def share_range_given_pairs(p):
    """PREREG 6a: the interval the share can occupy over every distribution
    carrying `p`'s three pair marginals.  Exact, no solver, no surrogate.

    All members of the fibre share one pair-maxent, so its entropy H* is a
    constant of the fibre and share(q) = H* - H(q).  The reachable interval is
    therefore [0, H* - min_d H(p + d*SIGMA)].  (An earlier version of this
    function returned H(p+d*SIGMA) - H(p), which is NOT the share; the error and
    its correction are recorded in DALITZ_RESULTS.md.)
    """
    p = np.asarray(p, dtype=float).reshape(2, 2, 2)
    p = p / p.sum()
    lo, hi = -p[SIGMA > 0].min(), p[SIGMA < 0].min()
    Hs = np.array([entropy(p + d * SIGMA) for d in np.linspace(lo, hi, 4001)])
    Hstar = Hs.max()
    return 0.0, float(Hstar - Hs.min())


def table(x, y, c):
    """8-cell contingency table from three +-1 (stored 0/1) slot arrays."""
    idx = (x.astype(np.int64) * 4 + y.astype(np.int64) * 2 + c.astype(np.int64))
    return np.bincount(idx, minlength=8).astype(float).reshape(2, 2, 2)


# ---------------------------------------------------------------------------
# 2. PLUMB LINES (PREREG section 5).  A failure here is K7 and stops the run.
# ---------------------------------------------------------------------------

def plumb_lines():
    out, ok = {}, True
    ln2 = np.log(2.0)

    parity = np.zeros((2, 2, 2))
    for i in (0, 1):
        for j in (0, 1):
            parity[i, j, i ^ j] = 0.25
    out["parity"] = {"got": share_2x2x2(parity), "want": ln2}

    copied = np.zeros((2, 2, 2))
    for i in (0, 1):
        for k in (0, 1):
            copied[i, i, k] = 0.25
    out["copied"] = {"got": share_2x2x2(copied), "want": 0.0}

    ferro = np.zeros((2, 2, 2))
    ferro[0, 0, 0] = ferro[1, 1, 1] = 0.5
    out["ferro"] = {"got": share_2x2x2(ferro), "want": 0.0}

    rng = np.random.default_rng(20260726)
    worst = 0.0
    for _ in range(400):                      # sign-symmetric family: exactly 0
        q = rng.random(4)
        s = np.zeros((2, 2, 2))
        for n, (i, j, k) in enumerate([(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1)]):
            s[i, j, k] = s[1 - i, 1 - j, 1 - k] = q[n]
        worst = max(worst, share_2x2x2(s))
    out["sign_symmetric_max"] = {"got": worst, "want": 0.0}

    worst = 0.0
    for _ in range(400):                      # product tables P(x,y)*P(c): exactly 0
        pxy = rng.random((2, 2)); pxy /= pxy.sum()
        pc = rng.random(2); pc /= pc.sum()
        worst = max(worst, share_2x2x2(pxy[:, :, None] * pc[None, None, :]))
    out["product_max"] = {"got": worst, "want": 0.0}

    out["uniform"] = {"got": share_2x2x2(np.full((2, 2, 2), 0.125)), "want": 0.0}

    for k, v in out.items():
        v["pass"] = bool(abs(v["got"] - v["want"]) < 1e-9)
        ok &= v["pass"]
    return ok, out


# ---------------------------------------------------------------------------
# 3. DATA
# ---------------------------------------------------------------------------

def load(mode="KKK", chunk=500_000):
    """Load, apply the PREREG section 3 selection, return per-event quantities.

    Returns dict with m_parent, s_low, s_high (opposite-sign two-body invariant
    masses squared, ordered), charge, polarity.
    """
    import uproot
    masses = {"KKK": (M_K, M_K, M_K), "Kpipi": (M_K, M_PI, M_PI),
              "pipipi": (M_PI, M_PI, M_PI), "piKK": (M_PI, M_K, M_K)}
    br = ["H1_PX", "H1_PY", "H1_PZ", "H2_PX", "H2_PY", "H2_PZ",
          "H3_PX", "H3_PY", "H3_PZ", "H1_ProbK", "H2_ProbK", "H3_ProbK",
          "H1_ProbPi", "H2_ProbPi", "H3_ProbPi", "H1_Charge", "H2_Charge",
          "H3_Charge", "H1_isMuon", "H2_isMuon", "H3_isMuon"]
    acc = {k: [] for k in ("mB", "slow", "shigh", "q", "pol")}

    for pol, fn in (("Down", "B2HHH_MagnetDown.root"), ("Up", "B2HHH_MagnetUp.root")):
        f = uproot.open(os.path.join(DATA, fn))["DecayTree"]
        for a in f.iterate(br, step_size=chunk, library="np"):
            P = np.stack([np.stack([a[f"H{i}_PX"], a[f"H{i}_PY"], a[f"H{i}_PZ"]], -1)
                          for i in (1, 2, 3)], 1)          # (N,3,3)
            Q = np.stack([a[f"H{i}_Charge"] for i in (1, 2, 3)], -1)
            mu = np.stack([a[f"H{i}_isMuon"] for i in (1, 2, 3)], -1)
            pk = np.stack([a[f"H{i}_ProbK"] for i in (1, 2, 3)], -1)
            pp = np.stack([a[f"H{i}_ProbPi"] for i in (1, 2, 3)], -1)

            keep = (mu == 0).all(1) & (np.abs(Q.sum(1)) == 1)
            Bq = Q.sum(1)
            # order tracks: the two same-sign-as-B first, opposite-sign last
            same = (Q == Bq[:, None])
            keep &= (same.sum(1) == 2)
            if mode == "KKK":
                keep &= (pk > 0.5).all(1) & (pp < 0.5).all(1)
            elif mode == "pipipi":
                keep &= (pp > 0.5).all(1) & (pk < 0.5).all(1)
            if not keep.any():
                continue
            P, Q, pk, pp, Bq, same = P[keep], Q[keep], pk[keep], pp[keep], Bq[keep], same[keep]

            order = np.argsort(~same, axis=1, kind="stable")   # same-sign first
            P = np.take_along_axis(P, order[:, :, None], axis=1)
            if mode == "Kpipi":     # same-sign pair = (K+, pi+) ; opposite = pi-
                pkO = np.take_along_axis(pk, order, 1); ppO = np.take_along_axis(pp, order, 1)
                sel = (pkO[:, 0] > 0.5) & (ppO[:, 1] > 0.5) & (ppO[:, 2] > 0.5)
                P, Bq = P[sel], Bq[sel]
                mm = (M_K, M_PI, M_PI)
            elif mode == "piKK":    # same-sign pair = (pi+, K+) ; opposite = K-
                pkO = np.take_along_axis(pk, order, 1); ppO = np.take_along_axis(pp, order, 1)
                sel = (ppO[:, 0] > 0.5) & (pkO[:, 1] > 0.5) & (pkO[:, 2] > 0.5)
                P, Bq = P[sel], Bq[sel]
                mm = (M_PI, M_K, M_K)
            else:
                mm = masses[mode]
            if len(P) == 0:
                continue

            m = np.array(mm)
            E = np.sqrt(m[None, :] ** 2 + (P ** 2).sum(-1))
            Etot, Ptot = E.sum(1), P.sum(1)
            mB2 = Etot ** 2 - (Ptot ** 2).sum(-1)
            mB = np.sqrt(np.clip(mB2, 0, None))

            def inv2(i, j):
                Eij = E[:, i] + E[:, j]
                Pij = P[:, i] + P[:, j]
                return Eij ** 2 - (Pij ** 2).sum(-1)

            s02, s12 = inv2(0, 2), inv2(1, 2)   # the two opposite-sign combinations
            slow, shigh = np.minimum(s02, s12), np.maximum(s02, s12)

            acc["mB"].append(mB); acc["slow"].append(slow); acc["shigh"].append(shigh)
            acc["q"].append(Bq); acc["pol"].append(np.full(len(mB), 0 if pol == "Down" else 1))
    return {k: np.concatenate(v) for k, v in acc.items()}


def apply_windows(d, mode="KKK", win=30.0, sb=(5150., 5220., 5340., 5410.)):
    sig = np.abs(d["mB"] - M_B) < win
    side = ((d["mB"] > sb[0]) & (d["mB"] < sb[1])) | ((d["mB"] > sb[2]) & (d["mB"] < sb[3]))
    if mode in ("KKK", "piKK"):   # charm veto on the opposite-sign K+K- combinations
        lo, hi = (M_D0 - 30.) ** 2, (M_D0 + 30.) ** 2
        veto = ((d["slow"] > lo) & (d["slow"] < hi)) | ((d["shigh"] > lo) & (d["shigh"] < hi))
        sig &= ~veto; side &= ~veto
    return sig, side


# ---------------------------------------------------------------------------
# 4. NULLS AND DYE TESTS
# ---------------------------------------------------------------------------

def perm_null(x, y, c, n, rng):
    """PREREG 7a: permute the charge labels, preserving the observed counts."""
    out = np.empty(n)
    cc = c.copy()
    for i in range(n):
        rng.shuffle(cc)
        out[i] = share_2x2x2(table(x, y, cc))
    return out


def significance(obs, null):
    med = float(np.median(null))
    sd = float(np.std(null))
    p = float((np.sum(null >= obs) + 1) / (len(null) + 1))
    return {"share": float(obs), "null_median": med, "null_sd": sd,
            "excess": float(obs - med), "z": float((obs - med) / sd) if sd > 0 else None,
            "p": p, "n_perm": int(len(null))}
