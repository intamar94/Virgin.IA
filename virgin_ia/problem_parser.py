from dataclasses import dataclass

from .formulation import BinaryFormulation, maxcut_to_qubo
from .problems import BinaryProblem


@dataclass(frozen=True)
class ParsedProblem:
    name: str
    formulation: BinaryFormulation


def formulate_problem(problem: BinaryProblem) -> ParsedProblem:
    """Translate supported problem definitions into a quantum-ready formulation."""
    if problem.name == "maxcut_triangle":
        formulation = maxcut_to_qubo(3, [(0, 1), (1, 2), (0, 2)])
        return ParsedProblem(problem.name, formulation)
    raise ValueError(f"No formulation adapter registered for: {problem.name}")
