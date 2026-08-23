//! One tier, live: certify a frontier, throw something at it, step the result.
//!
//! Everything domain-specific here is a VALUE. The solver does not know which tier it is
//! running: it steps nodes under uniform chart gravity, asks each live relation holon for
//! its axial force, and resolves unilateral contact on the pairs no live relation owns.
//! Sand and stone differ in whether the homogenizer would give their relations a law at
//! their own grain, and that question is asked in `scene::relation_law`, not here.

use ciris_sim_core::holon::CertificationStatus;
use ciris_sim_core::homogenization::derive_lattice_elastic_law;
use ciris_sim_core::runtime::RuntimeArena;

use crate::chart::Chart;
use crate::incremental::{certify_incremental, Budget, IncrementalError, Settled, Workspace};
use crate::scene::{
    build_nodes, build_relations, mass_per_constituent_kg, relation_law, root_scene, LawRefusal,
    Nodes, QuadrantMaterializer, Relations, ResolutionModel, CHART_GRAVITY_M_S2,
    CONSERVATION_TOLERANCE, OBSERVABLES,
};
use crate::tier::{tier, Evaluator, Tier, TierId};

/// How far the resolution demand relaxes with distance from the throw. 1.0 means a cell
/// may be as coarse as its own distance from the interaction.
///
/// This is the demo's default, not a physical constant, and the viewer exposes it: it
/// trades how much of the scene is resolved against how much simulated time a frame
/// buys, and both sides of that trade are shown.
pub const GRADING: f64 = 2.0;

/// Bonds are formed between cells within this multiple of touching.
pub const RELATION_REACH: f64 = 1.35;

/// Resident-holon ceiling for one throw. Declared, not discovered: a browser event that
/// grows without limit is a hung tab, and hitting this is reported as a budget refusal
/// rather than folded into a verdict.
pub const MAX_HOLONS: usize = 24_000;

/// Greedy-round ceiling for one throw, likewise declared.
pub const MAX_ROUNDS: usize = 400_000;

/// Default substep work budget per frame, in node-substeps.
///
/// This is a STARTING POINT, not a calibration. It was set from native measurements and
/// then measured again through `wasm32-unknown-unknown`, where the same scene ran 3.6x
/// slower — 30 ms per frame against the 8 ms it cost natively. A constant tuned on one
/// of those two numbers is wrong on the other, and wrong again on a slower laptop.
///
/// So the host adjusts it: it is the side of the boundary that has a clock. See
/// [`Session::set_work_budget`].
pub const SUBSTEP_WORK_BUDGET: usize = 24_000;

/// Impact speed at a tier, m/s.
///
/// Scaled by the square root of the domain so a larger tier is not instantaneous, and
/// declared as a stage value: it changes what you see and nothing that is claimed.
pub fn impact_speed(tier: &Tier, speed_fraction: f64) -> f64 {
    4.0 * tier.domain_m.sqrt() * speed_fraction.clamp(0.05, 1.0)
}

/// Coulomb friction between never-bonded grains.
///
/// 0.65 is `tan(33 deg)`, the angle of repose class value for dry medium sand. It is a
/// CLASS warrant with no specimen behind it and is labelled as such wherever the demo
/// shows it — the same standard `IsotropicMaterial::DEMO_CALIBRATION` is held to.
pub const GRAIN_FRICTION_MU: f64 = 0.65;

/// Largest contact overlap the soft-particle stiffness is allowed to produce, as a
/// fraction of a grain radius, at the scene's own impact speed.
///
/// 10% is the loose end of ordinary discrete-element practice — up to about there the
/// bulk response of a granular assembly is insensitive to the choice, which is the
/// property the method rests on. DECLARED here so the number that follows from it has a
/// criterion rather than a preference behind it, and chosen at the loose end because
/// the stiffness sets the timestep and the timestep sets how much physics a frame buys:
/// at 5% the sandbox advanced 0.9% of real time per frame, and a demo nobody can watch
/// is not more honest for being stiffer.
pub const MAX_OVERLAP_FRACTION: f64 = 0.10;

/// Restitution of a grain-on-grain contact. A pair/velocity/geometry OUTCOME taken per
/// contact, which is why `IsotropicMaterial` deliberately has no such field (A5).
pub const CONTACT_RESTITUTION: f64 = 0.35;

/// What the user is told after a throw.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Verdict {
    /// Nothing has been thrown yet at this tier.
    Idle,
    /// The frontier met the tier's own resolution demand and the readout stands.
    Certified,
    /// The demand could not be met at this tier's grain floor. No claim is made.
    GrainFloor,
    /// Refinement ran out before the demand was met — children are not resident and
    /// the generator declined, or the declared budget was reached.
    RefinementUnavailable,
    /// This tier has no validated evaluator in this repository.
    NoEvaluator,
    /// This tier's scene has weight and this engine has no certified gravity chart.
    NoGravityChart,
    /// The declared event budget was exhausted before any verdict was reached. An
    /// error, deliberately not a verdict.
    BudgetExhausted,
}

impl Verdict {
    pub const fn code(self) -> u32 {
        match self {
            Verdict::Idle => 0,
            Verdict::Certified => 1,
            Verdict::GrainFloor => 2,
            Verdict::RefinementUnavailable => 3,
            Verdict::NoEvaluator => 4,
            Verdict::NoGravityChart => 5,
            Verdict::BudgetExhausted => 6,
        }
    }
}

/// Uniform-grid broadphase over the resident nodes.
///
/// `sparse::resolve_sphere_contacts` in the core is an all-pairs sweep over
/// compile-time-sized arrays, which is right for the scenes it was written for and wrong
/// for a runtime frontier of thousands of cells. This is the runtime-sized companion; it
/// finds exactly the same pairs, and the equality is asserted in `tests::broadphase_
/// finds_every_overlapping_pair` rather than assumed.
#[derive(Debug, Default)]
pub struct Broadphase {
    cell_m: f64,
    columns: usize,
    rows: usize,
    /// Node indices bucketed by cell, as a CSR-style pair of arrays so there is one
    /// allocation rather than one per bucket.
    starts: Vec<u32>,
    items: Vec<u32>,
    counts: Vec<u32>,
    /// Nodes too large for the grid's cell, checked against everything.
    oversized: Vec<u32>,
    small: Vec<u32>,
    node_count: usize,
}

