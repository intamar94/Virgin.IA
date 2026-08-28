from dataclasses import dataclass

from .architecture import ArchitectureDiscovery
from .experiment import ExperimentRecord, ExperimentStore
from .formulation import maxcut_to_qubo
from .meta_search import MetaSearch
from .problems import BinaryProblem


@dataclass(frozen=True)
class AutoDiscoveryResult:
    formulation: object
    discovery: object
    experiment: ExperimentRecord


class AutoDiscovery:
    """End-to-end bounded discovery loop with persistent experiment memory."""

    def __init__(self, store: ExperimentStore | None = None):
        self.store = store or ExperimentStore()
        self.search = MetaSearch(ArchitectureDiscovery())

    def run(self, problem: BinaryProblem, generations: int = 2) -> AutoDiscoveryResult:
        if problem.num_variables < 2:
            raise ValueError("Virgin.IA requires at least two binary variables")
        if problem.name == "maxcut_triangle":
            formulation = maxcut_to_qubo(3, [(0, 1), (1, 2), (0, 2)])
        else:
            formulation = None
        result = self.search.discover(problem, generations=generations)
        record = self.store.record(problem.name, result.strategy, result)
        return AutoDiscoveryResult(formulation, result, record)
