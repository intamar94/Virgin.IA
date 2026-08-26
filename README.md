# Virgin.IA

## Objective

Virgin.IA is an experimental system for **automatically discovering and optimizing quantum circuits** for problems defined by the user.

The target loop is:

**problem → formulation → strategy search → circuit generation → simulation → evaluation → mutation/optimization → learning → final circuit**

## Current state

### v0.1 — parameter discovery
Virgin.IA optimizes parameters of a QAOA circuit on a small MaxCut benchmark.

### v0.2 — architecture discovery
Virgin.IA searches the circuit structure itself. Candidate architectures are represented as gate genes and evolved through selection and mutation.

### v0.3 — meta-strategy discovery
Virgin.IA compares different circuit initialization strategies and evolves each strategy independently before selecting the strongest result.

### v0.4 — formulation layer
Virgin.IA now has a first problem-to-quantum formulation layer. Supported binary problems can be translated into a QUBO-style representation, creating the bridge between a user-defined objective and the circuit-discovery engine.

## Structure

- `virgin_ia/problems.py` — problem definitions and benchmarks
- `virgin_ia/formulation.py` — binary/QUBO formulation
- `virgin_ia/problem_parser.py` — problem-to-formulation adapters
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
4. Problem formulation layer — initial implementation
5. Automatic QUBO/Ising → Hamiltonian conversion
6. Experiment database and learned search policy
7. Hardware-aware cost model and real quantum backends
8. User-defined problem → automatically discovered quantum circuit
