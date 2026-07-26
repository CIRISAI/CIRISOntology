/-
CIRISOntology.Core.Creation — maintenance is not preservation. It is creation.

WHAT IS PROVED. One application of a code's repair map to PURE NOISE mints that
code's whole-only share exactly, from nothing.

  * `repair_creates_parity` — `share (pushforward parityRepair indep) = log 2`.
    `indep` is the uniform state on the eight three-bit words: its share is zero
    (`share_indep`) and its total dependence is zero (`S_total_indep`); there is
    no pattern in it at any order. `parityRepair` is the minimal maintenance
    operation of the parity code — recompute the check bit from the two data
    bits and touch nothing else. Pushing the uniform state through it gives the
    parity state EXACTLY (`pushforward_parityRepair_indep`, an eight-cell
    computation: each of the four code words has exactly two preimages), so by
    `share_parity` one full bit of whole-only pattern now stands where none did.
    Stated as a difference in `repair_mints_from_noise`.

  * `parityRepair_pays_one_bit` — and the bit is not free. The repair is
    deterministic and lossy: it discards exactly `log 2` of entropy
    (`3 log 2 → 2 log 2`) and mints exactly `log 2` of whole-only share. One bit
    paid, one bit minted, with no slack in either direction.

  * `repair_creates_ferro` / `S_total_majorityRepair` — WHICH pattern a repair
    can mint is governed by `Core.SignSymmetry`. The repetition code's repair is
    the majority vote (`majorityRepair`: overwrite all three cells with the
    majority). Its pushforward of the uniform state is `ferro` exactly, and
    `ferro` is sign-symmetric — so this repair mints whole-only share ZERO while
    minting two full bits of ORDINARY correlation, at a price of two bits of
    entropy (`majorityRepair_pays_two_bits`). Same machine, same noise, same
    kind of operation; the code's symmetry decides what comes out.

  * `percell_no_creation` — the no-creation half, general in the input state.
    A PER-CELL map (`percell f g h`: each slot rewritten by a function of itself
    alone, reading no neighbour) can never raise the share:
    `share (pushforward (percell f g h) p) ≤ share p`. The proof splits the four
    functions `Bool → Bool` into the two bijections and the two constants. On
    bijections the share is exactly INVARIANT (`share_pushforward_percell_of_bijective`,
    by reindexing the whole variational problem — entropy and the pair envelope
    are both carried along by the relabeling). On a constant factor the output
    slot is deterministic and the share is exactly ZERO
    (`share_pushforward_percell_of_const₁` and its two siblings, via
    `share_eq_zero_of_first_det` and siblings: a state with a frozen slot is its
    own maximum-entropy competitor).

  * `parityRepair_not_percell` / `majorityRepair_not_percell` — and the two
    minting maps are provably NOT per-cell. So the divide is exhibited, not
    asserted: the check bit reads two neighbours, the majority reads all three,
    and only maps that read more than their own cell mint anything. The third
    that SEES (`third_sees_parity`) is also the only agent that can BUILD.

  * `parityRepair_idempotent` / `parityRepair_fixed_iff` and their majority
    siblings — the word "repair" is checked, not assumed. Each map is a
    projection, and its fixed-point set is EXACTLY the code it maintains, so
    it changes nothing already well maintained and nothing else is left alone.

THE ROUTE. Three stones, all already in this repository. `pushforward` and
`entropy_map_le` (`Core.ShareK`) carry the coarse-graining; `share_parity`
(`Core.Share`) and `share_ferro` / `S_total_ferro` (`Core.SignSymmetry`) are the
two exhibited values the two repairs land on; `entropy_grouping` (`Core.Share`)
closes the deterministic-slot case in all three slot positions, the other two
obtained from it by reindexing the slots through an explicit involution
(`swap₁₃`, `swap₂₃`).

CREDIT. The computational finding is this repository's own maintenance sweep,
the MISMATCH arm (`scratchpad/maintenance_sweep.log`, MEASUREMENT 5, same day):
drift plus upkeep pointed at a structure the state does not have produces share
2.718 against 0.000 with no upkeep. This file is the machine-checked core of
that observation, at the smallest size where it can be stated exactly. The
coarse-graining reading (a repair map is a projection onto a code; the code is
its fixed-point set) is standard renormalization-group context, and the reading
of the discarded entropy as the price of the minted pattern is the standard
Szilard/Landauer accounting — both are named here as context, not as results of
ours.

SCOPE. Proved here: the ONE-STEP minting, exactly, on three binary slots, and
the no-creation half for per-cell maps on three binary slots. The dichotomy the
per-cell proof runs on — every `Bool → Bool` is a bijection or a constant — is
specific to two-letter cells; on three letters or more there are maps that are
neither, and the argument as written does not reach them. The general-alphabet
and general-k forms are NOT proved here.

NOT proved here either: the dynamical version — repair iterated against noise,
with rates, fixed points and a steady-state share. That is measured in the sweep
and modeled in `Core.Maintenance`'s rent clause; it is not a theorem of this
file, and this file's "creation" is one application of one map, not a claim
about what a maintained system settles down to. NOT proved anywhere: any claim
about which maintenance processes in nature carry whole-only share.

