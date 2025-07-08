import unittest, time
from src.labeling_solver import find_optimal_k_labeling, greedy_k_labeling, is_labeling_valid
from src.graph_generator import create_mongolian_tent_graph
from src.graph_properties import calculate_lower_bound

class TestIntegration(unittest.TestCase):

    def test_backtracking_solver_n3(self):
        """find_minimum_k_labeling should return theoretical lower bound for n=3 (k=6)."""
        expected_k = calculate_lower_bound(3)
        k, labeling = find_optimal_k_labeling(3)
        self.assertEqual(k, expected_k)
        # sanity check
        graph = create_mongolian_tent_graph(3)
        self.assertTrue(is_labeling_valid(graph, labeling))

    def test_upper_bound_respect_n1(self):
        """Solver should not exceed greedy-derived upper bound for n=1."""
        n = 1
        graph = create_mongolian_tent_graph(n)
        lower = calculate_lower_bound(n)
        greedy_labeling = greedy_k_labeling(graph, lower)
        self.assertIsNotNone(greedy_labeling)
        greedy_k = max(greedy_labeling.values())  # type: ignore[arg-type]
        k, _ = find_optimal_k_labeling(n)
        self.assertLessEqual(k, greedy_k)

if __name__ == '__main__':
    unittest.main() 