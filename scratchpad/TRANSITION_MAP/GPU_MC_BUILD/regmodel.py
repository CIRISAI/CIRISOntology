#!/usr/bin/env python3
"""Frozen microscopic REG+ lattice constants, re-derived from the prereg text.

Six hard-core directional carries on an L x L periodic axial (triangular) torus.
Local state = 6-bit occupancy. Local conservation sectors keyed by (N, Px, Py).
theta = 1.30 rad frozen; phi is the Wilson-loop angle on the size-3 sectors.

Global mode index convention: mode = (y*L + x)*6 + a.
"""
from __future__ import annotations
import numpy as np

THETA = 1.30
PHI_DEFAULT = np.pi / 6.0          # 30 degrees
PAIR_STATES = (9, 18, 36)          # head-on orientations {0,3}, {1,4}, {2,5}

AXIAL_CARRIES = np.array([[1, 0], [0, 1], [-1, 1], [-1, 0], [0, -1], [1, -1]], dtype=int)

_STATES = np.arange(64, dtype=int)
BITS = ((_STATES[:, None] >> np.arange(6)) & 1).astype(np.int8)
N_PART = BITS.sum(axis=1)
P_AXIAL = BITS @ AXIAL_CARRIES


def build_sectors():
    """Group the 64 local states by (N,Px,Py); states ascending within a sector."""
    groups = {}
    for s in range(64):
        key = (int(N_PART[s]), int(P_AXIAL[s, 0]), int(P_AXIAL[s, 1]))
        groups.setdefault(key, []).append(s)
    sector_states = [tuple(v) for v in groups.values()]
    sector_of_state = np.empty(64, dtype=np.int32)
    index_in_sector = np.empty(64, dtype=np.int32)
    for sid, states in enumerate(sector_states):
        for j, s in enumerate(states):
            sector_of_state[s] = sid
            index_in_sector[s] = j
    return sector_states, sector_of_state, index_in_sector


SECTOR_STATES, SECTOR_OF_STATE, INDEX_IN_SECTOR = build_sectors()
SECTOR_SIZE = np.array([len(s) for s in SECTOR_STATES], dtype=np.int32)


def _unitary_from_hermitian(H, theta):
    vals, vecs = np.linalg.eigh(H)
    return (vecs * np.exp(-1j * theta * vals)) @ vecs.conj().T


def local_unitaries(theta=THETA, phi=PHI_DEFAULT):
    """U_by_sector[sid][k, j] = amplitude from sector-index j to sector-index k."""
    out = []
    for states in SECTOR_STATES:
        d = len(states)
        if d == 1:
            out.append(np.ones((1, 1), dtype=complex))
        elif d == 2:
            H = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
            out.append(_unitary_from_hermitian(H, theta))
        elif d == 3:
            H = np.zeros((3, 3), dtype=complex)
            H[0, 1] = H[1, 0] = 1.0
            H[1, 2] = H[2, 1] = 1.0
            H[2, 0] = np.exp(1j * phi)
            H[0, 2] = np.exp(-1j * phi)
            out.append(_unitary_from_hermitian(H, theta))
        else:
            raise AssertionError(f"unexpected sector dimension {d}")
    return out


def stream_permutation(L):
    """perm[m] = destination global mode of the occupant of global mode m."""
    nmode = 6 * L * L
    perm = np.empty(nmode, dtype=np.int64)
    for y in range(L):
        for x in range(L):
            site = y * L + x
            for a in range(6):
                dx, dy = AXIAL_CARRIES[a]
                site2 = ((y + dy) % L) * L + ((x + dx) % L)
                perm[site * 6 + a] = site2 * 6 + a
    return perm


def local_states_of_config(occ, L):
    """occ: (6*L*L,) uint8 occupancy -> (L*L,) local 6-bit states."""
    o = occ.reshape(L * L, 6).astype(np.int64)
    return (o * (1 << np.arange(6))).sum(axis=1)
