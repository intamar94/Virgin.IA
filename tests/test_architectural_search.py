from virgin_ia.architectural_search import ArchitectureDiscovery
from virgin_ia.problems import maxcut_triangle


def test_architecture_discovery_returns_valid_candidate():
    result = ArchitectureDiscovery(seed=11).discover(
        maxcut_triangle(), population_size=4, generations=2, initial_depth=4
    )
    assert result.architecture.num_qubits == 3
    assert len(result.architecture.genes) >= 1
    result.architecture.build()
