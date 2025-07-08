import unittest, time
from src.graph_generator import create_mongolian_tent_graph
from src.graph_properties import calculate_lower_bound, calculate_graph_metrics
from src.labeling_solver import greedy_k_labeling, is_labeling_valid

class TestHighNGraphs(unittest.TestCase):

    def _expected_counts(self, n: int):
        vertices = 3 * n + 1  # 3 rows of n vertices each, plus 1 apex vertex
        edges = 6 * n - 3     # Correct formula for Mongolian Tent graph edges
        return vertices, edges

    def test_graph_sizes(self):
        """Graph vertex and edge counts should scale correctly for n = 30."""
        n = 30
        graph = create_mongolian_tent_graph(n)
        vertices_expected, edges_expected = self._expected_counts(n)
        self.assertEqual(len(graph), vertices_expected)
        edge_count, _ = calculate_graph_metrics(graph)
        self.assertEqual(edge_count, edges_expected)

    def test_lower_bound_formula(self):
        """Lower bound calculation should match manual formula for n = 30."""
        n = 30
        edges = 6 * n - 3  # Use correct edge count formula
        # Lower bound formula: max(ceil((|E|+1)/2), max_degree)
        # For Mongolian Tent graphs, max_degree is n (apex vertex connected to top row)
        import math
        manual_lb = max(math.ceil((edges + 1) / 2), n)
        self.assertEqual(calculate_lower_bound(n), manual_lb)

    def test_greedy_solver_completes_quickly(self):
        """Greedy solver should finish within 5s for n=30 (may return None)."""
        n = 30
        graph = create_mongolian_tent_graph(n)
        max_k = calculate_lower_bound(n)
        start = time.perf_counter()
        labeling = greedy_k_labeling(graph, max_k)
        elapsed = time.perf_counter() - start
        self.assertLessEqual(elapsed, 5.0, msg=f"Greedy solver too slow: {elapsed:.2f}s >5s")
        if labeling:
            self.assertTrue(is_labeling_valid(graph, labeling))

if __name__ == '__main__':
    unittest.main() 