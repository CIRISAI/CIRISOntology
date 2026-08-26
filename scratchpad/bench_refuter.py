import sys, numpy as np
sys.path.insert(0,'.'); import bench_experiment as E, bench_detector as D
import cupy as cp
rng = np.random.default_rng(20260724); cp.random.seed(20260724)
rt = E.build_runtime(64)
# f=1 data
raw = E.run_f(rt, 64, 0.10, 1.0, 4000, 1e-3, rng)
bA,_,_=E.binarize_median(raw['A']); bB,_,_=E.binarize_median(raw['B']); bC,_,_=E.binarize_median(raw['Cc'])
bits=np.stack([bA,bB,bC],1)
r_true = D.joint_detector(bits, n_surr=60, rng=rng)
print(f"f=1 TRUE align : C3={r_true['c3_obs']:.4f} z={r_true['z']:.1f}")
# shuffle C across trials (destroys a,b,c trial alignment; preserves marginals)
zs=[]
for s in range(5):
    perm = np.random.default_rng(1000+s).permutation(len(bC))
    bits_s = np.stack([bA,bB,bC[perm]],1)
    rs = D.joint_detector(bits_s, n_surr=60, rng=rng)
    zs.append(rs['z']); 
    print(f"   shuffle-C #{s}: C3={rs['c3_obs']:.4f} z={rs['z']:.1f}  pair max|corr|={D.pair_meter(bits_s)[0]:.4f}")
print(f"shuffle-C mean z = {np.mean(zs):.2f} (must be at floor, |z|<3)")
# also shuffle ALL three independently at f=1 (full destruction)
bits_a = np.stack([bA[np.random.default_rng(1).permutation(len(bA))],
                   bB[np.random.default_rng(2).permutation(len(bB))],
                   bC[np.random.default_rng(3).permutation(len(bC))]],1)
ra=D.joint_detector(bits_a,n_surr=60,rng=rng)
print(f"shuffle-ALL    : C3={ra['c3_obs']:.4f} z={ra['z']:.1f}")
