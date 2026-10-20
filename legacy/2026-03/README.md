# Archiv první verze projektu (březen 2026)

Jen ke čtení. Nic odsud se nespouští a needituje.

| Soubor | Co to je |
|---|---|
| `FuturesTrend01_CURRENT.py` | poslední stav strategie v souboru (`rsi > 55`, `close > open`, ATR custom stoploss) |
| `FuturesTrend01_ROLLBACK_BASELINE_2026-03-27.py` | snapshot „rollback baseline“ (`rsi > 50`, bez `close > open`, stále s custom stoplossem) |
| `spot_config_ROLLBACK_BASELINE_2026-03-27.json` | spot config, na kterém se ladilo |
| `STRATEGY_SPEC.md` | původní specifikace StableTrendPullback |
| `RESEARCH_LOG.md` | původní výzkumný log |

Pozor: dokument `TRADING_IMPLEMENTATION_STATUS_v4` popisoval jako „živý stav“
ještě třetí variantu (`stoploss = -0.05`, bez custom stoplossu), která v žádném
z těchto souborů není. Právě tahle nejednoznačnost byla jeden z důvodů restartu.

Shrnutí poznatků je v [`docs/LEARNINGS.md`](../../docs/LEARNINGS.md).
