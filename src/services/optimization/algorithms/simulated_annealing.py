"""
Implements Simulated Annealing for route optimization with fallback strategies.

This module provides a SimulatedAnnealing class that:
- Generates a neighbor solution by swapping two elements.
- Uses an acceptance probability function based on a cooling schedule.
- Iterates until a minimum temperature is reached.
- Maintains and returns the best-known solution even if the algorithm stagnates.

Assumptions:
- A chromosome is a list of route nodes.
- The fitness function returns a value where higher indicates a better solution.
"""

import math
import random
from typing import List, Callable, Tuple

class SimulatedAnnealing:
    def __init__(self, initial_state: List[int], fitness_fn: Callable[[List[int]], float],
                 initial_temp: float = 1000.0, cooling_rate: float = 0.95, min_temp: float = 1e-3, max_iter: int = 1000):
        """
        Initialize the Simulated Annealing algorithm.
        
        Args:
            initial_state (List[int]): The starting solution (chromosome).
            fitness_fn (Callable[[List[int]], float]): Fitness function to evaluate a solution.
            initial_temp (float): Starting temperature.
            cooling_rate (float): Rate at which the temperature decreases.
            min_temp (float): Minimum temperature to stop the algorithm.
            max_iter (int): Maximum iterations to perform at each temperature level.
        """
        self.state = initial_state
        self.fitness_fn = fitness_fn
        self.temp = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp
        self.max_iter = max_iter

    def get_neighbor(self, state: List[int]) -> List[int]:
        """
        Generate a neighbor solution by swapping two random elements.
        
        Args:
            state (List[int]): Current solution.
        
        Returns:
            List[int]: Neighbor solution.
        """
        neighbor = state.copy()
        idx1, idx2 = random.sample(range(len(state)), 2)
        neighbor[idx1], neighbor[idx2] = neighbor[idx2], neighbor[idx1]
        return neighbor

    def acceptance_probability(self, current_fitness: float, neighbor_fitness: float) -> float:
        """
        Calculate the acceptance probability for a (possibly worse) solution.
        
        Args:
            current_fitness (float): Fitness of the current solution.
            neighbor_fitness (float): Fitness of the neighbor solution.
        
        Returns:
            float: Acceptance probability.
        """
        if neighbor_fitness > current_fitness:
            return 1.0
        return math.exp((neighbor_fitness - current_fitness) / self.temp)

    def run(self) -> Tuple[List[int], float]:
        """
        Execute the simulated annealing algorithm.
        
        Returns:
            Tuple[List[int], float]: The best solution found and its corresponding fitness.
        """
        current_state = self.state.copy()
        best_state = current_state.copy()
        current_fitness = self.fitness_fn(current_state)
        best_fitness = current_fitness

        while self.temp > self.min_temp:
            for _ in range(self.max_iter):
                neighbor = self.get_neighbor(current_state)
                neighbor_fitness = self.fitness_fn(neighbor)
                if self.acceptance_probability(current_fitness, neighbor_fitness) > random.random():
                    current_state = neighbor
                    current_fitness = neighbor_fitness
                    if current_fitness > best_fitness:
                        best_state = current_state.copy()
                        best_fitness = current_fitness
            self.temp *= self.cooling_rate
            print(f"Temperature: {self.temp:.4f}, Best Fitness: {best_fitness:.4f}")
        return best_state, best_fitness

# Example usage:
if __name__ == "__main__":
    def fitness(state: List[int]) -> float:
        # Dummy fitness: lower sum of elements indicates a better solution.
        return -sum(state)

    initial = list(range(1, 11))
    random.shuffle(initial)
    sa = SimulatedAnnealing(initial_state=initial, fitness_fn=fitness, initial_temp=1000, cooling_rate=0.9, min_temp=1)
    best_solution, best_fitness = sa.run()
    print("Best Solution:", best_solution)
    print("Best Fitness:", best_fitness)
