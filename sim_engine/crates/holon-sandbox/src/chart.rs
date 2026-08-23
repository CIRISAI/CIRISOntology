//! The spatial chart: where a holon sits, in metres, at whatever tier it belongs to.
//!
//! A chart is not a second ontology and carries no state of its own beyond geometry. It
//! is a pure function of the arena's TREE STRUCTURE: child ordinal within its batch
//! selects the quadrant, batches append contiguously, so the ordinal is the running
//! child count of the parent. That is the same construction
//! `ciris_sim_core::fracture::WallChart` uses, kept because it is correct and because
//! reusing its shape means a reader who knows one knows the other.
//!
//! Cells are square at every depth because every tier's domain is square (see
//! `tier`'s header for why that is a choice and not a limitation).

use ciris_sim_core::runtime::{RuntimeArena, NO_RUNTIME_HOLON};

/// Quadtree fanout. Two dimensions, halved on both axes.
pub const FANOUT: usize = 4;

/// One resident cell, in tier metres.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Cell {
    pub x0: f64,
    pub y0: f64,
    pub size: f64,
}

impl Cell {
    pub fn centre(&self) -> [f64; 2] {
        [self.x0 + 0.5 * self.size, self.y0 + 0.5 * self.size]
    }

    /// Distance from this cell's rectangle to a point; zero if the point is inside.
    pub fn distance_to(&self, point: [f64; 2]) -> f64 {
        let dx = (self.x0 - point[0])
            .max(point[0] - (self.x0 + self.size))
            .max(0.0);
        let dy = (self.y0 - point[1])
            .max(point[1] - (self.y0 + self.size))
            .max(0.0);
        (dx * dx + dy * dy).sqrt()
    }

    /// Fraction of this cell's area below `y`, in [0, 1]. This is how a domain-filling
    /// matter line apportions constituents between quadrants exactly.
    pub fn fraction_below(&self, y: f64) -> f64 {
        if self.size <= 0.0 {
            return 0.0;
        }
        ((y - self.y0) / self.size).clamp(0.0, 1.0)
    }
}

/// Cell rectangles for every holon in an arena, extended as the arena grows.
#[derive(Clone, Debug, Default)]
pub struct Chart {
    domain_m: f64,
    cells: Vec<Cell>,
    children_seen: Vec<u8>,
}

impl Chart {
    pub fn new(domain_m: f64) -> Self {
        Self {
            domain_m,
            cells: Vec::new(),
            children_seen: Vec::new(),
        }
    }

    pub fn domain_m(&self) -> f64 {
        self.domain_m
    }

    pub fn len(&self) -> usize {
        self.cells.len()
    }

    pub fn is_empty(&self) -> bool {
        self.cells.is_empty()
    }

    /// Extend to cover newly materialized holons. Cheap and idempotent: it does nothing
    /// once the chart has caught up with the arena.
    pub fn sync(&mut self, arena: &RuntimeArena) {
        if self.cells.len() == arena.len() {
            return;
        }
        for id in self.cells.len()..arena.len() {
            let record = arena.holons()[id];
            let cell = if record.parent == NO_RUNTIME_HOLON {
                Cell {
                    x0: 0.0,
                    y0: 0.0,
                    size: self.domain_m,
                }
            } else {
                let parent = record.parent as usize;
                let ordinal = self.children_seen[parent] as usize;
                self.children_seen[parent] += 1;
                debug_assert!(ordinal < FANOUT);
                let parent_cell = self.cells[parent];
                let half = 0.5 * parent_cell.size;
                Cell {
                    x0: parent_cell.x0 + (ordinal % 2) as f64 * half,
                    y0: parent_cell.y0 + (ordinal / 2) as f64 * half,
                    size: half,
                }
            };
            self.cells.push(cell);
            self.children_seen.push(0);
        }
    }

    pub fn cell(&self, holon: usize) -> Cell {
        self.cells[holon]
    }

    pub fn get(&self, holon: usize) -> Option<Cell> {
        self.cells.get(holon).copied()
    }
}

/// Resolution the fractional cell weights are quantized to before apportionment.
///
/// One part per million of a cell is far finer than any geometry this chart resolves,
/// and quantizing is what lets the apportionment run in exact integer arithmetic.
pub const WEIGHT_SCALE: u64 = 1_000_000;

