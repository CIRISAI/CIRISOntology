//! Rust/WASM Newtonian material-fracture gate for CIRISHolon.
//!
//! The browser owns input and pixels. This crate owns every state transition, contact,
//! cohesive relation, and crack. The 10,000-holon ball and 1,000,000-holon wall retain
//! exact REG+ constituent counts while a fixed resident frontier resolves the impact.

use ciris_sim_core::material::{
    CohesiveBond, CohesiveLaw, IsotropicMaterial, MaterialBinding, RigidChartExport,
};
use ciris_sim_core::regplus::GrossState;
use std::sync::{Mutex, MutexGuard};

pub const BALL_HOLONS: u64 = 10_000;
pub const WALL_HOLONS: u64 = 1_000_000;
pub const ROOT_HOLON: usize = 0;
pub const BALL_HOLON: usize = 1;
pub const WALL_HOLON: usize = 2;
pub const STONE_DESCRIPTOR_HOLON: usize = 3;
pub const BALL_GROSS: GrossState = GrossState::aggregate(BALL_HOLONS, 0, [0, 0]);
pub const WALL_GROSS: GrossState = GrossState::aggregate(WALL_HOLONS, 0, [0, 0]);
pub const SCENE_GROSS: GrossState = BALL_GROSS.combine(WALL_GROSS);

const WALL_COLUMNS: usize = 18;
const WALL_ROWS: usize = 16;
const WALL_NODE_COUNT: usize = WALL_COLUMNS * WALL_ROWS;
const WALL_X: f64 = 7.05;
const WALL_Y: f64 = 1.28;
const WALL_SPACING: f64 = 0.245;
const NODE_RADIUS: f64 = 0.098;
const NODE_MASS: f64 = 0.72;
const BALL_RADIUS: f64 = 0.34;
// The resident mass ratio follows the gross count ratio: the ball is approximately one
// percent of the wall, rather than being enlarged merely to make the demo dramatic.
const BALL_MASS: f64 = 2.1;
const BALL_START_X: f64 = 1.25;
const BALL_START_Y: f64 = 3.18;
const GRAVITY: f64 = 1.8;
const FIXED_STEP: f64 = 1.0 / 600.0;
const MAX_FRAME_STEP: f64 = 1.0 / 20.0;

// A5 — solver damping, named as such. These stabilize the explicit integrator and the
// penalty contact; they are solver configuration with no physics-tier ancestor, and
// they are declared here instead of hiding inline in the stepping loop. Material
// dissipation (the descriptor's `material_damping_ratio`, granite band ζ ~ 5e-4–5e-3)
// is deliberately NOT consumed by this demo's integrator.
const SOLVER_VELOCITY_DAMPING_PER_S: f64 = 0.10;
const SOLVER_CONTACT_STIFFNESS_N_M: f64 = 2_150.0;
const SOLVER_CONTACT_DAMPING_N_S_M: f64 = 13.0;

const STONE_BINDING: MaterialBinding = MaterialBinding {
    subject_holon: WALL_HOLON,
    descriptor_holon: STONE_DESCRIPTOR_HOLON,
    properties: IsotropicMaterial::DEMO_CALIBRATION,
};

#[derive(Clone, Copy, Debug, Default)]
struct Vec2 {
    x: f64,
    y: f64,
}

impl Vec2 {
    const ZERO: Self = Self { x: 0.0, y: 0.0 };

    fn new(x: f64, y: f64) -> Self {
        Self { x, y }
    }

    fn length(self) -> f64 {
        (self.x * self.x + self.y * self.y).sqrt()
    }

    fn dot(self, other: Self) -> f64 {
        self.x * other.x + self.y * other.y
    }

    fn normalized(self) -> Self {
        let length = self.length();
        if length > 1.0e-12 {
            self * (1.0 / length)
        } else {
            Self::new(1.0, 0.0)
        }
    }
}

impl std::ops::Add for Vec2 {
    type Output = Self;
    fn add(self, rhs: Self) -> Self::Output {
        Self::new(self.x + rhs.x, self.y + rhs.y)
    }
}

