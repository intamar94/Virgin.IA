from dataclasses import dataclass
from typing import Callable

import numpy as np


@dataclass(frozen=True)
class BinaryProblem:
    """Small binary optimization problem used by the v0.1 discovery loop."""

    name: str
    num_variables: int
    objective: Callable[[np.ndarray], float]
    maximize: bool = False

    def score(self, bits: np.ndarray) -> float:
        bits = np.asarray(bits, dtype=int)
        if bits.shape != (self.num_variables,):
            raise ValueError("bits has the wrong shape")
        return float(self.objective(bits))


def maxcut_triangle() -> BinaryProblem:
    """Return a 3-node MaxCut benchmark with a known optimum of 2."""

    edges = ((0, 1), (1, 2), (0, 2))

    def objective(bits: np.ndarray) -> float:
        return sum(int(bits[a] != bits[b]) for a, b in edges)

    return BinaryProblem("maxcut_triangle", 3, objective, maximize=True)
