//! Material traits and breakable relations for mechanical realizations.
//!
//! A material is not a second kind of object. [`MaterialBinding`] says that one holon
//! is interpreted through another, descriptor holon (for example, the holon named
//! "stone") by this mechanical chart. Likewise a connection is itself addressable as
//! a relation holon. This keeps bodies, descriptions, and bonds inside the same recursive
//! identity system while giving the Newtonian evaluator the constitutive numbers it
//! needs.

use crate::holon::NO_HOLON;

/// Isotropic small-strain properties read by a mechanical realization.
///
/// Values use SI units. A named material such as stone should normally be a measured,
/// warranted descriptor holon whose properties populate this chart; the illustrative
/// preset below is deliberately not a claim about every kind of stone.
///
/// Dissipation is split into two separately-warranted fields (amendment A5,
/// DESCRIPTOR_CHAIN.md §4.2): `material_damping_ratio` may carry only values with a
/// physics-tier ancestor, while `solver_damping_ratio` is named numerical
/// stabilization with no such ancestor. Restitution is deliberately NOT a field here:
/// it is a pair/velocity/geometry OUTCOME of a contact, so contact charts (for
/// example [`crate::mechanical::SphereContactModel`]) take it per contact pair.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct IsotropicMaterial {
    pub density_kg_m3: f64,
    pub young_modulus_pa: f64,
    pub poisson_ratio: f64,
    /// Intrinsic material dissipation as a viscous damping ratio, zeta = 1/(2Q).
    ///
    /// Physically warranted field: only values with a measured ancestry (resonant-bar /
    /// ultrasonic attenuation class benchmarks) belong here. For intrinsic dry granite
    /// the seismic/ultrasonic quality factor is Q ~ 1e2–1e3, so zeta ~ 5e-4–5e-3.
    pub material_damping_ratio: f64,
    /// Numerical stabilization for whatever discrete solver consumes this chart.
    ///
    /// UNWARRANTED BY ANY PHYSICS TIER, and named as such (A5). This is solver
    /// configuration, not a material constant: it has no benchmark ancestor and must
    /// never be exported as a property of the material. It exists so that solver
    /// damping is declared where it acts instead of wearing material-constant costume.
    pub solver_damping_ratio: f64,
    pub tensile_strength_pa: f64,
    pub compressive_strength_pa: f64,
    pub fracture_energy_j_m2: f64,
}

impl IsotropicMaterial {
    /// A demo CALIBRATION, not a specimen: these values match no named published
    /// granite record. The programme's ground-truth granite (Lac du Bonnet, Martin &
    /// Chandler 1994, Int. J. Rock Mech. Min. Sci. 31) measures 200±22 MPa uniaxial
    /// compressive strength against this preset's 95 MPa, so the preset must not be
    /// read as "granite" or as any warranted stone (coherence fix C4,
    /// DESCRIPTOR_CHAIN.md §4.2). It is a transparent set of stone-scale numbers that
    /// exercises the chart. A production descriptor resolves a warranted specimen
    /// record — a descriptor holon carrying Record provenance — before any claim
    /// rides on these values.
    pub const DEMO_CALIBRATION: Self = Self {
        density_kg_m3: 2_650.0,
        young_modulus_pa: 45.0e9,
        poisson_ratio: 0.24,
        // zeta = 1/(2Q) at Q ≈ 250, mid-band of the granite intrinsic Q ~ 1e2–1e3
        // attenuation literature (A5 warrant note above).
        material_damping_ratio: 2.0e-3,
        // The legacy `damping_ratio` 0.055 retained under its honest name: a solver
        // stabilization number with no physics ancestor (it is 1–2 orders more
        // dissipative than intrinsic granite permits).
        solver_damping_ratio: 0.055,
        tensile_strength_pa: 6.0e6,
        compressive_strength_pa: 95.0e6,
        fracture_energy_j_m2: 110.0,
    };

    pub fn validate(&self) -> Result<(), MaterialError> {
        let finite = self.density_kg_m3.is_finite()
            && self.young_modulus_pa.is_finite()
            && self.poisson_ratio.is_finite()
            && self.material_damping_ratio.is_finite()
            && self.solver_damping_ratio.is_finite()
            && self.tensile_strength_pa.is_finite()
            && self.compressive_strength_pa.is_finite()
            && self.fracture_energy_j_m2.is_finite();
        if !finite
            || self.density_kg_m3 <= 0.0
            || self.young_modulus_pa <= 0.0
            || !(-1.0..0.5).contains(&self.poisson_ratio)
            || !(0.0..1.0).contains(&self.material_damping_ratio)
            || self.solver_damping_ratio < 0.0
            || self.tensile_strength_pa <= 0.0
            || self.compressive_strength_pa <= 0.0
            || self.fracture_energy_j_m2 <= 0.0
        {
            return Err(MaterialError::InvalidMaterial);
        }
        Ok(())
    }
}

