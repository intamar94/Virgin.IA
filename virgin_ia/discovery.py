from dataclasses import dataclass

import numpy as np
from scipy.optimize import minimize

from .circuits import CircuitSpec, qaoa_maxcut
from .evaluator import Evaluation, evaluate_counts, reward
from .problems import BinaryProblem, maxcut_triangle
from .simulator import QuantumSimulator


@dataclass(frozen=True)
class DiscoveryResult:
    layers: int
    gammas: list[float]
    betas: list[float]
    evaluation: Evaluation
    reward: float


class CircuitDiscovery:
    """First Virgin.IA search engine: optimize QAOA parameters automatically."""

    def __init__(self, simulator: QuantumSimulator | None = None):
        self.simulator = simulator or QuantumSimulator()

    def discover(self, problem: BinaryProblem | None = None, layers: int = 1) -> DiscoveryResult:
        problem = problem or maxcut_triangle()
        spec = CircuitSpec(problem.num_variables, layers)

        def objective(params: np.ndarray) -> float:
            gammas = params[:layers].tolist()
            betas = params[layers:].tolist()
            circuit = qaoa_maxcut(spec, gammas, betas)
            counts = self.simulator.run(circuit)
            evaluation = evaluate_counts(problem, counts, circuit.size())
            return -reward(evaluation)

        initial = np.full(2 * layers, 0.5, dtype=float)
        result = minimize(objective, initial, method="Nelder-Mead", options={"maxiter": 25})
        gammas = result.x[:layers].tolist()
        betas = result.x[layers:].tolist()
        circuit = qaoa_maxcut(spec, gammas, betas)
        counts = self.simulator.run(circuit)
        evaluation = evaluate_counts(problem, counts, circuit.size())
        return DiscoveryResult(layers, gammas, betas, evaluation, reward(evaluation))