Mathlib survey: `Equiv.sum_comp` for every reindexing, `Finite.injective_iff_bijective`
for the Bool dichotomy, `IsGreatest.csSup_eq` to close each supremum. The
pushforward's normalization is `Core.HammingCap`'s `isProb_pushforward`, reused.
No gaps to port.
-/
import CIRISOntology.Core.HammingCap
import CIRISOntology.Core.SignSymmetry

namespace CIRISOntology.Core

open scoped BigOperators

/-! ### The repair maps -/

/-- THE PARITY CODE'S REPAIR: recompute the check bit from the two data bits.
    The minimal maintenance operation of the code — it reads two cells and
    writes the third, and it is the identity on every word already in the
    code. -/
def parityRepair (t : Bool × Bool × Bool) : Bool × Bool × Bool :=
  (t.1, t.2.1, Bool.xor t.1 t.2.1)

/-- Majority vote on three bits. -/
def majority (a b c : Bool) : Bool := (a && b) || (b && c) || (a && c)

/-- THE REPETITION CODE'S REPAIR: overwrite all three cells with the majority.
    Reads all three cells; the identity on the two code words. -/
def majorityRepair (t : Bool × Bool × Bool) : Bool × Bool × Bool :=
  (majority t.1 t.2.1 t.2.2, majority t.1 t.2.1 t.2.2, majority t.1 t.2.1 t.2.2)

/-- A PER-CELL map: every slot is rewritten by a function of itself alone. No
    cell reads a neighbour, so nothing in the map knows about the whole. -/
def percell (f g h : Bool → Bool) (t : Bool × Bool × Bool) : Bool × Bool × Bool :=
  (f t.1, g t.2.1, h t.2.2)

/-! ### The repair maps are projections onto their codes

Checked rather than asserted, so the word "repair" carries its meaning: each map
is idempotent, and its fixed-point set is exactly the code it maintains. -/

/-- The parity repair is a projection: applying it twice is applying it once. -/
theorem parityRepair_idempotent (t : Bool × Bool × Bool) :
    parityRepair (parityRepair t) = parityRepair t := by
  obtain ⟨a, b, c⟩ := t
  revert a b c
  decide

/-- Its fixed points are EXACTLY the parity code: the words the check bit
    already agrees with. So the repair leaves alone exactly what is already
    well maintained, and nothing else. -/
theorem parityRepair_fixed_iff (t : Bool × Bool × Bool) :
    parityRepair t = t ↔ t.2.2 = Bool.xor t.1 t.2.1 := by
  obtain ⟨a, b, c⟩ := t
  revert a b c
  decide

/-- The majority is the value at least two of the three cells carry. -/
theorem majority_eq (a b c : Bool) : majority a b c = if a = b then a else c := by
  revert a b c
  decide

/-- The majority repair is a projection. -/
theorem majorityRepair_idempotent (t : Bool × Bool × Bool) :
    majorityRepair (majorityRepair t) = majorityRepair t := by
  obtain ⟨a, b, c⟩ := t
  revert a b c
  decide

/-- Its fixed points are EXACTLY the repetition code: the words whose three
    cells agree. -/
theorem majorityRepair_fixed_iff (t : Bool × Bool × Bool) :
    majorityRepair t = t ↔ (t.1 = t.2.1 ∧ t.2.1 = t.2.2) := by
  obtain ⟨a, b, c⟩ := t
  revert a b c
  decide

/-! ### Basic facts about the pushforward -/

/-- The pushforward along a BIJECTION is a relabeling: no cell is merged with
    another, so the state is only carried across by the inverse. -/
lemma pushforward_equiv {X Y : Type*} [Fintype X] [DecidableEq Y]
    (e : X ≃ Y) (p : X → ℝ) : pushforward (⇑e) p = fun y => p (e.symm y) := by
  funext y
  have hfil : Finset.univ.filter (fun x => e x = y) = {e.symm y} := by
    ext x
    simp [Equiv.apply_eq_iff_eq_symm_apply]
  simp [pushforward, hfil]

/-! ### Repair one: the parity code mints one whole-only bit from noise -/

/-- THE EIGHT-CELL COMPUTATION. Pushing the uniform state through the parity
    code's repair gives the parity state exactly: each of the four code words
    has exactly two preimages (the discarded check bit), so each collects
    `2/8 = 1/4`, and every non-code word collects nothing. -/
theorem pushforward_parityRepair_indep : pushforward parityRepair indep = parity := by
  funext y
  obtain ⟨a, b, c⟩ := y
  simp only [pushforward, Finset.sum_filter, indep, parityRepair, parity,
    Fintype.sum_prod_type, Fintype.sum_bool]
  cases a <;> cases b <;> cases c <;> norm_num

/-- MAINTENANCE IS CREATION. One application of the parity code's repair map to
    PURE NOISE — the uniform state, whose share is exactly zero — leaves a state
    whose whole-only share is exactly one bit. Nothing was preserved, because
    there was nothing there to preserve; the pattern was minted. -/
theorem repair_creates_parity : share (pushforward parityRepair indep) = Real.log 2 := by
  rw [pushforward_parityRepair_indep, share_parity]

