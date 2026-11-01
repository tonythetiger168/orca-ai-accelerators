# Integration — ORCA CPU／NPU／TV-STB-IPCAM

更新：2026-11-01 15:04（Asia/Taipei）。ETA：未知。
此檔由本工作維護，供中央每小時讀取；不新增排程、不跨聊天發訊。

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

