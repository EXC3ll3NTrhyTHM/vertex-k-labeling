import unittest, time
from src.labeling_solver import find_minimum_k_labeling

class TestPerformanceBenchmarks(unittest.TestCase):

    def _time_solver(self, n: int) -> float:
        start = time.perf_counter()
        _ = find_minimum_k_labeling(n)
        end = time.perf_counter()
        return end - start

    def test_baseline_timing(self):
        """Solver should finish MT_{3,3} and MT_{3,5} within ≤10 s each (dev-machine baseline)."""
        for n in (3, 5):
            elapsed = self._time_solver(n)
            print(f"Performance baseline n={n}: {elapsed:.3f}s")
            self.assertLessEqual(elapsed, 10.0, msg=f"Solver too slow for n={n}: {elapsed:.2f}s > 10s threshold")

    def test_regression_guard(self):
        """Runtime for MT_{3,5} should not exceed 2× runtime for MT_{3,3}."""
        t3 = self._time_solver(3)
        t5 = self._time_solver(5)
        print(f"Regression guard n=3: {t3:.3f}s, n=5: {t5:.3f}s")
        self.assertLessEqual(t5, 2 * t3 + 0.5, msg="Potential performance regression detected (n=5 too slow)")

if __name__ == '__main__':
    unittest.main() 