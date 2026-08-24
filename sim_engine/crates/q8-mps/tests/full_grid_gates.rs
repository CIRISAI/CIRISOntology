//! G2, G3-secondary, G6, G0-2, G7 — `Q8_MPS_PREREG.md` §4. The staked N=8,10,12 x U/t in
//! {0,1,4,16} grid at generous chi=256. `#[ignore]`d: this is a genuinely long-running
//! validation (minutes per configuration, N=12's exact reference is a fresh Lanczos solve at
//! dim 853776 per D3), run explicitly with `cargo test --release -- --ignored --nocapture`, not
//! on every default `cargo test`.
//!
//! One DMRG run per configuration backs every gate below — they are reported and asserted
//! together per configuration (one gate per invariant, per house rule, but sharing the run that
//! produces them all is not the same as conflating what they test).

mod common;

use common::U_GRID;
use q8_mps::dmrg::{self, Params};
use q8_mps::observables;

const CHI_MAX: usize = 256;
const MAX_SWEEPS: usize = 20;
const SWEEP_TOL: f64 = 1e-10;

const ENERGY_TOL_GAPPED: f64 = 1e-8; // relative, U/t in {1,4,16}
const ENERGY_TOL_GAPLESS: f64 = 1e-6; // relative, U=0
const DENSITY_TOL: f64 = 1e-6;
const DOCC_TOL: f64 = 1e-6;
const MI_TOL: f64 = 1e-6; // G6
const SECTOR_TOL: f64 = 1e-6; // G0-2: |<N_tot>-N|, |<Sz>|, <Sz^2>
const FLOOR_SLACK: f64 = 1e-9; // G3-secondary

