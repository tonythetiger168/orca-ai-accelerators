# NPU 與三產品 SoC UVM 接入合約

日期：2026-11-01，Asia/Taipei。狀態：design。
本文件配合orca-v63 PR #9的SoC integration/CRV/UVM合約；
不寫中央verification/目錄、不重複實作platform UVM元件。

## Scope與來源

- CTRL_S0只含真實APB crossbar、system registers及ICG；不含NPU。
- CPU/NPU候選commit：
  `c1db39aa2ba58d7be23be66912d9051042369c60`，未合併main。
- 完整candidate filelist共81個RTL source，尚未elaborate完整SoC。
- 不能把CTRL_S0的elaboration或host reference12 tests當NPU UVM/coverage。
- TV/IPCAM為選配AI；STB原表不含NPU，full SKU/config仍待定。

## NPU agent／RAL／memory／scoreboard界面

1. APB使用candidate共用ID/CFG0/CFG1、IRQ_STATUS/ENABLE表頭；
   command staging與CPL_POP/PEEK側效依固定source，不能套舊descriptor CSR map。
2. command transaction保留8-bit completion id＋host generation/reset epoch，
   GEMM/DMA/VEC/NOP、wt、shape/addresses與byte↔64B line轉換證據。
3. 多引擎可不同序完成，scoreboard按ID+generation配對，禁止依發送順序猜配。
   wt fence要確認先前accepted job之結果/可見性，不只看busy counter。
4. memory agent明列有序read response、grant latency與outstanding上界；
   verification memory model不是DDR controller/PHY RTL。
5. NPU在candidate SoC的外部grant/rvalid接0，產品DMA campaign仍BLOCKED；
   不能用TLM接通就宣稱SoC RTL完成。
6. golden tensor取自獨立CPU mathematical model；本repohost GEMM/rescale
   可作primitive reference，不能直接複用DUT MAC/quant RTL結果。
7. format、signedness、tail padding、scale/zero-point、overflow與K=0語意
   需host legality/RTL capability分層；尚未支援的model op不能變成ignore_bins。

## Constrained-random／錯誤campaign草案

|ID|範圍|要求|
|---|---|---|
|N01|GEMM/tail/sign|極值、非整tile、K邊界、正負與獨立逐tensor比對|
|N02|DMA/64B packing|2D stride、alignment、address wrap拒絕、延遲與grant回壓|
|N03|多引擎/完成|CQ滿、completion stall、ID重用、wt與混合GEMM/DMA/VEC|
|N04|reset/drain|busy reset、不同domain phase、舊epoch回應、timeout/取消政策|
|N05|model E2E|固定weights/input/SHA、accuracy、cycles/bytes與CPU fallback|
|N06|mutation|有效MAC計數錯、tail lane不mask、重複completion、忽略wt/回壓|

以上都是待執行計畫；沒有本輪NPU RTL CRV/UVM結果。
需先有可建置backend slice、正確memory adapter與platform UVM工具/scoreboard。
初始seed清單與replay/raw DB沿用總repo合約，不以跑多久取代coverage洞分析。

## 六類coverage與准入

line、FSM state＋arc、toggle兩方向、branch outcomes、
SVA attempts/antecedent/non-vacuous pass/cover witnesses與functional合法bins，
按每產品/config/scope各自100%目標；assertion零失敗。
raw/核准排除/有效分母分開，不排除缺RTL、未實作或工具不支援的能力。
只合併完全相同source/config/checker/tool/coverage-options的raw DB；
Nano/X1/Pro或TV/IPCAM不同profile不得混成一個100%。
本輪所有NPU六類coverage維持NOT_RUN，作者報告及host tests分開存證。
FSM extractor缺少時BLOCKED，不用手工covergroups取代native FSM的state/arc。

## 交付責任與阻塞

integration鎖top/filelist/hierarchy/clock/reset/地址/IRQ/line/frame contracts；
platform實作shared UVM agents、RAL、virtual sequence、independent scoreboard、
QoS/ownership/reset/abort檢查與adapters；NPU owner提供固定source/capability。
主CPU/OS、真DDR/PHY、完整models與full product chains仍BLOCKED，ETA未知。
docs/progress/integration.md分design/RTL/verified/physical回報，
本repo不新增排程，不把stub或model當產品RTL。

