import pandas as pd
import numpy as np
from .indicators.volatility.average_true_range import average_true_range as atr
from .patterns.candlestick.triangle_pattern import detect_triangle_pattern

class VolumeProfileAnalysis:
    def __init__(self, volume_col='Volume', price_col='Close', time_period=20, num_levels=10, atr_period=14):
        self.volume_col = volume_col
        self.price_col = price_col
        self.time_period = time_period
        self.num_levels = num_levels
        self.atr_period = atr_period
        self.account_balance = 100000  # Initialize as needed
        self.latest_close_price = None
        self.risk_per_trade = 0.02  # 2% risk per trade
        self.required_patterns = ['Triangle']

    def analyze_volume_profile(self, data: pd.DataFrame) -> dict:
        """
        Analyze the volume profile using a more sophisticated approach.
        """
        if self.volume_col not in data.columns or self.price_col not in data.columns:
            raise ValueError(f"Missing required columns: {self.volume_col}, {self.price_col}")

        recent_data = data.tail(self.time_period)
        price_min, price_max = recent_data[self.price_col].min(), recent_data[self.price_col].max()
        price_levels = np.linspace(price_min, price_max, self.num_levels)

        recent_data['Price_Level'] = pd.cut(recent_data[self.price_col], bins=price_levels, labels=False)
        volume_profile = recent_data.groupby('Price_Level')[self.volume_col].sum().reset_index()
        volume_profile['Price'] = price_levels[:-1] + (price_levels[1] - price_levels[0]) / 2
        volume_profile = volume_profile.sort_values('Volume', ascending=False)

        poc = volume_profile.iloc[0]['Price']
        total_volume = volume_profile[self.volume_col].sum()
        cumulative_volume = 0
        value_area_low = value_area_high = poc

        for _, row in volume_profile.iterrows():
            cumulative_volume += row[self.volume_col]
            if cumulative_volume <= total_volume * 0.7:
                value_area_low = min(value_area_low, row['Price'])
                value_area_high = max(value_area_high, row['Price'])
            else:
                break

        return {
            'volume_profile': volume_profile,
            'poc': poc,
            'value_area_low': value_area_low,
            'value_area_high': value_area_high
        }

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Detect patterns and generate signals based on volume profile analysis.
        """
        volume_analysis = self.analyze_volume_profile(data)
        data = atr(data, period=self.atr_period)
        data = detect_triangle_pattern(data, column=self.price_col)

        data['Signal'] = 0
        data['Position_Size'] = 0
        data['Stop_Loss'] = 0
        data['Take_Profit'] = 0

        for i in range(1, len(data)):
            if self._is_buy_signal(data.iloc[i], volume_analysis):
                data.loc[data.index[i], 'Signal'] = 1
            elif self._is_sell_signal(data.iloc[i], volume_analysis):
                data.loc[data.index[i], 'Signal'] = -1

            if data.loc[data.index[i], 'Signal'] != 0:
                data.loc[data.index[i], 'Position_Size'] = self._calculate_position_size(data.iloc[i])
                data.loc[data.index[i], 'Stop_Loss'] = self._calculate_stop_loss(data.iloc[i], 'long' if data.loc[data.index[i], 'Signal'] == 1 else 'short')
                data.loc[data.index[i], 'Take_Profit'] = self._calculate_take_profit(data.iloc[i], 'long' if data.loc[data.index[i], 'Signal'] == 1 else 'short')

        self.latest_close_price = data[self.price_col].iloc[-1]
        return data

    def _is_buy_signal(self, row, volume_analysis):
        return (
            row['Triangle_Pattern'] and
            row[self.price_col] > volume_analysis['poc'] and
            row[self.price_col] < volume_analysis['value_area_high']
        )

    def _is_sell_signal(self, row, volume_analysis):
        return (
            row['Triangle_Pattern'] and
            row[self.price_col] < volume_analysis['poc'] and
            row[self.price_col] > volume_analysis['value_area_low']
        )

    def _calculate_position_size(self, row):
        risk_amount = self.account_balance * self.risk_per_trade
        return np.floor(risk_amount / row[f'ATR_{self.atr_period}'])

    def _calculate_stop_loss(self, row, direction):
        atr = row[f'ATR_{self.atr_period}']
        return row[self.price_col] - 2 * atr if direction == 'long' else row[self.price_col] + 2 * atr

    def _calculate_take_profit(self, row, direction):
        atr = row[f'ATR_{self.atr_period}']
        return row[self.price_col] + 3 * atr if direction == 'long' else row[self.price_col] - 3 * atr

    def check_position_size(self, account_balance, risk_per_trade):
        position_size = self._calculate_position_size({self.price_col: self.latest_close_price, f'ATR_{self.atr_period}': self.latest_close_price * 0.02})
        max_position_size = account_balance * 0.05  # Maximum 5% of account balance
        return position_size <= max_position_size

    def check_daily_drawdown(self, daily_loss, max_drawdown=0.1):
        allowable_loss = max_drawdown * self.account_balance
        return daily_loss <= allowable_loss
