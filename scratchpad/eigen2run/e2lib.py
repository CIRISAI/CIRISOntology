"""EIGEN2 shared library — corpus E2, the Euler-circuit balanced split (prereg S7.2),
nuisance matrices (S4), and the C1/C1P renderings (S3.1).

Governed by /home/emoore/CIRISOntology/scratchpad/EIGEN2_PREREG.md (FROZEN, S24).
Reuses v1 machinery from /home/emoore/CIRISOntology/scratchpad/eigen/ WITHOUT modifying it.

Class index order is ALPHABETICAL over the 11 internal names.  Pinned here because the
prereg's S7.2 seed-0 per-kind listing (20/19, 20/20, 20/20, 29/30, 30/29, 18/19, 20/20 x5)
is exactly the alphabetical order of the class counts (39, 40, 40, 59, 59, 37, 40x5).
"""
import hashlib, json, os, sys

import numpy as np

EIGEN = '/home/emoore/CIRISOntology/scratchpad/eigen'
RUN = '/home/emoore/CIRISOntology/scratchpad/eigen2run'
OUT = os.path.join(RUN, 'out')
CACHE = os.path.join(RUN, 'cache')
if EIGEN not in sys.path:
    sys.path.insert(0, EIGEN)

CORPUS = '/home/emoore/CIRISOntology/scratchpad/plane_corpus/eigen2/eigen2_corpus.jsonl'
CORPUS_SHA = 'cf26b604d8aeeebda906ad2c0729b1b71df5d37a55c25faf770447cf92be7c40'

KINDS = ['axiomatic', 'axiotic', 'contingent', 'deontic', 'empirical', 'epistemic',
         'nomological', 'ontological', 'pragmatic', 'procedural', 'structural']
KIDX = {k: i for i, k in enumerate(KINDS)}
NK = 11
RANK_B = 10                       # S5.1 counting identity at K = 11

PLAIN = {'axiotic': 'Priorities', 'deontic': 'Rules', 'pragmatic': 'Manner',
         'ontological': 'Identity', 'epistemic': 'Confidence', 'empirical': 'Facts',
         'contingent': 'Circumstances', 'procedural': 'Process', 'nomological': 'Model',
         'structural': 'Structure', 'axiomatic': 'Premises', 'testimonial': 'Record'}

# S7.1: domain-11 rival — the 12 authored domains with `report` merged into `bulletin`.
DOMAIN_MERGE = {'report': 'bulletin'}

BGE = 'BAAI/bge-large-en-v1.5'
QWEN = 'Qwen/Qwen3-Embedding-0.6B'
ARMS = ['qwen', 'bge', 'qwen_noinstr']         # primary, witness, ablation
ARM_MODEL = {'qwen': QWEN, 'bge': BGE, 'qwen_noinstr': QWEN}
CTX_LIMIT = {'qwen': 32768, 'bge': 512, 'qwen_noinstr': 32768}

NSPLIT = 200
NPERM = 500
SEED = 20260819


# ----------------------------------------------------------------- corpus
def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 20), b''):
            h.update(blk)
    return h.hexdigest()


def load_e2(verify=True):
    """Rows of E2 with mechanical span fields attached (S3.1's pinned construction)."""
    import phase0_span as ps
    if verify:
        got = sha256_file(CORPUS)
        if got != CORPUS_SHA:
            raise RuntimeError(f'corpus sha256 mismatch: {got}')
    rows = [json.loads(l) for l in open(CORPUS) if l.strip()]
    ps.attach(rows)                      # ctx_before / ctx_after / ctx_chars
    return rows


def labels_of(rows):
    return np.array([KIDX[r['kind_target']] for r in rows], dtype=np.int64)


def batches_of(rows):
    return np.array([int(r['batch']) for r in rows], dtype=np.int64)


def domain11_of(rows):
    """S7.1's pinned 11-way domain rival."""
    vals = [DOMAIN_MERGE.get(r['domain'], r['domain']) for r in rows]
    u = sorted(set(vals))
    assert len(u) == 11, f'domain-11 rival has {len(u)} classes'
    idx = {d: i for i, d in enumerate(u)}
    return np.array([idx[v] for v in vals], dtype=np.int64), u


# ------------------------------------------------ S7.2 Euler-circuit balanced split
def _euler_circuit(adj, start, n_edges):
    """Hierholzer, returning edge ids in TRUE CIRCUIT ORDER.

    Guard 2 of S7.2: colours must be assigned along the Eulerian circuit order, i.e.
    the REVERSED POP order, not the DFS push order.  We collect on pop and reverse.
    """
    ptr = {v: 0 for v in adj}
    used = bytearray(n_edges)
    stack = [start]
    estack = [-1]
    popped = []
    while stack:
        v = stack[-1]
        av = adj[v]
        i = ptr[v]
        while i < len(av) and used[av[i][1]]:
            i += 1
        ptr[v] = i
        if i == len(av):
            stack.pop()
            e = estack.pop()
            if e >= 0:
                popped.append(e)
        else:
            nb, eid = av[i]
            ptr[v] = i + 1
            used[eid] = 1
            stack.append(nb)
            estack.append(eid)
    popped.reverse()
    return popped


