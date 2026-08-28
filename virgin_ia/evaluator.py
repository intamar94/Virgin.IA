from dataclasses import dataclass

import numpy as np

from .problems import BinaryProblem


@dataclass(frozen=True)
class Evaluation:
    best_score: float
    expected_score: float
    circuit_cost: int
    counts: dict[str, int]
    success_probability: float


def evaluate_counts(problem: BinaryProblem, counts: dict[str, int], circuit_cost: int) -> Evaluation:
    total = sum(counts.values())
    if not total:
        raise ValueError("No measurement results")

    scored_counts: list[tuple[float, int]] = []
    weighted = 0.0
    for bitstring, count in counts.items():
        bits = np.array([int(x) for x in reversed(bitstring)], dtype=int)
        score = problem.score(bits)
        scored_counts.append((score, count))
        weighted += score * count

    expected = weighted / total
    best = max(score for score, _ in scored_counts) if problem.maximize else min(score for score, _ in scored_counts)
    optimal_shots = sum(count for score, count in scored_counts if score == best)
    success_probability = optimal_shots / total
    return Evaluation(best, expected, circuit_cost, counts, success_probability)


def reward(evaluation: Evaluation) -> float:
    """Reward solution quality while penalizing circuit size."""
    return evaluation.expected_score - 0.01 * evaluation.circuit_cost