/// Mechanical interpretation of a "made of" relation. Both ends are ordinary holons.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct MaterialBinding {
    /// The body whose mechanical response is being evaluated.
    pub subject_holon: usize,
    /// A descriptor holon such as a warranted sample, grade, or named "stone" profile.
    pub descriptor_holon: usize,
    pub properties: IsotropicMaterial,
}

impl MaterialBinding {
    pub fn validate(&self) -> Result<(), MaterialError> {
        if self.subject_holon == NO_HOLON || self.descriptor_holon == NO_HOLON {
            return Err(MaterialError::InvalidHolon);
        }
        self.properties.validate()
    }
}

/// Bilinear cohesive-zone law for one connection between two holons.
///
/// Stiffness is force per opening, peak force starts softening, and fracture energy is
/// the total work required to fully separate this discrete connection. Lower peak force
/// or fracture energy is the precise meaning of "weakly connected" in this realization.
/// The friction coefficient governs the Coulomb slider on the closed, partially
/// decohered interface (see the regime table on [`CohesiveBond`]).
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct CohesiveLaw {
    pub stiffness_n_m: f64,
    pub damping_n_s_m: f64,
    pub peak_force_n: f64,
    pub fracture_energy_j: f64,
    /// Coulomb friction coefficient for the closed interface. Rock-joint values are
    /// Byerlee-class, 0.6–0.85; the T4 spec's McClintock–Walsh inversion of the demo
    /// strength ratio gives 0.74.
    pub friction_coefficient: f64,
}

impl CohesiveLaw {
    pub fn opening_at_peak(&self) -> f64 {
        self.peak_force_n / self.stiffness_n_m
    }

    pub fn opening_at_failure(&self) -> f64 {
        2.0 * self.fracture_energy_j / self.peak_force_n
    }

    pub fn validate(&self) -> Result<(), MaterialError> {
        let finite = self.stiffness_n_m.is_finite()
            && self.damping_n_s_m.is_finite()
            && self.peak_force_n.is_finite()
            && self.fracture_energy_j.is_finite()
            && self.friction_coefficient.is_finite();
        if !finite
            || self.stiffness_n_m <= 0.0
            || self.damping_n_s_m < 0.0
            || self.peak_force_n <= 0.0
            || self.fracture_energy_j <= 0.0
            || self.friction_coefficient < 0.0
            || self.opening_at_failure() <= self.opening_at_peak()
        {
            return Err(MaterialError::InvalidCohesiveLaw);
        }
        Ok(())
    }

    /// Scale resistance without changing the elastic stiffness of the adjoining matter.
    pub const fn weakened(self, strength: f64, toughness: f64) -> Self {
        Self {
            stiffness_n_m: self.stiffness_n_m,
            damping_n_s_m: self.damping_n_s_m,
            peak_force_n: self.peak_force_n * strength,
            fracture_energy_j: self.fracture_energy_j * toughness,
            friction_coefficient: self.friction_coefficient,
        }
    }
}

/// Stateful relation holon. Damage is irreversible: zero is intact and one is a crack.
///
/// # Interface ownership per (damage, contact-state) regime — amendment A3
///
/// Exactly ONE owner and ONE law govern each regime; there is no regime in which two
/// laws in two places act on the same interface, and the D = 1 handoff changes the
/// owner without a jump in the constitutive response:
///
/// | damage D  | contact state         | owner          | law |
/// |-----------|-----------------------|----------------|-----|
/// | D < 1     | open (extension ≥ 0)  | `CohesiveBond` | bilinear cohesive traction `(1−D)·(K·δ + c·δ̇)`, damage monotone in maximum opening |
/// | D < 1     | closed (extension < 0)| `CohesiveBond` | crack closure: FULL-stiffness compression `K·δ + c·δ̇` (compression is not degraded by opening-driven damage — closed crack faces bear load), plus a Coulomb slider capped at `D·μ·|F_n|` |
/// | D = 1     | any                   | contact solver | the bond returns zero forever; unilateral contact and friction `μ·|F_n|` between the now-free bodies belong to the contact solver |
///
/// The slider cap `D·μ·|F_n|` is the single-owner resolution of the previously
/// ambiguous 0 < D < 1 closed regime: it vanishes at D = 0 (a fully bonded interface
/// has no failed surface to slide on — tangential resistance there is carried by the
/// elastic network), and it tends to the contact solver's Coulomb capacity `μ·|F_n|`
/// as D → 1, so the ownership transfer at full failure is continuous. Damage `D` and
/// `maximum_opening_m` are Record-axis: irreversible history of the relation.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct CohesiveBond {
    pub relation_holon: usize,
    pub a_holon: usize,
    pub b_holon: usize,
    pub rest_length_m: f64,
    pub law: CohesiveLaw,
    damage: f64,
    maximum_opening_m: f64,
}

