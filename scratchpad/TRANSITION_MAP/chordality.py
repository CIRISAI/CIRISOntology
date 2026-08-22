"""CHORD-1 runner. Frozen in CHORDALITY_PREREG.md before any ray was tested.
Implements: beta-sets (arXiv:2412.18018 Def.1-2), correlation hypergraph (Def.3),
its line graph, and chordality (Thm 11 + sufficiency of arXiv:2512.24490)."""
import itertools, sys
from pathlib import Path

N = 6                      # parties; subsystem 6 (0-indexed) is the purifier
ALL = list(range(N + 1))   # 7 subsystems

def subsets_lex(n):
    """non-empty subsets of {0..n-1} in the paper's lexicographic order"""
    out = []
    for size in range(1, n + 1):
        for c in itertools.combinations(range(n), size):
            out.append(frozenset(c))
    return out

LEX = subsets_lex(N)        # 63 entries

def make_S(vec):
    """entropy of any subset of the 7 subsystems, using purification."""
    base = {LEX[i]: vec[i] for i in range(len(LEX))}
    base[frozenset()] = 0
    def S(X):
        X = frozenset(X)
        if N in X:                      # contains purifier -> complement in 0..N-1
            X = frozenset(range(N)) - (X - {N})
        return base[X]
    return S

def positive_beta_sets(S):
    """X (|X|>=2, X subset of the 7) whose every bipartition MI is strictly positive"""
    heads = []
    for size in range(2, len(ALL) + 1):
        for X in itertools.combinations(ALL, size):
            Xs = set(X); ok = True
            for r in range(1, len(X)):
                for Y in itertools.combinations(X, r):
                    Z = Xs - set(Y)
                    if not Z: continue
                    if S(Y) + S(Z) - S(Xs) <= 0:
                        ok = False; break
                if not ok: break
            if ok: heads.append(frozenset(X))
    return heads

def line_graph(hyperedges):
    n = len(hyperedges)
    adj = {i: set() for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            if hyperedges[i] & hyperedges[j]:
                adj[i].add(j); adj[j].add(i)
    return adj

def is_chordal(adj):
    """maximum-cardinality search + perfect-elimination-ordering verification"""
    n = len(adj)
    if n == 0: return True
    weight = {v: 0 for v in adj}; order = []; visited = set()
    for _ in range(n):
        v = max((x for x in adj if x not in visited), key=lambda x: weight[x])
        order.append(v); visited.add(v)
        for u in adj[v]:
            if u not in visited: weight[u] += 1
    order.reverse()                      # perfect elimination ordering candidate
    pos = {v: i for i, v in enumerate(order)}
    for v in order:
        later = [u for u in adj[v] if pos[u] > pos[v]]
        if not later: continue
        w = min(later, key=lambda u: pos[u])
        for u in later:
            if u != w and u not in adj[w]:
                return False
    return True

def analyse(vec):
    S = make_S(vec)
    he = positive_beta_sets(S)
    return is_chordal(line_graph(he)), len(he)

if __name__ == '__main__':
    path = Path(sys.argv[1])
    rays = [[int(x) for x in l.split()] for l in path.read_text().splitlines() if l.strip()]
    print(f"loaded {len(rays)} rays, {len(rays[0])} components each")
    res = []
    for i, v in enumerate(rays, start=1):
        ch, nh = analyse(v); res.append((i, ch, nh))
    chordal = [i for i, c, _ in res if c]
    print(f"\nIMPLEMENTATION CONTROL: chordal rays = {len(chordal)} of {len(rays)}")
    print(f"  prereg expectation ~44 (paper reports 44 simple trees)")
    print(f"  control {'PASSES' if 35 <= len(chordal) <= 55 else 'FAILS — no verdict may be reported'}")
    for target in (111, 207):
        i, c, nh = res[target - 1]
        print(f"\nRAY #{target}: chordal = {c}   (|hyperedges| = {nh})")
    print(f"\nfirst 20 chordal ray indices: {chordal[:20]}")
