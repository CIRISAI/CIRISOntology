#!/usr/bin/env python3
"""Stream a GlassBench *_models tarball into one compact .npz per temperature.

Disk on this box is at 99%.  The tarball is read SEQUENTIALLY with `tarfile`
in stream mode, each member's .npz decoded in memory, and only the fields this
campaign needs are kept:

    types                      (int8,   Nstruct x N)
    initial_positions          (float32, Nstruct x N x d)
    initial_positions_inherent (float32, Nstruct x N x d)

Everything else in the archive -- the ML model predictions, the propensities,
the coarse-grained structural descriptors -- is discarded here.  Those are the
DYNAMICS side of the benchmark; this campaign asks a purely STATIC question and
must not have a dynamical label anywhere near the estimator.

Peak extra disk: one tarball.  Output: ~27 MB per temperature.
"""
import io
import json
import os
import sys
import tarfile

import numpy as np

WANT = ("types", "initial_positions", "initial_positions_inherent")


def convert(tarpath, outpath, meta_out):
    structs, seen_keys, order = {}, set(), []
    nbad = 0
    with tarfile.open(tarpath, mode="r|gz") as tf:
        for m in tf:
            if not m.isfile() or not m.name.endswith(".npz"):
                continue
            split = "train" if "/train/" in m.name else (
                "test" if "/test/" in m.name else "?")
            base = os.path.basename(m.name)[:-4]
            try:
                idx = int(base.rsplit("_", 1)[1])
            except (ValueError, IndexError):
                nbad += 1
                continue
            buf = io.BytesIO(tf.extractfile(m).read())
            with np.load(buf, allow_pickle=False) as z:
                seen_keys.update(z.files)
                rec = {}
                for k in WANT:
                    if k in z.files:
                        rec[k] = z[k]
                if "initial_positions" not in rec:
                    nbad += 1
                    continue
            key = (split, idx)
            structs[key] = rec
            order.append(key)
            if len(order) % 100 == 0:
                sys.stderr.write(f"  {tarpath}: {len(order)} structures\n")
                sys.stderr.flush()

    order = sorted(set(order))
    N = structs[order[0]]["initial_positions"].shape[0]
    d = structs[order[0]]["initial_positions"].shape[1]
    pos = np.empty((len(order), N, d), dtype=np.float32)
    inh = np.full((len(order), N, d), np.nan, dtype=np.float32)
    typ = np.zeros((len(order), N), dtype=np.int8)
    n_inh = 0
    for i, key in enumerate(order):
        r = structs[key]
        pos[i] = r["initial_positions"]
        typ[i] = r["types"]
        if "initial_positions_inherent" in r:
            inh[i] = r["initial_positions_inherent"]
            n_inh += 1
    split = np.array([k[0] for k in order])
    sid = np.array([k[1] for k in order], dtype=np.int32)

    np.savez_compressed(outpath, positions=pos, inherent=inh, types=typ,
                        split=split, struct_id=sid)
    meta = dict(
        tar=os.path.basename(tarpath), out=os.path.basename(outpath),
        n_structures=len(order), n_particles=int(N), dim=int(d),
        n_with_inherent=n_inh, n_skipped=nbad,
        npz_keys_seen=sorted(seen_keys),
        splits={s: int((split == s).sum()) for s in sorted(set(split.tolist()))},
        type_counts={int(t): int((typ == t).sum()) for t in np.unique(typ)},
        pos_min=[float(x) for x in pos.reshape(-1, d).min(0)],
        pos_max=[float(x) for x in pos.reshape(-1, d).max(0)],
        inh_min=(None if n_inh == 0 else
                 [float(x) for x in np.nanmin(inh.reshape(-1, d), 0)]),
        inh_max=(None if n_inh == 0 else
                 [float(x) for x in np.nanmax(inh.reshape(-1, d), 0)]),
    )
    json.dump(meta, open(meta_out, "w"), indent=1)
    print(json.dumps(meta, indent=1))
    return meta


if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2], sys.argv[3])
