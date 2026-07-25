/-
CIRISOntology.Core.ShareQuantum — the whole-only share, lifted to the quantum
state-over-times.

`Core.Share` defines the share for classical alphabets. This file lifts the
same variational form to density operators — the genuinely quantum multi-time
object — over any `RCLike` field (so ℂ in particular):

  * `IsDensity`, `ptr₁₂`/`ptr₁₃`/`ptr₂₃`, `QSamePairs` — density operators,
    the three two-slot partial traces, and "carries the same pair data".
  * `vnEntropy` — von Neumann entropy, through the eigenvalue distribution of
    the spectral theorem, so the classical `entropy` and its Gibbs stone carry
    over verbatim. Junk value 0 off the Hermitian domain.
  * `qPairEnvelope`, `qShare` — the same variational functional as `share`,
    now ranging over ALL densities with the state's pair partial traces —
    including coherent and entangled ones the classical envelope cannot see.
  * `vnEntropy_le_log_card` — the quantum Gibbs bound, free from the classical
    one: eigenvalues of a density are a probability state
    (`PosSemidef.eigenvalues_nonneg` + trace = eigenvalue sum).
  * `vnEntropy_diagEmbed` — THE DIAGONAL BRIDGE: the von Neumann entropy of a
    classically-embedded state is its classical entropy. Proved by pinning the
    eigenvalue MULTISET of a diagonal matrix: `det(x•1 − A)` computed once by
    the spectral theorem and once directly, lifted to a polynomial identity
    (`Polynomial.funext`), roots read off (`roots_multiset_prod_X_sub_C`),
    coercion stripped by injectivity.
  * `qShare_parity` — THE EXHIBITED COMPUTATION, quantum: the share of the
    classically-embedded parity state is exactly `log 2` — and this is now a
    stronger statement than the classical one, because the supremum ranges
    over every density matching the pair data, coherent and entangled ones
    included, and none of them beats the diagonal maximizer.
    `qShare_eq_share_parity` records the agreement with `Core.Share`.

SCOPE. Proved here: the items above, exact, over any `RCLike` field. NOT
here, and said plainly: the share of any non-diagonal (coherent) density —
stated as definitions, computed on none; the causal-ordering (process-tensor)
constraint on the envelope, which this file does not impose; and any claim
about which processes in nature carry a nonzero share. Pre-registered in
`scratchpad/temporal-share/DEFINITION_PREREG.md` (phase 2).

Mathlib survey: `IsHermitian.spectral_theorem` / `eigenvectorUnitary` /
`PosSemidef.eigenvalues_nonneg` / `posSemidef_diagonal_iff` carry the spectral
side; `Polynomial.funext` and `roots_multiset_prod_X_sub_C` carry the bridge;
`trace_diagonal`, `det_diagonal`, `det_mul` the bookkeeping. The eigenvalue
sum-equals-trace step is proved here for `RCLike` (the repository's
`trace_eq_sum_eigenvalues` in `Core.Entropy` is the ℝ case). No gaps to port.
-/
import CIRISOntology.Core.Share
import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.LinearAlgebra.Matrix.Spectrum
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Algebra.Polynomial.Roots

namespace CIRISOntology.Core

open Matrix
open scoped BigOperators ComplexOrder

variable {𝕜 : Type*} [RCLike 𝕜]

/-! ### Densities, partial traces, and the quantum share -/

/-- A density operator: positive semidefinite with unit trace. -/
def IsDensity {m : Type*} [Fintype m] (ρ : Matrix m m 𝕜) : Prop :=
  ρ.PosSemidef ∧ ρ.trace = 1

/-- The (1,2) two-slot partial trace of a three-slot operator. -/
noncomputable def ptr₁₂ {α β γ : Type*} [Fintype γ]
    (ρ : Matrix (α × β × γ) (α × β × γ) 𝕜) : Matrix (α × β) (α × β) 𝕜 :=
  Matrix.of fun ab ab' => ∑ c, ρ (ab.1, ab.2, c) (ab'.1, ab'.2, c)

