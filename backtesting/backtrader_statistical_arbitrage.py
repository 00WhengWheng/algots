import backtrader as bt
import pandas as pd
from ..strategies.statistical_arbitrage import StatisticalArbitrage

class StatisticalArbitrageStrategy(bt.Strategy):
    params = (
        ('lookback_period', 60),
        ('z_score_threshold', 2.0),
        ('printlog', False),
    )

    def __init__(self):
        self.data0 = self.datas[0]
        self.data1 = self.datas[1]

        self.stat_arb = StatisticalArbitrage(
            lookback_period=self.params.lookback_period,
            z_score_threshold=self.params.z_score_threshold
        )

        self.order = None

    def next(self):
        if self.order:
            return

        data = pd.DataFrame({
            'asset1': self.data0.close.get(size=self.params.lookback_period),
            'asset2': self.data1.close.get(size=self.params.lookback_period)
        })

        if len(data) < self.params.lookback_period:
            return

        signals = self.stat_arb.generate_signals(data)

        if not self.position:
            if signals['asset1'].iloc[-1] == 1:
                self.order = self.buy(data=self.data0, size=1)
                self.sell(data=self.data1, size=1)
            elif signals['asset1'].iloc[-1] == -1:
                self.order = self.sell(data=self.data0, size=1)
                self.buy(data=self.data1, size=1)
        else:
            if signals['asset1'].iloc[-1] == 0:
                self.close(data=self.data0)
                self.close(data=self.data1)

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

def run_backtest(data1: pd.DataFrame, data2: pd.DataFrame, initial_cash: float = 100000.0):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(StatisticalArbitrageStrategy)
    cerebro.broker.setcash(initial_cash)
    cerebro.broker.setcommission(commission=0.001)

    data_feed1 = bt.feeds.PandasData(dataname=data1)
    data_feed2 = bt.feeds.PandasData(dataname=data2)
    cerebro.adddata(data_feed1)
    cerebro.adddata(data_feed2)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot()