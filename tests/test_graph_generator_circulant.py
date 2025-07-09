import unittest
import collections
from src.graph_generator import generate_circulant_graph

class TestCirculantGenerator(unittest.TestCase):

    def test_invalid_n_odd_or_small(self):
        """generate_circulant_graph returns empty graph for odd or too-small n."""
        self.assertEqual(generate_circulant_graph(9, 0), collections.defaultdict(list))  # odd n
        self.assertEqual(generate_circulant_graph(5, 0), collections.defaultdict(list))  # too small for removal

    def test_even_n_degree_and_edge_count(self):
        """Test circulant graph for even n: degree = n-6, edge count = n*(n-6)/2."""
        n = 12
        graph = generate_circulant_graph(n, 0)
        degree = n - 6
        # vertex count
        self.assertEqual(len(graph), n)
        # degree of each vertex
        self.assertTrue(all(len(neighbors) == degree for neighbors in graph.values()))
        # total edges
        total_edges = sum(len(v) for v in graph.values()) // 2
        self.assertEqual(total_edges, n * degree // 2)

if __name__ == '__main__':
    unittest.main() 