# CPU arithmetic reference 驗證 — 2026-11-01

時間：2026-11-01 05:09（Asia/Taipei），Python3.14.8。
狀態：host primitive verified；RTL／模型／OS／physical未驗證。

repo根目錄重現：

```text
python -m unittest discover -s tools/reference -p 'test_*.py' -v
```

本輪在獨立工作目錄work/followup_2026_11_01/reference執行同一份程式。
實際命令exit code：0。
12個test methods通過；其中4635個Fraction比較是同一test內的迴圈，
不是4635個獨立模型／RTL測試。
已知答案覆蓋signed endpoints、M2/N3/K5、bias只加一次、
per-channel scaling、zero-point、ties-to-even、飽和與非法shape/範圍。
沒有借用RTL結果當golden，沒有重跑CPU PR #1的測試。

```text
Ran 12 tests in 0.006s

OK
```

這不是模型accuracy、NPU效能、target CPU或DMA整合報告。
主體reference無計時與device存取；不產生現有backend的命令。
詳見tools/reference/README.md與總repo的2026-11-01跟進文件。

完整原始輸出見 reference_2026-11-01.log（未換行改寫）。