impl CohesiveBond {
    pub fn new(
        relation_holon: usize,
        a_holon: usize,
        b_holon: usize,
        rest_length_m: f64,
        law: CohesiveLaw,
    ) -> Result<Self, MaterialError> {
        if relation_holon == NO_HOLON
            || a_holon == NO_HOLON
            || b_holon == NO_HOLON
            || a_holon == b_holon
        {
            return Err(MaterialError::InvalidHolon);
        }
        if !rest_length_m.is_finite() || rest_length_m <= 0.0 {
            return Err(MaterialError::InvalidRestLength);
        }
        law.validate()?;
        Ok(Self {
            relation_holon,
            a_holon,
            b_holon,
            rest_length_m,
            law,
            damage: 0.0,
            maximum_opening_m: 0.0,
        })
    }

    pub const fn damage(&self) -> f64 {
        self.damage
    }

    pub const fn is_broken(&self) -> bool {
        self.damage >= 1.0
    }

    pub const fn maximum_opening_m(&self) -> f64 {
        self.maximum_opening_m
    }

    /// Advance irreversible damage and return the axial force magnitude along the bond
    /// direction (positive = tension pulling the endpoints together).
    ///
    /// This implements the normal-direction column of the regime table above: open
    /// bonds soften bilinearly, closed bonds carry FULL-stiffness compression (crack
    /// closure), and a fully broken relation returns zero — post-failure contact
    /// belongs to the contact solver, not to the failed bond.
    pub fn axial_force(&mut self, extension_m: f64, relative_speed_m_s: f64) -> f64 {
        if !extension_m.is_finite() || !relative_speed_m_s.is_finite() || self.is_broken() {
            return 0.0;
        }

        if extension_m < 0.0 {
            // CLOSED regime, bond owner: opening-driven damage does not degrade
            // compression, because the closed crack faces are back in contact.
            return self.law.stiffness_n_m * extension_m
                + self.law.damping_n_s_m * relative_speed_m_s;
        }

        let opening = extension_m;
        self.maximum_opening_m = self.maximum_opening_m.max(opening);
        let peak = self.law.opening_at_peak();
        let failure = self.law.opening_at_failure();
        if self.maximum_opening_m >= failure {
            self.damage = 1.0;
            return 0.0;
        }
        if self.maximum_opening_m > peak {
            // Standard bilinear cohesive damage: (1-D) K delta follows the descending
            // line from peak traction to zero at the failure opening.
            let target = failure * (self.maximum_opening_m - peak)
                / (self.maximum_opening_m * (failure - peak));
            self.damage = self.damage.max(target.clamp(0.0, 1.0));
        }

        let intact = 1.0 - self.damage;
        intact
            * (self.law.stiffness_n_m * extension_m + self.law.damping_n_s_m * relative_speed_m_s)
    }

    /// Coulomb slider on the closed, partially decohered interface (A3 regime table,
    /// tangential column). Returns a force magnitude ≥ 0 to be applied OPPOSITE the
    /// tangential sliding direction.
    ///
    /// `axial_force_n` is the value just returned by [`Self::axial_force`]; the slider
    /// engages only while it is compressive (the interface is closed). The capacity is
    /// `D·μ·|F_n|` — zero on an intact bond, the full contact-solver Coulomb capacity
    /// in the D → 1 limit — and the slider is viscosity-regularized for explicit
    /// integration using the law's damping coefficient: `min(c·|v_t|, D·μ·|F_n|)`.
    /// A broken bond returns zero: friction between separated bodies is owned by the
    /// contact solver.
    pub fn closed_friction_force(&self, axial_force_n: f64, tangential_speed_m_s: f64) -> f64 {
        if !axial_force_n.is_finite()
            || !tangential_speed_m_s.is_finite()
            || self.is_broken()
            || axial_force_n >= 0.0
        {
            return 0.0;
        }
        let capacity = self.damage * self.law.friction_coefficient * (-axial_force_n);
        let viscous = self.law.damping_n_s_m * tangential_speed_m_s.abs();
        viscous.min(capacity)
    }
}

