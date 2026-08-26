#!/usr/bin/env python3
"""adequacy — SECOND independent fMRI cohort. Frozen per fmri_cohort2_prereg.md.

Estimator / null / positive-control are IMPORTED VERBATIM from cohort 1
(fmri_whole_only.py). Only the loader changes: nilearn fetch_development_fmri
(Richardson 2018, movie-watching, independent site) + Schaefer-200 extraction.
"""
import os, sys, json, time
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fmri_whole_only as base   # run_subject, positive_control, mvpr_surrogate, ... verbatim

CACHE = os.path.join(HERE, "cohort2_schaefer200_ts.npz")
B = 2
SEED = 0


def log(m): print(m, flush=True)


def extract_cohort():
    """Fetch development_fmri + Schaefer-200, return list of (T,R) arrays.
    Cached to CACHE so b=3 reruns skip re-extraction."""
    if os.path.exists(CACHE):
        z = np.load(CACHE, allow_pickle=True)
        arrs = [z[k] for k in sorted(z.files, key=lambda s: int(s.split("_")[1]))]
        log(f"  loaded {len(arrs)} cached subject series from {CACHE}")
        return arrs

    from nilearn import datasets
    from nilearn.maskers import NiftiLabelsMasker

    log("  fetching Schaefer-2018 200-region atlas ...")
    atlas = datasets.fetch_atlas_schaefer_2018(n_rois=200, yeo_networks=17,
                                               resolution_mm=2)
    log("  fetching development_fmri (Richardson 2018) — all subjects ...")
    # nilearn caches per-file and resumes; retry around flaky OSF/googleapis timeouts
    dev = None
    for attempt in range(40):
        try:
            dev = datasets.fetch_development_fmri()   # ~155 subjects; resumes cached
            break
        except Exception as e:
            log(f"    fetch attempt {attempt+1} interrupted ({type(e).__name__}); retrying ...")
            time.sleep(5)
    if dev is None:
        raise RuntimeError("development_fmri fetch failed after 40 attempts")
    funcs = dev["func"]; confs = dev["confounds"]
    log(f"  {len(funcs)} subjects fetched")

    masker = NiftiLabelsMasker(
        labels_img=atlas["maps"], standardize="zscore_sample", detrend=True,
        low_pass=0.1, high_pass=0.01, t_r=2.0, verbose=0,
        resampling_target="data")

    arrs = []
    for i, (f, c) in enumerate(zip(funcs, confs)):
        try:
            cf = pd.read_csv(c, sep="\t")
            # match filt_noglobal: drop any global-signal regressor
            drop = [col for col in cf.columns if "global" in col.lower()]
            cf = cf.drop(columns=drop)
            cf = cf.fillna(0.0).values
            ts = masker.fit_transform(f, confounds=cf)   # (T, 200)
        except Exception as e:
            log(f"    subj {i}: FAILED ({e})"); continue
        arrs.append(np.asarray(ts, dtype=float))
        if (i + 1) % 20 == 0:
            log(f"    extracted {i+1}/{len(funcs)}")
    np.savez_compressed(CACHE, **{f"subj_{i}": a for i, a in enumerate(arrs)})
    log(f"  cached {len(arrs)} series to {CACHE}")
    return arrs


def qc(ts):
    """Same quality gates as base.load_subject: T>=60, drop ~0-var regions, R>=30."""
    if ts.ndim != 2 or ts.shape[0] < base.MIN_T:
        return None
    sd = ts.std(axis=0)
    ts = ts[:, sd > 1e-9]
    if ts.shape[1] < 30:
        return None
    return ts


def main():
    t0 = time.time()
    b = int(sys.argv[1]) if len(sys.argv) > 1 else B
    log("=" * 70)
    log(f"adequacy cohort 2 — development_fmri + Schaefer-200 — b={b}, "
        f"M={base.M_TRIPLETS}, n_surr={base.N_SURR}")
    log("=" * 70)
    rng = np.random.default_rng(SEED)

    raw = extract_cohort()
    subs = [s for s in (qc(a) for a in raw) if s is not None]
    log(f"  {len(subs)}/{len(raw)} subjects pass QC (T>=60, R>=30)")

    ties = [base.tie_report(s) for s in subs[:10]]
    log(f"  exact-tie fraction (first 10 subj): median {np.median(ties):.2e}")

    results = []
    for i, ts in enumerate(subs):
        r = base.run_subject(ts, b, base.M_TRIPLETS, base.N_SURR, rng)
        r["T"] = int(ts.shape[0]); r["R"] = int(ts.shape[1])
        results.append(r)
        if (i + 1) % 10 == 0 or i < 3:
            zs = np.array([x["z"] for x in results])
            log(f"  [{i+1:3d}/{len(subs)}] T={r['T']:3d} R={r['R']:3d} "
                f"z={r['z']:+6.2f}  running mean z={zs.mean():+.3f} "
                f"(Zgrp={zs.mean()*np.sqrt(len(zs)):+.2f})")

    z = np.array([x["z"] for x in results])
    n = len(z)
    Zgroup = float(z.mean() * np.sqrt(n))
    phi_med = float(np.median([x["phi_med"] for x in results]))
    out = dict(cohort="development_fmri+Schaefer200", b=b, n=n,
               mean_z=float(z.mean()), median_z=float(np.median(z)),
               max_z=float(z.max()), min_z=float(z.min()), Zgroup=Zgroup,
               phi_median=phi_med, tie_fraction=float(np.median(ties)),
               n_past5=int((z >= 5).sum()), per_subject=results)

    log("\n" + "=" * 70)
    log(f"RESULT cohort 2 (b={b}, n={n})")
    log("=" * 70)
    log(f"  per-subject z: mean {z.mean():+.3f}  median {np.median(z):+.3f}  "
        f"[{z.min():+.2f}, {z.max():+.2f}]  (# past +5: {(z>=5).sum()})")
    log(f"  whole-only fraction phi: median {phi_med:.4f}")
    log(f"  Z_group = mean_z * sqrt(n) = {Zgroup:+.2f}")
    if Zgroup >= 5:
        v = "DETECTION — adequacy kill FIRES on cohort 2"
    elif abs(Zgroup) <= 3:
        v = "CLEAN NULL — mild ABIDE lean does NOT replicate; settles toward floor"
    else:
        v = "INCONCLUSIVE — mild lean reproduces at similar magnitude"
    log(f"  VERDICT (pending valid positive control): {v}")

    op = os.path.join(HERE, f"fmri_cohort2_result_b{b}.json")
    json.dump(out, open(op, "w"), indent=1)
    log(f"  wrote {op}   ({time.time()-t0:.0f}s)")

    # positive control on subject 0 — validates power AND null on THIS cohort
    log("\n  running positive control (validates the run) ...")
    rngc = np.random.default_rng(123)
    pc = base.positive_control([subs[0]], b, rngc)
    json.dump(pc, open(os.path.join(HERE, "fmri_cohort2_poscontrol.json"), "w"), indent=1)
    log(f"  positive control: unplanted z={pc['unplanted_z']:+.2f} "
        f"(must be within +-3), smallest firing f={pc['fire_threshold']}")
    valid = (pc["fire_threshold"] is not None and pc["fire_threshold"] <= 0.3
             and abs(pc["unplanted_z"]) <= 3)
    log(f"  CONTROL VALID: {valid}")
    if not valid:
        log("  *** control INVALID — run is a pipeline failure, do NOT read as null ***")
    return out, pc


if __name__ == "__main__":
    main()
