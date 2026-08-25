//! DIAGNOSTIC ONLY — independent TNC View for OBJECT.md claim transport.
//!
//! The q8 MPS returned by the optimizer is frozen as the World.  This process then
//! translates each real `[physical][left][right]` tensor into TNC leaf tensors and
//! asks TNC/TBLIS to contract the norm, Hubbard energy, and site-local content
//! claims.  It calls no q8 MPO, environment, or observable contraction routine.
//!
//! The correspondence under test is
//! `[empty, up, down, full] <-> adjacent q8 JW bits [up, down]`.
//! A direct exact-seam state-vector View and q-seam Door remain live in the same
//! receipt.  The commuting square passes only when TNC and the direct View agree to
//! `1e-10`.  A planted mutation which erases the intervening Jordan-Wigner Z string
//! must move the energy by more than `1e-6`.

use num_complex::Complex64;
use q8_mps::dmrg::{self, Params, RefusalPolicy, SweepResult};
use q8_mps::mps::{self, TensorSite};
use rustc_hash::FxHashMap;
use std::time::Instant;
use tnc::contractionpath::ContractionPath;
use tnc::tensornetwork::contraction::contract_tensor_network;
use tnc::tensornetwork::tensor::{CompositeTensor, LeafTensor};
use tnc::tensornetwork::tensordata::TensorData;

const TRANSPORT_TOL: f64 = 1e-10;
const MUTANT_MIN_MOVE: f64 = 1e-6;

type Op = [[f64; 2]; 2];

const ID: Op = [[1.0, 0.0], [0.0, 1.0]];
const NUMBER: Op = [[0.0, 0.0], [0.0, 1.0]];
const Z: Op = [[1.0, 0.0], [0.0, -1.0]];
const CREATE: Op = [[0.0, 0.0], [1.0, 0.0]];
const ANNIHILATE: Op = [[0.0, 1.0], [0.0, 0.0]];

#[derive(Debug)]
struct ContentView {
    norm_squared: f64,
    energy: f64,
    density: Vec<f64>,
    magnetization: Vec<f64>,
    double_occupancy: Vec<f64>,
}

#[derive(Debug)]
struct TncReceipt {
    content: ContentView,
    mutant_energy: f64,
    contractions: usize,
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let sites = parse_arg(&args, 1, 8usize, "sites");
    let u = parse_arg(&args, 2, 16.0f64, "U");
    let chi = parse_arg(&args, 3, 32usize, "chi");
    assert!(sites > 0 && sites % 2 == 0, "frozen family requires even N");
    assert!(sites <= 10, "direct exact-seam View is bounded to N <= 10");

    let t = 1.0;
    let params = Params {
        sites,
        t,
        u,
        chi_max: chi,
        max_sweeps: 20,
        sweep_tol: 1e-10,
    };

    let door_started = Instant::now();
    let exact_h = q_seam::hubbard::Hubbard::new(sites, t, u);
    let exact = q_seam::lanczos::ground_state(&exact_h).expect("q-seam Door refused");

    println!("=== OBJECT / TNC claim-transport receipt ===");
    println!("TNC source: qc-tum/TNC@0b35c58146751cafeadcf31684cd51ae8f4602c2");
    println!("World: open Hubbard N={sites} t={t} U={u} Ne={sites} 2Sz=0 chi={chi}");
    println!(
        "Door: q-seam E={:.15} residual={:.3e} iterations={} wall={:.3}s",
        exact.energy,
        exact.residual,
        exact.iterations,
        door_started.elapsed().as_secs_f64()
    );
    println!("R: [empty,up,down,full] <-> adjacent interleaved JW bits [up,down]");
    println!(
        "Predeclared: transport <= {:.1e}; mutant energy move > {:.1e}",
        TRANSPORT_TOL, MUTANT_MIN_MOVE
    );

