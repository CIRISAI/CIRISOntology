//! DIAGNOSTIC ONLY — not a gate. Reproduces one deterministic configuration (no RNG anywhere in
//! the engine, so this is bit-identical to the same config inside `full_grid_gates`) and prints
//! the extra instrumentation the main gate suite does not: canonical-form defects, the worst
//! Lanczos residual, the full per-site magnetization vector, and total Sz — the checks
//! team-lead/chief-of-staff-2 ordered on any config that failed G6 or showed a non-monotone
//! energy rise, run as ITS OWN instrument on just the failing configs, not a re-run of the grid.
//!
//! Usage: `cargo run --release --example diag_failing_config -- <sites> <U>`
//! e.g.:  `cargo run --release --example diag_failing_config -- 8 16`

use q8_mps::dmrg::{self, Params, RefusalPolicy};
use q8_mps::observables;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let sites: usize = args.get(1).map(|s| s.parse().unwrap()).unwrap_or(8);
    let u: f64 = args.get(2).map(|s| s.parse().unwrap()).unwrap_or(16.0);

    let p = Params { sites, t: 1.0, u, chi_max: 256, max_sweeps: 20, sweep_tol: 1e-10 };
    let r = dmrg::run(&p, RefusalPolicy::Typed).expect("refused unexpectedly");

    println!("=== N={sites} U={u} diagnostic ===");
    println!("converged={} sweeps_used={}", r.converged, r.sweeps_used);
    println!(
        "worst_left_canonical_defect={:e}  worst_right_canonical_defect={:e}  (band for a clean sweep: ~1e-12)",
        r.worst_left_canonical_defect, r.worst_right_canonical_defect
    );
    println!(
        "worst_lanczos_residual={:e}  (this is the local eigensolver's own ||Hv-Ev||/max(1,|E|), RESIDUAL_GATE=1e-10 is the early-exit heuristic, not a verified bound)",
        r.worst_lanczos_residual
    );

    let mag = observables::magnetization_profile(&r.tensors, sites);
    let total_sz = observables::total_sz(&r.tensors);
    let total_sz_sq = observables::total_sz_squared(&r.tensors);
    println!("m_i per chain site: {mag:?}");
    println!("total Sz = {total_sz:e}   total Sz^2 = {total_sz_sq:e}");

    // The discriminator: staggered (alternating sign) vs uniform.
    let staggered = mag.windows(2).all(|w| w[0] * w[1] <= 0.0) && mag.iter().any(|&m| m.abs() > 1e-6);
    println!(
        "sign pattern: {} (staggered-with-Sz~0 => Neel symmetry-broken basin; uniform or nonzero total Sz => sector leak, a different and more serious finding)",
        if staggered { "STAGGERED" } else { "not staggered (or all ~zero)" }
    );
}
