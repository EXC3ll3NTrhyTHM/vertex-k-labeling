import unittest, os, tempfile
from pathlib import Path

try:
    from graphviz.backend import ExecutableNotFound
    from graphviz import Digraph
    _GRAPHVIZ_BIN = True
except Exception:
    _GRAPHVIZ_BIN = False

from src.graph_generator import generate_mongolian_tent_graph
from src.labeling_solver import find_minimum_k_labeling
from src.visualization import visualize_labeling

@unittest.skipUnless(_GRAPHVIZ_BIN, "Graphviz binaries not available")
class TestVisualization(unittest.TestCase):

    def test_visualization_file_created(self):
        n = 3
        k, labeling = find_minimum_k_labeling(n)
        graph = generate_mongolian_tent_graph(n)
        with tempfile.TemporaryDirectory() as tmp:
            out_file = Path(tmp) / "test.png"
            result_path = visualize_labeling(graph, labeling, output=str(out_file))
            self.assertTrue(result_path.exists())
            self.assertGreater(result_path.stat().st_size, 0)

if __name__ == "__main__":
    unittest.main() 