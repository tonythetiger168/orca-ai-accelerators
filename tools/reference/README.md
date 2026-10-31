# Edge NPU CPU arithmetic reference

狀態：可執行host reference，非target runtime/compiler/driver或RTL模型。
只用Python3標準函式庫；本輪環境為Python3.14.8。

從repo根目錄執行：

```text
python -m unittest discover -s tools/reference -p 'test_*.py' -v
```

- gemm_int8：signed INT8矩陣，B以[K,N] row-major表示，輸出INT32。
- bias為每output channel的INT32，只在GEMM加入一次。
- rescale_int32：一列accumulator，scale可per-tensor或per-channel。
- multiplier為signed INT32、shift為0..31，product以INT64範圍檢查。
- ties-to-even使用整數除法，與Fraction的精確round獨立交叉核對。
- output zero-point先加再clamp；ReLU下界為quantized zero而非固定0。
- 輸入須為Python list／整數；不接受bool、浮點、空shape或超界數字。

輸出超INT32時拋ValueError；沒有模擬DUT中間wrap或飽和。
input zero-point只支援0；不是ONNX/TFLite所有quant算子的等價實作。
沒有conv/depthwise/pooling、64B packing、bus protocol、計時或電源模型。
本工具輸出不可直接解讀成PR #1的npu_tile_cmd_t；
需先完成G1的backend/packing/語意adapter審查。
不以wall-clock Python時間換算NPU效能。