/-- The same statement as a difference, so "from nothing" is not rhetoric: the
    input carries zero whole-only share and the output carries `log 2`. -/
theorem repair_mints_from_noise :
    share (pushforward parityRepair indep) - share indep = Real.log 2 := by
  rw [repair_creates_parity, share_indep]
  ring

/-- And the total-dependence reading agrees: the minted pattern is visible to
    the third-aware instrument at exactly one bit. -/
theorem S_total_parityRepair : S_total (pushforward parityRepair indep) = Real.log 2 := by
  rw [pushforward_parityRepair_indep, third_sees_parity]

/-- THE BIT IS NOT FREE. The repair is deterministic and lossy: it discards
    exactly `log 2` of entropy and mints exactly `log 2` of whole-only share.
    One bit paid, one bit minted — the ledger balances with no slack in either
    direction. (The reading of the discarded entropy as the price of the minted
    pattern is standard Szilard/Landauer accounting, named here as context.) -/
theorem parityRepair_pays_one_bit :
    entropy indep - entropy (pushforward parityRepair indep) = Real.log 2 := by
  rw [pushforward_parityRepair_indep, entropy_indep', entropy_parity']
  ring

/-! ### Repair two: sign symmetry decides what a repair can mint -/

/-- The repetition code's repair sends the uniform state to `ferro` exactly:
    the four words with a majority of `false` collect `4/8 = 1/2` at `(F,F,F)`,
    the other four collect `1/2` at `(T,T,T)`. -/
theorem pushforward_majorityRepair_indep : pushforward majorityRepair indep = ferro := by
  funext y
  obtain ⟨a, b, c⟩ := y
  simp only [pushforward, Finset.sum_filter, indep, majorityRepair, majority, ferro,
    Fintype.sum_prod_type, Fintype.sum_bool]
  cases a <;> cases b <;> cases c <;> norm_num

/-- WHICH PATTERN GETS MINTED IS GOVERNED BY SIGN SYMMETRY. The repetition
    code's repair is every bit as much a maintenance operation as the parity
    code's, and it runs on the same noise — but its code is sign-symmetric, so
    by `share_ferro` it mints whole-only share EXACTLY ZERO. What each repair
    mints is the uniform state ON ITS OWN CODE (both maps have equal-sized
    fibers, so the noise lands evenly), and the code's symmetry then fixes the
    answer: sign-symmetric code, no whole-only share, at any strength. -/
theorem repair_creates_ferro : share (pushforward majorityRepair indep) = 0 := by
  rw [pushforward_majorityRepair_indep, share_ferro]

/-- The zero above is not an absence of order: the same repair mints TWO FULL
    BITS of ordinary correlation. Ordinary pattern is easy to make; whole-only
    pattern needs a code that breaks the global sign symmetry. -/
theorem S_total_majorityRepair :
    S_total (pushforward majorityRepair indep) = 2 * Real.log 2 := by
  rw [pushforward_majorityRepair_indep, S_total_ferro]

private lemma log_half''' : Real.log ((1:ℝ)/2) = -Real.log 2 := by
  rw [one_div, Real.log_inv]

private lemma entropy_ferro' : entropy ferro = Real.log 2 := by
  unfold entropy ferro
  simp only [Fintype.sum_prod_type, Fintype.sum_bool]
  norm_num [log_half''']
  ring

/-- And it pays twice as much for it: two bits of entropy discarded, two bits
    of ordinary correlation minted, zero whole-only share. -/
theorem majorityRepair_pays_two_bits :
    entropy indep - entropy (pushforward majorityRepair indep) = 2 * Real.log 2 := by
  rw [pushforward_majorityRepair_indep, entropy_indep', entropy_ferro']
  ring

/-! ### The minting maps are not per-cell -/

/-- The parity code's repair READS A NEIGHBOUR, and provably must: no per-cell
    map agrees with it. The check bit is a function of two cells, and a
    function of the third cell alone cannot be it. -/
theorem parityRepair_not_percell : ¬ ∃ f g h, parityRepair = percell f g h := by
  rintro ⟨f, g, h, heq⟩
  have h1 := congrArg (fun π => (π (false, false, false)).2.2) heq
  have h2 := congrArg (fun π => (π (true, false, false)).2.2) heq
  simp only [parityRepair, percell] at h1 h2
  simp at h1 h2
  exact absurd (h1.symm.trans h2) (by decide)

/-- The repetition code's repair reads all three cells, and provably must. -/
theorem majorityRepair_not_percell : ¬ ∃ f g h, majorityRepair = percell f g h := by
  rintro ⟨f, g, h, heq⟩
  have h1 := congrArg (fun π => (π (false, false, false)).1) heq
  have h2 := congrArg (fun π => (π (false, true, true)).1) heq
  simp only [majorityRepair, majority, percell] at h1 h2
  simp at h1 h2
  exact absurd (h1.symm.trans h2) (by decide)

/-! ### Per-cell bijections: the share is exactly invariant

A per-cell map whose factors are bijections merely renames the values, slot by
slot. The whole variational problem — the state's entropy AND the pair envelope
it is measured against — is carried along by the renaming, so the share cannot
move. -/

