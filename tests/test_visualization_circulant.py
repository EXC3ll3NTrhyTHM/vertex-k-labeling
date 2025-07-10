import unittest, tempfile
from pathlib import Path

from src.graph_generator import generate_circulant_graph
from src.visualization import visualize_k_labeling

class TestVisualizationCirculant(unittest.TestCase):

    def test_visualization_circulant_file_created(self):
        n, r = 8, 3
        graph = generate_circulant_graph(n, r)
        # simple labeling: label all vertices as 1 (validate=False by default)
        labeling = {v: 1 for v in graph}
        with tempfile.TemporaryDirectory() as tmp:
            out_file = Path(tmp) / "circ.png"
            result_path = visualize_k_labeling(graph, labeling, output=str(out_file), shaped=False)
            self.assertTrue(result_path.exists())
            self.assertGreater(result_path.stat().st_size, 0)

if __name__ == "__main__":
    unittest.main() 