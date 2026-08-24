//! The scene's geometry, and the one combinatorial fact the whole gate rests on.
//!
//! A scene is a `w × h` grid of cells at ONE tier — one declared `g0`, no re-root anywhere
//! (`MESH_DESIGN.md` §1, and `CIRISOntology/Core/GrainFloor.lean`'s
//! `cert_does_not_transport_across_reroot` is why that is a fence rather than a preference).
//!
//! # The fact: an edge colour is a PERFECT MATCHING, and that is what makes sharding free
//!
//! Cell adjacency is the 4-neighbour stencil, radius `r = 1`. Its edges partition into four
//! classes by `(axis, parity of the lower endpoint's coordinate on that axis)`:
//!
//! ```text
//!   colour 0: horizontal edges (x, y)-(x+1, y) with x even
//!   colour 1: horizontal edges (x, y)-(x+1, y) with x odd
//!   colour 2: vertical   edges (x, y)-(x, y+1) with y even
//!   colour 3: vertical   edges (x, y)-(x, y+1) with y odd
//! ```
//!
//! **Within one colour, every cell appears in at most one edge.** That is proved by
//! [`tests::each_colour_is_a_perfect_matching`] over every cell of several grids, and it is
//! the load-bearing property of this design, because it yields both halves of the gate at
//! once:
//!
//! * **applying a colour's edges in any order gives the same answer** — edge `e`'s two writes
//!   touch no cell edge `f` reads, so there is no read-after-write hazard to order;
//! * **partitioning the grid into shards cannot change the answer** — an edge's plan is a
//!   function of its two endpoints' pre-colour values, and which shard owns them is not an
//!   input to that function.
//!
//! The second point is the whole reason `meshed == unsharded` is achievable bit-for-bit
//! rather than approximately. It is also a real constraint the mesh imposes on any solver
//! that wants to ride it, and `MESH_DESIGN.md` states it: a sweep whose writes are visible to
//! later reads *within the same phase* (a true Gauss-Seidel) is not shardable bit-identically,
//! because then shard boundaries become physically visible. Red/black is fine — each colour is
//! a Jacobi phase — and that is what this module encodes.
//!
//! Counts, for the 3D generalisation `MESH_DESIGN.md` §5.1 states: 2D has Δ = 4 and four
//! colours; 3D has Δ = 6 and six, both meeting Vizing's lower bound exactly.

/// Number of edge colours for the 2D 4-neighbour stencil. Δ of the grid graph, and the
/// number of perfect matchings its edges decompose into.
pub const EDGE_COLOURS: usize = 4;

/// Interaction radius of the stencil, in cells. Every dependence bound in this crate is
/// `n * RADIUS` for `n` sub-steps, which is `Core/Locality.lean::iterate_depends_within`.
pub const RADIUS: usize = 1;

/// A `w × h` single-tier scene. Cell `(x, y)` has global index `y * w + x`, and global
/// index order is the canonical order everything in this crate falls back to.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Grid {
    pub w: usize,
    pub h: usize,
}

impl Grid {
    pub const fn new(w: usize, h: usize) -> Self {
        Self { w, h }
    }

    pub const fn len(&self) -> usize {
        self.w * self.h
    }

    pub const fn is_empty(&self) -> bool {
        self.w == 0 || self.h == 0
    }

    #[inline]
    pub const fn index(&self, x: usize, y: usize) -> u32 {
        (y * self.w + x) as u32
    }

    #[inline]
    pub const fn coord(&self, index: u32) -> (usize, usize) {
        let i = index as usize;
        (i % self.w, i / self.w)
    }
}

/// One adjacency, oriented `lo < hi` by GLOBAL CELL INDEX — never by visit order, never by
/// which shard was reached first. The orientation fixes the transfer's sign convention, and
/// mutation `PairOrientedByVisitOrder` is what proves that matters.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Edge {
    pub lo: u32,
    pub hi: u32,
}

impl Edge {
    fn new(a: u32, b: u32) -> Self {
        if a < b {
            Self { lo: a, hi: b }
        } else {
            Self { lo: b, hi: a }
        }
    }
}

