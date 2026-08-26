from .architectural_search import ArchitectureDiscovery
from .discovery import CircuitDiscovery
from .problems import maxcut_triangle


if __name__ == "__main__":
    problem = maxcut_triangle()

    parameter_result = CircuitDiscovery().discover(problem, layers=1)
    print("Virgin.IA v0.1 — parameter discovery")
    print(f"best score: {parameter_result.evaluation.best_score}")
    print(f"expected score: {parameter_result.evaluation.expected_score:.4f}")
    print(f"reward: {parameter_result.reward:.4f}")

    architecture_result = ArchitectureDiscovery().discover(
        problem,
        population_size=8,
        generations=6,
        initial_depth=6,
    )
    print("Virgin.IA v0.2 — architecture discovery")
    print(f"gates: {len(architecture_result.architecture.genes)}")
    print(f"best score: {architecture_result.evaluation.best_score}")
    print(f"expected score: {architecture_result.evaluation.expected_score:.4f}")
    print(f"reward: {architecture_result.reward:.4f}")
    print("architecture:")
    for gene in architecture_result.architecture.genes:
        print(f"  {gene}")
