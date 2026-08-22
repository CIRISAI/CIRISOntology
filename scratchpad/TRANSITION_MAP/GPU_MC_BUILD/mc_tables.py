#!/usr/bin/env python3
"""Collision lookup tables for the annihilating MC.

Key fact used throughout: for a site in local state s, BOTH the conservation sector and the
position of s inside that sector are functions of s alone. So the whole local collision is a
(64,3) table lookup, and size-1 sectors need no special-casing.
"""
from __future__ import annotations
import numpy as np
import regmodel as R


def collision_tables(theta=R.THETA, phi=R.PHI_DEFAULT):
    """UCOL[s,k] = U_sector(s)[k, idx(s)]; OUT[s,k] = k-th state of s's sector; QCOL=|UCOL|^2.

    For k >= d(s): UCOL=0, QCOL=0, OUT=s (never selected, since QCOL is 0 there).
    QCOL[s,:].sum() == 1 exactly for every s (unitary columns).
    """
    U = R.local_unitaries(theta, phi)
    UCOL = np.zeros((64, 3), dtype=np.complex128)
    OUT = np.zeros((64, 3), dtype=np.uint8)
    for s in range(64):
        sid = int(R.SECTOR_OF_STATE[s])
        j = int(R.INDEX_IN_SECTOR[s])
        states = R.SECTOR_STATES[sid]
        d = len(states)
        OUT[s, :] = s
        for k in range(d):
            UCOL[s, k] = U[sid][k, j]
            OUT[s, k] = states[k]
    QCOL = np.abs(UCOL) ** 2
    return UCOL, OUT, QCOL


def kmax_table():
    """KMAX[s] = d(s)-1, the largest valid output index for a site in local state s.

    Needed because cumsum(QCOL[s]) can fall short of 1.0 by up to ~1e-15 (20 of the 64
    states do), so a uniform draw just below 1 would otherwise select k = d(s) -- an
    out-of-sector slot whose QCOL is exactly 0, giving an infinite weight.
    """
    return np.array([len(R.SECTOR_STATES[int(R.SECTOR_OF_STATE[s])]) - 1
                     for s in range(64)], dtype=np.int64)


def stream_dst(L):
    """dst[a][src_site] = destination site of an occupant of channel a at src_site."""
    ns = L * L
    dst = np.zeros((6, ns), dtype=np.int64)
    for a in range(6):
        dx, dy = R.AXIAL_CARRIES[a]
        for y in range(L):
            for x in range(L):
                dst[a, y * L + x] = ((y + dy) % L) * L + ((x + dx) % L)
    return dst


def initial_site_states(L, spectator_modes):
    """(L*L,) uint8 local states for the frozen initial configuration."""
    st = np.zeros(L * L, dtype=np.uint8)
    st[0] = 9                                    # head-on pair on channels 0 and 3
    for m in spectator_modes:
        site, a = divmod(int(m), 6)
        if site == 0:
            raise ValueError("spectator placed on the origin site")
        if (st[site] >> a) & 1:
            raise ValueError("duplicate spectator mode")
        st[site] |= np.uint8(1 << a)
    return st


def exact_branch_weights(L, spectator_modes, theta=R.THETA, phi=R.PHI_DEFAULT):
    """|a_j|^2 for the three origin head-on orientations after the first collision."""
    U = R.local_unitaries(theta, phi)
    s0 = 9
    sid = int(R.SECTOR_OF_STATE[s0]); j0 = int(R.INDEX_IN_SECTOR[s0])
    bw = np.zeros(3)
    for j, ps in enumerate(R.PAIR_STATES):
        k = R.SECTOR_STATES[sid].index(ps)
        bw[j] = abs(U[sid][k, j0]) ** 2
    return bw
