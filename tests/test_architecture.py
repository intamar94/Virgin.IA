import random

from virgin_ia.architecture import Architecture, GateGene, mutate, random_architecture


def test_architecture_builds():
    architecture = Architecture(
        2,
        [GateGene("h", 0), GateGene("cx", 0, 1), GateGene("rx", 1, theta=0.3)],
    )
    circuit = architecture.build()
    assert circuit.num_qubits == 2
    assert circuit.size() == 3


def test_mutation_preserves_valid_cx():
    rng = random.Random(3)
    architecture = random_architecture(3, 5, rng)
    child = mutate(architecture, rng)
    child.build()
