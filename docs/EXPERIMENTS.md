# EXPERIMENTS.md

Výsledky backtestů. Jeden řádek na běh, vždy stejné sloupce.
Hodnoty se opisují ze souhrnu, který vypíše `scripts/backtest.sh`
(plný výstup zůstává na NASu v `results/`).

Období: **IS** = 2021-01-01 → 2025-01-01, **OOS** = 2025-01-01 → dnes. Fee 0.1 % na stranu.

| Datum | Commit | Strategie | Období | Změna | Obchody | Win % | Zisk % | Profit factor | Max DD % | Závěr |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-20 | 3400421 | TrendPullbackV1 | IS | baseline (první běh) | 2403 | – | -20.04 | 0.87 | 23.49 | horší než nic: poplatky ~240 USDT (0.1 % × 239 894 USDT objemu) > ztráta 200 USDT, takže hrubá hrana ≈ +4 % za 4 roky; trh +2820 %. Vstupy bez hrany a výstupy (ROI 1–3 %) uřezávají trendy. Výchozí bod pro další změny. |
| 2026-10-21 | a9dce99 | TrendPullbackV1 | IS | výstupy: ROI vypnuto, exit při `close_4h < ema_fast_4h` | 660 | 22.6 | 82.28 | 1.95 | 6.65 | **lepší → nechat.** Exit signál +1382 USDT (444×, Ø +6.2 %), stoploss −559 USDT (216×). Poplatky ~67 USDT místo ~240. Pozor: zisk stojí na pár trendových měsících (2021 +563, 2023 +353; 2022 −73, 2024 −21), nejlepší obchod +235 % (AVAX), 22 ztrát v řadě. |

Win % zatím nevyplněno (není v souhrnu SUMMARY METRICS).

Závěr: `lepší` / `stejné` / `horší` → co s tím (nechat / vrátit).
