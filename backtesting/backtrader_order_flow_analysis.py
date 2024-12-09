import backtrader as bt
import pandas as pd
from ..strategies.order_flow_analysis import OrderFlowAnalysis

class OrderFlowAnalysisStrategy(bt.Strategy):
    params = (
        ('buy_volume_col', 'Buy_Volume'),
        ('sell_volume_col', 'Sell_Volume'),
        ('printlog', False),
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.data_buy_volume = self.datas[0].getcolumn(self.params.buy_volume_col)
        self.data_sell_volume = self.datas[0].getcolumn(self.params.sell_volume_col)
        self.order = None

    def next(self):
        if self.order:
            return

        order_flow_imbalance = self.data_buy_volume[0] - self.data_sell_volume[0]
        double_top_detected = self.detect_double_top()

        if not self.position:
            if order_flow_imbalance > 0 and not double_top_detected:
                self.order = self.buy()
        else:
            if order_flow_imbalance < 0:
                self.order = self.sell()

    def detect_double_top(self):
        # Implement the logic to detect double top pattern
        # This is a placeholder for the actual pattern detection logic
        return False

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
    cerebro.addstrategy(OrderFlowAnalysisStrategy)
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