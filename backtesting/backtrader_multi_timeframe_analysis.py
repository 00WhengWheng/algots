import backtrader as bt
import pandas as pd
from ..strategies.multi_timeframe_analysis import MultiTimeframeAnalysis

class MultiTimeframeAnalysisStrategy(bt.Strategy):
    params = (
        ('short_period', 20),
        ('long_period', 50),
        ('timeframes', ["daily", "4h", "1h"]),
        ('printlog', False),
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.short_ma = {tf: self.get_moving_average(self.params.short_period, tf) for tf in self.params.timeframes}
        self.long_ma = {tf: self.get_moving_average(self.params.long_period, tf) for tf in self.params.timeframes}
        self.order = None

    def get_moving_average(self, period, timeframe):
        return bt.indicators.SimpleMovingAverage(self.datas[0], period=period)

    def next(self):
        if self.order:
            return

        signals = {tf: 0 for tf in self.params.timeframes}
        for tf in self.params.timeframes:
            if self.short_ma[tf][0] > self.long_ma[tf][0]:
                signals[tf] = 1
            elif self.short_ma[tf][0] < self.long_ma[tf][0]:
                signals[tf] = -1

        combined_signal = sum(signals.values())

        if not self.position:
            if combined_signal > 0:
                self.order = self.buy()
        else:
            if combined_signal < 0:
                self.order = self.sell()

    def notify_order(self, order):
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, Price: {order.executed.price}')
            elif order.issell():
                self.log(f'SELL EXECUTED, Price: {order.executed.price}')
            self.order = None

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        if self.params.printlog:
            print(f'{dt.isoformat()} {txt}')

    def stop(self):
        self.log(f'Ending Value {self.broker.getvalue()}', dt=self.datas[0].datetime.date(0))

def run_backtest(data: pd.DataFrame, initial_cash: float = 100000.0):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MultiTimeframeAnalysisStrategy)
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