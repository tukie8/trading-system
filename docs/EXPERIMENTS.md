# EXPERIMENTS.md

Výsledky backtestů. Jeden řádek na běh, vždy stejné sloupce.
Hodnoty se opisují ze souhrnu, který vypíše `scripts/backtest.sh`
(plný výstup zůstává na NASu v `results/`).

Období: **IS** = 2021-01-01 → 2025-01-01, **OOS** = 2025-01-01 → dnes. Fee 0.1 % na stranu.

| Datum | Commit | Strategie | Období | Změna | Obchody | Win % | Zisk % | Profit factor | Max DD % | Závěr |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-20 | 3400421 | TrendPullbackV1 | IS | baseline (první běh) | 2403 | – | -20.04 | 0.87 | 23.49 | horší než nic: poplatky ~240 USDT (0.1 % × 239 894 USDT objemu) > ztráta 200 USDT, takže hrubá hrana ≈ +4 % za 4 roky; trh +2820 %. Vstupy bez hrany a výstupy (ROI 1–3 %) uřezávají trendy. Výchozí bod pro další změny. |

Win % zatím nevyplněno (není v souhrnu SUMMARY METRICS).

Závěr: `lepší` / `stejné` / `horší` → co s tím (nechat / vrátit).
