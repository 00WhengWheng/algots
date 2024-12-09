import backtrader as bt
import pandas as pd
from ..strategies.sentiment_analysis import SentimentAnalysis

class SentimentAnalysisStrategy(bt.Strategy):
    params = (
        ('sentiment_column', 'Sentiment'),
        ('threshold', 0.1),
        ('printlog', False),
    )

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.sentiment_data = self.datas[0].sentiment

        self.sentiment_analysis = SentimentAnalysis(
            sentiment_column=self.params.sentiment_column,
            threshold=self.params.threshold
        )

        self.order = None

    def next(self):
        if self.order:
            return

        data = pd.DataFrame({
            'Close': self.dataclose.get(size=1),
            self.params.sentiment_column: self.sentiment_data.get(size=1)
        })

        signals = self.sentiment_analysis.generate_signals(data)

        if not self.position:
            if signals['Signal'].iloc[-1] == 1:
                self.order = self.buy()
            elif signals['Signal'].iloc[-1] == -1:
                self.order = self.sell()
        else:
            if signals['Signal'].iloc[-1] == 0:
                self.close()

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
    cerebro.addstrategy(SentimentAnalysisStrategy)
    cerebro.broker.setcash(initial_cash)
    cerebro.broker.setcommission(commission=0.001)

    data_feed = bt.feeds.PandasData(dataname=data)
    cerebro.adddata(data_feed)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot()