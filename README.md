# Virgin.IA

## v0.1

Virgin.IA is an experimental system for **automatic discovery and optimization of quantum circuits** for problems defined by the user.

The first milestone deliberately works in simulation. The core loop is:

**problem → circuit generation → simulation → measurement → evaluation → optimization → better circuit**

### Current prototype

v0.1 starts with a small MaxCut benchmark and automatically optimizes the parameters of a QAOA circuit. This establishes the first autonomous search loop before expanding to circuit topology discovery, multiple algorithm families, persistent experiment memory, and real quantum hardware.

### Structure

- `virgin_ia/problems.py` — problem definitions and benchmarks
- `virgin_ia/circuits.py` — candidate circuit generation
- `virgin_ia/simulator.py` — local quantum simulation
- `virgin_ia/evaluator.py` — measurement evaluation and reward
- `virgin_ia/discovery.py` — automatic search/optimization
- `tests/` — regression tests

### Run

```bash
pip install -r requirements.txt
python -m virgin_ia
pytest
```

### Roadmap

1. Parameter optimization — implemented in v0.1
2. Automatic gate/topology mutations
3. Search across multiple circuit families
4. Experiment database and learning from previous runs
5. Hardware abstraction and real quantum backends
6. Benchmark against classical and established quantum methods