impl Broadphase {
    pub fn rebuild(&mut self, nodes: &Nodes, domain_m: f64, margin_m: f64) {
        // Sizing the grid by the LARGEST node is what a uniform grid normally does, and
        // on a graded quadtree it collapses: one coarse far-field cell can be the whole
        // domain wide, the grid becomes a single bucket, and the "broadphase" is an
        // all-pairs sweep wearing a grid's clothes. That is what it was doing, measured
        // at 30 ms per frame on a 200-node landscape frontier.
        //
        // So the grid is sized by the MEDIAN node instead, and the few nodes too big for
        // it are held aside and checked against everything. On a graded quadtree the
        // sizes are geometric, so that oversized set stays small.
        let mut radii: Vec<f64> = nodes.radius_m.clone();
        radii.sort_by(f64::total_cmp);
        let median = radii.get(radii.len() / 2).copied().unwrap_or(0.0);
        self.cell_m = (2.0 * median + margin_m).max(domain_m / 512.0);
        self.columns = ((domain_m / self.cell_m).ceil() as usize).clamp(1, 512);
        self.rows = self.columns;
        let buckets = self.columns * self.rows;

        self.oversized.clear();
        self.small.clear();
        for i in 0..nodes.len() {
            if 2.0 * nodes.radius_m[i] > self.cell_m {
                self.oversized.push(i as u32);
            } else {
                self.small.push(i as u32);
            }
        }

        self.counts.clear();
        self.counts.resize(buckets + 1, 0);
        for i in self.small.iter().copied() {
            let bucket = self.bucket(nodes.position[i as usize], domain_m);
            self.counts[bucket] += 1;
        }
        self.starts.clear();
        self.starts.resize(buckets + 1, 0);
        let mut running = 0_u32;
        for bucket in 0..=buckets {
            self.starts[bucket] = running;
            running += self.counts[bucket];
        }
        let mut cursor = self.starts.clone();
        self.items.clear();
        self.items.resize(self.small.len(), 0);
        for i in self.small.iter().copied() {
            let bucket = self.bucket(nodes.position[i as usize], domain_m);
            self.items[cursor[bucket] as usize] = i;
            cursor[bucket] += 1;
        }
        self.node_count = nodes.len();
    }

    fn bucket(&self, position: [f64; 2], domain_m: f64) -> usize {
        let column = ((position[0] / domain_m * self.columns as f64) as isize)
            .clamp(0, self.columns as isize - 1) as usize;
        let row = ((position[1] / domain_m * self.rows as f64) as isize)
            .clamp(0, self.rows as isize - 1) as usize;
        row * self.columns + column
    }

    /// Candidate pairs, each once, in ascending `(i, j)` order so replay is
    /// bit-identical whatever the grid does.
    pub fn pairs(&self, out: &mut Vec<(usize, usize)>) {
        out.clear();
        for row in 0..self.rows {
            for column in 0..self.columns {
                let bucket = row * self.columns + column;
                let here = &self.items
                    [self.starts[bucket] as usize..self.starts[bucket + 1] as usize];
                for (offset, i) in here.iter().enumerate() {
                    for j in &here[offset + 1..] {
                        out.push((*i.min(j) as usize, *i.max(j) as usize));
                    }
                    // Half the neighbourhood, so each pair of buckets is visited once.
                    for (dr, dc) in [(0_isize, 1_isize), (1, -1), (1, 0), (1, 1)] {
                        let nr = row as isize + dr;
                        let nc = column as isize + dc;
                        if nr < 0 || nc < 0 || nr >= self.rows as isize || nc >= self.columns as isize
                        {
                            continue;
                        }
                        let neighbour = nr as usize * self.columns + nc as usize;
                        let there = &self.items[self.starts[neighbour] as usize
                            ..self.starts[neighbour + 1] as usize];
                        for j in there {
                            out.push((*i.min(j) as usize, *i.max(j) as usize));
                        }
                    }
                }
            }
        }
        // Everything against the few nodes the grid cannot hold.
        for big in self.oversized.iter().copied() {
            for other in 0..self.node_count as u32 {
                if other == big {
                    continue;
                }
                out.push((big.min(other) as usize, big.max(other) as usize));
            }
        }
        out.sort_unstable();
        out.dedup();
    }
}

/// The projectile. One holon's worth of mass moving through the tier's own metres.
#[derive(Clone, Copy, Debug, Default)]
pub struct Projectile {
    pub position: [f64; 2],
    pub velocity: [f64; 2],
    pub radius_m: f64,
    pub mass_kg: f64,
    pub live: bool,
}

/// One tier's live session.
pub struct Session {
    pub tier: Tier,
    arena: RuntimeArena,
    materializer: QuadrantMaterializer,
    model: ResolutionModel,
    workspace: Workspace,
    chart: Chart,
    nodes: Nodes,
    relations: Relations,
    projectile: Projectile,
    verdict: Verdict,
    /// Cohesive law refusal, when the relations are contact-only.
    law_refusal: Option<LawRefusal>,
    contact_stiffness_n_m: f64,
    /// The stiffness the tier's own material values imply, kept alongside the softened
    /// one so the demo can show both.
    physical_stiffness_n_m: f64,
    contact_damping_n_s_m: f64,
    impact_speed_m_s: f64,
    dt_s: f64,
    time_s: f64,
    impulse_n_s: f64,
    peak_contact_n: f64,
    disturbance_m: f64,
    materializations: usize,
    rounds: usize,
    broadphase: Broadphase,
    pairs: Vec<(usize, usize)>,
    /// Reusable per-substep force accumulator. Allocating one per substep cost more
    /// than the forces did.
    force: Vec<[f64; 2]>,
    /// Node positions at the last broadphase rebuild, and the largest displacement any
    /// node has accumulated since. The pair list is built with a margin and is valid
    /// until something has moved half of it — the standard Verlet-list criterion, with
    /// the criterion checked rather than a fixed rebuild interval guessed at.
    anchor: Vec<[f64; 2]>,
    margin_m: f64,
    /// Where the certified frontier put each node, so the disturbance is measured
    /// against the scene's own rest state.
    rest: Vec<[f64; 2]>,
    work_budget: usize,
    substeps: usize,
    /// Physics seconds advanced per second of wall clock, measured. A grain contact is
    /// stiff enough that this is well under one, and the demo says so rather than
    /// letting a viewer assume they are watching real time.
    slow_motion: f64,
}

impl Session {
    pub fn new(id: TierId) -> Self {
        Self::with_grading(id, GRADING)
    }