/-- Relabeling a three-slot state's VALUES, slot by slot. -/
def reidx (e₁ e₂ e₃ : Equiv.Perm Bool) (p : Bool × Bool × Bool → ℝ) :
    Bool × Bool × Bool → ℝ :=
  fun t => p (e₁ t.1, e₂ t.2.1, e₃ t.2.2)

/-- Entropy does not read the names of the outcomes: reindexing along any
    bijection leaves `−∑ p log p` unmoved. -/
lemma entropy_reindex {X Y : Type*} [Fintype X] [Fintype Y] (e : X ≃ Y) (p : Y → ℝ) :
    entropy (fun x => p (e x)) = entropy p := by
  unfold entropy
  rw [neg_inj]
  exact Equiv.sum_comp e (fun y => p y * Real.log (p y))

private lemma reidx_eq_comp (e₁ e₂ e₃ : Equiv.Perm Bool) (p : Bool × Bool × Bool → ℝ) :
    reidx e₁ e₂ e₃ p = fun t => p ((e₁.prodCongr (e₂.prodCongr e₃)) t) := rfl

lemma entropy_reidx (e₁ e₂ e₃ : Equiv.Perm Bool) (p : Bool × Bool × Bool → ℝ) :
    entropy (reidx e₁ e₂ e₃ p) = entropy p := by
  rw [reidx_eq_comp]
  exact entropy_reindex _ p

lemma isProb_reidx {e₁ e₂ e₃ : Equiv.Perm Bool} {p : Bool × Bool × Bool → ℝ}
    (hp : IsProb p) : IsProb (reidx e₁ e₂ e₃ p) := by
  refine ⟨fun t => hp.1 _, ?_⟩
  rw [reidx_eq_comp, Equiv.sum_comp (e₁.prodCongr (e₂.prodCongr e₃)) p]
  exact hp.2

private lemma marg₁₂_reidx (e₁ e₂ e₃ : Equiv.Perm Bool) (p : Bool × Bool × Bool → ℝ)
    (ab : Bool × Bool) : marg₁₂ (reidx e₁ e₂ e₃ p) ab = marg₁₂ p (e₁ ab.1, e₂ ab.2) :=
  Equiv.sum_comp e₃ (fun c => p (e₁ ab.1, e₂ ab.2, c))

private lemma marg₁₃_reidx (e₁ e₂ e₃ : Equiv.Perm Bool) (p : Bool × Bool × Bool → ℝ)
    (ac : Bool × Bool) : marg₁₃ (reidx e₁ e₂ e₃ p) ac = marg₁₃ p (e₁ ac.1, e₃ ac.2) :=
  Equiv.sum_comp e₂ (fun b => p (e₁ ac.1, b, e₃ ac.2))

private lemma marg₂₃_reidx (e₁ e₂ e₃ : Equiv.Perm Bool) (p : Bool × Bool × Bool → ℝ)
    (bc : Bool × Bool) : marg₂₃ (reidx e₁ e₂ e₃ p) bc = marg₂₃ p (e₂ bc.1, e₃ bc.2) :=
  Equiv.sum_comp e₁ (fun a => p (a, e₂ bc.1, e₃ bc.2))

/-- The relabeling carries the pair data along: two states with the same pair
    marginals still have the same pair marginals after it. -/
lemma samePairs_reidx (e₁ e₂ e₃ : Equiv.Perm Bool) {p q : Bool × Bool × Bool → ℝ}
    (h : SamePairs p q) : SamePairs (reidx e₁ e₂ e₃ p) (reidx e₁ e₂ e₃ q) := by
  obtain ⟨h12, h13, h23⟩ := h
  refine ⟨?_, ?_, ?_⟩
  · funext ab; rw [marg₁₂_reidx, marg₁₂_reidx, h12]
  · funext ac; rw [marg₁₃_reidx, marg₁₃_reidx, h13]
  · funext bc; rw [marg₂₃_reidx, marg₂₃_reidx, h23]

private lemma reidx_reidx (f₁ f₂ f₃ e₁ e₂ e₃ : Equiv.Perm Bool)
    (p : Bool × Bool × Bool → ℝ) :
    reidx f₁ f₂ f₃ (reidx e₁ e₂ e₃ p)
      = reidx (f₁.trans e₁) (f₂.trans e₂) (f₃.trans e₃) p := rfl

private lemma reidx_refl (p : Bool × Bool × Bool → ℝ) :
    reidx (Equiv.refl Bool) (Equiv.refl Bool) (Equiv.refl Bool) p = p := rfl

private lemma pairEnvelope_reidx_subset (e₁ e₂ e₃ : Equiv.Perm Bool)
    (p : Bool × Bool × Bool → ℝ) : pairEnvelope (reidx e₁ e₂ e₃ p) ⊆ pairEnvelope p := by
  rintro _ ⟨r, hr, hpairs, rfl⟩
  refine ⟨reidx e₁.symm e₂.symm e₃.symm r, isProb_reidx hr, ?_, entropy_reidx _ _ _ r⟩
  have h := samePairs_reidx e₁.symm e₂.symm e₃.symm hpairs
  rwa [reidx_reidx, Equiv.symm_trans_self, Equiv.symm_trans_self, Equiv.symm_trans_self,
    reidx_refl] at h

