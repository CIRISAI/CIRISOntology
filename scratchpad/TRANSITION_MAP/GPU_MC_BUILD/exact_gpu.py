#!/usr/bin/env python3
"""Exact sparse state-vector propagation for the coherent REG+ lattice, array-based.

Same protocol as exact_ref_sup.py (collide; then L x (stream, collide); read after the final
collision) but the state is held as
    st  : (n, nsites) uint8   local 6-bit state per site
    amp : (n,)        complex128
so it runs on numpy or cupy and reaches supports far beyond a Python dict.

The global collision factorises over sites, so a configuration expands into the product over
sites of its per-site sector dimension. Expansion is done in chunks sized to a row budget,
each chunk is aggregated by exact complex summation on the packed configuration key, and the
chunks are aggregated together at the end.
"""
from __future__ import annotations
import numpy as np
import annihil_mc as A
import regmodel as R


def _xp():
    return A.xp()


def aggregate(st, amp, tab):
    """Exact complex summation over identical configurations."""
    rep_st, s_c, _ = A.annihilate(st, amp, tab)
    return rep_st, s_c


def expansion_factor(st, tab):
    """prod over sites of the site's sector dimension -- the row count each config expands to."""
    x = _xp()
    d = tab.KMAX[st.astype(x.int32)] + 1          # (n, nsites) int
    return x.prod(d.astype(x.float64), axis=1)


def _expand_chunk(st, amp, tab, force_origin):
    """Full per-site expansion of one chunk, no intermediate aggregation."""
    x = _xp()
    for site in range(tab.nsites):
        if site == 0 and force_origin is not None:
            st = st.copy()
            st[:, 0] = x.uint8(tab.pair_states[force_origin])
            continue
        s = st[:, site].astype(x.int32)
        d = tab.KMAX[s] + 1
        total = int(d.sum())
        cum = x.cumsum(d)
        offs = cum - d
        marks = x.zeros(total, dtype=x.int64)
        marks[offs] = 1
        idx = x.cumsum(marks) - 1
        k = x.arange(total) - offs[idx]
        s_exp = s[idx]
        st = st[idx]
        st[:, site] = tab.OUT[s_exp, k]
        amp = amp[idx] * tab.UCOL[s_exp, k]
    return st, amp


def collide(st, amp, tab, force_origin=None, row_budget=20_000_000, cap=None):
    """One exact global collision, chunked by expansion cost then aggregated."""
    x = _xp()
    fac = expansion_factor(st, tab)
    if force_origin is not None:
        d0 = float(tab.KMAX[int(st[0, 0])] + 1)   # origin is forced, not expanded
        fac = fac / d0
    n = st.shape[0]
    parts_st, parts_amp = [], []
    i = 0
    while i < n:
        j, acc = i, 0.0
        while j < n:
            f = float(fac[j])
            if j > i and acc + f > row_budget:
                break
            acc += f; j += 1
        cst, camp = _expand_chunk(st[i:j], amp[i:j], tab, force_origin)
        cst, camp = aggregate(cst, camp, tab)
        parts_st.append(cst); parts_amp.append(camp)
        i = j
    if len(parts_st) == 1:
        out_st, out_amp = parts_st[0], parts_amp[0]
    else:
        out_st, out_amp = aggregate(x.concatenate(parts_st, axis=0),
                                    x.concatenate(parts_amp), tab)
    if cap is not None and out_st.shape[0] > cap:
        raise RuntimeError(f"exact support {out_st.shape[0]:,d} exceeded cap {cap:,d}")
    return out_st, out_amp


def origin_pair_probs(st, amp, tab):
    """RAW q_j: probability the origin site's local state is exactly PAIR_STATES[j]."""
    x = _xp()
    p = x.abs(amp) ** 2
    o = st[:, 0]
    return np.array([float(p[o == ps].sum()) for ps in tab.pair_states])


def run_exact(L, spectator_modes, theta=R.THETA, phi=R.PHI_DEFAULT,
              cap=None, row_budget=20_000_000):
    """Both arms; returns raw q vectors so BOTH witness conventions can be formed."""
    x = _xp()
    tab = A.Tables(L, theta, phi)
    import mc_tables as T
    init = T.initial_site_states(L, spectator_modes)
    st = x.asarray(init[None, :].copy())
    amp = x.ones(1, dtype=x.complex128)

    max_support = 1
    st_c, amp_c = collide(st, amp, tab, cap=cap, row_budget=row_budget)
    max_support = max(max_support, st_c.shape[0])
    for _ in range(L):
        st_c = A.stream(st_c, tab)
        st_c, amp_c = collide(st_c, amp_c, tab, cap=cap, row_budget=row_budget)
        max_support = max(max_support, st_c.shape[0])
    q_coh = origin_pair_probs(st_c, amp_c, tab)
    norm_coh = float((x.abs(amp_c) ** 2).sum())

    bw = T.exact_branch_weights(L, spectator_modes, theta, phi)
    q_deph = np.zeros(3)
    for j in range(3):
        stb, ampb = collide(st, amp, tab, force_origin=j, cap=cap, row_budget=row_budget)
        nb = float((x.abs(ampb) ** 2).sum())
        for _ in range(L):
            stb = A.stream(stb, tab)
            stb, ampb = collide(stb, ampb, tab, cap=cap, row_budget=row_budget)
            max_support = max(max_support, stb.shape[0])
        q_deph += bw[j] * origin_pair_probs(stb, ampb, tab) / nb
    return dict(q_coh=q_coh, q_deph=q_deph, branch_weights=bw,
                norm_coh=norm_coh, max_support=int(max_support))


def witnesses(q_coh, q_deph):
    """BOTH declared conventions (E2 D2) from the same raw q vectors."""
    pc = q_coh / q_coh.sum(); pd = q_deph / q_deph.sum()
    return dict(M_norm=float(0.5 * np.abs(pc - pd).sum()),
                M_raw=float(0.5 * np.abs(q_coh - q_deph).sum()),
                p_coh=pc, p_deph=pd,
                support_coh=float(q_coh.sum()), support_deph=float(q_deph.sum()))
