import unittest
import collections
from src.graph_generator import generate_ladder_graph, generate_mongolian_tent_graph

class TestGraphGenerator(unittest.TestCase):

    def test_generate_ladder_graph_n0(self):
        """Test ladder graph with n=0"""
        # For n=0, we expect an empty graph.
        graph = generate_ladder_graph(0)
        self.assertEqual(graph, collections.defaultdict(list))

    def test_generate_ladder_graph_n1(self):
        """Test ladder graph with n=1"""
        # For n=1, the ladder graph has two vertices (1,1) and (2,1) connected by a single edge.
        graph = generate_ladder_graph(1)
        expected_graph = collections.defaultdict(list)
        expected_graph[(1, 1)].append((2, 1))
        expected_graph[(2, 1)].append((1, 1))
        self.assertEqual(dict(graph), dict(expected_graph))

    def test_generate_ladder_graph_n3(self):
        """Test ladder graph with n=3"""
        # For n=3, the ladder graph has 3*3=9 vertices.
        # Total edges = 5n-3 = 12 ⇒ total degree = 24.
        graph = generate_ladder_graph(3)
        self.assertEqual(len(graph), 9)  # 3*n vertices
        self.assertEqual(sum(len(v) for v in graph.values()), 24)  # 2 * (5n-3) edges
        # Check some specific edges to ensure connectivity.
        self.assertIn((1, 2), graph[(1, 1)])
        self.assertIn((2, 1), graph[(1, 1)])
        self.assertIn((1, 3), graph[(1, 2)])
        self.assertIn((2, 2), graph[(1, 2)])
        self.assertIn((2, 3), graph[(2, 2)])

    def test_generate_mongolian_tent_graph_n0(self):
        """Test Mongolian Tent graph with n=0"""
        # For n=0, we expect an empty graph.
        graph = generate_mongolian_tent_graph(0)
        self.assertEqual(graph, collections.defaultdict(list))

    def test_generate_mongolian_tent_graph_n1(self):
        """Test Mongolian Tent graph with n=1"""
        # For n=1, ladder L_1 has 3 vertices plus apex 'x'.
        graph = generate_mongolian_tent_graph(1)
        expected_graph = collections.defaultdict(list)
        expected_graph[(1, 1)].extend([(2, 1), 'x'])
        expected_graph[(2, 1)].extend([(1, 1), (3,1)])
        expected_graph[(3,1)].append((2,1))
        
        # Convert to dict and sort lists for comparison.
        # We convert values to strings to handle mixed types (tuples and strings) during sorting.
        graph_dict = {str(k): sorted(map(str, v)) for k, v in dict(graph).items()}
        expected_dict = {str(k): sorted(map(str, v)) for k, v in dict(expected_graph).items()}
        
        self.assertEqual(graph_dict, expected_dict)

    def test_generate_mongolian_tent_graph_n2(self):
        """Test Mongolian Tent graph with n=2"""
        # For n=2, vertices = 3*2+1 = 7.
        # Edges = 6n-3 = 9 ⇒ total degree = 18.
        graph = generate_mongolian_tent_graph(2)
        self.assertEqual(len(graph), 7)
        self.assertEqual(sum(len(v) for v in graph.values()), 18)
        # Check that the apex vertex 'x' exists and is connected to the top row vertices.
        self.assertIn('x', graph)
        self.assertIn((1, 1), graph['x'])
        self.assertIn((1, 2), graph['x'])

if __name__ == '__main__':
    unittest.main() 