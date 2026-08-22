# ATTACKING THE OPEN BRANCH — contraction maps as a source of QUANTUM entropy inequalities
(sealed 2026-08-23)

The authors of arXiv:2409.17317 prove (Cor 4.1) that a quantum inequality with M LHS
terms needs N ≤ M, and write: *"We leave a detailed discussion about generating valid
quantum inequalities from contraction maps for future work."* This is that sweep, run
to the M=4 bound at n=4.

## RESULT — a bounded NEGATIVE, stated first
**The contraction-map generator under M ≥ N produces NO candidate quantum entropy
inequality at n = 4 for M ≤ 4.** Every candidate it yields is either already implied by
strong subadditivity, or is a valid HOLOGRAPHIC inequality that quantum states refute.
The M ≥ N condition is necessary but very far from sufficient.

## The ladder, with every count
| stage | result |
|---|---|
| checker controls | MMI ✓, **MMI-reversed correctly REJECTED** ✓, SA ✓, SSA ✓ |
| n=3, M ≤ 3 (control: cone known = SSA+WM) | 177 candidates, **0 refuted**, all consequences — correct |
| n=4, M ≤ 3 | 4,965 candidates, 0 refuted, **ALL implied by SSA** |
| n=4, M = 4, GPU boundary filter | 2,650,215 pairs → **37,410** survive (70×, sub-second on the 4090) |
| n=4, M = 4, exact CSP | **36,530** admit contraction maps |
| … of those, not implied by SSA | **200** |
| … surviving refutation | **0** |

The GPU did the part it should: the boundary conditions must themselves be contracting
(`popcount(x_p⊕x_q) ≥ popcount(y_p⊕y_q)` over the 5 subsystems, plus well-definedness),
which is pure bit arithmetic over millions of candidates. Only survivors reached the
branchy CSP.

## The 200 are the MMI family, and GHZ kills them
Inspecting a survivor showed the shape immediately: `S(A) + S(BC) + S(BD) + S(CD) ≥
S(B) + S(C) + S(D) + S(BCD)` is exactly **MMI + S(A)**. Valid holographically; refuted
by any state where a subsystem decouples while the rest violates MMI. All 200 die to
GHZ states on 4 of the 5 subsystems, in blocks of 40.

## A METHOD FAILURE I CAUGHT AND MUST RECORD
Refutation round 1 — GHZ(5), W(5), and **6,000 random full-support pure states** —
reported **160 of 200 surviving**. That was WRONG, and wrong in the dangerous
direction: it would have been a "candidate new quantum inequality" headline. The cause:
random full-support states never DECOUPLE a subsystem, so they cannot exhibit the
S(A)=0-with-MMI-violated configuration that kills these candidates. Round 2 added
product/decoupled structures and killed all 200.
**The lesson, worth more than the sweep: a refutation search is only as strong as the
structures it can produce, and random sampling of a big space is not coverage.** The
survivor was caught by READING it and recognising MMI + S(A), not by more sampling.

## What is and is not established
ESTABLISHED: within n=4 and M ≤ 4, contraction maps under Cor 4.1's necessary condition
generate nothing that is both un-implied by SSA and un-refutable — a bounded, concrete
answer to a question the authors posed and left open.
NOT ESTABLISHED, and not claimed: whether new unconstrained quantum entropy inequalities
exist. That remains open. We have shown one generation method, at one bound, does not
produce a candidate. Extending to M ≥ 5 or n ≥ 5 is mechanical with the GPU filter and
is the obvious continuation.
