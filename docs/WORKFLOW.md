# Jak probíhá jedna iterace

Každá změna strategie jde stejnou cestou. Díky tomu jsou výsledky porovnatelné
a nikdo nemusí vzpomínat, „co tam vlastně teď je“.

## Role

| Kdo | Co dělá |
|---|---|
| Nikolas | určuje směr, schvaluje (merguje) PR, spouští backtest na NASu |
| Codex | píše kód, dělá PR (jedna změna na PR), řídí se `AGENTS.md` |
| Claude / ChatGPT | přemýšlení, review PR, rozbor výsledků |

## Smyčka

1. **Hypotéza jednou větou.**
   Např. „Když vyřadím vstupy při nízkém ADX, ubude ztrátových obchodů v bočním trhu.“
2. **Codex udělá PR** s jednou změnou + řádkem v `docs/DECISIONS.md`.
3. **Review** (Claude nebo ChatGPT si přečte diff přímo na GitHubu). Merge.
4. **Backtest na NASu:**
   ```bash
   cd /mnt/tukieNAS/trading
   git pull
   ./scripts/backtest.sh "adx-filtr"
   ```
5. **Zápis výsledku** do `docs/EXPERIMENTS.md` (jeden řádek, vždy stejné sloupce).
6. **Rozhodnutí:** nechat, nebo vrátit (revert PR). Zapsat do `docs/DECISIONS.md`.

## Pravidla, která drží výsledky poctivé

- **Pevné období.** In-sample `2021-01-01 → 2025-01-01` na ladění.
  Out-of-sample `2025-01-01 → dnes` se pouští jen občas (`OOS=1`), na kontrolu.
  Kdo ladí na OOS datech, přestane je mít.
- **Stejné poplatky** pokaždé (0.1 % na stranu, nastaveno ve skriptu).
- **Málo obchodů = žádný závěr.** Pod ~100 obchodů v in-sample je rozdíl mezi
  dvěma běhy často jen náhoda. Raději méně filtrů a víc obchodů.
- **Jedna změna najednou.** Když se změní dvě věci, nevíš, která pomohla.

## Kdy přidat druhého bota

Až `spot_swing_01` projde několika iteracemi a jeho výsledek je stabilní
(podobný na in-sample i out-of-sample). Ne dřív.
