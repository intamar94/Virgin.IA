# Virgin.IA

Virgin.IA is an experimental system for **automatic discovery and optimization of quantum circuits** for problems defined by the user.

## Current state

### v0.1 — parameter discovery

Given a circuit family (currently QAOA), Virgin.IA automatically searches its continuous parameters and evaluates the resulting quantum behavior.

### v0.2 — architecture discovery

Virgin.IA now also searches the **structure** of a circuit. Candidate architectures can mutate their gate type, qubit assignment, rotation angle, insertion and deletion of operations. An evolutionary search keeps higher-reward candidates and generates new variants.

The current benchmark is a 3-node MaxCut problem executed entirely on a local simulator.

## Core loop

**problem → candidate circuit → simulation → measurement → evaluation → reward → mutation/optimization → candidate circuit**

The long-term objective is to replace manually selected circuit architectures with an autonomous discovery process.

## Structure

- `virgin_ia/problems.py` — problem definitions and benchmarks
- `virgin_ia/circuits.py` — QAOA circuit generation
- `virgin_ia/architecture.py` — circuit genome, construction and mutations
- `virgin_ia/simulator.py` — local quantum simulation
- `virgin_ia/evaluator.py` — measurement evaluation and reward
- `virgin_ia/discovery.py` — parameter optimization
- `virgin_ia/architectural_search.py` — evolutionary architecture search
- `tests/` — regression tests
- `.github/workflows/ci.yml` — automated test workflow

## Run

```bash
pip install -r requirements.txt
python -m virgin_ia
pytest
```

## Roadmap

1. Parameter discovery — implemented
2. Architecture discovery — implemented as first evolutionary prototype
3. Multi-family algorithm discovery
4. Better multi-objective fitness: solution quality, gates, depth, connectivity and robustness
5. Persistent experiment database and learned search policy
6. Hardware-aware compilation and noise-aware optimization
7. Real quantum hardware backends
8. User-defined problem → automatic formulation → circuit discovery
