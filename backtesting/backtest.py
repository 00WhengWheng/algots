from typing import Dict, Any, Optional
import pandas as pd
import numpy as np
from ..strategies.strategy_loader import StrategyLoader
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Backtester:
    def __init__(self, 
                 initial_capital: float = 100000.0,
                 commission: float = 0.001,
                 slippage: float = 0.001):
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.strategy_loader = StrategyLoader()
        self.reset()

    def reset(self):
        self.capital = self.initial_capital
        self.positions = {}
        self.trades = []
        self.equity_curve = []
        
    def run(self, 
            strategy_name: str,
            data: pd.DataFrame,
            parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run backtest for a given strategy and data
        
        Args:
            strategy_name: Name of the strategy to test
            data: Historical price data
            parameters: Strategy parameters
        """
        self.reset()
        strategy = self.strategy_loader.load_strategy(strategy_name, parameters)
        
        # Generate signals
        signals_df = strategy.generate_signals(data)
        
        # Track performance
        for i in range(len(signals_df)):
            current_bar = signals_df.iloc[i]
            self._process_bar(current_bar, strategy)
            self.equity_curve.append(self._calculate_total_equity(current_bar))
            
        return self._generate_results()

    def _process_bar(self, bar, strategy):
        # Process exits first
        self._process_exits(bar)
        
        # Process entries
        if bar['Signal'] != 0:
            position_size = strategy.calculate_position_size(self.capital)
            entry_price = self._calculate_entry_price(bar['Close'])
            
            if bar['Signal'] > 0:  # Buy signal
                cost = position_size * entry_price * (1 + self.commission)
                if cost <= self.capital:
                    self.positions[bar.name] = {
                        'type': 'long',
                        'size': position_size,
                        'entry_price': entry_price,
                        'stop_loss': bar.get('Stop_Loss'),
                        'take_profit': bar.get('Take_Profit')
                    }
                    self.capital -= cost
                    self._record_trade('LONG', entry_price, position_size, bar.name)
                    
            elif bar['Signal'] < 0:  # Sell signal
                cost = position_size * entry_price * (1 + self.commission)
                if cost <= self.capital:
                    self.positions[bar.name] = {
                        'type': 'short',
                        'size': position_size,
                        'entry_price': entry_price,
                        'stop_loss': bar.get('Stop_Loss'),
                        'take_profit': bar.get('Take_Profit')
                    }
                    self.capital -= cost
                    self._record_trade('SHORT', entry_price, position_size, bar.name)

    def _process_exits(self, bar):
        for timestamp, position in list(self.positions.items()):
            exit_price = None
            
            if position['type'] == 'long':
                if (position['stop_loss'] and bar['Low'] <= position['stop_loss']) or \
                   (position['take_profit'] and bar['High'] >= position['take_profit']):
                    exit_price = self._calculate_exit_price(bar['Close'])
                    
            elif position['type'] == 'short':
                if (position['stop_loss'] and bar['High'] >= position['stop_loss']) or \
                   (position['take_profit'] and bar['Low'] <= position['take_profit']):
                    exit_price = self._calculate_exit_price(bar['Close'])
            
            if exit_price:
                self._close_position(timestamp, position, exit_price, bar.name)

    def _calculate_entry_price(self, price):
        return price * (1 + self.slippage)

    def _calculate_exit_price(self, price):
        return price * (1 - self.slippage)

    def _close_position(self, timestamp, position, exit_price, exit_time):
        if position['type'] == 'long':
            profit = (exit_price - position['entry_price']) * position['size']
        else:
            profit = (position['entry_price'] - exit_price) * position['size']
            
        self.capital += (position['size'] * exit_price * (1 - self.commission)) + profit
        self._record_trade('EXIT', exit_price, position['size'], exit_time, profit)
        del self.positions[timestamp]

    def _record_trade(self, trade_type, price, size, timestamp, pnl=None):
        self.trades.append({
            'timestamp': timestamp,
            'type': trade_type,
            'price': price,
            'size': size,
            'pnl': pnl
        })

    def _calculate_total_equity(self, bar):
        equity = self.capital
        for position in self.positions.values():
            if position['type'] == 'long':
                equity += position['size'] * bar['Close']
            else:
                equity += position['size'] * (2 * position['entry_price'] - bar['Close'])
        return equity

    def _generate_results(self) -> Dict[str, Any]:
        equity_curve = pd.Series(self.equity_curve)
        returns = equity_curve.pct_change().dropna()
        
        results = {
            'initial_capital': self.initial_capital,
            'final_capital': self.equity_curve[-1],
            'total_return': (self.equity_curve[-1] / self.initial_capital - 1) * 100,
            'sharpe_ratio': self._calculate_sharpe_ratio(returns),
            'max_drawdown': self._calculate_max_drawdown(equity_curve),
            'trade_count': len(self.trades),
            'equity_curve': equity_curve,
            'trades': pd.DataFrame(self.trades)
        }
        
        return results

    def _calculate_sharpe_ratio(self, returns):
        if len(returns) < 2:
            return 0
        return np.sqrt(252) * returns.mean() / returns.std()

    def _calculate_max_drawdown(self, equity_curve):
        rolling_max = equity_curve.expanding().max()
        drawdowns = equity_curve / rolling_max - 1
        return drawdowns.min() * 100
