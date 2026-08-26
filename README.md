# Virgin.IA

## Objective

Virgin.IA is an experimental system for **automatically discovering and optimizing quantum circuits** for problems defined by the user.

The target loop is:

**problem → formulation → strategy search → circuit generation → simulation → evaluation → mutation/optimization → learning → final circuit**

## Current state

### v0.1 — parameter discovery

Virgin.IA optimizes parameters of a QAOA circuit on a small MaxCut benchmark.

### v0.2 — architecture discovery

Virgin.IA searches the **circuit structure itself**. Candidate architectures are represented as gate genes and evolved through selection and mutation. Mutations can change gate type, qubit placement, rotation angle, insert gates, or delete gates.

The objective combines solution quality with a circuit-cost penalty, so the search is not simply looking for any high-scoring circuit: it also prefers cheaper candidates.

### v0.3 — meta-strategy discovery

Virgin.IA can now compare different circuit initialization strategies and evolve each strategy independently before selecting the strongest resulting architecture. This is the first layer above individual circuit search: Virgin.IA is beginning to search **how to search**.

## Structure

- `virgin_ia/problems.py` — problem definitions and benchmarks
- `virgin_ia/circuits.py` — QAOA circuit generation
- `virgin_ia/architecture.py` — circuit genome and mutations
- `virgin_ia/architectural_search.py` — evolutionary topology search
- `virgin_ia/strategy.py` — candidate circuit strategies
- `virgin_ia/meta_search.py` — strategy-level search
- `virgin_ia/discovery.py` — parameter optimization
- `virgin_ia/simulator.py` — local quantum simulation
- `virgin_ia/evaluator.py` — measurement evaluation and reward
- `tests/` — regression tests

## Run

```bash
pip install -r requirements.txt
python -m virgin_ia
pytest
```

## Roadmap

1. Parameter optimization — implemented
2. Architecture/gate discovery — implemented
3. Multi-strategy search — initial implementation
4. General problem-to-Hamiltonian/formulation layer
5. Experiment database and learned search policy
6. Hardware-aware cost model and real quantum backends
7. Benchmark against classical and established quantum methods
8. User-defined problem → automatically discovered quantum circuit
