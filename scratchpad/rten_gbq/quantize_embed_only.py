"""DIAGNOSTIC ONLY -- not a shipping artifact.

The embedding table is TIED: it is both the input embedding (Gather) and the output
projection (lm_head). Quantising it therefore perturbs the logits directly, not just
the token representations. This variant quantises ONLY the Gather side and leaves
lm_head on the original fp16 weight, so the two effects can be told apart:

  * if this variant is equivalent to the baseline, GatherBlockQuantized and the
    4-bit input embedding are not what costs the accuracy -- the lm_head is;
  * if it is not, the input embedding itself is doing the damage.

It is LARGER than the baseline (it keeps the fp16 table and adds a quantised copy),
which is fine: nobody would ship it, it exists to attribute the cost.
"""
import sys, numpy as np, onnx
from onnx import TensorProto, helper

SRC, DST = sys.argv[1], sys.argv[2]
BLOCK, BITS, ZP = 32, 4, 8

model = onnx.load(SRC)
g = model.graph
inits = {i.name: i for i in g.initializer}
W = "model.embed_tokens.weight"
gather = next(n for n in g.node if n.op_type == "Gather" and n.input[0] == W)
w_init = inits[W]
V, D = w_init.dims
NB = D // BLOCK
w = np.frombuffer(w_init.raw_data, dtype=np.float16).reshape(V, D)

qw = np.empty((V, D // 2), dtype=np.uint8)
scales = np.empty((V, NB), dtype=np.float16)
for s0 in range(0, V, 8192):
    s1 = min(s0 + 8192, V)
    blk = w[s0:s1].astype(np.float32).reshape(-1, NB, BLOCK)
    scale = np.maximum(np.abs(blk.min(axis=2)) / ZP, blk.max(axis=2) / (ZP - 1))
    scale[scale == 0] = np.float32(6.0e-8)
    s16 = scale.astype(np.float16); s16[s16 == 0] = np.float16(6.0e-8)
    s = s16.astype(np.float32)
    q = np.clip(np.rint(blk / s[:, :, None]) + ZP, 0, 15).astype(np.uint8).reshape(s1 - s0, D)
    qw[s0:s1] = q[:, 0::2] | (q[:, 1::2] << 4)
    scales[s0:s1] = s16

QW, SC = "model.embed_tokens.qweight_flat", "model.embed_tokens.scales"
for name, arr, dt in [(QW, qw, TensorProto.UINT8), (SC, scales, TensorProto.FLOAT16)]:
    g.initializer.append(helper.make_tensor(name, dt, list(arr.shape), arr.tobytes(), raw=True))

node = helper.make_node("GatherBlockQuantized", [QW, gather.input[1], SC],
                        list(gather.output), name=gather.name, domain="com.microsoft",
                        bits=BITS, block_size=BLOCK, gather_axis=0, quantize_axis=1)
idx = list(g.node).index(gather)
g.node.remove(gather)
g.node.insert(idx, node)   # lm_head's Transpose+MatMul keep the fp16 weight untouched

if not any(o.domain == "com.microsoft" for o in model.opset_import):
    model.opset_import.append(helper.make_opsetid("com.microsoft", 1))
onnx.save(model, DST)
print("saved", DST)
