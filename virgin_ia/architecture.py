from dataclasses import dataclass
import random

from qiskit import QuantumCircuit


@dataclass
class GateGene:
    gate: str
    q0: int
    q1: int | None = None
    theta: float = 0.0


@dataclass
class Architecture:
    num_qubits: int
    genes: list[GateGene]

    def copy(self) -> "Architecture":
        return Architecture(
            self.num_qubits,
            [GateGene(g.gate, g.q0, g.q1, g.theta) for g in self.genes],
        )

    @property
    def depth_proxy(self) -> int:
        return len(self.genes)

    def build(self) -> QuantumCircuit:
        qc = QuantumCircuit(self.num_qubits)
        for gene in self.genes:
            if gene.gate == "h":
                qc.h(gene.q0)
            elif gene.gate == "rx":
                qc.rx(gene.theta, gene.q0)
            elif gene.gate == "rz":
                qc.rz(gene.theta, gene.q0)
            elif gene.gate == "cx":
                if gene.q1 is None or gene.q0 == gene.q1:
                    raise ValueError("CX requires two distinct qubits")
                qc.cx(gene.q0, gene.q1)
            else:
                raise ValueError(f"Unsupported gate: {gene.gate}")
        return qc


def random_architecture(num_qubits: int, depth: int, rng: random.Random) -> Architecture:
    genes: list[GateGene] = []
    for _ in range(depth):
        gate = rng.choice(("h", "rx", "rz", "cx"))
        q0 = rng.randrange(num_qubits)
        if gate == "cx":
            q1 = rng.randrange(num_qubits - 1)
            if q1 >= q0:
                q1 += 1
            genes.append(GateGene(gate, q0, q1, 0.0))
        elif gate == "h":
            genes.append(GateGene(gate, q0, None, 0.0))
        else:
            genes.append(GateGene(gate, q0, None, rng.uniform(-3.14159, 3.14159)))
    return Architecture(num_qubits, genes)


def mutate(architecture: Architecture, rng: random.Random) -> Architecture:
    child = architecture.copy()
    if not child.genes:
        return child
    index = rng.randrange(len(child.genes))
    gene = child.genes[index]
    mutation = rng.choice(("gate", "qubit", "theta", "insert", "delete"))
    if mutation == "gate":
        replacement = rng.choice(("h", "rx", "rz", "cx"))
        if replacement == "cx" and child.num_qubits > 1:
            q0 = rng.randrange(child.num_qubits)
            q1 = rng.randrange(child.num_qubits - 1)
            if q1 >= q0:
                q1 += 1
            child.genes[index] = GateGene("cx", q0, q1, 0.0)
        elif replacement == "h":
            child.genes[index] = GateGene("h", gene.q0)
        else:
            child.genes[index] = GateGene(replacement, gene.q0, None, rng.uniform(-3.14159, 3.14159))
    elif mutation == "qubit":
        gene.q0 = rng.randrange(child.num_qubits)
        if gene.gate == "cx" and child.num_qubits > 1:
            q1 = rng.randrange(child.num_qubits - 1)
            if q1 >= gene.q0:
                q1 += 1
            gene.q1 = q1
    elif mutation == "theta" and gene.gate in {"rx", "rz"}:
        gene.theta += rng.uniform(-0.5, 0.5)
    elif mutation == "insert" and len(child.genes) < 12:
        extra = random_architecture(child.num_qubits, 1, rng).genes[0]
        child.genes.insert(index, extra)
    elif mutation == "delete" and len(child.genes) > 1:
        child.genes.pop(index)
    return child
