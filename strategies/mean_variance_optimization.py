import pandas as pd
import numpy as np
from scipy.optimize import minimize


class MeanVarianceOptimization:
    def __init__(self, risk_free_rate: float = 0.01, target_return: float = None):
        self.risk_free_rate = risk_free_rate
        self.target_return = target_return

    required_patterns = []

    def optimize_portfolio(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Optimize portfolio using mean-variance optimization.

        :param data: Pandas DataFrame with price data for multiple assets.
        :return: DataFrame with portfolio weights and metrics.
        """
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
        weights = result.x

        # Calculate portfolio metrics
        portfolio_return = np.sum(returns * weights)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_volatility

        # Create results DataFrame
        results = pd.DataFrame({
            'Weight': weights,
            'Return': returns,
            'Symbol': returns.index
        })
        results['Portfolio_Return'] = portfolio_return
        results['Portfolio_Volatility'] = portfolio_volatility
        results['Sharpe_Ratio'] = sharpe_ratio

        return results

    def negative_sharpe_ratio(self, weights, returns, cov_matrix):
        """
        Calculate the negative Sharpe ratio (for minimization).

        :param weights: Array of asset weights.
        :param returns: Series of asset returns.
        :param cov_matrix: Covariance matrix of returns.
        :return: Negative Sharpe ratio.
        """
        portfolio_return = np.sum(returns * weights)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_volatility
        return -sharpe_ratio  # Negative because we want to maximize Sharpe ratio

    def optimize_for_target_return(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Optimize portfolio for minimum variance given a target return.

        :param data: Pandas DataFrame with price data for multiple assets.
        :return: DataFrame with portfolio weights and metrics.
        """
        if self.target_return is None:
            raise ValueError("Target return must be set for this optimization method.")

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
        constraints = (
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},  # weights sum to 1
            {'type': 'eq', 'fun': lambda x: np.sum(returns * x) - self.target_return}  # target return
        )

        # Bounds for weights (0 to 1)
        bounds = tuple((0, 1) for _ in range(n))

        # Optimize for minimum variance
        result = minimize(
            self.portfolio_variance,
            initial_weights,
            args=(cov_matrix,),
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )

        # Extract the optimized weights
        weights = result.x

        # Calculate portfolio metrics
        portfolio_return = np.sum(returns * weights)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_volatility

        # Create results DataFrame
        results = pd.DataFrame({
            'Weight': weights,
            'Return': returns,
            'Symbol': returns.index
        })
        results['Portfolio_Return'] = portfolio_return
        results['Portfolio_Volatility'] = portfolio_volatility
        results['Sharpe_Ratio'] = sharpe_ratio

        return results

    def portfolio_variance(self, weights, cov_matrix):
        """
        Calculate the portfolio variance.

        :param weights: Array of asset weights.
        :param cov_matrix: Covariance matrix of returns.
        :return: Portfolio variance.
        """
        return np.dot(weights.T, np.dot(cov_matrix, weights))