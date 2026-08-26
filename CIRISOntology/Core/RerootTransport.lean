/-
CIRISOntology.Core.RerootTransport — R1's missing grammar: the claim square,
and the fence that a correspondence is not a license.

PROVENANCE, because it matters what this is and is not. This file originated on
`experiment/quantum-native-r1`, whose larger proposal was to re-present the
maximal object with a quantum World, density operators and Kraus channels. That
proposal is NOT adopted: a universal encoding into which every finite map lifts
is a re-description rather than a simplification, and the object earns its keep
by REFUSING (floors, ceilings, non-factoring, VOID) rather than by admitting
everything. This result is taken on its own merits, standing alone: it needs no
Hilbert space, no channel, and no tiered carrier, and its import of the quantum
scaffolding was incidental and is removed. The quantum branch informed and
inspired; it did not land.

WHAT R1 SAYS AND WHAT THIS ADDS. `Core/Factoring.lean` establishes that
`Factors` does not transport a claim across incomparable roots, and `OBJECT.md`
records the refinement: correspondence (which claimant HERE is the same one
THERE) is a different question from claim transport (does a license survive it).
The correspondence layer has a concrete spatial instance; the transport layer
had no grammar. This is the grammar:

    source state  ──reroot──▶  target state
         │ sourceClaim              │ targetClaim
         ▼                          ▼
    source reading ──carry──▶ target reading

`ClaimTransport` is that square. It has identity and composition, and
`carry_path_independent` proves direct and composed readings agree on every
presented source claimant whenever the underlying reroot maps agree — so
Newton, position, momentum, energy and orientation do NOT each earn a separate
composition theorem. No surjectivity fiction: as in `Habit.rate_unique_on_range`,
the carried map is constrained on the source claim's actual range.

CERTIFICATES ARE A SECOND SQUARE, AND THE FENCE IS THE POINT.
`CertifiedTransport` additionally requires the source license to imply the
target license, and that field is never inferred from correspondence.
`claim_transport_does_not_grant_certificate` proves the two are logically
independent — but that witness is DEGENERATE, its target certificate valid of
nothing, so it shows only that the second field cannot be derived. Added here:
`certificate_fails_on_a_satisfiable_target`, where BOTH certificates are
satisfiable and the obstruction is real — a genuine license the carry simply
does not land in. A fence demonstrated only on an unsatisfiable target is a
fence nobody has shown can be met, which is this repository's own
non-vacuity standard applied to its own fence.

THE FINITE THREE-ROOT INSTRUMENT at the foot is theorem-shaped and
mutation-sensitive: two roots each flip a represented orientation, the direct
map flips twice, state maps and transports compose exactly, and a planted wrong
middle map is PROVED unequal. It validates the grammar. It does NOT assert that
the simulator has measured a physical internal orientation across those tiers —
each physical claim still owes its own `CertifiedTransport`, which is exactly
what keeps R1 open rather than closing it by construction.
-/
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

/-- **THE DIAGNOSTIC DIRECTION, mechanized — and twice measured before it was
    stated.** `comp` says a composite is certified when both legs are. The
    contrapositive with one leg in hand is how a failed composite CONVICTS the
    other leg: if the first leg carries its certificate and the composite
    cannot, then no certified second leg exists at all.

    This is the inference the hardware campaigns performed at the counts level,
    now stated once:
    * RESTORATION (`scratchpad/temporal-share/RESTORATION_RESULTS.md`): prep and
      readout near-ideal (joint view 1.9× floor idle) while the composite
      splits the n-fibers at 105× — the conviction lands on the gate.
    * S1 reciprocal (`scratchpad/composition/S1_RESULTS.md`): first CRX at 0.96
      fidelity while the composite's reverse influence reads 0.082 against an
      ideal 0.50 — the conviction lands on the second CRX.

    The physical face of the second-square fence: a certificate granted for the
    DECLARED arrow does not transport to the REALIZED arrow, and when the
    composite fails, this lemma is what localizes the failure. -/
theorem comp_failure_convicts_second_leg
    (ab : CertifiedTransport rab qa qb ca cb)
    (h : ¬ Nonempty (CertifiedTransport (rbc ∘ rab) qa qc ca cc)) :
    ¬ Nonempty (CertifiedTransport rbc qb qc cb cc) :=
  fun ⟨bc⟩ => h ⟨ab.comp bc⟩

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

private def trueClaim : Unit → Bool := fun _ => true
private def falseClaim : Unit → Bool := fun _ => false
private def validTrue : Certificate Bool := ⟨fun q => q = true⟩

/-- **THE NON-DEGENERATE FENCE.** The theorem above uses a target certificate
    valid of NOTHING, so it establishes only that the license field cannot be
    derived from the square. Here both certificates are SATISFIABLE — `true`
    meets each — and the transport still cannot exist, because the lawful carry
    lands on `false`. A real license, reachable in principle, that this
    correspondence does not deliver. That is the obstruction R1 actually names,
    rather than an artefact of an empty predicate. -/
theorem certificate_fails_on_a_satisfiable_target :
    Nonempty (ClaimTransport (id : Unit → Unit) trueClaim falseClaim) ∧
    (∃ q, validTrue.valid q) ∧
    ¬ Nonempty (CertifiedTransport (id : Unit → Unit) trueClaim falseClaim
      validTrue validTrue) := by
  refine ⟨⟨⟨fun _ => false, rfl⟩⟩, ⟨true, rfl⟩, ?_⟩
  rintro ⟨T⟩
  have hc : (falseClaim ∘ (id : Unit → Unit)) () = (T.claims.carry ∘ trueClaim) () :=
    congrFun T.claims.commutes ()
  have hcarry : T.claims.carry true = false := by
    simpa [trueClaim, falseClaim, Function.comp] using hc.symm
  have hval := T.carriesCertificate true rfl
  rw [hcarry] at hval
  simp [validTrue] at hval

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
