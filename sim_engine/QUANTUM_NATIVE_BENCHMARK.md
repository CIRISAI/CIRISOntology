# Quantum-native crossover benchmark — preregistration

## Question

Can the CIRIS quantum-native object outperform optimized OpenQASM simulators
on the structured physical domains it represents, while returning the same
declared observables to the same error budget?

This is a crossover claim, not a universal simulator claim. The Rapier results
justify testing specialization; they do not predict a quantum-circuit win.

## Falsifiable hypothesis

The native path wins only when it can retain a representation substantially
smaller than a generic full statevector: a fixed symmetry sector, bounded-bond
MPS, sparse local operator, stabilizer-like fragment, or symbolic diagonal
classical channel. It should lose or converge to the baseline on arbitrary
deep circuits whose entanglement forces that representation to grow toward the
full Hilbert space.

For `n` qubits and `G` gates, a generic statevector baseline touches a state of
size `2^n`; an exact MPS path replaces that dimension with a bond dimension
whose worst case is still exponential. The CIRIS advantage, if any, must come
from preserving a smaller physical sector or avoiding QASM lowering and
generic gate dispatch—not from changing those worst-case facts.

## Baselines

Pin versions and build flags before timing:

- Google qsim, CPU statevector and GPU where available;
- Qiskit Aer `statevector`, `matrix_product_state`, and applicable tensor or
  stabilizer methods;
- Qulacs CPU/GPU;
- NVIDIA cuStateVec/cuTensorNet on the matched GPU lane.

The best valid baseline per workload is the comparator. A slow default backend
does not count.

## Workloads

Each workload must have both a native representation and a semantically
equivalent QASM circuit:

1. number-conserving Hubbard evolution and the existing CIRIS MPS seam;
2. local Ising/Heisenberg evolution at low and deliberately rising
   entanglement;
3. gauge-link plaquettes within a fixed charge sector;
4. diagonal deterministic and stochastic channels, reported separately from
   coherent unitary simulation;
5. random universal circuits as the negative control.

Sweep qubit/site count, depth/time, noise, sector filling, and MPS bond cap.
Include at least one regime designed to destroy every expected native
advantage.

## Equivalence gate before speed

No timing sample is admissible until both paths agree on the preregistered
outputs: norm/trace, energy, conserved charges, selected one- and two-site
observables, and final-state fidelity or trace-distance proxy where feasible.
Record truncation error and use the same total error budget. Exact and
approximate runs are separate strata.

## Measurement protocol

- identical host/GPU, thread count, precision, and warm/cold policy;
- include end-to-end parse/compile/lowering time and also report steady-state
  kernel time separately;
- median and dispersion over repeated isolated runs;
- peak resident memory, accelerator memory, and bytes transferred;
- native representation size (sector dimension or maximum bond dimension);
- no result caching across semantically distinct samples;
- publish raw samples, commands, commit SHAs, compiler flags, and failures.

The primary outcome is end-to-end wall time at matched error. Secondary
outcomes are kernel time and peak memory. Report the crossover surface rather
than one headline ratio.

## Decision rule

The speed thesis survives only if a preregistered structured family shows a
repeatable advantage over the best matching baseline and the advantage tracks
the predicted smaller representation. It is falsified for a family if the
optimized native implementation cannot beat the best baseline within the same
error budget. Random-circuit losses are expected and must remain visible.

R1 transport and this benchmark are independent gates: R1 proves which claims
may cross roots; this benchmark measures how quickly a licensed local kernel
computes them.
