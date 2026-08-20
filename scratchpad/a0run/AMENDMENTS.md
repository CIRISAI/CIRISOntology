# A0 — AMENDMENTS (append-only; each entry written BEFORE the deviating computation runs)

Format: `## A<n> — <UTC timestamp> — <title>` then what changes, why, and whether any
outcome-crossed number had been seen at the time of writing.

---

## A0-NOTE-1 — 2026-08-20 — Execution-order reading (NOT a design change)

§12's execution order lists CP-FACT second, before the judged arms. §18's freeze stamp says
"the outcome column is opened only by the analysis stage, after every gate that can be
evaluated without it." These are reconciled as: all outcome-blind work (frames, MC2, MC1, the
main judging pass, the adversarial probe's CALLS, the diff arm) runs first and writes its
done-markers; the outcome column is then opened and **CP-FACT runs first among the
outcome-crossing computations**, with the §6.2 tautology diagnostic last, exactly as §12 and
freeze item 22 require. The protective property §12 gives for CP-FACT-first — that a judge
failure cannot be blamed for CP-FACT's result — is preserved because CP-FACT reads no panel
output at any point, and the panel's labels are frozen to disk and hashed before the outcome
opens.

The adversarial leak probe (§6.5) is split accordingly: its judge calls are outcome-blind and
run in OB5; its AUC against the true override (gate V7b) is an outcome-crossing computation and
is discharged in the analysis stage, before any band is read, as §12 step 7 requires relative to
steps 9-10.

No outcome-crossed number had been seen when this note was written.

---

## A0-NOTE-2 — 2026-08-20 — N1c mixing gate: which "distinct tables" (reading pinned BEFORE the chain runs)

sec 7.4's mixing gate declares N1c NON-MIXING if "fewer than 1,000 distinct tables are
visited across the 10,000 recorded draws". "Table" is not defined there. Two readings exist:
(a) the 3-way contingency table, and (b) the chain's state (the assignment of cluster-level
OVR vectors to clusters). For a 2x2x2 with all three 2-way margins fixed the fiber is a
one-dimensional integer lattice whose length is set by the margins, and it may contain fewer
than 1,000 points in total — in which case reading (a) cannot be passed by ANY chain, however
perfectly it mixes.

**Pinned now, before the chain is run and before any outcome-crossed number is seen:** the
gate is evaluated on reading (a), the literal one, and its pinned NON-MIXING consequence (fall
back to N2 and print the A-O and C-O margin drift) is taken if it fires. Reading (b) and the
EXACT fiber size (from N1's enumeration) are reported beside it, so a reader can see whether a
fired gate is a property of the chain or of the fiber. The verdict is not read from the
reading that gives the more convenient answer: the literal reading governs, the fallback is
the pinned one, and the diagnosis is disclosed.

No outcome-crossed number had been seen when this note was written.

---

## A0-NOTE-3 — 2026-08-20 — N1c is degenerate BY CONSTRUCTION (analytic prediction, recorded before the chain is run)

Not a design change: N1c is implemented and run exactly as sec 7.4 pins it, and its
pre-registered NON-MIXING consequence is taken if its gate fires. This note records, in
advance, an analytic proof of WHY the gate will fire, so the empirical check below is a
forward prediction and not a post-hoc rationalisation.

**Claim.** Under sec 7.4's move set, every ACCEPTED N1c move leaves the 3-way (A, C, O)
contingency table completely unchanged. The null is therefore a point mass at the observed
share, for any corpus in which the context leg is constant within every cluster.

**Proof.** Let two clusters c1, c2 be equal in size, language and version, with row-wise action
labels A1, A2 and OVR vectors v1, v2. Both carry the SAME language L (required by the move
set). A and C never move, so only cells with context L can change, and the change in cell
(a, L, 1) is
    delta_a = sum_i 1{A1_i = a}(v2_i - v1_i) + sum_i 1{A2_i = a}(v1_i - v2_i).
Because L is the only context touched, the induced change in the A-O two-way margin cell
(a, 1) is exactly delta_a. Acceptance requires the A-O margin to be unchanged, i.e.
delta_a = 0 for every a, which is precisely the condition that every cell of the 3-way table is
unchanged. QED.

**Consequence, and it is the pinned one.** Distinct tables visited = 1 < 1,000, so N1c is
declared NON-MIXING by its own sec 7.4 gate; the verdict falls back to N2 with the A-O and C-O
margin drift printed, exactly as pinned. N1 (the exact conditional fiber enumeration) is
reported beside it as the exactness reference sec 7.4 makes it. No new null is invented after
freeze.

**Why this is not a rescue in disguise.** The failure is in the direction that makes the
verdict HARDER to obtain, not easier: N2 does not condition on the A-O and C-O margins, so the
null it produces is wider than the conditional one, and a share that clears N2's 99th
percentile has cleared a bar the conditional test would have set lower. The reader is owed the
drift numbers to see exactly what the fallback stopped conditioning on, and sec 7.4 requires
them to be printed.

No outcome-crossed number had been seen when this note was written.

---

## A0-NOTE-4 — 2026-08-20 — Consequences of the N1c degeneracy for the MI floors (V6, V7, V12, sec 10.1)

Written before the analysis stage runs. Follows from A0-NOTE-3 and invokes sec 7.4's own
NON-MIXING fallback; no new construction is invented.

sec 10.1 subtracts "its N1c permutation mean" from each of I_K and I_L, and V6 admits the
legacy arm if I_L exceeds "its own N1c permutation 95th percentile". A mutual information
between one predictor and the override IS a function of that predictor's two-way margin with
the override. N1c accepts only moves that leave that margin unchanged (A0-NOTE-3), so an N1c
ensemble reproduces the observed MI exactly and has zero spread: it cannot supply a floor or a
percentile for ANY of these gates, for the same structural reason it cannot supply a null for
the share.

**Pinned, before any of these numbers is computed:** wherever sec 10 calls for an "N1c
permutation" of a mutual information, the pinned NON-MIXING fallback applies and the null is
**N2** — permutation of the override vectors among whole canonical `task_id` clusters of equal
size, 10,000 draws. This is the same substitution sec 7.4 already pins for the share, applied
to the same gate family, and it is the conservative direction: N2's ensemble is wider than the
conditional one, so a floor read from it is larger and an arm must clear a higher bar to pass
V6 or V12.

**V7's ratio, pinned now:** I_leak and I_kind are compared on their FLOOR-SUBTRACTED values
(each minus its own N2 permutation mean), because the leak arm realises up to six levels
against the kind arm's five and an unsubtracted ratio would reward the arm with more degrees of
freedom. The raw ratio is reported beside it. sec 11 already requires every MI to be reported
floor-subtracted; this states which of the two the gate reads.

No outcome-crossed number had been seen when this note was written.

---

## A0-NOTE-5 — 2026-08-20 — Code defect found and fixed mid-run (diff arm only)

The OB6 diff-arm stage read the heuristic instruments' result key as `fires`; the instruments
return `fired`. The first run therefore reported zero firings for all five instruments. The key
was corrected and OB6 was re-run in full before any diff-arm number entered A0_RESULTS.md.

Blast radius: none. The diff arm is outcome-blind, is a declared secondary, and is never
kill-bearing under any outcome (sec 5.4). No gate, null, band or verdict depends on it. Both the
defective and the corrected runs happened while the outcome column was still sealed.
