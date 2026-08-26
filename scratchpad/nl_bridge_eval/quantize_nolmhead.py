import onnx, os, sys
from onnxruntime.quantization.matmul_nbits_quantizer import MatMulNBitsQuantizer, RTNWeightOnlyQuantConfig
src, dst = 'onnx_fp32/model.onnx', 'onnx_q4f16'
os.makedirs(dst, exist_ok=True)
m = onnx.load(src, load_external_data=True)
# symmetric, block 32 -> matches rten's documented MatMulNBits requirement
# block 32, symmetric, accuracy_level 0 -> exactly rten's documented MatMulNBits
# requirement (symmetric only, accuracy_level=0)
q = MatMulNBitsQuantizer(m, bits=4, block_size=32, is_symmetric=True, nodes_to_exclude=['/lm_head/MatMul'],
                         accuracy_level=0, algo_config=RTNWeightOnlyQuantConfig())
q.process()
onnx.save(q.model.model, f'{dst}/model_q4.onnx', save_as_external_data=True,
          all_tensors_to_one_file=True, location='model_q4.onnx_data')
print('q4 saved')
from onnxruntime.transformers.float16 import convert_float_to_float16
m2 = onnx.load(f'{dst}/model_q4.onnx', load_external_data=True)
m2 = convert_float_to_float16(m2, keep_io_types=True, disable_shape_infer=True)
onnx.save(m2, f'{dst}/model_q4f16.onnx', save_as_external_data=True,
          all_tensors_to_one_file=True, location='model_q4f16.onnx_data')
print('q4f16 saved')
