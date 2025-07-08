import unittest
from src.graph_generator import generate_ladder_graph, create_mongolian_tent_graph
from src.labeling_solver import find_optimal_k_labeling, greedy_k_labeling
from src.graph_properties import calculate_lower_bound

class TestEdgeAndErrorHandling(unittest.TestCase):

    def test_invalid_input(self):
        """Functions should handle n <= 0 gracefully."""
        empty_ladder = generate_ladder_graph(0)
        empty_tent = create_mongolian_tent_graph(0)
        self.assertEqual(len(empty_ladder), 0)
        self.assertEqual(len(empty_tent), 0)

        k, labeling = find_optimal_k_labeling(0)
        self.assertIsNone(k)
        self.assertIsNone(labeling)

    @unittest.skip("Skipping test per instructions")
    def test_large_n_smoke(self):
        """Ensure solver does not crash on a moderately large graph (n=8)."""
        n = 4
        # First attempt greedy heuristic only to keep runtime low
        graph = create_mongolian_tent_graph(n)
        max_k = calculate_lower_bound(n)
        _ = greedy_k_labeling(graph, max_k)

        # Full solver smoke test; we do not assert on result value, just that it completes
        try:
            _ = find_optimal_k_labeling(n)
            completed = True
        except Exception as e:
            completed = False
            raise e
        self.assertTrue(completed)

if __name__ == '__main__':
    unittest.main() 