#[test]
#[ignore]
fn full_grid_g2_g3_g6_g0_2_g7() {
    let mut failures: Vec<String> = Vec::new();

    for &sites in &[8usize, 10, 12] {
        for &u in &U_GRID {
            eprintln!("=== N={sites} U={u} — running DMRG (chi={CHI_MAX}) ===");
            let p =
                Params { sites, t: 1.0, u, chi_max: CHI_MAX, max_sweeps: MAX_SWEEPS, sweep_tol: SWEEP_TOL };
            let r = match dmrg::run(&p, dmrg::RefusalPolicy::Typed) {
                Ok(r) => r,
                Err(refusal) => {
                    failures.push(format!(
                        "N={sites} U={u}: engine REFUSED at chi={CHI_MAX} — bond={} weight={:e} \
                         (unexpected: chi=256 is meant to be generous, not forcing)",
                        refusal.bond, refusal.weight
                    ));
                    continue;
                }
            };

            let n_target = sites as f64;
            let mu = u / 2.0;
            let unshifted = r.energy_shifted + mu * n_target;

            eprintln!(
                "N={sites} U={u}: E={unshifted:.10} sweeps={} converged={} discarded_max={:e}",
                r.sweeps_used,
                r.converged,
                r.discarded_weight.iter().cloned().fold(0.0, f64::max)
            );

            // G7 — fixed schedule, no post-hoc extension. A non-convergence is recorded, not
            // silently retried with a bigger cap.
            if !r.converged {
                failures.push(format!("N={sites} U={u}: G7 FAILED — did not converge in {MAX_SWEEPS} sweeps"));
            }

            eprintln!("N={sites} U={u}: calling q-seam exact reference (dev-dependency, live)...");
            let h = q_seam::hubbard::Hubbard::new(sites, 1.0, u);
            let exact = match q_seam::lanczos::ground_state(&h) {
                Some(g) => g,
                None => {
                    failures.push(format!("N={sites} U={u}: q-seam Lanczos failed to converge — VOID"));
                    continue;
                }
            };
            let exact_obs = q_seam::observables::ExactObservables::measure(&h, &exact.vector);

            // G3-secondary: the variational floor, unshifted (valid once G0-2 below confirms
            // sector lock — reported together, not conflated).
            if unshifted < exact.energy - FLOOR_SLACK {
                failures.push(format!(
                    "N={sites} U={u}: G3-secondary FAILED — DMRG {unshifted} BELOW exact {} by {:e}",
                    exact.energy,
                    exact.energy - unshifted
                ));
            }

            // G2 — energy.
            let etol = if u == 0.0 { ENERGY_TOL_GAPLESS } else { ENERGY_TOL_GAPPED };
            let e_rel = (unshifted - exact.energy).abs() / exact.energy.abs().max(1.0);
            if e_rel > etol {
                failures.push(format!(
                    "N={sites} U={u}: G2 energy FAILED — rel err {e_rel:e} > {etol:e} (mps={unshifted}, exact={})",
                    exact.energy
                ));
            }

            // G2 — density profile (n_i = up+down per chain site).
            let mps_occ = observables::occupation_profile(&r.tensors, sites);
            let exact_occ = &exact_obs.density;
            let occ_err = mps_occ
                .iter()
                .zip(exact_occ.iter())
                .map(|(a, b)| (a - b).abs())
                .fold(0.0, f64::max);
            if occ_err > DENSITY_TOL {
                failures.push(format!("N={sites} U={u}: G2 density FAILED — max|Δn_i|={occ_err:e} > {DENSITY_TOL:e}"));
            }

            // G2 — double occupancy.
            let mps_docc = observables::double_occupancy_profile(&r.tensors, sites);
            let exact_docc = &exact_obs.double_occ;
            let docc_err = mps_docc
                .iter()
                .zip(exact_docc.iter())
                .map(|(a, b)| (a - b).abs())
                .fold(0.0, f64::max);
            if docc_err > DOCC_TOL {
                failures.push(format!("N={sites} U={u}: G2 double-occ FAILED — max|Δd_i|={docc_err:e} > {DOCC_TOL:e}"));
            }

            // G6 — m_i theorem anchor (=0 exactly; Q7 §2.2 spin-independence + Sz-sector
            // uniqueness, not Lieb). Needs no exact reference.
            let mps_mag = observables::magnetization_profile(&r.tensors, sites);
            let mag_err = mps_mag.iter().cloned().map(f64::abs).fold(0.0, f64::max);
            if mag_err > MI_TOL {
                failures.push(format!("N={sites} U={u}: G6 m_i FAILED — max|m_i|={mag_err:e} > {MI_TOL:e}"));
            }

            // G0-2 — standing sector-lock anchor. Needs no exact reference either.
            let n_tot = observables::total_number(&r.tensors);
            let sz = observables::total_sz(&r.tensors);
            let sz_sq = observables::total_sz_squared(&r.tensors);
            if (n_tot - n_target).abs() > SECTOR_TOL {
                failures.push(format!("N={sites} U={u}: G0-2 N_tot FAILED — |{n_tot}-{n_target}| > {SECTOR_TOL:e}"));
            }
            if sz.abs() > SECTOR_TOL {
                failures.push(format!("N={sites} U={u}: G0-2 Sz FAILED — |Sz|={} > {SECTOR_TOL:e}", sz.abs()));
            }
            if sz_sq.abs() > SECTOR_TOL {
                failures.push(format!("N={sites} U={u}: G0-2 Sz^2 FAILED — Sz^2={sz_sq} > {SECTOR_TOL:e}"));
            }

            // Particle-hole anchor (theorem-pinned <n_i>=1/2), free alongside G0-2.
            let ph_err = mps_occ.iter().map(|n| (n - 0.5).abs()).fold(0.0, f64::max);
            if ph_err > DENSITY_TOL {
                failures.push(format!("N={sites} U={u}: particle-hole anchor FAILED — max|n_i-0.5|={ph_err:e}"));
            }
        }
    }

    if !failures.is_empty() {
        panic!("{} gate failure(s):\n{}", failures.len(), failures.join("\n"));
    }
}
