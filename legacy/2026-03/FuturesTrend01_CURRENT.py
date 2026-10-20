from freqtrade.strategy import IStrategy, informative
from pandas import DataFrame
from datetime import datetime
from freqtrade.persistence import Trade
import pandas as pd
import talib.abstract as ta

class FuturesTrend01(IStrategy):
    """
    StableTrendPullback - full spec v1
    Entry timeframe: 1h
    Trend timeframe: 4h
    """

    timeframe = "1h"
    can_short = False  # full spec v1 zatím long-only, short přidáme až po validaci edge
    startup_candle_count = 250
    process_only_new_candles = True

    minimal_roi = {
     "0": 0.03,
     "60": 0.02,
     "180": 0.01

}
    stoploss = -0.10

    trailing_stop = True
    trailing_stop_positive = 0.015
    trailing_stop_positive_offset = 0.02
    trailing_only_offset_is_reached = True

    use_custom_stoploss = True

    use_exit_signal = False
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    @informative("4h")
    def populate_indicators_4h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["ema50"] = ta.EMA(dataframe, timeperiod=50)
        dataframe["ema200"] = ta.EMA(dataframe, timeperiod=200)
        dataframe["ema200_slope"] = dataframe["ema200"] - dataframe["ema200"].shift(1)
        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["ema50"] = ta.EMA(dataframe, timeperiod=50)
        dataframe["ema200"] = ta.EMA(dataframe, timeperiod=200)
        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)
        dataframe["atr"] = ta.ATR(dataframe, timeperiod=14)
        dataframe["atr_mean_50"] = dataframe["atr"].rolling(50).mean()
        dataframe["adx"] = ta.ADX(dataframe, timeperiod=14)
        dataframe["volume_mean_20"] = dataframe["volume"].rolling(20).mean()

        dataframe["ema_distance"] = (dataframe["close"] - dataframe["ema200"]) / dataframe["close"]
        dataframe["ema_strength"] = (dataframe["ema50"] - dataframe["ema200"]) / dataframe["close"]

        dataframe["prev_close"] = dataframe["close"].shift(1)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["enter_long"] = 0

        dataframe.loc[
            (
                # 4h trend
                (dataframe["ema50_4h"] > dataframe["ema200_4h"]) &
                (dataframe["close_4h"] > dataframe["ema200_4h"]) &
                (dataframe["ema200_slope_4h"] > 0) &

                # 1h trend
                (dataframe["close"] > dataframe["ema200"]) &
                (dataframe["ema50"] > dataframe["ema200"]) &

                # trend strength
                (dataframe["ema_strength"] > 0.03) &
                (dataframe["ema_distance"] > 0.02) &

                # pullback + reclaim EMA50
                (dataframe["close"] > dataframe["ema50"]) &
                (dataframe["low"] < dataframe["ema50"]) &
                (dataframe["close"] > dataframe["open"]) &  # 🔥 potvrzení odrazu

                # momentum
                (dataframe["rsi"] > 55) &
                (dataframe["close"] > dataframe["high"].shift(1)) &

                # volatility
                (dataframe["atr"] > dataframe["atr_mean_50"]) &

                # ADX
                (dataframe["adx"] > 25) &

                # volume
                (dataframe["volume"] > dataframe["volume_mean_20"]) &

                # safety
                (dataframe["volume"] > 0)
            ),
            "enter_long"
        ] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["exit_long"] = 0
        dataframe["exit_short"] = 0

        return dataframe

    def custom_stoploss(
        self,
        pair: str,
        trade,
        current_time,
        current_rate: float,
        current_profit: float,
        **kwargs
    ) -> float:

        dataframe, _ = self.dp.get_analyzed_dataframe(pair=pair, timeframe=self.timeframe)

        if dataframe is None or dataframe.empty:
            print(f"DEBUG: dataframe None for {pair}")
            return self.stoploss

        last_candle = dataframe.iloc[-1].squeeze()

        atr = last_candle.get("atr", None)
        close_price = last_candle.get("close", None)

        if atr is None or close_price is None or close_price <= 0:
            return self.stoploss

        atr_percent = atr / close_price
        dynamic_sl = atr_percent * 2.0

        # clamp mezi 3% a 8%
        dynamic_sl = max(0.03, min(dynamic_sl, 0.08))

        return -dynamic_sl
