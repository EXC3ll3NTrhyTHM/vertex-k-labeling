import unittest
from src.graph_properties import get_graph_properties, calculate_lower_bound
from src.graph_generator import generate_ladder_graph, generate_mongolian_tent_graph

class TestGraphProperties(unittest.TestCase):

    def test_get_graph_properties_empty(self):
        """Test with an empty graph"""
        edge_count, max_degree = get_graph_properties({})
        self.assertEqual(edge_count, 0)
        self.assertEqual(max_degree, 0)

    def test_get_graph_properties_ladder_graph(self):
        """Test with a ladder graph L_3"""
        graph = generate_ladder_graph(3)
        # L_3 has 7 edges and max degree of 3 (for vertices (1,2) and (2,2))
        edge_count, max_degree = get_graph_properties(graph)
        self.assertEqual(edge_count, 7)
        self.assertEqual(max_degree, 3)

    def test_get_graph_properties_mongolian_tent_graph(self):
        """Test with a Mongolian Tent graph MT_3,3"""
        graph = generate_mongolian_tent_graph(3)
        # MT_3,3 has 10 edges (7 from L_3 + 3 to apex)
        # Max degree is 4 for vertex (1,2)
        edge_count, max_degree = get_graph_properties(graph)
        self.assertEqual(edge_count, 10)
        self.assertEqual(max_degree, 4)

    def test_calculate_lower_bound_n0(self):
        """Test lower bound calculation for n=0"""
        self.assertEqual(calculate_lower_bound(0), 0)

    def test_calculate_lower_bound_n1(self):
        """Test lower bound calculation for n=1"""
        # For MT_3,1: |E|=2, d=2. k >= max(ceil(3/2), 2) = max(2,2) = 2
        self.assertEqual(calculate_lower_bound(1), 2)

    def test_calculate_lower_bound_n3(self):
        """Test lower bound calculation for n=3"""
        # For MT_3,3: |E|=10, d=4. k >= max(ceil(11/2), 4) = max(6,4) = 6
        self.assertEqual(calculate_lower_bound(3), 6)

    def test_calculate_lower_bound_n5(self):
        """Test lower bound calculation for n=5"""
        # For MT_3,5: |E|=18, d=5. k >= max(ceil(19/2), 5) = max(10,5) = 10
        self.assertEqual(calculate_lower_bound(5), 10)

if __name__ == '__main__':
    unittest.main() 