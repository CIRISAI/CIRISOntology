//! The zoom ladder: which grain constant each tier declares, and what the REG+ ledger
//! will actually let it count.
//!
//! # The ladder is arithmetic, not taste
//!
//! `GrossState::constituents` is a `u64` and `Holon::grain_units` is a `u32`. Those two
//! integers decide how far one arena can zoom, and they bind hard:
//!
//! * a dense 3D scene fits `u64` only while `extent / g0 <= 2.642e6` — **6.42 decades**;
//! * `grain_units` is a diameter ratio, so no arena spans more than `4.295e9` — **9.63
//!   decades** — whatever its density.
//!
//! One 0.5 mm quartz grain is **5.216e18 atoms**, which leaves the ledger 3.54x of
//! headroom: it can count about three and a half grains of sand in atoms and no more.
//! The sandbox in this demo holds 6.60e8 grains; expressed in atoms that is 3.44e27,
//! which is **1.87e8 times** over the cap, and `GrossState::checked_combine` returns
//! `None` rather than a wrong number. The observable universe in atoms is over by 5.4e60.
//!
//! That refusal is the frame working, and it is why zoom here is a **re-root**: each
//! tier is its own arena with its own declared `g0`, which `CIRIS_HOLON_ENGINE.md`
//! already licenses ("There is no absolute maximal holon. A root can become a child when
//! a larger holarchy is formed"). Re-rooting is a VALUES change — a different grain
//! constant on the scene chart — not a new object, not a new field, not a second
//! ontology. [`Tier::ledger`] is that arithmetic made executable, and
//! [`Ledger::Overflows`] is what the demo shows when a user asks for a grain the ledger
//! cannot carry.
//!
//! # Square domains, and a debt that turned out not to be owed
//!
//! Every tier's domain is SQUARE, so the 2x2 quadtree halves both axes and cells stay
//! square at every depth. `ciris_sim_core::fracture::WallChart` is square-only and that
//! was on the list of debts to pay here; choosing square domains means the demo does not
//! need per-axis extents at all. A sandbox is a square domain with sand in the lower
//! part and air above — the air cells are ordinary holons carrying zero constituents,
//! and the ledger composes exactly through them. Building rectangular charts that
//! nothing uses would have been machinery, not payment.
//!
//! # Two dimensions on purpose
//!
//! The chart is 2D; the LEDGER is 3D. A tier's `constituents` is the real count of
//! physical terminal holons — grains, unit cells, galaxies — while the quadtree cells
//! are the resident refinement window over them. That split is the shipped demo's own
//! (`holon-ball-game` carries a 1,000,000-holon wall on 288 2D nodes) and it is stated
//! here rather than left for a reader to infer.

use ciris_sim_core::material::IsotropicMaterial;

/// Avogadro's constant, CODATA 2018 (exact by SI definition since 2019).
pub const AVOGADRO: f64 = 6.022_140_76e23;
/// Molar mass of SiO2, kg/mol.
pub const SIO2_MOLAR_MASS_KG: f64 = 0.060_08;
/// Atoms per SiO2 formula unit.
pub const SIO2_ATOMS_PER_UNIT: f64 = 3.0;

/// The eight zoom tiers, coarse index ascending outward from the gauge floor.
#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord)]
#[repr(u8)]
pub enum TierId {
    Gauge = 0,
    Crystal = 1,
    Grain = 2,
    Sandbox = 3,
    Landscape = 4,
    Planet = 5,
    Galactic = 6,
    Cosmic = 7,
}

impl TierId {
    pub const ALL: [TierId; 8] = [
        TierId::Gauge,
        TierId::Crystal,
        TierId::Grain,
        TierId::Sandbox,
        TierId::Landscape,
        TierId::Planet,
        TierId::Galactic,
        TierId::Cosmic,
    ];

    pub fn from_index(index: u32) -> Option<Self> {
        Self::ALL.get(index as usize).copied()
    }

    pub const fn index(self) -> u32 {
        self as u32
    }
}

/// What can actually be evaluated at a tier, today, in this repository.
///
/// Three of the eight tiers carry a refusal rather than an evaluator. That is not a
/// shortfall dressed up as a feature: each refusal names the specific open item that
/// produces it, and none of them can be removed by writing more code here.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Evaluator {
    /// Exact finite algebra: the one-plaquette U(1) quantum link.
    GaugePlaquette,
    /// Grain-on-grain unilateral contact with Coulomb friction.
    GranularContact,
    /// Bilinear cohesive relations with irreversible damage, over
    /// `ciris_sim_core::material::CohesiveBond`.
    Cohesive,
    /// No validated evaluator exists at this tier in this repository.
    Unavailable(Refusal),
}

/// Why a tier refuses, in the words of the document that owns the gap.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Refusal {
    /// T1/T2 are specification-only. There are no force constants in the tree, and the
    /// DFT elastic tensor is Phase 2 IN PROGRESS (`T2_DFT_REFERENCE.md`) — 12 strained
    /// -cell relaxations owed. Rendering a lattice from published cell parameters is
    /// data; running dynamics on it would be a number with no ancestor.
    NoValidatedEvaluator,
    /// `relativity.rs` is flat by design and contains no gravity. INTEGRATION_FRAME.md
    /// L29 states it plainly: every engine scene with weight is outside the T5
    /// certificate until the curved tier (A3) closes. A gravitating scene therefore has
    /// a ledger and no certified dynamics.
    NoGravityChart,
}

/// What the REG+ ledger says about a proposed (domain, grain) pair.
#[derive(Clone, Copy, Debug, PartialEq)]
pub enum Ledger {
    Fits {
        /// Terminal holons the scene claims.
        constituents: u64,
        /// `domain / g0`, the root's grain-unit count.
        grain_ratio: f64,
    },
    /// The constituent count exceeds `u64::MAX`. `factor` is how many times over.
    OverflowsConstituents { factor: f64 },
    /// `domain / g0` exceeds `u32::MAX`, so no root grain-unit count can express it.
    OverflowsGrainUnits { factor: f64 },
}

impl Ledger {
    pub const fn fits(&self) -> bool {
        matches!(self, Ledger::Fits { .. })
    }
}

/// One tier of the ladder. Every field is a VALUE on the same holon machinery; nothing
/// here is a per-tier type.
#[derive(Clone, Copy, Debug)]
pub struct Tier {
    pub id: TierId,
    pub name: &'static str,
    /// One line a general reader can hold on to.
    pub plain: &'static str,
    /// The declared grain constant in metres. `f64::NAN` at the gauge tier, where the
    /// lattice spacing is not pinned to any length and saying otherwise would invent a
    /// number.
    pub g0_m: f64,
    /// Side of the square domain, metres. `f64::NAN` at the gauge tier.
    pub domain_m: f64,
    /// Root grain-unit count: the domain measured in `g0`, rounded up to a power of two
    /// so the 2x2 quadtree bottoms out exactly at `g0`.
    pub root_grain_units: u32,
    /// Physical terminal holons in the whole scene — the 3D count, not the 2D cell
    /// count.
    pub constituents: u64,
    /// Fraction of the square domain's height occupied by matter. Air above carries
    /// zero constituents and composes exactly.
    pub fill: f64,
    pub evaluator: Evaluator,
    /// The chart values this tier's evaluator reads, where it has one.
    pub material: Option<IsotropicMaterial>,
    /// What the terminal holon at this tier IS, in plain words.
    pub terminal: &'static str,
}

/// Single-crystal alpha-quartz, as a grain's own chart values.
///
/// Provenance, per field, because a value with no ancestor is the thing this programme
/// exists to refuse:
/// * `young_modulus_pa` 95 GPa — the isotropic (Voigt-Reuss-Hill class) reduction of
///   the trigonal tensor in DESCRIPTOR_CHAIN.md §3.2 (C11 86.7-87.3, C33 105.8-107.2,
///   C44 57.2-58.2 GPa). It is a REDUCTION and it destroys C14 (~18 GPa) identically —
///   misfit L24, carried here rather than hidden: zooming to the crystal must MINT
///   anisotropy, never interpolate toward it.
/// * `fracture_energy_j_m2` 1.0 — twice the quartz surface energy, T2's exported
///   `gamma` 0.4-1.0 J/m^2 (§3.2), taken at 0.5. This is the TRANSPORTED value.
///   `IsotropicMaterial::DEMO_CALIBRATION` carries 110 J/m^2 at T4, and the 110x
///   difference is process-zone dissipation MINTED at the continuum tier (misfit
///   L23/M25). The two numbers are differently typed and the demo shows both.
/// * `tensile_strength_pa` 150 MPa — the middle of the §3.3 grain-strength range
///   50-300 MPa. In the running demo this field is REPLACED per grain by the quenched
///   Weibull draw, which is the whole point of the grain tier.
/// * `density_kg_m3` 2648 — the §3.2 pin.
/// * `poisson_ratio` 0.08 — quartz is anomalously low; a class value, flagged as such.
/// * `material_damping_ratio` 5.0e-4 — Q ~ 1e3 class warrant only, no specimen.
/// * `solver_damping_ratio` — solver stabilization, no physics ancestor, named as such
///   (amendment A5).
pub const QUARTZ_GRAIN: IsotropicMaterial = IsotropicMaterial {
    density_kg_m3: 2_648.0,
    young_modulus_pa: 95.0e9,
    poisson_ratio: 0.08,
    material_damping_ratio: 5.0e-4,
    solver_damping_ratio: 0.02,
    tensile_strength_pa: 150.0e6,
    compressive_strength_pa: 1.1e9,
    fracture_energy_j_m2: 1.0,
};