impl std::ops::Sub for Vec2 {
    type Output = Self;
    fn sub(self, rhs: Self) -> Self::Output {
        Self::new(self.x - rhs.x, self.y - rhs.y)
    }
}

impl std::ops::Mul<f64> for Vec2 {
    type Output = Self;
    fn mul(self, rhs: f64) -> Self::Output {
        Self::new(self.x * rhs, self.y * rhs)
    }
}

impl std::ops::AddAssign for Vec2 {
    fn add_assign(&mut self, rhs: Self) {
        self.x += rhs.x;
        self.y += rhs.y;
    }
}

impl std::ops::SubAssign for Vec2 {
    fn sub_assign(&mut self, rhs: Self) {
        self.x -= rhs.x;
        self.y -= rhs.y;
    }
}

#[derive(Clone, Copy, Debug)]
struct Node {
    position: Vec2,
    velocity: Vec2,
    force: Vec2,
    anchored: bool,
}

#[derive(Clone, Copy, Debug)]
struct Ball {
    position: Vec2,
    velocity: Vec2,
    force: Vec2,
    launched: bool,
}

#[derive(Clone, Debug)]
struct Bond {
    a: usize,
    b: usize,
    relation: CohesiveBond,
    weak_interface: bool,
}

#[derive(Debug)]
struct Simulation {
    nodes: Vec<Node>,
    bonds: Vec<Bond>,
    ball: Ball,
    time: f64,
    impacts: u32,
    peak_contact_force: f64,
    initialized: bool,
}

impl Simulation {
    const fn empty() -> Self {
        Self {
            nodes: Vec::new(),
            bonds: Vec::new(),
            ball: Ball {
                position: Vec2 {
                    x: BALL_START_X,
                    y: BALL_START_Y,
                },
                velocity: Vec2::ZERO,
                force: Vec2::ZERO,
                launched: false,
            },
            time: 0.0,
            impacts: 0,
            peak_contact_force: 0.0,
            initialized: false,
        }
    }

    fn reset(&mut self) {
        debug_assert!(STONE_BINDING.validate().is_ok());
        self.nodes.clear();
        self.bonds.clear();
        self.time = 0.0;
        self.impacts = 0;
        self.peak_contact_force = 0.0;
        self.ball = Ball {
            position: Vec2::new(BALL_START_X, BALL_START_Y),
            velocity: Vec2::ZERO,
            force: Vec2::ZERO,
            launched: false,
        };

        for row in 0..WALL_ROWS {
            for column in 0..WALL_COLUMNS {
                self.nodes.push(Node {
                    position: Vec2::new(
                        WALL_X + column as f64 * WALL_SPACING,
                        WALL_Y + row as f64 * WALL_SPACING,
                    ),
                    velocity: Vec2::ZERO,
                    force: Vec2::ZERO,
                    anchored: column == WALL_COLUMNS - 1,
                });
            }
        }

        let base_law = CohesiveLaw {
            // These are similarity-scaled discrete law values for the visible resident
            // frontier. The descriptor above retains the SI material properties.
            stiffness_n_m: 510.0,
            damping_n_s_m: 2.6,
            peak_force_n: 12.0,
            fracture_energy_j: 0.35,
            // Byerlee-class rock friction is 0.6–0.85; 0.74 is the T4 spec's
            // McClintock–Walsh inversion of the demo strength ratio.
            friction_coefficient: 0.74,
        };

        for row in 0..WALL_ROWS {
            for column in 0..WALL_COLUMNS {
                let a = node_index(column, row);
                if column + 1 < WALL_COLUMNS {
                    self.add_bond(a, node_index(column + 1, row), base_law, column == 8);
                }
                if row + 1 < WALL_ROWS {
                    let flaw = deterministic_flaw(column, row);
                    self.add_bond(a, node_index(column, row + 1), base_law, flaw);
                }
                if column + 1 < WALL_COLUMNS && row + 1 < WALL_ROWS {
                    let crossing_seam = column == 8;
                    if (column + row) % 2 == 0 {
                        self.add_bond(a, node_index(column + 1, row + 1), base_law, crossing_seam);
                    } else {
                        self.add_bond(
                            node_index(column + 1, row),
                            node_index(column, row + 1),
                            base_law,
                            crossing_seam,
                        );
                    }
                }
            }
        }
        self.initialized = true;
    }