/-- The (1,3) two-slot partial trace of a three-slot operator. -/
noncomputable def ptr₁₃ {α β γ : Type*} [Fintype β]
    (ρ : Matrix (α × β × γ) (α × β × γ) 𝕜) : Matrix (α × γ) (α × γ) 𝕜 :=
  Matrix.of fun ac ac' => ∑ b, ρ (ac.1, b, ac.2) (ac'.1, b, ac'.2)

/-- The (2,3) two-slot partial trace of a three-slot operator. -/
noncomputable def ptr₂₃ {α β γ : Type*} [Fintype α]
    (ρ : Matrix (α × β × γ) (α × β × γ) 𝕜) : Matrix (β × γ) (β × γ) 𝕜 :=
  Matrix.of fun bc bc' => ∑ a, ρ (a, bc.1, bc.2) (a, bc'.1, bc'.2)

/-- `σ` carries exactly the same two-slot data as `ρ`, at every pair of slots. -/
def QSamePairs {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ]
    (ρ σ : Matrix (α × β × γ) (α × β × γ) 𝕜) : Prop :=
  ptr₁₂ σ = ptr₁₂ ρ ∧ ptr₁₃ σ = ptr₁₃ ρ ∧ ptr₂₃ σ = ptr₂₃ ρ

open Classical in
/-- Von Neumann entropy, through the eigenvalue distribution. Off the
    Hermitian domain the value is the junk 0, in the standard convention. -/
noncomputable def vnEntropy {m : Type*} [Fintype m] [DecidableEq m]
    (ρ : Matrix m m 𝕜) : ℝ :=
  if h : ρ.IsHermitian then entropy h.eigenvalues else 0

lemma vnEntropy_of_isHermitian {m : Type*} [Fintype m] [DecidableEq m]
    {ρ : Matrix m m 𝕜} (h : ρ.IsHermitian) :
    vnEntropy ρ = entropy h.eigenvalues := by
  unfold vnEntropy
  exact dif_pos h

/-- The quantum pair envelope: the von Neumann entropies of ALL densities
    carrying exactly the state's two-slot partial traces — coherent and
    entangled ones included. -/
def qPairEnvelope {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ]
    [DecidableEq α] [DecidableEq β] [DecidableEq γ]
    (ρ : Matrix (α × β × γ) (α × β × γ) 𝕜) : Set ℝ :=
  { h | ∃ σ, IsDensity σ ∧ QSamePairs ρ σ ∧ vnEntropy σ = h }

/-- THE WHOLE-ONLY SHARE of a quantum three-slot state: the same variational
    functional as `share`, on the density operator itself. -/
noncomputable def qShare {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ]
    [DecidableEq α] [DecidableEq β] [DecidableEq γ]
    (ρ : Matrix (α × β × γ) (α × β × γ) 𝕜) : ℝ :=
  sSup (qPairEnvelope ρ) - vnEntropy ρ

/-! ### The quantum Gibbs bound -/

/-- Trace equals the sum of eigenvalues, over any `RCLike` field. The ℝ case
    is `Core.Entropy.trace_eq_sum_eigenvalues`; same spectral-theorem proof. -/
theorem trace_eq_sum_eigenvalues_rclike {m : Type*} [Fintype m] [DecidableEq m]
    {A : Matrix m m 𝕜} (hA : A.IsHermitian) :
    A.trace = ∑ i, (hA.eigenvalues i : 𝕜) := by
  have hU : star (hA.eigenvectorUnitary : Matrix m m 𝕜)
      * (hA.eigenvectorUnitary : Matrix m m 𝕜) = 1 :=
    mem_unitaryGroup_iff'.mp hA.eigenvectorUnitary.2
  conv_lhs => rw [hA.spectral_theorem]
  rw [Matrix.trace_mul_comm, ← Matrix.mul_assoc, hU, Matrix.one_mul, Matrix.trace_diagonal]
  simp [Function.comp]