/// Diameter of the median sand grain in this sandbox, metres. Medium sand on the
/// Wentworth scale is 0.25-0.5 mm; 0.5 mm is its coarse edge and the `g0` of the
/// sandbox tier.
pub const SAND_GRAIN_M: f64 = 5.0e-4;

/// Atoms in one sphere of quartz of diameter `d`.
pub fn atoms_in_grain(diameter_m: f64) -> f64 {
    let volume = core::f64::consts::PI / 6.0 * diameter_m * diameter_m * diameter_m;
    let mass = volume * QUARTZ_GRAIN.density_kg_m3;
    mass / SIO2_MOLAR_MASS_KG * AVOGADRO * SIO2_ATOMS_PER_UNIT
}

/// What the ledger says about counting `domain_m` of dense matter in grains of `g0_m`.
///
/// `packing` is the volume fraction actually occupied (1.0 for a solid, ~0.6 for
/// randomly packed spheres). This is the executable form of the module header's
/// arithmetic, and [`Ledger::OverflowsConstituents`] is what the demo renders when a
/// user asks for a grain the tier cannot carry.
pub fn ledger_for(domain_m: f64, g0_m: f64, packing: f64) -> Ledger {
    let ratio = domain_m / g0_m;
    if !(ratio.is_finite() && ratio > 0.0) || ratio > u32::MAX as f64 {
        return Ledger::OverflowsGrainUnits {
            factor: ratio / u32::MAX as f64,
        };
    }
    let count = ratio * ratio * ratio * packing;
    if count > u64::MAX as f64 {
        return Ledger::OverflowsConstituents {
            factor: count / u64::MAX as f64,
        };
    }
    Ledger::Fits {
        constituents: count as u64,
        grain_ratio: ratio,
    }
}

/// Smallest power of two at or above `value`, saturating at `u32::MAX`'s highest power.
///
/// The ladder's `root_grain_units` are written out as literals rather than computed, so
/// that a typo is a test failure instead of a silently different scene. This is the
/// function `declared_root_grain_covers_the_domain` checks them against.
pub fn ceil_pow2(value: f64) -> u32 {
    if !(value.is_finite() && value > 1.0) {
        return 1;
    }
    let mut units: u32 = 1;
    while (units as f64) < value {
        match units.checked_mul(2) {
            Some(next) => units = next,
            None => return units,
        }
    }
    units
}

