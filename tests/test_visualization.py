import unittest, tempfile
from pathlib import Path

from src.graph_generator import create_mongolian_tent_graph
from src.labeling_solver import find_optimal_k_labeling
from src.visualization import visualize_k_labeling

class TestVisualization(unittest.TestCase):

    def test_visualization_file_created(self):
        n = 3
        k, labeling = find_optimal_k_labeling(n)
        assert labeling is not None, "Solver failed to return labeling"
        graph = create_mongolian_tent_graph(n)
        with tempfile.TemporaryDirectory() as tmp:
            out_file = Path(tmp) / "test.png"
            result_path = visualize_k_labeling(graph, labeling, output=str(out_file))  # type: ignore[arg-type]
            self.assertTrue(result_path.exists())
            self.assertGreater(result_path.stat().st_size, 0)

if __name__ == "__main__":
    unittest.main() 