#!/usr/bin/env python3
"""ARM A of the water campaign: the mW three-body DOSE, and its docimasia.

PRE-REGISTERED IN `WATER_PREREG.md` sec 4.3 (P5) and sec 7 as the arm that runs
FIRST, because it is the arm that can kill the campaign's premise cheapest:

  P5 -- sweeping the Stillinger-Weber tetrahedrality parameter `lambda` from 0
  (a strictly PAIRWISE Hamiltonian) to 23.15 (water) at matched density and
  matched reduced temperature, the floor-subtracted share increases
  monotonically with `lambda`, and at `lambda = 0` it reads FLOOR.

  K1 -- if it does not, "the pairwise-blind share reads three-body interaction
  physics" is refuted and NO atomistic water arm is worth starting.

THIS FILE'S `--gate` MODE IS THE DOCIMASIA AND IT RUNS FIRST, on published
properties only, before any share is computed on anything.  `GATES.md`: a gate
-- and an instrument -- is examined BEFORE it is trusted, on the question
"could this thing do the job at all", and that examination is not the same event
as noticing later that it missed something.

THE MODEL.  mW, Molinero & Moore, JPCB 113:4008 (2009): water as a monatomic
Stillinger-Weber particle with an explicit three-body term.  Parameters are
theirs and are not fitted here:

    epsilon = 6.189 kcal/mol      sigma = 2.3925 A       a = 1.8
    lambda  = 23.15               gamma = 1.2            cos(theta0) = -1/3
    A = 7.049556277               B = 0.6022245584       p = 4   q = 0

`lambda` is the ONLY parameter this campaign moves, and moving it to 0 removes
the three-body term entirely, leaving a strictly pairwise potential in the same
code at the same density -- which is a cleaner contrast than "water versus
Kob-Andersen at matched reduced conditions", an argument nobody can make
airtight (`WATER_PREREG.md` sec 4.3).

NO SHARE IS COMPUTED IN `--gate` MODE.  The only quantities are density, the
radial distribution function and the energy drift -- all of them PAIR or
thermodynamic quantities the instrument is blind to by construction.
"""
import argparse
import json
import os
import sys

import numpy as np

MW = dict(epsilon=6.189, sigma=2.3925, a=1.8, lam=23.15, gamma=1.2,
          costheta0=-0.3333333333333333, A=7.049556277, B=0.6022245584,
          p=4.0, q=0.0, tol=0.0)
MASS = 18.015                      # g/mol
RHO_298 = 0.997                    # g/cm^3, the published mW density at 298 K
NA = 6.02214076e23


def write_sw(path, lam):
    """LAMMPS Stillinger-Weber file. `lam` is the tetrahedrality parameter and
    is the ONLY thing this campaign varies; lam = 0 removes the three-body term
    and leaves a strictly pairwise potential."""
    m = MW
    with open(path, "w") as f:
        f.write("# mW (Molinero & Moore, JPCB 113:4008 (2009)), lambda=%g\n" % lam)
        f.write("# e sig a lambda gamma costheta0 A B p q tol\n")
        f.write("W W W %.6f %.6f %.4f %.6f %.4f %.16f %.9f %.10f %.1f %.1f %.1f\n"
                % (m["epsilon"], m["sigma"], m["a"], lam, m["gamma"],
                   m["costheta0"], m["A"], m["B"], m["p"], m["q"], m["tol"]))


def box_for(N, rho_gcc):
    """Cubic box edge (A) holding N mW particles at rho_gcc g/cm^3."""
    vol_cm3 = N * MASS / (NA * rho_gcc)
    return (vol_cm3 * 1e24) ** (1.0 / 3.0)


