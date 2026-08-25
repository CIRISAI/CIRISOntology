//! A finite witness for OBJECT.md's Habit/View compatibility, not a proof of `Closed`.
//!
//! `World` here is an admissibly canonical MPS chart, `T` is one complete DMRG sweep, and
//! `v` forgets the chart by expanding it to the physical state vector.  If `v` is closed under
//! `T`, two charts in one fiber of `v` must remain in one fiber after the sweep.  An orthogonal
//! bond rechart gives a nontrivial pair in that fiber while preserving the canonical-basis
//! witness the ordinary local eigenproblem requires.
//!
//! This test measures one such pair.  It does not establish closure for every MPS gauge, and a
//! non-orthogonal rechart is deliberately outside its domain: although it can preserve the
//! physical state, it destroys the canonical metric and turns the local solve into a generalized
//! eigenproblem.  `canonical_sweep.rs` gates that separate admissibility condition.

use q8_mps::dmrg::{self, Params, RefusalPolicy};
use q8_mps::mps::TensorSite;

#[test]
fn orthogonal_rechart_has_the_same_one_sweep_successor_view() {
    let prepare = Params {
        sites: 4,
        t: 1.0,
        u: 16.0,
        chi_max: 16,
        max_sweeps: 2,
        sweep_tol: 0.0,
    };
    let prepared = dmrg::run(&prepare, RefusalPolicy::Typed).expect("unexpected ledger refusal");

    let mut recharted = prepared.tensors.clone();
    let bond = recharted.len() / 2 - 1;
    assert!(
        recharted[bond].chi_r >= 2,
        "test needs a nontrivial internal bond"
    );
    orthogonal_rechart(&mut recharted, bond, 0.37);
    let chart_move = tensor_max_defect(&prepared.tensors, &recharted);
    assert!(
        chart_move >= 1e-3,
        "the planted rechart was numerically trivial: move={chart_move:e}"
    );

    let before = normalized_view(&prepared.tensors);
    let before_recharted = normalized_view(&recharted);
    let before_defect = phase_aligned_max_defect(&before, &before_recharted);
    assert!(
        before_defect <= 2e-13,
        "the planted chart change did not stay in one physical-state fiber"
    );

    let advance = Params {
        max_sweeps: 1,
        ..prepare
    };
    let direct = dmrg::run_from(&advance, RefusalPolicy::Typed, prepared.tensors)
        .expect("direct chart refused");
    let through_rechart = dmrg::run_from(&advance, RefusalPolicy::Typed, recharted)
        .expect("orthogonally recharted state refused");

    let after = normalized_view(&direct.tensors);
    let after_recharted = normalized_view(&through_rechart.tensors);
    let defect = phase_aligned_max_defect(&after, &after_recharted);
    eprintln!(
        "Habit conveyance witness: bond_chi={} chart_move={chart_move:e} \
         input_view_defect={before_defect:e} \
         successor_view_defect={defect:e}",
        direct.tensors[bond].chi_r
    );
    assert!(
        defect <= 1e-9,
        "one-sweep physical successor depends on an admissible MPS chart: defect={defect:e}"
    );
}

fn tensor_max_defect(left: &[TensorSite], right: &[TensorSite]) -> f64 {
    assert_eq!(left.len(), right.len());
    left.iter()
        .zip(right)
        .flat_map(|(a, b)| {
            assert_eq!((a.chi_l, a.chi_r), (b.chi_l, b.chi_r));
            a.data.iter().zip(&b.data).map(|(x, y)| (x - y).abs())
        })
        .fold(0.0, f64::max)
}

/// Apply `A -> A G`, `B -> G^T B` at one bond.  The contraction is unchanged because `G` is
/// orthogonal, and the local block metrics remain identities for the same reason.
fn orthogonal_rechart(tensors: &mut [TensorSite], bond: usize, angle: f64) {
    let chi = tensors[bond].chi_r;
    assert_eq!(chi, tensors[bond + 1].chi_l);

    let (cos, sin) = (angle.cos(), angle.sin());
    let mut g = vec![0.0; chi * chi];
    for i in 0..chi {
        g[i * chi + i] = 1.0;
    }
    g[0] = cos;
    g[1] = -sin;
    g[chi] = sin;
    g[chi + 1] = cos;

    let left_old = tensors[bond].clone();
    for physical in 0..2 {
        for left in 0..left_old.chi_l {
            for new_right in 0..chi {
                let value = (0..chi)
                    .map(|old_right| {
                        left_old.get(physical, left, old_right) * g[old_right * chi + new_right]
                    })
                    .sum();
                tensors[bond].set(physical, left, new_right, value);
            }
        }
    }

    let right_old = tensors[bond + 1].clone();
    for physical in 0..2 {
        for new_left in 0..chi {
            for right in 0..right_old.chi_r {
                let value = (0..chi)
                    .map(|old_left| {
                        g[old_left * chi + new_left] * right_old.get(physical, old_left, right)
                    })
                    .sum();
                tensors[bond + 1].set(physical, new_left, right, value);
            }
        }
    }
}

fn normalized_view(tensors: &[TensorSite]) -> Vec<f64> {
    let mut view = expand_statevector(tensors);
    let norm = view.iter().map(|x| x * x).sum::<f64>().sqrt();
    assert!(norm > 0.0);
    for amplitude in &mut view {
        *amplitude /= norm;
    }
    view
}

fn phase_aligned_max_defect(left: &[f64], right: &[f64]) -> f64 {
    assert_eq!(left.len(), right.len());
    let overlap = left.iter().zip(right).map(|(a, b)| a * b).sum::<f64>();
    let sign = if overlap < 0.0 { -1.0 } else { 1.0 };
    left.iter()
        .zip(right)
        .map(|(a, b)| (a - sign * b).abs())
        .fold(0.0, f64::max)
}

/// Independent physical-state View. Bit `j` is the occupation of interleaved JW orbital `j`.
fn expand_statevector(tensors: &[TensorSite]) -> Vec<f64> {
    assert!(!tensors.is_empty());
    assert_eq!(tensors[0].chi_l, 1);
    let mut partial = vec![1.0f64];
    let mut prefixes = 1usize;
    let mut left_dim = 1usize;

    for (site, tensor) in tensors.iter().enumerate() {
        assert_eq!(
            tensor.chi_l, left_dim,
            "broken MPS bond before orbital {site}"
        );
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
