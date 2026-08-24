//! The two-site DMRG sweep — `Q8_MPS_PREREG.md` §2, §4 (G7: fixed schedule, no post-hoc
//! extension). Environments are rebuilt fresh from the current tensors at every bond rather than
//! updated incrementally: `O(L)` redundant work per bond instead of `O(1)`, `O(L^2)` per sweep
//! instead of `O(L)` — a deliberate correctness-over-speed trade the commission's "speed clause
//! scoped out of v1" licenses, and it removes an entire class of stale-environment bugs.

use crate::lanczos;
use crate::mpo;
use crate::mps::{self, Env, TensorSite};

pub struct Params {
    pub sites: usize,
    pub t: f64,
    pub u: f64,
    /// The bond ledger — every truncation in this run is capped here (§2's single uniform
    /// scalar; the physical near-boundary cap `min(chi, 2^b, 2^(L-b))` needs no separate code,
    /// it falls out of the SVD's own economy rank at each bond).
    pub chi_max: usize,
    pub max_sweeps: usize,
    pub sweep_tol: f64,
}

pub struct SweepResult {
    pub tensors: Vec<TensorSite>,
    /// `<H'>` — the WORKING (shifted) Hamiltonian's energy, from the last two-site solve of the
    /// last sweep. Unshift with the integer `N_target`, never a measured expectation, per
    /// `Q8_MPS_PREREG.md` §2's pinned convention — this module does not do that unshift itself,
    /// callers do, so the convention lives in exactly one place (the prereg's own wording).
    pub energy_shifted: f64,
    pub sweeps_used: usize,
    pub converged: bool,
    /// Per-bond discarded weight from the run's LAST full sweep only — earlier sweeps' values
    /// are corrected by later optimization and are not representative (`Q8_MPS_PREREG.md` §5).
    pub discarded_weight: Vec<f64>,
}

pub fn run(p: &Params) -> SweepResult {
    let l = 2 * p.sites;
    let mu = p.u / 2.0;
    let mut tensors = mps::initial_state(p.sites);
    let w: Vec<Vec<f64>> =
        (0..l).map(|j| mpo::w_dense(mps::is_up_orbital(j), p.t, p.u, mu)).collect();

    let mut prev_energy = f64::INFINITY;
    let mut last_energy = 0.0;
    let mut converged = false;
    let mut sweeps_used = 0;
    let mut discarded = vec![0.0; l - 1];

    for sweep in 0..p.max_sweeps {
        sweeps_used = sweep + 1;

        // Left-to-right: orthogonality center moves right, so S is absorbed into the RIGHT
        // tensor of each pair (`absorb_s_left = false`).
        for j in 0..(l - 1) {
            let (e, dw) = two_site_update(&mut tensors, &w, j, p.chi_max, false);
            last_energy = e;
            discarded[j] = dw;
        }
        // Right-to-left: mirror, S absorbed into the LEFT tensor.
        for j in (0..(l - 1)).rev() {
            let (e, dw) = two_site_update(&mut tensors, &w, j, p.chi_max, true);
            last_energy = e;
            discarded[j] = dw;
        }

        if (last_energy - prev_energy).abs() <= p.sweep_tol {
            converged = true;
            break;
        }
        prev_energy = last_energy;
    }

    SweepResult { tensors, energy_shifted: last_energy, sweeps_used, converged, discarded_weight: discarded }
}

fn two_site_update(
    tensors: &mut [TensorSite],
    w: &[Vec<f64>],
    j: usize,
    chi_max: usize,
    absorb_s_left: bool,
) -> (f64, f64) {
    let l = tensors.len();
    let left_env = build_left_env_upto(tensors, w, j);
    let right_env = build_right_env_from(tensors, w, j + 2, l);

    let chi_l = tensors[j].chi_l;
    let chi_r = tensors[j + 1].chi_r;
    let mid = tensors[j].chi_r;
    debug_assert_eq!(mid, tensors[j + 1].chi_l, "adjacent bond dimensions out of sync");

    // seed[l,a,b,r] = sum_m A_j[a,l,m] . A_{j+1}[b,m,r] — the current two-site tensor,
    // contracted through its shared bond, as the deterministic Lanczos warm start.
    let mut seed = vec![0.0; chi_l * 2 * 2 * chi_r];
    for lft in 0..chi_l {
        for a in 0..2 {
            for m in 0..mid {
                let av = tensors[j].get(a, lft, m);
                if av == 0.0 {
                    continue;
                }
                let base = (lft * 2 + a) * 2 * chi_r;
                for b in 0..2 {
                    for r in 0..chi_r {
                        seed[base + b * chi_r + r] += av * tensors[j + 1].get(b, m, r);
                    }
                }
            }
        }
    }

    let dim = chi_l * 2 * 2 * chi_r;
    let w1 = &w[j];
    let w2 = &w[j + 1];
    let gs = lanczos::ground_state(
        |psi| mps::apply_effective_h(&left_env, w1, w2, &right_env, psi, chi_l, chi_r),
        &seed,
        dim,
    )
    .expect("local Lanczos failed to converge");

    let (a_left, a_right, discarded) =
        mps::split_two_site(&gs.vector, chi_l, chi_r, chi_max, absorb_s_left);
    tensors[j] = a_left;
    tensors[j + 1] = a_right;

    (gs.energy, discarded)
}

fn build_left_env_upto(tensors: &[TensorSite], w: &[Vec<f64>], j: usize) -> Env {
    let mut env = mps::trivial_left_env();
    for k in 0..j {
        env = mps::grow_left(&env, &w[k], &tensors[k]);
    }
    env
}

fn build_right_env_from(tensors: &[TensorSite], w: &[Vec<f64>], j: usize, l: usize) -> Env {
    let mut env = mps::trivial_right_env();
    for k in (j..l).rev() {
        env = mps::grow_right(&env, &w[k], &tensors[k]);
    }
    env
}
