"""aut_counts_exact.py — EXACT automorphism group orders for every roster substrate.

Why this exists: `maintenance_sweep.py`'s `find_automorphisms()` is a BOUNDED RANDOM SEARCH
(cap `limit=60`, 20000 random tries, plus the guaranteed translations for linear codes). Its
output is a lower bound that saturates at the cap; it is NOT a group order. A sibling memo
(`RENT_COMPARISON.md`, commit f89e235) reads those numbers as automorphism counts and
concludes "the automorphism hypothesis INVERTS ... H11 has ONE automorphism". This script
computes the true orders so that claim can be checked rather than inherited.

An automorphism of a support S subset of {0,1}^k is a pair (sigma, c) with sigma a
permutation of the k coordinates and c in {0,1}^k such that { s.sigma XOR c : s in S } = S.
Counted exactly by backtracking over output positions with row-multiset pruning.
"""
import sys, os, json
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import maintenance_sweep as MS


def aut_order(S):
    """Exact number of (sigma, c) pairs preserving the row set of S (n x k, 0/1)."""
    S = np.asarray(S, dtype=np.int8)
    n, k = S.shape
    target = sorted(map(tuple, S.tolist()))

    # prefix signature of the ORIGINAL rows on the first m output positions
    def orig_sig(m):
        return sorted(tuple(r) for r in S[:, :m].tolist())

    sigs = [orig_sig(m) for m in range(k + 1)]
    count = 0
    used = [False] * k
    built = np.zeros((n, k), dtype=np.int8)

    def rec(pos):
        nonlocal count
        if pos == k:
            if sorted(map(tuple, built.tolist())) == target:
                count += 1
            return
        for j in range(k):
            if used[j]:
                continue
            for cb in (0, 1):
                built[:, pos] = S[:, j] ^ cb
                # prune: the multiset of row prefixes must already match the original's
                if sorted(tuple(r) for r in built[:, :pos + 1].tolist()) != sigs[pos + 1]:
                    continue
                used[j] = True
                rec(pos + 1)
                used[j] = False
    rec(0)
    return count


if __name__ == "__main__":
    specs = MS.build_structures()
    print("=" * 78)
    print("EXACT automorphism orders |{(sigma,c) : sigma(S) XOR c = S}|")
    print("=" * 78)
    print(f"{'id':5s}{'k':>3s}{'|S|':>5s}{'kind':>10s}{'random-search count':>22s}"
          f"{'EXACT order':>14s}")
    out = {}
    searched = {'L5': 60, 'L7': 60, 'E8': 60, 'H8': 10, 'H9': 5, 'H10': 2, 'H11': 1,
                'L11': 16, 'L12': 16, 'R12': 30}
    for tag in MS.ROSTER:
        s = MS.Substrate(tag, specs[tag])
        a = aut_order(s.S)
        out[tag] = dict(k=s.k, ns=s.ns, kind=s.kind, exact=a, searched=searched[tag])
        print(f"{tag:5s}{s.k:3d}{s.ns:5d}{s.kind:>10s}{searched[tag]:22d}{a:14d}")

    print("\n--- what the sibling memo's k-matched pairs actually look like ---")
    for a, b in [('H8', 'E8'), ('H11', 'L11'), ('L12', 'R12')]:
        pa, pb = out[a], out[b]
        print(f"  k={pa['k']:2d}: {a} exact {pa['exact']:6d} (searched {pa['searched']:2d})"
              f"   vs {b} exact {pb['exact']:6d} (searched {pb['searched']:2d})"
              f"   -> {a if pa['exact']>pb['exact'] else b} has MORE automorphisms")
    json.dump(out, open('/home/emoore/CIRISOntology/scratchpad/aut_counts_exact.json', 'w'),
              indent=1)
    print("\nwrote aut_counts_exact.json")