/// The ladder.
///
/// Two entries had to be RE-SIZED because the caps bit during construction, and both are
/// left visible in the numbers rather than smoothed away: a 1 m grain on Earth is 1.08e21
/// constituents (59x over `u64`), so the planet tier declares 10 m; and a 10 kpc grain on
/// the observable universe is 2.32e19 geometric cells (1.26x over), so the cosmic tier
/// declares 40 kpc. A ladder chosen for looks would not have been bent twice by
/// arithmetic.
pub fn tiers() -> [Tier; 8] {
    [
        Tier {
            id: TierId::Gauge,
            name: "gauge",
            plain: "One square of the vacuum's own bookkeeping: four links carrying \
                    electric flux, and a rule that says how much is allowed to meet at \
                    a corner.",
            g0_m: f64::NAN,
            domain_m: f64::NAN,
            root_grain_units: 1,
            constituents: 4,
            fill: 1.0,
            evaluator: Evaluator::GaugePlaquette,
            material: None,
            terminal: "one oriented link",
        },
        Tier {
            id: TierId::Crystal,
            name: "crystal",
            plain: "A speck of quartz one micrometre across, drawn as the repeating \
                    unit cell it is really made of.",
            g0_m: 4.913_4e-10,
            domain_m: 1.0e-6,
            root_grain_units: 2048,
            constituents: 8_430_000_000,
            fill: 1.0,
            evaluator: Evaluator::Unavailable(Refusal::NoValidatedEvaluator),
            material: None,
            terminal: "one alpha-quartz unit cell",
        },
        Tier {
            id: TierId::Grain,
            name: "grain",
            plain: "One grain of sand, half a millimetre across, and the flaws inside \
                    it that decide how it breaks.",
            g0_m: 1.0e-6,
            domain_m: SAND_GRAIN_M,
            root_grain_units: 512,
            constituents: 125_000_000,
            fill: 1.0,
            evaluator: Evaluator::Cohesive,
            material: Some(QUARTZ_GRAIN),
            terminal: "one micrometre of crystal",
        },
        Tier {
            id: TierId::Sandbox,
            name: "sandbox",
            plain: "Sand, in a box. Throw something at it and the grains move because \
                    they push on each other, not because anything was animated.",
            g0_m: SAND_GRAIN_M,
            domain_m: 0.6,
            root_grain_units: 2048,
            constituents: 622_080_000,
            fill: 0.45,
            evaluator: Evaluator::GranularContact,
            material: Some(QUARTZ_GRAIN),
            terminal: "one grain of sand",
        },
        Tier {
            id: TierId::Landscape,
            name: "landscape",
            plain: "Two kilometres of stone ground. This is the tier the engine's \
                    fracture work was actually built and gated for.",
            g0_m: 1.0e-2,
            domain_m: 2.0e3,
            root_grain_units: 262_144,
            constituents: 4_800_000_000_000_000,
            fill: 0.6,
            evaluator: Evaluator::Cohesive,
            material: Some(IsotropicMaterial::DEMO_CALIBRATION),
            terminal: "one centimetre of rock",
        },
        Tier {
            id: TierId::Planet,
            name: "planet",
            plain: "The Earth, counted in ten-metre blocks. It has a ledger and a \
                    weight, and this engine has no certified way to make weight pull.",
            g0_m: 1.0e1,
            domain_m: 1.274_2e7,
            root_grain_units: 2_097_152,
            constituents: 1_083_000_000_000_000_000,
            fill: 1.0,
            evaluator: Evaluator::Unavailable(Refusal::NoGravityChart),
            material: Some(IsotropicMaterial::DEMO_CALIBRATION),
            terminal: "one ten-metre block",
        },
        Tier {
            id: TierId::Galactic,
            name: "galactic",
            plain: "The Milky Way, counted in stars. A hundred billion of them fit in \
                    the ledger with room to spare, because space is mostly empty.",
            g0_m: 3.085_7e16,
            domain_m: 9.46e20,
            root_grain_units: 32_768,
            constituents: 100_000_000_000,
            fill: 1.0,
            evaluator: Evaluator::Unavailable(Refusal::NoGravityChart),
            material: None,
            terminal: "one star",
        },
        Tier {
            id: TierId::Cosmic,
            name: "cosmic",
            plain: "Everything we can see, counted in galaxies: two trillion of them, \
                    which the same ledger carries without complaint.",
            g0_m: 1.2e21,
            domain_m: 8.8e26,
            root_grain_units: 1_048_576,
            constituents: 2_000_000_000_000,
            fill: 1.0,
            evaluator: Evaluator::Unavailable(Refusal::NoGravityChart),
            material: None,
            terminal: "one galaxy",
        },
    ]
}

pub fn tier(id: TierId) -> Tier {
    tiers()[id.index() as usize]
}

impl Tier {
    /// What the ledger says about this tier as declared.
    pub fn ledger(&self) -> Ledger {
        if !self.domain_m.is_finite() {
            return Ledger::Fits {
                constituents: self.constituents,
                grain_ratio: 1.0,
            };
        }
        ledger_for(self.domain_m, self.g0_m, self.fill)
    }

