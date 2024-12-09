import backtrader as bt
import pandas as pd
from src.indicators.volatility import atr
from src.indicators.volume import twap
from src.patterns.trend_patterns import detect_head_and_shoulders
from src.utils.options_data_provider import OptionsDataProvider

class GammaScalpingStrategy(bt.Strategy):
    params = (
        ('atr_period', 14),
        ('risk_per_trade', 0.01),
        ('max_drawdown', 0.1),
        ('account_balance', 100000.0),
    )

    def __init__(self):
        self.atr = atr(self.data.high, self.data.low, self.data.close, self.params.atr_period)
        self.twap = twap(self.data.close, self.data.volume)
        self.head_and_shoulders = detect_head_and_shoulders(self.data.close)
        self.options_data_provider = OptionsDataProvider()

    def next(self):
        # Fetch options data
        options_data = self.options_data_provider.get_options_data(self.data._name, self.data.datetime.date(0), self.data.datetime.date(-1))

        # Implement your gamma scalping logic here using options_data and other indicators
        # Example logic: Buy if close price is above TWAP and head and shoulders pattern is detected
        if self.data.close[0] > self.twap[0] and self.head_and_shoulders[0]:
            if not self.position:
                self.buy(size=1)
        elif self.data.close[0] < self.twap[0]:
            if self.position:
                self.sell(size=1)

def run_backtest(data: pd.DataFrame, initial_cash: float = 100000.0):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(GammaScalpingStrategy)
    cerebro.broker.setcash(initial_cash)
    cerebro.broker.setcommission(commission=0.001)
    cerebro.addsizer(bt.sizers.FixedSize, stake=1)

    data_feed = bt.feeds.PandasData(dataname=data)
    cerebro.adddata(data_feed)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot()

# Example usage
# Assuming `data` is a pandas DataFrame with your historical data
# data = pd.read_csv('your_data.csv', parse_dates=True, index_col='Date')
# run_backtest(data)