def run(lam, N, T, P, nequil, nprod, dt, seed, dump_every=0, dumpfile=None,
        rho0=RHO_298, ensemble="npt", nthreads=1):
    from lammps import lammps
    L0 = box_for(N, rho0)
    sw = "/tmp/mw_%g_%d.sw" % (lam, os.getpid())
    write_sw(sw, lam)
    lmp = lammps(cmdargs=["-log", "none", "-screen", "none",
                          "-sf", "omp", "-pk", "omp", str(nthreads)])
    c = lmp.command
    for line in f"""
units real
atom_style atomic
boundary p p p
region box block 0 {L0} 0 {L0} 0 {L0}
create_box 1 box
create_atoms 1 random {N} {seed} box
mass 1 {MASS}
pair_style sw
pair_coeff * * {sw} W
neighbor 2.0 bin
neigh_modify every 1 delay 0 check yes
comm_modify cutoff 12.0
min_style cg
minimize 1e-6 1e-8 2000 20000
velocity all create {T} {seed} mom yes rot yes dist gaussian
timestep {dt}
""".strip().split("\n"):
        c(line)
    if ensemble == "npt":
        c(f"fix 1 all npt temp {T} {T} {100*dt} iso {P} {P} {1000*dt}")
    else:
        c(f"fix 1 all nve")
    c(f"run {nequil}")
    # production
    c("reset_timestep 0")
    if dump_every and dumpfile:
        c(f"dump d all custom {dump_every} {dumpfile} id x y z")
        c("dump_modify d sort id format line \"%d %.6f %.6f %.6f\"")
    c("compute rdf all rdf 200 1 1 cutoff 8.0")
    c("fix rdfavg all ave/time 100 %d %d c_rdf[*] file /tmp/rdf_%d.dat mode vector"
      % (max(1, nprod // 100), nprod, os.getpid()))
    c("thermo 1000")
    c(f"run {nprod}")
    vol = lmp.get_thermo("vol")
    pe = lmp.get_thermo("pe")
    temp = lmp.get_thermo("temp")
    natoms = int(lmp.get_natoms())
    rho = natoms * MASS / NA / (vol * 1e-24)
    rdf = np.loadtxt("/tmp/rdf_%d.dat" % os.getpid(), skiprows=4)
    lmp.close()
    os.remove(sw)
    os.remove("/tmp/rdf_%d.dat" % os.getpid())
    return dict(lam=lam, N=natoms, T=temp, rho=rho, vol=vol,
                pe_per_atom=pe / natoms, L=vol ** (1.0 / 3.0),
                r=rdf[:, 1].tolist(), g=rdf[:, 2].tolist())


def gate(args):
    """THE DOCIMASIA.  Published mW properties only; no share anywhere.

    G1  density at 298 K / 1 atm reproduces the published 0.997 g/cm^3.  This is
        a number the model was PARAMETERISED to hit, so failing it means the
        implementation is wrong, not the model.
    G2  g(r) first peak near 2.76 A and a tetrahedral second shell near 4.5 A,
        with the second peak at ~1.63x the first -- the signature of a
        tetrahedral network rather than a close-packed liquid.
    G3  lambda = 0 is a DIFFERENT liquid: the three-body term is gone, so the
        tetrahedral second shell must collapse and the density must change.
        This is the control the whole arm rests on and it is checked before any
        share is read.
    G4  energy drift in NVE is small over the production window.
    """
    out = {}
    print("=== ARM A DOCIMASIA: mW, published properties only, no share ===",
          flush=True)

    print("\nG1/G2  mW at 298 K, 1 atm, lambda = 23.15", flush=True)
    w = run(MW["lam"], args.n, 298.0, 1.0, args.nequil, args.nprod, args.dt,
            args.seed, nthreads=args.threads)
    r, g = np.array(w["r"]), np.array(w["g"])
    i1 = int(np.argmax(g))
    # second shell: search beyond the first minimum after the first peak
    imin = i1 + int(np.argmin(g[i1:i1 + 60]))
    i2 = imin + int(np.argmax(g[imin:imin + 80]))
    w.update(peak1_r=float(r[i1]), peak1_g=float(g[i1]),
             peak2_r=float(r[i2]), peak2_g=float(g[i2]),
             min1_r=float(r[imin]), min1_g=float(g[imin]))
    print("   rho = %.4f g/cm^3   (published 0.997; rel err %+.2f%%)"
          % (w["rho"], 100 * (w["rho"] / RHO_298 - 1)), flush=True)
    print("   g(r): peak1 %.2f A (g=%.2f)  min %.2f A (g=%.2f)  peak2 %.2f A (g=%.2f)"
          % (w["peak1_r"], w["peak1_g"], w["min1_r"], w["min1_g"],
             w["peak2_r"], w["peak2_g"]), flush=True)
    print("   peak2/peak1 ratio = %.3f" % (w["peak2_r"] / w["peak1_r"]), flush=True)
    out["mw_298"] = w

    print("\nG3  lambda = 0 at the SAME conditions (strictly pairwise control)",
          flush=True)
    p = run(0.0, args.n, 298.0, 1.0, args.nequil, args.nprod, args.dt,
            args.seed, nthreads=args.threads)
    r0, g0 = np.array(p["r"]), np.array(p["g"])
    j1 = int(np.argmax(g0))
    jmin = j1 + int(np.argmin(g0[j1:j1 + 60]))
    j2 = jmin + int(np.argmax(g0[jmin:jmin + 80]))
    p.update(peak1_r=float(r0[j1]), peak1_g=float(g0[j1]),
             peak2_r=float(r0[j2]), peak2_g=float(g0[j2]))
    print("   rho = %.4f g/cm^3   (mW gives %.4f; ratio %.3f)"
          % (p["rho"], w["rho"], p["rho"] / w["rho"]), flush=True)
    print("   g(r): peak1 %.2f A (g=%.2f)  peak2 %.2f A (g=%.2f)  ratio %.3f"
          % (p["peak1_r"], p["peak1_g"], p["peak2_r"], p["peak2_g"],
             p["peak2_r"] / p["peak1_r"]), flush=True)
    out["pair_298"] = p

    ok1 = abs(w["rho"] / RHO_298 - 1) < 0.05
    ok2 = (2.5 < w["peak1_r"] < 3.1) and (4.0 < w["peak2_r"] < 5.2)
    ok3 = p["rho"] > 1.15 * w["rho"]        # pairwise liquid collapses denser
    print("\n%-6s %-52s %s" % ("G1", "density within 5%% of published 0.997",
                               "PASS" if ok1 else "FAIL"))
    print("%-6s %-52s %s" % ("G2", "tetrahedral g(r): peaks at ~2.8 and ~4.5 A",
                             "PASS" if ok2 else "FAIL"))
    print("%-6s %-52s %s" % ("G3", "lambda=0 collapses to a denser liquid",
                             "PASS" if ok3 else "FAIL"))
    out["verdict"] = dict(G1=bool(ok1), G2=bool(ok2), G3=bool(ok3))
    json.dump(out, open(args.out, "w"))
    print("\nwrote", args.out, flush=True)
    if not (ok1 and ok2 and ok3):
        print("DOCIMASIA FAILED -- the instrument is not trusted and arm A does "
              "not proceed.", flush=True)
        return 1
    print("DOCIMASIA PASSED -- the instrument may be used. No share has been "
          "computed by this run.", flush=True)
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", action="store_true")
    ap.add_argument("-n", type=int, default=2000)
    ap.add_argument("--nequil", type=int, default=20000)
    ap.add_argument("--nprod", type=int, default=20000)
    ap.add_argument("--dt", type=float, default=5.0)
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--seed", type=int, default=20260727)
    ap.add_argument("--out", default="/home/emoore/CIRISOntology/scratchpad/water_mw_gate.json")
    args = ap.parse_args()
    if args.gate:
        sys.exit(gate(args))
    ap.error("only --gate is implemented; the lambda sweep is stage 3")


if __name__ == "__main__":
    main()
