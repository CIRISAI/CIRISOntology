Adds `com.microsoft.GatherBlockQuantized` behind the existing `contrib` feature.

### Why

LLM exports that quantize their embedding table emit this operator instead of `Gather`, and without it the model does not load at all. The embedding is usually the single largest tensor in a small LLM, so it is frequently the difference between a runnable export and a shippable one — for Qwen3-0.6B the table is 151,936 x 1024, which is **311 MB of a 570 MB f16 export**. Quantizing just that tensor and running it through this operator takes the same model to **346 MB**, a 39% reduction, with no other change to the graph.

### What it does

Gathers rows from a block-quantized table and dequantizes **only the rows it gathered**, rather than dequantizing the table. That is the point of the operator: the table is far larger than the slice any one step needs.

Scope, and what is deliberately not supported:

- `data` must be `uint8`, with the `bits` attribute (2, 4 or 8) saying how many logical values each byte holds. Models whose `data` is a true `int4`/`uint4` tensor are **rejected rather than misread**, since RTen has no 4-bit tensor type.
- With and without `zero_points`. When absent, the spec's default of `2^(bits-1)` is used, which is also what `MatMulNBits` assumes — so a model that shares one quantized buffer between a tied `lm_head` and its embedding gets a consistent result from both operators for free.
- As in ONNX Runtime, `gather_axis` must be 0 and `quantize_axis` must be the last dimension for `uint8` data. Those two restrictions are what keep the index arithmetic simple.
- Output is `f32` even where the model declares `float16`, consistent with RTen converting f16 to f32 at load.

Parallelized over gathered rows, which is safe for RTen's determinism guarantee: each output row is a pure function of the inputs, so the result does not depend on the thread count. Verified at 1, 2 and 8 threads.

### Verification

**Against ONNX Runtime 1.29**, which is the reference implementation of this contrib operator — so this checks the code against the definition rather than against my reading of the definition. 63 single-node models, 76,560 output elements, sweeping `bits` {2,4,8} x `block_size` {16,32,128} x with/without `zero_points` x f32/f16 scales x rank 2 and 3 x ragged block counts (row width not a whole number of blocks) x negative and 2-D indices.

- f32 scales: **bit-exact**. Both runtimes evaluate `(v - zp) * scale` in f32, so there is no reason to accept less.
- f16 scales: **`float16(rten) == ort` exactly**. ORT rounds that same f32 result to f16 on the way out; RTen keeps f32. One rounding, no tolerance.

That suite was mutation-tested rather than trusted. Five deliberate bugs, all caught, with counts matching the case design: nibble-order swap caught by 21 cases (exactly the `bits=4` ones); zero point addressed by the flat scale index — the mistake ONNX Runtime's own source comments warn about — caught by 21; default zero point 0 instead of `2^(bits-1)` caught by 18 (exactly the no-zero-point cases); block index off-by-one caught by all 63; missing negative-index wraparound caught by 18 (exactly the negative-index cases).

**In-crate tests** (`cargo test --features contrib gather::contrib`): 5 tests covering a reference implementation that dequantizes the whole table and then gathers — the opposite order to the implementation, so agreement is a real check; a worked example with hand-computed values; error cases; consistency between a gathered row and the fully dequantized table; and rejection of non-`uint8` data. Full suite `cargo test --features contrib -p rten` passes 511/511. `cargo fmt` clean, `cargo clippy --features contrib` clean. Builds for `wasm32-unknown-unknown`.

**End to end**: Qwen3-0.6B with its embedding quantized to 4-bit blocks of 32 loads and runs at 22.5 ms/token, against 23.8 ms/token for the 570 MB f16 baseline on the same machine.
