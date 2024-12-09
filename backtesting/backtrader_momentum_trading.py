import backtrader as bt
import pandas as pd
from ..strategies.momentum_trading import MomentumTrading

class MomentumTradingStrategy(bt.Strategy):
    params = (
        ('rsi_period', 14),
        ('stochastic_period', 14),
        ('ma_period', 50),
        ('stop_loss_pct', 0.02),
        ('take_profit_pct', 0.04),
        ('max_holding_days', 5),
        ('printlog', False),
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.dataopen = self.datas[0].open
        self.datavolume = self.datas[0].volume
        self.rsi = bt.indicators.RSI(self.datas[0], period=self.params.rsi_period)
        self.stochastic = bt.indicators.Stochastic(self.datas[0], period=self.params.stochastic_period)
        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.ma_period)
        self.doji_detected = False
        self.hammer_detected = False

    def next(self):
        if not self.position:
            if self.buy_signal():
                self.buy(size=100)
        else:
            if self.sell_signal():
                self.sell(size=100)

    def buy_signal(self):
        return (self.rsi < 30 and self.stochastic.percK < 20 and self.hammer_detected and
                self.dataclose[0] > self.sma[0] and self.datavolume[0] > bt.indicators.Average(self.datavolume, period=20))

    def sell_signal(self):
        return (self.rsi > 70 and self.stochastic.percK > 80 and self.doji_detected and
                self.dataclose[0] < self.sma[0] and self.datavolume[0] > bt.indicators.Average(self.datavolume, period=20))

    def notify_order(self, order):
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, Price: {order.executed.price}')
            elif order.issell():
                self.log(f'SELL EXECUTED, Price: {order.executed.price}')

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        if self.params.printlog:
            print(f'{dt.isoformat()} {txt}')

    def stop(self):
        self.log(f'Ending Value {self.broker.getvalue()}', dt=self.datas[0].datetime.date(0))

def run_backtest(data: pd.DataFrame, initial_cash: float = 100000.0):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MomentumTradingStrategy)
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