    let mut returned_energies = Vec::new();
    for (start_name, initial) in [
        ("neel", mps::initial_state(sites)),
        ("doublon-hole", doublon_hole_state(sites)),
    ] {
        let habit_started = Instant::now();
        let result = match dmrg::run_from(&params, RefusalPolicy::Typed, initial) {
            Ok(result) => result,
            Err(refusal) => {
                println!(
                    "\n{start_name}: FLOOR REFUSAL bond={} discarded_weight={:.6e}",
                    refusal.bond, refusal.weight
                );
                continue;
            }
        };
        let habit_seconds = habit_started.elapsed().as_secs_f64();

        let direct_started = Instant::now();
        let amplitudes = expand_statevector(&result.tensors);
        let direct = direct_content_view(&amplitudes, sites, t, u, true);
        let direct_seconds = direct_started.elapsed().as_secs_f64();

        let tnc_started = Instant::now();
        let tnc = tnc_receipt(&result.tensors, sites, t, u);
        let tnc_seconds = tnc_started.elapsed().as_secs_f64();

        let reported_energy = unshifted_reported_energy(&result, sites, u);
        let transport_defect = content_defect(&tnc.content, &direct);
        let report_tnc_defect = (reported_energy - tnc.content.energy).abs();
        let exact_defect = (tnc.content.energy - exact.energy).abs();
        let mutant_move = (tnc.mutant_energy - tnc.content.energy).abs();
        let transport_pass = transport_defect <= TRANSPORT_TOL;
        let report_pass = report_tnc_defect <= TRANSPORT_TOL;
        let mutant_pass = mutant_move > MUTANT_MIN_MOVE;
        returned_energies.push(tnc.content.energy);

        println!("\n--- frozen World from {start_name} ---");
        println!(
            "E: q8-report={reported_energy:.15} direct={:.15} TNC={:.15}",
            direct.energy, tnc.content.energy
        );
        println!(
            "defects: TNC<->direct={transport_defect:.6e} report<->TNC={report_tnc_defect:.6e} TNC<->Door={exact_defect:.6e}"
        );
        println!(
            "norm2: direct={:.15} TNC={:.15}",
            direct.norm_squared, tnc.content.norm_squared
        );
        println!(
            "content max defects: density={:.6e} magnetization={:.6e} double_occ={:.6e}",
            max_abs_diff(&direct.density, &tnc.content.density),
            max_abs_diff(&direct.magnetization, &tnc.content.magnetization),
            max_abs_diff(&direct.double_occupancy, &tnc.content.double_occupancy)
        );
        println!(
            "mutant(no JW Z) E={:.15} move={mutant_move:.6e}",
            tnc.mutant_energy
        );
        println!(
            "Habit: sweeps={} converged={} canonical(L/R)=({:.3e},{:.3e}) local-residual={:.3e} wall={habit_seconds:.3}s",
            result.sweeps_used,
            result.converged,
            result.worst_left_canonical_defect,
            result.worst_right_canonical_defect,
            result.worst_lanczos_residual
        );
        println!(
            "Views: direct={direct_seconds:.3}s TNC={tnc_seconds:.3}s contractions={} transport={} report-is-state={} mutant-caught={}",
            tnc.contractions,
            pass(transport_pass),
            pass(report_pass),
            pass(mutant_pass)
        );

        assert!(transport_pass, "TNC/direct claim transport failed");
        assert!(report_pass, "q8 report is not the TNC energy of its returned state");
        assert!(mutant_pass, "planted Jordan-Wigner mutation was not discriminated");
    }

    assert_eq!(returned_energies.len(), 2, "both posed starts must return a World");
    println!(
        "\nposed contrast: |E_neel-E_doublon-hole|={:.6e}",
        (returned_energies[0] - returned_energies[1]).abs()
    );
    println!("RESULT: narrow content-bearing claim transport PASS");
}