/// Every edge of one colour, in ascending `lo` order.
///
/// `colour` is `axis * 2 + parity`: 0/1 are the horizontal matchings, 2/3 the vertical ones.
pub fn edges_of_colour(grid: Grid, colour: usize) -> Vec<Edge> {
    let mut edges = Vec::new();
    if grid.is_empty() {
        return edges;
    }
    let axis = colour / 2;
    let parity = colour % 2;
    if axis == 0 {
        for y in 0..grid.h {
            let mut x = parity;
            while x + 1 < grid.w {
                edges.push(Edge::new(grid.index(x, y), grid.index(x + 1, y)));
                x += 2;
            }
        }
    } else {
        let mut y = parity;
        while y + 1 < grid.h {
            for x in 0..grid.w {
                edges.push(Edge::new(grid.index(x, y), grid.index(x, y + 1)));
            }
            y += 2;
        }
    }
    edges.sort_unstable_by_key(|e| (e.lo, e.hi));
    edges
}

/// A partition of the grid into rectangular shards, and the map from cell to owner.
///
/// The shard shape is an axis-aligned block, which is the 2D form of `MESH_DESIGN.md` §1's
/// "a shard is a complete set of sub-octrees at one level". Blocks are cut on both axes so
/// shard counts are `nx * ny`.
#[derive(Clone, Debug)]
pub struct Partition {
    grid: Grid,
    /// Owning shard of every cell, indexed by global cell index.
    owner: Vec<u32>,
    /// Owned cells of every shard, ascending by global index.
    owned: Vec<Vec<u32>>,
    /// Position of a cell within its owner's `owned` list, indexed by global cell index.
    slot: Vec<u32>,
}

impl Partition {
    /// Cut the grid into `nx * ny` rectangular blocks, as evenly as the dimensions allow.
    pub fn blocks(grid: Grid, nx: usize, ny: usize) -> Self {
        let nx = nx.max(1).min(grid.w.max(1));
        let ny = ny.max(1).min(grid.h.max(1));
        let mut owner = vec![0u32; grid.len()];
        let mut owned = vec![Vec::new(); nx * ny];
        for y in 0..grid.h {
            let by = y * ny / grid.h;
            for x in 0..grid.w {
                let bx = x * nx / grid.w;
                let shard = (by * nx + bx) as u32;
                let cell = grid.index(x, y);
                owner[cell as usize] = shard;
            }
        }
        // Fill `owned` in ascending global index so a shard's local ids are a deterministic
        // function of the partition alone, never of iteration order.
        let mut slot = vec![0u32; grid.len()];
        for cell in 0..grid.len() as u32 {
            let shard = owner[cell as usize] as usize;
            slot[cell as usize] = owned[shard].len() as u32;
            owned[shard].push(cell);
        }
        Self {
            grid,
            owner,
            owned,
            slot,
        }
    }

    /// One shard holding the whole grid. The degenerate partition, used as a control: the
    /// mesh at `single()` must agree with the unsharded reference trivially, and if it does
    /// not, the defect is in the stepper rather than in the sharding.
    pub fn single(grid: Grid) -> Self {
        Self::blocks(grid, 1, 1)
    }

    pub fn grid(&self) -> Grid {
        self.grid
    }

    pub fn shard_count(&self) -> usize {
        self.owned.len()
    }

    #[inline]
    pub fn owner(&self, cell: u32) -> u32 {
        self.owner[cell as usize]
    }

    /// Local holon id of a cell inside its owning shard's arena. Arena id 0 is the root, so
    /// owned cell `k` is holon `k + 1`.
    #[inline]
    pub fn local_id(&self, cell: u32) -> u32 {
        self.slot[cell as usize] + 1
    }

    pub fn owned(&self, shard: usize) -> &[u32] {
        &self.owned[shard]
    }

    /// Every edge of `colour` whose endpoints lie in DIFFERENT shards — the boundary
    /// relations of this partition at this colour, in canonical order.
    pub fn cross_edges(&self, colour: usize) -> Vec<Edge> {
        edges_of_colour(self.grid, colour)
            .into_iter()
            .filter(|e| self.owner(e.lo) != self.owner(e.hi))
            .collect()
    }