/// Damage/Record tag carried by every rigid export: the summary of the relation
/// network's irreversible history. Damage and maximum openings are Record-axis, so
/// this tag is what keeps the past provable across the tier boundary.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct DamageRecord {
    pub bond_count: u32,
    pub broken_count: u32,
    pub mean_damage: f64,
    pub max_damage: f64,
    pub total_maximum_opening_m: f64,
}

impl DamageRecord {
    pub fn from_bonds<'a>(bonds: impl IntoIterator<Item = &'a CohesiveBond>) -> Self {
        let mut bond_count = 0u32;
        let mut broken_count = 0u32;
        let mut damage_sum = 0.0f64;
        let mut max_damage = 0.0f64;
        let mut total_maximum_opening_m = 0.0f64;
        for bond in bonds {
            bond_count += 1;
            if bond.is_broken() {
                broken_count += 1;
            }
            damage_sum += bond.damage();
            max_damage = max_damage.max(bond.damage());
            total_maximum_opening_m += bond.maximum_opening_m();
        }
        let mean_damage = if bond_count == 0 {
            0.0
        } else {
            damage_sum / bond_count as f64
        };
        Self {
            bond_count,
            broken_count,
            mean_damage,
            max_damage,
            total_maximum_opening_m,
        }
    }
}

/// The engine's OWN rigid chart over a bonded holon — amendment A4.
///
/// When a holon is healthy enough to be stepped as a rigid body, the export is THIS
/// chart over the SAME holon: the wall never stops being a holon by being certified
/// healthy. Rapier (or any external rigid-body engine) remains a limiting-case
/// CONTROL to compare against, never the definition of the export.
///
/// The tuple carries a [`DamageRecord`] tag. This instantiates
/// `repairable_does_not_factor` at the T4/T5 seam: a pristine wall and one pre-loaded
/// to 0.9 of critical (all D < 1) agree in every current-configuration view — same
/// mass, same geometry, empty crack observable `{r | D = 1}` — yet whether the
/// loading past can still be proven downstream depends on what the export retains.
/// Dropping the tag would make the two walls export identically, erasing the
/// provability of history at the tier boundary (misfit L18, repaired here).
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct RigidChartExport {
    pub subject_holon: usize,
    pub mass_kg: f64,
    pub record: DamageRecord,
}

