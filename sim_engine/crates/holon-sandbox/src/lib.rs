//! CIRISHolon sandbox: sand, in a box, at every zoom tier of one recursive holon.
//!
//! The browser owns pointer input and pixels. This crate owns every holon, every
//! materialization, every contact, and every certificate. Zoom is not a rendering
//! trick: each tier is a re-rooted [`ciris_sim_core::runtime::RuntimeArena`] with its
//! own declared grain constant, and the certificate says whether the coarse view is
//! honest at that tier or refuses.
//!
//! # The WebAssembly boundary
//!
//! JavaScript reads FLAT BUFFERS out of linear memory, not one call per field. The
//! shipped `holon-ball-game` exports a scalar getter per node coordinate, which is
//! clear at 288 nodes and is thousands of boundary crossings per frame at four
//! thousand. Everything per-frame here is packed into two `f32` arrays whose pointers
//! JavaScript reads once; everything per-event is a scalar; everything textual is a
//! single UTF-8 blob built once from the Rust tier table, so the words a reader sees
//! are the ones the engine holds.

pub mod chart;
pub mod incremental;
pub mod scene;
pub mod sim;
pub mod tier;

use std::sync::{Mutex, MutexGuard, OnceLock};

use scene::LawRefusal;
use sim::Session;
use tier::{Evaluator, Ledger, Refusal, TierId};

/// Floats per node in the render buffer: x, y, radius, anchored, speed.
pub const NODE_STRIDE: usize = 5;
/// Floats per relation in the render buffer: ax, ay, bx, by, damage.
pub const BOND_STRIDE: usize = 5;

struct World {
    session: Session,
    tier: TierId,
    grading: f64,
    /// Per-frame solver work budget, in node-substeps. Owned here so it survives the
    /// re-root a zoom or a throw performs.
    work_budget: usize,
    nodes: Vec<f32>,
    bonds: Vec<f32>,
    text: Vec<u8>,
}

impl World {
    fn new() -> Self {
        let mut world = Self {
            session: Session::new(TierId::Sandbox),
            tier: TierId::Sandbox,
            grading: sim::GRADING,
            work_budget: sim::SUBSTEP_WORK_BUDGET,
            nodes: Vec::new(),
            bonds: Vec::new(),
            text: Vec::new(),
        };
        world.text = describe_tiers().into_bytes();
        world
    }

    fn publish(&mut self) {
        let nodes = self.session.nodes();
        self.nodes.clear();
        self.nodes.reserve(nodes.len() * NODE_STRIDE);
        for i in 0..nodes.len() {
            let speed = (nodes.velocity[i][0] * nodes.velocity[i][0]
                + nodes.velocity[i][1] * nodes.velocity[i][1])
                .sqrt();
            self.nodes.push(nodes.position[i][0] as f32);
            self.nodes.push(nodes.position[i][1] as f32);
            self.nodes.push(nodes.radius_m[i] as f32);
            self.nodes.push(if nodes.anchored[i] { 1.0 } else { 0.0 });
            self.nodes.push(speed as f32);
        }

        let relations = self.session.relations();
        self.bonds.clear();
        self.bonds.reserve(relations.len() * BOND_STRIDE);
        for (index, ends) in relations.ends.iter().enumerate() {
            let [a, b] = *ends;
            self.bonds.push(nodes.position[a][0] as f32);
            self.bonds.push(nodes.position[a][1] as f32);
            self.bonds.push(nodes.position[b][0] as f32);
            self.bonds.push(nodes.position[b][1] as f32);
            self.bonds.push(relations.bonds[index].damage() as f32);
        }
    }
}

fn world() -> MutexGuard<'static, World> {
    static WORLD: OnceLock<Mutex<World>> = OnceLock::new();
    WORLD
        .get_or_init(|| Mutex::new(World::new()))
        .lock()
        .unwrap_or_else(|poisoned| poisoned.into_inner())
}

/// Escape the few characters a JSON string may not carry raw. The tier table's prose is
/// written in this repository and contains none of them today; the function exists so
/// that stays true of prose written later, rather than depending on it.
fn json_escape(text: &str) -> String {
    let mut out = String::with_capacity(text.len());
    for character in text.chars() {
        match character {
            '"' => out.push_str("\\\""),
            '\\' => out.push_str("\\\\"),
            '\n' => out.push_str("\\n"),
            '\r' => out.push_str("\\r"),
            '\t' => out.push_str("\\t"),
            control if (control as u32) < 0x20 => {
                out.push_str(&format!("\\u{:04x}", control as u32));
            }
            other => out.push(other),
        }
    }
    out
}

