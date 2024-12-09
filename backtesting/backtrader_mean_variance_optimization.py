import backtrader as bt
import pandas as pd
import numpy as np
from scipy.optimize import minimize

class MeanVarianceOptimizationStrategy(bt.Strategy):
    params = (
        ('risk_free_rate', 0.01),
        ('target_return', None),
        ('printlog', False),
    )

    def __init__(self):
        self.weights = None

    def optimize_portfolio(self, data: pd.DataFrame):
        # Calculate returns if not already present
        if 'Returns' not in data.columns:
            data['Returns'] = data.groupby('Symbol')['Close'].pct_change()

        # Group by symbol and calculate mean returns and covariance matrix
        returns = data.groupby('Symbol')['Returns'].mean()
        cov_matrix = data.groupby('Symbol')['Returns'].apply(lambda x: x.cov())

        # Number of assets
        n = len(returns)

        # Initial guess of equal weights
        initial_weights = np.array([1/n for _ in range(n)])

        # Constraints
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})  # weights sum to 1

        # Bounds for weights (0 to 1)
        bounds = tuple((0, 1) for _ in range(n))

        # Optimize for maximum Sharpe ratio
        result = minimize(
            self.negative_sharpe_ratio,
            initial_weights,
            args=(returns, cov_matrix),
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )

        # Extract the optimized weights
        self.weights = result.x

    def negative_sharpe_ratio(self, weights, returns, cov_matrix):
        portfolio_return = np.sum(returns * weights)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        sharpe_ratio = (portfolio_return - self.params.risk_free_rate) / portfolio_volatility
        return -sharpe_ratio  # Negative because we want to maximize Sharpe ratio

    def next(self):
        # Implement logic to apply the optimized weights to the portfolio
        # This is a placeholder for applying the optimized portfolio weights
        pass

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        if self.params.printlog:
            print(f'{dt.isoformat()} {txt}')

    def stop(self):
        self.log(f'Ending Value {self.broker.getvalue()}', dt=self.datas[0].datetime.date(0))

def run_backtest(data: pd.DataFrame, initial_cash: float = 100000.0):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MeanVarianceOptimizationStrategy)
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