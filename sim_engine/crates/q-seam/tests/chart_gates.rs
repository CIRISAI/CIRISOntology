//! `Q_SEAM_PREREG.md` §3 — the chart's own gates, G-C1 to G-C3.

use q_seam::chart::Chart;
use q_seam::hubbard::{free_chain_energy_per_site, Hubbard};
use q_seam::lanczos::ground_state;

/// G-C1 — SCF convergence at `1e-12`, at every configuration of the pinned sweep.
#[test]
fn g_c1_scf_converges_everywhere() {
    for &n in &q_seam::SWEEP_SITES {
        for &u in &q_seam::SWEEP_U {
            let c = Chart::best(n, 1.0, u);
            assert!(c.is_some(), "N={n} U={u}: no guess converged; configuration would be VOID");
        }
    }
}

/// G-C2 — the chart's density matrix is idempotent: Booleanity CHECKED, not assumed.
///
/// This is `Core/ModeChart.lean`'s `meanOcc_boolean_of_pure` as an executable assertion: the
/// chart's mode occupations really are `{0,1}`, which is exactly why it cannot see its own
/// fractionality.
#[test]
fn g_c2_chart_density_matrix_is_idempotent() {
    for &n in &q_seam::SWEEP_SITES {
        for &u in &q_seam::SWEEP_U {
            let c = Chart::best(n, 1.0, u).unwrap();
            assert!(
                c.idempotency <= 1e-12,
                "N={n} U={u}: ||rho^2 - rho||_max = {:e}",
                c.idempotency
            );
        }
    }
}

/// G-C3 — the variational gate. Mean field is an upper bound, so `E_UHF >= E_exact` always.
/// A violation is a bug, and this is the cheapest place to catch one.
#[test]
fn g_c3_chart_is_variational() {
    for &n in &[2usize, 4, 6, 8] {
        for &u in &q_seam::SWEEP_U {
            let h = Hubbard::new(n, 1.0, u);
            let g = ground_state(&h).unwrap();
            let c = Chart::best(n, 1.0, u).unwrap();
            assert!(
                c.energy - g.energy >= -1e-10,
                "N={n} U={u}: E_UHF {} is BELOW E_exact {} by {:e}",
                c.energy,
                g.energy,
                g.energy - c.energy
            );
        }
    }
}

/// The chart is EXACT at `U = 0` — the premise of joint-gate clause (3), and the reason a
/// criterion that refuses `U = 0` is broken rather than conservative.
#[test]
fn the_chart_is_exact_at_u_zero() {
    for &n in &q_seam::SWEEP_SITES {
        let c = Chart::best(n, 1.0, 0.0).unwrap();
        let predicted = free_chain_energy_per_site(n);
        assert!(
            (c.energy_per_site() - predicted).abs() <= 1e-12,
            "N={n}: chart E/N = {} vs exact {predicted}",
            c.energy_per_site()
        );
        let (spin, ph, refl) = c.symmetry_breaking();
        assert!(spin <= 1e-12 && ph <= 1e-12 && refl <= 1e-12,
            "N={n}: chart breaks a symmetry at U=0 (spin {spin:e}, ph {ph:e}, refl {refl:e})");
    }
}
