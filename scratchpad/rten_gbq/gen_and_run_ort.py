"""Build single-node GatherBlockQuantized models, run them in ONNX Runtime, and write
the inputs and reference outputs in the flat format `gbq_check` reads.

ONNX Runtime is the reference implementation of this contrib operator, so this is a
comparison against the definition rather than against my reading of the definition.
Cases sweep every knob the spec exposes that RTen can represent.
"""
import itertools, json, os, sys
import numpy as np, onnx
from onnx import TensorProto, helper
import onnxruntime as ort

OUT = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(20260822)


def write_flat(path, arr):
    """dtype tag 0 = int64 source, 1 = float32; see gbq_check/src/main.rs."""
    with open(path, "wb") as f:
        f.write(np.int64(0 if arr.dtype == np.int64 else 1).tobytes())
        f.write(np.int64(arr.ndim).tobytes())
        f.write(np.asarray(arr.shape, dtype=np.int64).tobytes())
        f.write(np.ascontiguousarray(arr).tobytes())


def make_case(name, data_shape, bits, block_size, use_zp, scale_dtype,
              indices_shape, quantize_axis_attr, gather_axis_attr, neg_indices):
    """data_shape is the PACKED shape; the last dim holds 8/bits values per byte."""
    components = 8 // bits
    logical_last = data_shape[-1] * components
    n_blocks = (logical_last + block_size - 1) // block_size

    data = rng.integers(0, 256, size=data_shape, dtype=np.uint8)
    scales_shape = list(data_shape[:-1]) + [n_blocks]
    scales = (rng.random(scales_shape).astype(np.float32) * 0.5 + 0.01).astype(scale_dtype)

    inits = [
        helper.make_tensor("data", TensorProto.UINT8, data_shape, data.tobytes(), raw=True),
        helper.make_tensor("scales",
                           TensorProto.FLOAT if scale_dtype == np.float32 else TensorProto.FLOAT16,
                           scales_shape, scales.tobytes(), raw=True),
    ]
    node_inputs = ["data", "indices", "scales"]
    if use_zp:
        zp_last = (n_blocks + components - 1) // components
        zp_shape = list(data_shape[:-1]) + [zp_last]
        zp = rng.integers(0, 256, size=zp_shape, dtype=np.uint8)
        inits.append(helper.make_tensor("zero_points", TensorProto.UINT8, zp_shape,
                                        zp.tobytes(), raw=True))
        node_inputs.append("zero_points")

    attrs = {"bits": bits, "block_size": block_size}
    if quantize_axis_attr is not None:
        attrs["quantize_axis"] = quantize_axis_attr
    if gather_axis_attr is not None:
        attrs["gather_axis"] = gather_axis_attr

    node = helper.make_node("GatherBlockQuantized", node_inputs, ["output"],
                            domain="com.microsoft", **attrs)
    lo = -data_shape[0] if neg_indices else 0
    indices = rng.integers(lo, data_shape[0], size=indices_shape, dtype=np.int64)

    out_shape = list(indices_shape) + list(data_shape[1:])
    out_shape[-1] *= components
    graph = helper.make_graph(
        [node], name,
        [helper.make_tensor_value_info("indices", TensorProto.INT64, indices_shape)],
        [helper.make_tensor_value_info(
            "output",
            TensorProto.FLOAT if scale_dtype == np.float32 else TensorProto.FLOAT16,
            out_shape)],
        initializer=inits,
    )
    model = helper.make_model(graph, opset_imports=[
        helper.make_opsetid("", 21), helper.make_opsetid("com.microsoft", 1)])
    model.ir_version = 10
    path = os.path.join(OUT, f"{name}.onnx")
    onnx.save(model, path)

    sess = ort.InferenceSession(path, providers=["CPUExecutionProvider"])
    ref = sess.run(None, {"indices": indices})[0]

    write_flat(os.path.join(OUT, f"{name}.indices.bin"), indices)
    np.save(os.path.join(OUT, f"{name}.ref.npy"), ref)
    return dict(name=name, bits=bits, block_size=block_size, use_zp=use_zp,
                scale_dtype=str(np.dtype(scale_dtype)), data_shape=list(data_shape),
                indices_shape=list(indices_shape), neg_indices=neg_indices,
                quantize_axis=quantize_axis_attr, gather_axis=gather_axis_attr,
                out_shape=list(ref.shape))


cases = []
i = 0
for bits, block_size in itertools.product([2, 4, 8], [16, 32, 128]):
    components = 8 // bits
    for scale_dtype in (np.float32, np.float16):
        for use_zp in (True, False):
            # rank-2 data, packed last dim chosen so the logical width is a whole
            # number of blocks plus, in one case, a partial block.
            packed = (block_size * 3) // components
            cases.append(make_case(f"c{i:03d}", (37, packed), bits, block_size, use_zp,
                                   scale_dtype, (5,), None, None, False)); i += 1
    # ragged: logical width is NOT a multiple of block_size, which is where the
    # zero-point row addressing goes wrong if the flat scale index is used.
    packed_ragged = (block_size * 3 + block_size // 2) // components
    cases.append(make_case(f"c{i:03d}", (23, packed_ragged), bits, block_size, True,
                           np.float32, (4,), None, None, False)); i += 1
    # rank 3, explicit axes, 2-D indices, negative indices
    packed = (block_size * 2) // components
    cases.append(make_case(f"c{i:03d}", (19, 3, packed), bits, block_size, True,
                           np.float32, (2, 3), 2, 0, True)); i += 1
    # odd block count -> packed zero-point row is not a whole number of components
    packed_odd = (block_size * 5) // components
    cases.append(make_case(f"c{i:03d}", (11, packed_odd), bits, block_size, True,
                           np.float32, (7,), -1, -2 if False else 0, True)); i += 1

json.dump(cases, open(os.path.join(OUT, "cases.json"), "w"), indent=1)
print(f"generated {len(cases)} cases")
