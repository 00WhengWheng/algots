import backtrader as bt
import pandas as pd

class DeltaNeutralHedgingStrategy(bt.Strategy):
    params = (
        ('delta_threshold', 0.5),
        ('risk_per_trade', 0.01),
        ('max_drawdown', 0.1),
        ('account_balance', 100000.0),
    )

    def __init__(self):
        self.delta = self.data.delta  # Assuming 'delta' is a column in your data
        self.position_size = None

    def next(self):
        if abs(self.delta[0]) > self.params.delta_threshold:
            self.position_size = self.calculate_position_size()

            if self.position_size is not None:
                if self.delta[0] > 0:
                    self.sell(size=self.position_size)
                else:
                    self.buy(size=self.position_size)

    def calculate_position_size(self):
        # Implement your position size calculation logic here
        return self.params.account_balance * self.params.risk_per_trade

def run_backtest(data: pd.DataFrame, initial_cash: float = 100000.0):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(DeltaNeutralHedgingStrategy)
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