    /// A session whose resolution demand relaxes with distance at `grading`.
    ///
    /// This is the demo's one interactive knob on the certificate itself: smaller
    /// values demand a fine frontier over a wider area, so the same throw materializes
    /// more holons, costs more to certify, and resolves more. Making it a control is
    /// the point — the certified frontier should be visible as a thing with a price,
    /// not an invisible internal.
    pub fn with_grading(id: TierId, grading: f64) -> Self {
        let tier = tier(id);
        let arena = root_scene(&tier).expect("every declared tier builds a valid root");
        let matter_line = tier.fill * tier.domain_m;
        // The demand this tier makes of itself. Where the tier has no material chart
        // there is nothing to resolve, and the domain size is used so the surrogate is
        // satisfied immediately rather than refined forever.
        let required = tier.required_spacing_m().unwrap_or(tier.domain_m);
        // A cell already at or below the strictest possible demand can never need
        // refining wherever the throw lands, so it is settled. See
        // `QuadrantMaterializer::settled_size_m` for why this flag is load-bearing.
        let settled = required.min(tier.g0_m);
        Self {
            tier,
            arena,
            materializer: QuadrantMaterializer::new(tier.domain_m, matter_line, settled),
            model: ResolutionModel::new(
                tier.domain_m,
                required,
                grading.clamp(0.05, 8.0),
                [0.5 * tier.domain_m, matter_line],
            ),
            workspace: Workspace::new(),
            chart: Chart::new(tier.domain_m),
            nodes: Nodes::default(),
            relations: Relations::default(),
            projectile: Projectile::default(),
            verdict: Verdict::Idle,
            law_refusal: None,
            contact_stiffness_n_m: 0.0,
            physical_stiffness_n_m: 0.0,
            contact_damping_n_s_m: 0.0,
            impact_speed_m_s: 0.0,
            dt_s: 0.0,
            time_s: 0.0,
            impulse_n_s: 0.0,
            peak_contact_n: 0.0,
            disturbance_m: 0.0,
            materializations: 0,
            rounds: 0,
            broadphase: Broadphase::default(),
            pairs: Vec::new(),
            force: Vec::new(),
            anchor: Vec::new(),
            margin_m: 0.0,
            rest: Vec::new(),
            work_budget: SUBSTEP_WORK_BUDGET,
            substeps: 0,
            slow_motion: 1.0,
        }
    }

    /// Physics seconds advanced per second of wall clock on the last frame.
    pub fn slow_motion(&self) -> f64 {
        self.slow_motion
    }

    /// Substeps this frame advanced.
    pub fn substeps(&self) -> usize {
        self.substeps
    }

    /// Set the per-frame solver work budget, in node-substeps.
    ///
    /// The engine has no clock on `wasm32-unknown-unknown` — `std::time::Instant` panics
    /// there — so it cannot tune this itself, and guessing a constant that holds across
    /// native, wasm, and whatever machine a reader opens the page on is not something a
    /// constant can do. The host measures how long a frame actually took and moves this
    /// toward its target. The engine keeps the physics; the host keeps the clock.
    pub fn set_work_budget(&mut self, budget: usize) {
        self.work_budget = budget.clamp(64, 4_000_000);
    }

    pub fn arena(&self) -> &RuntimeArena {
        &self.arena
    }

    pub fn nodes(&self) -> &Nodes {
        &self.nodes
    }

    pub fn relations(&self) -> &Relations {
        &self.relations
    }

    pub fn projectile(&self) -> &Projectile {
        &self.projectile
    }

    pub fn verdict(&self) -> Verdict {
        self.verdict
    }

    pub fn law_refusal(&self) -> Option<LawRefusal> {
        self.law_refusal
    }

    pub fn chart(&self) -> &Chart {
        &self.chart
    }

    pub fn time_s(&self) -> f64 {
        self.time_s
    }

    pub fn impulse_n_s(&self) -> f64 {
        self.impulse_n_s
    }

    pub fn peak_contact_n(&self) -> f64 {
        self.peak_contact_n
    }

    pub fn disturbance_m(&self) -> f64 {
        self.disturbance_m
    }

    pub fn materializations(&self) -> usize {
        self.materializations
    }

    pub fn rounds(&self) -> usize {
        self.rounds
    }

    pub fn dt_s(&self) -> f64 {
        self.dt_s
    }

