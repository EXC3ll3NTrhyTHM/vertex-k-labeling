import unittest, time
from src.graph_generator import generate_mongolian_tent_graph
from src.graph_properties import calculate_lower_bound, get_graph_properties
from src.labeling_solver import greedy_labeling_solver, _is_valid_assignment

class TestHighNGraphs(unittest.TestCase):

    def _expected_counts(self, n: int):
        vertices = 2 * n + 1
        edges = 4 * n - 2  # Based on construction L_n edges = 3n-2, plus n apex edges
        return vertices, edges

    def test_graph_sizes(self):
        """Graph vertex and edge counts should scale correctly for n = 30."""
        n = 30
        graph = generate_mongolian_tent_graph(n)
        vertices_expected, edges_expected = self._expected_counts(n)
        self.assertEqual(len(graph), vertices_expected)
        edge_count, _ = get_graph_properties(graph)
        self.assertEqual(edge_count, edges_expected)

    def test_lower_bound_formula(self):
        """Lower bound calculation should match manual formula for n = 30."""
        n = 30
        edges = 4 * n - 2
        manual_lb = max((edges + 1 + 1) // 2 // 1, n if n > 4 else 4)  # ceiling of (|E|+1)/2 vs Δ (≈ n)
        # We compute ceil((edges+1)/2) manually
        manual_lb = max((edges + 1 + 1) // 2, n)
        self.assertEqual(calculate_lower_bound(n), manual_lb)

    def test_greedy_solver_completes_quickly(self):
        """Greedy solver should finish within 5s for n=30 (may return None)."""
        n = 30
        graph = generate_mongolian_tent_graph(n)
        max_k = calculate_lower_bound(n)
        start = time.perf_counter()
        labeling = greedy_labeling_solver(graph, max_k)
        elapsed = time.perf_counter() - start
        self.assertLessEqual(elapsed, 5.0, msg=f"Greedy solver too slow: {elapsed:.2f}s >5s")
        if labeling:
            self.assertTrue(_is_valid_assignment(graph, labeling))

if __name__ == '__main__':
    unittest.main() 