fn parse_arg<T>(args: &[String], index: usize, default: T, label: &str) -> T
where
    T: std::str::FromStr,
    T::Err: std::fmt::Debug,
{
    args.get(index)
        .map(|value| value.parse().unwrap_or_else(|_| panic!("{label} has invalid syntax")))
        .unwrap_or(default)
}

fn pass(value: bool) -> &'static str {
    if value { "PASS" } else { "FAIL" }
}

fn unshifted_reported_energy(result: &SweepResult, sites: usize, u: f64) -> f64 {
    result.energy_shifted + (u / 2.0) * sites as f64
}

fn doublon_hole_state(sites: usize) -> Vec<TensorSite> {
    (0..2 * sites)
        .map(|orbital| {
            let occupied = (orbital / 2) % 2 == 0;
            let mut tensor = TensorSite::zeros(1, 1);
            tensor.set(usize::from(occupied), 0, 0, 1.0);
            tensor
        })
        .collect()
}

fn tnc_receipt(tensors: &[TensorSite], sites: usize, t: f64, u: f64) -> TncReceipt {
    let orbitals = tensors.len();
    assert_eq!(orbitals, 2 * sites);
    let identity = vec![ID; orbitals];
    let norm_squared = tnc_expectation(tensors, &identity);
    assert!(norm_squared > 0.0);
    let mut contractions = 1usize;

    let energy_numerator = tnc_hubbard_numerator(tensors, sites, t, u, true, &mut contractions);
    let mutant_numerator =
        tnc_hubbard_numerator(tensors, sites, t, u, false, &mut contractions);

    let mut density = vec![0.0; sites];
    let mut magnetization = vec![0.0; sites];
    let mut double_occupancy = vec![0.0; sites];
    for site in 0..sites {
        let up = one_body_expectation(tensors, 2 * site, NUMBER, &mut contractions);
        let down = one_body_expectation(tensors, 2 * site + 1, NUMBER, &mut contractions);
        let mut ops = identity.clone();
        ops[2 * site] = NUMBER;
        ops[2 * site + 1] = NUMBER;
        let double = tnc_expectation(tensors, &ops);
        contractions += 1;

        density[site] = (up + down) / norm_squared;
        magnetization[site] = (up - down) / norm_squared;
        double_occupancy[site] = double / norm_squared;
    }

    TncReceipt {
        content: ContentView {
            norm_squared,
            energy: energy_numerator / norm_squared,
            density,
            magnetization,
            double_occupancy,
        },
        mutant_energy: mutant_numerator / norm_squared,
        contractions,
    }
}

fn one_body_expectation(
    tensors: &[TensorSite],
    orbital: usize,
    operator: Op,
    contractions: &mut usize,
) -> f64 {
    let mut ops = vec![ID; tensors.len()];
    ops[orbital] = operator;
    *contractions += 1;
    tnc_expectation(tensors, &ops)
}

fn tnc_hubbard_numerator(
    tensors: &[TensorSite],
    sites: usize,
    t: f64,
    u: f64,
    fermionic_signs: bool,
    contractions: &mut usize,
) -> f64 {
    let mut total = 0.0;
    for site in 0..sites {
        let mut ops = vec![ID; tensors.len()];
        ops[2 * site] = NUMBER;
        ops[2 * site + 1] = NUMBER;
        total += u * tnc_expectation(tensors, &ops);
        *contractions += 1;
    }

    for site in 0..sites - 1 {
        for spin in 0..2 {
            let left = 2 * site + spin;
            let right = 2 * (site + 1) + spin;

            let mut right_to_left = vec![ID; tensors.len()];
            right_to_left[left] = CREATE;
            right_to_left[right] = ANNIHILATE;
            if fermionic_signs {
                right_to_left[left + 1..right].fill(Z);
            }
            total -= t * tnc_expectation(tensors, &right_to_left);
            *contractions += 1;

            let mut left_to_right = vec![ID; tensors.len()];
            left_to_right[left] = ANNIHILATE;
            left_to_right[right] = CREATE;
            if fermionic_signs {
                left_to_right[left + 1..right].fill(Z);
            }
            total -= t * tnc_expectation(tensors, &left_to_right);
            *contractions += 1;
        }
    }
    total
}

