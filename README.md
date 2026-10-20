# trading-system

Portfolio krypto trading botů nad [Freqtrade](https://www.freqtrade.io/) a Binance.
Běží v Dockeru na domácím TrueNAS serveru. Restart projektu z října 2026 (v2).

> **Stav:** raná fáze stavby. Všechno běží jen v `dry_run`. Žádné live obchodování.

## Hlavní pravidlo

**Co není v tomhle repu, neexistuje.** Strategie, configy, rozhodnutí i výsledky
testů žijí tady. Chat (Claude, ChatGPT) je místo na přemýšlení, ne úložiště stavu.
Na NASu se kód needituje, jen se stahuje (`git pull`).

## Struktura

```text
trading-system/
├── AGENTS.md              pravidla pro Codex / AI agenty (čti jako první)
├── bots/
│   ├── spot_swing_01/     JEDINÝ aktivní bot (spot, long-only)
│   │   ├── config/        config.json (bez klíčů)
│   │   └── strategies/    TrendPullbackV1.py
│   ├── futures_trend_01/  spí – přijde na řadu později
│   └── dca_core_01/       spí – přijde na řadu později
├── compose/
│   └── docker-compose.yml
├── scripts/               stažení dat, backtest (vždy stejný postup)
├── docs/
│   ├── WORKFLOW.md        jak probíhá jedna iterace
│   ├── DECISIONS.md       co se změnilo a proč (1 řádek na změnu)
│   ├── EXPERIMENTS.md     výsledky backtestů ve stejném formátu
│   ├── LEARNINGS.md       co víme z první verze projektu (březen 2026)
│   └── SETUP_NAS.md       jak repo nasadit na TrueNAS
└── legacy/2026-03/        archiv původních strategií a configů (jen ke čtení)
```

Adresáře `logs/`, `state/`, `tmp/`, `shared/market_data/`, `results/` a všechny
`.env` / `*.secrets.json` soubory jsou v `.gitignore`. Vznikají až na serveru.

## Jak se pracuje

Viz [`docs/WORKFLOW.md`](docs/WORKFLOW.md). Ve zkratce:

1. hypotéza jednou větou
2. Codex udělá malý PR s **jednou** změnou
3. review (Claude / ChatGPT), merge
4. na NASu `git pull` + `scripts/backtest.sh`
5. výsledek do `docs/EXPERIMENTS.md`, rozhodnutí do `docs/DECISIONS.md`

## Rychlý start na NASu

```bash
cd /mnt/tukieNAS/trading
cp .env.example compose/.env        # případně upravit
./scripts/download_data.sh          # jednorázově, stáhne historii
./scripts/backtest.sh "baseline"    # první backtest
```

Podrobně v [`docs/SETUP_NAS.md`](docs/SETUP_NAS.md).
