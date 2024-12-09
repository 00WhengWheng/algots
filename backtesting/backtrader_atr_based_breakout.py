import backtrader as bt
import pandas as pd

class ATRBasedBreakoutStrategy(bt.Strategy):
    params = (
        ('atr_period', 14),
        ('atr_multiplier', 2),
        ('use_stop_loss', True),
    )

    def __init__(self):
        self.atr = bt.indicators.AverageTrueRange(self.data, period=self.params.atr_period)
        self.upper_band = bt.indicators.Highest(self.data.high, period=self.params.atr_period) + self.atr * self.params.atr_multiplier
        self.lower_band = bt.indicators.Lowest(self.data.low, period=self.params.atr_period) - self.atr * self.params.atr_multiplier
        self.stop_loss = None

    def next(self):
        if not self.position:
            if self.data.close[0] > self.upper_band[0]:
                self.buy()
                if self.params.use_stop_loss:
                    self.stop_loss = self.data.close[0] - self.atr[0] * self.params.atr_multiplier
            elif self.data.close[0] < self.lower_band[0]:
                self.sell()
                if self.params.use_stop_loss:
                    self.stop_loss = self.data.close[0] + self.atr[0] * self.params.atr_multiplier
        else:
            if self.params.use_stop_loss:
                if self.position.size > 0 and self.data.low[0] < self.stop_loss:
                    self.sell()
                elif self.position.size < 0 and self.data.high[0] > self.stop_loss:
                    self.buy()

def run_backtest(data: pd.DataFrame, initial_cash: float = 100000.0):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(ATRBasedBreakoutStrategy)
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