/// Build and fully contract `<MPS| product_j(op_j) |MPS>` in TNC.
///
/// Every edge id occurs exactly twice.  The fixed left fold is part of the receipt:
/// no path finder or q8 contraction schedule participates in this View.
fn tnc_expectation(tensors: &[TensorSite], operators: &[Op]) -> f64 {
    assert_eq!(tensors.len(), operators.len());
    let orbitals = tensors.len();
    let ket_bond_base = orbitals + 1;
    let bra_physical_base = 2 * (orbitals + 1);
    let ket_physical_base = bra_physical_base + orbitals;

    let mut dimensions = FxHashMap::default();
    for bond in 0..=orbitals {
        let dimension = if bond == 0 {
            tensors[0].chi_l
        } else {
            tensors[bond - 1].chi_r
        };
        dimensions.insert(bond, dimension as u64);
        dimensions.insert(ket_bond_base + bond, dimension as u64);
    }
    for orbital in 0..orbitals {
        dimensions.insert(bra_physical_base + orbital, 2);
        dimensions.insert(ket_physical_base + orbital, 2);
    }

    let mut leaves = Vec::with_capacity(3 * orbitals + 4);
    leaves.push(real_leaf(vec![0], &dimensions, &[1.0]));
    leaves.push(real_leaf(vec![ket_bond_base], &dimensions, &[1.0]));

    for (orbital, (tensor, operator)) in tensors.iter().zip(operators).enumerate() {
        assert_eq!(tensor.chi_l as u64, dimensions[&orbital]);
        assert_eq!(tensor.chi_r as u64, dimensions[&(orbital + 1)]);

        leaves.push(real_leaf(
            vec![bra_physical_base + orbital, orbital, orbital + 1],
            &dimensions,
            &tensor.data,
        ));

        let operator_data = [
            operator[0][0],
            operator[0][1],
            operator[1][0],
            operator[1][1],
        ];
        leaves.push(real_leaf(
            vec![bra_physical_base + orbital, ket_physical_base + orbital],
            &dimensions,
            &operator_data,
        ));

        leaves.push(real_leaf(
            vec![ket_physical_base + orbital, ket_bond_base + orbital, ket_bond_base + orbital + 1],
            &dimensions,
            &tensor.data,
        ));
    }

    leaves.push(real_leaf(vec![orbitals], &dimensions, &[1.0]));
    leaves.push(real_leaf(
        vec![ket_bond_base + orbitals],
        &dimensions,
        &[1.0],
    ));

    let path = ContractionPath::simple((1..leaves.len()).map(|index| (0, index)).collect());
    let result = contract_tensor_network(CompositeTensor::new(leaves), &path);
    assert!(result.legs().is_empty(), "TNC left dangling claim edges");
    let data = result.into_data().into_data();
    assert_eq!(data.len(), 1, "fully contracted claim must be scalar");
    let value = data.iter().next().copied().unwrap();
    assert!(value.im.abs() <= 1e-11, "real claim acquired imaginary residue {value:?}");
    value.re
}

fn real_leaf(
    legs: Vec<usize>,
    dimensions: &FxHashMap<usize, u64>,
    data: &[f64],
) -> LeafTensor {
    let shape: Vec<usize> = legs.iter().map(|leg| dimensions[leg] as usize).collect();
    assert_eq!(shape.iter().product::<usize>(), data.len());
    let complex_data = data.iter().map(|value| Complex64::new(*value, 0.0)).collect();
    let mut tensor = LeafTensor::new_from_map(legs, dimensions);
    tensor.set_tensor_data(TensorData::new_from_data(&shape, complex_data));
    tensor
}

