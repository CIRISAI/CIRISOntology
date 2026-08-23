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
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct IsotropicMaterial {
    pub density_kg_m3: f64,
    pub young_modulus_pa: f64,
    pub poisson_ratio: f64,
    pub damping_ratio: f64,
    pub restitution: f64,
    pub tensile_strength_pa: f64,
    pub compressive_strength_pa: f64,
    pub fracture_energy_j_m2: f64,
}

impl IsotropicMaterial {
    /// A transparent demo calibration for dense building stone. Production descriptors
    /// should be populated from a specimen or warranted material record.
    pub const DEMO_STONE: Self = Self {
        density_kg_m3: 2_650.0,
        young_modulus_pa: 45.0e9,
        poisson_ratio: 0.24,
        damping_ratio: 0.055,
        restitution: 0.32,
        tensile_strength_pa: 6.0e6,
        compressive_strength_pa: 95.0e6,
        fracture_energy_j_m2: 110.0,
    };

    pub fn validate(&self) -> Result<(), MaterialError> {
        let finite = self.density_kg_m3.is_finite()
            && self.young_modulus_pa.is_finite()
            && self.poisson_ratio.is_finite()
            && self.damping_ratio.is_finite()
            && self.restitution.is_finite()
            && self.tensile_strength_pa.is_finite()
            && self.compressive_strength_pa.is_finite()
            && self.fracture_energy_j_m2.is_finite();
        if !finite
            || self.density_kg_m3 <= 0.0
            || self.young_modulus_pa <= 0.0
            || !(-1.0..0.5).contains(&self.poisson_ratio)
            || self.damping_ratio < 0.0
            || !(0.0..=1.0).contains(&self.restitution)
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
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct CohesiveLaw {
    pub stiffness_n_m: f64,
    pub damping_n_s_m: f64,
    pub peak_force_n: f64,
    pub fracture_energy_j: f64,
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
            && self.fracture_energy_j.is_finite();
        if !finite
            || self.stiffness_n_m <= 0.0
            || self.damping_n_s_m < 0.0
            || self.peak_force_n <= 0.0
            || self.fracture_energy_j <= 0.0
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
        }
    }
}

/// Stateful relation holon. Damage is irreversible: zero is intact and one is a crack.
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

    /// Advance irreversible damage and return tensile force magnitude. Compression is
    /// intentionally not transmitted by a fully broken relation; body contact belongs to
    /// the contact solver, not to the failed bond.
    pub fn axial_force(&mut self, extension_m: f64, relative_speed_m_s: f64) -> f64 {
        if !extension_m.is_finite() || !relative_speed_m_s.is_finite() || self.is_broken() {
            return 0.0;
        }

        let opening = extension_m.max(0.0);
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
        }
    }

    #[test]
    fn stone_is_a_valid_mechanical_chart() {
        let binding = MaterialBinding {
            subject_holon: 7,
            descriptor_holon: 11,
            properties: IsotropicMaterial::DEMO_STONE,
        };
        assert_eq!(binding.validate(), Ok(()));
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
}
