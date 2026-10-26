# Edge NPU 收斂與實測改善計畫

日期：2026-10-26（Asia/Taipei）。狀態：設計立項，未宣稱 RTL、PPA 或量產驗收完成。
本計畫涵蓋 TV／STB／IPCAM 共用平台。實作前重讀最新 main、AGENTS.md／CLAUDE.md、相關 PR 與驗證報告；來源衝突以具體 RTL、較新報告及可重現結果判定。不得把 VIP、行為 PHY、命名或 coverage 百分比等同完整協定或產品成熟度。

## 來源治理
與orca-v63/accelerators存在重疊。先逐檔diff/sha，提出唯一source-of-truth與版本鎖定方案，不複製後各自修改。
## 核心缺口
預設Kestrel的8 MAC lanes若每lane每cycle一MAC，以2 operations/MAC、1GHz計算上限16GOPS；檔頭1TOPS不得當成量測結果。各配置列MAC數、pipeline issue、clock假設、dense/sparse口徑、利用率與外部記憶體成本。
交付 docs/design/edge_npu_architecture.md：GEMM/conv/depthwise、activation、pooling、rescale/quantization、tensor layout、SRAM banking、DMA、scheduler/context、模型前後處理。
列出ONNX/TFLite importer/compiler/runtime/driver現況；先選小型分類/偵測模型做CPU golden→quantized golden→RTL端到端，記錄accuracy/cycles/帶寬/峰值與有效運算。
首代目標為可驗證edge配置；不帶入HBM/chiplet/cloud訓練需求。PPA須合成與STA後才能承諾。

## 共通交付與驗收
- 設計交付：block diagram、模組責任、介面／CSR、資料格式、clock/reset/power、吞吐／頻寬估算、錯誤／abort／recovery、安全邊界、依賴及驗證矩陣。
- 依序進行參考模型、RTL、獨立 scoreboard、CRV、SVA、coverage（保留 raw 數據與逐條 waiver）、適用控制形式驗證與 mutation、系統端到端測試。
- 效能以實測 cycles、配置與工具版本記錄；假設頻率與估算 PPA 必須標明，合成／STA／板級驗證未做不得宣稱完成。
- 每次更新 docs/PROGRESS_TV_STB_IPCAM.md：台北時間、commit、完成／待驗收／阻塞、測試命令與結果、下一步。無結果不得填 PASS。
- 設計工作使用 codex/ 分支與 draft PR；不自動合併，不新增付費服務。跨 repo 介面變更須列出所有 consumer 與相容性。
