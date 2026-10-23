//! Cross-root correspondence probe: does the existing tier geometry admit a named,
//! composable spatial transport before any state transport is invented?
//!
//! This is deliberately an EXPERIMENT binary, not a new engine primitive. The runtime's
//! current `ciris_set_tier` still constructs a fresh session at the target tier, so this
//! file makes no claim about physical-state holonomy. It tests the smaller prerequisite
//! isolated by the mesh/Pointing review: can a spatial claimant be carried across roots
//! with a receipt that composes exactly?
//!
//! # The construction
//!
//! A spatial claimant is a normalized 2D anchor. It is represented in Q32 fixed point:
//! each axis is `ticks / 2^32`, with `ticks : u32`. This is intentional. A float anchor
//! would make the direct and two-step paths disagree by roundoff and turn an arithmetic
//! identity into a tolerance choice.
//!
//! If a parent domain contains an integer `factor` child domains across each axis, split
//! the anchor into
//!
//! ```text
//! parent anchor --split(factor)--> (child-region address, child-local anchor)
//! ```
//!
//! by Euclidean division of `ticks * factor` by `2^32`. The quotient is the named region
//! in the parent; the remainder is the anchor in the re-rooted child. The receipt is
//! invertible exactly, and receipts compose exactly:
//!
//! ```text
//! Sandbox -> Grain -> Crystal == Sandbox -> Crystal
//! ```
//!
//! for every Q32 anchor, whenever both factors exist. The adjacent Grain/Sandbox and
//! Crystal/Grain relations are already `Reroot::OneTerminalHolon`; the direct
//! Crystal/Sandbox relation is only `Contained`, so the direct side below is an ADDRESS
//! refinement of the sandbox domain, not a claim that the sandbox chart already carries
//! one-micrometre terminal cells.
//!
//! # Pointing diagnostic
//!
//! The clean value is not fitted. The named map is the receipt round-trip and the named
//! comparator is identity. `join(split(a)) = a` and direct = composed are therefore the
//! plumb lines. A planted wrong factor must break the second equality.

use holon_sandbox::tier::{reroot, tier, Reroot, TierId};

const Q32_SCALE: u128 = 1_u128 << 32;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
struct Anchor {
    ticks: [u32; 2],
}

