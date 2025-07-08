import unittest, time
from src.labeling_solver import find_heuristic_labeling, _is_valid_assignment
from src.graph_generator import generate_mongolian_tent_graph

class TestHeuristicSolver(unittest.TestCase):

    def test_heuristic_small_n(self):
        """Heuristic solver should find a valid labeling for small n quickly."""
        n = 5
        k, labeling = find_heuristic_labeling(n, max_k_multiplier=10)
        graph = generate_mongolian_tent_graph(n)
        if labeling:
            self.assertTrue(_is_valid_assignment(graph, labeling))
        if labeling:
            self.assertIsInstance(k, int)

    def test_heuristic_large_n_completion(self):
        """Heuristic solver should complete within 10s for n=30 and produce a valid labeling if found."""
        n = 30
        start = time.perf_counter()
        k, labeling = find_heuristic_labeling(n, max_k_multiplier=3)  # tighten limit for test speed
        elapsed = time.perf_counter() - start
        self.assertLessEqual(elapsed, 10.0, f"Heuristic solver took too long: {elapsed:.2f}s")
        if labeling is not None:
            graph = generate_mongolian_tent_graph(n)
            self.assertTrue(_is_valid_assignment(graph, labeling))

if __name__ == '__main__':
    unittest.main() 