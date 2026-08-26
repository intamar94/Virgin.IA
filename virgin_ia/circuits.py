from dataclasses import dataclass

from qiskit import QuantumCircuit


@dataclass(frozen=True)
class CircuitSpec:
    """Compact representation of a candidate circuit architecture."""

    num_qubits: int
    layers: int


def qaoa_maxcut(spec: CircuitSpec, gammas: list[float], betas: list[float]) -> QuantumCircuit:
    """Build a QAOA circuit for the triangle MaxCut benchmark."""
    if len(gammas) != spec.layers or len(betas) != spec.layers:
        raise ValueError("Parameter count must equal the number of layers")
    qc = QuantumCircuit(spec.num_qubits)
    qc.h(range(spec.num_qubits))
    edges = ((0, 1), (1, 2), (0, 2))
    for layer in range(spec.layers):
        for a, b in edges:
            qc.cx(a, b)
            qc.rz(2 * gammas[layer], b)
            qc.cx(a, b)
        for q in range(spec.num_qubits):
            qc.rx(2 * betas[layer], q)
    return qc
