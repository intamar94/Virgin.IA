from dataclasses import dataclass
from typing import Callable

import numpy as np

from .architecture import Architecture, GateGene


@dataclass(frozen=True)
class Strategy:
    name: str
    generator: Callable[[int], Architecture]


def empty_variational(num_qubits: int) -> Architecture:
    return Architecture(
        num_qubits,
        [GateGene("h", q) for q in range(num_qubits)],
    )


def ring_entangler(num_qubits: int) -> Architecture:
    genes = [GateGene("h", q) for q in range(num_qubits)]
    for q in range(num_qubits):
        genes.append(GateGene("cx", q, (q + 1) % num_qubits))
    return Architecture(num_qubits, genes)


def rx_ring(num_qubits: int) -> Architecture:
    genes = [GateGene("h", q) for q in range(num_qubits)]
    genes.extend(GateGene("rx", q, theta=float(np.pi / 4)) for q in range(num_qubits))
    for q in range(num_qubits - 1):
        genes.append(GateGene("cx", q, q + 1))
    return Architecture(num_qubits, genes)


def default_strategies() -> list[Strategy]:
    return [
        Strategy("empty_variational", empty_variational),
        Strategy("ring_entangler", ring_entangler),
        Strategy("rx_ring", rx_ring),
    ]
