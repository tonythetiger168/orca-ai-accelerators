# 依三產品IP表收斂的CPU／NPU／SKU整合

日期：2026-11-01，Asia/Taipei。狀態：design，需求未凍結。
責任總矩陣在orca-v63設計PR #9，docs/design/iptable/integration_matrix.md。
共享表：TV#33與IPCAM#31有ORCA選配；STB31列沒有NPU。
STB可選AI是另立需求，不從TV/IPCAM表自動繼承。

## current → required → gap → update → acceptance → evidence

### TV#33 — Optional AI inference

- current：Kestrel/Falcon舊候選；ORCA PR #1另有X1 Nano/X1/Pro backend。
- required：若選AI需凍結模型/精度/latency/bandwidth/power；
  AI-SR仍是功能決策，不能假設現有NPU已實現。
- gap：model importer/compiler/tiler、runtime/driver、frame/tensor adapter，
  模型RTL E2E與actual DDR/OS均未驗收。
- update：把AI放在可關閉best-effort client，不阻塞display deadline；
  舊CSR表暫不作driver ABI，先審現有APB共用表頭與backend重用。
- acceptance：固定模型/校正資料/SHA與品質門檻，
  CPU→quant→RTL，再測decoder/PQ/display/CPU並行；納入所有搬移與fallback。
- evidence：ORCA固定來源與host測試在iptable evidence；不是TV產品PASS。
- 狀態：design草案；RTL候選；verified只到host primitives；physical未知。
- ETA：未知，等待模型/平台/G1；不承諾TOPS或frame rate。

### IPCAM#31 — Optional AI inference

- current：同一edge候選；camera主pipeline不能由NPU取代。
- required：若選偵測/分類需模型、解析度/ROI、推論rate及privacy政策待定。
- gap：前處理色彩/resize/normalize、量化/後處理、sensor/ISP/encoder鏈，
  accuracy/cycles/bytes與DDR QoS未建立端到端證據。
- update：以完成frame ownership/fence後才給AI讀取；
  timeout可丟過期AI job，不能繞過privacy mask或阻塞主碼流。
- acceptance：sensor→ISP→preprocess→AI→postprocess＋主副碼流、
  JPEG、network/storage並行，測精度、buffer lifetime、延遲與錯誤恢復。
- evidence：shared表IPCAM#31；ORCA SoC外部DMA grant仍接0；
  12個host reference測試本輪重跑，不代表camera/model驗收。
- 狀態：design草案；RTL候選；verified只到host primitives；physical未知。
- ETA：未知；1080p30是舊總計畫目標，沒有凍結每frame都跑AI。

### STB — NPU未列入原表

- current：STB表沒有ORCA AI項，主CPU及graphics/compositor仍列gap。
- required：傳統STB不要求NPU；若新增智慧功能，先立模型/成本與OS需求。
- gap：不可用NPU或ICP/8051/OH1填主CPU/GPU欄。
- update：STB NPU=optional/off；保持不依賴AI的decode/display驗收路徑。
- acceptance：AI關閉時完整STB路徑；若選AI，再做同樣模型與QoS驗收。
- evidence：共享STB表31列及unfilled architecture requirements。
- 狀態：design選型待定；不宣稱有STB NPU產品；ETA未知。

## 峰值與有效性能口徑

dense peak = MAC/cycle × issue rate × Hz × 2；
下表issue rate假設1，頻率是假設值，未經synthesis/STA。
dense peak不乘利用率；GEMM達成吞吐與模型E2E另欄記錄。

|候選|MAC/cycle|假設頻率|理論dense上限|本輪驗收|
|---|---|---|---|---|
|Kestrel|8|1GHz|16GOPS = 0.016TOPS|無RTL/模型重跑|
|Falcon source|1024|1.5GHz|3.072TOPS|無第二array的證據|
|X1-Nano PR候選|16|1GHz|32GOPS|作者RTL報告未重跑|
|X1 PR候選|256|1GHz|512GOPS|作者RTL報告未重跑|
|X1-Pro PR候選|2048|1GHz|4.096TOPS|作者RTL報告未重跑|

Kestrel的「1TOPS」不是上述8MAC配置可達的理論值。
Falcon註解寫dual array不等於實際source有兩組；不使用4TOPS claim作驗收。
各配置以source/參數/工具與有效MAC計數核實，不能用busy counter代替。
稀疏、FP16/BF16/FP8能力需個別source/測試，不以命名推導。
首代沒有HBM、chiplet或cloud訓練需求。

## 軟體與主CPU分工矩陣

|層/角色|current|required/gap|update與acceptance|
|---|---|---|---|
|application CPU|ZEN++候選；OS未驗|MMU/privilege/cache/IRQ與BSP|獨立ISA→OS→DMA/並行gate|
|ICP/AON/8051|控制候選|mailbox/IRQ/power/隔離|只管sensor/standby/housekeeping|
|GPU/compositor|無已驗收方案|UI/display stack選型|OH1不填graphics GPU|
|importer|文件描述|固定opset/shape/quant/模型來源|逐op legality與拒絕unsupported|
|tiler/compiler|文件/計畫|layout/64B packing/排程|command dump與逐tensor golden|
|host reference|GEMM/rescale已測|不是完整模型或device模型|本輪12 tests，4635 rounding點|
|runtime/HAL|草案|CAP/ABI/fence/cache/error|mock→RTL co-sim，含reset/abort|
|Linux driver|無已交付target驗收|DMA API/IRQ/client隔離/suspend|kernel build＋target stress|
|model/SDK|未固定weights/data|accuracy門檻與完整pipeline|CPU→quant→RTL→target E2E|

PR #1的APB表頭為ID/CFG0/CFG1與IRQ_STATUS/ENABLE；
command staging、64B line與8-bit completion id不同於舊128B descriptor草案。
需host adapter、packing、ID lifecycle與range checks，禁止binary直接轉型。
目前SoC外部DMA grant/rvalid接0，driver或host reference不能使它完成。
本輪只新增可審查的整合矩陣及證據，沒有修改另一工作分支的RTL。

## 驗收與每小時追蹤

本repo的docs/progress/integration.md提供中央管理讀取：
source hashes、main/PR/head、design/RTL/verified/physical、真實測試、
阻塞、下一步與ETA。中央每小時追蹤；本工作不另建排程或跨聊天發訊。
有新source/review/test才能改對應狀態；無法確定ETA就寫未知。