/-- THE QUANTUM GIBBS BOUND: the von Neumann entropy of a density on a finite
    space is at most the log of the dimension. The eigenvalues of a density
    are a probability state, so the classical Gibbs stone carries it. -/
theorem vnEntropy_le_log_card {m : Type*} [Fintype m] [DecidableEq m] [Nonempty m]
    {ρ : Matrix m m 𝕜} (hρ : IsDensity ρ) :
    vnEntropy ρ ≤ Real.log (Fintype.card m) := by
  obtain ⟨hpsd, htr⟩ := hρ
  rw [vnEntropy_of_isHermitian hpsd.1]
  refine entropy_le_log_card (fun i => hpsd.eigenvalues_nonneg i) ?_
  have h := trace_eq_sum_eigenvalues_rclike hpsd.1
  rw [htr] at h
  have h' : ((∑ i, hpsd.1.eigenvalues i : ℝ) : 𝕜) = 1 := by
    push_cast
    exact h.symm
  exact_mod_cast h'

/-- The quantum envelope is bounded above — the supremum in `qShare` is
    honest. -/
theorem qPairEnvelope_bddAbove {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ]
    [DecidableEq α] [DecidableEq β] [DecidableEq γ]
    [Nonempty α] [Nonempty β] [Nonempty γ]
    (ρ : Matrix (α × β × γ) (α × β × γ) 𝕜) : BddAbove (qPairEnvelope ρ) := by
  refine ⟨Real.log (Fintype.card (α × β × γ)), ?_⟩
  rintro h ⟨σ, hσ, -, rfl⟩
  exact vnEntropy_le_log_card hσ

/-- A density sits in its own envelope, so its quantum share is never
    negative. -/
theorem qShare_nonneg {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ]
    [DecidableEq α] [DecidableEq β] [DecidableEq γ]
    [Nonempty α] [Nonempty β] [Nonempty γ]
    {ρ : Matrix (α × β × γ) (α × β × γ) 𝕜} (hρ : IsDensity ρ) : 0 ≤ qShare ρ := by
  have hmem : vnEntropy ρ ∈ qPairEnvelope ρ := ⟨ρ, hρ, ⟨rfl, rfl, rfl⟩, rfl⟩
  have := le_csSup (qPairEnvelope_bddAbove ρ) hmem
  unfold qShare
  linarith

/-! ### The classical embedding -/

/-- The diagonal (classical) embedding of a finite state. -/
noncomputable def diagEmbed {X : Type*} [Fintype X] [DecidableEq X] (p : X → ℝ) :
    Matrix X X 𝕜 :=
  Matrix.diagonal fun x => (p x : 𝕜)

theorem isHermitian_diagEmbed {X : Type*} [Fintype X] [DecidableEq X] (p : X → ℝ) :
    (diagEmbed (𝕜 := 𝕜) p).IsHermitian := by
  rw [diagEmbed]
  refine Matrix.isHermitian_diagonal_of_self_adjoint _ ?_
  show star (fun x => ((p x : ℝ) : 𝕜)) = fun x => ((p x : ℝ) : 𝕜)
  funext x
  simp [RCLike.star_def, RCLike.conj_ofReal]

/-- A classically-embedded probability state is a density. -/
theorem isDensity_diagEmbed {X : Type*} [Fintype X] [DecidableEq X]
    {p : X → ℝ} (hp : IsProb p) : IsDensity (diagEmbed (𝕜 := 𝕜) p) := by
  constructor
  · rw [diagEmbed]
    refine posSemidef_diagonal_iff.mpr fun x => ?_
    exact_mod_cast hp.1 x
  · rw [diagEmbed, Matrix.trace_diagonal]
    exact_mod_cast hp.2

/-- Partial traces of a classical embedding are the embeddings of the
    classical marginals: the quantum pair data of a diagonal state IS its
    classical pair data. -/
