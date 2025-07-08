import unittest, tempfile
from pathlib import Path
import shutil

try:
    from graphviz import Digraph
    _GRAPHVIZ_BIN = shutil.which("dot") is not None
except ImportError:
    _GRAPHVIZ_BIN = False

from src.graph_generator import generate_mongolian_tent_graph
from src.labeling_solver import find_optimal_k_labeling
from src.visualization import visualize_labeling

@unittest.skipUnless(_GRAPHVIZ_BIN, "Graphviz system binary not available")
class TestVisualization(unittest.TestCase):

    def test_visualization_file_created(self):
        n = 3
        k, labeling = find_optimal_k_labeling(n)
        graph = generate_mongolian_tent_graph(n)
        with tempfile.TemporaryDirectory() as tmp:
            out_file = Path(tmp) / "test.png"
            result_path = visualize_labeling(graph, labeling, output=str(out_file))
            self.assertTrue(result_path.exists())
            self.assertGreater(result_path.stat().st_size, 0)

if __name__ == "__main__":
    unittest.main() 