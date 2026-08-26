from .discovery import CircuitDiscovery


if __name__ == "__main__":
    result = CircuitDiscovery().discover()
    print("Virgin.IA v0.1")
    print(f"layers: {result.layers}")
    print(f"gammas: {result.gammas}")
    print(f"betas: {result.betas}")
    print(f"best score: {result.evaluation.best_score}")
    print(f"expected score: {result.evaluation.expected_score:.4f}")
    print(f"reward: {result.reward:.4f}")
