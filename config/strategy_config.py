from typing import Dict, Any
from strategies.delta_neutral_hedging import DeltaNeutralHedging
from strategies.mean_reversion import MeanReversion
from strategies.momentum_trading import MomentumTrading
from strategies.moving_average_crossover import MovingAverageCrossover
from strategies.statistical_arbitrage import StatisticalArbitrage
from strategies.trend_following import TrendFollowing
from strategies.volume_weighted_momentum import VolumeWeightedMomentum
from strategies.atr_based_breakout import ATRBasedBreakout
from strategies.event_driven import EventDriven
from strategies.gamma_scalping import GammaScalping
from strategies.keltner_channel import KeltnerChannel
from strategies.ma_crossover import MACrossover
from strategies.mean_variance_optimization import MeanVarianceOptimization
from strategies.multi_timeframe_analysis import MultiTimeframeAnalysis
from strategies.order_flow_analysis import OrderFlowAnalysis
from strategies.seasonality import Seasonality
from strategies.sentiment_analysis import SentimentAnalysis
from strategies.volatility_based import VolatilityBased
from strategies.volatility_breakout import VolatilityBreakout
from strategies.genetic_algorithms import GeneticAlgorithms
from strategies.volume_confirmation import VolumeConfirmation
from strategies.volume_profile_analysis import VolumeProfileAnalysis
from strategies.vwap_twap import VWAPTWAP
# Import all other strategy classes

