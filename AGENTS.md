# AGENTS.md – pravidla pro Codex a další AI agenty

Tento soubor čte každý agent, který v repu pracuje. Komunikuj s uživatelem česky.

## O projektu

- Freqtrade boti pro Binance, běží v Dockeru na TrueNAS (`/mnt/tukieNAS/trading`).
- Aktivní je jen `bots/spot_swing_01` se strategií `TrendPullbackV1` (spot, long-only, 1h + 4h).
- `bots/futures_trend_01` a `bots/dca_core_01` zatím spí. Nic do nich nepřidávej, dokud to uživatel neřekne.
- Pevná verze Freqtrade je v `compose/docker-compose.yml` (image tag). Neměň ji v rámci jiné změny.

## Tvrdá pravidla (nikdy neporušit)

1. **Žádné live obchodování.** `dry_run` musí zůstat `true` ve všech configech. Nikdy nepřidávej kód, který zadává reálné objednávky mimo Freqtrade.
2. **Žádné klíče v repu.** API klíče, hesla a JWT secrets patří jen do git-ignorovaných souborů (`compose/.env`, `*.secrets.json`). Pokud nějaký klíč najdeš v kódu nebo historii, upozorni uživatele, ať ho zneplatní (rotace).
3. **Na `legacy/` nesahej.** Je to archiv, slouží jen ke čtení.

## Jak dělat změny

- **Jedna změna = jeden PR.** Jedna hypotéza, jedna úprava. Ne „a ještě jsem přidal…“.
- **Parametry na jednom místě.** Všechny prahy strategie (RSI, délky EMA, stoploss, ROI) jsou atributy na začátku třídy strategie v bloku `# --- PARAMETRY ---`. Nepiš čísla natvrdo do podmínek.
- **Zapiš proč.** Každý PR, který mění logiku nebo parametr, přidá jeden řádek do `docs/DECISIONS.md` (datum, co, proč).
- **Nový filtr jen s důvodem.** Do strategie nepřidávej podmínku, u které neumíš jednou větou říct, jaký problém řeší.
- **Nová verze strategie = nový soubor.** Velká změna logiky znamená `TrendPullbackV2.py` vedle V1, ne přepsání V1. Malé ladění parametrů se dělá ve stávajícím souboru.

## Správnost (vždy)

- Signály počítej jen z uzavřených svíček. Nepoužívej `shift(-1)` ani nic, co se dívá do budoucnosti.
- Informativní timeframe (4h) přidávej přes dekorátor `@informative`, ten řeší zarovnání bez lookahead biasu.
- Časy jsou v UTC.

## Ověření před PR

V sandboxu většinou nemáš data ani Docker. Minimum:

```bash
python -m py_compile bots/spot_swing_01/strategies/*.py
python -m json.tool bots/spot_swing_01/config/config.json > /dev/null
```

Pokud máš nainstalovaný Freqtrade:

```bash
freqtrade list-strategies -c bots/spot_swing_01/config/config.json \
  --strategy-path bots/spot_swing_01/strategies
```

Backtesty se spouští na NASu přes `scripts/backtest.sh`, ne v sandboxu. Výsledky nevymýšlej: když jsi backtest nespustil, napiš to.

## Kde co je

- `docs/ROADMAP.md` – plán po fázích a kritéria pro postup (čti, než navrhneš větší změnu)
- `docs/WORKFLOW.md` – jak probíhá jedna iterace
- `docs/DECISIONS.md` – historie rozhodnutí
- `docs/EXPERIMENTS.md` – výsledky backtestů
- `docs/LEARNINGS.md` – poznatky z první verze projektu