    fn add_bond(&mut self, a: usize, b: usize, base: CohesiveLaw, weak: bool) {
        let delta = self.nodes[b].position - self.nodes[a].position;
        let law = if weak {
            base.weakened(0.42, 0.30)
        } else {
            base
        };
        let relation_holon = 10_000 + self.bonds.len();
        let relation = CohesiveBond::new(relation_holon, 100 + a, 100 + b, delta.length(), law)
            .expect("game cohesive law is valid");
        self.bonds.push(Bond {
            a,
            b,
            relation,
            weak_interface: weak,
        });
    }

    fn ensure_initialized(&mut self) {
        if !self.initialized {
            self.reset();
        }
    }

    fn launch(&mut self, target_y: f64, speed: f64) {
        self.reset();
        let target = Vec2::new(WALL_X + 0.65, target_y.clamp(WALL_Y, wall_top()));
        let direction = (target - self.ball.position).normalized();
        self.ball.velocity = direction * speed.clamp(7.0, 18.0);
        self.ball.launched = true;
    }

    fn advance(&mut self, elapsed: f64) {
        self.ensure_initialized();
        if !self.ball.launched {
            return;
        }
        let mut remaining = elapsed.clamp(0.0, MAX_FRAME_STEP);
        while remaining > 1.0e-12 {
            let dt = remaining.min(FIXED_STEP);
            self.substep(dt);
            remaining -= dt;
        }
    }

    fn substep(&mut self, dt: f64) {
        for node in &mut self.nodes {
            node.force = if node.anchored {
                Vec2::ZERO
            } else {
                Vec2::new(0.0, -GRAVITY * NODE_MASS * 0.035)
            };
        }
        self.ball.force = Vec2::new(0.0, -GRAVITY * BALL_MASS);

        for bond in &mut self.bonds {
            let a = self.nodes[bond.a];
            let b = self.nodes[bond.b];
            let delta = b.position - a.position;
            let distance = delta.length();
            if distance <= 1.0e-12 {
                continue;
            }
            let normal = delta * (1.0 / distance);
            let relative_velocity = b.velocity - a.velocity;
            let relative_speed = relative_velocity.dot(normal);
            let magnitude = bond
                .relation
                .axial_force(distance - bond.relation.rest_length_m, relative_speed);
            let force = normal * magnitude;
            self.nodes[bond.a].force += force;
            self.nodes[bond.b].force -= force;

            // A3: Coulomb slider on the closed, partially decohered interface. The
            // BOND owns friction while D < 1 (regime table on CohesiveBond); the
            // contact solver owns post-failure contact.
            let tangential = relative_velocity - normal * relative_speed;
            let tangential_speed = tangential.length();
            if tangential_speed > 1.0e-12 {
                let friction = bond
                    .relation
                    .closed_friction_force(magnitude, tangential_speed);
                if friction > 0.0 {
                    let slide = tangential * (1.0 / tangential_speed);
                    self.nodes[bond.b].force -= slide * friction;
                    self.nodes[bond.a].force += slide * friction;
                }
            }
        }

        let mut contact_force_total = 0.0;
        let mut contact = false;
        for node in &mut self.nodes {
            let delta = node.position - self.ball.position;
            let distance = delta.length();
            let overlap = BALL_RADIUS + NODE_RADIUS - distance;
            if overlap <= 0.0 {
                continue;
            }
            let normal = delta.normalized();
            let separating_speed = (node.velocity - self.ball.velocity).dot(normal);
            let magnitude = (SOLVER_CONTACT_STIFFNESS_N_M * overlap
                - SOLVER_CONTACT_DAMPING_N_S_M * separating_speed)
                .max(0.0);
            let force = normal * magnitude;
            if !node.anchored {
                node.force += force;
            }
            self.ball.force -= force;
            contact_force_total += magnitude;
            contact = true;
        }
        if contact && self.peak_contact_force == 0.0 {
            self.impacts += 1;
        }
        self.peak_contact_force = self.peak_contact_force.max(contact_force_total);

        for node in &mut self.nodes {
            if node.anchored {
                node.velocity = Vec2::ZERO;
                continue;
            }
            node.velocity += node.force * (dt / NODE_MASS);
            node.velocity = node.velocity * (1.0 / (1.0 + SOLVER_VELOCITY_DAMPING_PER_S * dt));
            node.position += node.velocity * dt;
        }
        self.ball.velocity += self.ball.force * (dt / BALL_MASS);
        self.ball.position += self.ball.velocity * dt;
        self.time += dt;
    }

