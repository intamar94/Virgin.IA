import numpy as np

from virgin_ia.formulation import maxcut_to_qubo
from virgin_ia.problem_parser import formulate_problem
from virgin_ia.problems import maxcut_triangle


def test_maxcut_formulation_matches_cut_energy():
    formulation = maxcut_to_qubo(3, [(0, 1), (1, 2), (0, 2)])
    bits = np.array([0, 1, 0])
    assert formulation.energy(bits) == -2.0


def test_problem_parser():
    parsed = formulate_problem(maxcut_triangle())
    assert parsed.formulation.num_variables == 3
