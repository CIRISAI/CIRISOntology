/-
CIRISOntology.Core.RouteSymmetry — Brick 2 of the confrontation core: the REG+
three-route sector's exact route symmetries, as theorems.

WHAT IS PROVED. For the three-route holonomy generator H(φ) (the R1-pinned form:
phase e^{±iφ} on the 0–2 edge, all other couplings 1) and U(φ) = exp(−iθ·H(φ)):
  * `routeH_transpose` — H(φ)ᵀ = H(−φ): time reversal is transposition.
  * `routeU_neg` — U(−φ) = U(φ)ᵀ, hence `return_even`: every RETURN amplitude is
    an even function of the loop phase. This is the algebraic content behind the
    measured even-harmonics-only returns (odd power ~1e-17 numerically; here 0).
  * `conj_identity` + `transfer_chirality` — the 1↔2 relabelling conjugates H(φ)
    to a diagonal-gauge copy of H(−φ), so |U(φ)₀₂| = |U(−φ)₀₁|: the transfers are
    CHIRAL PARTNERS under φ → −φ. This is the measured p01(φ) = p02(−φ) (4e-16
    numerically; here exact).

STATUS AND FENCE. These are theorems about the MODEL's route sector — quantum
mechanics on a graph. They upgrade the REG side of ledger row R4 and bridge stake
BS-2 from machine-exact numerics to machine-checked proof. The evidential bin is
UNCHANGED: agreement with AAS-type physics remains DEGENERATE-LIMIT (Sornette bin)
because these are QM facts; what the corpus does with them is BS-2/BS-3's business.

CONVERGENT ART (credited per house rule): Al'tshuler–Aronov–Spivak 1981 (the
even-harmonic pairing, cited via secondary — pre-DOI); Douçot–Rammal, PRL 55:1148
(1985) (AAS on networks); Arnault–Debbasch, PRA 93:052301 (2016) and
Cedzich–Geib–Werner–Werner, JMP 60:012107 (2019) (gauge fields on lattice walks —
what minimal coupling means here); Büttiker reciprocity for the chirality pairing's
mesoscopic face.
-/
import Mathlib.Analysis.Normed.Algebra.MatrixExponential
import Mathlib.Data.Matrix.Notation
import Mathlib.Analysis.SpecialFunctions.Complex.Circle

namespace CIRISOntology.Core.RouteSymmetry

open Matrix Complex

noncomputable section

/-- The unit phase `e^{iφ}`. -/
def ph (φ : ℝ) : ℂ := Complex.exp ((φ : ℂ) * Complex.I)

@[simp] theorem ph_neg_mul (φ : ℝ) : ph (-φ) * ph φ = 1 := by
  simp [ph, ← Complex.exp_add]

@[simp] theorem ph_mul_neg (φ : ℝ) : ph φ * ph (-φ) = 1 := by
  simp [ph, ← Complex.exp_add]

@[simp] theorem norm_ph (φ : ℝ) : ‖ph φ‖ = 1 := by
  simp [ph]

/-- The three-route holonomy generator, exactly as pinned in the R1 handoff:
`H(φ) = [[0,1,e^{-iφ}],[1,0,1],[e^{iφ},1,0]]`. -/
def routeH (φ : ℝ) : Matrix (Fin 3) (Fin 3) ℂ :=
  !![0, 1, ph (-φ); 1, 0, 1; ph φ, 1, 0]

/-- Time reversal is transposition: `H(φ)ᵀ = H(−φ)`. -/
theorem routeH_transpose (φ : ℝ) : (routeH φ)ᵀ = routeH (-φ) := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [routeH, Matrix.transpose_apply, neg_neg]

/-- The evolution `U(φ) = exp(−iθ H(φ))`. -/
def routeU (θ φ : ℝ) : Matrix (Fin 3) (Fin 3) ℂ :=
  NormedSpace.exp ℂ ((-(θ : ℂ) * Complex.I) • routeH φ)

/-- `U(−φ) = U(φ)ᵀ`. -/
theorem routeU_neg (θ φ : ℝ) : routeU θ (-φ) = (routeU θ φ)ᵀ := by
  unfold routeU
  rw [← routeH_transpose, ← Matrix.transpose_smul, Matrix.exp_transpose]

/-- Every return amplitude is even in the loop phase. -/
theorem return_even (θ φ : ℝ) (i : Fin 3) :
    routeU θ (-φ) i i = routeU θ φ i i := by
  rw [routeU_neg]; rfl

/-- Return PROBABILITIES are even in the loop phase — the mechanized face of the
measured even-harmonics-only returns. -/
theorem return_prob_even (θ φ : ℝ) (i : Fin 3) :
    ‖routeU θ (-φ) i i‖ = ‖routeU θ φ i i‖ := by
  rw [return_even]

/-! ### Chirality: the 1↔2 relabelling pairs the transfers across φ → −φ -/

/-- The 1↔2 relabelling. -/
def P : Matrix (Fin 3) (Fin 3) ℂ := !![1, 0, 0; 0, 0, 1; 0, 1, 0]

theorem P_mul_P : P * P = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [P, Matrix.mul_apply, Fin.sum_univ_three, Matrix.one_apply,
      Matrix.vecHead, Matrix.vecTail]

/-- `P` as a unit (it is an involution). -/
def Punit : (Matrix (Fin 3) (Fin 3) ℂ)ˣ := ⟨P, P, P_mul_P, P_mul_P⟩