theorem ptr₁₂_diagEmbed {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ]
    [DecidableEq α] [DecidableEq β] [DecidableEq γ] (p : α × β × γ → ℝ) :
    ptr₁₂ (diagEmbed (𝕜 := 𝕜) p) = diagEmbed (marg₁₂ p) := by
  ext ab ab'
  rcases eq_or_ne ab ab' with rfl | h
  · simp only [ptr₁₂, diagEmbed, Matrix.of_apply, Matrix.diagonal_apply_eq, marg₁₂]
    push_cast
    rfl
  · simp only [ptr₁₂, diagEmbed, Matrix.of_apply]
    rw [Matrix.diagonal_apply_ne _ h]
    refine Finset.sum_eq_zero fun c _ => Matrix.diagonal_apply_ne _ fun hc => h ?_
    obtain ⟨h1, h2⟩ := Prod.ext_iff.mp hc
    exact Prod.ext_iff.mpr ⟨h1, (Prod.ext_iff.mp h2).1⟩

theorem ptr₁₃_diagEmbed {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ]
    [DecidableEq α] [DecidableEq β] [DecidableEq γ] (p : α × β × γ → ℝ) :
    ptr₁₃ (diagEmbed (𝕜 := 𝕜) p) = diagEmbed (marg₁₃ p) := by
  ext ac ac'
  rcases eq_or_ne ac ac' with rfl | h
  · simp only [ptr₁₃, diagEmbed, Matrix.of_apply, Matrix.diagonal_apply_eq, marg₁₃]
    push_cast
    rfl
  · simp only [ptr₁₃, diagEmbed, Matrix.of_apply]
    rw [Matrix.diagonal_apply_ne _ h]
    refine Finset.sum_eq_zero fun b _ => Matrix.diagonal_apply_ne _ fun hc => h ?_
    obtain ⟨h1, h2⟩ := Prod.ext_iff.mp hc
    exact Prod.ext_iff.mpr ⟨h1, (Prod.ext_iff.mp h2).2⟩

theorem ptr₂₃_diagEmbed {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ]
    [DecidableEq α] [DecidableEq β] [DecidableEq γ] (p : α × β × γ → ℝ) :
    ptr₂₃ (diagEmbed (𝕜 := 𝕜) p) = diagEmbed (marg₂₃ p) := by
  ext bc bc'
  rcases eq_or_ne bc bc' with rfl | h
  · simp only [ptr₂₃, diagEmbed, Matrix.of_apply, Matrix.diagonal_apply_eq, marg₂₃]
    push_cast
    rfl
  · simp only [ptr₂₃, diagEmbed, Matrix.of_apply]
    rw [Matrix.diagonal_apply_ne _ h]
    refine Finset.sum_eq_zero fun a _ => Matrix.diagonal_apply_ne _ fun hc => h ?_
    exact (Prod.ext_iff.mp hc).2

/-! ### The diagonal bridge: eigenvalues of a diagonal are its diagonal -/

private lemma smul_one_sub_diagonal {m : Type*} [Fintype m] [DecidableEq m]
    (x : 𝕜) (v : m → 𝕜) :
    x • (1 : Matrix m m 𝕜) - Matrix.diagonal v = Matrix.diagonal fun i => x - v i := by
  ext i j
  rcases eq_or_ne i j with rfl | hij
  · simp
  · simp [Matrix.diagonal_apply_ne _ hij, Matrix.one_apply_ne hij]

