"""
TrendPullbackV1 – startovní strategie restartu (v2, říjen 2026).

Myšlenka jednou větou:
    Kupuj, když je na 4h jasný uptrend a cena na 1h udělá pullback k EMA50
    a znovu nad ni zavře.

Záměrně jen 4 podmínky. Další filtr se přidává jen s důvodem
(viz AGENTS.md a docs/DECISIONS.md).

Spot, long-only. Entry 1h, trend 4h.
"""

from freqtrade.strategy import IStrategy, informative
from pandas import DataFrame
import talib.abstract as ta


class TrendPullbackV1(IStrategy):
    INTERFACE_VERSION = 3

    # --- PARAMETRY (všechny prahy jen tady) ---------------------------------
    trend_ema_fast = 50      # 4h rychlá EMA
    trend_ema_slow = 200     # 4h pomalá EMA
    pullback_ema = 50        # 1h EMA, ke které čekáme pullback
    rsi_period = 14
    rsi_min = 50             # momentum po odrazu

    minimal_roi = {"0": 100}
    stoploss = -0.05
    trailing_stop = False
    # ------------------------------------------------------------------------

    timeframe = "1h"
    can_short = False
    process_only_new_candles = True
    # 200 EMA na 4h potřebuje ~200 * 4 = 800 hodinových svíček historie.
    startup_candle_count = 800

    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    @informative("4h")
    def populate_indicators_4h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["ema_fast"] = ta.EMA(dataframe, timeperiod=self.trend_ema_fast)
        dataframe["ema_slow"] = ta.EMA(dataframe, timeperiod=self.trend_ema_slow)
        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["ema_pullback"] = ta.EMA(dataframe, timeperiod=self.pullback_ema)
        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=self.rsi_period)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = (
            # 1) 4h uptrend: cena nad pomalou EMA a rychlá nad pomalou
            (dataframe["close_4h"] > dataframe["ema_slow_4h"])
            & (dataframe["ema_fast_4h"] > dataframe["ema_slow_4h"])
            # 2) 1h pullback: svíčka sáhla pod EMA50 a zavřela nad ní
            & (dataframe["low"] < dataframe["ema_pullback"])
            & (dataframe["close"] > dataframe["ema_pullback"])
            # 3) momentum
            & (dataframe["rsi"] > self.rsi_min)
            # 4) bezpečnost: žádné prázdné svíčky
            & (dataframe["volume"] > 0)
        )
        dataframe.loc[conditions, ["enter_long", "enter_tag"]] = (1, "pullback_ema50")
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            dataframe["close_4h"] < dataframe["ema_fast_4h"],
            ["exit_long", "exit_tag"],
        ] = (1, "trend_lost_4h")
        return dataframe