STRATEGY_REGISTRY = {
    'ATR_BREAKOUT': {
        'class': 'ATRBasedBreakout',
        'module': 'strategies.atr_based_breakout',
        'parameters': ATRBasedBreakout.parameters
    },
     'DELTA_NEUTRAL_HEDGING': {
         'class': 'DeltaNeutralHedging',
         'module': 'strategies.delta_neutral_hedging',
         'parameters': DeltaNeutralHedging.parameters
     },
    'EVENT_DRIVEN': {
        'class': 'EventDriven',
        'module': 'strategies.event_driven',
        'parameters': EventDriven.parameters
    },
     'GAMMA_SCALPING': {
         'class': 'GammaScalping',
         'module': 'strategies.gamma_scalping',
         'parameters': GammaScalping.parameters
     },
     'GENETIC_ALGO': {
         'class': 'GeneticAlgorithms',
         'module': 'strategies.genetic_algorithms',
         'parameters': {
             'pop_size': {'default': 50, 'type': int, 'min': 20, 'max': 200},
             'num_generations': {'default': 100, 'type': int, 'min': 50, 'max': 500},
             'mutation_rate': {'default': 0.1, 'type': float, 'min': 0.01, 'max': 0.5},
             'num_top_strategies': {'default': 10, 'type': int, 'min': 5, 'max': 50}
         }
     },
      'KELTNER_CHANNEL': {
          'class': 'KeltnerChannel',
          'module': 'strategies.keltner_channel',
          'parameters': KeltnerChannel.parameters
      },
    "MA_CROSSOVER": {
        "module": "strategies.ma_crossover",
        "class": "MACrossover",
        "parameters": {
            "fast_period": 10,
            "slow_period": 30,
            "initial_capital": 10000,
            "risk_per_trade": 0.02
        }
    },
     'MEAN_REVERSION': {
         'class': 'MeanReversion',
         'module': 'strategies.mean_reversion',
         'parameters': MeanReversion.parameters
     },
     'MEAN_VARIANCE_OPT': {
         'class': 'MeanVarianceOptimization',
         'module': 'strategies.mean_variance_optimization',
         'parameters': {
             'risk_free_rate': {'default': 0.01, 'type': float, 'min': 0, 'max': 0.1},
             'target_return': {'default': None, 'type': float}
         }
     },
     'MOMENTUM_TRADING': {
         'class': 'MomentumTrading',
         'module': 'strategies.momentum_trading',
         'parameters': {
             'rsi_period': {'default': 14, 'type': int, 'min': 2, 'max': 50},
             'stochastic_period': {'default': 14, 'type': int, 'min': 2, 'max': 50},
             'ma_period': {'default': 50, 'type': int, 'min': 10, 'max': 200}
         }
     },
      'MOVING_AVERAGE_CROSSOVER': {
          'class': 'MovingAverageCrossover',
          'module': 'strategies.moving_average_crossover',
      },
     'MULTI_TIMEFRAME': {
         'class': 'MultiTimeframeAnalysis',
         'module': 'strategies.multi_timeframe_analysis',
         'parameters': {
             'short_period': {'default': 20, 'type': int, 'min': 5, 'max': 50},
             'long_period': {'default': 50, 'type': int, 'min': 20, 'max': 200},
             'timeframes': {'default': ["daily", "4h", "1h"], 'type': list}
         }
     },
     'ORDER_FLOW': {
         'class': 'OrderFlowAnalysis',
         'module': 'strategies.order_flow_analysis',
         'parameters': {
             'buy_volume_col': {'default': 'Buy_Volume', 'type': str},
             'sell_volume_col': {'default': 'Sell_Volume', 'type': str}
         }
     },
     'SEASONALITY': {
         'class': 'Seasonality',
         'module': 'strategies.seasonality',
         'parameters': {
             'target_month': {'default': 1, 'type': int, 'min': 1, 'max': 12}
         }
     },
     'SENTIMENT': {
         'class': 'SentimentAnalysis',
         'module': 'strategies.sentiment_analysis',
         'parameters': {
             'sentiment_column': {'default': 'Sentiment', 'type': str},
             'threshold': {'default': 0.1, 'type': float, 'min': -1.0, 'max': 1.0}
         }
     },
     'STATISTICAL_ARBITRAGE': {
         'class': 'StatisticalArbitrage',
         'module': 'strategies.statistical_arbitrage',
         'parameters': {
             'lookback_period': {'default': 60, 'type': int, 'min': 20, 'max': 200},
             'z_score_threshold': {'default': 2.0, 'type': float, 'min': 0.5, 'max': 4.0}
         }
     },
     'TREND_FOLLOWING': {
         'class': 'TrendFollowing',
         'module': 'strategies.trend_following',
         'parameters': {
             'short_period': {'default': 20, 'type': int, 'min': 5, 'max': 50},
             'long_period': {'default': 50, 'type': int, 'min': 20, 'max': 200},
             'atr_period': {'default': 14, 'type': int, 'min': 5, 'max': 30}
         }
     },
     'VOLATILITY_BASED': {
         'class': 'VolatilityBased',
         'module': 'strategies.volatility_based',
         'parameters': {
             'atr_period': {'default': 14, 'type': int, 'min': 5, 'max': 30},
             'bb_period': {'default': 20, 'type': int, 'min': 5, 'max': 50},
             'bb_std': {'default': 2.0, 'type': float, 'min': 1.0, 'max': 4.0},
             'rsi_period': {'default': 14, 'type': int, 'min': 5, 'max': 30}
         }
     },
     'VOLATILITY_BREAKOUT': {
         'class': 'VolatilityBreakout',
         'module': 'strategies.volatility_breakout',
         'parameters': {
             'bb_period': {'default': 20, 'type': int, 'min': 5, 'max': 50},
             'bb_std': {'default': 2.0, 'type': float, 'min': 1.0, 'max': 4.0},
             'atr_period': {'default': 14, 'type': int, 'min': 5, 'max': 30},
             'rsi_period': {'default': 14, 'type': int, 'min': 5, 'max': 30}
         }
     },
     'VOLUME_CONFIRMATION': {
         'class': 'VolumeConfirmation',
         'module': 'strategies.volume_confirmation',
         'parameters': {
             'bb_period': {'default': 20, 'type': int, 'min': 5, 'max': 50},
             'bb_std': {'default': 2.0, 'type': float, 'min': 1.0, 'max': 4.0},
             'atr_period': {'default': 14, 'type': int, 'min': 5, 'max': 30},
             'rsi_period': {'default': 14, 'type': int, 'min': 5, 'max': 30}
         }
     },
     'VOLUME_PROFILE': {
         'class': 'VolumeProfileAnalysis',
         'module': 'strategies.volume_profile_analysis',
         'parameters': {
             'volume_col': {'default': 'Volume', 'type': str},
             'price_col': {'default': 'Close', 'type': str},
             'time_period': {'default': 20, 'type': int, 'min': 5, 'max': 100},
             'num_levels': {'default': 10, 'type': int, 'min': 5, 'max': 50}
         }
     },
     'VOLUME_WEIGHTED_MOMENTUM': {
         'class': 'VolumeWeightedMomentum',
         'module': 'strategies.volume_weighted_momentum'
     },
     'VWAP_TWAP': {
         'class': 'VWAPTWAP',
         'module': 'strategies.vwap_twap',
         'parameters': {
             'vwap_period': {'default': 20, 'type': int, 'min': 5, 'max': 100},
             'twap_period': {'default': 20, 'type': int, 'min': 5, 'max': 100},
             'rsi_period': {'default': 14, 'type': int, 'min': 2, 'max': 50},
             'atr_period': {'default': 14, 'type': int, 'min': 2, 'max': 50}
         }
     }
}
COMMON_PARAMETERS = {
    'timeframe': {'default': '1h', 'type': str, 'options': ['1m', '5m', '15m', '1h', '4h', '1d']},
    'risk_per_trade': {'default': 0.02, 'type': float, 'min': 0.01, 'max': 0.05},
    'stop_loss': {'default': 0.02, 'type': float, 'min': 0.01, 'max': 0.10},
    'take_profit': {'default': 0.03, 'type': float, 'min': 0.01, 'max': 0.20},
    'max_positions': {'default': 3, 'type': int, 'min': 1, 'max': 10}
}