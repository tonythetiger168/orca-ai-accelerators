# Integration — ORCA CPU／NPU／TV-STB-IPCAM

更新：2026-11-01 15:14（Asia/Taipei）。ETA：未知。
此檔由本工作維護，供中央每小時讀取；不新增排程、不跨聊天發訊。

## 2026-11-01 15:14 — SoC slice／CRV-UVM gate更新

- docs/design/soc_uvm_integration_contract.md：
  NPU的APB/64B memory/command/completion-ID與epoch、獨立golden、
  GEMM/DMA/VEC/reset/mutation campaigns及逐config coverage合約。
- NPU未加入CTRL_S0；不把host12 tests或控制面elaboration當NPU UVM通過。
- platform接shared UVM agents/RAL/virtual sequence/scoreboard/adapters，
  本工作不寫中央verification/目錄或重複實作其元件。

|階段|本輪真實狀態|
|---|---|
|design|共用CRV/UVM合約、E0-E5 gates與缺IP責任已交付，產品config未凍結|
|RTL|僅總repo新增有界控制面wrapper；沒有完整TV/STB/IPCAM SoC RTL|
|verified|總repoCTRL_S0：pyslang12.1.0，0 errors/7 warnings，未waive|
|verified|source gate6 tests通過；非DUT功能mutation、非UVM/coverage|
|physical|未做；全產品CPU/DDR/PHY/CDC/OS/media鏈仍BLOCKED|

六類line/FSM state+arc/toggle/branch/SVA/functional各100%是逐產品/config/scope目標。
raw/批准排除/effective分母分列；工具不支援/缺RTL不能排除成100%。
SVA attempts、antecedent、non-vacuous pass與cover witness分開，assertion零失敗。
只合併同source/config/TB/checker/tool/coverage-options之raw DB；
沒有raw DB，所有coverage數值維持NOT_RUN，沒有宣稱100%。

實際命令：
- python tools/elaborate_control_slice.py --candidate-root <pinned source>
  --report <run-dir>/elaboration_report.json：總repo實測exit0。
- python -m unittest discover -s tests/integration -p 'test_*.py' -v：
  設定ORCA_CANDIDATE_ROOT/ORCA_GATE_TEST_WORK後，總repo6 tests exit0。
- 完整診斷與原始gate test log在總repodocs/design/soc_crv/。
- 缺Verilator/Icarus/VCS/Xcelium/UVM環境，simulation與六類coverage未跑。

本輪更新前head：`126b2950dfcc965b807b3dc4190b65bd44a805cd`。
依賴candidate：`c1db39aa2ba58d7be23be66912d9051042369c60`（未合併）。
本次commit以本檔所在commit/PR head識別；不自動合併、不付費。

下一步與ETA：
1. platform依合約建立UVM agent/RAL/獨立scoreboard及directed smoke；ETA未知。
2. 建立支援六類metrics的sim工具/DB adapter及native FSM extraction；ETA未知。
3. 先跑CTRL_S0合法/錯誤/重置CRV與DUT功能mutations，再依hole追加seed；
   未跑不填PASS；ETA未知。
4. TV/STB/IPCAM先凍結完整IP/source/config並接真DMA/frame/security鏈；
   缺dependency維持BLOCKED，不能由stub/TLM關閉；ETA未知。

以下15:04表格矩陣紀錄保留；本輪建構與驗證狀態以上方更新為準。

## 本次實際交付

- 對TV#33與IPCAM#31逐項列current/required/gap/update/acceptance/evidence。
- STB表沒有NPU，維持optional/off，不把主CPU或graphics角色轉給NPU。
- 核實Kestrel16GOPS、Falcon3.072TOPS及X1候選峰值（均假設頻率）。
- 分開host primitive、importer/compiler/runtime/driver、模型E2E與physical。
- 舊CSR草案不直接當現有APB driver ABI；沿用總repo合約審查。

## 狀態與真實檢查

|階段|狀態|
|---|---|
|design|矩陣/責任/驗收及SKU決策已寫入draft；需求未凍結|
|RTL|本工作本輪未改RTL；現有候選不能當production完成|
|verified|96列/40候選覆蓋、4檔hash、5峰值算術；host12 tests通過|
|physical|未合成/STA/CDC-RDC/PHY/板級/PPA驗收|

- Python3.14.8 host GEMM/rescale：12 tests，exit0；
  包含4635個Fraction精確rounding比較點，非4635個模型/RTL測試。
- ORCA總repo的audit_integration_matrix.py：exit0；
  檢查三表/JSON一致、完整六欄、96個唯一membership與未知ETA/未凍結狀態。
- 本輪未重跑CPU PR #1、其他IP的RTL/coverage/formal/mutation或模型accuracy。
- 5個dense peak計算的頻率為假設，沒有測得NPU效能或PPA。

## 分支、提交與來源

- repo：tonythetiger168/orca-ai-accelerators
- branch：codex/edge-npu-soc-design-2026-10-26
- draft PR：[設計更新](https://github.com/tonythetiger168/orca-ai-accelerators/pull/1)
- 更新前head：`4d694d8fb38382f4b767611207c1151dc0263bb1`
- 本次提交SHA以本檔所在commit／PR head識別；避免自引用。
- main基線：`8059f10d6f1f54e3afbe676f71a71ba998172ade`
- CPU/NPU候選PR #1：
  `c1db39aa2ba58d7be23be66912d9051042369c60`（未合併）。
- main/本工作head無AGENTS/CLAUDE；已讀CONTRIBUTING與總計畫。
- 表格來源hash與固定ORCA blob在總repo docs/design/iptable/。
- 外部IP能力依共享表/JSON，repository claims未由本輪重跑確認。

## 阻塞與下一步

1. G1：SKU的codec/model/fps/容量/頻率/功耗/OS與角色需求未凍結；ETA未知。
2. 主CPU：ZEN++是候選，application OS與DMA/cache/BSP未驗收；
   8051/ICP只作控制，OH1不作graphics GPU；ETA未知。
3. 記憶體：候選SoC NPU外部grant/rvalid接0；實際DDR/PHY、QoS、
   firewall、cache ownership與abort/drain尚未驗收；ETA未知。
4. AI：先決定backend與64B packing，再接獨立RTL scoreboard與模型E2E；
   importer/compiler/runtime/driver與固定模型資料仍缺；ETA未知。
5. 各IP owner按矩陣補固定commit、介面與raw test證據。
   本工作只修本repo設計文件，不單方面修改其他owner合約或路徑。
6. 保留main、draft狀態；不自動合併、不付費。

中央下一次每小時巡檢應比較source hash／PR head／review／test結果，
有實際進展再更新對應階段；本檔不冒稱持續執行或已完成產品驗收。