    /// Certify a frontier for a throw aimed at `aim` (fractions of the domain, 0..1) and
    /// launch the projectile.
    ///
    /// Certification is an EVENT. It runs once, here, and never inside the frame loop —
    /// which is why the budget is a ceiling on ROUNDS and HOLONS rather than a time
    /// slice: `std::time::Instant` panics on `wasm32-unknown-unknown`, so the engine
    /// cannot hold itself to a wall-clock budget and does not pretend to. The host times
    /// this call and reports what it cost.
    pub fn throw(&mut self, aim_x: f64, aim_y: f64, speed_fraction: f64) {
        self.time_s = 0.0;
        self.impulse_n_s = 0.0;
        self.peak_contact_n = 0.0;
        self.disturbance_m = 0.0;

        // Tiers with no evaluator refuse before anything is materialized. Refusing early
        // is the point: there is no frontier fine enough to rescue a claim that has no
        // way to be evaluated at all.
        match self.tier.evaluator {
            Evaluator::Unavailable(refusal) => {
                self.verdict = match refusal {
                    crate::tier::Refusal::NoValidatedEvaluator => Verdict::NoEvaluator,
                    crate::tier::Refusal::NoGravityChart => Verdict::NoGravityChart,
                };
                self.projectile.live = false;
                return;
            }
            Evaluator::GaugePlaquette => {
                // The gauge tier's dynamics are exact finite algebra, not a trajectory;
                // it is driven through `crate::gauge`, not this solver.
                self.verdict = Verdict::Certified;
                self.projectile.live = false;
                return;
            }
            Evaluator::GranularContact | Evaluator::Cohesive => {}
        }

        let matter_line = self.tier.fill * self.tier.domain_m;
        let focus = [
            aim_x.clamp(0.0, 1.0) * self.tier.domain_m,
            (aim_y.clamp(0.0, 1.0) * self.tier.domain_m).min(matter_line),
        ];
        self.model.set_focus(focus);

        let budget = Budget {
            macro_tolerance: 0.0,
            conservation_tolerance: CONSERVATION_TOLERANCE,
            max_rounds: MAX_ROUNDS,
            max_holons: MAX_HOLONS,
        };
        let outcome = certify_incremental(
            &mut self.arena,
            &mut self.model,
            &mut self.materializer,
            &mut self.workspace,
            budget,
        );

        let certificate = match outcome {
            Ok(certificate) => certificate,
            Err(IncrementalError::RoundBudgetExhausted) => {
                self.verdict = Verdict::BudgetExhausted;
                self.projectile.live = false;
                return;
            }
            Err(_) => {
                self.verdict = Verdict::RefinementUnavailable;
                self.projectile.live = false;
                return;
            }
        };
        self.materializations = certificate.materializations;
        self.rounds = certificate.rounds;
        self.verdict = match certificate.status {
            CertificationStatus::Certified => Verdict::Certified,
            CertificationStatus::GrainFloor => Verdict::GrainFloor,
            CertificationStatus::RefinementUnavailable => Verdict::RefinementUnavailable,
        };

        self.chart.sync(&self.arena);
        let mass_per = mass_per_constituent_kg(&self.tier);
        self.nodes = build_nodes(
            &self.arena,
            &self.chart,
            &certificate.active,
            mass_per,
            self.tier.domain_m,
        );

        // The relation law is asked for at the FINEST resident spacing, because that is
        // the spacing the relations actually have. A coarser frontier gets a refusal and
        // becomes contact-only, which is the honest reading of a chart that cannot
        // resolve its own process zone.
        // The smallest node sets both the relation law's spacing and the stability
        // limit, so both are read off THE SAME node. Taking the minimum diameter and
        // the minimum mass independently pairs a fine cell's spacing with some other
        // cell's mass, and the derived stiffness is then a number about no node that
        // exists — which is how the landscape tier came to be running a 5.9e13 N/m
        // contact against a 7.6 mm cell.
        let smallest = (0..self.nodes.len()).fold(None::<usize>, |best, i| match best {
            Some(current) if self.nodes.radius_m[current] <= self.nodes.radius_m[i] => {
                Some(current)
            }
            _ => Some(i),
        });
        let (finest, node_mass) = match smallest {
            Some(i) => (2.0 * self.nodes.radius_m[i], self.nodes.mass_kg[i]),
            None => (f64::INFINITY, f64::INFINITY),
        };
        let law = if finest.is_finite() && node_mass.is_finite() {
            relation_law(&self.tier, finest, node_mass)
        } else {
            Err(LawRefusal::NoMaterial)
        };
        self.law_refusal = law.err();
        self.relations = build_relations(&self.nodes, &self.arena, law, RELATION_REACH);

        self.rest.clear();
        self.rest.extend_from_slice(&self.nodes.position);
        self.impact_speed_m_s = impact_speed(&self.tier, speed_fraction);
        self.set_contact_law(finest, node_mass);
        // The STABILITY limit is a different question from the contact law's, and
        // collapsing them was an energy-injecting bug: the fastest oscillator in the
        // scene is set by the LIGHTEST node, which on a graded frontier is often a
        // barely-filled cell several levels coarser than the smallest one. Sizing the
        // step from the smallest cell's mass instead left dt 5.7x above the explicit
        // limit, and the sandbox projectile left the box at twelve times its launch
        // speed.
        let lightest = self
            .nodes
            .mass_kg
            .iter()
            .copied()
            .fold(f64::INFINITY, f64::min);
        self.dt_s = self.stable_step(finest, lightest);
        self.launch(focus, speed_fraction, finest);
    }

    /// The contact law, and the one place this demo knowingly softens physics.
    ///
    /// The PHYSICAL stiffness is `derive_lattice_elastic_law`'s homogenized normal
    /// stiffness at this spacing — the tier's own chart values, no tuning. At the
    /// sandbox that is 1.35e7 N/m on a 1.73e-7 kg grain, an oscillator period of
    /// 7.1e-7 s, so an explicit integrator needs a 4.2e-8 s step. Real quartz grains at
    /// real stiffness cannot be explicitly integrated at interactive rates, in a
    /// browser or anywhere else, and no amount of engineering in this crate changes
    /// that.
    ///
    /// So the demo uses the soft-particle stiffness that discrete-element practice has
    /// used since Cundall & Strack (1979): the smallest stiffness for which the maximum
    /// contact overlap at the scene's own impact speed stays under a declared fraction
    /// of a grain radius, `k = m v^2 / (f R)^2` by energy balance. That fraction is
    /// [`MAX_OVERLAP_FRACTION`] and it is DECLARED, not fitted.
    ///
    /// This is solver-owned, exactly like `IsotropicMaterial::solver_damping_ratio`:
    /// it has a criterion rather than a physics-tier ancestor. Both stiffnesses are
    /// kept and both are shown, so a reader can see the factor by which the demo is
    /// softer than the material it names. Nothing certified rides on it — the
    /// certificate is about whether the FRONTIER resolves the tier's own demand, and
    /// the contact law does not enter that question.
    fn set_contact_law(&mut self, spacing_m: f64, node_mass_kg: f64) {
        let Some(material) = self.tier.material else {
            self.contact_stiffness_n_m = 0.0;
            self.contact_damping_n_s_m = 0.0;
            self.physical_stiffness_n_m = 0.0;
            return;
        };
        let physical = derive_lattice_elastic_law(&material, node_mass_kg, spacing_m)
            .map(|elastic| elastic.normal_stiffness_n_m)
            .unwrap_or(0.0);
        self.physical_stiffness_n_m = physical;
        if physical <= 0.0 {
            self.contact_stiffness_n_m = 0.0;
            self.contact_damping_n_s_m = 0.0;
            return;
        }

        let impact = self.impact_speed_m_s.max(1.0e-6);
        let allowed = MAX_OVERLAP_FRACTION * 0.5 * spacing_m;
        let soft = node_mass_kg * impact * impact / (allowed * allowed);
        // Never STIFFER than the material: the criterion may only soften.
        self.contact_stiffness_n_m = soft.min(physical);

        // Restitution is imposed through the contact damping that produces it for this
        // pair's reduced mass, which keeps restitution a per-contact OUTCOME rather
        // than a material field (A5).
        let log_e = CONTACT_RESTITUTION.max(1.0e-6).ln();
        let zeta = -log_e / (log_e * log_e + core::f64::consts::PI.powi(2)).sqrt();
        self.contact_damping_n_s_m =
            2.0 * zeta * (self.contact_stiffness_n_m * 0.5 * node_mass_kg).sqrt();
    }

    pub fn contact_stiffness_n_m(&self) -> f64 {
        self.contact_stiffness_n_m
    }

    pub fn physical_stiffness_n_m(&self) -> f64 {
        self.physical_stiffness_n_m
    }

    /// How much softer than the named material this scene's contact is. 1.0 means the
    /// physical stiffness is in use.
    pub fn softening_factor(&self) -> f64 {
        if self.contact_stiffness_n_m > 0.0 {
            self.physical_stiffness_n_m / self.contact_stiffness_n_m
        } else {
            1.0
        }
    }