    fn cracked_bonds(&self) -> usize {
        self.bonds
            .iter()
            .filter(|bond| bond.relation.is_broken())
            .count()
    }

    fn maximum_damage(&self) -> f64 {
        self.bonds
            .iter()
            .map(|bond| bond.relation.damage())
            .fold(0.0, f64::max)
    }

    /// A4: the wall's rigid export is the engine's OWN chart over the same holon,
    /// carrying the relation network's damage Record — never a Rapier object (Rapier
    /// stays the limiting-case control). See `RigidChartExport` for the
    /// `repairable_does_not_factor` reading of the tag.
    fn rigid_export(&self) -> RigidChartExport {
        RigidChartExport::over(
            WALL_HOLON,
            WALL_NODE_COUNT as f64 * NODE_MASS,
            self.bonds.iter().map(|bond| &bond.relation),
        )
        .expect("wall rigid chart is valid")
    }
}

fn node_index(column: usize, row: usize) -> usize {
    row * WALL_COLUMNS + column
}

fn wall_top() -> f64 {
    WALL_Y + (WALL_ROWS - 1) as f64 * WALL_SPACING
}

fn deterministic_flaw(column: usize, row: usize) -> bool {
    // Sparse, repeatable weaker relations make this a heterogeneous stone wall rather
    // than an implausibly perfect crystal. The visible centre seam remains the dominant
    // intentionally weak interface.
    (column * 17 + row * 31 + 7).is_multiple_of(43)
}

static SIMULATION: Mutex<Simulation> = Mutex::new(Simulation::empty());

fn simulation() -> MutexGuard<'static, Simulation> {
    SIMULATION
        .lock()
        .unwrap_or_else(|poisoned| poisoned.into_inner())
}

#[no_mangle]
pub extern "C" fn ciris_reset() {
    simulation().reset();
}

#[no_mangle]
pub extern "C" fn ciris_launch(target_y: f64, speed: f64) {
    simulation().launch(target_y, speed);
}

#[no_mangle]
pub extern "C" fn ciris_step(elapsed_seconds: f64) {
    simulation().advance(elapsed_seconds);
}

#[no_mangle]
pub extern "C" fn ciris_node_count() -> u32 {
    WALL_NODE_COUNT as u32
}

#[no_mangle]
pub extern "C" fn ciris_node_x(index: u32) -> f64 {
    simulation()
        .nodes
        .get(index as usize)
        .map_or(0.0, |node| node.position.x)
}

#[no_mangle]
pub extern "C" fn ciris_node_y(index: u32) -> f64 {
    simulation()
        .nodes
        .get(index as usize)
        .map_or(0.0, |node| node.position.y)
}

#[no_mangle]
pub extern "C" fn ciris_node_anchored(index: u32) -> u32 {
    simulation()
        .nodes
        .get(index as usize)
        .map_or(0, |node| node.anchored as u32)
}

#[no_mangle]
pub extern "C" fn ciris_node_terminal_holons(index: u32) -> u32 {
    let base = WALL_HOLONS / WALL_NODE_COUNT as u64;
    let remainder = WALL_HOLONS % WALL_NODE_COUNT as u64;
    (base + u64::from((index as u64) < remainder)) as u32
}

#[no_mangle]
pub extern "C" fn ciris_bond_count() -> u32 {
    let mut sim = simulation();
    sim.ensure_initialized();
    sim.bonds.len() as u32
}