    /// What the ledger says if this tier's domain is counted in ATOMS instead of its
    /// declared grain. This is the demo's zoom-out refusal, computed rather than
    /// asserted: ask for the sandbox in atoms and the answer is a number of times over
    /// the cap, not a count.
    pub fn ledger_in_atoms(&self) -> Ledger {
        if !self.domain_m.is_finite() {
            return Ledger::OverflowsGrainUnits { factor: f64::NAN };
        }
        // One atom of quartz, as an equivalent sphere diameter: the cube root of the
        // volume per atom. This is a size, not a claim about atomic structure.
        let volume_per_atom = SIO2_MOLAR_MASS_KG
            / (SIO2_ATOMS_PER_UNIT * AVOGADRO * QUARTZ_GRAIN.density_kg_m3);
        let atom_m = volume_per_atom.cbrt();
        ledger_for(self.domain_m, atom_m, self.fill)
    }

    /// `l_ch = E * G_F / f_t^2` for this tier's chart values: the length over which a
    /// crack in this material hands its energy over. `None` where the tier has no
    /// material chart.
    ///
    /// This one formula, evaluated on each tier's own VALUES, is what makes the tiers
    /// disagree. At the landscape tier it is 13.75 cm, so the process zone it demands
    /// (a tenth of that) is 27x COARSER than a grain of sand — the continuum chart
    /// cannot see a grain at all. At the grain tier it is 4.2 um, so the demand is
    /// sub-micrometre: below that tier's own floor.
    pub fn characteristic_length_m(&self) -> Option<f64> {
        let material = self.material?;
        Some(
            material.young_modulus_pa * material.fracture_energy_j_m2
                / (material.tensile_strength_pa * material.tensile_strength_pa),
        )
    }

