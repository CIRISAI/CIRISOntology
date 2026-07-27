"""lfsr_design_check.py — CONSTRUCTION validation for the temporal (LFSR) arms.

Run BEFORE the addendum prereg is written. Establishes which trinomial recurrences are
maximal-length, where their weight-3 dual words sit (i.e. which lag pairs carry an exact
three-time parity), and that a population of replicas with states drawn uniformly over ALL
2^L states gives exactly pair-uniform, exactly-parity three-time marginals.

No dynamics, no noise, no maintenance quantity is computed here.
"""
import numpy as np
from itertools import combinations

LN2 = float(np.log(2))


def lfsr_period(a, b):
    """y_t = y_{t-a} XOR y_{t-b}.  Returns the period of the nonzero state orbit."""
    L = b
    state = 1  # nonzero seed, bits state[0..L-1] = y_{t-1}..y_{t-L}
    seen = state
    n = 0
    while True:
        nb = ((state >> (a - 1)) ^ (state >> (b - 1))) & 1
        state = ((state << 1) | nb) & ((1 << L) - 1)
        n += 1
        if state == seen:
            return n
        if n > (1 << L):
            return -1


def gen_sequences(a, b, T, states=None):
    """All 2^L output windows of length T, one per initial state (including all-zero)."""
    L = b
    if states is None:
        states = np.arange(1 << L, dtype=np.int64)
    n = len(states)
    out = np.zeros((n, T), dtype=np.int8)
    reg = np.zeros((n, L), dtype=np.int8)
    for i in range(L):
        reg[:, i] = (states >> i) & 1
    # reg[:, i] holds y_{-1-i}; emit forward
    hist = list(reg.T)                      # hist[i] = y_{t-1-i}
    for t in range(T):
        nb = hist[a - 1] ^ hist[b - 1]
        out[:, t] = nb
        hist = [nb] + hist[:-1]
    return out


def triple_dist(seq, i, j):
    """Empirical joint of (y_t, y_{t+i}, y_{t+j}) pooled over t and replicas."""
    n, T = seq.shape
    hi = max(i, j)
    A = seq[:, :T - hi].ravel()
    B = seq[:, i:T - hi + i].ravel()
    C = seq[:, j:T - hi + j].ravel()
    idx = (A.astype(np.int64) << 2) | (B.astype(np.int64) << 1) | C.astype(np.int64)
    c = np.bincount(idx, minlength=8).astype(float)
    return c / c.sum()


def H(p):
    p = np.asarray(p, float).ravel()
    p = p[p > 1e-300]
    return float(-np.sum(p * np.log(p)))


def share3(p):
    """k=3 whole-only share when the state is pair-uniform: 3 ln2 - H."""
    p3 = p.reshape(2, 2, 2)
    devs = [abs(p3.sum(axis=ax) - 0.25).max() for ax in (0, 1, 2)]
    return 3 * LN2 - H(p), max(devs)


def pair_mi(p):
    """Max pairwise mutual information over the three pairs."""
    p3 = p.reshape(2, 2, 2)
    out = 0.0
    for ax in (0, 1, 2):
        m = p3.sum(axis=ax)
        mi = 0.0
        for x in range(2):
            for y in range(2):
                if m[x, y] > 0:
                    mi += m[x, y] * np.log(m[x, y] / (m[x].sum() * m[:, y].sum()))
        out = max(out, mi)
    return out


if __name__ == "__main__":
    print("=" * 78)
    print("LFSR DESIGN CHECK — construction only")
    print("=" * 78)

    print("\n--- maximal-length trinomial recurrences y_t = y_{t-a} ^ y_{t-b} ---")
    good = []
    for b in range(5, 14):
        for a in range(1, b):
            per = lfsr_period(a, b)
            if per == (1 << b) - 1:
                good.append((a, b, per))
                print(f"  a={a:2d} b={b:2d}  period = {per} = 2^{b} - 1   MAXIMAL")
    print(f"  {len(good)} maximal trinomials found")

    A, B = 4, 9
    assert (A, B) in [(x, y) for x, y, _ in good], f"({A},{B}) not maximal"
    print(f"\n--- CHOSEN: a={A}, b={B}  (period {(1<<B)-1}) ---")

    T = 128
    seq = gen_sequences(A, B, T)
    print(f"  {seq.shape[0]} windows of length {T} (all 2^{B} states, incl. all-zero)")

    print("\n--- three-time readout at the TAP lags (a,b) ---")
    p = triple_dist(seq, A, B)
    s, dev = share3(p)
    print(f"  joint = {np.round(p, 6).tolist()}")
    print(f"  share = {s:.12f}   ln2 = {LN2:.12f}   pair dev = {dev:.2e}   "
          f"max pair MI = {pair_mi(p):.3e}")

    print("\n--- three-time readout at EQUALLY SPACED lags (D, 2D), D = 1..20 ---")
    print("  (this is the readout HABIT_DYNAMICS_RESULTS.md used)")
    for D in range(1, 21):
        p = triple_dist(seq, D, 2 * D)
        s, dev = share3(p)
        flag = "  <== SPIKE" if s > 1e-9 else ""
        print(f"   D={D:2d}: share = {s:.9f}  pairdev = {dev:.1e}  "
              f"maxpairMI = {pair_mi(p):.2e}{flag}")

    print("\n--- FULL COMB: all lag pairs (i,j), 1 <= i < j <= 24, with nonzero share ---")
    spikes = []
    for i in range(1, 25):
        for j in range(i + 1, 25):
            p = triple_dist(seq, i, j)
            s, dev = share3(p)
            if s > 1e-9:
                spikes.append((i, j, s, dev))
    for (i, j, s, dev) in spikes:
        print(f"   (i,j) = ({i:2d},{j:2d}): share = {s:.12f} = {s/LN2:.6f} * ln2"
              f"   pairdev = {dev:.1e}")
    print(f"  {len(spikes)} spikes among {24*23//2} lag pairs "
          f"({len(spikes)/(24*23//2):.1%} of the grid)")

    print("\n--- pairwise MI at every lag 1..40 (pooled over replicas) ---")
    n, TT = seq.shape
    mis = []
    for tau in range(1, 41):
        A_ = seq[:, :TT - tau].ravel()
        B_ = seq[:, tau:].ravel()
        c = np.bincount((A_.astype(np.int64) << 1) | B_.astype(np.int64),
                        minlength=4).astype(float)
        m = (c / c.sum()).reshape(2, 2)
        mi = sum(m[x, y] * np.log(m[x, y] / (m[x].sum() * m[:, y].sum()))
                 for x in range(2) for y in range(2) if m[x, y] > 0)
        mis.append(mi)
    print(f"  max over lags 1..40 of pairwise MI = {max(mis):.3e} nats")
    print(f"  (exact independence at every lag => tau_pair is ZERO at every lag)")
