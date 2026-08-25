//! DIAGNOSTIC ONLY — not a gate, not staked Q10 evidence.
//!
//! `OBJECT.md`-native localization of q8-mps's N=8/U=16 failure.  The candidate MPS is the
//! World state; `dmrg::run_from` is Habit; the quantities below are Views; q-seam is the Door.
//! This probe asks whether the energy q8 reports from its last local eigensolve is the global
//! energy of the MPS it actually returns.  It also realizes the site-local four-state chart
//! `{empty, up, down, full}` as the adjacent JW-bit chart `(n_up, n_down)` and checks the
//! content-bearing views that must survive that correspondence.
//!
//! The global view is deliberately independent of q8's MPO/environment contraction: expand the
//! MPS into the 2^(2N) occupation basis, then apply the bare Hubbard Hamiltonian by explicit
//! fermionic creation/annihilation signs.  This is cheap only at the exact seam (N <= 10 here),
//! which is exactly where the claim-transport receipt is needed.
//!
//! Predeclared diagnostic bands:
//! - view correspondence: max absolute observable difference <= 1e-10;
//! - reported-local versus returned-state energy: absolute difference <= 1e-10;
//! - planted mutant (erase every JW sign): must move the energy by > 1e-6.
//!
//! A TNC adapter can consume the same tensor/operator network as a third View.  It is kept out
//! of this crate because q8-mps's zero-runtime-dependency warrant is load-bearing.
//!
//! Run:
//! `cargo run --release -p q8-mps --example object_claim_transport -- [sites] [U] [chi]`

use q8_mps::dmrg::{self, Params, RefusalPolicy, SweepResult};
use q8_mps::mps::{self, TensorSite};
use q8_mps::observables;
use std::time::Instant;

const VIEW_TOL: f64 = 1e-10;
const REPORTED_ENERGY_TOL: f64 = 1e-10;
const MUTANT_MIN_MOVE: f64 = 1e-6;

#[derive(Debug)]
struct DirectView {
    energy: f64,
    energy_variance: f64,
    norm_squared: f64,
    particle_number: f64,
    two_sz: f64,
    two_sz_squared: f64,
    density: Vec<f64>,
    magnetization: Vec<f64>,
    double_occupancy: Vec<f64>,
}

#[derive(Debug)]
struct Receipt {
    start: &'static str,
    reported_energy: f64,
    view: DirectView,
    mutant_energy: f64,
    observable_transport_defect: f64,
    reported_state_energy_defect: f64,
    exact_energy_defect: f64,
    sweeps: usize,
    converged: bool,
    worst_left_canonical_defect: f64,
    worst_right_canonical_defect: f64,
    worst_lanczos_residual: f64,
    wall_seconds: f64,
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let sites: usize = args.get(1).map(|s| s.parse().expect("sites must be usize")).unwrap_or(8);
    let u: f64 = args.get(2).map(|s| s.parse().expect("U must be f64")).unwrap_or(16.0);
    let chi: usize = args.get(3).map(|s| s.parse().expect("chi must be usize")).unwrap_or(32);
    assert!(sites > 0 && sites % 2 == 0, "the frozen family is half-filled Sz=0");
    assert!(sites <= 10, "the explicit 2^(2N) view is an exact-seam instrument only");

    let t = 1.0;
    let params = Params { sites, t, u, chi_max: chi, max_sweeps: 20, sweep_tol: 1e-10 };
    let exact_started = Instant::now();
    let exact_h = q_seam::hubbard::Hubbard::new(sites, t, u);
    let exact = q_seam::lanczos::ground_state(&exact_h).expect("q-seam Door refused");
    let exact_observables = q_seam::observables::ExactObservables::measure(&exact_h, &exact.vector);

    println!("=== OBJECT claim-transport probe ===");
    println!(
        "World: open Hubbard N={sites} t={t} U={u} N_e={sites} 2Sz=0; chi={chi}"
    );
    println!(
        "Door: q-seam E={:.15} residual={:.3e} iterations={} ({:.3}s)",
        exact.energy,
        exact.residual,
        exact.iterations,
        exact_started.elapsed().as_secs_f64()
    );
    println!(
        "Claim transport: site-local [empty,up,down,full] <-> adjacent JW bits [up,down]"
    );

    let mut receipts = Vec::new();
    for (name, initial) in [
        ("neel", mps::initial_state(sites)),
        ("doublon-hole", doublon_hole_state(sites)),
    ] {
        let started = Instant::now();
        match dmrg::run_from(&params, RefusalPolicy::Typed, initial) {
            Ok(result) => receipts.push(receipt(
                name,
                sites,
                t,
                u,
                &result,
                exact.energy,
                started.elapsed().as_secs_f64(),
            )),
            Err(refusal) => {
                println!(
                    "{name}: FLOOR REFUSAL at bond {} discarded_weight={:.6e}",
                    refusal.bond, refusal.weight
                );
            }
        }
    }

