"""Tokenise real prompts from the NL-bridge test split and write model inputs.

Real application traffic, not synthetic text: the question is whether the smaller
payload behaves the same on the inputs it will actually see. Prefill only -- the whole
prompt in one pass with an empty KV cache -- so every prompt token goes through the
embedding and we get a full [1, S, 151936] logit tensor per prompt to compare, rather
than one row.
"""
import json, os, sys
import numpy as np
from transformers import AutoTokenizer

OUT = os.path.dirname(os.path.abspath(__file__))
TOK = "/home/emoore/.cache/huggingface/hub/models--Qwen--Qwen3-0.6B/snapshots/c1899de289a04d12100db370d81485cdf75e47ca"
SPLIT = "/home/emoore/CIRISOntology/scratchpad/nl_bridge_eval/test_split.jsonl"
N_PROMPTS = int(sys.argv[1]) if len(sys.argv) > 1 else 24
MAX_TOK = int(sys.argv[2]) if len(sys.argv) > 2 else 256

tok = AutoTokenizer.from_pretrained(TOK)
rows = [json.loads(l) for l in open(SPLIT)]
print(f"{len(rows)} rows in the split; using {N_PROMPTS}")


def write_flat(path, arr, dtype_tag):
    with open(path, "wb") as f:
        f.write(np.int64(dtype_tag).tobytes())
        f.write(np.int64(arr.ndim).tobytes())
        f.write(np.asarray(arr.shape, dtype=np.int64).tobytes())
        f.write(np.ascontiguousarray(arr).tobytes())


# Empty KV cache, shared by every prompt: [1, 8, 0, 128].
empty = np.zeros((1, 8, 0, 128), dtype=np.float32)
write_flat(os.path.join(OUT, "past_empty.bin"), empty, 1)

manifest = []
step = max(1, len(rows) // N_PROMPTS)
for k, row in enumerate(rows[::step][:N_PROMPTS]):
    text = row["before"]
    ids = tok(text, return_tensors="np")["input_ids"][:, :MAX_TOK].astype(np.int64)
    S = ids.shape[1]
    write_flat(os.path.join(OUT, f"p{k:02d}.input_ids.bin"), ids, 0)
    write_flat(os.path.join(OUT, f"p{k:02d}.attention_mask.bin"),
               np.ones((1, S), dtype=np.int64), 0)
    write_flat(os.path.join(OUT, f"p{k:02d}.position_ids.bin"),
               np.arange(S, dtype=np.int64)[None, :], 0)
    manifest.append(dict(name=f"p{k:02d}", id=row["id"], tokens=int(S)))

json.dump(manifest, open(os.path.join(OUT, "prompts.json"), "w"), indent=1)
print(f"wrote {len(manifest)} prompts, {sum(m['tokens'] for m in manifest)} tokens total, "
      f"lengths {min(m['tokens'] for m in manifest)}-{max(m['tokens'] for m in manifest)}")
