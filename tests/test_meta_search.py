from virgin_ia.meta_search import MetaSearch
from virgin_ia.problems import maxcut_triangle


def test_meta_search_returns_valid_strategy():
    result = MetaSearch().discover(maxcut_triangle(), generations=1)
    assert result.strategy
    assert result.result.architecture.num_qubits == 3
    assert result.result.evaluation.best_score >= 0
