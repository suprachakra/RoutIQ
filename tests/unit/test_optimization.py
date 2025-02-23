"""
Unit tests for optimization algorithms and the orchestrator.
Tests include:
- Genetic Algorithm execution.
- Simulated Annealing execution.
- Reinforcement Learning action selection.
"""

import pytest
import random
from src.services.optimization.optimizer import Optimizer

# Dummy fitness function: lower sum indicates a better solution.
def dummy_fitness(chromosome):
    return -sum(chromosome)

@pytest.fixture
def optimizer_instance():
    gene_pool = list(range(1, 21))
    chromosome_length = 10
    return Optimizer(dummy_fitness, gene_pool, chromosome_length)

def test_run_genetic(optimizer_instance):
    best_solution, best_fitness = optimizer_instance.run_genetic(
        generations=10,
        population_size=30,
        mutation_rate=0.1,
        crossover_rate=0.8
    )
    assert isinstance(best_solution, list), "Best solution should be a list."
    assert len(best_solution) == optimizer_instance.chromosome_length, "Chromosome length mismatch."
    assert isinstance(best_fitness, float), "Best fitness should be a float."

def test_run_simulated_annealing(optimizer_instance):
    initial_solution = random.sample(optimizer_instance.gene_pool, optimizer_instance.chromosome_length)
    best_solution, best_fitness = optimizer_instance.run_simulated_annealing(
        initial_solution=initial_solution,
        initial_temp=500,
        cooling_rate=0.9,
        min_temp=1,
        max_iter=100
    )
    assert isinstance(best_solution, list), "Best solution should be a list."
    assert len(best_solution) == optimizer_instance.chromosome_length, "Chromosome length mismatch."
    assert isinstance(best_fitness, float), "Best fitness should be a float."

def test_run_reinforcement_learning(optimizer_instance):
    import numpy as np
    # Create a dummy state as a numpy array.
    state = np.array(optimizer_instance.gene_pool[:optimizer_instance.chromosome_length], dtype=float)
    action = optimizer_instance.run_reinforcement_learning(
        state=state,
        state_size=optimizer_instance.chromosome_length,
        action_size=5,
        training_steps=10
    )
    assert isinstance(action, int), "RL should return an integer action."

if __name__ == "__main__":
    pytest.main()
