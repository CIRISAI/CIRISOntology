# K2.3 LINEWIDTH FORMULA — external verification and two corrections owed (2026-08-23)

Independent verification agent, arXiv API + Crossref + targeted full-text fetches,
with the algebra checked symbolically and numerically. Result: **the formula is
STANDARD PHYSICS — a rederivation, not a discovery.** Recorded so the campaign
never stakes novelty on it.

## Q1 — VERDICT: KNOWN, and the identity is exact
`C(kappa) = sum_j |<b_j|V|d>|^2 kappa/((E_d-E_j)^2+(kappa/2)^2)` IS the second-order
Feshbach (P-Q partitioning) self-energy of a discrete state coupled to a Lindblad-damped
manifold: `Gamma = -2 Im Sigma`. The verifier's sympy check reports the **symbolic
difference is identically zero**, with numerical agreement to ~2e-5 relative at s=1e-3
against exact non-Hermitian diagonalization, and `Gamma/s^2` constant to 8 digits over
s = 1e-1..1e-4. It is simultaneously:
- Fermi golden rule with Lorentzian-broadened final states (literally
  `Gamma = 2 pi sum_j |V_dj|^2 L_kappa(E_d - E_j)`);
- a SUM OF DETUNED PURCELL RATES — Auffeves, Gerace, Gerard, Franca Santos, Andreani,
  PRB 81, 245419 (2010) Eq. (7) reduces term-by-term to ours at gamma=gamma*=0;
- the discrete-sum form of the cavity-protection kernel — Diniz, Portolan, Ferreira,
  Gerard, Bertet, Auffeves, PRA 84, 063810 (2011) Eq. (6);
- Bixon-Jortner (JCP 48, 715, 1968) and Fano (PR 124, 1866, 1961) in the kappa->0 limit;
- the quantum Zeno law `Gamma -> 4 sum_j |V_dj|^2 / kappa` in the kappa->inf limit.
Review: Auerbach & Zelevinsky, Rep. Prog. Phys. 74, 106301 (2011).
**Stance consequence: no novelty may be claimed for the formula.** Its value to us is
as a VALIDATED INSTRUMENT, which is what an anchor is for (alignment rule A1).

## CORRECTION 1 (owed to DARK_STATE_K23_RESULTS.md) — the turnover is CONDITIONAL
The kappa-turnover is REGIME-DEPENDENT, not generic. For a single bright state at
detuning Delta, `C(kappa)` peaks at `kappa = 2|Delta|` with `C_max = |V|^2/|Delta|`
(verifier's numerics: peak at kappa = 1.999998 for Delta = 1). **ON RESONANCE
(Delta = 0) there is NO peak at all** — `C = 4|V|^2/kappa` decreases monotonically.
The campaign's own data is consistent with this (Str/Cir turns over, Pri/Prc does not),
so the MEASUREMENT stands; what needs the condition attached is the MECHANISM SENTENCE.
Any statement of the form "resonance enhancement then Zeno suppression" must carry
"for detuned bright manifolds" or it overclaims.

## CORRECTION 2 — "parameter-free" is not a distinguishing virtue
Second-order perturbation theory ALWAYS returns a coefficient with no free parameters.
The epistemic content is only whether `|<b_j|V|d>|^2`, `E_j` and `kappa` are
**independently measured**. Campaign write-ups that lean on "parameter-free" as the
strength of the result should say instead: predicted-before-fitting, on inputs taken
from the symmetry-restored spectrum.

## Q2 — CONFIRMED with two caveats
The linear-coupling / quadratic-loss pair IS canonical quasi-BIC scaling: Koshelev,
Lepeshov, Liu, Bogdanov, Kivshar, PRL 121, 193903 (2018) Eq. (3),
`Q_rad = Q_0 [alpha]^(-2)`; review Hsu, Zhen, Stone, Joannopoulos, Soljacic,
Nat. Rev. Mater. 1, 16048 (2016). Caveats to carry: the alpha^-2 law is stated for
SMALL alpha only; and linear opening is GENERIC BUT NOT GUARANTEED — if a residual
symmetry survives or the breaking enters at higher multipole order, the leading
coupling is higher order. It holds when the breaking has a nonzero first-order matrix
element, which is the generic case.

## Q3 — what an actual test against nature would need
The rare ingredient is a **kappa SWEEP with everything else fixed** — that tests
C(kappa) as a FUNCTION rather than at a point. Ranked candidates:
1. Cold-atom cavity QED with controlled disorder — Baghdad, Bourdel, Schwartz, Ferri,
   Reichel, Nature Physics 19, 1104 (2023). Has the rare piece: independently TUNABLE
   AND KNOWN disorder distribution. Lacks a kappa sweep; measures bright polaritons.
2. NV ensemble + superconducting resonator — Putz et al., Nature Physics 10, 720
   (2014); Kubo et al., PRL 105, 140502 (2010). Best-characterised kappa and
   distribution; limited kappa tunability, near-Lorentzian distribution.
3. Photonic quasi-BIC metasurfaces (Koshelev above) — tests the EXPONENT, not the
   coefficient; kappa not independently tunable.
4. Erbium in a nanophotonic cavity (arXiv:2309.16641, UNREFEREED) — has the detuning
   axis at fixed kappa.
5. Superconducting/waveguide-QED subradiance (NJP 21, 025003, 2019) — few emitters.
DO NOT CITE as data: arXiv:2304.13123 (Q-factor sweep) is MOLECULAR DYNAMICS
SIMULATION, not experiment. Flagged by the verifier as an easy trap.

## Verification limits, carried
WebSearch was exhausted before the sweep began and OpenAlex hit its daily cap; the
sweep is arXiv + Crossref + targeted fetches. That STRONGLY supports "the formula is
in the literature" (found four times over) and only WEAKLY supports "nobody published
this exact packaging" — so the packaging must NOT be reported as novel. Koshelev's
supplemental, Bixon-Jortner's original equations, and Fano's equation number could not
be opened; independence of kappa and disorder measurement in candidates 1 and 4 needs
full text before anything is staked on either.
