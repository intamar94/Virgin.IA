from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


class QuantumSimulator:
    """Local simulator backend for Virgin.IA v0.1."""

    def __init__(self, shots: int = 2048):
        self.shots = shots
        self.backend = AerSimulator()

    def run(self, circuit: QuantumCircuit) -> dict[str, int]:
        measured = circuit.copy()
        measured.measure_all()
        result = self.backend.run(measured, shots=self.shots).result()
        return dict(result.get_counts())