/// A finite number as JSON, or `null`. JSON has no `NaN`, and the gauge tier's grain
/// and domain are deliberately not numbers — writing `NaN` would take the whole table
/// down with it, and writing a zero would be inventing a length the tier does not have.
fn json_number(value: f64) -> String {
    if value.is_finite() {
        format!("{value:e}")
    } else {
        "null".into()
    }
}

/// The tier table as JSON, built from the Rust values so the page cannot drift from the
/// engine. Hand-rolled rather than pulled in as a dependency: this is one array of flat
/// records emitted once at start-up, and a serialization crate in a browser module that
/// is otherwise `ciris-sim-core` and nothing else is not worth the bytes.
fn describe_tiers() -> String {
    let mut out = String::from("[");
    for (index, tier) in tier::tiers().into_iter().enumerate() {
        if index > 0 {
            out.push(',');
        }
        let (evaluator, refusal) = match tier.evaluator {
            Evaluator::GaugePlaquette => ("exact plaquette", ""),
            Evaluator::GranularContact => ("granular contact", ""),
            Evaluator::Cohesive => ("cohesive relations", ""),
            Evaluator::Unavailable(Refusal::NoValidatedEvaluator) => (
                "none",
                "No validated evaluator exists at this tier in this repository. The \
                 crystal tier is specification-only: there are no force constants in \
                 the tree, and the density-functional calculation that would supply \
                 them is still running. The cell geometry is published measurement, \
                 which is data; running dynamics on it would be a number with no \
                 ancestor.",
            ),
            Evaluator::Unavailable(Refusal::NoGravityChart) => (
                "none",
                "This engine has no certified gravity. Its relativity chart is flat by \
                 design, and its own integration frame says every scene with weight is \
                 outside that certificate until the curved tier lands. So this tier has \
                 an exact ledger and no dynamics, and the honest thing is to show you \
                 the first and refuse the second.",
            ),
        };
        // The gauge tier has no length, so "this tier counted in atoms" is not a
        // question about it — the overflow factor comes back non-finite and the honest
        // answer is that the question does not apply, not a token spelling NaN.
        let atoms = match tier.ledger_in_atoms() {
            Ledger::Fits { constituents, .. } => format!("{constituents}"),
            Ledger::OverflowsConstituents { factor } | Ledger::OverflowsGrainUnits { factor }
                if factor.is_finite() =>
            {
                format!("over:{factor:e}")
            }
            _ => "n/a".into(),
        };
        out.push_str(&format!(
            "{{\"name\":\"{}\",\"plain\":\"{}\",\"g0\":{},\"domain\":{},\
             \"root\":{},\"constituents\":{},\"terminal\":\"{}\",\"evaluator\":\"{}\",\
             \"refusal\":\"{}\",\"required\":{},\"lch\":{},\"atoms\":\"{}\"}}",
            json_escape(tier.name),
            json_escape(tier.plain),
            json_number(tier.g0_m),
            json_number(tier.domain_m),
            tier.root_grain_units,
            tier.constituents,
            json_escape(tier.terminal),
            evaluator,
            json_escape(refusal),
            json_number(tier.required_spacing_m().unwrap_or(f64::NAN)),
            json_number(tier.characteristic_length_m().unwrap_or(f64::NAN)),
            atoms,
        ));
    }
    out.push(']');
    out
}

/// Pointer to the tier-table JSON in linear memory, and its length in bytes.
#[no_mangle]
pub extern "C" fn ciris_text_ptr() -> *const u8 {
    world().text.as_ptr()
}

#[no_mangle]
pub extern "C" fn ciris_text_len() -> u32 {
    world().text.len() as u32
}

/// Move to a tier. Re-roots the scene: a new arena with that tier's own grain constant.
#[no_mangle]
pub extern "C" fn ciris_set_tier(index: u32) {
    let Some(id) = TierId::from_index(index) else {
        return;
    };
    let mut world = world();
    let grading = world.grading;
    let budget = world.work_budget;
    world.tier = id;
    world.session = Session::with_grading(id, grading);
    world.session.set_work_budget(budget);
    world.publish();
}

#[no_mangle]
pub extern "C" fn ciris_tier() -> u32 {
    world().tier.index()
}

/// How fast the resolution demand relaxes with distance from the throw. Smaller demands
/// a finer frontier over a wider area, which is the control that makes the certified
/// frontier visible as a thing with a cost.
#[no_mangle]
pub extern "C" fn ciris_set_grading(grading: f64) {
    let mut world = world();
    world.grading = grading.clamp(0.05, 8.0);
}

#[no_mangle]
pub extern "C" fn ciris_grading() -> f64 {
    world().grading
}

/// Throw at `(aim_x, aim_y)` in domain fractions, at `speed` in 0..1.
#[no_mangle]
pub extern "C" fn ciris_throw(aim_x: f64, aim_y: f64, speed: f64) {
    let mut world = world();
    let id = world.tier;
    let grading = world.grading;
    // A throw re-roots the tier, so each one is certified from the root rather than
    // accumulated on top of the last throw's frontier. Replay is then a function of the
    // aim alone, which is what makes the same throw twice the same throw.
    let budget = world.work_budget;
    world.session = Session::with_grading(id, grading);
    world.session.set_work_budget(budget);
    world.session.throw(aim_x, aim_y, speed);
    world.publish();
}

#[no_mangle]
pub extern "C" fn ciris_step(elapsed_seconds: f64) {
    let mut world = world();
    world.session.step(elapsed_seconds);
    world.publish();
}

#[no_mangle]
pub extern "C" fn ciris_node_ptr() -> *const f32 {
    world().nodes.as_ptr()
}

#[no_mangle]
pub extern "C" fn ciris_node_count() -> u32 {
    (world().nodes.len() / NODE_STRIDE) as u32
}

#[no_mangle]
pub extern "C" fn ciris_bond_ptr() -> *const f32 {
    world().bonds.as_ptr()
}

#[no_mangle]
pub extern "C" fn ciris_bond_count() -> u32 {
    (world().bonds.len() / BOND_STRIDE) as u32
}

/// Verdict code: 0 idle, 1 certified, 2 grain floor, 3 refinement unavailable,
/// 4 no evaluator, 5 no gravity chart, 6 budget exhausted.
#[no_mangle]
pub extern "C" fn ciris_verdict() -> u32 {
    world().session.verdict().code()
}

#[no_mangle]
pub extern "C" fn ciris_holons() -> u32 {
    world().session.arena().len() as u32
}

#[no_mangle]
pub extern "C" fn ciris_materializations() -> u32 {
    world().session.materializations() as u32
}

#[no_mangle]
pub extern "C" fn ciris_rounds() -> u32 {
    world().session.rounds() as u32
}

/// Set the solver's per-frame work budget, in node-substeps.
///
/// The engine cannot time itself on `wasm32-unknown-unknown`, so the host — which has a
/// clock — measures the frame and moves this toward its target. Nothing certified
/// depends on it: it changes how much SIMULATED time one frame buys, and the honest
/// consequence of that is reported by [`ciris_slow_motion`].
#[no_mangle]
pub extern "C" fn ciris_set_work_budget(budget: u32) {
    let mut world = world();
    world.work_budget = budget as usize;
    world.session.set_work_budget(budget as usize);
}

#[no_mangle]
pub extern "C" fn ciris_work_budget() -> u32 {
    world().work_budget as u32
}

#[no_mangle]
pub extern "C" fn ciris_substeps() -> u32 {
    world().session.substeps() as u32
}

#[no_mangle]
pub extern "C" fn ciris_impulse() -> f64 {
    world().session.impulse_n_s()
}

#[no_mangle]
pub extern "C" fn ciris_peak_contact() -> f64 {
    world().session.peak_contact_n()
}

#[no_mangle]
pub extern "C" fn ciris_disturbance() -> f64 {
    world().session.disturbance_m()
}

#[no_mangle]
pub extern "C" fn ciris_cracked() -> u32 {
    world().session.relations().cracked() as u32
}

#[no_mangle]
pub extern "C" fn ciris_slow_motion() -> f64 {
    world().session.slow_motion()
}

#[no_mangle]
pub extern "C" fn ciris_softening() -> f64 {
    world().session.softening_factor()
}

#[no_mangle]
pub extern "C" fn ciris_dt() -> f64 {
    world().session.dt_s()
}

#[no_mangle]
pub extern "C" fn ciris_domain() -> f64 {
    world().session.tier.domain_m
}

#[no_mangle]
pub extern "C" fn ciris_projectile_x() -> f64 {
    world().session.projectile().position[0]
}

#[no_mangle]
pub extern "C" fn ciris_projectile_y() -> f64 {
    world().session.projectile().position[1]
}

#[no_mangle]
pub extern "C" fn ciris_projectile_r() -> f64 {
    world().session.projectile().radius_m
}