impl Anchor {
    const fn from_ticks(x: u32, y: u32) -> Self {
        Self { ticks: [x, y] }
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
struct Receipt {
    /// Number of child-root domains across one parent-domain axis.
    factor: u64,
    /// Which child-sized region of the parent contains the anchor.
    cell: [u64; 2],
    /// The same claimant, re-expressed in the selected child root.
    local: Anchor,
}

/// Integer number of child ROOT DOMAINS across the parent root, when that statement is
/// geometrically exact to the tier table's own tolerance. This is not the same claim as
/// `tier::reroot`: `reroot` asks how the child domain sits against the PARENT TERMINAL
/// grain; this function asks whether the whole parent domain can be addressed in
/// child-root-sized regions. They coincide on `OneTerminalHolon` adjacencies and need not
/// coincide on a skipped tier.
fn address_factor(child: TierId, parent: TierId) -> Option<u64> {
    if child.index() >= parent.index() {
        return None;
    }
    let child = tier(child);
    let parent = tier(parent);
    if !(child.domain_m.is_finite()
        && parent.domain_m.is_finite()
        && child.domain_m > 0.0
        && parent.domain_m > 0.0)
    {
        return None;
    }
    let ratio = parent.domain_m / child.domain_m;
    if !(ratio.is_finite() && ratio >= 1.0 && ratio <= u64::MAX as f64) {
        return None;
    }
    let rounded = ratio.round();
    let relative = (ratio - rounded).abs() / rounded.max(1.0);
    if relative > 1.0e-9 {
        return None;
    }
    Some(rounded as u64)
}

fn split_axis(ticks: u32, factor: u64) -> Option<(u64, u32)> {
    if factor == 0 {
        return None;
    }
    let scaled = (ticks as u128).checked_mul(factor as u128)?;
    let cell = scaled / Q32_SCALE;
    let local = scaled % Q32_SCALE;
    Some((u64::try_from(cell).ok()?, u32::try_from(local).ok()?))
}

fn split(anchor: Anchor, factor: u64) -> Option<Receipt> {
    let (x, lx) = split_axis(anchor.ticks[0], factor)?;
    let (y, ly) = split_axis(anchor.ticks[1], factor)?;
    Some(Receipt {
        factor,
        cell: [x, y],
        local: Anchor::from_ticks(lx, ly),
    })
}

fn correspondence(child: TierId, parent: TierId, anchor: Anchor) -> Option<Receipt> {
    split(anchor, address_factor(child, parent)?)
}

/// Compose `parent -> middle` with `middle -> child`. The second receipt must have been
/// taken from the first receipt's `local` anchor; the caller owns that typing discipline
/// in this tiny experiment, and the tests exercise it both honestly and with a mutant.
fn compose(outer: Receipt, inner: Receipt) -> Option<Receipt> {
    let factor = outer.factor.checked_mul(inner.factor)?;
    let mut cell = [0_u64; 2];
    for (axis, slot) in cell.iter_mut().enumerate() {
        *slot = outer.cell[axis]
            .checked_mul(inner.factor)?
            .checked_add(inner.cell[axis])?;
    }
    Some(Receipt {
        factor,
        cell,
        local: inner.local,
    })
}

fn join_axis(cell: u64, local: u32, factor: u64) -> Option<u32> {
    if factor == 0 || cell >= factor {
        return None;
    }
    let numerator = (cell as u128)
        .checked_mul(Q32_SCALE)?
        .checked_add(local as u128)?;
    let factor128 = factor as u128;
    if numerator % factor128 != 0 {
        return None;
    }
    u32::try_from(numerator / factor128).ok()
}

/// Inverse of `split` on receipts that actually came from a Q32 anchor.
fn join(receipt: Receipt) -> Option<Anchor> {
    Some(Anchor::from_ticks(
        join_axis(receipt.cell[0], receipt.local.ticks[0], receipt.factor)?,
        join_axis(receipt.cell[1], receipt.local.ticks[1], receipt.factor)?,
    ))
}

fn relation_name(child: TierId, parent: TierId) -> &'static str {
    match reroot(child, parent) {
        Some(Reroot::OneTerminalHolon { .. }) => "one-terminal-holon",
        Some(Reroot::WholeMultiple { .. }) => "whole-multiple",
        Some(Reroot::Contained { .. }) => "contained",
        None => "none",
    }
}

fn main() {
    let anchor = Anchor::from_ticks(0x1357_9bdf, 0x2468_ace0);

    let sandbox_to_grain = correspondence(TierId::Grain, TierId::Sandbox, anchor)
        .expect("sandbox -> grain address correspondence");
    let grain_to_crystal = correspondence(
        TierId::Crystal,
        TierId::Grain,
        sandbox_to_grain.local,
    )
    .expect("grain -> crystal address correspondence");
    let composed = compose(sandbox_to_grain, grain_to_crystal)
        .expect("composed sandbox -> crystal correspondence");
    let direct = correspondence(TierId::Crystal, TierId::Sandbox, anchor)
        .expect("direct sandbox -> crystal address correspondence");

    println!("REROOT CORRESPONDENCE PROBE");
    println!(
        "grain/sandbox: {} ; crystal/grain: {} ; crystal/sandbox: {}",
        relation_name(TierId::Grain, TierId::Sandbox),
        relation_name(TierId::Crystal, TierId::Grain),
        relation_name(TierId::Crystal, TierId::Sandbox),
    );
    println!(
        "factors: sandbox->grain={} grain->crystal={} sandbox->crystal={}",
        sandbox_to_grain.factor, grain_to_crystal.factor, direct.factor
    );
    println!("anchor:   {:?}", anchor);
    println!("composed: {:?}", composed);
    println!("direct:   {:?}", direct);

    if composed != direct {
        eprintln!("KILLED: the named two-step address transport is path-dependent");
        std::process::exit(1);
    }
    if join(composed) != Some(anchor) {
        eprintln!("KILLED: closed address transport does not return to the claimant");
        std::process::exit(1);
    }

    println!("FLAT: direct == composed and the closed Q32 address loop is identity");
    println!("SCOPE: spatial correspondence only; runtime state re-root still resets");
}

#[cfg(test)]
mod tests {
    use super::*;

