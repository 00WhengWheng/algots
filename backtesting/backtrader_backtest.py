import backtrader as bt
import pandas as pd

class MyStrategy(bt.Strategy):
    params = (
        ('sma_period', 15),
    )

    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.sma_period)

    def next(self):
        if self.data.close[0] > self.sma[0]:
            if not self.position:
                self.buy(size=1)
        elif self.data.close[0] < self.sma[0]:
            if self.position:
                self.sell(size=1)

def run_backtest(data: pd.DataFrame, initial_cash: float = 100000.0):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MyStrategy)
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