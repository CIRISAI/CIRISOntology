"""Quantise ONLY the embedding table of a working ONNX export, and rewire both of its
consumers to read the quantised form.

Why not adopt a ready-made quantised export: those also use MatMulNBits WITH zero
points on all 197 matmuls, which rten does not implement. Quantising one tensor of a
model that already runs needs only the new GatherBlockQuantized operator, and leaves
every other weight bit-identical to the baseline -- so the payload comparison is a
controlled one, with the embedding as the single variable.

The table is TIED: `Gather` reads it for the token embedding and `Transpose`+`MatMul`
read it for the lm_head. Both are rewired to one shared buffer:

  Gather   -> Reshape(qweight, [V, D/2]) -> GatherBlockQuantized(.., indices, scales)
  MatMul   -> MatMulNBits(hidden, qweight, scales)

That forces SYMMETRIC quantisation: rten's MatMulNBits takes no zero-point input and
dequantises as `(q - 8) * scale`, so the gather must use the same convention. It does,
for free -- the spec's default zero point for uint8 data is 2^(bits-1) = 8, so the
GatherBlockQuantized node is emitted with no zero_points input and agrees exactly.
"""
import sys, numpy as np, onnx
from onnx import TensorProto, helper

SRC, DST = sys.argv[1], sys.argv[2]
BLOCK, BITS = 32, 8
ZP = 1 << (BITS - 1)          # 8, the implicit zero point of both operators
BLOB = BLOCK * BITS // 8      # 16 bytes per block

model = onnx.load(SRC)
g = model.graph
inits = {i.name: i for i in g.initializer}

W = "model.embed_tokens.weight"
gather = next(n for n in g.node if n.op_type == "Gather" and n.input[0] == W)
transpose = next(n for n in g.node if n.op_type == "Transpose" and n.input[0] == W)
matmul = next(n for n in g.node if transpose.output[0] in n.input)
w_init = inits[W]
V, D = w_init.dims
assert D % BLOCK == 0
NB = D // BLOCK
print(f"embedding [{V}, {D}] fp16 = {len(w_init.raw_data)/1e6:.1f} MB, tied to "
      f"'{gather.name}' and '{matmul.name}'")

w = np.frombuffer(w_init.raw_data, dtype=np.float16).reshape(V, D)
qw = np.empty((V, NB, BLOB), dtype=np.uint8)  # BLOB = BLOCK*BITS/8
scales = np.empty((V, NB), dtype=np.float16)

err_num = 0.0
err_den = 0.0
CHUNK = 8192
for start in range(0, V, CHUNK):
    stop = min(start + CHUNK, V)
    blk = w[start:stop].astype(np.float32).reshape(-1, NB, BLOCK)
    # Symmetric with an implicit zero point of 8: representable range is
    # [-8*s, 7*s], so the scale must cover the negative side by 8 and the
    # positive side by 7.
    scale = np.maximum(np.abs(blk.min(axis=2)) / ZP, blk.max(axis=2) / (ZP - 1))
    scale[scale == 0] = np.float32(6.0e-8)
    scale16 = scale.astype(np.float16)
    scale16[scale16 == 0] = np.float16(6.0e-8)
    s = scale16.astype(np.float32)

    q = np.clip(np.rint(blk / s[:, :, None]) + ZP, 0, (1 << BITS) - 1).astype(np.uint8)
    deq = (q.astype(np.float32) - ZP) * s[:, :, None]
    err_num += float(((deq - blk) ** 2).sum())
    err_den += float((blk ** 2).sum())

    qw[start:stop] = q if BITS == 8 else (q[:, :, 0::2] | (q[:, :, 1::2] << 4))
    scales[start:stop] = scale16

print(f"  quantisation error on the table itself: "
      f"relative RMS = {np.sqrt(err_num/err_den):.4%}")

g.initializer.remove(w_init)
QW, SC = "model.embed_tokens.qweight", "model.embed_tokens.scales"
for name, arr, dtype in [(QW, qw, TensorProto.UINT8), (SC, scales, TensorProto.FLOAT16)]:
    g.initializer.append(helper.make_tensor(name, dtype, list(arr.shape),
                                            arr.tobytes(), raw=True))
    print(f"  {name}: {list(arr.shape)} {arr.dtype} {arr.nbytes/1e6:.1f} MB")

# The gather reads the same buffer as a flat [V, D/2] byte matrix.
flat_shape = "model.embed_tokens.qweight_shape"
g.initializer.append(helper.make_tensor(flat_shape, TensorProto.INT64, [2],
                                        np.array([V, D * BITS // 8], dtype=np.int64).tobytes(),
                                        raw=True))
reshaped = "model.embed_tokens.qweight_flat"
nodes = [
    helper.make_node("Reshape", [QW, flat_shape], [reshaped],
                     name="/model/embed_tokens/Reshape"),
    helper.make_node("GatherBlockQuantized", [reshaped, gather.input[1], SC],
                     list(gather.output), name=gather.name, domain="com.microsoft",
                     bits=BITS, block_size=BLOCK, gather_axis=0, quantize_axis=1),
]
idx = list(g.node).index(gather)
g.node.remove(gather)
for k, n in enumerate(nodes):
    g.node.insert(idx + k, n)

# lm_head: Transpose + MatMul -> a single MatMulNBits over the same buffer.
mm = helper.make_node("MatMulNBits", [matmul.input[0], QW, SC], list(matmul.output),
                      name=matmul.name, domain="com.microsoft",
                      K=D, N=V, bits=BITS, block_size=BLOCK, accuracy_level=0)
idx = list(g.node).index(matmul)
g.node.remove(matmul)
g.node.remove(transpose)
g.node.insert(idx - 1, mm)

if not any(o.domain == "com.microsoft" for o in model.opset_import):
    model.opset_import.append(helper.make_opsetid("com.microsoft", 1))

onnx.save(model, DST)
print("saved", DST)
