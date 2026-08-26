/-
CIRISOntology.Core.RentLaw — the rent function, mechanized from A4's derivation
(scratchpad/omega/gcost/GCOST_DERIVATION.md).

The atlas killed "maintenance is priced by the closure defect" (the closed parity
view with Δ_v ≡ 0 and W* ≈ 0.8–0.97). A4 derived the successor: the price lives
in the INDUCED chain's decay. This file pays the algebraic core as Lean:

  * the maintained scalar `rentStep lam q s0 : s ↦ (1−q)·lam·s + q·s0` — decay
    then affine repair, the repo's reading (b);
  * `rent_closed_form` — the orbit in closed form, by induction;
  * `rent_tendsto` — convergence to the fixed point at geometric rate, so the
    stationary retention exists and equals `Ginf`;
  * `Ginf lam q = q / (ε + q·lam)` with `ε = 1 − lam` — the measured law of
    three substrates (LFSR, lattice, Wilson-loop), now the fixed point of one
    affine recursion;
  * `Wstar γ δ = (1−δ)·γ/(γ + δ·(1−γ))` and `Ginf_at_Wstar`: dosing at `Wstar`
    holds retention at exactly `1 − δ` — the defining property of the price;
  * `Wstar_strictMono` — the price is STRICTLY increasing in the gap at fixed
    tolerance: falsifier 5 of the derivation, as a theorem. The atlas data walked
    this line (γ: 0.078→0.64, W* tracking to the grid digit, Δ_v pinned at 0).

SCOPE. Scalar, single tracked mode, affine deposit, decay-then-repair — A1–A6 of
the derivation; the multi-mode and misalignment FLOORS and the schedule
comparison are measured/derived in the campaign files and NOT mechanized here.
`ε` is one minus the decay eigenvalue of the TRACKED MODE, never the microscopic
noise rate. Nothing here is a claim about nature.

CREDIT: the affine-recursion fixed point is elementary; the identification with
the rent clause and the three-substrate law is this repository's (Maintenance.lean,
HOLONOMY_RENT, A4).
-/
import Mathlib.Analysis.SpecificLimits.Basic

namespace CIRISOntology.Core.RentLaw

/-- One maintained step: decay by `(1−q)·lam`, deposit `q·s0`. -/
def rentStep (lam q s0 : ℝ) (s : ℝ) : ℝ := (1 - q) * lam * s + q * s0

/-- The maintained orbit from `s0`. -/
def rentOrbit (lam q s0 : ℝ) : ℕ → ℝ
  | 0 => s0
  | n + 1 => rentStep lam q s0 (rentOrbit lam q s0 n)

/-- The fixed point of the maintained step. -/
noncomputable def rentFix (lam q s0 : ℝ) : ℝ := q * s0 / (1 - (1 - q) * lam)

/-- Stationary retention as a fraction of the deposit target:
    `Ginf = q / (ε + q·lam)`, `ε = 1 − lam`. -/
noncomputable def Ginf (lam q : ℝ) : ℝ := q / ((1 - lam) + q * lam)

/-- The price of retention `1 − δ` at gap `γ`. -/
noncomputable def Wstar (γ δ : ℝ) : ℝ := (1 - δ) * γ / (γ + δ * (1 - γ))

/-- The fixed point is the `Ginf` fraction of the target. -/
theorem rentFix_eq_Ginf_mul (lam q s0 : ℝ) :
    rentFix lam q s0 = Ginf lam q * s0 := by
  unfold rentFix Ginf
  have : 1 - (1 - q) * lam = (1 - lam) + q * lam := by ring
  rw [this]; ring

/-- **The closed form**: the orbit is the fixed point plus a geometrically
    decaying transient. -/