/-- The diagonal gauge `D(φ) = diag(e^{−iφ},1,1)`. -/
def Dm (φ : ℝ) : Matrix (Fin 3) (Fin 3) ℂ := Matrix.diagonal ![ph (-φ), 1, 1]

def DmInv (φ : ℝ) : Matrix (Fin 3) (Fin 3) ℂ := Matrix.diagonal ![ph φ, 1, 1]

theorem Dm_mul_DmInv (φ : ℝ) : Dm φ * DmInv φ = 1 := by
  unfold Dm DmInv
  rw [Matrix.diagonal_mul_diagonal]
  have h : (fun i => ![ph (-φ), 1, 1] i * ![ph φ, 1, 1] i) = fun _ => (1:ℂ) := by
    funext i; fin_cases i <;> simp
  rw [h, Matrix.diagonal_one]

theorem DmInv_mul_Dm (φ : ℝ) : DmInv φ * Dm φ = 1 := by
  unfold Dm DmInv
  rw [Matrix.diagonal_mul_diagonal]
  have h : (fun i => ![ph φ, 1, 1] i * ![ph (-φ), 1, 1] i) = fun _ => (1:ℂ) := by
    funext i; fin_cases i <;> simp
  rw [h, Matrix.diagonal_one]

/-- `D(φ)` as a unit. -/
def Dunit (φ : ℝ) : (Matrix (Fin 3) (Fin 3) ℂ)ˣ :=
  ⟨Dm φ, DmInv φ, Dm_mul_DmInv φ, DmInv_mul_Dm φ⟩

/-- The key conjugation identity: relabelling 1↔2 carries `H(φ)` to a diagonal-gauge
copy of `H(−φ)` — the loop orientation reverses, the Wilson phase conjugates. -/
theorem conj_identity (φ : ℝ) :
    P * routeH φ * P = Dm φ * routeH (-φ) * DmInv φ := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [P, Dm, DmInv, routeH, Matrix.mul_apply, Fin.sum_univ_three,
      Matrix.diagonal, neg_neg, Matrix.vecHead, Matrix.vecTail, Function.comp]

/-- The conjugation at the evolution level: `P U(φ) P = D U(−φ) D⁻¹`. -/
theorem routeU_conj (θ φ : ℝ) :
    P * routeU θ φ * P = Dm φ * routeU θ (-φ) * DmInv φ := by
  unfold routeU
  have h1 : P * NormedSpace.exp ℂ ((-(θ:ℂ) * Complex.I) • routeH φ) * P
      = NormedSpace.exp ℂ (P * ((-(θ:ℂ) * Complex.I) • routeH φ) * P) := by
    have := (Matrix.exp_units_conj ℂ Punit ((-(θ:ℂ) * Complex.I) • routeH φ)).symm
    simpa [Punit] using this
  have h2 : P * ((-(θ:ℂ) * Complex.I) • routeH φ) * P
      = Dm φ * ((-(θ:ℂ) * Complex.I) • routeH (-φ)) * DmInv φ := by
    rw [Matrix.mul_smul, Matrix.smul_mul, conj_identity, Matrix.mul_smul,
      Matrix.smul_mul]
  have h3 : NormedSpace.exp ℂ (Dm φ * ((-(θ:ℂ) * Complex.I) • routeH (-φ)) * DmInv φ)
      = Dm φ * NormedSpace.exp ℂ ((-(θ:ℂ) * Complex.I) • routeH (-φ)) * DmInv φ := by
    have := Matrix.exp_units_conj ℂ (Dunit φ) ((-(θ:ℂ) * Complex.I) • routeH (-φ))
    simpa [Dunit] using this
  rw [h1, h2, h3]

/-- Entry extraction on the P side: `(P M P)₀₁ = M₀₂`. -/
theorem P_entry (M : Matrix (Fin 3) (Fin 3) ℂ) : (P * M * P) 0 1 = M 0 2 := by
  simp [P, Matrix.mul_apply, Matrix.vecMul, Matrix.dotProduct, Fin.sum_univ_three]

/-- Entry extraction on the D side: `(D M D⁻¹)₀₁ = e^{−iφ} M₀₁`. -/
theorem D_entry (φ : ℝ) (M : Matrix (Fin 3) (Fin 3) ℂ) :
    (Dm φ * M * DmInv φ) 0 1 = ph (-φ) * M 0 1 := by
  simp [Dm, DmInv, Matrix.mul_apply, Fin.sum_univ_three, Matrix.diagonal,
    Matrix.vecHead, Matrix.vecTail, Function.comp]

/-- **Transfer chirality**: `|U(φ)₀₂| = |U(−φ)₀₁|` — the two transfer routes are
chiral partners under reversal of the loop phase. Mechanizes the measured
`p01(φ) = p02(−φ)` (numerically 4e-16; here exact). -/
theorem transfer_chirality (θ φ : ℝ) :
    ‖routeU θ φ 0 2‖ = ‖routeU θ (-φ) 0 1‖ := by
  have h := congrArg (fun M => M 0 1) (routeU_conj θ φ)
  simp only [P_entry, D_entry] at h
  calc ‖routeU θ φ 0 2‖ = ‖ph (-φ) * routeU θ (-φ) 0 1‖ := by rw [h]
    _ = ‖ph (-φ)‖ * ‖routeU θ (-φ) 0 1‖ := norm_mul _ _
    _ = ‖routeU θ (-φ) 0 1‖ := by rw [norm_ph, one_mul]

end

end CIRISOntology.Core.RouteSymmetry