    const ANCHORS: [Anchor; 6] = [
        Anchor::from_ticks(0, 0),
        Anchor::from_ticks(1, u32::MAX),
        Anchor::from_ticks(u32::MAX, 1),
        Anchor::from_ticks(0x1357_9bdf, 0x2468_ace0),
        Anchor::from_ticks(0x8000_0000, 0x7fff_ffff),
        Anchor::from_ticks(u32::MAX, u32::MAX),
    ];

    #[test]
    fn the_two_adjacent_reroots_are_the_existing_exact_kind() {
        assert!(matches!(
            reroot(TierId::Grain, TierId::Sandbox),
            Some(Reroot::OneTerminalHolon { .. })
        ));
        assert!(matches!(
            reroot(TierId::Crystal, TierId::Grain),
            Some(Reroot::OneTerminalHolon { .. })
        ));
        assert!(matches!(
            reroot(TierId::Crystal, TierId::Sandbox),
            Some(Reroot::Contained { .. })
        ));
    }

    #[test]
    fn the_address_factors_are_the_geometry_not_fitted_numbers() {
        assert_eq!(address_factor(TierId::Grain, TierId::Sandbox), Some(1_200));
        assert_eq!(address_factor(TierId::Crystal, TierId::Grain), Some(500));
        assert_eq!(
            address_factor(TierId::Crystal, TierId::Sandbox),
            Some(600_000)
        );
        assert_eq!(1_200_u64 * 500, 600_000);
    }

    #[test]
    fn a_receipt_round_trip_is_exact_identity() {
        for anchor in ANCHORS {
            for factor in [1_u64, 2, 3, 500, 1_200, 600_000] {
                let receipt = split(anchor, factor).expect("factor is nonzero");
                assert_eq!(join(receipt), Some(anchor), "{anchor:?} at factor {factor}");
            }
        }
    }

    #[test]
    fn crystal_grain_sandbox_is_exactly_path_independent() {
        for anchor in ANCHORS {
            let sg = correspondence(TierId::Grain, TierId::Sandbox, anchor).unwrap();
            let gc = correspondence(TierId::Crystal, TierId::Grain, sg.local).unwrap();
            let via_grain = compose(sg, gc).unwrap();
            let direct = correspondence(TierId::Crystal, TierId::Sandbox, anchor).unwrap();
            assert_eq!(via_grain, direct, "path moved at {anchor:?}");
            assert_eq!(join(via_grain), Some(anchor), "loop moved at {anchor:?}");
        }
    }

    #[test]
    fn the_flatness_gate_has_teeth_wrong_middle_factor_is_caught() {
        let anchor = Anchor::from_ticks(0x1357_9bdf, 0x2468_ace0);
        let sg = correspondence(TierId::Grain, TierId::Sandbox, anchor).unwrap();
        let honest_gc = correspondence(TierId::Crystal, TierId::Grain, sg.local).unwrap();
        let direct = correspondence(TierId::Crystal, TierId::Sandbox, anchor).unwrap();
        assert_eq!(compose(sg, honest_gc).unwrap(), direct);

        // MUTANT: the grain claims 501 crystal-root domains across instead of the 500
        // derived from the tier table. Conservation-style checks could still be written
        // around that wrong choice; path conformance cannot.
        let mutant_gc = split(sg.local, honest_gc.factor + 1).unwrap();
        assert_ne!(
            compose(sg, mutant_gc).unwrap(),
            direct,
            "the planted wrong correspondence factor escaped the path gate"
        );
    }

    #[test]
    fn nonintegral_cross_root_addressing_refuses_instead_of_rounding() {
        assert_eq!(address_factor(TierId::Galactic, TierId::Cosmic), None);
    }
}
