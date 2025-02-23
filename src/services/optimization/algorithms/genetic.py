"""
Implements Genetic Algorithm for route optimization.

This module provides a GeneticAlgorithm class that supports:
- Initialization of a population from a gene pool.
- Selection of parents via tournament selection.
- Crossover using an ordered crossover (OX) approach.
- Mutation through random gene swaps.
- Iterative evolution to produce improved solutions over a set number of generations.

Assumptions:
- The gene pool represents available route nodes.
- A chromosome is represented as a permutation (ordering) of genes.
- The fitness function is user-defined and evaluates route quality (e.g., lower distance equals higher fitness).
"""

import random
from typing import List, Callable, Tuple

class GeneticAlgorithm:
    def __init__(self, population_size: int, mutation_rate: float, crossover_rate: float, fitness_fn: Callable[[List[int]], float]):
        """
        Initialize the Genetic Algorithm.
        
        Args:
            population_size (int): Number of individuals in the population.
            mutation_rate (float): Probability of mutation for each gene.
            crossover_rate (float): Probability of performing crossover.
            fitness_fn (Callable[[List[int]], float]): Function to evaluate the fitness of a chromosome.
        """
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.fitness_fn = fitness_fn

    def initialize_population(self, gene_pool: List[int], chromosome_length: int) -> List[List[int]]:
        """
        Create an initial population of chromosomes.

        Args:
            gene_pool (List[int]): List of available genes (e.g., route nodes).
            chromosome_length (int): Number of genes per chromosome.
        
        Returns:
            List[List[int]]: A list containing the initial population.
        """
        population = []
        for _ in range(self.population_size):
            # Generate a random permutation from the gene pool.
            chromosome = random.sample(gene_pool, chromosome_length)
            population.append(chromosome)
        return population

    def tournament_selection(self, population: List[List[int]], tournament_size: int = 3) -> List[int]:
        """
        Select one individual from the population using tournament selection.

        Args:
            population (List[List[int]]): Current population of chromosomes.
            tournament_size (int): Number of individuals competing in the tournament.
        
        Returns:
            List[int]: The selected chromosome.
        """
        tournament = random.sample(population, tournament_size)
        # Sort based on fitness (higher fitness is better).
        tournament.sort(key=self.fitness_fn, reverse=True)
        return tournament[0]

    def crossover(self, parent1: List[int], parent2: List[int]) -> Tuple[List[int], List[int]]:
        """
        Perform crossover between two parents to produce two offspring.

        Args:
            parent1 (List[int]): First parent chromosome.
            parent2 (List[int]): Second parent chromosome.
        
        Returns:
            Tuple[List[int], List[int]]: Two offspring chromosomes.
        """
        if random.random() < self.crossover_rate:
            size = len(parent1)
            point1 = random.randint(0, size - 2)
            point2 = random.randint(point1 + 1, size - 1)
            child1 = self.__ordered_crossover(parent1, parent2, point1, point2)
            child2 = self.__ordered_crossover(parent2, parent1, point1, point2)
            return child1, child2
        else:
            # No crossover occurs; return copies of the parents.
            return parent1.copy(), parent2.copy()

    def __ordered_crossover(self, parent1: List[int], parent2: List[int], point1: int, point2: int) -> List[int]:
        """
        Helper method to perform ordered crossover (OX).

        Args:
            parent1 (List[int]): Chromosome to extract the segment from.
            parent2 (List[int]): Chromosome to fill remaining genes.
            point1 (int): Start index of crossover segment.
            point2 (int): End index of crossover segment.
        
        Returns:
            List[int]: Offspring chromosome after ordered crossover.
        """
        child = [None] * len(parent1)
        # Copy a segment from parent1.
        child[point1:point2] = parent1[point1:point2]
        current_index = point2
        # Fill in genes from parent2 that are not already in the child.
        for gene in parent2:
            if gene not in child:
                if current_index >= len(parent1):
                    current_index = 0
                child[current_index] = gene
                current_index += 1
        return child

    def mutate(self, chromosome: List[int]) -> List[int]:
        """
        Mutate a chromosome by swapping two genes based on the mutation rate.

        Args:
            chromosome (List[int]): Chromosome to mutate.
        
        Returns:
            List[int]: Mutated chromosome.
        """
        for i in range(len(chromosome)):
            if random.random() < self.mutation_rate:
                j = random.randint(0, len(chromosome) - 1)
                chromosome[i], chromosome[j] = chromosome[j], chromosome[i]
        return chromosome

    def evolve(self, population: List[List[int]], gene_pool: List[int]) -> List[List[int]]:
        """
        Evolve the current population by applying selection, crossover, and mutation.

        Args:
            population (List[List[int]]): Current population of chromosomes.
            gene_pool (List[int]): Gene pool for validation.
        
        Returns:
            List[List[int]]: New population after evolution.
        """
        new_population = []
        # Apply elitism: preserve the best individual.
        population.sort(key=self.fitness_fn, reverse=True)
        best_individual = population[0].copy()
        new_population.append(best_individual)

        # Generate rest of the new population.
        while len(new_population) < self.population_size:
            parent1 = self.tournament_selection(population)
            parent2 = self.tournament_selection(population)
            child1, child2 = self.crossover(parent1, parent2)
            new_population.append(self.mutate(child1))
            if len(new_population) < self.population_size:
                new_population.append(self.mutate(child2))
        return new_population

    def run(self, gene_pool: List[int], chromosome_length: int, generations: int) -> Tuple[List[int], float]:
        """
        Run the genetic algorithm for a specified number of generations.

        Args:
            gene_pool (List[int]): Available genes (e.g., route nodes).
            chromosome_length (int): Length of each chromosome.
            generations (int): Number of generations to evolve.
        
        Returns:
            Tuple[List[int], float]: The best chromosome found and its corresponding fitness score.
        """
        population = self.initialize_population(gene_pool, chromosome_length)
        best_chromosome = None
        best_fitness = float('-inf')

        for gen in range(generations):
            population = self.evolve(population, gene_pool)
            current_best = max(population, key=self.fitness_fn)
            current_fitness = self.fitness_fn(current_best)
            if current_fitness > best_fitness:
                best_chromosome = current_best.copy()
                best_fitness = current_fitness
            # Debug output for each generation.
            print(f"Generation {gen + 1}: Best Fitness = {best_fitness:.4f}")

        return best_chromosome, best_fitness

# Example usage:
if __name__ == "__main__":
    # Dummy fitness function: aim to minimize total route distance.
    def fitness(chromosome: List[int]) -> float:
        # In a real implementation, this would use a distance matrix.
        # Here, we simulate by summing gene values (assuming lower sum means shorter distance).
        return -sum(chromosome)

    gene_pool = list(range(1, 21))  # Example gene pool: nodes 1 to 20.
    chromosome_length = 10         # Each chromosome represents a route with 10 stops.

    ga = GeneticAlgorithm(
        population_size=50,
        mutation_rate=0.05,
        crossover_rate=0.7,
        fitness_fn=fitness
    )
    best_route, best_score = ga.run(gene_pool, chromosome_length, generations=50)
    print("Best Route Found:", best_route)
    print("Best Fitness Score:", best_score)