/-- The pair envelope is carried across by the relabeling, as a SET: every
    competitor on one side has a competitor of equal entropy on the other. -/
lemma pairEnvelope_reidx (e₁ e₂ e₃ : Equiv.Perm Bool) (p : Bool × Bool × Bool → ℝ) :
    pairEnvelope (reidx e₁ e₂ e₃ p) = pairEnvelope p := by
  refine Set.Subset.antisymm (pairEnvelope_reidx_subset e₁ e₂ e₃ p) ?_
  have h := pairEnvelope_reidx_subset e₁.symm e₂.symm e₃.symm (reidx e₁ e₂ e₃ p)
  rwa [reidx_reidx, Equiv.symm_trans_self, Equiv.symm_trans_self, Equiv.symm_trans_self,
    reidx_refl] at h

/-- THE SHARE IS BLIND TO VALUE NAMES. Renaming each slot's values by its own
    bijection leaves the whole-only share exactly unchanged: both the state's
    entropy and the envelope it is measured against move together. -/
theorem share_reidx (e₁ e₂ e₃ : Equiv.Perm Bool) (p : Bool × Bool × Bool → ℝ) :
    share (reidx e₁ e₂ e₃ p) = share p := by
  unfold share
  rw [pairEnvelope_reidx, entropy_reidx]

private lemma pushforward_percell_of_perm (e₁ e₂ e₃ : Equiv.Perm Bool)
    (p : Bool × Bool × Bool → ℝ) :
    pushforward (percell e₁ e₂ e₃) p = reidx e₁.symm e₂.symm e₃.symm p := by
  have hcoe : percell (⇑e₁) (⇑e₂) (⇑e₃) = ⇑(e₁.prodCongr (e₂.prodCongr e₃)) := rfl
  rw [hcoe, pushforward_equiv]
  rfl

/-- A `Bool → Bool` that separates the two bits is a bijection. -/
lemma bool_bijective_of_ne {f : Bool → Bool} (h : f false ≠ f true) :
    Function.Bijective f := by
  refine Finite.injective_iff_bijective.mp ?_
  intro x y hxy
  cases x <;> cases y <;>
    first
      | rfl
      | exact absurd hxy h
      | exact absurd hxy.symm h

/-- A `Bool → Bool` that does not separate the two bits is constant. -/
lemma bool_const_of_eq {f : Bool → Bool} (h : f false = f true) : ∀ x y, f x = f y := by
  intro x y
  cases x <;> cases y <;> simp [h]

/-- PER-CELL BIJECTIONS MINT NOTHING: they leave the share exactly where it was.
    A per-cell bijection is a renaming, and the share does not read names. -/
theorem share_pushforward_percell_of_bijective {f g h : Bool → Bool}
    (hf : Function.Bijective f) (hg : Function.Bijective g) (hh : Function.Bijective h)
    (p : Bool × Bool × Bool → ℝ) :
    share (pushforward (percell f g h) p) = share p := by
  have hcoe : percell f g h = percell (⇑(Equiv.ofBijective f hf))
      (⇑(Equiv.ofBijective g hg)) (⇑(Equiv.ofBijective h hh)) := rfl
  rw [hcoe, pushforward_percell_of_perm, share_reidx]

/-! ### A frozen slot leaves no room above the pairs

If one slot never varies, the state is its own maximum-entropy competitor: the
pair data of the two live slots plus the frozen slot's point mass already
determine every competitor's entropy ceiling, and the state itself attains it.
The stone is `entropy_grouping`, used in each of the three slot positions — the
other two obtained from it by reindexing the slots through an involution. -/

/-- The first single-slot marginal of a three-slot state. -/
noncomputable def marg₁ {α β γ : Type*} [Fintype β] [Fintype γ]
    (p : α × β × γ → ℝ) : α → ℝ :=
  fun a => ∑ b, ∑ c, p (a, b, c)

/-- The second single-slot marginal of a three-slot state. -/
noncomputable def marg₂ {α β γ : Type*} [Fintype α] [Fintype γ]
    (p : α × β × γ → ℝ) : β → ℝ :=
  fun b => ∑ a, ∑ c, p (a, b, c)

/-- Swapping slots one and three: an involution of the three-bit cube. -/
def swap₁₃ : (Bool × Bool × Bool) ≃ (Bool × Bool × Bool) where
  toFun t := (t.2.2, t.2.1, t.1)
  invFun t := (t.2.2, t.2.1, t.1)
  left_inv _ := rfl
  right_inv _ := rfl

/-- Swapping slots two and three: an involution of the three-bit cube. -/
def swap₂₃ : (Bool × Bool × Bool) ≃ (Bool × Bool × Bool) where
  toFun t := (t.1, t.2.2, t.2.1)
  invFun t := (t.1, t.2.2, t.2.1)
  left_inv _ := rfl
  right_inv _ := rfl

/-- Grouping subadditivity with the (2,3) pair against the FIRST slot — the
    orientation `Core.Share`'s `entropy_grouping` does not have, obtained from
    it by reindexing the cube through `swap₁₃`. -/
