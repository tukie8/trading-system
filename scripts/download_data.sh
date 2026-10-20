#!/usr/bin/env bash
# Stáhne historická data (1h + 4h) pro páry z configu do shared/market_data.
# Spouštět z kořene repa na NASu:  ./scripts/download_data.sh
# Opakované spuštění data jen doplní o nové svíčky.
set -euo pipefail

BOT="${BOT:-spot_swing_01}"
SINCE="${SINCE:-20200101}"

cd "$(dirname "$0")/.."
mkdir -p shared/market_data "results/$BOT" "bots/$BOT"/{logs,state,tmp}

docker compose -f compose/docker-compose.yml run --rm "$BOT" \
  download-data \
  --config /freqtrade/user_data/config/config.json \
  --timeframes 1h 4h \
  --timerange "${SINCE}-"
