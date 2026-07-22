/-
CIRISOntology.Core.Provenance — what the instrument structurally cannot tell you.

THE PROVENANCE LINE. `S` is a functional of a correlation matrix. Any datum
about how that matrix was CONSTRUCTED — the scale of the variables, their
marginals, the statistics of the underlying state space, the partition of the
system into units — is not a function of the matrix, hence not a function of
`S`. Any claimed derivation of such a datum from the instrument alone is a
structural error and is rejected on sight.

THE CONTRAPOSITIVE IS THE POSITIVE CONTENT. Legitimate predictions from this
instrument are dimensionless, marginal-free and partition-declared: statements
about the SHAPE of dependence, nothing else. A prediction that requires a scale
requires an external bridge constant, and that constant is owed, not derived.

This file proves one theorem — an instance of `not_computable_from` — and records
the four classes of upstream datum. It asserts nothing about physics.
-/
import CIRISOntology.Core.Coordination

namespace CIRISOntology.Core

/-- An UPSTREAM datum: one that separates two states presenting the same
    correlation matrix. Equivalently, a fact about the construction of `C`
    rather than a fact about `C`. -/
def Upstream {State Corr Datum : Type*}
    (toCorr : State → Corr) (d : State → Datum) : Prop :=
  SeparatesFiber toCorr d

/-- THE PROVENANCE LINE: no upstream datum is computable from the correlation
    matrix, hence none is computable from `S` or any statistic derived from it.
    A direct instance of the domain argument. -/
theorem provenance_line {State Corr Datum : Type*}
    (toCorr : State → Corr) (d : State → Datum) (h : Upstream toCorr d) :
    ¬ ∃ g : Corr → Datum, ∀ x, d x = g (toCorr x) :=
  not_computable_from toCorr d h

/-- The four classes of upstream datum, recorded. Each is a fact about
    construction, not about dependence shape; each is therefore outside the
    instrument's range by `provenance_line`. -/
structure UpstreamClasses where
  /-- SCALE. No masses, no energy densities, no bridge constant. A dimensionful
      output requires an external marriage to a unit scale, which is owed and
      declared, never derived. -/
  scale_is_not_derivable : True
  /-- MARGINALS. No ratios of magnitudes and no coupling strengths, even
      dimensionless ones — the normalization has already discarded them. -/
  marginals_are_not_derivable : True
  /-- STATE-SPACE CONSTRUCTION. The statistics of the underlying state space are
      an INPUT whose consequences the instrument reads; they are not an output. -/
  statistics_are_input_not_output : True
  /-- PARTITION. Which degrees of freedom count as one unit is a choice made
      before the instrument is applied. It is declared, and it is the single
      largest source of silent error. -/
  partition_is_declared_not_discovered : True

/-- The upstream classes are recorded. -/
def upstream_classes : UpstreamClasses :=
  ⟨trivial, trivial, trivial, trivial⟩

end CIRISOntology.Core
