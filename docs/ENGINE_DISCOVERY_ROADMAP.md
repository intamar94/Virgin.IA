# Virgin.IA — Engine Discovery Roadmap

## Objective
Evolve Virgin.IA from validated quantum examples into an experimental engine that can generate, evaluate and optimize candidate circuits reproducibly.

## Discovery loop
1. Define a problem instance.
2. Encode it into a compatible objective/QUBO representation.
3. Generate candidate circuit structures.
4. Simulate/evaluate candidates.
5. Score quality, depth, gate count, qubits and objective value.
6. Mutate or optimize the best candidates.
7. Repeat with reproducible seeds.
8. Record evidence and distinguish known baselines from novel candidates.

## Quality gates
- Deterministic tests for objective functions.
- Regression tests for known solutions.
- Reproducible experiment metadata.
- No claim of novelty without a baseline comparison.
- Resource metrics recorded for every candidate.

## Vercel boundary
The research engine and tests should be completed independently of Vercel. Deployment is a final integration step only.