#[no_mangle]
pub extern "C" fn ciris_bond_a(index: u32) -> u32 {
    simulation()
        .bonds
        .get(index as usize)
        .map_or(0, |bond| bond.a as u32)
}

#[no_mangle]
pub extern "C" fn ciris_bond_b(index: u32) -> u32 {
    simulation()
        .bonds
        .get(index as usize)
        .map_or(0, |bond| bond.b as u32)
}

#[no_mangle]
pub extern "C" fn ciris_bond_damage(index: u32) -> f64 {
    simulation()
        .bonds
        .get(index as usize)
        .map_or(0.0, |bond| bond.relation.damage())
}

#[no_mangle]
pub extern "C" fn ciris_bond_is_weak(index: u32) -> u32 {
    simulation()
        .bonds
        .get(index as usize)
        .map_or(0, |bond| bond.weak_interface as u32)
}

#[no_mangle]
pub extern "C" fn ciris_ball_x() -> f64 {
    simulation().ball.position.x
}

#[no_mangle]
pub extern "C" fn ciris_ball_y() -> f64 {
    simulation().ball.position.y
}

#[no_mangle]
pub extern "C" fn ciris_ball_speed() -> f64 {
    simulation().ball.velocity.length()
}

#[no_mangle]
pub extern "C" fn ciris_time() -> f64 {
    simulation().time
}

#[no_mangle]
pub extern "C" fn ciris_cracked_bonds() -> u32 {
    simulation().cracked_bonds() as u32
}

#[no_mangle]
pub extern "C" fn ciris_maximum_damage() -> f64 {
    simulation().maximum_damage()
}

#[no_mangle]
pub extern "C" fn ciris_peak_contact_force() -> f64 {
    simulation().peak_contact_force
}

#[no_mangle]
pub extern "C" fn ciris_impact_count() -> u32 {
    simulation().impacts
}

#[no_mangle]
pub extern "C" fn ciris_wall_holons() -> u32 {
    WALL_HOLONS as u32
}

#[no_mangle]
pub extern "C" fn ciris_ball_holons() -> u32 {
    BALL_HOLONS as u32
}

#[no_mangle]
pub extern "C" fn ciris_wall_rigid_mass() -> f64 {
    let mut sim = simulation();
    sim.ensure_initialized();
    sim.rigid_export().mass_kg
}

#[no_mangle]
pub extern "C" fn ciris_wall_rigid_mean_damage() -> f64 {
    let mut sim = simulation();
    sim.ensure_initialized();
    sim.rigid_export().record.mean_damage
}

#[no_mangle]
pub extern "C" fn ciris_wall_rigid_max_damage() -> f64 {
    let mut sim = simulation();
    sim.ensure_initialized();
    sim.rigid_export().record.max_damage
}

#[no_mangle]
pub extern "C" fn ciris_wall_rigid_broken_bonds() -> u32 {
    let mut sim = simulation();
    sim.ensure_initialized();
    sim.rigid_export().record.broken_count
}

#[no_mangle]
pub extern "C" fn ciris_material_density() -> f64 {
    STONE_BINDING.properties.density_kg_m3
}

#[no_mangle]
pub extern "C" fn ciris_material_young_modulus() -> f64 {
    STONE_BINDING.properties.young_modulus_pa
}

#[no_mangle]
pub extern "C" fn ciris_material_tensile_strength() -> f64 {
    STONE_BINDING.properties.tensile_strength_pa
}