    /// Every edge of `colour` whose endpoints lie in the SAME shard.
    pub fn interior_edges(&self, colour: usize) -> Vec<Edge> {
        edges_of_colour(self.grid, colour)
            .into_iter()
            .filter(|e| self.owner(e.lo) == self.owner(e.hi))
            .collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::BTreeSet;

    /// **The load-bearing property.** Within one colour every cell is in at most one edge.
    /// Everything else in this crate — order-freedom of the apply phase, and the claim that
    /// partitioning cannot change the answer — is downstream of this.
    #[test]
    fn each_colour_is_a_perfect_matching() {
        for (w, h) in [(1, 1), (2, 3), (5, 5), (8, 4), (7, 9), (16, 16)] {
            let grid = Grid::new(w, h);
            for colour in 0..EDGE_COLOURS {
                let mut seen = BTreeSet::new();
                for edge in edges_of_colour(grid, colour) {
                    assert!(
                        seen.insert(edge.lo),
                        "{w}x{h} colour {colour}: cell {} is in two edges",
                        edge.lo
                    );
                    assert!(
                        seen.insert(edge.hi),
                        "{w}x{h} colour {colour}: cell {} is in two edges",
                        edge.hi
                    );
                }
            }
        }
    }

    /// The four colours together are exactly the adjacency graph: nothing counted twice,
    /// nothing missed. A colouring that dropped edges would still pass the matching test
    /// while quietly making the scene not interact.
    #[test]
    fn the_four_colours_cover_every_adjacency_exactly_once() {
        for (w, h) in [(2, 3), (5, 5), (8, 4), (7, 9)] {
            let grid = Grid::new(w, h);
            let mut all = BTreeSet::new();
            let mut count = 0;
            for colour in 0..EDGE_COLOURS {
                for edge in edges_of_colour(grid, colour) {
                    assert!(all.insert((edge.lo, edge.hi)), "edge counted twice");
                    count += 1;
                }
            }
            // A w x h 4-neighbour grid has (w-1)*h horizontal and w*(h-1) vertical edges.
            let expected = (w - 1) * h + w * (h - 1);
            assert_eq!(count, expected, "{w}x{h}: wrong edge count");
        }
    }

    /// Edges are oriented by global index, so the orientation is a property of the scene and
    /// not of how the edge list was built.
    #[test]
    fn edges_are_oriented_by_global_index_not_construction_order() {
        let grid = Grid::new(6, 6);
        for colour in 0..EDGE_COLOURS {
            for edge in edges_of_colour(grid, colour) {
                assert!(edge.lo < edge.hi);
            }
        }
    }

    #[test]
    fn a_partition_owns_every_cell_exactly_once() {
        let grid = Grid::new(12, 8);
        for (nx, ny) in [(1, 1), (2, 2), (3, 2), (4, 4)] {
            let part = Partition::blocks(grid, nx, ny);
            let mut total = 0;
            for shard in 0..part.shard_count() {
                for &cell in part.owned(shard) {
                    assert_eq!(part.owner(cell) as usize, shard);
                    total += 1;
                }
            }
            assert_eq!(total, grid.len(), "{nx}x{ny} lost or duplicated cells");
        }
    }

    /// Interior and cross edges partition the colour's edges — no edge is in neither list,
    /// and none is in both. The mesh steps exactly these two lists, so a gap here would be a
    /// silently dropped interaction.
    #[test]
    fn interior_and_cross_edges_partition_the_colour() {
        let grid = Grid::new(10, 10);
        let part = Partition::blocks(grid, 3, 3);
        for colour in 0..EDGE_COLOURS {
            let all = edges_of_colour(grid, colour).len();
            let interior = part.interior_edges(colour).len();
            let cross = part.cross_edges(colour).len();
            assert_eq!(interior + cross, all, "colour {colour} lost edges");
            assert!(cross > 0, "colour {colour} has no boundary to test");
        }
    }
}
