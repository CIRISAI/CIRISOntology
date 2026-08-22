import numpy as np
from collections import defaultdict

AXIAL_CARRIES = np.array([[1, 0], [0, 1], [-1, 1], [-1, 0], [0, -1], [1, -1]], dtype=int)
PAIR_STATES = [9, 18, 36]  # Head-on pair states: {0,3}, {1,4}, {2,5}

def build_sectors():
    """Build sector information for all 64 local states."""
    sector_of_state = np.zeros(64, dtype=int)
    sector_states = defaultdict(list)
    sector_index_of_state = np.zeros(64, dtype=int)
    
    for s in range(64):
        occ = [a for a in range(6) if (s >> a) & 1]
        N = len(occ)
        P = np.zeros(2, dtype=int)
        for a in occ:
            P += AXIAL_CARRIES[a]
        key = (N, int(P[0]), int(P[1]))
        sector_states[key].append(s)
    
    # Sort states within each sector and assign sector IDs
    sorted_keys = sorted(sector_states.keys())
    by_sid = {}
    for sid, key in enumerate(sorted_keys):
        states = sorted(sector_states[key])
        by_sid[sid] = states
        for idx, s in enumerate(states):
            sector_of_state[s] = sid
            sector_index_of_state[s] = idx

    return sector_of_state, by_sid, sector_index_of_state

def local_unitaries(theta, phi):
    """Compute unitary matrices for each sector."""
    sector_of_state, sector_states, _ = build_sectors()
    U_by_sector = {}
    
    for sid, states in sector_states.items():
        d = len(states)
        if d == 1:
            U = np.array([[1.0+0j]], dtype=np.complex128)
        elif d == 2:
            H = np.array([[0, 1], [1, 0]], dtype=np.complex128)
            w, v = np.linalg.eigh(H)
            U = v @ np.diag(np.exp(-1j * theta * w)) @ v.conj().T
        elif d == 3:
            H = np.zeros((3,3), dtype=np.complex128)
            H[0,1] = H[1,0] = 1
            H[1,2] = H[2,1] = 1
            H[0,2] = np.exp(-1j * phi)
            H[2,0] = np.exp(1j * phi)
            w, v = np.linalg.eigh(H)
            U = v @ np.diag(np.exp(-1j * theta * w)) @ v.conj().T
        else:
            raise ValueError(f"Sector size {d} not supported")
        U_by_sector[sid] = U
    return U_by_sector

def collide_state(state_dict, L, U_by_sector, sector_of_state, sector_states, sector_index_of_state, cap=3000000):
    """Apply global collision to the state vector."""
    new_state = defaultdict(complex)
    n_sites = L * L
    for config, amp in state_dict.items():
        # Decompose into per-site local states
        site_states = [0] * n_sites
        for mode in config:
            site_idx = mode // 6
            channel = mode % 6
            site_states[site_idx] |= (1 << channel)
        
        # Precompute output contributions per site
        site_outputs = []
        for s in site_states:
            sid = sector_of_state[s]
            idx_in_sector = sector_index_of_state[s]
            U = U_by_sector[sid]
            d = U.shape[0]
            outputs = []
            for k in range(d):
                new_s = sector_states[sid][k]
                outputs.append((new_s, U[k, idx_in_sector]))
            site_outputs.append(outputs)
        
        # Enumerate the product over sites
        new_configs = [([], 1.0+0j)]
        for site_idx, outputs in enumerate(site_outputs):
            new_configs_next = []
            for base_config, base_amp in new_configs:
                for new_s, u_amp in outputs:
                    new_config = base_config + [new_s]
                    new_amp = base_amp * u_amp
                    new_configs_next.append((new_config, new_amp))
            new_configs = new_configs_next
            if len(new_configs) > cap:
                raise RuntimeError(f"Exceeded cap {cap} during collision")
        
        # Convert site states back to global mode indices
        for site_config, site_amp in new_configs:
            occupied_modes = []
            for site_idx, s_val in enumerate(site_config):
                for a in range(6):
                    if (s_val >> a) & 1:
                        global_mode = site_idx * 6 + a
                        occupied_modes.append(global_mode)
            key = tuple(sorted(occupied_modes))
            new_state[key] += amp * site_amp
    
    return dict(new_state)

def stream_state(state_dict, L):
    """Apply global streaming to the state vector."""
    new_state = defaultdict(complex)
    n_sites = L * L
    for config, amp in state_dict.items():
        new_config = []
        for mode in config:
            site_idx = mode // 6
            channel = mode % 6
            x0 = site_idx % L
            y0 = site_idx // L
            dx, dy = AXIAL_CARRIES[channel]
            x1 = (x0 + dx) % L
            y1 = (y0 + dy) % L
            new_site_idx = y1 * L + x1
            new_mode = new_site_idx * 6 + channel
            new_config.append(new_mode)
        key = tuple(sorted(new_config))
        new_state[key] += amp
    return dict(new_state)