def euler_split(labels, batches, seed):
    """One balanced 2-colouring: returns a boolean mask (True = half 1).

    Bipartite multigraph, vertices = 11 kinds ('K',k) U 40 batches ('B',b), one edge
    per item.  Odd-degree vertices are joined to a dummy vertex.  An Eulerian circuit
    is 2-coloured alternately; the two colours are the two halves.  Randomisation is
    by shuffling the edge insertion order.

    Guard 1 of S7.2: the total edge count including dummy edges must be even, and the
    circuit length must be even; both are asserted and the function aborts otherwise.
    """
    rng = np.random.default_rng(seed)
    n = len(labels)
    order = rng.permutation(n)
    edges = []                                   # (u, v, is_real)
    for i in order:
        edges.append((('K', int(labels[i])), ('B', int(batches[i])), int(i)))
    deg = {}
    for u, v, _ in edges:
        deg[u] = deg.get(u, 0) + 1
        deg[v] = deg.get(v, 0) + 1
    odd = [v for v, d in deg.items() if d % 2 == 1]
    dummy = ('D', 0)
    for v in odd:
        edges.append((v, dummy, -1))
    m = len(edges)
    if m % 2 != 0:
        raise AssertionError(f'GUARD 1 FAILED: total edge count {m} is odd')
    adj = {}
    for eid, (u, v, _) in enumerate(edges):
        adj.setdefault(u, []).append((v, eid))
        adj.setdefault(v, []).append((u, eid))
    for v, lst in adj.items():
        if len(lst) % 2 != 0:
            raise AssertionError(f'GUARD 1 FAILED: vertex {v} has odd degree {len(lst)}')
    start = edges[0][0]
    circ = _euler_circuit(adj, start, m)
    if len(circ) != m:
        raise AssertionError(f'GUARD: circuit covers {len(circ)} of {m} edges '
                             '(graph is disconnected)')
    if len(circ) % 2 != 0:
        raise AssertionError(f'GUARD 1 FAILED: circuit length {len(circ)} is odd')
    mask = np.zeros(n, dtype=bool)
    for pos, eid in enumerate(circ):
        item = edges[eid][2]
        if item >= 0 and pos % 2 == 0:
            mask[item] = True
    return mask


def make_splits(labels, batches, nsplit=NSPLIT, seed=SEED):
    out = np.zeros((nsplit, len(labels)), dtype=bool)
    for t in range(nsplit):
        out[t] = euler_split(labels, batches, seed + 7919 * t)
    return out


def split_violations(mask, labels, batches):
    """Max |half1 - half2| imbalance over kinds and over batches, and the half sizes."""
    worst_k = 0
    for k in range(NK):
        m = labels == k
        worst_k = max(worst_k, abs(int(mask[m].sum()) - int((~mask[m]).sum())))
    worst_b = 0
    for b in np.unique(batches):
        m = batches == b
        worst_b = max(worst_b, abs(int(mask[m].sum()) - int((~mask[m]).sum())))
    return worst_k, worst_b, int(mask.sum()), int((~mask).sum())


# ----------------------------------------------------------------- nuisance (S4)
def dummies(vals):
    """Drop-first, K-1 dummy columns — pinned to run_phase0.py's `sorted(set(vals))[1:]`."""
    u = sorted(set(vals))[1:]
    return np.array([[1.0 if v == c else 0.0 for c in u] for v in vals])


def nuisance_Z(rows, kind='full'):
    """S4's Z.  'full' = [1, log10(1+span), domain(11), batch(39)] = 52 cols at full rank.
    'spandom' = [1, log10(1+span), domain(11)] = 13 cols.  'none' = [1]."""
    sp = np.log10(1.0 + np.array([r['ctx_chars'] for r in rows], dtype=float))
    one = np.ones(len(rows))
    if kind == 'none':
        return one[:, None]
    if kind == 'spandom':
        return np.column_stack([one, sp, dummies([r['domain'] for r in rows])])
    if kind == 'full':
        return np.column_stack([one, sp, dummies([r['domain'] for r in rows]),
                                dummies([int(r['batch']) for r in rows])])
    if kind == 'nodom':
        # AMENDMENTS.md A6: the frozen Z with ONLY the term that defines the domain-11
        # rival removed, so the rival conjunct is evaluable at all.  41 columns.
        return np.column_stack([one, sp, dummies([int(r['batch']) for r in rows])])
    if kind == 'nobatch':
        # A6: the frozen Z with only the batch dummies removed, for D-B2.  13 columns.
        return np.column_stack([one, sp, dummies([r['domain'] for r in rows])])
    raise ValueError(kind)


# ----------------------------------------------------------------- texts (S3.1)
def c1_texts(rows):
    import phase0_span as ps
    c1 = [ps.c1_text(r['ctx_before'], r['ctx_after']) for r in rows]
    c1p = [ps.c1_text(r['ctx_before'], r['ctx_before']) for r in rows]
    return c1, c1p


def arm_prefix(arm, t):
    import phase0_span as ps
    return ps.qwen(t) if arm == 'qwen' else t


# ----------------------------------------------------------------- misc
def atomic_json(obj, path):
    tmp = path + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(obj, f, indent=1, default=str)
    os.replace(tmp, path)


def done_marker(name, payload):
    atomic_json(payload, os.path.join(OUT, f'{name}.done.json'))
