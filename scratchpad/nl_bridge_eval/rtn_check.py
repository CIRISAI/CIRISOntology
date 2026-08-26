#!/usr/bin/env python3
"""Cross-check sim-portability's lead INSIDE my harness, against MY reference.

Simulates RTN 4-bit symmetric block-32 on the matmul tensors of ft_merged and scores
with the SAME constrained-greedy scorer used for every other arm. Everything runs in
torch float32, so the only thing that varies between the two numbers is the quantisation.
"""
import json, os, sys, collections, torch
from transformers import AutoTokenizer, AutoModelForCausalLM
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import importlib.util
spec = importlib.util.spec_from_file_location("ft", f"{HERE}/finetune4.py")
ft = importlib.util.module_from_spec(spec); spec.loader.exec_module(ft)

def rtn_quant_(w, block=32, bits=4):
    """Round-to-nearest, SYMMETRIC, per-block along the input dim. In-place fake-quant."""
    out, inn = w.shape
    pad = (-inn) % block
    x = torch.nn.functional.pad(w, (0, pad)) if pad else w
    x = x.reshape(out, -1, block).float()
    qmax = 2 ** (bits - 1) - 1                       # symmetric: [-8, 7] -> use 7
    scale = x.abs().amax(dim=-1, keepdim=True) / qmax
    scale = torch.where(scale == 0, torch.ones_like(scale), scale)
    q = torch.clamp(torch.round(x / scale), -qmax - 1, qmax)
    deq = (q * scale).reshape(out, -1)[:, :inn]
    w.copy_(deq.to(w.dtype))

def main():
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    tok = AutoTokenizer.from_pretrained(f"{HERE}/ft_merged")
    test = ft.load(f"{HERE}/test_split.jsonl")
    print(f"scoring {len(test)} frozen-test items, torch float32, constrained greedy\n")

    m = AutoModelForCausalLM.from_pretrained(f"{HERE}/ft_merged", dtype=torch.float32).to(dev)
    acc0, rows0 = ft.score(m, tok, test, dev)
    print(f"  REFERENCE  float32, unquantised          = {acc0:.3f}")

    targets = [(n, p) for n, p in m.named_parameters()
               if p.dim() == 2 and any(k in n for k in
               ("q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"))]
    print(f"  quantising {len(targets)} matmul tensors (RTN, symmetric, block 32, 4-bit)")
    with torch.no_grad():
        for _, p in targets: rtn_quant_(p.data)
    acc1, rows1 = ft.score(m, tok, test, dev)
    print(f"  SIMULATED  RTN 4-bit matmuls only        = {acc1:.3f}")

    agree = sum(a["pred"] == b["pred"] for a, b in zip(rows0, rows1)) / len(rows0)
    print(f"  agreement vs float32 reference           = {agree:.3f}")
    print()
    print(f"  measured ONNX q4f16 export (same weights) = 0.576")
    print(f"  measured ONNX fp32   export (same weights)= 0.772")
    print(f"  => simulation minus export = {acc1-0.576:+.3f}")
    for tag, r in (("rtn_sim", rows1), ("fp32_torch", rows0)):
        with open(f"{HERE}/pred4_{tag}.jsonl", "w") as f:
            for x in r: f.write(json.dumps(x) + "\n")
    print("  labels sim:", dict(collections.Counter(x["pred"] for x in rows1)))

if __name__ == "__main__":
    main()