lemma entropy_grouping₂₃ {q : Bool × Bool × Bool → ℝ} (hq : IsProb q) :
    entropy q ≤ entropy (marg₂₃ q) + entropy (marg₁ q) := by
  have hq' : IsProb (fun t => q (swap₁₃ t)) := by
    refine ⟨fun t => hq.1 _, ?_⟩
    rw [Equiv.sum_comp swap₁₃ q]
    exact hq.2
  have h := entropy_grouping hq'
  have e1 : marg₁₂ (fun t => q (swap₁₃ t))
      = fun x => marg₂₃ q ((Equiv.prodComm Bool Bool) x) := rfl
  have e2 : marg₃ (fun t => q (swap₁₃ t)) = marg₁ q := by
    funext c
    exact Finset.sum_comm
  rw [entropy_reindex swap₁₃ q, e1, e2, entropy_reindex (Equiv.prodComm Bool Bool)] at h
  exact h

/-- Grouping subadditivity with the (1,3) pair against the SECOND slot, from
    `entropy_grouping` by reindexing the cube through `swap₂₃`. -/
lemma entropy_grouping₁₃ {q : Bool × Bool × Bool → ℝ} (hq : IsProb q) :
    entropy q ≤ entropy (marg₁₃ q) + entropy (marg₂ q) := by
  have hq' : IsProb (fun t => q (swap₂₃ t)) := by
    refine ⟨fun t => hq.1 _, ?_⟩
    rw [Equiv.sum_comp swap₂₃ q]
    exact hq.2
  have h := entropy_grouping hq'
  have e1 : marg₁₂ (fun t => q (swap₂₃ t)) = marg₁₃ q := rfl
  have e2 : marg₃ (fun t => q (swap₂₃ t)) = marg₂ q := rfl
  rw [entropy_reindex swap₂₃ q, e1, e2] at h
  exact h

/-- A state's single-slot marginals are fixed by its pair marginals, so every
    competitor in the envelope carries them too. -/
lemma marg₁_of_samePairs {p q : Bool × Bool × Bool → ℝ} (h : SamePairs p q) :
    marg₁ q = marg₁ p := by
  funext a
  have hr : ∀ r : Bool × Bool × Bool → ℝ, marg₁ r a = ∑ b, marg₁₂ r (a, b) := fun _ => rfl
  rw [hr, hr, h.1]

lemma marg₂_of_samePairs {p q : Bool × Bool × Bool → ℝ} (h : SamePairs p q) :
    marg₂ q = marg₂ p := by
  funext b
  have hr : ∀ r : Bool × Bool × Bool → ℝ, marg₂ r b = ∑ a, marg₁₂ r (a, b) := fun _ => rfl
  rw [hr, hr, h.1]

lemma marg₃_of_samePairs {p q : Bool × Bool × Bool → ℝ} (h : SamePairs p q) :
    marg₃ q = marg₃ p := by
  funext c
  have hr : ∀ r : Bool × Bool × Bool → ℝ, marg₃ r c = ∑ b, marg₂₃ r (b, c) :=
    fun _ => Finset.sum_comm
  rw [hr, hr, h.2.2]

/-- A point mass has no entropy. -/
lemma entropy_point_mass {m : Bool → ℝ} {v : Bool}
    (hz : ∀ x, x ≠ v → m x = 0) (h1 : ∑ x, m x = 1) : entropy m = 0 := by
  have hsum := h1
  rw [Fintype.sum_bool] at hsum
  unfold entropy
  rw [Fintype.sum_bool]
  cases v with
  | false =>
      rw [hz true (by decide)] at hsum ⊢
      rw [show m false = 1 by linarith]
      simp
  | true =>
      rw [hz false (by decide)] at hsum ⊢
      rw [show m true = 1 by linarith]
      simp

/-- The maximum-entropy criterion in the form the frozen-slot cases need: if no
    competitor in the envelope beats the state itself, the share is zero. -/
lemma share_eq_zero_of_entropy_maximal {p : Bool × Bool × Bool → ℝ} (hp : IsProb p)
    (h : ∀ q, IsProb q → SamePairs p q → entropy q ≤ entropy p) : share p = 0 := by
  have hgreat : IsGreatest (pairEnvelope p) (entropy p) := by
    refine ⟨⟨p, hp, ⟨rfl, rfl, rfl⟩, rfl⟩, ?_⟩
    rintro _ ⟨q, hq, hpairs, rfl⟩
    exact h q hq hpairs
  unfold share
  rw [hgreat.csSup_eq]
  ring

/-! #### Slot three frozen -/

private lemma entropy_marg₁₂_of_third_det {p : Bool × Bool × Bool → ℝ} {v : Bool}
    (hdet : ∀ a b c, c ≠ v → p (a, b, c) = 0) : entropy (marg₁₂ p) = entropy p := by
  unfold entropy marg₁₂
  cases v with
  | false =>
      have hz : ∀ a b, p (a, b, true) = 0 := fun a b => hdet a b true (by decide)
      simp only [Fintype.sum_prod_type, Fintype.sum_bool, hz, zero_mul, zero_add, add_zero]
  | true =>
      have hz : ∀ a b, p (a, b, false) = 0 := fun a b => hdet a b false (by decide)
      simp only [Fintype.sum_prod_type, Fintype.sum_bool, hz, zero_mul, zero_add, add_zero]

