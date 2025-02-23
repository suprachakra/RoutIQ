"""
Core orchestration to select and run the appropriate optimization algorithm.

This module integrates multiple optimization strategies:
- Genetic Algorithm (via genetic.py)
- Simulated Annealing (via simulated_annealing.py)
- Reinforcement Learning (via reinforcement_learning.py)

The Optimizer class provides methods to select an optimization method based on configuration,
execute the chosen method, and compare results. Fallback strategies are in place to ensure robust performance.
"""

from typing import List, Callable, Tuple
import random
import numpy as np

# Import the algorithms.
from src.services.optimization.algorithms.genetic import GeneticAlgorithm
from src.services.optimization.algorithms.simulated_annealing import SimulatedAnnealing
from src.services.optimization.algorithms.reinforcement_learning import RLAgent

class Optimizer:
    def __init__(self, fitness_fn: Callable[[List[int]], float], gene_pool: List[int], chromosome_length: int):
        """
        Initialize the Optimizer with a fitness function, gene pool, and chromosome length.
        
        Args:
            fitness_fn (Callable[[List[int]], float]): Function to evaluate a chromosome.
            gene_pool (List[int]): List of available genes.
            chromosome_length (int): Length of each chromosome.
        """
        self.fitness_fn = fitness_fn
        self.gene_pool = gene_pool
        self.chromosome_length = chromosome_length

    def run_genetic(self, generations: int = 50, population_size: int = 50,
                    mutation_rate: float = 0.05, crossover_rate: float = 0.7) -> Tuple[List[int], float]:
        """
        Run the Genetic Algorithm optimization.
        
        Args:
            generations (int): Number of generations.
            population_size (int): Population size.
            mutation_rate (float): Mutation rate.
            crossover_rate (float): Crossover rate.
        
        Returns:
            Tuple[List[int], float]: Best solution and its fitness.
        """
        ga = GeneticAlgorithm(population_size, mutation_rate, crossover_rate, self.fitness_fn)
        population = ga.initialize_population(self.gene_pool, self.chromosome_length)
        best_solution, best_fitness = ga.run(self.gene_pool, self.chromosome_length, generations)
        return best_solution, best_fitness

    def run_simulated_annealing(self, initial_solution: List[int] = None, initial_temp: float = 1000,
                                cooling_rate: float = 0.95, min_temp: float = 1e-3, max_iter: int = 1000) -> Tuple[List[int], float]:
        """
        Run the Simulated Annealing optimization.
        
        Args:
            initial_solution (List[int]): Starting solution; if None, generate randomly.
            initial_temp (float): Starting temperature.
            cooling_rate (float): Cooling rate.
            min_temp (float): Minimum temperature threshold.
            max_iter (int): Maximum iterations per temperature level.
        
        Returns:
            Tuple[List[int], float]: Best solution and its fitness.
        """
        if initial_solution is None:
            initial_solution = random.sample(self.gene_pool, self.chromosome_length)
        sa = SimulatedAnnealing(initial_solution, self.fitness_fn, initial_temp, cooling_rate, min_temp, max_iter)
        best_solution, best_fitness = sa.run()
        return best_solution, best_fitness

    def run_reinforcement_learning(self, state: np.ndarray, state_size: int, action_size: int,
                                   training_steps: int = 100) -> int:
        """
        Run a simplified RL model to decide on a route adjustment action.
        
        Args:
            state (np.ndarray): Current state.
            state_size (int): Dimensionality of the state.
            action_size (int): Number of possible actions.
            training_steps (int): Number of training iterations (for demo purposes).
        
        Returns:
            int: Selected action based on the RL model.
        """
        agent = RLAgent(state_size, action_size)
        # Dummy training loop for demonstration purposes.
        for _ in range(training_steps):
            action = agent.act(state)
            # In a real system, environment feedback would be incorporated.
            reward = self.fitness_fn(list(state[:self.chromosome_length]))  # Dummy reward based on partial state.
            next_state = state  # No change in state for demo.
            done = False
            agent.train(state, action, reward, next_state, done)
        return agent.act(state)

# Example usage:
if __name__ == "__main__":
    # Dummy fitness function: Lower sum indicates better solution.
    def fitness(chromosome: List[int]) -> float:
        return -sum(chromosome)

    gene_pool = list(range(1, 21))
    chromosome_length = 10

    optimizer = Optimizer(fitness, gene_pool, chromosome_length)
    
    best_genetic, fitness_genetic = optimizer.run_genetic(generations=50)
    print("Genetic Algorithm Best Solution:", best_genetic, "Fitness:", fitness_genetic)
    
    best_sa, fitness_sa = optimizer.run_simulated_annealing()
    print("Simulated Annealing Best Solution:", best_sa, "Fitness:", fitness_sa)
    
    # Create a dummy state for RL demonstration (using first chromosome_length elements as state).
    state = np.array(gene_pool[:chromosome_length], dtype=float)
    action_rl = optimizer.run_reinforcement_learning(state, state_size=chromosome_length, action_size=5)
    print("Reinforcement Learning selected action:", action_rl)
