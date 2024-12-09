import backtrader as bt
import pandas as pd
from ..strategies.moving_average_crossover import MovingAverageCrossover

class MovingAverageCrossoverStrategy(bt.Strategy):
    params = (
        ('fast_ma_period', 20),
        ('slow_ma_period', 50),
        ('ma_type', 'sma'),
        ('position_size', 1.0),
        ('stop_loss', 0.02),
        ('take_profit', 0.04),
        ('printlog', False),
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.fast_ma = self.get_moving_average(self.params.fast_ma_period)
        self.slow_ma = self.get_moving_average(self.params.slow_ma_period)
        self.order = None

    def get_moving_average(self, period):
        if self.params.ma_type == 'ema':
            return bt.indicators.ExponentialMovingAverage(self.datas[0], period=period)
        elif self.params.ma_type == 'wma':
            return bt.indicators.WeightedMovingAverage(self.datas[0], period=period)
        else:
            return bt.indicators.SimpleMovingAverage(self.datas[0], period=period)

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.fast_ma > self.slow_ma:
                self.order = self.buy(size=self.calculate_position_size())
        else:
            if self.fast_ma < self.slow_ma:
                self.order = self.sell(size=self.position.size)

    def calculate_position_size(self):
        return self.broker.get_cash() * self.params.position_size / self.dataclose[0]

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
    cerebro.addstrategy(MovingAverageCrossoverStrategy)
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