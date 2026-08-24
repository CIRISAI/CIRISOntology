/-
CIRISOntology.Core.SelfAudit — a self-consistent lie audits clean, and the one
door out: an external theorem makes the error readable again.

WHAT FORCED IT (the Q-seam campaign, `sim_engine/Q_SEAM_RESULTS.md`, 2026-08-23).
The campaign's certificate candidate C1 audited the mean-field chart's error from
the chart's OWN data (its MP2 amplitudes over its own orbitals), and at the
planted worst case it CERTIFIED the lie: the self-audit reported errors two to
four orders of magnitude too small, exactly where the chart was most wrong.
Candidate C3 — the same chart data, but read against THEOREM-pinned values
(particle-hole gives ⟨n⟩ = 1/2 exactly; Lieb gives m = 0 exactly) — refused the
same plant without ever consulting a reference state. The prereg's H1 named the
mechanism in advance: C1 estimates the CORRECTION to the chart's prediction, the
certificate needs the DEVIATION from the truth, and for a symmetry-pinned
observable those are different objects. Both halves are mechanized here, so the
next campaign inherits the lesson as a type rather than as prose.

THE TWO STATEMENTS, and the asymmetry between them is the content.

  * `error_not_computable_from_chart` — THE LIMIT. The deviation of a chart from
    the truth is not a function of the chart's data: two worlds sharing one chart
    state differ in the error, so NO self-audit — however clever, MP2 or
    anything else — can compute it. This is the lake's founding domain argument
    (`not_computable_from`) pointed at audits: the exhibited pair is the chart
    that happens to be right and the same chart in a world where it is wrong.
    "A self-consistent lie audits clean" is this theorem's plain reading, and
    the campaign's C1 row (FP = 20, plant CERTIFIED) is its measured face.
  * `pinned_error_computable_from_chart` — THE DOOR. Where an external theorem
    supplies the true value of an observable (the truth map is CONSTANT on the
    worlds compatible with the theorem's hypotheses), the deviation IS a
    function of chart data — compute the chart's value, subtract the pinned
    constant. C3's warrant, as a construction. The certificate design this
    forces: honest self-certification is exactly certification against the
    theorems the world is known to satisfy, never against the chart's own
    residuals.

DRY NOTE. The limit is a `NonFactoring`-shaped fact and is derived through the
same spine (`Core/Coordination`'s domain argument), not argued afresh — the
family of views is the chart projection, the quantity is the error. It is graded
as an INSTANCE of the founding shape doing new work, not as a sixth independent
witness: the witness pair here is constructed, not found in nature (contrast
`Core/IsomerWitness`).

MEASURED COMPANIONS (2026-08-23, the Q7b campaign; `sim_engine/Q7B_SEAM_RESULTS.md`).
Both theorems now have field readings. THE DOOR, working: the reflection anchor —
the chart's own density asymmetry against a theorem-pinned zero — fired on 9
region-instances, 9/9 on genuinely wrong regions, zero false refusals, exactly in
the deep-well strong-interaction domain staked in advance. THE LIMIT, priced: the
one soundness gap in the campaign's best certificate was a band where the
self-residual under-reported by 11–21% while the symmetry anchors read exactly
zero — the lie sat precisely in the blind spot this file says must exist. And the
comparison the campaign was built for: theorem-anchored chart-data criteria
covered 0.909 and discriminated within configurations 21 times where every
post-hoc coordinate cutoff covered ≤0.436 and discriminated zero — informative
and unsound against sound and useless, with the kill fired as staked on the
soundness clause and kept marked.

SCOPE. Model brick: worlds are pairs (truth, chart) over an arbitrary value
type; nothing quantum, nothing statistical. It does not say self-audits are
useless — it says exactly which part of the error they cannot carry (the part
that varies at fixed chart data) and which part they can (the part a theorem
pins). Kill, separable: exhibit a self-audit — a function of chart data alone —
that provably bounds the deviation from the truth on a family where the truth
genuinely varies at fixed chart data, and `error_not_computable_from_chart` says
the exhibit is impossible, so the exhibit would refute the MODEL's fit, not the
arithmetic: it would mean real audits consume more than this model's "chart
data" (e.g. fresh measurements), which is the door the second theorem names.
-/
import CIRISOntology.Core.Coordination
import Mathlib.Tactic

namespace CIRISOntology.Core.SelfAudit

/-- A world: the truth and the chart's rendering of it, over one value type.
    `V` needs two distinguishable values for anything to be at stake. -/
structure World (V : Type*) where
  truth : V
  chart : V

/-- The chart projection: everything a self-audit is allowed to read. -/
def chartData {V : Type*} (w : World V) : V := w.chart

/-- The deviation of the chart from the truth — what a certificate must bound.
    Stated over an additive group so "deviation" is literal subtraction. -/
def deviation {V : Type*} [Sub V] (w : World V) : V := w.truth - w.chart

/-- The witness pair, named: the chart that happens to be right and the same
    chart in a world where it is wrong share every reading a self-audit can take
    and differ in the error — the deviation separates a fiber of the chart
    projection. -/
theorem deviation_separates_chart_fiber :
    SeparatesFiber (chartData (V := ℝ)) (deviation (V := ℝ)) := by
  refine ⟨⟨0, 0⟩, ⟨1, 0⟩, rfl, ?_⟩
  simp [deviation]

/-- **THE LIMIT: a self-consistent lie audits clean.** No function of chart data
    — no self-audit whatever — computes the deviation from the truth. Derived
    through the lake's spine (`not_computable_from`), not argued afresh. -/
theorem error_not_computable_from_chart :
    ¬ ∃ audit : ℝ → ℝ, ∀ w : World ℝ, deviation w = audit (chartData w) :=
  not_computable_from chartData deviation deviation_separates_chart_fiber

/-- **THE DOOR: a theorem-pinned observable is auditable from chart data.**
    Where an external theorem fixes the true value — the truth is CONSTANT `v₀`
    on every world the theorem admits — the deviation IS computable from chart
    data alone: read the chart, subtract the pinned value. This is C3's warrant
    as a construction, and the reason honest self-certification is certification
    against the theorems the world is known to satisfy. -/
theorem pinned_error_computable_from_chart {V : Type*} [Sub V] (v₀ : V) :
    ∃ audit : V → V,
      ∀ w : World V, w.truth = v₀ → deviation w = audit (chartData w) :=
  ⟨fun c => v₀ - c, fun w hw => by simp [deviation, chartData, hw]⟩

/-! ### The stationarity ideal — which self-audits are vacuous, exactly

Q-seam's §2.4 obstruction (stated there with hypotheses, mechanized here as
promised): a converged self-consistent process is a zero of its own
stationarity residual, so ANY audit that factors through that residual and
vanishes at zero reads zero on every converged chart — the chart cannot catch
itself out with its own equations. The class is named (`StationarityAudit`),
its blindness is one line, and the ESCAPE CRITERION is its contrapositive: an
audit that fires on a converged chart is PROVABLY outside the ideal — which is
the formal warrant for why the theorem-pinned anchors (C3, D1b) could refuse
the plant while every self-residual certified it. Measured face:
`sim_engine/Q7B_SEAM_RESULTS.md` (D1b 9/9; the self-audit missing by 11–21%
exactly where its class says it must). -/

variable {X R : Type*} [Zero R]

/-- Converged: the chart is a zero of its own stationarity residual. -/
def Converged (g : X → R) (x : X) : Prop := g x = 0

/-- The stationarity ideal: audits that factor through the residual and vanish
    at zero — everything the process's own equations imply. -/
def StationarityAudit (g : X → R) {A' : Type*} [Zero A'] (A : X → A') : Prop :=
  ∃ φ : R → A', (∀ x, A x = φ (g x)) ∧ φ 0 = 0

/-- **THE OBSTRUCTION.** Every audit in the ideal reads zero on every converged
    chart, however wrong the chart is. -/
theorem stationarityAudit_blind {g : X → R} {A' : Type*} [Zero A'] {A : X → A'}
    (hA : StationarityAudit g A) {x : X} (hx : Converged g x) : A x = 0 := by
  obtain ⟨φ, hφ, h0⟩ := hA
  rw [hφ, hx, h0]

/-- **THE ESCAPE CRITERION.** An audit that fires on a converged chart is
    provably outside the ideal — it consumed something the stationarity
    conditions do not imply. This is why symmetry anchors work: the chart is
    free to break a symmetry its own equations never mention. -/
theorem not_stationarityAudit_of_fires {g : X → R} {A' : Type*} [Zero A'] {A : X → A'}
    {x : X} (hx : Converged g x) (hfire : A x ≠ 0) :
    ¬ StationarityAudit g A :=
  fun hA => hfire (stationarityAudit_blind hA hx)

end CIRISOntology.Core.SelfAudit
