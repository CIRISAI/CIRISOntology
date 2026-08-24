//! Shared gate infrastructure for G0-1 (`tests/g0_sector_shift.rs`) and G1a/G1b
//! (`tests/g1_mpo_correctness.rs`) — `Q8_MPS_PREREG.md` §3.
//!
//! `mod common;` is compiled once PER integration-test binary, so a function only one of the two
//! binaries calls is "unused" from the other's point of view — not a real dead-code question,
//! the standard shape of a shared `tests/common/mod.rs`.
#![allow(dead_code)]
//!
//! `independent_dense_h` is the G1a cross-check: a brute-force second-quantization build over
//! Fock-basis bitmasks, sharing NO code with `q8_mps::mpo`'s tensor contraction — the whole
//! point of G1a is two independently-derived constructions agreeing. It is written directly
//! from `c†_p c_q = sigma+_p . (Z-string over strictly-between sites) . sigma-_q` (`p<q`), the
//! same derivation `mpo.rs`'s header states, but as flat bitmask arithmetic rather than tensor
//! contraction — a genuinely different code shape, not a copy.

/// `c†_a c_b` acting on `mask` (bit `q` = occupation of JW site `q`, 0-indexed). `None` if the
/// term annihilates. General JW sign: `(-1)^(popcount of mask strictly between a and b)`.
pub fn jw_hop(mask: u32, a: usize, b: usize) -> Option<(u32, f64)> {
    if mask & (1 << b) == 0 {
        return None;
    }
    let new_mask = mask & !(1u32 << b);
    if new_mask & (1 << a) != 0 {
        return None;
    }
    let lo = a.min(b) + 1;
    let hi = a.max(b);
    let sign = if hi > lo {
        let between = (mask >> lo) & ((1u32 << (hi - lo)) - 1);
        if between.count_ones().is_multiple_of(2) {
            1.0
        } else {
            -1.0
        }
    } else {
        1.0
    };
    Some((new_mask | (1 << a), sign))
}

/// Dense `H'` (or bare `H` at `mu=0.0`) over the FULL `2^(2*sites)`-dim Fock space, built
/// directly from `jw_hop` — independent of `q8_mps::mpo`. Gate-only, `sites<=4`.
pub fn independent_dense_h(sites: usize, t: f64, u: f64, mu: f64) -> Vec<f64> {
    let l = 2 * sites;
    let dim = 1usize << l;
    let mut h = vec![0.0; dim * dim];

    for mask in 0..dim as u32 {
        let mut diag = -mu * mask.count_ones() as f64;
        for s in 0..sites {
            let up = (mask >> (2 * s)) & 1;
            let dn = (mask >> (2 * s + 1)) & 1;
            diag += u * (up * dn) as f64;
        }
        h[mask as usize * dim + mask as usize] += diag;

        for j in 0..l.saturating_sub(2) {
            let (a, b) = (j, j + 2);
            if let Some((new_mask, sign)) = jw_hop(mask, a, b) {
                h[new_mask as usize * dim + mask as usize] += -t * sign;
            }
            if let Some((new_mask, sign)) = jw_hop(mask, b, a) {
                h[new_mask as usize * dim + mask as usize] += -t * sign;
            }
        }
    }
    h
}

/// `(<N_up>, <N_down>)` of a real eigenvector over the full `2^(2*sites)` Fock basis — the
/// "measured, not assumed" sector check both G0-1 and G1b rely on.
pub fn sector_of(v: &[f64], sites: usize) -> (f64, f64) {
    let mut nup = 0.0;
    let mut ndn = 0.0;
    for (mask, &amp) in v.iter().enumerate() {
        let w = amp * amp;
        if w == 0.0 {
            continue;
        }
        let m = mask as u32;
        for s in 0..sites {
            if (m >> (2 * s)) & 1 == 1 {
                nup += w;
            }
            if (m >> (2 * s + 1)) & 1 == 1 {
                ndn += w;
            }
        }
    }
    (nup, ndn)
}

pub fn max_abs_diff(a: &[f64], b: &[f64]) -> f64 {
    a.iter().zip(b).map(|(x, y)| (x - y).abs()).fold(0.0, f64::max)
}

/// The validation grid's `U/t` values, `Q8_MPS_PREREG.md` §1.
pub const U_GRID: [f64; 4] = [0.0, 1.0, 4.0, 16.0];