#[no_mangle]
pub extern "C" fn ciris_projectile_live() -> u32 {
    u32::from(world().session.projectile().live)
}

/// 0 none, 1 the homogenizer refused a cohesive law at this frontier's spacing (so the
/// relations are contact-only), 2 the tier declares no material chart.
#[no_mangle]
pub extern "C" fn ciris_law_refusal() -> u32 {
    match world().session.law_refusal() {
        None => 0,
        Some(LawRefusal::UnderResolved) => 1,
        Some(LawRefusal::NoMaterial) => 2,
    }
}

/// How many times over the REG+ ledger's `u64` this tier's domain would be if it were
/// counted in ATOMS instead of its own grain. Zero means it fits.
///
/// This is the zoom-out refusal, computed rather than asserted: the sandbox holds
/// 6.6e8 grains, which is 3.4e27 atoms, which is 1.9e8 times more than the ledger can
/// represent — and `GrossState::checked_combine` returns `None` rather than a wrong
/// number.
#[no_mangle]
pub extern "C" fn ciris_atom_overflow() -> f64 {
    match world().session.tier.ledger_in_atoms() {
        Ledger::Fits { .. } => 0.0,
        Ledger::OverflowsConstituents { factor } => factor,
        Ledger::OverflowsGrainUnits { factor } => factor,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use sim::Verdict;

    #[test]
    fn the_tier_table_reaches_the_browser_as_the_engine_holds_it() {
        let text = describe_tiers();
        assert!(text.starts_with('['), "{text}");
        assert!(text.ends_with(']'));
        for tier in tier::tiers() {
            assert!(text.contains(tier.name), "the tier table lost {}", tier.name);
            assert!(
                text.contains(tier.terminal),
                "the tier table lost what {}'s terminal holon is",
                tier.name
            );
        }
        // The refusals have to survive the trip, or the demo's most honest feature is
        // the one that silently does not ship.
        assert!(text.contains("No validated evaluator exists"));
        assert!(text.contains("no certified gravity"));
        // JSON has no NaN. The gauge tier has no grain and no domain, and both of those
        // must arrive as `null` rather than as a token that takes the table down.
        assert!(!text.contains("NaN"), "the tier table emitted a bare NaN");
        assert!(text.contains("\"g0\":null"), "the gauge tier must have no length");
    }

    /// Every exported function takes the world lock for the duration of its own call
    /// and no longer, so two of them may appear in one expression. Writing
    /// `assert_eq!(world().nodes.len(), ciris_node_count() ...)` holds the first guard
    /// across the second lock and deadlocks the test binary — silently, as a hang.
    /// The buffers are therefore read into locals first, which is also what the
    /// JavaScript side does.
    #[test]
    fn the_frame_buffers_are_packed_at_their_declared_stride() {
        ciris_set_tier(TierId::Sandbox.index());
        ciris_throw(0.5, 0.4, 0.6);
        let nodes = ciris_node_count() as usize;
        assert!(nodes > 0);
        assert_eq!(world().nodes.len(), nodes * NODE_STRIDE);
        let bonds = ciris_bond_count() as usize;
        assert_eq!(world().bonds.len(), bonds * BOND_STRIDE);
        assert_eq!(ciris_verdict(), Verdict::Certified.code());
        ciris_step(1.0 / 60.0);
        let stepped = ciris_node_count() as usize;
        assert_eq!(world().nodes.len(), stepped * NODE_STRIDE);
    }

    #[test]
    fn the_zoom_out_refusal_is_computed_and_reaches_the_browser() {
        ciris_set_tier(TierId::Sandbox.index());
        let factor = ciris_atom_overflow();
        assert!(
            (1.0e8..1.0e9).contains(&factor),
            "the sandbox in atoms should be ~1.9e8x over the ledger, got {factor:e}"
        );
        ciris_set_tier(TierId::Grain.index());
        assert_eq!(
            ciris_atom_overflow(),
            0.0,
            "one grain of sand IS countable in atoms"
        );
    }

    #[test]
    fn every_tier_can_be_selected_and_thrown_at() {
        for id in TierId::ALL {
            ciris_set_tier(id.index());
            assert_eq!(ciris_tier(), id.index());
            ciris_throw(0.5, 0.4, 0.6);
            for _ in 0..10 {
                ciris_step(1.0 / 60.0);
            }
            assert!(ciris_holons() >= 1);
            assert!(ciris_impulse().is_finite());
        }
    }
}
