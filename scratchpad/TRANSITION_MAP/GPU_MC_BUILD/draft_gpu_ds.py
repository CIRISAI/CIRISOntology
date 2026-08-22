```python
import numpy as np
import cupy as cp
from scipy.linalg import expm, eigh

# Backend selection
_xp = None

def set_backend(backend):
    global _xp
    if backend == 'cpu':
        _xp = np
    elif backend == 'gpu':
        _xp = cp
    else:
        raise ValueError("Backend must be 'cpu' or 'gpu'")

# Constants
AXIAL_CARRIES = [[1,0], [0,1], [-1,1], [-1,0], [0,-1], [1,-1]]
PAIR_STATES = [9, 18, 36]  # Head-on pair states
THETA = 1.30
PHI = np.pi / 6

def compute_sector_key(s):
    n = bin(s).count('1')
    px, py = 0, 0
    for a in range(6):
        if s & (1 << a):
            dx, dy = AXIAL_CARRIES[a]
            px += dx
            py += dy
    return (n, px, py)

def build_tables(theta=THETA, phi=PHI):
    sectors = {}
    for s in range(64):
        key = compute_sector_key(s)
        if key not in sectors:
            sectors[key] = []
        sectors[key].append(s)
    
    UCOL = _xp.zeros((64, 3), dtype=_xp.complex128)
    OUT = _xp.zeros((64, 3), dtype=_xp.uint8)
    QCOL = _xp.zeros((64, 3), dtype=_xp.float64)
    
    for key, states in sectors.items():
        d = len(states)
        if d == 1:
            H = _xp.array([[1.0]])
            U = _xp.array([[1.0]])
        elif d == 2:
            H = _xp.array([[0, 1], [1, 0]], dtype=_xp.complex128)
            vals, vecs = eigh(H)
            U = vecs @ _xp.diag(_xp.exp(-1j * theta * vals)) @ vecs.conj().T
        elif d == 3:
            H = _xp.array([[0, 1, _xp.exp(-1j*phi)],
                          [1, 0, 1],
                          [_xp.exp(1j*phi), 1, 0]], dtype=_xp.complex128)
            vals, vecs = eigh(H)
            U = vecs @ _xp.diag(_xp.exp(-1j * theta * vals)) @ vecs.conj().T
        else:
            continue
        
        for j, s_in in enumerate(states):
            for k in range(d):
                UCOL[s_in, k] = U[k, j]
                OUT[s_in, k] = states[k]
                QCOL[s_in, k] = _xp.abs(U[k, j])**2
    
    return UCOL, OUT, QCOL

def precompute_stream_maps(L):
    nsites = L * L
    dst_site = _xp.zeros((6, nsites), dtype=_xp.int32)
    for a in range(6):
        dx, dy = AXIAL_CARRIES[a]
        for src_idx in range(nsites):
            x, y = src_idx % L, src_idx // L
            nx, ny = (x + dx) % L, (y + dy) % L
            dst_site[a, src_idx] = ny * L + nx
    return dst_site

def collide(st, wt, UCOL, OUT, QCOL, rng):
    W, nsites = st.shape
    for site in range(nsites):
        s = st[:, site]
        q = QCOL[s]
        u = UCOL[s]
        cum = _xp.cumsum(q, axis=1)
        r = rng.random(W, dtype=_xp.float64)
        k = _xp.sum(r[:, _xp.newaxis] >= cum, axis=1)
        k = _xp.clip(k, 0, 2)
        st[:, site] = OUT[s, _xp.arange(W), k]
        wt *= u[_xp.arange(W), k] / q[_xp.arange(W), k]
    return st, wt

def stream(st, dst_site):
    W, nsites = st.shape
    new_st = _xp.zeros_like(st)
    for a in range(6):
        bit = (st >> a) & 1
        new_st[:, dst_site[a]] |= bit << a
    return new_st

def pack_keys(st):
    W, nsites = st.shape
    nwords = (nsites * 6 + 63) // 64
    keys = _xp.zeros((W, nwords), dtype=_xp.uint64)
    for i in range(nsites):
        word_idx = (i * 6) // 64
        shift = (i * 6) % 64
        keys[:, word_idx] |= st[:, i].astype(_xp.uint64) << shift
        if shift + 6 > 64:
            keys[:, word_idx+1] |= st[:, i].astype(_xp.uint64) >> (64 - shift)
    return keys

def annihilate_and_resample(st, wt, W, rng):
    keys = pack_keys(st)
    sorted_idxs = _xp.lexsort(keys.T[::-1])
    sorted_st = st[sorted_idxs]
    sorted_wt = wt[sorted_idxs]
    sorted_keys = keys[sorted_idxs]
    
    diff = _xp.any(sorted_keys[1:] != sorted_keys[:-1], axis=1)
    is_start = _xp.concatenate([_xp.array([True]), diff])
    segment_ids = _xp.cumsum(is_start) - 1
    n_unique = segment_ids[-1] + 1
    
    s_c_real = _xp.zeros(n_unique, dtype=_xp.float64)
    s_c_imag = _xp.zeros(n_unique, dtype=_xp.float64)
    _xp.add.at(s_c_real, segment_ids, sorted_wt.real)
    _xp.add.at(s_c_imag, segment_ids, sorted_wt.imag)
    s_c = s_c_real + 1j * s_c_imag
    
    absS = _xp.abs(s_c)
    total_S = _xp.sum(absS)
    if total_S == 0:
        return None, None, total_S, n_unique
    
    cum = _xp.cumsum(absS)
    r = rng.random(W, dtype=_xp.float64) * total_S
    idx = _xp.searchsorted(cum, r)
    
    rep_idxs = _xp.zeros(n_unique, dtype=_xp.int32)
    rep_idxs[segment_ids] = _xp.arange(len(segment_ids))
    st_new = sorted_st[rep_idxs[idx]]
    wt_new = (total_S / W) * (s_c[idx] / absS[idx])
    
    return st_new, wt_new, total_S, n_unique

def amplitude_map(st, wt, W):
    keys = pack_keys(st)
    sorted_idxs = _xp.lexsort(keys.T[::-1])
    sorted_st = st[sorted_idxs]
    sorted_wt = wt[sorted_idxs]
    sorted_keys = keys[sorted_idxs]
    
    diff = _xp.any(sorted_keys[1:] != sorted_keys[:-1], axis=1)
    is_start = _xp.concatenate([_xp.array([True]), diff])
    segment_ids = _xp.cumsum(is_start) - 1
    n_unique = segment_ids[-1] + 1
    
    s_c_real = _xp.zeros(n_unique, dtype=_xp.float64)
    s_c_imag = _xp.zeros(n_unique, dtype=_xp.float64)
    _xp.add.at(s_c_real, segment_ids, sorted_wt.real)
    _xp.add.at(s_c_imag, segment_ids, sorted_wt.imag)
    s_c = s_c_real + 1j * s_c_imag
    amps = s_c / W
    
    rep_idxs = _xp.zeros(n_unique, dtype=_xp.int32)
    rep_idxs[segment_ids] = _xp.arange(len(segment_ids))
    unique_keys = sorted_keys[rep_idxs[_xp.arange(n_unique)]]
    origin_state = sorted_st[rep_idxs[_xp.arange(n_unique)], 0]
    
    return unique_keys, amps, origin_state

def cross_probs(mapA, mapB):
    keysA, ampsA, originA = mapA
    keysB, ampsB, originB = mapB
    nwords = keysA.shape[1]
    all_keys = _xp.concatenate([keysA, keysB])
    sorted_idxs = _xp.lexsort(all_keys.T[::-1])
    sorted_keys = all_keys[sorted_idxs]
    diff = _xp.any(sorted_keys[1:] != sorted_keys[:-1], axis=1)
    is_start = _xp.concatenate([_xp.array([True]), diff])
    unique_keys = sorted_keys[is_start]
    
    idxA = _xp.searchsorted(unique_keys, keysA)
    idxB = _xp.searchsorted(unique_keys, keysB)
    
    probs = _xp.zeros(3, dtype=_xp.float64)
    for j, pair_state in enumerate(PAIR_STATES):
        maskA = (originA == pair_state)
        maskB = (originB == pair_state)
        common_idxs = _xp.intersect1d(idxA[maskA], idxB[maskB])
        if len(common_idxs) > 0:
            locA = _xp.isin(idxA, common_idxs) & maskA
            locB = _xp.isin(idxB, common_idxs) & maskB
            probs[j] += _xp.sum(_xp.real(ampsA[locA] * _xp.conj(ampsB[locB])))
    return probs

def run_replica(L, N, init_state, forced_origin_branch, W, seed, tables):
    UCOL, OUT, QCOL = tables
    nsites = L * L
    rng = _xp.random.RandomState(seed)
    st = _xp.full((W, nsites), init_state, dtype=_xp.uint8)
    wt = _xp.ones(W, dtype=_xp.complex128)
    
    if forced_origin_branch is not None:
        st[:, 0] = PAIR_STATES[forced_origin_branch]
    else:
        st, wt = collide(st, wt, UCOL, OUT, QCOL, rng)
    st, wt, S, n_unique = annihilate_and_resample(st, wt, W, rng)
    
    dst_site = precompute_stream_maps(L)
    for _ in range(L):
        st = stream(st, dst_site)
        st, wt = collide(st, wt, UCOL, OUT, QCOL, rng)
        st, wt, S, n_unique = annihilate_and_resample(st, wt, W, rng)
    
    return amplitude_map(st, wt, W)

def estimate_M(L, spectator_modes, W, n_batches, base_seed, theta, phi, exact_branch_weights):
    tables = build_tables(theta, phi)
    nsites = L * L
    init_state = _xp.zeros(nsites, dtype=_xp.uint8)
    init_state[0] = 9
    for mode in spectator_modes:
        site, channel = mode
        init_state[site] |= 1 << channel
    
    M_vals = _xp.zeros(n_batches, dtype=_xp.float64)
    out_of_bounds = _xp.zeros(n_batches, dtype=_xp.float64)
    
    for batch in range(n_batches):
        seed_coherent = base_seed + 2 * batch
        seed_dephased = base_seed + 2 * batch + 1
        
        map_coherent1 = run_replica(L, len(spectator_modes)+2, init_state, None, W, seed_coherent, tables)
        map_coherent2 = run_replica(L, len(spectator_modes)+2, init_state, None, W, seed_coherent+100000, tables)
        q_coh = cross_probs(map_coherent1, map_coherent2)
        support_coh = _xp.sum(q_coh)
        if support_coh > 0:
            p_coh = q_coh / support_coh
        else:
            p_coh = _xp.zeros(3)
        
        q_deph = _xp.zeros(3, dtype=_xp.float64)
        for j in range(3):
            map_deph1 = run_replica(L, len(spectator_modes)+2, init_state, j, W, seed_dephased, tables)
            map_deph2 = run_replica(L, len(spectator_modes)+2, init_state, j, W, seed_dephased+100000, tables)
            q_j = cross_probs(map_deph1, map_deph2)
            q_deph += exact_branch_weights[j] * q_j
        support_deph = _xp.sum(q_deph)
        if support_deph > 0:
            p_deph = q_deph / support_deph
        else:
            p_deph = _xp.zeros(3)
        
        M_batch = 0.5 * _xp.sum(_xp.abs(p_coh - p_deph))
        M_vals[batch] = M_batch
        out_of_bounds[batch] = _xp.any((p_coh < -0.05) | (p_coh > 1.05)) | _xp.any((p_deph < -0.05) | (p_deph > 1.05))
    
    mean_M = _xp.mean(M_vals)
    se_M = _xp.std(M_vals) / _xp.sqrt(n_batches)
    frac_out = _xp.mean(out_of_bounds)
    return mean_M, se_M, M_vals, frac_out
```