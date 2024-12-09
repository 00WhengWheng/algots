import backtrader as bt
import pandas as pd

class KeltnerChannelStrategy(bt.Strategy):
    params = (
        ('atr_period', 14),
        ('multiplier', 2.0),
        ('printlog', False),
    )

    def __init__(self):
        self.atr = bt.indicators.AverageTrueRange(self.data, period=self.params.atr_period)
        self.midline = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.atr_period)
        self.upper_channel = self.midline + self.params.multiplier * self.atr
        self.lower_channel = self.midline - self.params.multiplier * self.atr

    def next(self):
        if self.data.close > self.upper_channel:  # Price crosses above upper channel
            if not self.position:
                self.buy()
        elif self.data.close < self.lower_channel:  # Price crosses below lower channel
            if self.position:
                self.sell()

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        if self.params.printlog:
            print(f'{dt.isoformat()} {txt}')

    def stop(self):
        self.log(f'(ATR Period {self.params.atr_period}) (Multiplier {self.params.multiplier}) Ending Value {self.broker.getvalue()}', dt=self.datas[0].datetime.date(0))

def run_backtest(data: pd.DataFrame, initial_cash: float = 100000.0):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(KeltnerChannelStrategy)
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