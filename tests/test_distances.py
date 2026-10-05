import math

from traversal_distance import Graph, compute_traversal_distances, traversal_decisions
from examples.u_path_immersed_tree import make_u_path_immersed_tree


def test_identical_segment_zero():
    g = Graph.from_data({0: (0, 0), 1: (2, 0)}, {0: (0, 1)})
    d = compute_traversal_distances(g, g, tolerance=1e-8)
    assert d.first_to_second == 0.0
    assert d.second_to_first == 0.0
    assert d.symmetric == 0.0
    assert d.complete == 0.0


def test_u_path_immersed_tree_exact_values():
    p, h = make_u_path_immersed_tree()

    d = compute_traversal_distances(p, h, tolerance=1e-6)
    assert abs(d.first_to_second - 8 * math.sqrt(2)) <= 2e-6
    assert abs(d.second_to_first - 12.0) <= 2e-6
    assert abs(d.symmetric - 12.0) <= 2e-6
    assert abs(d.complete - math.sqrt(149)) <= 2e-6

    assert traversal_decisions(p, h, 12.0) == (True, True, False)
    assert traversal_decisions(p, h, 12.3) == (True, True, True)
