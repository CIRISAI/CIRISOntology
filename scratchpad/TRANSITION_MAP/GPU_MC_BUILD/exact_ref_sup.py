#!/usr/bin/env python3
"""Exact dense-ish state-vector reference for the coherent REG+ lattice (supervisor build).

State = dict {tuple(sorted occupied global modes): complex amplitude}.
Protocol (frozen): collide; then L times (stream, collide); read after the final collision.
"""
from __future__ import annotations
import itertools
import numpy as np
import regmodel as R


def initial_config(L, spectator_modes):
    """Origin site (0,0) holds the head-on pair on channels 0 and 3; spectators elsewhere."""
    modes = [0 * 6 + 0, 0 * 6 + 3]
    for m in spectator_modes:
        if m // 6 == 0:
            raise ValueError("spectator placed on the origin site")
        modes.append(int(m))
    if len(set(modes)) != len(modes):
        raise ValueError("duplicate modes in initial configuration")
    return tuple(sorted(modes))


def _site_decomp(cfg, L):
    """cfg -> dict site -> local 6-bit state."""
    sites = {}
    for m in cfg:
        site, a = divmod(m, 6)
        sites[site] = sites.get(site, 0) | (1 << a)
    return sites


def collide(state, L, U, force_origin=None, cap=3_000_000):
    """One global collision. force_origin: if not None, the origin site's output is FORCED
    to R.PAIR_STATES[force_origin] with amplitude factor 1.0 (dephasing-branch preparation)."""
    out = {}
    for cfg, amp in state.items():
        sites = _site_decomp(cfg, L)
        # per-site output options: list of (site, [(local_state, factor), ...])
        options = []
        for site, s in sites.items():
            sid = int(R.SECTOR_OF_STATE[s])
            d = int(R.SECTOR_SIZE[sid])
            if site == 0 and force_origin is not None:
                options.append((site, [(R.PAIR_STATES[force_origin], 1.0 + 0j)]))
                continue
            if d == 1:
                continue                      # amplitude factor exactly 1, single output
            j = int(R.INDEX_IN_SECTOR[s])
            col = U[sid][:, j]
            options.append((site, [(R.SECTOR_STATES[sid][k], col[k]) for k in range(d)
                                   if col[k] != 0]))
        if not options:
            out[cfg] = out.get(cfg, 0j) + amp
            continue
        fixed = [m for m in cfg if (m // 6) not in {s for s, _ in options}]
        site_list = [s for s, _ in options]
        for combo in itertools.product(*[o for _, o in options]):
            f = amp
            modes = list(fixed)
            for site, (ls, fac) in zip(site_list, combo):
                f = f * fac
                for a in range(6):
                    if (ls >> a) & 1:
                        modes.append(site * 6 + a)
            key = tuple(sorted(modes))
            out[key] = out.get(key, 0j) + f
        if len(out) > cap:
            raise RuntimeError(f"basis support exceeded cap {cap}")
    return {k: v for k, v in out.items() if v != 0}


def stream(state, perm):
    return {tuple(sorted(int(perm[m]) for m in cfg)): amp for cfg, amp in state.items()}


def origin_pair_probs(state):
    """RAW q_j: probability that the origin site's local state is exactly PAIR_STATES[j]."""
    q = np.zeros(3)
    for cfg, amp in state.items():
        s = 0
        for m in cfg:
            if m < 6:
                s |= 1 << m
        for j, ps in enumerate(R.PAIR_STATES):
            if s == ps:
                q[j] += abs(amp) ** 2
    return q


def norm(state):
    return sum(abs(a) ** 2 for a in state.values())


def _evolve(state, L, U, perm, cap):
    mx = len(state)
    for _ in range(L):
        state = stream(state, perm)
        state = collide(state, L, U, cap=cap)
        mx = max(mx, len(state))
    return state, mx


def run_exact(L, spectator_modes, theta=R.THETA, phi=R.PHI_DEFAULT, cap=3_000_000):
    """Both arms and the witness M."""
    U = R.local_unitaries(theta, phi)
    perm = R.stream_permutation(L)
    cfg0 = initial_config(L, spectator_modes)
    psi0 = {cfg0: 1.0 + 0j}

    # --- coherent arm -------------------------------------------------------
    phi_state = collide(psi0, L, U, cap=cap)
    n1 = norm(phi_state)
    coh, mx_c = _evolve(phi_state, L, U, perm, cap)
    q_coh = origin_pair_probs(coh)
    sup_coh = q_coh.sum()
    p_coh = q_coh / sup_coh

    # --- dephased arm: project the ORIGIN site onto each head-on orientation -
    q_deph = np.zeros(3)
    sup_branch = np.zeros(3)
    bw = np.zeros(3)
    mx_d = 0
    for j in range(3):
        br = collide(psi0, L, U, force_origin=j, cap=cap)
        # branch weight = ||P_j phi||^2 ; P_j phi has the same non-origin factor,
        # so the weight is |a_j|^2 with a_j the origin column entry.
        s0 = 0
        for m in cfg0:
            if m < 6:
                s0 |= 1 << m
        sid0 = int(R.SECTOR_OF_STATE[s0])
        j0 = int(R.INDEX_IN_SECTOR[s0])
        k = R.SECTOR_STATES[sid0].index(R.PAIR_STATES[j])
        bw[j] = abs(U[sid0][k, j0]) ** 2
        st, m2 = _evolve(br, L, U, perm, cap)
        mx_d = max(mx_d, m2)
        qb = origin_pair_probs(st)
        sup_branch[j] = qb.sum() / norm(br)      # normalised branch
        q_deph += bw[j] * qb / norm(br)
    sup_deph = q_deph.sum()
    p_deph = q_deph / sup_deph

    M = 0.5 * np.abs(p_coh - p_deph).sum()
    return dict(M=float(M), p_coh=p_coh, p_deph=p_deph,
                support_coh=float(sup_coh), support_deph=float(sup_deph),
                branch_weights=bw, norm_after_first_collision=float(n1),
                norm_final=float(norm(coh)), max_support=max(mx_c, mx_d))


if __name__ == "__main__":
    print("Phi(deg)      M")
    for d in range(0, 360, 30):
        r = run_exact(11, [], phi=np.deg2rad(d))
        print(f"{d:>6d}  {r['M']:.6f}   norm={r['norm_final']:.15f}  support={r['support_coh']:.15f}")
