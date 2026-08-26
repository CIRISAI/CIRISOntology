/-
CIRISOntology.Core.RerootTransport — R1's missing grammar, with the blanket
reading killed and the claim-specific reading compositional.

R1 said that `Factors` does not transport a claim across incomparable roots.
That remains true.  The correction is not to force the roots into one Factors
chain; it is to require two independently named maps and one square:

    source state  ──reroot──▶  target state
         │ sourceClaim              │ targetClaim
         ▼                          ▼
    source reading ──carry──▶ target reading

`ClaimTransport` is precisely that square.  It composes, and
`carry_path_independent` proves that direct and composed claim readings agree
on every source claimant whenever the underlying reroot maps agree.  No
surjectivity fiction is needed: as with `Habit.rate_unique_on_range`, the
carried map is constrained on the source claim's actual range.

CERTIFICATES ARE A SECOND SQUARE.  `CertifiedTransport` additionally requires
the source license to imply the target license.  The theorem
`claim_transport_does_not_grant_certificate` exhibits a claim correspondence
for which no such license transport can exist.  This is the formal fence behind
the engine's minted-vs-transported quantities and prevents a correspondence
receipt from silently becoming a physical certificate.

The finite orientation triangle at the foot is an executable theorem-shaped
instrument: Sandbox -> Grain and Grain -> Crystal each flip the represented
orientation; the direct Sandbox -> Crystal map flips twice.  State maps and
claim/certificate transports compose exactly, while a planted wrong middle map
is proved unequal.  It validates the grammar and its mutation sensitivity.  It
does not assert that the simulator has measured a physical internal orientation
across those tiers; the Rust Q32 probe supplies the current concrete spatial
instance, and each physical claim still owes its own `ClaimTransport`.
-/
import CIRISOntology.Core.NativeObject
import Mathlib.Tactic

namespace CIRISOntology.Core.RerootTransport

/-! ### The claim-transport square -/

/-- A named re-root carries a named claim exactly when this square commutes. -/
structure ClaimTransport {A B QA QB : Type*}
    (reroot : A → B) (sourceClaim : A → QA) (targetClaim : B → QB) where
  carry : QA → QB
  commutes : targetClaim ∘ reroot = carry ∘ sourceClaim

namespace ClaimTransport

variable {A B C QA QB QC : Type*}
variable {rab : A → B} {rbc : B → C} {rac : A → C}
variable {qa : A → QA} {qb : B → QB} {qc : C → QC}

/-- Pointwise form of the claim-transport square. -/
theorem commutes_apply (T : ClaimTransport rab qa qb) (a : A) :
    qb (rab a) = T.carry (qa a) :=
  congrFun T.commutes a

/-- Identity correspondence transports every claim by identity. -/
def id (q : A → QA) : ClaimTransport (id : A → A) q q where
  carry := _root_.id
  commutes := rfl

/-- Claim transport composes along re-root paths. -/
def comp (ab : ClaimTransport rab qa qb) (bc : ClaimTransport rbc qb qc) :
    ClaimTransport (rbc ∘ rab) qa qc where
  carry := bc.carry ∘ ab.carry
  commutes := by
    funext a
    change qc (rbc (rab a)) = bc.carry (ab.carry (qa a))
    rw [bc.commutes_apply, ab.commutes_apply]

/-- **R1 PATH LAW.** If the direct and composed state correspondences agree,
    the direct and composed carried claims agree on every presented source
    claimant.  The law is deliberately range-scoped. -/
theorem carry_path_independent
    (direct : ClaimTransport rac qa qc)
    (ab : ClaimTransport rab qa qb) (bc : ClaimTransport rbc qb qc)
    (hpath : rac = rbc ∘ rab) (a : A) :
    direct.carry (qa a) = bc.carry (ab.carry (qa a)) := by
  calc
    direct.carry (qa a) = qc (rac a) := (direct.commutes_apply a).symm
    _ = qc ((rbc ∘ rab) a) := by rw [hpath]
    _ = bc.carry (qb (rab a)) := bc.commutes_apply (rab a)
    _ = bc.carry (ab.carry (qa a)) :=
      congrArg bc.carry (ab.commutes_apply a)

end ClaimTransport

/-! ### A physical license is extra structure -/

/-- A certificate is a predicate on a claim reading. -/
structure Certificate (Q : Type*) where
  valid : Q → Prop

/-- Claim transport plus an explicit law carrying the source license to the
    target license.  This field is never inferred from correspondence alone. -/
structure CertifiedTransport {A B QA QB : Type*}
    (reroot : A → B) (sourceClaim : A → QA) (targetClaim : B → QB)
    (sourceCertificate : Certificate QA) (targetCertificate : Certificate QB) where
  claims : ClaimTransport reroot sourceClaim targetClaim
  carriesCertificate : ∀ q, sourceCertificate.valid q →
    targetCertificate.valid (claims.carry q)

namespace CertifiedTransport

variable {A B C QA QB QC : Type*}
variable {rab : A → B} {rbc : B → C}
variable {qa : A → QA} {qb : B → QB} {qc : C → QC}
variable {ca : Certificate QA} {cb : Certificate QB} {cc : Certificate QC}

