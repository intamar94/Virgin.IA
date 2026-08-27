from dataclasses import dataclass

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
        if x.shape != (self.num_variables,):
            raise ValueError(
                f"bits must have shape ({self.num_variables},), got {x.shape}"
            )
        return float(self.constant + self.linear @ x + x @ self.quadratic @ x)


def maxcut_to_qubo(num_variables: int, edges: list[tuple[int, int]]) -> BinaryFormulation:
    """Construct a QUBO whose minimum encodes a MaxCut solution.

    For binary variables x in {0,1}, each edge contributes
    ``-(x_a + x_b - 2*x_a*x_b)``. Therefore minimizing the energy is
    equivalent to maximizing the number of cut edges.
    """
    if num_variables < 1:
        raise ValueError("num_variables must be positive")

    linear = np.zeros(num_variables, dtype=float)
    quadratic = np.zeros((num_variables, num_variables), dtype=float)

    for a, b in edges:
        if a == b:
            raise ValueError("self-loops are not valid MaxCut edges")
        if not (0 <= a < num_variables and 0 <= b < num_variables):
            raise ValueError(f"edge ({a}, {b}) contains an invalid variable index")
        linear[a] -= 1.0
        linear[b] -= 1.0
        quadratic[a, b] += 2.0

    return BinaryFormulation(num_variables, linear, quadratic)