private lemma entropy_marg₃_of_third_det {p : Bool × Bool × Bool → ℝ} {v : Bool}
    (hp : IsProb p) (hdet : ∀ a b c, c ≠ v → p (a, b, c) = 0) : entropy (marg₃ p) = 0 := by
  refine entropy_point_mass (v := v) (fun x hx => ?_) ?_
  · unfold marg₃
    simp [Fintype.sum_bool, show ∀ a b, p (a, b, x) = 0 from fun a b => hdet a b x hx]
  · have hsum := hp.2
    simp only [Fintype.sum_prod_type] at hsum
    unfold marg₃
    calc ∑ c, ∑ a, ∑ b, p (a, b, c) = ∑ a, ∑ c, ∑ b, p (a, b, c) := Finset.sum_comm
      _ = ∑ a, ∑ b, ∑ c, p (a, b, c) := Finset.sum_congr rfl fun _ _ => Finset.sum_comm
      _ = 1 := hsum

/-- A FROZEN THIRD SLOT LEAVES NO WHOLE-ONLY SHARE. If the third slot never
    varies, the state's entropy is exactly that of its (1,2) marginal, the
    frozen slot contributes nothing, and grouping subadditivity makes the state
    its own envelope maximum. -/
theorem share_eq_zero_of_third_det {p : Bool × Bool × Bool → ℝ} {v : Bool}
    (hp : IsProb p) (hdet : ∀ a b c, c ≠ v → p (a, b, c) = 0) : share p = 0 := by
  refine share_eq_zero_of_entropy_maximal hp (fun q hq hpairs => ?_)
  have h := entropy_grouping hq
  rw [hpairs.1, marg₃_of_samePairs hpairs, entropy_marg₁₂_of_third_det hdet,
    entropy_marg₃_of_third_det hp hdet] at h
  linarith

/-! #### Slot one frozen -/

private lemma entropy_marg₂₃_of_first_det {p : Bool × Bool × Bool → ℝ} {v : Bool}
    (hdet : ∀ a b c, a ≠ v → p (a, b, c) = 0) : entropy (marg₂₃ p) = entropy p := by
  unfold entropy marg₂₃
  cases v with
  | false =>
      have hz : ∀ b c, p (true, b, c) = 0 := fun b c => hdet true b c (by decide)
      simp only [Fintype.sum_prod_type, Fintype.sum_bool, hz, zero_mul, zero_add, add_zero]
  | true =>
      have hz : ∀ b c, p (false, b, c) = 0 := fun b c => hdet false b c (by decide)
      simp only [Fintype.sum_prod_type, Fintype.sum_bool, hz, zero_mul, zero_add, add_zero]

private lemma entropy_marg₁_of_first_det {p : Bool × Bool × Bool → ℝ} {v : Bool}
    (hp : IsProb p) (hdet : ∀ a b c, a ≠ v → p (a, b, c) = 0) : entropy (marg₁ p) = 0 := by
  refine entropy_point_mass (v := v) (fun x hx => ?_) ?_
  · unfold marg₁
    simp [Fintype.sum_bool, show ∀ b c, p (x, b, c) = 0 from fun b c => hdet x b c hx]
  · have hsum := hp.2
    simp only [Fintype.sum_prod_type] at hsum
    exact hsum

/-- A FROZEN FIRST SLOT LEAVES NO WHOLE-ONLY SHARE. -/
theorem share_eq_zero_of_first_det {p : Bool × Bool × Bool → ℝ} {v : Bool}
    (hp : IsProb p) (hdet : ∀ a b c, a ≠ v → p (a, b, c) = 0) : share p = 0 := by
  refine share_eq_zero_of_entropy_maximal hp (fun q hq hpairs => ?_)
  have h := entropy_grouping₂₃ hq
  rw [hpairs.2.2, marg₁_of_samePairs hpairs, entropy_marg₂₃_of_first_det hdet,
    entropy_marg₁_of_first_det hp hdet] at h
  linarith

/-! #### Slot two frozen -/

private lemma entropy_marg₁₃_of_second_det {p : Bool × Bool × Bool → ℝ} {v : Bool}
    (hdet : ∀ a b c, b ≠ v → p (a, b, c) = 0) : entropy (marg₁₃ p) = entropy p := by
  unfold entropy marg₁₃
  cases v with
  | false =>
      have hz : ∀ a c, p (a, true, c) = 0 := fun a c => hdet a true c (by decide)
      simp only [Fintype.sum_prod_type, Fintype.sum_bool, hz, zero_mul, zero_add, add_zero]
  | true =>
      have hz : ∀ a c, p (a, false, c) = 0 := fun a c => hdet a false c (by decide)
      simp only [Fintype.sum_prod_type, Fintype.sum_bool, hz, zero_mul, zero_add, add_zero]