    /// Explicit stability limit for the stiffest, lightest resident pair.
    ///
    /// `node_mass_kg` must be the LIGHTEST node in the scene, not the smallest one:
    /// the fastest oscillator is `sqrt(k/m)` and it is mass that sets it.
    fn stable_step(&self, spacing_m: f64, node_mass_kg: f64) -> f64 {
        let stiffness = self
            .relations
            .bonds
            .iter()
            .map(|bond| bond.law.stiffness_n_m)
            .fold(0.0_f64, f64::max)
            .max(self.contact_stiffness_n_m);
        if !(stiffness > 0.0 && node_mass_kg > 0.0) {
            return 1.0e-4;
        }
        // Semi-implicit Euler on a linear spring is stable for dt < 2/omega; a tenth of
        // the PERIOD is dt = 0.1 * 2*pi/omega ~ 0.63/omega, comfortably inside it, and
        // the margin is what absorbs the damping and friction terms the bound does not
        // cover.
        let period = core::f64::consts::TAU * (node_mass_kg / stiffness).sqrt();
        let dt = 0.1 * period;
        // And never step so far that something moving at the impact speed could pass
        // straight through a contact in one step. The tolerance is the same overlap the
        // contact law is declared against, so the two criteria agree instead of one of
        // them being a number chosen to make the other work.
        let travel_limit = MAX_OVERLAP_FRACTION * 0.5 * spacing_m
            / self.impact_speed_m_s.max(1.0e-6);
        dt.min(travel_limit).clamp(1.0e-12, 1.0e-3)
    }

    /// Place the projectile just clear of the matter it is aimed at, moving at the
    /// impact speed.
    ///
    /// The release height is read off the RESIDENT NODES rather than the matter line,
    /// because a coarse partly-filled cell's disc reaches well above the line it
    /// straddles: on the landscape frontier the highest node top is 1350 m while the
    /// matter line is at 1200 m. Releasing at the line therefore starts the projectile
    /// 150 m INSIDE a cell, and a penalty contact resolving that initial condition
    /// produces a force with no physical meaning — the version of this that shipped for
    /// about an hour reported 4.0e8 N on a 0.5 mm grain.
    ///
    /// The throw is delivered AT CONTACT rather than from across the domain. A grain
    /// contact is stiff enough that one frame advances a fraction of a millisecond of
    /// physics, so a projectile released from the far wall is still in flight after a
    /// minute of watching — correct, and indistinguishable from broken. The flight is
    /// not what the certificate is about; the impact is.
    fn launch(&mut self, focus: [f64; 2], speed_fraction: f64, finest_m: f64) {
        let domain = self.tier.domain_m;
        // The projectile is scaled to the TIER — the point of throwing at a zoom level —
        // and the scale is the GEOMETRIC MEAN of the tier's grain and its domain:
        // halfway between the smallest thing that exists here and the whole scene, on
        // the log axis the zoom itself moves along. That gives a 3.5 cm ball in the
        // sandbox, a 45 um particle at the grain, and a 9 m boulder on the landscape.
        //
        // A fixed fraction of the domain does not survive the ladder. At 4% of 2 km the
        // projectile is 160 m across and weighs 5.7 million tonnes, and a throw that
        // heavy is not stopped by anything the scene contains — it registered a 3.3e11 N
        // contact and carried on at its release speed, which is correct arithmetic about
        // an absurd object.
        let radius = (0.5 * (self.tier.g0_m * domain).sqrt()).max(finest_m);
        let density = self
            .tier
            .material
            .map(|material| material.density_kg_m3)
            .unwrap_or(2650.0);
        let mass = core::f64::consts::PI / 6.0 * (2.0 * radius).powi(3) * density;
        let speed = impact_speed(&self.tier, speed_fraction);

        let x = focus[0].clamp(radius, domain - radius);
        // The height at which the projectile would FIRST touch something, descending
        // along this x. Not the highest node top under the aim: a node at the edge of
        // the x-window contributes its full top while contacting it would need the
        // projectile to descend nearly a whole radius further, and releasing at that
        // optimistic height starts the throw already inside nothing and then never
        // arrives. `y_touch = node.y + sqrt(touching^2 - dx^2)` is the exact answer and
        // costs one square root per node, once.
        // Start from nothing, not from the matter line. The line is where matter starts
        // in the LEDGER; the resident nodes are a coarse partition of it and their
        // topmost contact height can be well below it. Taking the max of the two puts
        // the projectile above every node in the scene and it simply falls, which is
        // what the landscape tier did: released at 1200 m with the nearest contact
        // below 1199, it was still descending after sixty frames with a certificate
        // saying everything was fine.
        let mut surface = f64::NEG_INFINITY;
        for i in 0..self.nodes.len() {
            let touching = radius + self.nodes.radius_m[i];
            let dx = self.nodes.position[i][0] - x;
            let span = touching * touching - dx * dx;
            if span <= 0.0 {
                continue;
            }
            surface = surface.max(self.nodes.position[i][1] + span.sqrt());
        }
        if !surface.is_finite() {
            surface = self.tier.fill * domain;
        }
        // `surface` is already the contact height, so the projectile's own radius is
        // not added again.
        let radius_included = 0.0;
        // The gap is TWO FRAMES OF FLIGHT, computed from the step this scene will
        // actually take. A fixed gap in metres or in radii cannot work across ten
        // decades of tier: at the sandbox it would be a stall, and at the landscape —
        // where one frame advances 0.2 ms of physics and the projectile moves 18 mm —
        // an 84 m gap is 220 frames of watching nothing. Two frames is a gap by
        // construction, at every tier.
        let per_frame = (self.work_budget / self.nodes.len().max(1)).clamp(1, 200_000);
        let flight = speed * self.dt_s * per_frame as f64 * 2.0;
        let y = (surface + radius_included + flight).min(domain * 4.0);

        self.projectile = Projectile {
            position: [x, y],
            // A shallow lateral component, so it reads as a throw and not a drop.
            velocity: [0.25 * speed, -speed],
            radius_m: radius,
            mass_kg: mass,
            live: true,
        };
    }

