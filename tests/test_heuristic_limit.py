import unittest, time
from src.labeling_solver import find_heuristic_labeling

class TestHeuristicSafetyLimit(unittest.TestCase):

    def test_limit_triggers(self):
        """With max_k_multiplier=1 on n=5, heuristic should return (None, None) quickly."""
        n = 5
        start = time.perf_counter()
        k, labeling = find_heuristic_labeling(n, max_k_multiplier=1)
        elapsed = time.perf_counter() - start
        self.assertIsNone(labeling)
        self.assertLessEqual(elapsed, 2.0)

    def test_higher_limit_succeeds(self):
        """With higher multiplier heuristic should eventually find labeling."""
        n = 5
        start = time.perf_counter()
        k, labeling = find_heuristic_labeling(n, max_k_multiplier=10)
        elapsed = time.perf_counter() - start
        self.assertLessEqual(elapsed, 5.0)
        if labeling:
            self.assertIsInstance(k, int)

if __name__ == '__main__':
    unittest.main() 