    for r in &receipts {
        println!("\n--- Habit start: {} ---", r.start);
        println!(
            "reported(last local) E={:.15}; returned-state global E={:.15}; |difference|={:.6e}",
            r.reported_energy, r.view.energy, r.reported_state_energy_defect
        );
        println!(
            "|E_state-E_exact|={:.6e}; variance={:.6e}; norm2={:.15}",
            r.exact_energy_defect, r.view.energy_variance, r.view.norm_squared
        );
        println!(
            "views: N={:.12} 2Sz={:.12} <(2Sz)^2>={:.6e}; transport defect={:.6e}",
            r.view.particle_number,
            r.view.two_sz,
            r.view.two_sz_squared,
            r.observable_transport_defect
        );
        println!(
            "mutant(no JW signs) E={:.15}; move={:.6e}",
            r.mutant_energy,
            (r.mutant_energy - r.view.energy).abs()
        );
        println!(
            "sweeps={} converged={} canonical(L/R)=({:.3e},{:.3e}) local-residual={:.3e} wall={:.3}s",
            r.sweeps,
            r.converged,
            r.worst_left_canonical_defect,
            r.worst_right_canonical_defect,
            r.worst_lanczos_residual,
            r.wall_seconds
        );
        println!(
            "transport={} reported-is-state={} mutant-caught={}",
            pass(r.observable_transport_defect, VIEW_TOL),
            pass(r.reported_state_energy_defect, REPORTED_ENERGY_TOL),
            if (r.mutant_energy - r.view.energy).abs() > MUTANT_MIN_MOVE {
                "PASS"
            } else {
                "FAIL"
            }
        );
    }

    if receipts.len() == 2 {
        let start_move = (receipts[0].view.energy - receipts[1].view.energy).abs();
        println!("\nposed contrast: |E_neel-E_doublon-hole|={start_move:.6e}");
    }

    if let Some(best) = receipts
        .iter()
        .min_by(|a, b| a.exact_energy_defect.total_cmp(&b.exact_energy_defect))
    {
        let density_door = max_abs_diff(&best.view.density, &exact_observables.density);
        let magnetization_door =
            max_abs_diff(&best.view.magnetization, &exact_observables.magnetization);
        let double_door =
            max_abs_diff(&best.view.double_occupancy, &exact_observables.double_occ);
        println!(
            "Door observables (best returned state): density={density_door:.6e} magnetization={magnetization_door:.6e} double_occ={double_door:.6e}"
        );
    }
}

fn pass(value: f64, tolerance: f64) -> &'static str {
    if value <= tolerance { "PASS" } else { "FAIL" }
}

fn doublon_hole_state(sites: usize) -> Vec<TensorSite> {
    (0..2 * sites)
        .map(|orbital| {
            let chain_site = orbital / 2;
            let occupied = chain_site % 2 == 0;
            let mut tensor = TensorSite::zeros(1, 1);
            tensor.set(usize::from(occupied), 0, 0, 1.0);
            tensor
        })
        .collect()
}

fn receipt(
    start: &'static str,
    sites: usize,
    t: f64,
    u: f64,
    result: &SweepResult,
    exact_energy: f64,
    wall_seconds: f64,
) -> Receipt {
    let amplitudes = expand_statevector(&result.tensors);
    let view = direct_view(&amplitudes, sites, t, u, true);
    let mutant = direct_view(&amplitudes, sites, t, u, false);
    let reported_energy = result.energy_shifted + (u / 2.0) * sites as f64;

    let internal_density = observables::occupation_profile(&result.tensors, sites);
    let internal_magnetization = observables::magnetization_profile(&result.tensors, sites);
    let internal_double = observables::double_occupancy_profile(&result.tensors, sites);
    let internal_number = observables::total_number(&result.tensors);
    let internal_two_sz = observables::total_sz(&result.tensors);
    let internal_two_sz_squared = observables::total_sz_squared(&result.tensors);
    let observable_transport_defect = [
        max_abs_diff(&view.density, &internal_density),
        max_abs_diff(&view.magnetization, &internal_magnetization),
        max_abs_diff(&view.double_occupancy, &internal_double),
        (view.particle_number - internal_number).abs(),
        (view.two_sz - internal_two_sz).abs(),
        (view.two_sz_squared - internal_two_sz_squared).abs(),
    ]
    .into_iter()
    .fold(0.0f64, f64::max);

    Receipt {
        start,
        reported_energy,
        mutant_energy: mutant.energy,
        observable_transport_defect,
        reported_state_energy_defect: (reported_energy - view.energy).abs(),
        exact_energy_defect: (view.energy - exact_energy).abs(),
        sweeps: result.sweeps_used,
        converged: result.converged,
        worst_left_canonical_defect: result.worst_left_canonical_defect,
        worst_right_canonical_defect: result.worst_right_canonical_defect,
        worst_lanczos_residual: result.worst_lanczos_residual,
        wall_seconds,
        view,
    }
}

