from dataclasses import dataclass
import random

from .architecture import Architecture, mutate, random_architecture
from .evaluator import Evaluation, evaluate_counts, reward
from .problems import BinaryProblem
from .simulator import QuantumSimulator


@dataclass(frozen=True)
class ArchitectureResult:
    architecture: Architecture
    evaluation: Evaluation
    reward: float


class ArchitectureDiscovery:
    """Evolutionary search over circuit topology and gate choices."""

    def __init__(self, simulator: QuantumSimulator | None = None, seed: int = 7):
        self.simulator = simulator or QuantumSimulator(shots=1024)
        self.rng = random.Random(seed)

    def evaluate(self, problem: BinaryProblem, architecture: Architecture) -> ArchitectureResult:
        counts = self.simulator.run(architecture.build())
        evaluation = evaluate_counts(problem, counts, architecture.depth_proxy)
        return ArchitectureResult(architecture, evaluation, reward(evaluation))

    def discover(
        self,
        problem: BinaryProblem,
        population_size: int = 8,
        generations: int = 6,
        initial_depth: int = 6,
    ) -> ArchitectureResult:
        population = [
            random_architecture(problem.num_variables, initial_depth, self.rng)
            for _ in range(population_size)
        ]
        best: ArchitectureResult | None = None
        for _ in range(generations):
            scored = sorted(
                (self.evaluate(problem, candidate) for candidate in population),
                key=lambda result: result.reward,
                reverse=True,
            )
            if best is None or scored[0].reward > best.reward:
                best = scored[0]
            survivors = [item.architecture for item in scored[: max(2, population_size // 2)]]
            population = survivors[:]
            while len(population) < population_size:
                parent = self.rng.choice(survivors)
                population.append(mutate(parent, self.rng))
        assert best is not None
        return best
