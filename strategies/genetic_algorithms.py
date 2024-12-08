import pandas as pd
import numpy as np
import random
from ..utils.base_strategy import BaseStrategy

class GeneticAlgorithms(BaseStrategy):
    def __init__(self, pop_size=50, num_generations=100, num_top_strategies=10, mutation_rate=0.1, 
                 short_window_range=(5, 50), long_window_range=(50, 200)):
        super().__init__()
        self.pop_size = pop_size
        self.num_generations = num_generations
        self.num_top_strategies = num_top_strategies
        self.mutation_rate = mutation_rate
        self.short_window_range = short_window_range
        self.long_window_range = long_window_range
        self.best_strategy = None
    required_patterns = []

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        self.data = data
        self.evolve_population()
        return self.apply_best_strategy(data)

    def moving_average_crossover_strategy(self, data, short_window, long_window):
        data['short_mavg'] = data['Close'].rolling(window=short_window).mean()
        data['long_mavg'] = data['Close'].rolling(window=long_window).mean()
        data['signal'] = 0
        data['signal'][short_window:] = np.where(data['short_mavg'][short_window:] > data['long_mavg'][short_window:], 1, -1)
        return data

    def calculate_fitness(self, data):
        data['returns'] = data['Close'].pct_change()
        data['strategy_returns'] = data['returns'] * data['signal'].shift(1)
        total_return = (1 + data['strategy_returns']).prod() - 1
        sharpe_ratio = np.sqrt(252) * data['strategy_returns'].mean() / data['strategy_returns'].std()
        return total_return * sharpe_ratio  # Combine return and risk metrics

    def initialize_population(self):
        return [(random.randint(*self.short_window_range), random.randint(*self.long_window_range)) 
                for _ in range(self.pop_size)]

    def evaluate_population(self, population):
        fitness_scores = []
        for short_window, long_window in population:
            strategy_data = self.moving_average_crossover_strategy(self.data.copy(), short_window, long_window)
            fitness = self.calculate_fitness(strategy_data)
            fitness_scores.append((fitness, (short_window, long_window)))
        return fitness_scores

    def select_top_strategies(self, fitness_scores):
        return [strategy for _, strategy in sorted(fitness_scores, reverse=True)[:self.num_top_strategies]]

    def crossover(self, parent1, parent2):
        child1 = (parent1[0], parent2[1])
        child2 = (parent2[0], parent1[1])
        return child1, child2

    def mutate(self, strategy):
        if random.random() < self.mutation_rate:
            return (random.randint(*self.short_window_range), strategy[1])
        elif random.random() < self.mutation_rate:
            return (strategy[0], random.randint(*self.long_window_range))
        return strategy

    def evolve_population(self):
        population = self.initialize_population()
        for _ in range(self.num_generations):
            fitness_scores = self.evaluate_population(population)
            top_strategies = self.select_top_strategies(fitness_scores)
            new_population = top_strategies.copy()
            while len(new_population) < self.pop_size:
                parent1, parent2 = random.sample(top_strategies, 2)
                child1, child2 = self.crossover(parent1, parent2)
                new_population.append(self.mutate(child1))
                if len(new_population) < self.pop_size:
                    new_population.append(self.mutate(child2))
            population = new_population

        final_fitness_scores = self.evaluate_population(population)
        self.best_strategy = max(final_fitness_scores, key=lambda x: x[0])[1]

    def apply_best_strategy(self, data):
        if self.best_strategy is None:
            raise ValueError("No best strategy found. Run evolve_population() first.")
        return self.moving_average_crossover_strategy(data, self.best_strategy[0], self.best_strategy[1])

    def get_strategy_params(self):
        return {
            "short_window": self.best_strategy[0],
            "long_window": self.best_strategy[1]
        } if self.best_strategy else None
