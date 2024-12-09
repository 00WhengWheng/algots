import backtrader as bt
import pandas as pd
from ..strategies.volume_profile_analysis import VolumeProfileAnalysis

class VolumeProfileAnalysisStrategy(bt.Strategy):
    params = (
        ('volume_col', 'Volume'),
        ('price_col', 'Close'),
        ('time_period', 20),
        ('num_levels', 10),
        ('atr_period', 14),
        ('risk_per_trade', 0.02),
        ('printlog', False),
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.datavolume = self.datas[0].volume

        self.volume_profile_analysis = VolumeProfileAnalysis(
            volume_col=self.params.volume_col,
            price_col=self.params.price_col,
            time_period=self.params.time_period,
            num_levels=self.params.num_levels,
            atr_period=self.params.atr_period
        )

        self.order = None

    def next(self):
        if self.order:
            return

        data = self.datas[0].pandas()
        signals = self.volume_profile_analysis.generate_signals(data)

        if not self.position:
            if signals['Signal'].iloc[-1] == 1:
                self.order = self.buy(size=signals['Position_Size'].iloc[-1])
            elif signals['Signal'].iloc[-1] == -1:
                self.order = self.sell(size=signals['Position_Size'].iloc[-1])
        else:
            if self.position.size > 0 and signals['Signal'].iloc[-1] == -1:
                self.order = self.sell(size=self.position.size)
            elif self.position.size < 0 and signals['Signal'].iloc[-1] == 1:
                self.order = self.buy(size=self.position.size)

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
    cerebro.addstrategy(VolumeProfileAnalysisStrategy)
    cerebro.broker.setcash(initial_cash)
    cerebro.broker.setcommission(commission=0.001)
    cerebro.addsizer(bt.sizers.FixedSize, stake=1)

    data_feed = bt.feeds.PandasData(dataname=data)
    cerebro.adddata(data_feed)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot()