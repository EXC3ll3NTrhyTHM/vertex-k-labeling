import unittest
from src.labeling_solver import find_optimal_k_labeling, is_labeling_valid
from src.labeling_solver import find_feasible_k_labeling
from src.graph_generator import create_mongolian_tent_graph


class TestEdgeWeightsUniqueness(unittest.TestCase):
    """Ensure that solver-produced labelings contain no duplicate edge weights."""

    @staticmethod
    def _compute_edge_weights(graph, labeling):
        """Return a list of all edge weights treating the graph as undirected (no duplicates)."""
        weights = []
        seen_edges = set()
        for source, neighbours in graph.items():
            if source not in labeling:
                continue
            for target in neighbours:
                if target in labeling:
                    # Use frozenset to identify undirected edge uniquely
                    edge_key = frozenset((source, target))
                    if edge_key in seen_edges:
                        continue
                    seen_edges.add(edge_key)
                    weights.append(labeling[source] + labeling[target])
        return weights

    def test_solver_output_has_unique_edge_weights(self):
        """Run the exact solver for small n and confirm edge weights are unique."""
        # Test a range of n where exact backtracking remains tractable.
        for n in range(1, 6):  # n = 1 .. 5
            with self.subTest(n=n):
                k, labeling_opt = find_optimal_k_labeling(n)
                self.assertIsNotNone(labeling_opt, f"Solver did not return a labeling for n={n}")

                from typing import cast, Any, Dict  # local import for clarity
                labeling = cast(Dict[Any, int], labeling_opt)

                graph = create_mongolian_tent_graph(n)
                # Quick sanity via existing helper
                self.assertTrue(is_labeling_valid(graph, labeling))

                # Explicit duplicate-weight assertion
                weights = self._compute_edge_weights(graph, labeling)
                self.assertEqual(len(weights), len(set(weights)), f"Duplicate edge weights detected for n={n}")

    def test_heuristic_solver_output_has_unique_edge_weights(self):
        """Run heuristic solvers (accurate & fast) for small n and confirm edge weights are unique."""
        from typing import cast, Any, Dict  # local import to avoid top-level pollution

        # Broader range for heuristic solvers (they scale better).
        for algorithm in ("accurate", "fast"):
            for n in range(1, 11):  # n = 1 .. 10
                with self.subTest(algorithm=algorithm, n=n):
                    k_label = find_feasible_k_labeling(n, algorithm=algorithm)
                    self.assertIsNotNone(k_label[1], f"Heuristic ({algorithm}) did not find labeling for n={n}")

                    labeling = cast(Dict[Any, int], k_label[1])
                    graph = create_mongolian_tent_graph(n)
                    self.assertTrue(is_labeling_valid(graph, labeling), f"Heuristic ({algorithm}) produced invalid labeling for n={n}")

                    weights = self._compute_edge_weights(graph, labeling)
                    self.assertEqual(
                        len(weights),
                        len(set(weights)),
                        f"Duplicate edge weights detected for heuristic ({algorithm}) n={n}",
                    )


if __name__ == "__main__":
    unittest.main() 