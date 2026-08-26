from dataclasses import dataclass
from typing import Callable

import numpy as np


@dataclass(frozen=True)
class BinaryFormulation:
    """Ising/QUBO-ready representation of a binary objective."""

    num_variables: int
    linear: np.ndarray
    quadratic: np.ndarray
    constant: float = 0.0

    def energy(self, bits: np.ndarray) -> float:
        x = np.asarray(bits, dtype=float)
        return float(self.constant + self.linear @ x + x @ self.quadratic @ x)


def maxcut_to_qubo(num_variables: int, edges: list[tuple[int, int]]) -> BinaryFormulation:
    """Construct a QUBO whose minimum encodes a MaxCut solution."""
    linear = np.zeros(num_variables, dtype=float)
    quadratic = np.zeros((num_variables, num_variables), dtype=float)
    for a, b in edges:
        linear[a] += 1.0
        linear[b] += 1.0
        quadratic[a, b] -= 2.0
    return BinaryFormulation(num_variables, linear, quadratic)