private lemma det_smul_one_sub {m : Type*} [Fintype m] [DecidableEq m]
    {A : Matrix m m 𝕜} (hA : A.IsHermitian) (x : 𝕜) :
    (x • (1 : Matrix m m 𝕜) - A).det = ∏ i, (x - (hA.eigenvalues i : 𝕜)) := by
  have hU : (hA.eigenvectorUnitary : Matrix m m 𝕜)
      * star (hA.eigenvectorUnitary : Matrix m m 𝕜) = 1 :=
    mem_unitaryGroup_iff.mp hA.eigenvectorUnitary.2
  have key : x • (1 : Matrix m m 𝕜) - A
      = (hA.eigenvectorUnitary : Matrix m m 𝕜)
        * (x • (1 : Matrix m m 𝕜) - Matrix.diagonal (RCLike.ofReal ∘ hA.eigenvalues))
        * star (hA.eigenvectorUnitary : Matrix m m 𝕜) := by
    rw [Matrix.mul_sub, Matrix.sub_mul]
    congr 1
    · rw [Matrix.mul_smul, Matrix.mul_one, Matrix.smul_mul, hU]
    · exact hA.spectral_theorem
  rw [key, Matrix.det_mul, Matrix.det_mul, smul_one_sub_diagonal, Matrix.det_diagonal,
      mul_right_comm, ← Matrix.det_mul, hU, Matrix.det_one, one_mul]
  simp [Function.comp]

private lemma det_smul_one_sub_diagEmbed {X : Type*} [Fintype X] [DecidableEq X]
    (d : X → ℝ) (x : 𝕜) :
    (x • (1 : Matrix X X 𝕜) - diagEmbed d).det = ∏ i, (x - (d i : 𝕜)) := by
  rw [diagEmbed, smul_one_sub_diagonal, Matrix.det_diagonal]

private lemma eval_prod_linear {μ : Type*} [Fintype μ] (u : μ → 𝕜) (x : 𝕜) :
    Polynomial.eval x
      ((Finset.univ.val.map u).map fun a => Polynomial.X - Polynomial.C a).prod
      = ∏ i, (x - u i) := by
  have hmap := map_multiset_prod (Polynomial.evalRingHom x)
    ((Finset.univ.val.map u).map fun a => Polynomial.X - Polynomial.C a)
  simp only [Polynomial.coe_evalRingHom] at hmap
  rw [hmap, Multiset.map_map, Multiset.map_map, Finset.prod_eq_multiset_prod]
  refine congrArg Multiset.prod (Multiset.map_congr rfl fun i _ => ?_)
  simp

/-- Two finite families with the same product of linear factors, as functions,
    are the same multiset. `Polynomial.funext` lifts the pointwise identity to
    the polynomial ring; `roots_multiset_prod_X_sub_C` reads the multisets. -/
private lemma multiset_eq_of_prod_linear {ι κ : Type*} [Fintype ι] [Fintype κ]
    (f : ι → 𝕜) (g : κ → 𝕜)
    (h : ∀ x : 𝕜, ∏ i, (x - f i) = ∏ j, (x - g j)) :
    Finset.univ.val.map f = Finset.univ.val.map g := by
  have hpoly :
      ((Finset.univ.val.map f).map fun a => Polynomial.X - Polynomial.C a).prod
        = ((Finset.univ.val.map g).map fun a => Polynomial.X - Polynomial.C a).prod := by
    apply Polynomial.funext
    intro x
    rw [eval_prod_linear f x, eval_prod_linear g x]
    exact h x
  have hroots := congrArg Polynomial.roots hpoly
  rwa [Polynomial.roots_multiset_prod_X_sub_C, Polynomial.roots_multiset_prod_X_sub_C]
    at hroots

/-- The eigenvalue multiset of a classically-embedded state is the state. -/
private lemma eigenvalues_diagEmbed_multiset {X : Type*} [Fintype X] [DecidableEq X]
    (d : X → ℝ) :
    Finset.univ.val.map (isHermitian_diagEmbed (𝕜 := 𝕜) d).eigenvalues
      = Finset.univ.val.map d := by
  have h := multiset_eq_of_prod_linear (𝕜 := 𝕜)
    (fun i => ((isHermitian_diagEmbed (𝕜 := 𝕜) d).eigenvalues i : 𝕜))
    (fun i => (d i : 𝕜))
    (fun x => by
      rw [← det_smul_one_sub (isHermitian_diagEmbed (𝕜 := 𝕜) d) x,
          det_smul_one_sub_diagEmbed])
  have h' : (Finset.univ.val.map (isHermitian_diagEmbed (𝕜 := 𝕜) d).eigenvalues).map
        ((↑) : ℝ → 𝕜)
      = (Finset.univ.val.map d).map ((↑) : ℝ → 𝕜) := by
    rw [Multiset.map_map, Multiset.map_map]
    exact h
  exact Multiset.map_injective (RCLike.ofReal_injective (K := 𝕜)) h'

