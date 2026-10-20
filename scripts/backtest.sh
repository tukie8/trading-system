#!/usr/bin/env bash
# Spustí backtest vždy stejným postupem a uloží výstup do results/.
#
# Použití (z kořene repa na NASu):
#   ./scripts/backtest.sh "popis-zmeny"          # in-sample (vývoj)
#   OOS=1 ./scripts/backtest.sh "popis-zmeny"    # out-of-sample (kontrola)
#
# Out-of-sample období se při ladění NEPOUŽÍVÁ. Pouští se jen občas,
# na ověření, že se strategie nepřeladila na minulost.
set -euo pipefail

LABEL="${1:-bez-popisu}"
BOT="${BOT:-spot_swing_01}"

# Pevná období – neměnit bez záznamu v docs/DECISIONS.md
IN_SAMPLE="20210101-20250101"
OUT_OF_SAMPLE="20250101-"
FEE="0.001"   # Binance spot 0.1 % na stranu (Freqtrade ho počítá při vstupu i výstupu)

if [[ "${OOS:-0}" == "1" ]]; then
  TIMERANGE="$OUT_OF_SAMPLE"; PERIOD="OOS"
else
  TIMERANGE="$IN_SAMPLE"; PERIOD="IS"
fi

cd "$(dirname "$0")/.."
mkdir -p "results/$BOT" "bots/$BOT"/{logs,state,tmp}

COMMIT="$(git rev-parse --short HEAD 2>/dev/null || echo unknown)"
DIRTY="$(git status --porcelain 2>/dev/null | grep -q . && echo "+necommitnuto" || true)"
STAMP="$(date -u +%Y%m%d-%H%M)"
SAFE_LABEL="$(echo "$LABEL" | tr ' /' '__')"
OUT="results/$BOT/${STAMP}_${PERIOD}_${SAFE_LABEL}.txt"

{
  echo "# backtest $BOT | $PERIOD $TIMERANGE | fee $FEE | commit $COMMIT$DIRTY | $STAMP UTC"
  echo "# popis: $LABEL"
  echo
  docker compose -f compose/docker-compose.yml run --rm "$BOT" \
    backtesting \
    --config /freqtrade/user_data/config/config.json \
    --timerange "$TIMERANGE" \
    --fee "$FEE" \
    --export trades \
    --breakdown month \
    --cache none
} 2>&1 | tee "$OUT"

echo
echo "Uloženo: $OUT"
echo "Další krok: zapiš souhrnný řádek do docs/EXPERIMENTS.md"
