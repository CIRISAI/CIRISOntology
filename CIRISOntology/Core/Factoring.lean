/-
CIRISOntology.Core.Factoring — the one relation, and six predicates that were
its faces; with the two residues reported as loudly as the unification.

WHAT THIS IS (Eric, 2026-08-24: "the shape is an overcomplicated projection of
the underlying simple object"). The lake's DRY passes kept converging on one
relation between views of a world:

    Factors u v  ≔  ∃ h, u = h ∘ v      "everything u knows, v determines"

This file defines it once and re-derives, as instances or equivalences, the
predicates the season built separately: the frame order (`CoarserThan`), the
domain argument's separation (`SeparatesFiber`, via a completeness bridge),
posedness (`Poses`), the whole-only shape (`NonFactoring`, through the joint
view), the stationarity ideal (`StationarityAudit`), and grain admissibility
(on nested ladders — see residue R1). The philological names are positions in
the order this relation induces; `OBJECT.md` carries the full dictionary.

THE CENTRAL LEMMA is the completeness bridge `factors_iff_not_separatesFiber`:
a quantity factors through a view EXACTLY WHEN no witness pair separates a
fiber. The lake's negative results (five NonFactoring witnesses) and its
positive licenses (Posed's two-solve) are the two signs of one biconditional.

THE TWO RESIDUES — the unification was staked with "a predicate that resists
is a discovery", and two did, both small and both informative:

  R1. ADMISSIBILITY IS FACTORING ONLY ON NESTED LADDERS. On a dyadic grain
      ladder the threshold order IS the factoring order
      (`grainFactors_iff_le`): coarser-scale views factor through finer ones
      exactly when the scales nest. But two UNRELATED scales (1.5 vs 2) do
      not factor in either direction even when ≤ holds — factoring is a
      partial order on views, thresholds are a total order on lengths, and
      they agree only along a nested chain. The engine's charts nest BY
      CONSTRUCTION (the octree), which is why `GrainFloor`'s threshold model
      is faithful within one re-root ladder — and the failure of factoring
      ACROSS ladders is the order-theoretic reason certificates do not
      transport across re-roots. G4 was never an engineering accident; it is
      what non-comparability in this order looks like from inside.
  R2. THE STATIONARITY IDEAL NEEDS ONE PRIMITIVE BEYOND FACTORS: a POINTING.
      `StationarityAudit g A` is `Factors A g` PLUS `φ 0 = 0` — membership in
      the pointed part of the factoring cone over the residual. So the object
      has, besides its order, one distinguished point per audit codomain (the
      "reads clean" value). One relation and one pointing; not one relation.

SCOPE. Model bricks over arbitrary types; the dyadic ladder stands in for the
engine's nested charts. Kill, separable: exhibit one of the six predicates
whose intended use is NOT captured by its equivalence here (a use that the
Factors reading provably mis-adjudicates), and that predicate returns to
primitive status with the miss recorded.
-/
import CIRISOntology.Core.Coordination
import CIRISOntology.Core.FrameAxis
import CIRISOntology.Core.Posed
import CIRISOntology.Core.SelfAudit
import CIRISOntology.Core.NonFactoring
import Mathlib.Tactic

namespace CIRISOntology.Core.Factoring

variable {X : Type*}

/-- **THE RELATION.** `u` factors through `v`: everything `u` knows, `v`
    determines. The view order of the maximal object. -/
def Factors {C D : Type*} (u : X → C) (v : X → D) : Prop :=
  ∃ h : D → C, u = h ∘ v

theorem factors_refl {C : Type*} (u : X → C) : Factors u u := ⟨id, rfl⟩

theorem factors_trans {C D E : Type*} {u : X → C} {v : X → D} {w : X → E}
    (huv : Factors u v) (hvw : Factors v w) : Factors u w := by
  obtain ⟨h₁, rfl⟩ := huv
  obtain ⟨h₂, rfl⟩ := hvw
  exact ⟨h₁ ∘ h₂, rfl⟩

/-! ### The completeness bridge: factoring is exactly fiber-nonseparation -/

/-- **THE CENTRAL LEMMA.** A quantity factors through a view iff no witness
    pair separates a fiber. The lake's negatives and its licenses are the two
    signs of this biconditional. -/
theorem factors_iff_not_separatesFiber {S D : Type*} [Nonempty D]
    (d : X → D) (summary : X → S) :
    Factors d summary ↔ ¬ SeparatesFiber summary d := by
  constructor
  · rintro ⟨h, rfl⟩ ⟨a, b, hs, hd⟩
    exact hd (by simp only [Function.comp_apply, hs])
  · intro hns
    have hconst : ∀ a b, summary a = summary b → d a = d b := by
      intro a b hab
      by_contra hne
      exact hns ⟨a, b, hab, hne⟩
    classical
    refine ⟨fun s => if hx : ∃ x, summary x = s then d hx.choose
                     else Classical.arbitrary D, ?_⟩
    funext x
    have hx : ∃ y, summary y = summary x := ⟨x, rfl⟩
    simp only [Function.comp_apply, dif_pos hx]
    exact (hconst _ _ hx.choose_spec).symm

/-! ### Instance 1 — the frame order IS this order -/

theorem coarserThan_iff_factors {State : Type*} [Fintype State] {C C' : Type*}
    (view : State → C) (view' : State → C') :
    FrameAxis.CoarserThan view view' ↔ Factors view view' :=
  Iff.rfl

/-! ### Instance 2 — posedness is non-factoring through the trivial view -/

theorem poses_iff_not_factors_trivial {C V : Type*} [Nonempty V]
    (design : Set C) (contrast : C → V) :
    Posed.Poses design contrast ↔
      ¬ Factors (fun x : design => contrast x.val) (fun _ : design => ()) := by
  rw [Posed.poses_iff_separatesFiber,
      factors_iff_not_separatesFiber (fun x : design => contrast x.val)
        (fun _ : design => ()), not_not]

/-! ### Instance 3 — the whole-only shape is non-factoring through the joint view -/

theorem nonFactoring_iff_not_factors_joint {ι Datum : Type*} {View : ι → Type*}
    [Nonempty Datum] (view : (i : ι) → X → View i) (q : X → Datum) :
    NonFactoring view q ↔ ¬ Factors q (fun x i => view i x) := by
  rw [factors_iff_not_separatesFiber q (fun x i => view i x), not_not]
  constructor
  · rintro ⟨a, b, hv, hq⟩
    exact ⟨a, b, funext hv, hq⟩
  · rintro ⟨a, b, hv, hq⟩
    exact ⟨a, b, fun i => congrFun hv i, hq⟩

/-! ### Instance 4 — the stationarity ideal is the POINTED part of the cone (R2) -/

theorem stationarityAudit_factors {R A' : Type*} [Zero R] [Zero A']
    {g : X → R} {A : X → A'} (h : SelfAudit.StationarityAudit g A) :
    Factors A g := by
  obtain ⟨φ, hφ, _⟩ := h
  exact ⟨φ, funext hφ⟩

/-! ### Instance 5 — grain admissibility, on nested ladders (R1)

The dyadic ladder stands in for the engine's octree charts: scale-`k` cells of
a ℕ-line of base-grain sites. -/

/-- The grain view at dyadic scale `k`. -/
def grainView (k : ℕ) : ℕ → ℕ := (· / 2 ^ k)

/-- Coarser nested scales factor through finer ones. -/
theorem grainFactors_of_le {j k : ℕ} (h : j ≤ k) :
    Factors (X := ℕ) (grainView k) (grainView j) := by
  refine ⟨(· / 2 ^ (k - j)), funext fun n => ?_⟩
  simp only [grainView, Function.comp_apply, Nat.div_div_eq_div_mul, ← pow_add,
    Nat.add_sub_cancel' h]

/-- And never the other way: a finer view does not factor through a coarser
    one — the fiber witness is the base site `2^k` against `0`. -/
theorem grainNotFactors_of_lt {j k : ℕ} (h : k < j) :
    ¬ Factors (X := ℕ) (grainView k) (grainView j) := by
  rintro ⟨f, hf⟩
  have h0 := congrFun hf 0
  have h1 := congrFun hf (2 ^ k)
  have hp : 0 < 2 ^ k := Nat.two_pow_pos k
  have hlt : 2 ^ k < 2 ^ j := Nat.pow_lt_pow_right (by norm_num) h
  simp only [grainView, Function.comp_apply, Nat.zero_div, Nat.div_self hp,
    Nat.div_eq_of_lt hlt] at h0 h1
  omega

/-- **R1, stated as the theorem:** on a nested ladder the threshold order IS
    the factoring order — `GrainFloor`'s model is faithful exactly because the
    engine's charts nest. Across unrelated ladders factoring fails even where
    thresholds compare, which is G4 seen from inside the order. -/
theorem grainFactors_iff_le (j k : ℕ) :
    Factors (X := ℕ) (grainView k) (grainView j) ↔ j ≤ k := by
  constructor
  · intro hf
    by_contra hlt
    exact grainNotFactors_of_lt (Nat.lt_of_not_le hlt) hf
  · exact grainFactors_of_le

/-! ### Loops in the view order — the axis is provably FLAT

The STATE axis carries chosen maps: a re-root is a named function, so a cycle of
re-roots can compose to something other than the identity. Holonomy is
expressible there, `Core/RerootTransport.lean` supplies the grammar that carries
claims along it, and the maintained-holonomy campaign measured one.

The VIEW axis cannot do this, and the reason is not a missing construction. It
is that `Factors` supplies only the EXISTENCE of a mediating map — and whichever
map is chosen, a cycle is pinned to the identity on the range. Everything below
is one two-line fact applied twice. Its consequence is a fence: in this object
curvature has exactly ONE axis it can live on.
-/

/-- **THE LOOP CORE, stated once.** Any map carrying a view back to itself is
    the identity ON THAT VIEW'S RANGE — the same range-scoping as
    `Habit.rate_unique_on_range` and `ClaimTransport.carry_path_independent`.
    Every cycle in the `Factors` order is an instance: collapse the cycle with
    `factors_trans` and apply this. -/
theorem mediator_fixes_range {C : Type*} {u : X → C} {f : C → C}
    (h : u = f ∘ u) (x : X) : f (u x) = u x :=
  (congrFun h x).symm

/-- **THE TWO-CYCLE.** Two views that mediate each other round-trip to the
    identity on the range, for EVERY choice of mediating maps — so no choice of
    restriction can make a view loop accumulate anything.

    NOTE the hypotheses this does NOT take. `Factors u v` and `Factors v u` are
    absent because they are not needed: being HANDED the two mediators is
    already stronger than being told they exist. That strengthens the fence
    rather than weakening it — the flatness is not an artifact of `Factors`
    quantifying existentially, it survives choosing the maps by hand. -/
theorem factors_two_cycle_trivial {C D : Type*} {u : X → C} {v : X → D}
    (h : D → C) (h' : C → D) (hu : u = h ∘ v) (hv : v = h' ∘ u) (x : X) :
    h (h' (u x)) = u x := by
  have hv' : v x = h' (u x) := congrFun hv x
  have hu' : u x = h (v x) := congrFun hu x
  rw [← hv', ← hu']

/-- **ANY CYCLE, any length.** Transitivity collapses a factoring cycle to a
    self-mediation, and the core does the rest. Stated at length three; longer
    cycles are the same two lines with more `factors_trans`. -/
theorem factors_cycle_trivial {C D E : Type*}
    {u : X → C} {v : X → D} {w : X → E}
    (huv : Factors u v) (hvw : Factors v w) (hwu : Factors w u) :
    ∃ f : C → C, u = f ∘ u ∧ ∀ x : X, f (u x) = u x := by
  obtain ⟨f, hf⟩ := factors_trans (factors_trans huv hvw) hwu
  exact ⟨f, hf, mediator_fixes_range hf⟩

end CIRISOntology.Core.Factoring
