from dataclasses import dataclass

from .architecture import Architecture, mutate
from .architectural_search import ArchitectureDiscovery, ArchitectureResult
from .problems import BinaryProblem
from .strategy import Strategy, default_strategies


@dataclass(frozen=True)
class StrategyResult:
    strategy: str
    result: ArchitectureResult


class MetaSearch:
    """Compare multiple circuit starting strategies before evolutionary search."""

    def __init__(self, discovery: ArchitectureDiscovery | None = None):
        self.discovery = discovery or ArchitectureDiscovery()

    def discover(
        self,
        problem: BinaryProblem,
        strategies: list[Strategy] | None = None,
        generations: int = 4,
    ) -> StrategyResult:
        strategies = strategies or default_strategies()
        best: StrategyResult | None = None
        for strategy in strategies:
            seed_architecture = strategy.generator(problem.num_variables)
            population = [seed_architecture]
            while len(population) < 8:
                population.append(mutate(seed_architecture, self.discovery.rng))

            current: ArchitectureResult | None = None
            for _ in range(generations):
                scored = sorted(
                    (self.discovery.evaluate(problem, candidate) for candidate in population),
                    key=lambda item: item.reward,
                    reverse=True,
                )
                current = scored[0]
                survivors = [item.architecture for item in scored[:4]]
                population = survivors[:]
                while len(population) < 8:
                    parent = self.discovery.rng.choice(survivors)
                    population.append(mutate(parent, self.discovery.rng))

            assert current is not None
            candidate = StrategyResult(strategy.name, current)
            if best is None or candidate.result.reward > best.result.reward:
                best = candidate
        assert best is not None
        return best
