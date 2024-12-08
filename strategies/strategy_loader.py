import importlib
from typing import Dict, Any, Optional
from ..config.strategy_config import STRATEGY_REGISTRY

class StrategyLoader:
    @staticmethod
    def load_strategy(strategy_name: str, parameters: Optional[Dict[str, Any]] = None) -> Any:
        """
        Dynamically loads and instantiates a trading strategy.
        
        Args:
            strategy_name: Name of the strategy as defined in STRATEGY_REGISTRY
            parameters: Optional parameters to override defaults
            
        Returns:
            Instantiated strategy object
        """
        if strategy_name not in STRATEGY_REGISTRY:
            raise ValueError(f"Strategy {strategy_name} not found in registry")
            
        strategy_config = STRATEGY_REGISTRY[strategy_name]
        
        # Import the strategy module
        module = importlib.import_module(strategy_config['module'])
        
        # Get the strategy class
        strategy_class = getattr(module, strategy_config['class'])
        
        # Merge default parameters with provided parameters
        final_params = {}
        if 'parameters' in strategy_config:
            for param_name, param_config in strategy_config['parameters'].items():
                if parameters and param_name in parameters:
                    final_params[param_name] = parameters[param_name]
                else:
                    final_params[param_name] = param_config.get('default')
        
        # Instantiate the strategy
        return strategy_class(final_params)

    @staticmethod
    def get_strategy_parameters(strategy_name: str) -> Dict[str, Any]:
        """
        Returns the parameter configuration for a strategy.
        
        Args:
            strategy_name: Name of the strategy
            
        Returns:
            Dictionary of parameter configurations
        """
        if strategy_name not in STRATEGY_REGISTRY:
            raise ValueError(f"Strategy {strategy_name} not found in registry")
            
        return STRATEGY_REGISTRY[strategy_name].get('parameters', {})

    @staticmethod
    def list_available_strategies() -> list:
        """
        Returns a list of all available strategy names.
        
        Returns:
            List of strategy names
        """
        return list(STRATEGY_REGISTRY.keys())