/// Largest-remainder apportionment of `total` over fractional `weights`, exact by
/// construction: the shares sum to `total`, and ties break toward the lowest index so
/// replay is bit-identical.
///
/// The arithmetic is INTEGER throughout, in `u128`. The obvious float version —
/// multiply the total by each weight's share and hand out the remainder — silently
/// stops being exact once the total passes 2^53, and at `u64::MAX / 8` the rounding
/// error is large enough that the remainder loop does not terminate in any useful time.
/// `descriptor.rs` reaches the same conclusion for the same reason ("weights must each
/// be positive and fit in `u32` so the `i128` intermediate cannot overflow"), so this
/// follows it.
///
/// This is also what makes air cells honest. A quadrant with no matter in it gets a
/// share of zero and composes exactly; nothing is smeared into it to make the arithmetic
/// close.
pub fn apportion(total: u64, weights: &[f64]) -> Vec<u64> {
    let scaled: Vec<u64> = weights
        .iter()
        .map(|weight| {
            if !weight.is_finite() || *weight <= 0.0 {
                0
            } else {
                (weight.min(1.0) * WEIGHT_SCALE as f64).round() as u64
            }
        })
        .collect();
    apportion_exact(total, &scaled)
}

/// Exact largest-remainder apportionment over integer weights.
pub fn apportion_exact(total: u64, weights: &[u64]) -> Vec<u64> {
    let sum: u128 = weights.iter().map(|weight| *weight as u128).sum();
    if sum == 0 {
        // No weight anywhere. Everything to the first slot rather than losing it: the
        // ledger must still compose exactly, which is the only thing at stake.
        let mut shares = vec![0_u64; weights.len()];
        if let Some(first) = shares.first_mut() {
            *first = total;
        }
        return shares;
    }

    let total128 = total as u128;
    let mut shares = Vec::with_capacity(weights.len());
    let mut remainders = Vec::with_capacity(weights.len());
    let mut assigned: u128 = 0;
    for weight in weights {
        let numerator = total128 * (*weight as u128);
        let floor = numerator / sum;
        remainders.push(numerator % sum);
        assigned += floor;
        shares.push(floor as u64);
    }

    // Hand out the remainder by largest fractional part, lowest index first on a tie.
    // There are at most `weights.len() - 1` units left, so this loop is bounded by the
    // fanout however large the total is.
    let mut remaining = total128 - assigned;
    while remaining > 0 {
        let mut best = 0_usize;
        let mut best_remainder = 0_u128;
        let mut found = false;
        for (index, remainder) in remainders.iter().enumerate() {
            if !found || *remainder > best_remainder {
                best = index;
                best_remainder = *remainder;
                found = true;
            }
        }
        shares[best] += 1;
        remainders[best] = 0;
        remaining -= 1;
    }
    shares
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn apportionment_is_exact_and_gives_empty_quadrants_nothing() {
        let shares = apportion(1_000_001, &[0.0, 0.0, 0.5, 0.5]);
        assert_eq!(shares.iter().sum::<u64>(), 1_000_001);
        assert_eq!(shares[0], 0);
        assert_eq!(shares[1], 0);
        // The odd unit goes to the lowest-index tie, so replay is deterministic.
        assert_eq!(shares[2], 500_001);
        assert_eq!(shares[3], 500_000);
    }

    /// The exactness has to hold at the top of the ledger, not just at demo sizes.
    /// `u64::MAX / 8` is where the float version stopped terminating, which is how this
    /// case earned its place in the list.
    #[test]
    fn apportionment_never_loses_a_constituent() {
        for total in [0_u64, 1, 3, 7, 1_000_000, u64::MAX / 8, u64::MAX] {
            for weights in [
                vec![1.0, 1.0, 1.0, 1.0],
                vec![0.9, 0.1, 0.0, 0.0],
                vec![1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0, 0.0],
            ] {
                let shares = apportion(total, &weights);
                assert_eq!(
                    shares.iter().sum::<u64>(),
                    total,
                    "lost constituents at total {total} over {weights:?}"
                );
            }
        }
    }

    #[test]
    fn a_cell_knows_how_much_of_it_is_below_the_matter_line() {
        let cell = Cell {
            x0: 0.0,
            y0: 1.0,
            size: 2.0,
        };
        assert_eq!(cell.fraction_below(0.0), 0.0);
        assert_eq!(cell.fraction_below(2.0), 0.5);
        assert_eq!(cell.fraction_below(9.0), 1.0);
    }
}