fn expand_statevector(tensors: &[TensorSite]) -> Vec<f64> {
    assert!(!tensors.is_empty());
    assert_eq!(tensors[0].chi_l, 1);
    let mut partial = vec![1.0f64];
    let mut prefixes = 1usize;
    let mut left_dim = 1usize;

    for (orbital, tensor) in tensors.iter().enumerate() {
        assert_eq!(tensor.chi_l, left_dim, "broken MPS bond before orbital {orbital}");
        let mut next = vec![0.0; prefixes * 2 * tensor.chi_r];
        for prefix in 0..prefixes {
            for left in 0..left_dim {
                let coefficient = partial[prefix * left_dim + left];
                if coefficient == 0.0 {
                    continue;
                }
                for occupied in 0..2 {
                    let next_prefix = prefix | (occupied << orbital);
                    for right in 0..tensor.chi_r {
                        next[next_prefix * tensor.chi_r + right] +=
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

fn direct_content_view(
    amplitudes: &[f64],
    sites: usize,
    t: f64,
    u: f64,
    fermionic_signs: bool,
) -> ContentView {
    assert_eq!(amplitudes.len(), 1usize << (2 * sites));
    let norm_squared = amplitudes.iter().map(|value| value * value).sum::<f64>();
    assert!(norm_squared > 0.0);
    let hpsi = apply_hubbard(amplitudes, sites, t, u, fermionic_signs);
    let energy = amplitudes.iter().zip(&hpsi).map(|(a, b)| a * b).sum::<f64>() / norm_squared;

    let mut density = vec![0.0; sites];
    let mut magnetization = vec![0.0; sites];
    let mut double_occupancy = vec![0.0; sites];
    for (basis, amplitude) in amplitudes.iter().copied().enumerate() {
        let weight = amplitude * amplitude / norm_squared;
        for site in 0..sites {
            let up = ((basis >> (2 * site)) & 1) as f64;
            let down = ((basis >> (2 * site + 1)) & 1) as f64;
            density[site] += weight * (up + down);
            magnetization[site] += weight * (up - down);
            double_occupancy[site] += weight * up * down;
        }
    }

    ContentView { norm_squared, energy, density, magnetization, double_occupancy }
}

fn apply_hubbard(
    amplitudes: &[f64],
    sites: usize,
    t: f64,
    u: f64,
    fermionic_signs: bool,
) -> Vec<f64> {
    let mut output = vec![0.0; amplitudes.len()];
    for (basis, amplitude) in amplitudes.iter().copied().enumerate() {
        if amplitude == 0.0 {
            continue;
        }
        let doubles = (0..sites)
            .filter(|site| {
                basis & (1 << (2 * site)) != 0 && basis & (1 << (2 * site + 1)) != 0
            })
            .count();
        output[basis] += u * doubles as f64 * amplitude;

        for site in 0..sites - 1 {
            for spin in 0..2 {
                let left = 2 * site + spin;
                let right = 2 * (site + 1) + spin;
                for (destination, source) in [(left, right), (right, left)] {
                    if let Some((next, sign)) = hop(basis, destination, source, fermionic_signs) {
                        output[next] -= t * sign * amplitude;
                    }
                }
            }
        }
    }
    output
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

fn content_defect(left: &ContentView, right: &ContentView) -> f64 {
    [
        (left.norm_squared - right.norm_squared).abs(),
        (left.energy - right.energy).abs(),
        max_abs_diff(&left.density, &right.density),
        max_abs_diff(&left.magnetization, &right.magnetization),
        max_abs_diff(&left.double_occupancy, &right.double_occupancy),
    ]
    .into_iter()
    .fold(0.0, f64::max)
}

fn max_abs_diff(left: &[f64], right: &[f64]) -> f64 {
    assert_eq!(left.len(), right.len());
    left.iter()
        .zip(right)
        .map(|(a, b)| (a - b).abs())
        .fold(0.0, f64::max)
}
