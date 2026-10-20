# Poznatky z první verze projektu (březen 2026)

Shrnutí toho, co víme. Původní soubory jsou v `legacy/2026-03/`.

## Infrastruktura (funguje, bereme dál)

- TrueNAS SCALE, ZFS pool `tukieNAS`, projekt v `/mnt/tukieNAS/trading-system`.
  Cesty `/mnt/tank/...` jsou staré a neplatné.
- Model „jeden bot = jeden kontejner“ fungoval: všichni tři boti nabootovali,
  config prošel validací, strategie se načetla (milník 2026-03-20).
- Varování `Could not chown /freqtrade/user_data` při read-only mountech je neškodné.

## Data

- Binance **futures** mají v našem workflow historii jen cca 2025–2026.
- **Spot** data jsou od roku 2020, proto se strategie vyvíjí na spotu
  a futures slouží až k pozdější validaci.

## Strategie (FuturesTrend01 / StableTrendPullback)

- Trend pullback: 4h trend filtr + 1h návrat nad EMA50, long-only.
- Strategie zůstala ve všech testovaných variantách **ztrátová**.
- Hlavní problém nebyl exit ani infrastruktura, ale **kvalita vstupu**
  a citlivost na slabé trendy.
- `ema_strength` 0.02 / 0.03 / 0.05: vyšší hodnota zlepšila kvalitu obchodů,
  ale drasticky snížila jejich počet. 0.03 vypadalo jako kompromis.
- `rsi > 55` místo `> 50`: obchody klesly na ~40, drawdown klesl, výsledek se zhoršil.
- ATR custom stoploss (2× ATR, omezený na 3–8 %): bez zlepšení.
- Přidání objemového filtru: méně obchodů, kvalitnější vstupy (podle původního logu).
- Víc párů: víc obchodů, smíšené výsledky; multi-asset dává smysl.

## Co z toho plyne pro v2

- Při ~15 podmínkách zbylo málo obchodů a efekt každé změny byl převážně šum.
  Proto v2 začíná od jádra (4 podmínky) a filtry přidává po jednom s měřením.
- Stav projektu musí být na jednom místě (Git), ne ve snapshotech z chatu.
