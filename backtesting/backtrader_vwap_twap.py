import backtrader as bt
import pandas as pd
import numpy as np
from ..strategies.vwap_twap import VWAPTWAP

class VWAPTWAPStrategy(bt.Strategy):
    params = (
        ('vwap_period', 20),
        ('twap_period', 20),
        ('rsi_period', 14),
        ('atr_period', 14),
        ('risk_per_trade', 0.01),
        ('printlog', False),
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.datahigh = self.datas[0].high
        self.datalow = self.datas[0].low
        self.datavolume = self.datas[0].volume

        self.vwap = bt.indicators.VolumeWeightedAveragePrice(self.datas[0], period=self.params.vwap_period)
        self.twap = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.twap_period)
        self.rsi = bt.indicators.RelativeStrengthIndex(self.datas[0], period=self.params.rsi_period)
        self.atr = bt.indicators.AverageTrueRange(self.datas[0], period=self.params.atr_period)

        self.order = None

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.dataclose[0] > self.vwap[0] and self.dataclose[0] > self.twap[0] and self.rsi[0] < 70:
                self.order = self.buy()
        else:
            if self.dataclose[0] < self.vwap[0] and self.dataclose[0] < self.twap[0] and self.rsi[0] > 30:
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
    cerebro.addstrategy(VWAPTWAPStrategy)
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