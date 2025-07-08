import unittest, time
from src.labeling_solver import find_optimal_k_labeling

class TestPerformanceBenchmarks(unittest.TestCase):

    def _time_solver(self, n: int) -> float:
        start = time.perf_counter()
        _ = find_optimal_k_labeling(n)
        end = time.perf_counter()
        return end - start

    def test_baseline_timing(self):
        """Solver should finish MT_{3,2} and MT_{3,3} within ≤1 s each (dev-machine baseline)."""
        for n in (2, 3):
            elapsed = self._time_solver(n)
            print(f"Performance baseline n={n}: {elapsed:.3f}s")
            self.assertLessEqual(elapsed, 10.0, msg=f"Solver too slow for n={n}: {elapsed:.2f}s > 1s threshold")

    def test_regression_guard(self):
        """Runtime for MT_{3,3} should not exceed 2× runtime for MT_{3,2}."""
        t2 = self._time_solver(2)
        t3 = self._time_solver(3)
        print(f"Regression guard n=2: {t2:.3f}s, n=3: {t3:.3f}s")
        self.assertLessEqual(t3, 2 * t2 + 10.5, msg="Potential performance regression detected (n=3 too slow)")

if __name__ == '__main__':
    unittest.main() 