impl RigidChartExport {
    pub fn over<'a>(
        subject_holon: usize,
        mass_kg: f64,
        bonds: impl IntoIterator<Item = &'a CohesiveBond>,
    ) -> Result<Self, MaterialError> {
        if subject_holon == NO_HOLON {
            return Err(MaterialError::InvalidHolon);
        }
        if !mass_kg.is_finite() || mass_kg <= 0.0 {
            return Err(MaterialError::InvalidMaterial);
        }
        Ok(Self {
            subject_holon,
            mass_kg,
            record: DamageRecord::from_bonds(bonds),
        })
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum MaterialError {
    InvalidHolon,
    InvalidMaterial,
    InvalidCohesiveLaw,
    InvalidRestLength,
}

#[cfg(test)]
mod tests {
    use super::*;

    fn strong_law() -> CohesiveLaw {
        CohesiveLaw {
            stiffness_n_m: 1_000.0,
            damping_n_s_m: 2.0,
            peak_force_n: 10.0,
            fracture_energy_j: 0.1,
            friction_coefficient: 0.74,
        }
    }

    #[test]
    fn stone_is_a_valid_mechanical_chart() {
        let binding = MaterialBinding {
            subject_holon: 7,
            descriptor_holon: 11,
            properties: IsotropicMaterial::DEMO_CALIBRATION,
        };
        assert_eq!(binding.validate(), Ok(()));
    }

    #[test]
    fn material_dissipation_sits_in_the_intrinsic_rock_band() {
        // A5: the physically warranted field must carry a value in the band its own
        // warrant states (granite Q ~ 1e2–1e3, zeta = 1/(2Q)), and the legacy solver
        // number must live outside that band under its honest name.
        let preset = IsotropicMaterial::DEMO_CALIBRATION;
        assert!((5.0e-4..=5.0e-3).contains(&preset.material_damping_ratio));
        assert!(preset.solver_damping_ratio > 5.0e-3);
        assert_eq!(preset.validate(), Ok(()));
    }

    #[test]
    fn weak_relation_fails_before_strong_relation() {
        let strong = strong_law();
        let weak = strong.weakened(0.4, 0.2);
        let mut strong_bond = CohesiveBond::new(20, 1, 2, 1.0, strong).unwrap();
        let mut weak_bond = CohesiveBond::new(21, 1, 2, 1.0, weak).unwrap();

        weak_bond.axial_force(0.011, 0.0);
        strong_bond.axial_force(0.011, 0.0);

        assert!(weak_bond.is_broken());
        assert!(!strong_bond.is_broken());
    }

    #[test]
    fn damage_is_irreversible() {
        let mut bond = CohesiveBond::new(20, 1, 2, 1.0, strong_law()).unwrap();
        bond.axial_force(0.015, 0.0);
        let damaged = bond.damage();
        bond.axial_force(0.0, 0.0);
        assert!(damaged > 0.0 && damaged < 1.0);
        assert_eq!(bond.damage(), damaged);
    }

    #[test]
    fn partially_damaged_closed_bond_has_one_owner() {
        // A3: the D ∈ (0,1) closed regime that was previously ambiguous. The bond is
        // the single owner: full-stiffness crack-closure compression plus a Coulomb
        // slider capped at D·μ·|F_n|. At D = 1 both channels return zero because the
        // contact solver takes ownership.
        let law = strong_law();
        let mut bond = CohesiveBond::new(20, 1, 2, 1.0, law).unwrap();
        bond.axial_force(0.015, 0.0);
        let damage = bond.damage();
        assert!(damage > 0.0 && damage < 1.0);

        // Crack closure: compression carries FULL stiffness, not (1-D)-scaled.
        let compressive = bond.axial_force(-0.004, 0.0);
        assert_eq!(compressive, -0.004 * law.stiffness_n_m);
        assert_eq!(bond.damage(), damage, "closure must not advance damage");

        // The slider saturates at the Coulomb capacity D·μ·|F_n| ...
        let capacity = damage * law.friction_coefficient * compressive.abs();
        let sliding = bond.closed_friction_force(compressive, 1.0e3);
        assert!((sliding - capacity).abs() <= 1.0e-12 * capacity);
        // ... is viscosity-regularized below it ...
        let creeping = bond.closed_friction_force(compressive, 1.0e-6);
        assert!(creeping > 0.0 && creeping < capacity);
        // ... and never engages in tension (the interface is open, cohesion owns it).
        assert_eq!(bond.closed_friction_force(5.0, 1.0e3), 0.0);

        // An intact bond has no failed surface to slide on: capacity is zero at D = 0.
        let intact = CohesiveBond::new(21, 1, 2, 1.0, law).unwrap();
        assert_eq!(intact.closed_friction_force(-4.0, 1.0e3), 0.0);

        // At D = 1 the bond owns nothing; post-failure contact and friction belong to
        // the contact solver.
        let mut broken = CohesiveBond::new(22, 1, 2, 1.0, law).unwrap();
        broken.axial_force(1.0, 0.0);
        assert!(broken.is_broken());
        assert_eq!(broken.axial_force(-0.004, 0.0), 0.0);
        assert_eq!(broken.closed_friction_force(-4.0, 1.0e3), 0.0);
    }

    #[test]
    fn subcritical_damage_reaches_the_rigid_export() {
        // A4: a pristine wall and one pre-loaded to 0.9 of critical (all D < 1) must
        // export DIFFERENTLY, and the difference must live entirely in the Record tag
        // — `repairable_does_not_factor` at the T4/T5 seam.
        let law = strong_law();
        let pristine = [
            CohesiveBond::new(20, 1, 2, 1.0, law).unwrap(),
            CohesiveBond::new(21, 2, 3, 1.0, law).unwrap(),
        ];
        let mut loaded = pristine;
        let peak = law.opening_at_peak();
        let failure = law.opening_at_failure();
        loaded[0].axial_force(peak + 0.9 * (failure - peak), 0.0);
        assert!(loaded[0].damage() > 0.0 && loaded[0].damage() < 1.0);

        let pristine_export = RigidChartExport::over(2, 100.0, pristine.iter()).unwrap();
        let loaded_export = RigidChartExport::over(2, 100.0, loaded.iter()).unwrap();

        // Every current-configuration view agrees ...
        assert_eq!(loaded_export.subject_holon, pristine_export.subject_holon);
        assert_eq!(loaded_export.mass_kg, pristine_export.mass_kg);
        assert_eq!(loaded_export.record.broken_count, 0);
        assert_eq!(
            loaded_export.record.bond_count,
            pristine_export.record.bond_count
        );
        // ... and the exports still differ, through the Record alone.
        assert_ne!(loaded_export, pristine_export);
        assert!(loaded_export.record.mean_damage > 0.0);
        assert!(loaded_export.record.max_damage < 1.0);

        // Determinism: re-exporting the same state is bit-identical.
        assert_eq!(
            RigidChartExport::over(2, 100.0, pristine.iter()).unwrap(),
            pristine_export
        );
    }
}