private lemma entropy_marg₂_of_second_det {p : Bool × Bool × Bool → ℝ} {v : Bool}
    (hp : IsProb p) (hdet : ∀ a b c, b ≠ v → p (a, b, c) = 0) : entropy (marg₂ p) = 0 := by
  refine entropy_point_mass (v := v) (fun x hx => ?_) ?_
  · unfold marg₂
    simp [Fintype.sum_bool, show ∀ a c, p (a, x, c) = 0 from fun a c => hdet a x c hx]
  · have hsum := hp.2
    simp only [Fintype.sum_prod_type] at hsum
    unfold marg₂
    calc ∑ b, ∑ a, ∑ c, p (a, b, c) = ∑ a, ∑ b, ∑ c, p (a, b, c) := Finset.sum_comm
      _ = 1 := hsum

/-- A FROZEN SECOND SLOT LEAVES NO WHOLE-ONLY SHARE. -/
theorem share_eq_zero_of_second_det {p : Bool × Bool × Bool → ℝ} {v : Bool}
    (hp : IsProb p) (hdet : ∀ a b c, b ≠ v → p (a, b, c) = 0) : share p = 0 := by
  refine share_eq_zero_of_entropy_maximal hp (fun q hq hpairs => ?_)
  have h := entropy_grouping₁₃ hq
  rw [hpairs.2.1, marg₂_of_samePairs hpairs, entropy_marg₁₃_of_second_det hdet,
    entropy_marg₂_of_second_det hp hdet] at h
  linarith

/-! ### Per-cell constants: the output slot freezes, and the share is zero -/

/-- A constant first factor freezes the first output slot, so the pushforward
    has share exactly zero — whatever state it started from. -/
theorem share_pushforward_percell_of_const₁ {f g h : Bool → Bool}
    (hf : ∀ x y, f x = f y) {p : Bool × Bool × Bool → ℝ} (hp : IsProb p) :
    share (pushforward (percell f g h) p) = 0 := by
  refine share_eq_zero_of_first_det (v := f false) (isProb_pushforward _ hp) ?_
  intro a b c ha
  have hfil : Finset.univ.filter (fun x => percell f g h x = (a, b, c)) = ∅ := by
    ext x
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.not_mem_empty, iff_false]
    intro hx
    have hx1 : f x.1 = a := congrArg Prod.fst hx
    exact ha (by rw [← hx1]; exact hf x.1 false)
  simp [pushforward, hfil]

/-- A constant second factor freezes the second output slot. -/
theorem share_pushforward_percell_of_const₂ {f g h : Bool → Bool}
    (hg : ∀ x y, g x = g y) {p : Bool × Bool × Bool → ℝ} (hp : IsProb p) :
    share (pushforward (percell f g h) p) = 0 := by
  refine share_eq_zero_of_second_det (v := g false) (isProb_pushforward _ hp) ?_
  intro a b c hb
  have hfil : Finset.univ.filter (fun x => percell f g h x = (a, b, c)) = ∅ := by
    ext x
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.not_mem_empty, iff_false]
    intro hx
    have hx2 : g x.2.1 = b := congrArg (fun y => y.2.1) hx
    exact hb (by rw [← hx2]; exact hg x.2.1 false)
  simp [pushforward, hfil]

/-- A constant third factor freezes the third output slot. -/
theorem share_pushforward_percell_of_const₃ {f g h : Bool → Bool}
    (hh : ∀ x y, h x = h y) {p : Bool × Bool × Bool → ℝ} (hp : IsProb p) :
    share (pushforward (percell f g h) p) = 0 := by
  refine share_eq_zero_of_third_det (v := h false) (isProb_pushforward _ hp) ?_
  intro a b c hc
  have hfil : Finset.univ.filter (fun x => percell f g h x = (a, b, c)) = ∅ := by
    ext x
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.not_mem_empty, iff_false]
    intro hx
    have hx3 : h x.2.2 = c := congrArg (fun y => y.2.2) hx
    exact hc (by rw [← hx3]; exact hh x.2.2 false)
  simp [pushforward, hfil]

/-- THE NO-CREATION HALF, general in the input state. A map that reads no cell
    but its own can never raise the whole-only share of ANY state. Each factor
    of a per-cell map on bits is either a bijection — in which case the share is
    exactly invariant, the map being a renaming — or a constant, in which case
    the output slot is frozen and the share is exactly zero.

    With `repair_creates_parity` this is the file's separation: creation from
    noise is not a property of maintenance in general, it is a property of
    maintenance that READS THE WHOLE. The two minting maps of this file are
    provably outside the per-cell family (`parityRepair_not_percell`,
    `majorityRepair_not_percell`). -/
theorem percell_no_creation (f g h : Bool → Bool) {p : Bool × Bool × Bool → ℝ}
    (hp : IsProb p) : share (pushforward (percell f g h) p) ≤ share p := by
  by_cases hf : f false = f true
  · rw [share_pushforward_percell_of_const₁ (bool_const_of_eq hf) hp]
    exact share_nonneg hp
  · by_cases hg : g false = g true
    · rw [share_pushforward_percell_of_const₂ (bool_const_of_eq hg) hp]
      exact share_nonneg hp
    · by_cases hh : h false = h true
      · rw [share_pushforward_percell_of_const₃ (bool_const_of_eq hh) hp]
        exact share_nonneg hp
      · exact le_of_eq (share_pushforward_percell_of_bijective (bool_bijective_of_ne hf)
          (bool_bijective_of_ne hg) (bool_bijective_of_ne hh) p)

end CIRISOntology.Core
