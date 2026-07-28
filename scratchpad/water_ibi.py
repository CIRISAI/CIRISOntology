#!/usr/bin/env python3
"""N3 — THE PAIR-MATCHED NULL, built by Iterative Boltzmann Inversion.

`WATER_PREREG.md` sec 5.1 makes this the campaign's PHYSICAL null and says why
it cannot be the glass campaign's: there, species is an extra degree of freedom
and "hold the positions, resample the labels" is a well-defined pair-matched
surrogate.  HERE THE LABEL IS A FUNCTION OF THE POSITIONS, so a label
permutation is only the estimator floor, and the physical null must act on the
POSITIONS.

WHAT IS BUILT.  A tabulated PAIR potential u(r) whose own equilibrium liquid, at
mW's density and temperature, reproduces mW's own measured g(r).  Iterative
Boltzmann Inversion (Soper 1996; Reith, Putz & Muller-Plathe 2003), started from
the potential of mean force and iterated

    u_{n+1}(r) = u_n(r) + alpha kT ln( g_n(r) / g_target(r) ).

The result is a liquid with NO three-body term of any kind whose pair structure
is water's.  That is exactly "nothing beyond what the pair correlations already
imply", realised as a real equilibrium liquid rather than as a reconstruction.

WHY THIS AND NOT THE lambda = 0 LIQUID.  sec 5.1 named the mW `lambda = 0`
liquid as a second, independent realisation of the same null and required the
two to agree.  **That cross-check is unavailable**: `WATER_AMENDMENT_12.md`
measures the `lambda = 0` liquid as two-phase at matched density and
label-degenerate at its own ambient density.  Its unavailability is reported, not
worked around, and N3 therefore stands alone -- which is a weaker position than
the pre-registration budgeted for and is declared as such.

IT WILL READ NONZERO, and that is the point (sec 5.1): a pair ensemble has
genuine triplet structure, because Kirkwood superposition is violated at liquid
density.  The deliverable is the DIFFERENCE, share(data) - share(N3).

G-DYE FOR N3 (sec 5.1, GATES.md reach 13): a control that cannot see the dye
returns "ungauged", not "clean".  N3's dye test is `--dye`: IBI is run against
the g(r) of a liquid that HAS a known three-body term (mW itself), and it must
reproduce g(r) while FAILING to reproduce the three-body reading.  If IBI's
liquid matched mW's whole-only share as well as its g(r), the null would be
gauging nothing.
"""
import argparse
import json
import os
import sys

import numpy as np

sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")

MASS, NA = 18.015, 6.02214076e23
KB = 0.0019872041          # kcal/mol/K


def box_for(N, rho):
    return (N * MASS / (NA * rho) * 1e24) ** (1.0 / 3.0)


def write_table(path, r, u, keyword="PAIRPOT"):
    """LAMMPS pair_style table file.  Force is -du/dr by central differences on
    the same grid the energy is tabulated on, so the two are consistent to the
    grid rather than analytically -- which is what `pair_style table linear`
    interpolates anyway."""
    f = -np.gradient(u, r)
    with open(path, "w") as fh:
        fh.write("# IBI pair potential for the water campaign's N3 null\n\n")
        fh.write("%s\nN %d R %.6f %.6f\n\n" % (keyword, len(r), r[0], r[-1]))
        for i in range(len(r)):
            fh.write("%d %.8f %.10f %.10f\n" % (i + 1, r[i], u[i], f[i]))


