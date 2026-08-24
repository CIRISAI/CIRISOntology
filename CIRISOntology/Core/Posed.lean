/-
CIRISOntology.Core.Posed — a campaign is two problems, and the cheap one is a
witness pair: the two-solve rule, typed.

WHAT FORCED IT (Eric's question, 2026-08-23/24: "two solve — any way to look at
it as solving 2 problems also?"). The season paid for the same lesson three
times: Q5 staked a campaign on a sweep axis the chart's error did not vary
along; Q7 staked one on a spatial axis honesty did not vary across; the Q8
grids were staked on a compute budget nobody had probed. Q7b then bought with
two Lanczos solves what two full campaigns had paid to learn, and the house
rule became: MEASURE THE SPREAD FIRST. This file is that rule's type.

THE TWO PROBLEMS, and they differ in logical kind:

  * P_object — the campaign's question: universal, quantitative, over the whole
    design. Expensive: you pay the grid.
  * P_instrument — whether the design POSES the question at all: existential,
    a witness pair. Cheap: two points. `Poses` below.

Why two and not one is a theorem, not a habit: one point fixes a value; only
two witness a difference; and a question exists only over a difference the
design can see (`not_poses_subsingleton` — no subsingleton design poses
anything). The verdict of a campaign is then a Σ-pair — (the question is
posed, the answer) — and the two failure modes the record already uses are the
two components failing separately: VOID is the first component absent (the
Strawsonian truth-value gap), KILLED is the first present and the second
negative. `Outcome` and `outcome_void_iff_not_posed` state that VOID and
KILLED can never be conflated again.

THE DRY OBSERVATION, which is why this costs thirty lines and not a theory:
`Poses` is the lake's founding witness-pair shape pointed at the experiment
itself. Negatively, `SeparatesFiber` kills factoring claims — two states alike
under every view, differing in the quantity. Positively, the SAME pair licenses
a campaign: two configurations the design distinguishes in the staked contrast.
`poses_iff_separatesFiber` makes the identification exact: a design poses a
contrast iff the contrast separates a fiber of the trivial summary restricted
to the design. One shape, both signs — the same duality as
`Core/Locality` (what fails to factor is the Logos; what factors is
simulable), now at the level of method.

CREDIT. Strawson (1950) for presupposition and the truth-value gap that VOID
mechanizes; Fisher — identifiability as nonzero information along the contrast,
of which the two-point pre-check is the finite form; Bateson ("a difference
that makes a difference") for the sentence this file types. The engine faces
are Q7b's G7-FIT and spread pre-check and Q8's environment-probe lesson
(`sim_engine/Q7B_SEAM_PREREG.md`, `Q8_MPS_PREREG.md`); each is an instance,
none is re-argued here.

SCOPE. A model brick about DESIGNS, not about the world: `Poses` says the
design can see a difference, not that the difference matters, and a posed
question can still be answered badly. Kill, separable: exhibit a campaign
whose design provably poses its contrast by this definition and which is
nonetheless VOID for a reason of posedness (not power, not exactness) — then
witness-pair posedness is the wrong formalization of "the question was asked"
and this file's reading of VOID is retired.
-/
import CIRISOntology.Core.Coordination
import Mathlib.Tactic

namespace CIRISOntology.Core.Posed

variable {C V A : Type*}

/-- **P_instrument.** A design (the set of configurations a campaign will run)
    POSES a contrast when it holds a witness pair: two configurations the
    contrast tells apart. Existential, two points, cheap — the two-solve rule
    is exhibiting this witness. -/
def Poses (design : Set C) (contrast : C → V) : Prop :=
  ∃ a ∈ design, ∃ b ∈ design, contrast a ≠ contrast b

/-- **One point fixes a value; two witness a difference.** No subsingleton
    design poses anything — the "two" in two-solve is arithmetic, not habit. -/
theorem not_poses_subsingleton {design : Set C} (h : design.Subsingleton)
    (contrast : C → V) : ¬ Poses design contrast := by
  rintro ⟨a, ha, b, hb, hab⟩
  exact hab (congrArg contrast (h ha hb))

/-- A contrast constant on the design is never posed — the Q5/Q7 failure mode,
    as the definition's contrapositive. -/
theorem not_poses_of_constant {design : Set C} {contrast : C → V}
    (h : ∀ a ∈ design, ∀ b ∈ design, contrast a = contrast b) :
    ¬ Poses design contrast := by
  rintro ⟨a, ha, b, hb, hab⟩
  exact hab (h a ha b hb)

/-- Posedness is monotone in the design: enlarging the family never un-poses a
    question. (The converse move — shrinking to a subfamily — is what silently
    VOIDs campaigns.) -/
theorem poses_mono {d₁ d₂ : Set C} (h : d₁ ⊆ d₂) {contrast : C → V}
    (hp : Poses d₁ contrast) : Poses d₂ contrast := by
  obtain ⟨a, ha, b, hb, hab⟩ := hp
  exact ⟨a, h ha, b, h hb, hab⟩

/-- **THE DRY BRIDGE.** Posing a contrast IS the lake's founding witness-pair
    shape, run on the design: the contrast separates a fiber of the trivial
    summary on the design's subtype. Negatively the pair kills factoring
    claims; positively it licenses campaigns. One shape, both signs. -/
theorem poses_iff_separatesFiber (design : Set C) (contrast : C → V) :
    Poses design contrast ↔
      SeparatesFiber (fun _ : design => ()) (fun x : design => contrast x.val) := by
  constructor
  · rintro ⟨a, ha, b, hb, hab⟩
    exact ⟨⟨a, ha⟩, ⟨b, hb⟩, rfl, hab⟩
  · rintro ⟨x, y, _, hxy⟩
    exact ⟨x.val, x.property, y.val, y.property, hxy⟩

/-! ### The verdict is a Σ-pair, and VOID ≠ KILLED is typed -/

/-- A campaign's outcome: the two failure modes fail DIFFERENT components of
    the pair (posedness, answer). -/
inductive Outcome
  | void       -- the question was never posed: P_instrument failed
  | killed     -- posed, and the answer is no
  | supported  -- posed, and the answer is yes
  deriving DecidableEq

open Classical in
/-- The adjudication rule: VOID exactly when the design does not pose the
    contrast; otherwise the answer decides. Stated as a definition so a
    prereg's outcome table is this function and nothing else. -/
noncomputable def adjudicate (design : Set C) (contrast : C → V)
    (answer : Prop) : Outcome :=
  if Poses design contrast then (if answer then .supported else .killed)
  else .void

/-- **VOID and KILLED can never be conflated**: the adjudication returns VOID
    iff posedness failed — independent of the answer. A kill can only fire on
    a posed question, which is G7-FIT's clause as a theorem. -/
theorem adjudicate_void_iff (design : Set C) (contrast : C → V) (answer : Prop) :
    adjudicate design contrast answer = .void ↔ ¬ Poses design contrast := by
  classical
  unfold adjudicate
  by_cases hp : Poses design contrast <;> by_cases ha : answer <;> simp [hp, ha]

/-- And a kill really is a kill: on a posed design, the adjudication is never
    VOID, so a fired kill cannot be explained away as an unposed question. -/
theorem adjudicate_ne_void_of_posed {design : Set C} {contrast : C → V}
    (hp : Poses design contrast) (answer : Prop) :
    adjudicate design contrast answer ≠ .void := by
  rw [Ne, adjudicate_void_iff]
  exact fun h => h hp

end CIRISOntology.Core.Posed
