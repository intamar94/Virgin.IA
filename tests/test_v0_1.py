import numpy as np

from virgin_ia.circuits import CircuitSpec, qaoa_maxcut
from virgin_ia.problems import maxcut_triangle


def test_triangle_optimum():
    problem = maxcut_triangle()
    assert problem.score(np.array([0, 1, 0])) == 2


def test_qaoa_circuit_shape():
    circuit = qaoa_maxcut(CircuitSpec(3, 1), [0.5], [0.5])
    assert circuit.num_qubits == 3
    assert circuit.size() > 0
