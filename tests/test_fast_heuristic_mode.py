from __future__ import annotations
import time, unittest

from src.labeling_solver import find_feasible_k_labeling, is_labeling_valid
from src.graph_generator import create_mongolian_tent_graph
from src.graph_properties import calculate_lower_bound


class TestFastHeuristicMode(unittest.TestCase):
    """Unit tests for the new fast heuristic mode in ``find_feasible_k_labeling``."""

    def test_fast_mode_valid_small_n(self):
        """Fast mode should quickly find a valid labeling for small n."""
        n = 5
        k, labeling = find_feasible_k_labeling(n, algorithm="fast", max_k_multiplier=10)

        # Ensure a solution was found
        self.assertIsNotNone(labeling, "Fast mode failed to find a labeling for small n")
        self.assertIsNotNone(k, "k should not be None when labeling is found")

        if labeling is None or k is None:
            return  # Safety, though tests above already ensure this

        graph = create_mongolian_tent_graph(n)
        self.assertTrue(is_labeling_valid(graph, labeling))
        self.assertGreaterEqual(k, calculate_lower_bound(n))

    def test_fast_mode_speed_medium_n(self):
        """Fast mode should complete within a reasonable time for medium n."""
        n = 12
        start = time.perf_counter()
        k, labeling = find_feasible_k_labeling(n, algorithm="fast", max_k_multiplier=5)
        elapsed = time.perf_counter() - start

        # Expect completion well under 10 seconds on dev machine.
        self.assertLessEqual(elapsed, 10.0, f"Fast mode took too long: {elapsed:.2f}s")

        if labeling:
            graph = create_mongolian_tent_graph(n)
            self.assertTrue(is_labeling_valid(graph, labeling))


if __name__ == "__main__":
    unittest.main() 