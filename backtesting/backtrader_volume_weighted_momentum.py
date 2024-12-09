import backtrader as bt
import pandas as pd
from ..strategies.volume_weighted_momentum import VolumeWeightedMomentum

class VolumeWeightedMomentumStrategy(bt.Strategy):
    params = (
        ('momentum_period', 14),
        ('vwap_threshold', 0.02),
        ('risk_per_trade', 0.02),
        ('printlog', False),
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.datavolume = self.datas[0].volume

        self.vwap = bt.indicators.VolumeWeightedAveragePrice(self.datas[0], period=self.params.momentum_period)
        self.momentum = bt.indicators.Momentum(self.datas[0], period=self.params.momentum_period)

        self.order = None

    def next(self):
        if self.order:
            return

        threshold = self.params.vwap_threshold

        if not self.position:
            if self.dataclose[0] > self.vwap[0] * (1 + threshold) and self.momentum[0] > 0:
                self.order = self.buy()
        else:
            if self.dataclose[0] < self.vwap[0] * (1 - threshold) and self.momentum[0] < 0:
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
    cerebro.addstrategy(VolumeWeightedMomentumStrategy)
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