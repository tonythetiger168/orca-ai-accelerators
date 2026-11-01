# NPU／SoC 結構探測跟進

日期：2026-11-01 15:24（Asia/Taipei）。狀態：design／產品BLOCKED。
總repoPR #9已進一步探測含真實CPU/NPU instances的固定candidate。

- source：c1db39aa2ba58d7be23be66912d9051042369c60。
- 結構配置：NCT=1、NCO=1、NAI=1；不是TV/STB/IPCAM的凍結SKU。
- 81個RTL units＋2個includes逐blob核對；baseline為11 errors/366 warnings。
- 隔離宣告順序提案及移除兩個未例化舊unit後：0 errors/360 warnings。
- 兩模式2123個instance paths/definitions完全相同；raw hierarchy hash可重現。
- compatibility提案未改CPU PR或main，沒有simulation/formal equivalence/CPU回歸。
- CLI在baseline回2、compat回4，產品gate持續BLOCKED，沒有把0 errors當PASS。

NPU外部grant/rvalid在candidate SoC仍接0，CPU NoC/cache/memory與DDR路徑也不完整。
因此NPU模型E2E、DMA流量、OS、六類coverage與physical仍NOT_RUN。
不能把2123個module instances或host golden通過當成系統資料路徑完成。
NPU UVM agents/RAL/scoreboard依現有合約由platform實作，本輪不複製其工作。

詳細source lock、raw diagnostics、原/overlay fingerprints與可審查patch：
orca-v63的docs/design/soc_crv/structural_followup.md及integration/proposals/。
繼續以CTRL_S0作已elaborate的局部建構基準；full product依賴與ETA未知。