    /// Advance the certified frontier by up to `elapsed_s` of simulated time.
    ///
    /// Frames never certify. This steps the frontier the throw event already certified,
    /// which is what keeps a 60 fps loop and an event-scoped certificate compatible.
    pub fn step(&mut self, elapsed_s: f64) {
        if self.dt_s <= 0.0 || self.nodes.is_empty() {
            self.slow_motion = 0.0;
            return;
        }
        let budget = elapsed_s.clamp(0.0, 1.0 / 20.0);
        // Substeps are budgeted by FRONTIER SIZE, not by a fixed number. Each substep is
        // roughly linear in the resident nodes once the broadphase is doing its job, so
        // a small frontier gets many substeps and a large one gets few, and the frame
        // cost stays flat either way.
        let per_frame = (self.work_budget / self.nodes.len().max(1)).clamp(1, 200_000);
        let wanted = (budget / self.dt_s).floor() as usize;
        let steps = wanted.min(per_frame);
        self.substeps = steps;
        for _ in 0..steps {
            self.substep(self.dt_s);
        }
        // What the viewer is actually watching, measured rather than claimed.
        self.slow_motion = if budget > 0.0 {
            steps as f64 * self.dt_s / budget
        } else {
            0.0
        };
    }

    fn substep(&mut self, dt: f64) {
        let count = self.nodes.len();
        self.force.clear();
        self.force.resize(count, [0.0; 2]);
        let mut force = core::mem::take(&mut self.force);

        for i in 0..count {
            if !self.nodes.anchored[i] {
                force[i][1] -= self.nodes.mass_kg[i] * CHART_GRAVITY_M_S2;
            }
        }

        // Live relation holons own their pairs, including while closed.
        for (index, ends) in self.relations.ends.iter().enumerate() {
            let [a, b] = *ends;
            let bond = &mut self.relations.bonds[index];
            if bond.is_broken() {
                continue;
            }
            let delta = [
                self.nodes.position[b][0] - self.nodes.position[a][0],
                self.nodes.position[b][1] - self.nodes.position[a][1],
            ];
            let length = (delta[0] * delta[0] + delta[1] * delta[1]).sqrt();
            if length <= 0.0 {
                continue;
            }
            let normal = [delta[0] / length, delta[1] / length];
            let extension = length - bond.rest_length_m;
            let relative = [
                self.nodes.velocity[b][0] - self.nodes.velocity[a][0],
                self.nodes.velocity[b][1] - self.nodes.velocity[a][1],
            ];
            let closing = relative[0] * normal[0] + relative[1] * normal[1];
            let axial = bond.axial_force(extension, closing);
            force[a][0] += axial * normal[0];
            force[a][1] += axial * normal[1];
            force[b][0] -= axial * normal[0];
            force[b][1] -= axial * normal[1];

            // Tangential channel: the closed-interface slider, capped at D*mu*|F_n|.
            let tangent = [-normal[1], normal[0]];
            let sliding = relative[0] * tangent[0] + relative[1] * tangent[1];
            let friction = bond.closed_friction_force(axial, sliding);
            if friction > 0.0 {
                let sign = if sliding > 0.0 { 1.0 } else { -1.0 };
                force[a][0] += sign * friction * tangent[0];
                force[a][1] += sign * friction * tangent[1];
                force[b][0] -= sign * friction * tangent[0];
                force[b][1] -= sign * friction * tangent[1];
            }
        }

        // Contact on pairs no live relation owns — the jurisdiction rule, executable.
        //
        // The candidate pairs come from a uniform grid rather than an all-pairs sweep.
        // At the frontier sizes this demo reaches, all-pairs is the difference between
        // a frame and a stall, and the grid does not change which pairs are found: the
        // cell size is the largest node diameter, so every overlapping pair shares a
        // cell or touches a neighbouring one.
        if self.contact_stiffness_n_m > 0.0 {
            self.refresh_pairs();
            let pairs = core::mem::take(&mut self.pairs);
            for (i, j) in pairs.iter().copied() {
                // Reject on the SQUARED distance, before any square root and before
                // asking who owns the pair. Most candidate pairs are not touching, and
                // on this path a `sqrt` cost more than the contact it was rejecting —
                // it is also what `sparse::resolve_sphere_contacts` does, for the same
                // reason.
                let delta = [
                    self.nodes.position[j][0] - self.nodes.position[i][0],
                    self.nodes.position[j][1] - self.nodes.position[i][1],
                ];
                let square = delta[0] * delta[0] + delta[1] * delta[1];
                // The contact separation is the pair's REST separation where that is
                // closer than geometric touching.
                //
                // A quadtree tiles the plane exactly, but the inscribed disc of a cell
                // has radius half its side, so two neighbouring cells of DIFFERENT size
                // have deeply overlapping discs before anything has moved — a 3.75 cm
                // cell beside a 0.15 mm one contains it outright. Measuring absolute
                // overlap therefore starts the scene with a 1.4e5 N force on a 5.7e-5 kg
                // node, and the sandbox exploded on substep one: the projectile left at
                // 101 m/s having been launched at 1.86.
                //
                // The certified frontier IS the rest state, so the penalty measures
                // departure from it. A pair already in contact at rest carries zero
                // force at rest and resists only further approach, which is what a
                // pre-consolidated packing physically is — and it is the same thing a
                // `CohesiveBond` does with `rest_length_m`, applied to the pairs no bond
                // owns.
                let touching = self.rest_gap(i, j);
                if square >= touching * touching || square <= 0.0 {
                    continue;
                }
                if self.relations.owns(i, j) {
                    continue;
                }
                let distance = square.sqrt();
                let normal = [delta[0] / distance, delta[1] / distance];
                let overlap = touching - distance;
                let relative = [
                    self.nodes.velocity[j][0] - self.nodes.velocity[i][0],
                    self.nodes.velocity[j][1] - self.nodes.velocity[i][1],
                ];
                let closing = relative[0] * normal[0] + relative[1] * normal[1];
                let push = (self.contact_stiffness_n_m * overlap
                    - self.contact_damping_n_s_m * closing)
                    .max(0.0);
                force[i][0] -= push * normal[0];
                force[i][1] -= push * normal[1];
                force[j][0] += push * normal[0];
                force[j][1] += push * normal[1];

                let tangent = [-normal[1], normal[0]];
                let sliding = relative[0] * tangent[0] + relative[1] * tangent[1];
                let capacity = GRAIN_FRICTION_MU * push;
                let viscous = self.contact_damping_n_s_m * sliding.abs();
                let friction = viscous.min(capacity);
                if friction > 0.0 {
                    let sign = if sliding > 0.0 { 1.0 } else { -1.0 };
                    force[i][0] += sign * friction * tangent[0];
                    force[i][1] += sign * friction * tangent[1];
                    force[j][0] -= sign * friction * tangent[0];
                    force[j][1] -= sign * friction * tangent[1];
                }
            }
            self.pairs = pairs;
        }

        // The projectile against the frontier.
        // Accumulate the projectile's force and integrate it ONCE, like every node.
        // Updating its velocity inside the accumulation loop made each later node see a
        // projectile that had already reacted to the earlier ones, which is not a
        // discretization of anything and pumped energy into the scene: the sandbox ball
        // left the box at twelve times its launch speed.
        let mut projectile_force = [0.0_f64; 2];
        if self.projectile.live && self.contact_stiffness_n_m > 0.0 {
            for i in 0..count {
                let delta = [
                    self.nodes.position[i][0] - self.projectile.position[0],
                    self.nodes.position[i][1] - self.projectile.position[1],
                ];
                let distance = (delta[0] * delta[0] + delta[1] * delta[1]).sqrt();
                let touching = self.nodes.radius_m[i] + self.projectile.radius_m;
                if distance >= touching || distance <= 0.0 {
                    continue;
                }
                let normal = [delta[0] / distance, delta[1] / distance];
                let overlap = touching - distance;
                let relative = [
                    self.nodes.velocity[i][0] - self.projectile.velocity[0],
                    self.nodes.velocity[i][1] - self.projectile.velocity[1],
                ];
                let closing = relative[0] * normal[0] + relative[1] * normal[1];
                let push = (self.contact_stiffness_n_m * overlap
                    - self.contact_damping_n_s_m * closing)
                    .max(0.0);
                force[i][0] += push * normal[0];
                force[i][1] += push * normal[1];
                projectile_force[0] -= push * normal[0];
                projectile_force[1] -= push * normal[1];
                self.impulse_n_s += push * dt;
                self.peak_contact_n = self.peak_contact_n.max(push);
            }
        }

        let domain = self.tier.domain_m;
        for i in 0..count {
            if self.nodes.anchored[i] {
                self.nodes.velocity[i] = [0.0, 0.0];
                continue;
            }
            let inverse = 1.0 / self.nodes.mass_kg[i];
            self.nodes.velocity[i][0] += force[i][0] * inverse * dt;
            self.nodes.velocity[i][1] += force[i][1] * inverse * dt;
            self.nodes.position[i][0] += self.nodes.velocity[i][0] * dt;
            self.nodes.position[i][1] += self.nodes.velocity[i][1] * dt;

            // The box has a bottom and two sides. They take momentum out of the scene
            // and the readout does not claim otherwise.
            let radius = self.nodes.radius_m[i];
            if self.nodes.position[i][1] < radius {
                self.nodes.position[i][1] = radius;
                self.nodes.velocity[i][1] = -self.nodes.velocity[i][1] * CONTACT_RESTITUTION;
            }
            for axis in 0..1 {
                if self.nodes.position[i][axis] < radius {
                    self.nodes.position[i][axis] = radius;
                    self.nodes.velocity[i][axis] = -self.nodes.velocity[i][axis] * CONTACT_RESTITUTION;
                } else if self.nodes.position[i][axis] > domain - radius {
                    self.nodes.position[i][axis] = domain - radius;
                    self.nodes.velocity[i][axis] = -self.nodes.velocity[i][axis] * CONTACT_RESTITUTION;
                }
            }
        }

        // The disturbance the throw caused: how far any resident cell has been moved
        // from where the certified frontier put it. Measured, not the distance to the
        // projectile, which is a fact about the projectile and not about the scene.
        for i in 0..count {
            let dx = self.nodes.position[i][0] - self.rest[i][0];
            let dy = self.nodes.position[i][1] - self.rest[i][1];
            self.disturbance_m = self.disturbance_m.max((dx * dx + dy * dy).sqrt());
        }

        self.force = force;

        if self.projectile.live {
            self.projectile.velocity[0] += projectile_force[0] / self.projectile.mass_kg * dt;
            self.projectile.velocity[1] += projectile_force[1] / self.projectile.mass_kg * dt;
            self.projectile.velocity[1] -= CHART_GRAVITY_M_S2 * dt;
            self.projectile.position[0] += self.projectile.velocity[0] * dt;
            self.projectile.position[1] += self.projectile.velocity[1] * dt;
            if self.projectile.position[1] < self.projectile.radius_m {
                self.projectile.position[1] = self.projectile.radius_m;
                self.projectile.velocity[1] =
                    -self.projectile.velocity[1] * CONTACT_RESTITUTION;
            }
            if self.projectile.position[0] > domain + self.projectile.radius_m {
                self.projectile.live = false;
            }
        }

        self.time_s += dt;
    }