private lemma sum_mul_log_multiset {X : Type*} [Fintype X] (u : X → ℝ) :
    ∑ x, u x * Real.log (u x)
      = ((Finset.univ.val.map u).map fun t => t * Real.log t).sum := by
  rw [Multiset.map_map]
  exact Finset.sum_eq_multiset_sum _ _

/-- The entropy of a finite family depends only on its multiset of values. -/
private lemma entropy_congr_multiset {X Y : Type*} [Fintype X] [Fintype Y]
    {f : X → ℝ} {g : Y → ℝ}
    (h : Finset.univ.val.map f = Finset.univ.val.map g) :
    entropy f = entropy g := by
  unfold entropy
  rw [sum_mul_log_multiset f, sum_mul_log_multiset g, h]

/-- THE DIAGONAL BRIDGE: von Neumann entropy of a classical embedding is the
    classical entropy. The quantum functional restricts to the classical one
    on the diagonal sector — by theorem, not by convention. -/
theorem vnEntropy_diagEmbed {X : Type*} [Fintype X] [DecidableEq X] (p : X → ℝ) :
    vnEntropy (diagEmbed (𝕜 := 𝕜) p) = entropy p := by
  rw [vnEntropy_of_isHermitian (isHermitian_diagEmbed p)]
  exact entropy_congr_multiset (eigenvalues_diagEmbed_multiset p)

/-! ### The exhibited computation, quantum -/

private lemma qSamePairs_parity_indep :
    QSamePairs (diagEmbed (𝕜 := 𝕜) parity) (diagEmbed indep) := by
  refine ⟨?_, ?_, ?_⟩
  · rw [ptr₁₂_diagEmbed, ptr₁₂_diagEmbed, indep_samePairs.1]
  · rw [ptr₁₃_diagEmbed, ptr₁₃_diagEmbed, indep_samePairs.2.1]
  · rw [ptr₂₃_diagEmbed, ptr₂₃_diagEmbed, indep_samePairs.2.2]

private lemma qtop_parity :
    sSup (qPairEnvelope (diagEmbed (𝕜 := 𝕜) parity)) = 3 * Real.log 2 := by
  refine IsGreatest.csSup_eq
    ⟨⟨diagEmbed indep, isDensity_diagEmbed indep_isProb, qSamePairs_parity_indep,
      by rw [vnEntropy_diagEmbed]; exact entropy_indep'⟩, ?_⟩
  rintro h ⟨σ, hσ, -, rfl⟩
  calc vnEntropy σ ≤ Real.log (Fintype.card (Bool × Bool × Bool)) :=
        vnEntropy_le_log_card hσ
    _ = 3 * Real.log 2 := log_card_eight

/-- THE SHARE OF THE PARITY STATE, QUANTUM: exactly one bit — and now the
    supremum ranges over EVERY density carrying the parity pair data, coherent
    and entangled ones included. None of them beats the diagonal maximizer:
    the whole-only share of the exhibited state survives the quantum lift
    unchanged. -/
theorem qShare_parity : qShare (diagEmbed (𝕜 := 𝕜) parity) = Real.log 2 := by
  unfold qShare
  rw [qtop_parity, vnEntropy_diagEmbed, entropy_parity']
  ring

/-- The quantum and classical shares agree on the exhibited state. -/
theorem qShare_eq_share_parity :
    qShare (diagEmbed (𝕜 := 𝕜) parity) = share parity := by
  rw [qShare_parity, share_parity]

end CIRISOntology.Core
