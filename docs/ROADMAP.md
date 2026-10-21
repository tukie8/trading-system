# ROADMAP – plán stavby

Jediný plán projektu. Když se něco změní, upravuje se tady (přes PR) a důvod jde do `DECISIONS.md`.

## Cíl a rámec

- **Cíl:** vedlejší příjem a růst kapitálu. První rok je hlavně **učení a stavba systému, který funguje**; zisky jen mírné.
- **Peníze:** 200 USD měsíčně, dokud se systém neuživí sám. Do botů jde jen to, co projde fázemi níže.
- **Čas:** večery. Žádný termín, rozhoduje splnění kritérií, ne kalendář.
- **Styl:** konzervativní i agresivnější boti vedle sebe, ale agresivní až nakonec.

Realita čísel: při 2 400 USD vložených za první rok znamená i velmi dobrých 20 % ročně zhruba 40 USD měsíčně.
Příjem, který je znát, přijde až s větším kapitálem a delším časem. Proto se nejdřív staví spolehlivost, ne výnos.

## Boti – co je co

| Bot | Česky | Riziko | Co dělá |
|---|---|---|---|
| `spot_swing_01` | „swingový“ bot na spotu | střední | nakupuje skutečné coiny v trendu, drží dny až týdny, prodá při ztrátě trendu |
| `dca_core_01` | pravidelné nakupování | nízké | nakupuje pevnou částku v pravidelných intervalech, dlouhodobě drží; nepotřebuje „chytrou“ strategii |
| `futures_trend_01` | futures bot | vysoké | obchoduje kontrakty, umí vydělat i na poklesu (short), může používat páku; chyba stojí nejvíc |

**Pořadí:** `spot_swing_01` → `dca_core_01` → `futures_trend_01`.
Od nejlépe rozpracovaného přes nejjednodušší a nejbezpečnější k nejrizikovějšímu.

## Fáze

Do další fáze se jde **jen po splnění kritérií**. Kritéria se po startu fáze nemění (jinak si je přizpůsobíme výsledku).

### Fáze 0 – Základ ✅
Repo, postup Codex → PR → review → merge, NAS, opakovatelný backtest.

### Fáze 1 – Jeden bot s ověřenou hranou (`spot_swing_01`) ← **teď**
Ladění `TrendPullbackV1` na in-sample (2021–2024), jedna změna na PR.
Na konci **jednorázově** out-of-sample (2025 → dnes).

Kritéria:
- IS: profit factor ≥ 1.5, ≥ 300 obchodů
- OOS: profit factor ≥ 1.3, max drawdown ≤ 20 %, ≥ 100 obchodů
- Žádný jednotlivý obchod netvoří víc než 25 % celkového zisku

Pokud OOS neprojde: zpět do fáze 1 s **novou** myšlenkou, ne s dolaďováním na OOS data.

### Fáze 2 – Robustnost
Ověřit, že výsledek není náhoda:
- parametry ±20 % (EMA, RSI, stoploss) → profit factor stále ≥ 1.2
- žádný kalendářní rok horší než −10 %
- funguje aspoň na 3 z 5 párů a na 2–3 nových párech, které jsme při ladění nepoužili

### Fáze 3 – Papírový provoz (dry-run) na NASu, min. 6 týdnů
- bot běží 24/7 v `dry_run`, notifikace na mobil (Telegram)
- **předem:** upgrade RAM na NASu (dnes ~3 GB volné)
- kritéria: žádné pády, chování odpovídá backtestu za stejné období (počet obchodů, typ výstupů)
- během čekání se paralelně vyvíjí `dca_core_01`

### Fáze 4 – Malý ostrý provoz `spot_swing_01`, min. 3 měsíce
- start s **300 USD** z naspořených měsíčních vkladů
- API klíč jen pro obchodování: **bez výběrů**, omezený na IP NASu
- pojistka: bot se sám zastaví při propadu −20 % od maxima (Freqtrade protection `MaxDrawdown`)
- měsíčně: porovnání ostrých výsledků s backtestem a papírovým provozem

### Fáze 5 – `dca_core_01` (konzervativní vrstva)
Pravidelné nákupy z měsíčních vkladů. Jednoduchá logika, nízké riziko; ostrý start může být dřív než fáze 4, pokud projde papírovým provozem.

### Fáze 6 – `futures_trend_01` (agresivní vrstva)
Až po aspoň 3 měsících ostrého `spot_swing_01` bez porušení pojistek. Stejné fáze 1–4, přísnější limity, páka max. 2×.

### Fáze 7 – Portfolio
Rozdělení měsíčních vkladů mezi boty podle výsledků, společný limit rizika.

## Paralelně (infrastruktura)
- RAM na NASu 8 → 16 GB (před fází 3)
- Notifikace (Telegram), záloha `state/` botů
- Později: ML stroj s RTX 3090, akciová fáze

## Teď nedělat
- Přidávat filtry bez jasné hypotézy
- Testovat na OOS datech během ladění
- Spouštět víc botů najednou před fází 4
- AI/ML nad strategií, dokud nemáme fázi 2
