# DECISIONS.md

Jeden řádek na rozhodnutí. Nejnovější nahoře. Formát: `datum | co | proč`.

- 2026-10-21 | `TrendPullbackV1`: `minimal_roi = {"0": 100}`, `use_exit_signal = True`, výstup při `close_4h < ema_fast_4h` s tagem `trend_lost_4h`; stoploss zůstává `-0.05`, vstupy beze změny | Místo pevných ROI cílů držet pozici do ztráty 4h trendu, se zachováním ochranného stoplossu.
- 2026-10-20 | Přesun CI workflow do `.github/workflows/check.yml` | GitHub Actions workflow se standardně načítají z `.github/workflows`.
- 2026-10-20 | Restart projektu (v2): Git repo jako jediný zdroj pravdy, Codex dělá PR, NAS jen `git pull` | Stav byl rozházený v chatech a snapshotech, které si odporovaly; nebylo jasné, co vlastně platí.
- 2026-10-20 | Aktivní jen `spot_swing_01`, ostatní boti spí | Nejdřív jeden stabilní základ, pak další boti.
- 2026-10-20 | Nová startovní strategie `TrendPullbackV1` se 4 podmínkami místo `FuturesTrend01` s ~15 | Při ~15 filtrech zbylo ~40 obchodů a výsledky změn byly převážně náhoda. Začínáme od jádra a filtry přidáváme jen s důvodem.
- 2026-10-20 | Otevřená otázka „rsi > 50 vs > 55 a filtr close > open“ uzavřena přesunem do `legacy/` | V nové strategii je `rsi > 50` a filtr `close > open` není; staré varianty zůstávají v archivu.
- 2026-10-20 | `stoploss = -0.05`, bez trailing stopu a bez custom stoplossu | Méně knoflíků na začátku. ATR stoploss v první verzi nepomohl.
- 2026-10-20 | Nová instalace na NASu v `/mnt/tukieNAS/trading`, stará `/mnt/tukieNAS/trading-system` zůstává jako archiv | Čistý start bez rizika přepsání starého stavu.
- 2026-10-20 | Freqtrade připnutý na `2026.9` | Pevná verze, upgrade jen samostatnou změnou.
- 2026-10-20 | Pevná backtest období: IS 2021-01-01 → 2025-01-01, OOS 2025-01-01 → dnes; fee 0.1 % | Porovnatelné výsledky a čistý out-of-sample test.
- 2026-10-20 | `startup_candle_count = 800` | EMA200 na 4h potřebuje ~800 hodinových svíček; dřívějších 250 bylo málo.
