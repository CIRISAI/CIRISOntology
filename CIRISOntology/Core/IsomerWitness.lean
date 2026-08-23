/-
CIRISOntology.Core.IsomerWitness — the fifth NonFactoring witness, and it is
data-named: nature's own pair of wholes agreeing under every counting view.

THE DATUM (NUBASE2020; Kondev–Wang–Huang–Naimi–Audi, Chin. Phys. C 45, 030001
(2021)). ¹⁸⁰Ta and ¹⁸⁰ᵐTa have the same proton count (Z = 73) and the same
neutron count (N = 107) — they agree under EVERY view computable from the
counting chart: Z, N, A = Z + N, the chemistry, the mass to leading order. They
differ in spin-parity (1⁺ against 9⁻), in energy (the isomer sits 77 keV up),
and — spectacularly — in fate: the GROUND state dies in hours (T½ ≈ 8.15 h),
while the isomer is the only observationally stable nuclear isomer in nature
(T½ > 10¹⁵ yr). The excited configuration outlives the ground one by better
than eighteen orders of magnitude. Numeric values are QUOTED from the
evaluation, not machine-checked against it; what the machine checks is the
SHAPE.

WHY IT ENTERS THE LAKE. This is the founding shape — two wholes agreeing under
every partial view, differing in the quantity — witnessed at the bottom of the
periodic table by a published measurement rather than by a constructed model.
The lake carries four witnesses (parity, CP phase, Record, exchange sign); this
is the fifth, and the first the data hands over gratis. Graded per the house
rule: a fifth instance of one shape is SCOPE, not a fifth confirmation.

THE ENGINE CONSEQUENCE, which is why M21 was staked. The descriptor-chain
review killed the (Z,N) state key (L15-i, DESCRIPTOR_CHAIN.md, dead-marked);
this file is the reason, mechanized: any descriptor keyed on the counting chart
is PROVABLY blind to the isomer — `spin_not_computable_from_counts` — so a
composition boundary exporting only (Z,N) silently loses a 77-keV ledger entry
and a 10¹⁵-year stability distinction. A tier boundary must carry more than the
counting chart, and this is the theorem-shaped version of that sentence.

SCOPE. A model brick: nuclides are records of three numbers here, and the spin
slot stands in for the full configuration datum. The file derives no nuclear
physics; the physics is NUBASE's. Kill, separable: if the evaluation's
identification is ever revised so that the two states differ in Z or N, the
witness names the wrong nuclide pair and this file is retracted to a
constructed-model example.
-/
import CIRISOntology.Core.NonFactoring

namespace CIRISOntology.Core.IsomerWitness

/-- A nuclide, as the counting chart plus the one datum the chart cannot see.
    `spinTwice` carries 2J so half-integer spins stay in ℕ (¹⁸⁰Ta's are integer;
    the doubling is for the type's honesty, not this witness). -/
structure Nuclide where
  z : ℕ
  n : ℕ
  spinTwice : ℕ

/-- ¹⁸⁰Ta, the ground state: Z 73, N 107, Jπ = 1⁺. -/
def ta180 : Nuclide := ⟨73, 107, 2⟩

/-- ¹⁸⁰ᵐTa, the isomer: same counts, Jπ = 9⁻. -/
def ta180m : Nuclide := ⟨73, 107, 18⟩

/-- The two counting views: proton count and neutron count. Every chart datum of
    the counting kind — A, charge, chemistry keys — factors through these two. -/
def countView : Fin 2 → Nuclide → ℕ
  | 0 => Nuclide.z
  | 1 => Nuclide.n

/-- **THE FIFTH WITNESS, data-named.** Spin does not factor through the counting
    views: the ground state and the isomer agree under both counts and differ in
    spin. -/
theorem nonfactoring_isomer :
    NonFactoring countView Nuclide.spinTwice := by
  refine ⟨ta180, ta180m, ?_, by decide⟩
  intro i
  fin_cases i <;> rfl

/-- The general consequence, free from the shape: no rule whatever computes the
    spin from the counting data. A descriptor keyed on (Z, N) is blind to the
    isomer BY THEOREM, which is why the (Z,N) state key is dead (L15-i). -/
theorem spin_not_computable_from_counts :
    ¬ ∃ g : (Fin 2 → ℕ) → ℕ,
        ∀ x : Nuclide, Nuclide.spinTwice x = g (fun i => countView i x) :=
  not_computable_of_nonFactoring _ _ nonfactoring_isomer

end CIRISOntology.Core.IsomerWitness