theorem rent_closed_form (lam q s0 : ℝ) (h : (1 - q) * lam ≠ 1) (n : ℕ) :
    rentOrbit lam q s0 n = rentFix lam q s0 +
      ((1 - q) * lam) ^ n * (s0 - rentFix lam q s0) := by
  have hD : (1 : ℝ) - (1 - q) * lam ≠ 0 := sub_ne_zero.mpr (Ne.symm h)
  have hfix : (1 - q) * lam * rentFix lam q s0 + q * s0 = rentFix lam q s0 := by
    unfold rentFix; field_simp; ring
  induction n with
  | zero => simp [rentOrbit]
  | succ n ih =>
      show rentStep lam q s0 (rentOrbit lam q s0 n) = _
      rw [ih]
      unfold rentStep
      calc (1 - q) * lam * (rentFix lam q s0 +
              ((1 - q) * lam) ^ n * (s0 - rentFix lam q s0)) + q * s0
          = ((1 - q) * lam * rentFix lam q s0 + q * s0) +
              ((1 - q) * lam) ^ (n + 1) * (s0 - rentFix lam q s0) := by ring
        _ = _ := by rw [hfix]

/-- **Convergence**: under genuine decay `|(1−q)·lam| < 1`, the maintained orbit
    tends to the fixed point — the stationary retention EXISTS and is `Ginf·s0`. -/
theorem rent_tendsto (lam q s0 : ℝ) (h : |(1 - q) * lam| < 1) :
    Filter.Tendsto (rentOrbit lam q s0) Filter.atTop (nhds (rentFix lam q s0)) := by
  have hne : (1 - q) * lam ≠ 1 := by
    intro he; rw [he] at h; simp at h
  have hpow : Filter.Tendsto (fun n => ((1 - q) * lam) ^ n * (s0 - rentFix lam q s0))
      Filter.atTop (nhds 0) := by
    have := tendsto_pow_atTop_nhds_zero_iff.mpr h
    simpa using this.mul_const (s0 - rentFix lam q s0)
  have : Filter.Tendsto (fun n => rentFix lam q s0 +
      ((1 - q) * lam) ^ n * (s0 - rentFix lam q s0)) Filter.atTop
      (nhds (rentFix lam q s0 + 0)) := (tendsto_const_nhds).add hpow
  simpa [funext_iff.mpr (rent_closed_form lam q s0 hne)] using this

/-- **The defining property of the price**: dosing at `Wstar γ δ` holds retention
    at exactly `1 − δ`. (`lam = 1 − γ`.) -/
theorem Ginf_at_Wstar (γ δ : ℝ) (hγ : 0 < γ) (hδ : 0 < δ) (hδ1 : δ < 1) :
    Ginf (1 - γ) (Wstar γ δ) = 1 - δ := by
  have hE : (0:ℝ) < γ + δ * (1 - γ) := by nlinarith
  have hE' : γ + δ * (1 - γ) ≠ 0 := ne_of_gt hE
  unfold Ginf Wstar
  have hden : (1 - (1 - γ)) + (1 - δ) * γ / (γ + δ * (1 - γ)) * (1 - γ)
      = γ / (γ + δ * (1 - γ)) := by
    field_simp
    ring
  rw [hden, div_div_eq_mul_div, div_mul_cancel₀ _ hE',
      mul_div_cancel_right₀ _ hγ.ne']

/-- **Falsifier 5, as a theorem: the price strictly rises with the gap.** -/
theorem Wstar_strictMono (δ : ℝ) (hδ : 0 < δ) (hδ1 : δ < 1)
    {γ₁ γ₂ : ℝ} (h1 : 0 < γ₁) (h12 : γ₁ < γ₂) (h2 : γ₂ ≤ 1) :
    Wstar γ₁ δ < Wstar γ₂ δ := by
  unfold Wstar
  have d1 : γ₁ + δ * (1 - γ₁) > 0 := by nlinarith
  have d2 : γ₂ + δ * (1 - γ₂) > 0 := by nlinarith
  rw [div_lt_div_iff₀ d1 d2]
  have key : (0:ℝ) < (1 - δ) * δ * (γ₂ - γ₁) :=
    mul_pos (mul_pos (by linarith) hδ) (by linarith)
  nlinarith [key]

end CIRISOntology.Core.RentLaw
