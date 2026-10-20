# STRATEGY_SPEC.md

## Strategy Name

StableTrendPullback

## Strategy Type

Multi-timeframe trend pullback system

## Purpose

Stable, low-risk trading strategy focused on capturing pullbacks within
strong trends on volatile altcoins.

## Timeframes

Entry timeframe: 1h Trend timeframe: 4h

## Trading Universe

SOL/USDT\
AVAX/USDT\
LINK/USDT\
INJ/USDT\
NEAR/USDT

Excluded: BTC/USDT\
ETH/USDT

## Indicators

Trend: EMA50, EMA200

Trend strength: EMA50 - EMA200

Momentum: RSI (14), condition RSI \> 55

Volatility: ATR (14), filter ATR \> ATR mean (50)

Trend strength: ADX (14), condition ADX \> 25

Volume: Volume \> rolling mean (20)

## Entry Logic

All conditions must be met:

4h trend: close_4h \> EMA200_4h\
EMA200 slope \> 0

1h trend: close \> EMA200\
EMA50 \> EMA200

Trend strength: EMA strength \> 1% of price

Pullback: previous close \< EMA50\
current close \> EMA50

Momentum: RSI \> 55

Volatility: ATR \> ATR mean

Trend strength: ADX \> 25

Volume: Volume \> mean

## Exit Logic

ROI: 2.7%\
Stoploss: -2.6%

Trailing: positive = 0.008\
offset = 0.015

## Expected Behavior

-   high winrate
-   small profits
-   volatility dependent

## Weaknesses

-   large stoploss losses
-   regime sensitivity

## Future Improvements

-   ATR position sizing
-   volatility ranking
-   dynamic stoploss