/// Expand `[s][left][right]` tensors without calling any q8 contraction routine.  Bit `j` of
/// the resulting index is the occupation of q8 JW orbital `j`; adjacent pairs are therefore
/// exactly the site-local base-four digits `[empty, up, down, full] = [0, 1, 2, 3]`.
fn expand_statevector(tensors: &[TensorSite]) -> Vec<f64> {
    assert!(!tensors.is_empty());
    assert_eq!(tensors[0].chi_l, 1);
    let mut partial = vec![1.0f64];
    let mut prefixes = 1usize;
    let mut left_dim = 1usize;

    for (site, tensor) in tensors.iter().enumerate() {
        assert_eq!(tensor.chi_l, left_dim, "broken MPS bond before orbital {site}");
        let mut next = vec![0.0; prefixes * 2 * tensor.chi_r];
        for prefix in 0..prefixes {
            for left in 0..left_dim {
                let coefficient = partial[prefix * left_dim + left];
                if coefficient == 0.0 {
                    continue;
                }
                for occupied in 0..2 {
                    let next_prefix = prefix | (occupied << site);
                    let destination = next_prefix * tensor.chi_r;
                    for right in 0..tensor.chi_r {
                        next[destination + right] +=
                            coefficient * tensor.get(occupied, left, right);
                    }
                }
            }
        }
        partial = next;
        prefixes *= 2;
        left_dim = tensor.chi_r;
    }
    assert_eq!(left_dim, 1);
    partial
}

fn direct_view(psi: &[f64], sites: usize, t: f64, u: f64, fermionic_signs: bool) -> DirectView {
    let orbitals = 2 * sites;
    assert_eq!(psi.len(), 1usize << orbitals);
    let norm_squared = psi.iter().map(|x| x * x).sum::<f64>();
    assert!(norm_squared > 0.0);

    let hpsi = apply_hubbard(psi, sites, t, u, fermionic_signs);
    let energy = dot(psi, &hpsi) / norm_squared;
    let energy_variance = hpsi
        .iter()
        .zip(psi)
        .map(|(hv, v)| {
            let residual = hv - energy * v;
            residual * residual
        })
        .sum::<f64>()
        / norm_squared;

    let mut particle_number = 0.0;
    let mut two_sz = 0.0;
    let mut two_sz_squared = 0.0;
    let mut density = vec![0.0; sites];
    let mut magnetization = vec![0.0; sites];
    let mut double_occupancy = vec![0.0; sites];

    for (basis, amplitude) in psi.iter().copied().enumerate() {
        let weight = amplitude * amplitude / norm_squared;
        let mut state_number = 0i32;
        let mut state_two_sz = 0i32;
        for chain_site in 0..sites {
            let up = ((basis >> (2 * chain_site)) & 1) as i32;
            let down = ((basis >> (2 * chain_site + 1)) & 1) as i32;
            state_number += up + down;
            state_two_sz += up - down;
            density[chain_site] += weight * f64::from(up + down);
            magnetization[chain_site] += weight * f64::from(up - down);
            double_occupancy[chain_site] += weight * f64::from(up * down);
        }
        particle_number += weight * f64::from(state_number);
        two_sz += weight * f64::from(state_two_sz);
        two_sz_squared += weight * f64::from(state_two_sz * state_two_sz);
    }

    DirectView {
        energy,
        energy_variance,
        norm_squared,
        particle_number,
        two_sz,
        two_sz_squared,
        density,
        magnetization,
        double_occupancy,
    }
}

fn apply_hubbard(
    psi: &[f64],
    sites: usize,
    t: f64,
    u: f64,
    fermionic_signs: bool,
) -> Vec<f64> {
    let mut out = vec![0.0; psi.len()];
    for (basis, amplitude) in psi.iter().copied().enumerate() {
        if amplitude == 0.0 {
            continue;
        }
        let doubles = (0..sites)
            .filter(|&site| {
                basis & (1 << (2 * site)) != 0 && basis & (1 << (2 * site + 1)) != 0
            })
            .count();
        out[basis] += u * doubles as f64 * amplitude;

        for site in 0..sites - 1 {
            for spin in 0..2 {
                let left = 2 * site + spin;
                let right = 2 * (site + 1) + spin;
                for (destination, source) in [(left, right), (right, left)] {
                    if let Some((next, sign)) = hop(basis, destination, source, fermionic_signs) {
                        out[next] += -t * sign * amplitude;
                    }
                }
            }
        }
    }
    out
}

fn hop(
    basis: usize,
    destination: usize,
    source: usize,
    fermionic_signs: bool,
) -> Option<(usize, f64)> {
    if basis & (1 << source) == 0 || basis & (1 << destination) != 0 {
        return None;
    }
    let after_annihilation = basis ^ (1 << source);
    let next = after_annihilation | (1 << destination);
    if !fermionic_signs {
        return Some((next, 1.0));
    }
    let before_source = basis & ((1usize << source) - 1);
    let before_destination = after_annihilation & ((1usize << destination) - 1);
    let odd = (before_source.count_ones() + before_destination.count_ones()) % 2 == 1;
    Some((next, if odd { -1.0 } else { 1.0 }))
}

fn dot(left: &[f64], right: &[f64]) -> f64 {
    left.iter().zip(right).map(|(a, b)| a * b).sum()
}

fn max_abs_diff(left: &[f64], right: &[f64]) -> f64 {
    assert_eq!(left.len(), right.len());
    left.iter()
        .zip(right)
        .map(|(a, b)| (a - b).abs())
        .fold(0.0, f64::max)
}