def origin_pair_probs(state_dict, L):
    """Compute raw probabilities for origin site being in each head-on pair state."""
    origin_site_idx = 0  # (0,0) is site index 0
    q = np.zeros(3, dtype=np.float64)
    for config, amp in state_dict.items():
        origin_state = 0
        for mode in config:
            site_idx = mode // 6
            if site_idx == origin_site_idx:
                channel = mode % 6
                origin_state |= (1 << channel)
        if origin_state in PAIR_STATES:
            idx = PAIR_STATES.index(origin_state)
            q[idx] += np.abs(amp)**2
    return q

def run_exact(L, N, spectator_modes, theta, phi, cap=3000000):
    """Run exact simulation for both coherent and dephased arms."""
    # Build sector information and unitaries
    sector_of_state, sector_states, sector_index_of_state = build_sectors()
    U_by_sector = local_unitaries(theta, phi)
    
    # Initial state: pair at origin (state 9) plus spectators
    origin_site = 0
    initial_modes = [origin_site * 6 + a for a in [0, 3]]  # state 9
    initial_modes.extend(spectator_modes)
    initial_state = {tuple(sorted(initial_modes)): 1.0+0j}
    
    # Coherent arm
    state_coh = initial_state
    norm_err_coh = 0.0
    max_support = 0
    
    # First collision
    state_coh = collide_state(state_coh, L, U_by_sector, sector_of_state, sector_states, sector_index_of_state, cap)
    max_support = max(max_support, len(state_coh))
    norm = sum(np.abs(amp)**2 for amp in state_coh.values())
    norm_err_coh = max(norm_err_coh, abs(1 - norm))
    
    # Dephased arm: project after first collision
    branch_weights = np.zeros(3, dtype=np.float64)
    branch_states = [dict() for _ in range(3)]
    for config, amp in state_coh.items():
        origin_state = 0
        for mode in config:
            site_idx = mode // 6
            if site_idx == origin_site:
                channel = mode % 6
                origin_state |= (1 << channel)
        if origin_state in PAIR_STATES:
            idx = PAIR_STATES.index(origin_state)
            branch_weights[idx] += np.abs(amp)**2
            branch_states[idx][config] = amp
        else:
            # AMBIGUITY: states not in head-on pair are discarded in dephasing
            pass
    
    assert abs(branch_weights.sum() - 1.0) < 1e-12, (
        'dephasing projection lost probability: origin left the head-on sector')

    # Normalize branch states
    for i in range(3):
        norm = np.sqrt(branch_weights[i])
        if norm > 0:
            for config in branch_states[i]:
                branch_states[i][config] /= norm
    
    # Evolve both arms: L streams and collisions
    for step in range(L):
        # Stream
        state_coh = stream_state(state_coh, L)
        max_support = max(max_support, len(state_coh))
        for i in range(3):
            branch_states[i] = stream_state(branch_states[i], L)
            max_support = max(max_support, len(branch_states[i]))
        
        # Collide
        state_coh = collide_state(state_coh, L, U_by_sector, sector_of_state, sector_states, sector_index_of_state, cap)
        max_support = max(max_support, len(state_coh))
        norm = sum(np.abs(amp)**2 for amp in state_coh.values())
        norm_err_coh = max(norm_err_coh, abs(1 - norm))
        for i in range(3):
            branch_states[i] = collide_state(branch_states[i], L, U_by_sector, sector_of_state, sector_states, sector_index_of_state, cap)
            max_support = max(max_support, len(branch_states[i]))
    
    # Read results
    q_coh = origin_pair_probs(state_coh, L)
    support_coh = np.sum(q_coh)
    p_coh = q_coh / support_coh if support_coh > 0 else np.zeros(3)
    
    q_deph = np.zeros(3, dtype=np.float64)
    for i in range(3):
        q_branch = origin_pair_probs(branch_states[i], L)
        q_deph += branch_weights[i] * q_branch
    support_deph = np.sum(q_deph)
    p_deph = q_deph / support_deph if support_deph > 0 else np.zeros(3)
    
    M = 0.5 * np.sum(np.abs(p_coh - p_deph))
    
    return {
        'M': M,
        'p_coh': p_coh,
        'p_deph': p_deph,
        'support_coh': support_coh,
        'support_deph': support_deph,
        'norm_err_coh': norm_err_coh,
        'max_support': max_support,
        'branch_weights': branch_weights
    }

def run_exact_n2_bridge(L, theta, phi):
    """Special case for N=2 with no spectators."""
    return run_exact(L, 2, [], theta, phi)

if __name__ == "__main__":
    L = 11
    theta = 1.30
    print("Phi(deg)\tM")
    for phi_deg in range(0, 331, 30):
        phi_rad = np.deg2rad(phi_deg)
        result = run_exact_n2_bridge(L, theta, phi_rad)
        print(f"{phi_deg}\t{result['M']:.6f}")