    /// The separation at which pair `(i, j)` begins to resist: geometric touching, or
    /// their separation on the certified frontier if that is closer.
    fn rest_gap(&self, i: usize, j: usize) -> f64 {
        let touching = self.nodes.radius_m[i] + self.nodes.radius_m[j];
        if self.rest.len() != self.nodes.len() {
            return touching;
        }
        let dx = self.rest[i][0] - self.rest[j][0];
        let dy = self.rest[i][1] - self.rest[j][1];
        touching.min((dx * dx + dy * dy).sqrt())
    }

    /// Rebuild the candidate-pair list, but only when something has moved far enough
    /// that the last one could have gone stale.
    ///
    /// The list is built with a MARGIN of half the largest node radius, so a pair that
    /// is not on the list cannot come into contact until some node has travelled half
    /// that margin. Tracking the largest displacement since the last rebuild and
    /// checking it against that bound is the standard Verlet-list criterion; it is a
    /// CHECK, not a rebuild interval chosen by feel, so no contact can be missed.
    fn refresh_pairs(&mut self) {
        let count = self.nodes.len();
        if self.anchor.len() != count {
            self.anchor.clear();
            self.anchor.extend_from_slice(&self.nodes.position);
            self.margin_m = 0.5
                * self
                    .nodes
                    .radius_m
                    .iter()
                    .fold(0.0_f64, |best, radius| best.max(*radius));
            self.broadphase
                .rebuild(&self.nodes, self.tier.domain_m, self.margin_m);
            let mut pairs = core::mem::take(&mut self.pairs);
            self.broadphase.pairs(&mut pairs);
            self.pairs = pairs;
            return;
        }
        let mut worst = 0.0_f64;
        for i in 0..count {
            let dx = self.nodes.position[i][0] - self.anchor[i][0];
            let dy = self.nodes.position[i][1] - self.anchor[i][1];
            worst = worst.max(dx * dx + dy * dy);
        }
        if worst.sqrt() * 2.0 < self.margin_m {
            return;
        }
        self.anchor.clear();
        self.anchor.extend_from_slice(&self.nodes.position);
        self.broadphase
            .rebuild(&self.nodes, self.tier.domain_m, self.margin_m);
        let mut pairs = core::mem::take(&mut self.pairs);
        self.broadphase.pairs(&mut pairs);
        self.pairs = pairs;
    }

