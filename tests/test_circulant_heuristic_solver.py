import unittest, time
from src.labeling_solver import find_feasible_k_labeling, is_labeling_valid
from src.graph_generator import generate_circulant_graph

class TestCirculantHeuristicSolver(unittest.TestCase):

    def test_circulant_heuristic_small_n(self):
        """Heuristic solver should find a valid labeling for small circulant graphs quickly."""
        n = 6
        r = 1 # r is ignored in current generate_circulant_graph, but 1 is a valid generator
        k, labeling = find_feasible_k_labeling("circulant", {"n": n, "r": r}, max_k_multiplier=20)
        graph = generate_circulant_graph(n, r)
        self.assertIsNotNone(labeling, f"No labeling found for C({n}, {r})")
        if labeling:
            self.assertTrue(is_labeling_valid(graph, labeling), f"Invalid labeling for C({n}, {r})")
            self.assertIsInstance(k, int)

    def test_circulant_heuristic_medium_n(self):
        """Heuristic solver should find a valid labeling for medium circulant graphs."""
        n = 10
        r = 3
        k, labeling = find_feasible_k_labeling("circulant", {"n": n, "r": r}, max_k_multiplier=5)
        graph = generate_circulant_graph(n, r)
        self.assertIsNotNone(labeling, f"No labeling found for C({n}, {r})")
        if labeling:
            self.assertTrue(is_labeling_valid(graph, labeling), f"Invalid labeling for C({n}, {r})")
            self.assertIsInstance(k, int)

    def test_circulant_heuristic_large_n_completion(self):
        """Heuristic solver should complete within a reasonable time for large circulant graphs."""
        n = 20
        r = 7
        start = time.perf_counter()
        k, labeling = find_feasible_k_labeling("circulant", {"n": n, "r": r}, max_k_multiplier=3)  # tighten limit for test speed
        elapsed = time.perf_counter() - start
        self.assertLessEqual(elapsed, 300.0, f"Heuristic solver took too long: {elapsed:.2f}s")
        if labeling is not None:
            graph = generate_circulant_graph(n, r)
            self.assertTrue(is_labeling_valid(graph, labeling), f"Invalid labeling for C({n}, {r})")

if __name__ == '__main__':
    unittest.main()