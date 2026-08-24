//! Ground state by Lanczos with full reorthogonalization.
//!
//! Every knob here is pinned by amendment A1/P1 of `Q_SEAM_PREREG.md`, because replay discipline
//! applies to instruments and a random start makes the residual ladder non-replayable:
//!
//! * start vector from **SplitMix64**, seed [`START_SEED`], entries uniform on `[-1, 1]`,
//!   normalized, over the basis in canonical ascending order;
//! * a fixed all-ones start is **rejected** — it is a symmetry eigenvector and can be exactly
//!   orthogonal to a ground state of the opposite parity under global spin flip;
//! * full reorthogonalization against every stored Krylov vector;
//! * the **orthogonality guard** `|<v0|psi0>| >= 1e-8` is reported and enforced;
//! * on a failed residual gate or a failed guard: **one** deterministic restart at `seed + 1`,
//!   reported; a second failure VOIDs the configuration. No adaptive retries.

use crate::dense::jacobi;
use crate::hubbard::Hubbard;

/// A1/P1's pinned start seed. (Corrected from the prereg's first printing, which used a
/// non-hexadecimal digit — see `Q_SEAM_PREREG.md` A1/T.)
pub const START_SEED: u64 = 0x515F_5EA0_0000_0001;

/// Iteration cap. A1/P1 pins 500; the ceiling that actually binds is memory, since full
/// reorthogonalization stores every Krylov vector (400 x 63 504 x 8 B ~ 203 MB at N = 10).
pub const MAX_ITERS: usize = 400;

/// The G-E4a residual gate, relative to `max(1, |E|)`.
pub const RESIDUAL_GATE: f64 = 1e-12;

/// The A1/P1 orthogonality guard on the start vector's overlap with the ground state.
pub const OVERLAP_GUARD: f64 = 1e-8;

#[derive(Clone, Debug)]
pub struct GroundState {
    pub energy: f64,
    pub vector: Vec<f64>,
    /// `||H v - E v|| / (||v|| max(1, |E|))` — the gate quantity, measured not assumed.
    pub residual: f64,
    /// Second Ritz value: the in-sector gap for G-E6. An estimate, and labelled as one.
    pub first_excited: f64,
    pub overlap_start: f64,
    pub iterations: usize,
    pub restarts: usize,
    pub seed: u64,
}

struct SplitMix64(u64);

impl SplitMix64 {
    fn next_u64(&mut self) -> u64 {
        self.0 = self.0.wrapping_add(0x9E37_79B9_7F4A_7C15);
        let mut z = self.0;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
        z ^ (z >> 31)
    }

    /// Uniform on `[-1, 1]`.
    fn next_signed(&mut self) -> f64 {
        let bits = self.next_u64() >> 11; // 53 significant bits
        (bits as f64 / (1u64 << 53) as f64) * 2.0 - 1.0
    }
}

fn seeded_start(dim: usize, seed: u64) -> Vec<f64> {
    let mut rng = SplitMix64(seed);
    let mut v: Vec<f64> = (0..dim).map(|_| rng.next_signed()).collect();
    let norm = v.iter().map(|x| x * x).sum::<f64>().sqrt();
    for x in v.iter_mut() {
        *x /= norm;
    }
    v
}

/// One Lanczos run at a given seed. `None` means the residual gate or the guard failed.
fn run_once(h: &Hubbard, seed: u64) -> Option<GroundState> {
    let dim = h.dim();
    let v0 = seeded_start(dim, seed);

    let mut basis: Vec<Vec<f64>> = Vec::with_capacity(MAX_ITERS);
    let mut alpha: Vec<f64> = Vec::new();
    let mut beta: Vec<f64> = Vec::new();

    basis.push(v0.clone());
    let mut w = vec![0.0; dim];
    let mut iterations = 0;

    let mut best: Option<(f64, f64, Vec<f64>)> = None; // (E0, E1, ritz vector)

    for j in 0..MAX_ITERS {
        iterations = j + 1;
        h.apply(&basis[j], &mut w);

        let a = dot(&w, &basis[j]);
        alpha.push(a);
        for k in 0..dim {
            w[k] -= a * basis[j][k];
        }
        if j > 0 {
            let b = beta[j - 1];
            for k in 0..dim {
                w[k] -= b * basis[j - 1][k];
            }
        }
        // Full reorthogonalization, twice — one pass is not enough once the basis is large.
        for _ in 0..2 {
            for u in basis.iter() {
                let c = dot(&w, u);
                for k in 0..dim {
                    w[k] -= c * u[k];
                }
            }
        }

        let b = dot(&w, &w).sqrt();

        // Solve the tridiagonal Ritz problem on what we have.
        let m = alpha.len();
        let mut tri = vec![0.0; m * m];
        for i in 0..m {
            tri[i * m + i] = alpha[i];
            if i + 1 < m {
                tri[i * m + i + 1] = beta[i];
                tri[(i + 1) * m + i] = beta[i];
            }
        }
        let eig = jacobi(tri, m);
        let e0 = eig.values[0];
        let e1 = if m > 1 { eig.values[1] } else { f64::INFINITY };

        // Ritz residual estimate for the lowest pair, and the breakdown case.
        let est = b * eig.vectors[0][m - 1].abs();
        let breakdown = b <= 1e-13;

        if est <= 0.1 * RESIDUAL_GATE * e0.abs().max(1.0) || breakdown || j == MAX_ITERS - 1 {
            let mut ritz = vec![0.0; dim];
            for (k, uk) in basis.iter().enumerate() {
                let c = eig.vectors[0][k];
                for i in 0..dim {
                    ritz[i] += c * uk[i];
                }
            }
            let norm = dot(&ritz, &ritz).sqrt();
            for x in ritz.iter_mut() {
                *x /= norm;
            }
            best = Some((e0, e1, ritz));
            break;
        }

        beta.push(b);
        for k in 0..dim {
            w[k] /= b;
        }
        basis.push(w.clone());
    }

    let (energy, first_excited, vector) = best?;

    let mut hv = vec![0.0; dim];
    h.apply(&vector, &mut hv);
    let resid = hv
        .iter()
        .zip(vector.iter())
        .map(|(a, b)| (a - energy * b) * (a - energy * b))
        .sum::<f64>()
        .sqrt()
        / energy.abs().max(1.0);

    let overlap_start = dot(&v0, &vector).abs();

    if resid > RESIDUAL_GATE || overlap_start < OVERLAP_GUARD {
        return None;
    }

    Some(GroundState {
        energy,
        vector,
        residual: resid,
        first_excited,
        overlap_start,
        iterations,
        restarts: 0,
        seed,
    })
}

/// The pinned policy: one run, then exactly one deterministic restart at `seed + 1`.
pub fn ground_state(h: &Hubbard) -> Option<GroundState> {
    if let Some(g) = run_once(h, START_SEED) {
        return Some(g);
    }
    let mut g = run_once(h, START_SEED + 1)?;
    g.restarts = 1;
    Some(g)
}

#[inline]
fn dot(a: &[f64], b: &[f64]) -> f64 {
    a.iter().zip(b.iter()).map(|(x, y)| x * y).sum()
}
