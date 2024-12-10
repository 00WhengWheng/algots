from typing import Dict, Any, Optional
from config.strategy_config import STRATEGY_REGISTRY
from .base_strategy import BaseStrategy

class StrategyLoader:
    @staticmethod
    def load_strategy(strategy_name: str, parameters: Optional[Dict[str, Any]] = None) -> BaseStrategy:
        if strategy_name not in STRATEGY_REGISTRY:
            raise ValueError(f"Strategy '{strategy_name}' not found in registry")

        strategy_class = STRATEGY_REGISTRY[strategy_name]['class']
        default_params = STRATEGY_REGISTRY[strategy_name].get('parameters', {})

        final_params = default_params.copy()
        if parameters:
            final_params.update(parameters)

        return strategy_class(final_params)

    @staticmethod
    def get_strategy_parameters(strategy_name: str) -> Dict[str, Any]:
        if strategy_name not in STRATEGY_REGISTRY:
            raise ValueError(f"Strategy '{strategy_name}' not found in registry")

        return STRATEGY_REGISTRY[strategy_name].get('parameters', {})

    @staticmethod
    def list_available_strategies() -> list:
        return list(STRATEGY_REGISTRY.keys())
