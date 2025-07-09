import unittest
from src.graph_generator import generate_circulant_graph
from src.graph_properties import is_regular, compute_diameter

class TestCirculantProperties(unittest.TestCase):

    def test_invalid_n_odd_or_small(self):
        """is_regular should be False and diameter 0 for invalid graphs."""
        graph = generate_circulant_graph(9, 0)
        self.assertFalse(is_regular(graph, 3))
        self.assertEqual(compute_diameter(graph), 0)

    def test_even_n_regular_and_diameter(self):
        """For n=12, degree=6 and diameter=2."""
        n = 12
        graph = generate_circulant_graph(n, 0)
        r = n - 6
        self.assertTrue(is_regular(graph, r))
        self.assertEqual(compute_diameter(graph), 2)

if __name__ == '__main__':
    unittest.main() 