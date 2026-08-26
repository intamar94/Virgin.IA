from dataclasses import dataclass

import numpy as np

from .problems import BinaryProblem


@dataclass(frozen=True)
class Evaluation:
    best_score: float
    expected_score: float
    circuit_cost: int
    counts: dict[str, int]


def evaluate_counts(problem: BinaryProblem, counts: dict[str, int], circuit_cost: int) -> Evaluation:
    total = sum(counts.values())
    if not total:
        raise ValueError("No measurement results")
    scores = []
    weighted = 0.0
    for bitstring, count in counts.items():
        bits = np.array([int(x) for x in reversed(bitstring)], dtype=int)
        score = problem.score(bits)
        scores.append(score)
        weighted += score * count
    expected = weighted / total
    best = max(scores) if problem.maximize else min(scores)
    return Evaluation(best, expected, circuit_cost, counts)


def reward(evaluation: Evaluation) -> float:
    """Reward quality while penalizing circuit size."""
    return evaluation.expected_score - 0.01 * evaluation.circuit_cost