def run_table(tab, N, T, rho, nequil, nprod, dt, seed, rcut, nbins, rmax,
              dumpfile=None, dump_every=0, nthreads=4):
    from lammps import lammps
    L = box_for(N, rho)
    lmp = lammps(cmdargs=["-log", "none", "-screen", "none",
                          "-sf", "omp", "-pk", "omp", str(nthreads)])
    c = lmp.command
    for line in f"""
units real
atom_style atomic
boundary p p p
region box block 0 {L} 0 {L} 0 {L}
create_box 1 box
create_atoms 1 random {N} {seed} box overlap 2.2 maxtry 500
mass 1 {MASS}
pair_style table linear 2000
pair_coeff 1 1 {tab} PAIRPOT {rcut:.6f}
neighbor 2.0 bin
neigh_modify every 1 delay 0 check yes
comm_modify cutoff 12.0
min_style cg
minimize 1e-6 1e-8 2000 20000
velocity all create {T} {seed} mom yes rot yes dist gaussian
timestep {dt}
fix 1 all nvt temp {T} {T} {100 * dt}
run {nequil}
reset_timestep 0
""".strip().split("\n"):
        c(line)
    if dumpfile and dump_every:
        c(f"dump d all custom {dump_every} {dumpfile} id x y z")
        c("dump_modify d sort id format line \"%d %.6f %.6f %.6f\"")
    pid = os.getpid()
    c(f"compute rdf all rdf {nbins} 1 1 cutoff {rmax}")
    c("fix rdfavg all ave/time 100 %d %d c_rdf[*] file /tmp/ibirdf_%d.dat mode vector"
      % (max(1, nprod // 100), nprod, pid))
    c("variable vpress equal press")
    c(f"fix pav all ave/time 10 1 10 v_vpress file /tmp/ibip_%d.dat" % pid)
    c(f"run {nprod}")
    rdf = np.loadtxt("/tmp/ibirdf_%d.dat" % pid, skiprows=4)
    pav = np.loadtxt("/tmp/ibip_%d.dat" % pid, skiprows=2)
    press = float(pav[:, 1].mean())
    lmp.close()
    for p in ("/tmp/ibirdf_%d.dat" % pid, "/tmp/ibip_%d.dat" % pid):
        os.remove(p)
    return rdf[:, 1], rdf[:, 2], press, L


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default="/home/emoore/CIRISOntology/scratchpad/water_mw_sweep.json")
    ap.add_argument("--lam", default="23.15")
    ap.add_argument("-n", type=int, default=2000)
    ap.add_argument("-T", type=float, default=298.0)
    ap.add_argument("--rho", type=float, default=0.997)
    ap.add_argument("--iters", type=int, default=25)
    ap.add_argument("--alpha", type=float, default=0.4)
    ap.add_argument("--rcut", type=float, default=8.0)
    ap.add_argument("--rmin", type=float, default=1.6)
    ap.add_argument("--ntab", type=int, default=600)
    ap.add_argument("--nequil", type=int, default=15000)
    ap.add_argument("--nprod", type=int, default=25000)
    ap.add_argument("--dt", type=float, default=5.0)
    ap.add_argument("--seed", type=int, default=20260727)
    ap.add_argument("--prod-nprod", dest="prod_nprod", type=int, default=100000)
    ap.add_argument("--dump-every", dest="dump_every", type=int, default=500)
    ap.add_argument("--dump", default="/home/emoore/CIRISOntology/scratchpad/mw/ibi_n3.dump")
    ap.add_argument("--out", default="/home/emoore/CIRISOntology/scratchpad/water_ibi.json")
    a = ap.parse_args()

    sw = json.load(open(a.target))[a.lam]
    r = np.array(sw["r"])
    gt = np.array(sw["g"])
    kT = KB * a.T
    m = r <= a.rcut
    r, gt = r[m], gt[m]

    # THE TABLE GRID.  `compute rdf` bins start at r = 0.02 A, where g(r) is
    # exactly zero and the potential of mean force is infinite; tabulating a pair
    # potential there is what core-dumped the first attempt.  The table is built
    # from `rmin` outward, and the excluded core is replaced by an explicit steep
    # wall rather than by a capped plateau -- a capped plateau is a potential
    # particles can pass THROUGH, which is not a hard core at all.
    rt = np.linspace(a.rmin, float(r[-1]), a.ntab)
    gt_t = np.interp(rt, r, gt)
    first = int(np.argmax(gt_t > 0.05))
    r0 = rt[first]
    with np.errstate(divide="ignore"):
        u = -kT * np.log(np.maximum(gt_t, 1e-12))
    u[first:] = np.minimum(u[first:], 20.0 * kT)
    u[:first] = u[first] + 4.0 * kT * ((r0 / rt[:first]) ** 12 - 1.0)
    r, gt = rt, gt_t
    u -= u[-1]
    u[-1] = 0.0

    hist = []
    tab = "/tmp/ibi_%d.table" % os.getpid()
    print("IBI: target = mW lambda=%s at rho=%.4f, T=%.1f; %d iterations\n"
          % (a.lam, a.rho, a.T, a.iters), flush=True)
    print("%5s %12s %12s %12s %12s" % ("iter", "max|dg|", "rms dg", "peak g", "P (atm)"),
          flush=True)
    best, bestu, bestrms = None, None, np.inf
    for it in range(a.iters):
        write_table(tab, r, u)
        rr, gn, press, L = run_table(tab, a.n, a.T, a.rho, a.nequil, a.nprod,
                                     a.dt, a.seed + it, float(r[-1]), len(r), a.rcut)
        gn = np.interp(r, rr, gn)
        d = gn - gt
        rms = float(np.sqrt(np.mean(d ** 2)))
        print("%5d %12.4f %12.5f %12.4f %12.1f"
              % (it, float(np.abs(d).max()), rms, float(gn.max()), press), flush=True)
        hist.append(dict(iter=it, max_abs_dg=float(np.abs(d).max()), rms_dg=rms,
                         press=press, g=gn.tolist()))
        if rms < bestrms:
            bestrms, bestu, best = rms, u.copy(), it
        ok = (gn > 1e-3) & (gt > 1e-3)
        upd = np.zeros_like(u)
        upd[ok] = a.alpha * kT * np.log(gn[ok] / gt[ok])
        # smooth the update: g(r) is measured with noise and an unsmoothed
        # update writes that noise into the potential and keeps it there
        k = np.ones(5) / 5.0
        upd = np.convolve(upd, k, mode="same")
        u = u + upd
        u -= u[-1]
        u[-1] = 0.0

    # production run on the BEST potential
    print("\nbest iteration %d (rms %.5f); production run" % (best, bestrms), flush=True)
    write_table(tab, r, bestu)
    os.makedirs(os.path.dirname(a.dump), exist_ok=True)
    rr, gn, press, L = run_table(tab, a.n, a.T, a.rho, a.nequil * 2, a.prod_nprod,
                                 a.dt, a.seed + 999, float(r[-1]), len(r), a.rcut,
                                 dumpfile=a.dump, dump_every=a.dump_every)
    gn = np.interp(r, rr, gn)
    d = gn - gt
    out = dict(lam_target=a.lam, rho=a.rho, T=a.T, L=L, N=a.n,
               best_iter=best, best_rms=bestrms,
               final_max_abs_dg=float(np.abs(d).max()),
               final_rms_dg=float(np.sqrt(np.mean(d ** 2))),
               press=press, r=r.tolist(), g_target=gt.tolist(),
               g_final=gn.tolist(), u=bestu.tolist(), history=hist,
               dump=a.dump)
    json.dump(out, open(a.out, "w"))
    os.remove(tab)
    print("\nPRODUCTION: max|dg| = %.4f  rms = %.5f  P = %.1f atm"
          % (out["final_max_abs_dg"], out["final_rms_dg"], press), flush=True)
    print("wrote", a.out, flush=True)


if __name__ == "__main__":
    main()