    /// The cell spacing this tier's claim demands where the interaction is.
    ///
    /// The demand depends on WHAT IS BEING CLAIMED, and the two tiers that run claim
    /// different things:
    ///
    /// * a COHESIVE tier claims a crack path and a work of fracture, so it must resolve
    ///   the process zone: `l_ch / 10`, the requirement DESCRIPTOR_CHAIN.md §3.4 states
    ///   and `fracture.rs` enforces;
    /// * a GRANULAR tier claims a contact impulse between grains, so it must resolve a
    ///   GRAIN: `g0`. A cell coarser than one grain cannot represent grains moving past
    ///   each other, and a cell finer than one does not exist.
    ///
    /// Using `l_ch / 10` at the sandbox would demand 0.42 um cells of a tier whose
    /// terminal holon is 500 um, and the honest answer to that demand is `GrainFloor`
    /// forever. That is the right answer to the WRONG QUESTION: the sandbox is not
    /// claiming a crack, because at 0.5 mm cells the homogenizer has already refused it
    /// a cohesive law (`scene::relation_law`). The surrogate follows the claim.
    pub fn required_spacing_m(&self) -> Option<f64> {
        match self.evaluator {
            Evaluator::GranularContact => Some(self.g0_m),
            Evaluator::Cohesive => Some(self.characteristic_length_m()? / 10.0),
            Evaluator::GaugePlaquette | Evaluator::Unavailable(_) => None,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn every_declared_tier_fits_the_ledger() {
        for tier in tiers() {
            assert!(
                tier.ledger().fits(),
                "{} does not fit the REG+ ledger: {:?}",
                tier.name,
                tier.ledger()
            );
            assert!(
                tier.constituents <= u64::MAX,
                "{} constituent count is not representable",
                tier.name
            );
        }
    }

    #[test]
    fn declared_root_grain_covers_the_domain() {
        for tier in tiers() {
            if !tier.domain_m.is_finite() {
                continue;
            }
            let needed = ceil_pow2(tier.domain_m / tier.g0_m);
            assert_eq!(
                tier.root_grain_units, needed,
                "{}: root grain {} is not the power of two covering {} / {}",
                tier.name, tier.root_grain_units, tier.domain_m, tier.g0_m
            );
        }
    }

    /// The finding the whole ladder is built on, as a test rather than a claim.
    #[test]
    fn a_grain_of_sand_nearly_exhausts_the_ledger_in_atoms() {
        let atoms = atoms_in_grain(SAND_GRAIN_M);
        assert!(
            (atoms / 5.216e18 - 1.0).abs() < 0.01,
            "one 0.5 mm quartz grain should be ~5.216e18 atoms, got {atoms:e}"
        );
        let headroom = u64::MAX as f64 / atoms;
        assert!(
            (3.0..4.0).contains(&headroom),
            "the ledger should hold ~3.5 grains of sand in atoms, got {headroom:.2}"
        );
    }

    /// Mutation of the ledger gate: a tier that asks for a grain the ledger cannot
    /// carry must be REFUSED with the overflow factor, never silently truncated. The
    /// sandbox in atoms is the case that motivated the whole re-rooting design, so it
    /// is the one planted here.
    #[test]
    fn counting_a_tier_in_atoms_is_refused_with_its_factor() {
        let sandbox = tier(TierId::Sandbox);
        match sandbox.ledger_in_atoms() {
            Ledger::OverflowsConstituents { factor } => assert!(
                (1.0e8..1.0e9).contains(&factor),
                "the sandbox in atoms should be ~1.9e8x over the u64 ledger, got {factor:e}"
            ),
            other => panic!("the sandbox in atoms must overflow the ledger, got {other:?}"),
        }

        // And the refusal is not universal, which is what makes it informative: the
        // grain tier's own domain IS countable in atoms, with the headroom above.
        assert!(
            tier(TierId::Grain).ledger_in_atoms().fits(),
            "one grain of sand must still be countable in atoms"
        );
    }

    /// The 110x jump in fracture energy between the crystal-derived value and the
    /// continuum one is MINTED at the continuum tier, not transported (misfit L23/M25).
    /// A zoom UI that interpolated between them would be inventing a number, so the gap
    /// is pinned here.
    #[test]
    fn fracture_energy_is_minted_not_transported() {
        let grain = tier(TierId::Grain).material.unwrap();
        let landscape = tier(TierId::Landscape).material.unwrap();
        let ratio = landscape.fracture_energy_j_m2 / grain.fracture_energy_j_m2;
        assert!(
            (100.0..120.0).contains(&ratio),
            "the transported-to-minted fracture-energy gap should be ~110x, got {ratio:.0}x"
        );
    }

    /// The single arithmetic fact the demo is built around: the continuum chart's
    /// process zone is COARSER than a grain of sand, so sand cannot be cracked by that
    /// chart and must be contacted instead.
    #[test]
    fn the_continuum_chart_cannot_resolve_a_grain_of_sand() {
        let required = tier(TierId::Landscape).required_spacing_m().unwrap();
        assert!(
            required > SAND_GRAIN_M * 20.0,
            "the landscape chart's finest legal cell ({required:.4} m) should be far \
             coarser than a {SAND_GRAIN_M} m grain"
        );
        // And the grain tier's own demand is far finer than that tier's floor, which is
        // the reason its verdict is a refusal rather than a certificate.
        let grain_required = tier(TierId::Grain).required_spacing_m().unwrap();
        assert!(
            grain_required < tier(TierId::Grain).g0_m,
            "the grain chart should demand ({grain_required:e} m) finer than its own \
             grain floor ({:e} m)",
            tier(TierId::Grain).g0_m
        );
    }

    /// The granular tier asks a question it can answer and the cohesive tiers ask one
    /// they may not be able to. Both are the same surrogate; only the length differs,
    /// and the length follows from the claim.
    #[test]
    fn the_demand_follows_the_claim() {
        let sandbox = tier(TierId::Sandbox);
        assert_eq!(sandbox.required_spacing_m(), Some(sandbox.g0_m));
        // Had the sandbox been asked the cohesive question instead, its demand would be
        // three orders finer than its own terminal holon — which is exactly why asking
        // it would be the wrong question, not a stricter one.
        let cohesive_demand = sandbox.characteristic_length_m().unwrap() / 10.0;
        assert!(
            sandbox.g0_m / cohesive_demand > 1000.0,
            "the cohesive demand should be ~1184x finer than a grain, got {:.0}x",
            sandbox.g0_m / cohesive_demand
        );

        let landscape = tier(TierId::Landscape);
        assert_eq!(
            landscape.required_spacing_m(),
            Some(landscape.characteristic_length_m().unwrap() / 10.0)
        );
    }

    #[test]
    fn three_tiers_refuse_and_each_names_why() {
        let refusing: Vec<_> = tiers()
            .into_iter()
            .filter(|tier| matches!(tier.evaluator, Evaluator::Unavailable(_)))
            .map(|tier| (tier.id, tier.evaluator))
            .collect();
        assert_eq!(refusing.len(), 4, "refusing tiers: {refusing:?}");
        assert_eq!(
            refusing[0].1,
            Evaluator::Unavailable(Refusal::NoValidatedEvaluator)
        );
        for (_, evaluator) in &refusing[1..] {
            assert_eq!(*evaluator, Evaluator::Unavailable(Refusal::NoGravityChart));
        }
    }
}