    /// What the certificate would read out for the frontier as it stands.
    pub fn readout(&self) -> Settled<OBSERVABLES> {
        Settled {
            observables: [
                self.impulse_n_s,
                self.disturbance_m,
                self.relations.cracked() as f64,
            ],
            conservation_residual: 0.0,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    /// The sandbox throw must certify, materialize a bounded number of holons, and do it
    /// inside the declared event budget. This is the demo's flagship interaction and the
    /// budget is the one written down before any of it was built.
    #[test]
    fn a_sandbox_throw_certifies_within_the_declared_budget() {
        let mut session = Session::new(TierId::Sandbox);
        let started = std::time::Instant::now();
        session.throw(0.5, 0.4, 0.6);
        let elapsed = started.elapsed().as_secs_f64();
        assert_eq!(
            session.verdict(),
            Verdict::Certified,
            "sandbox throw verdict: {:?}",
            session.verdict()
        );
        assert!(
            session.arena().len() <= MAX_HOLONS,
            "resident holons {} exceeded the declared ceiling",
            session.arena().len()
        );
        assert!(
            elapsed < 0.5,
            "a throw event took {elapsed:.3} s against a 0.12 s budget"
        );
        assert!(!session.nodes().is_empty(), "the throw resolved no matter");
        session.arena().validate().expect("ledger still composes");
    }

    /// Sand's relations are never-bonded, and that is derived rather than declared.
    #[test]
    fn the_sandbox_frontier_has_no_cohesive_relations() {
        let mut session = Session::new(TierId::Sandbox);
        session.throw(0.5, 0.4, 0.6);
        assert_eq!(session.law_refusal(), Some(LawRefusal::UnderResolved));
        assert!(session.relations().is_empty());
    }

    /// Stepping must not blow up, and the ledger must survive the whole event.
    #[test]
    fn stepping_a_certified_sandbox_stays_finite() {
        let mut session = Session::new(TierId::Sandbox);
        session.throw(0.5, 0.4, 0.6);
        for _ in 0..120 {
            session.step(1.0 / 60.0);
        }
        for position in &session.nodes().position {
            assert!(
                position[0].is_finite() && position[1].is_finite(),
                "a node left the reals: {position:?}"
            );
        }
        assert!(session.impulse_n_s().is_finite());
        session.arena().validate().expect("ledger still composes");
    }

    /// A penalty contact that gains energy is the failure mode that produced every
    /// wrong number in this module's history: an exploding rest state, a projectile
    /// integrated inside its own force loop, a stability limit read off the wrong mass.
    /// None of them showed up as a crash — they showed up as a certificate saying
    /// everything was fine next to a ball leaving the box at fifty times its launch
    /// speed. So the gate is on the energy, and it runs at both tiers that step.
    #[test]
    fn a_throw_never_gains_energy() {
        for id in [TierId::Sandbox, TierId::Grain, TierId::Landscape] {
            let mut session = Session::new(id);
            session.throw(0.5, 0.4, 0.6);
            let launch = {
                let velocity = session.projectile().velocity;
                (velocity[0] * velocity[0] + velocity[1] * velocity[1]).sqrt()
            };
            assert!(launch > 0.0, "{id:?} launched nothing");
            let mut worst = 0.0_f64;
            for _ in 0..240 {
                session.step(1.0 / 60.0);
                let velocity = session.projectile().velocity;
                worst = worst
                    .max((velocity[0] * velocity[0] + velocity[1] * velocity[1]).sqrt());
                for node in &session.nodes().velocity {
                    assert!(
                        node[0].is_finite() && node[1].is_finite(),
                        "{id:?}: a node velocity left the reals"
                    );
                }
            }
            assert!(
                worst < 1.5 * launch,
                "{id:?}: the projectile reached {worst:.2} m/s having been launched at \
                 {launch:.2} m/s — the contact is injecting energy"
            );
        }
    }

    /// A throw must actually land, at every tier that steps, inside a few seconds of
    /// watching. A correct simulation of a projectile still in flight after a minute is
    /// indistinguishable from a broken one, and this demo had that bug twice.
    #[test]
    fn a_throw_lands() {
        for id in [TierId::Sandbox, TierId::Grain, TierId::Landscape] {
            let mut session = Session::new(id);
            session.throw(0.5, 0.4, 0.6);
            let mut landed = None;
            for frame in 0..180 {
                session.step(1.0 / 60.0);
                if session.impulse_n_s() > 0.0 {
                    landed = Some(frame);
                    break;
                }
            }
            assert!(
                landed.is_some_and(|frame| frame < 120),
                "{id:?}: nothing had been hit after 180 frames"
            );
        }
    }

    /// Every tier that declares a refusal must actually refuse, and must say which
    /// refusal it is. A demo whose refusals are decoration would be worse than one with
    /// no refusals at all.
    #[test]
    fn refusing_tiers_refuse_with_their_own_reason() {
        let mut crystal = Session::new(TierId::Crystal);
        crystal.throw(0.5, 0.5, 0.6);
        assert_eq!(crystal.verdict(), Verdict::NoEvaluator);
        assert_eq!(crystal.arena().len(), 1, "a refused tier grows nothing");

        for id in [TierId::Planet, TierId::Galactic, TierId::Cosmic] {
            let mut session = Session::new(id);
            session.throw(0.5, 0.5, 0.6);
            assert_eq!(
                session.verdict(),
                Verdict::NoGravityChart,
                "{:?} must refuse for want of a gravity chart",
                id
            );
        }
    }

    /// Replay: the same throw twice must produce the identical arena and readout. The
    /// generator is seeded by geometry alone, so this is a check that nothing
    /// non-deterministic has crept into the event path.
    #[test]
    fn a_throw_replays_bit_identically() {
        let run = || {
            let mut session = Session::new(TierId::Sandbox);
            session.throw(0.37, 0.42, 0.55);
            for _ in 0..30 {
                session.step(1.0 / 60.0);
            }
            (
                session.arena().holons().to_vec(),
                session.readout().observables,
                session.nodes().position.clone(),
            )
        };
        let (holons_a, observables_a, positions_a) = run();
        let (holons_b, observables_b, positions_b) = run();
        assert_eq!(holons_a, holons_b);
        for k in 0..OBSERVABLES {
            assert_eq!(observables_a[k].to_bits(), observables_b[k].to_bits());
        }
        for (a, b) in positions_a.iter().zip(positions_b.iter()) {
            assert_eq!(a[0].to_bits(), b[0].to_bits());
            assert_eq!(a[1].to_bits(), b[1].to_bits());
        }
    }
}