#[no_mangle]
pub extern "C" fn ciris_material_fracture_energy() -> f64 {
    STONE_BINDING.properties.fracture_energy_j_m2
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn resident_frontier_preserves_exact_wall_gross_count() {
        let total: u64 = (0..WALL_NODE_COUNT)
            .map(|index| {
                let base = WALL_HOLONS / WALL_NODE_COUNT as u64;
                let remainder = WALL_HOLONS % WALL_NODE_COUNT as u64;
                base + u64::from((index as u64) < remainder)
            })
            .sum();
        assert_eq!(total, WALL_HOLONS);
        assert_eq!(WALL_GROSS.constituents, WALL_HOLONS);
        assert_eq!(SCENE_GROSS, BALL_GROSS.combine(WALL_GROSS));
        assert_eq!(SCENE_GROSS.constituents, 1_010_000);
    }

    #[test]
    fn centre_throw_impacts_and_produces_a_crack_without_instability() {
        let mut sim = Simulation::empty();
        sim.launch((WALL_Y + wall_top()) * 0.5, 13.8);
        for _ in 0..180 {
            sim.advance(1.0 / 60.0);
        }
        assert!(sim.impacts > 0);
        assert!(sim.cracked_bonds() > 0);
        assert!(
            sim.cracked_bonds() < 64,
            "centre throw should form a local crack, not shatter the wall: {} failures",
            sim.cracked_bonds()
        );
        assert!(sim.ball.position.x.is_finite() && sim.ball.position.y.is_finite());
        assert!(sim
            .nodes
            .iter()
            .all(|node| node.position.x.is_finite() && node.position.y.is_finite()));
    }

    #[test]
    fn subcritical_wall_damage_reaches_the_rigid_export() {
        // A4: pre-load the wall to sub-critical damage (every D strictly below 1) and
        // assert the rigid export DIFFERS from pristine, through the Record tag alone.
        // Dropping the tag from the export makes this test fail: mass, holon, and the
        // crack observable {r | D = 1} are identical between the two walls.
        let mut sim = Simulation::empty();
        sim.reset();
        let pristine = sim.rigid_export();

        for bond in sim.bonds.iter_mut().take(40) {
            let peak = bond.relation.law.opening_at_peak();
            let failure = bond.relation.law.opening_at_failure();
            bond.relation.axial_force(peak + 0.9 * (failure - peak), 0.0);
        }
        assert!(
            sim.bonds.iter().all(|bond| bond.relation.damage() < 1.0),
            "the pre-load must stay sub-critical"
        );

        let loaded = sim.rigid_export();
        assert_eq!(loaded.subject_holon, pristine.subject_holon);
        assert_eq!(loaded.mass_kg, pristine.mass_kg);
        assert_eq!(loaded.record.broken_count, 0);
        assert_ne!(
            loaded, pristine,
            "a wall pre-loaded to 0.9 of critical must not export like a pristine one"
        );
        assert!(loaded.record.mean_damage > 0.0);
    }

    #[test]
    fn reset_is_deterministic() {
        let run = || {
            let mut sim = Simulation::empty();
            sim.launch(3.0, 12.5);
            for _ in 0..120 {
                sim.advance(1.0 / 60.0);
            }
            (
                sim.ball.position.x.to_bits(),
                sim.ball.position.y.to_bits(),
                sim.cracked_bonds(),
            )
        };
        assert_eq!(run(), run());
    }

    #[test]
    fn complete_player_aim_and_speed_envelope_produces_valid_impacts() {
        let target_heights = [
            WALL_Y,
            WALL_Y + (wall_top() - WALL_Y) * 0.25,
            (WALL_Y + wall_top()) * 0.5,
            WALL_Y + (wall_top() - WALL_Y) * 0.75,
            wall_top(),
        ];
        let speeds = [8.0, 13.8, 18.0];

        for target_y in target_heights {
            for speed in speeds {
                let mut sim = Simulation::empty();
                sim.launch(target_y, speed);
                for _ in 0..270 {
                    sim.advance(1.0 / 60.0);
                }
                assert!(
                    sim.impacts > 0,
                    "throw at y={target_y}, speed={speed} missed the wall"
                );
                assert!(
                    sim.ball.position.x.is_finite()
                        && sim.ball.position.y.is_finite()
                        && sim.ball.velocity.x.is_finite()
                        && sim.ball.velocity.y.is_finite(),
                    "throw at y={target_y}, speed={speed} produced a non-finite ball"
                );
                assert!(
                    sim.nodes.iter().all(|node| node.position.x.is_finite()
                        && node.position.y.is_finite()
                        && node.velocity.x.is_finite()
                        && node.velocity.y.is_finite()),
                    "throw at y={target_y}, speed={speed} produced a non-finite wall"
                );
            }
        }
    }
}
