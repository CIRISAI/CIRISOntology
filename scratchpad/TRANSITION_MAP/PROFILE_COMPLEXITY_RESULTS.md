# COMPLETE BATH-PROFILE COMPLEXITY — RESULTS

Executed 2026-08-22 against frozen `PROFILE_COMPLEXITY_PREREG.md` on GitHub Actions run `32586261088`.

Artifact `9479172127`; ZIP SHA256 `27e81227c085c404b45bb2c007a049ec56d20704dd12c0b6a4cbc039c00f2a46`.

## Gates

C1–C3 all pass:

- the r=2 smooth family reproduces the earlier approximate-class scale within the frozen one-grid-step tolerance;
- deterministic relabeling mismatch is `4.44e-16`;
- singleton/full-profile control error is `0.0`.

## Headline

**The favorable low-coordinate profile-class result does not extend uniformly as complete bath-profile complexity grows.**

At N=1024:

- FOURIER-SMOOTH r=2: minimum G=`128`;
- FOURIER-SMOOTH r=4: minimum G=`128`;
- FOURIER-SMOOTH r=8: minimum G=`128`;
- FOURIER-SMOOTH r=16: minimum G=`256`;
- FOURIER-SMOOTH r=32: no G<=256 reaches `1e-3` (G=256 error `2.17e-3`).

Thus frozen P1 (all smooth r<=16 bounded by G<=128 with N-stability) **fails**. P2, the weaker coordinate-growth condition G(r=16)<=4 G(r=2), passes because 256<=4*128, but the absolute growth is already large enough to narrow the plausible solver regime.

## Negative control

P4 passes strongly. At N=1024, IID-PROFILES r=8 does not reach `1e-3` for any G<=256; even G=256 has error `6.47e-2`. Higher IID coordinate counts are also strongly noncompressible on the frozen grid.

This demonstrates that the screen is not generically easy: complete-profile class reduction can fail badly when emitter bath profiles have high metric complexity.

## Roughness stake and the important correction

P3, “FOURIER-ROUGH requires more classes than FOURIER-SMOOTH in the majority of matched cells,” fails.

The failure should not be read as evidence that arbitrary rough baths are easy. The deterministic high-harmonic Fourier construction can create repeated/periodic row profiles on a finite ring. Those repetitions are **true bath-equivalence classes**, so some spatially high-frequency profiles collapse exactly or unusually early. For example several N=256 rough families reach machine floor already at G=128 even though their spatial pattern is visually/locally rough.

This identifies a better complexity variable:

**spatial roughness is not sufficient; the relevant object is the covering number / metric entropy of the complete emitter-to-environment coupling-profile set, including exact periodic repetitions.**

A high-frequency but periodic environment may remain symmetry-compressible; a smooth-looking but high-dimensional set of unique profiles may not.

## Representative scaling

For smooth profiles, fixed-G errors grow substantially with coordinate count. At N=1024:

| r | G=64 error | G=128 error | G=256 error |
|---:|---:|---:|---:|
| 2 | 1.70e-3 | 4.28e-4 | 1.07e-4 |
| 4 | 1.16e-3 | 3.27e-4 | 7.54e-5 |
| 8 | 3.09e-3 | 8.39e-4 | 2.17e-4 |
| 16 | 7.09e-3 | 1.67e-3 | 3.84e-4 |
| 32 | 3.55e-2 | 8.89e-3 | 2.17e-3 |

The finite-time class complexity therefore depends materially on the number of independently active complete-profile coordinates even when each coordinate is spatially smooth.

## Consequence for the chemistry bridge

Before proposing approximate bath-equivalence as a real molecular-polariton solver primitive, one must estimate from a physical environment model or ab initio/system-bath calculation:

1. the number of materially active spatial/vibrational coupling coordinates;
2. the distribution/covering number of complete molecule-to-bath profile vectors at the physically relevant tolerance;
3. exact or near periodic/profile repetitions;
4. how this profile metric entropy changes with aggregate size.

A single correlation length, covariance rank, or visual smoothness measure is insufficient.

## Simulation consequence

This result narrows rather than kills the profile-class route. Low-complexity profile manifolds can yield N-stable reductions, but multi-coordinate or IID profiles rapidly consume the reduction budget. The separate `FAIR_PROPAGATOR_COST_PREREG.md` decides whether the surviving low-complexity regime buys actual arithmetic after a common-kernel comparison.

## Fence

The synthetic Fourier/random/IID families are stress tests, not models of a specific molecular cavity. P3's failure also shows why “roughness” should not be promoted as a physical law. The measurable target is complete-profile metric entropy / equivalence structure.