/-- Licensed claim transport composes only because both legs separately carry
    their license. -/
def comp (ab : CertifiedTransport rab qa qb ca cb)
    (bc : CertifiedTransport rbc qb qc cb cc) :
    CertifiedTransport (rbc ∘ rab) qa qc ca cc where
  claims := ab.claims.comp bc.claims
  carriesCertificate := by
    intro q hq
    exact bc.carriesCertificate _ (ab.carriesCertificate q hq)

end CertifiedTransport

/-! ### The separable fence: correspondence is not certification -/

private def unitClaim : Unit → Bool := fun _ => false
private def sourceAlways : Certificate Bool := ⟨fun _ => True⟩
private def targetNever : Certificate Bool := ⟨fun _ => False⟩

/-- A perfectly lawful claim transport can exist while certificate transport is
    impossible.  Therefore R1 cannot be closed by treating a receipt as a
    certificate or by adding every root to one sum type. -/
theorem claim_transport_does_not_grant_certificate :
    Nonempty (ClaimTransport (id : Unit → Unit) unitClaim unitClaim) ∧
    ¬ Nonempty (CertifiedTransport (id : Unit → Unit) unitClaim unitClaim
      sourceAlways targetNever) := by
  constructor
  · exact ⟨ClaimTransport.id unitClaim⟩
  · rintro ⟨T⟩
    exact T.carriesCertificate false trivial

/-! ### A finite, mutation-sensitive three-root instrument -/

/-- Two bits stand in for one internal orientation presented in three roots. -/
abbrev Orientation := Bool × Bool

def sandboxToGrain : Orientation → Orientation :=
  fun x => (!x.1, x.2)

def grainToCrystal : Orientation → Orientation :=
  fun x => (x.1, !x.2)

def sandboxToCrystal : Orientation → Orientation :=
  fun x => (!x.1, !x.2)

def orientationClaim : Orientation → Bool :=
  fun x => Bool.xor x.1 x.2

def sandboxGrainClaims :
  ClaimTransport sandboxToGrain orientationClaim orientationClaim where
  carry := Bool.not
  commutes := by
    funext x
    rcases x with ⟨a, b⟩
    cases a <;> cases b <;> rfl

def grainCrystalClaims :
  ClaimTransport grainToCrystal orientationClaim orientationClaim where
  carry := Bool.not
  commutes := by
    funext x
    rcases x with ⟨a, b⟩
    cases a <;> cases b <;> rfl

def sandboxCrystalClaims :
  ClaimTransport sandboxToCrystal orientationClaim orientationClaim where
  carry := _root_.id
  commutes := by
    funext x
    rcases x with ⟨a, b⟩
    cases a <;> cases b <;> rfl

/-- The two state-level paths agree for every orientation. -/
theorem orientation_state_path :
    sandboxToCrystal = grainToCrystal ∘ sandboxToGrain := by
  funext x
  rcases x with ⟨a, b⟩
  cases a <;> cases b <;> rfl

/-- The content-bearing claim has the same direct and composed reading. -/
theorem orientation_claim_path (x : Orientation) :
    sandboxCrystalClaims.carry (orientationClaim x) =
      grainCrystalClaims.carry
        (sandboxGrainClaims.carry (orientationClaim x)) :=
  ClaimTransport.carry_path_independent sandboxCrystalClaims
    sandboxGrainClaims grainCrystalClaims orientation_state_path x

private def evenCertificate : Certificate Bool :=
  ⟨fun q => q = false⟩

private def oddCertificate : Certificate Bool :=
  ⟨fun q => q = true⟩

def sandboxGrainCertified : CertifiedTransport sandboxToGrain
    orientationClaim orientationClaim evenCertificate oddCertificate where
  claims := sandboxGrainClaims
  carriesCertificate := by
    intro q hq
    cases q <;> simp_all [evenCertificate, oddCertificate, sandboxGrainClaims]

def grainCrystalCertified : CertifiedTransport grainToCrystal
    orientationClaim orientationClaim oddCertificate evenCertificate where
  claims := grainCrystalClaims
  carriesCertificate := by
    intro q hq
    cases q <;> simp_all [evenCertificate, oddCertificate, grainCrystalClaims]

/-- The license survives the two-leg path because each leg earns transport. -/
def sandboxCrystalCertifiedViaGrain : CertifiedTransport
    (grainToCrystal ∘ sandboxToGrain) orientationClaim orientationClaim
    evenCertificate evenCertificate :=
  sandboxGrainCertified.comp grainCrystalCertified

private def wrongMiddle : Orientation → Orientation := id

/-- The path gate has teeth: replacing the second correspondence by identity is
    provably not the direct Sandbox -> Crystal map. -/
theorem wrong_middle_map_caught :
    sandboxToCrystal ≠ wrongMiddle ∘ sandboxToGrain := by
  intro h
  have hpoint := congrFun h (false, false)
  simp [sandboxToCrystal, wrongMiddle, sandboxToGrain] at hpoint

end CIRISOntology.Core.RerootTransport
