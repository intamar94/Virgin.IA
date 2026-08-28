from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import json
from pathlib import Path


@dataclass(frozen=True)
class ExperimentRecord:
    problem: str
    strategy: str
    reward: float
    success_probability: float
    best_score: float
    circuit_depth: int
    created_at: str


class ExperimentStore:
    """Small append-only local memory for discovery experiments."""

    def __init__(self, path: str = "artifacts/experiments.jsonl"):
        self.path = Path(path)

    def record(self, problem: str, strategy: str, result) -> ExperimentRecord:
        evaluation = result.result.evaluation if hasattr(result, "result") else result.evaluation
        reward = result.result.reward if hasattr(result, "result") else result.reward
        strategy_name = result.strategy if hasattr(result, "strategy") else "parameter_search"
        record = ExperimentRecord(
            problem=problem,
            strategy=strategy_name,
            reward=float(reward),
            success_probability=float(evaluation.success_probability),
            best_score=float(evaluation.best_score),
            circuit_depth=int(evaluation.circuit_depth),
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(asdict(record)) + "\n")
        return record
