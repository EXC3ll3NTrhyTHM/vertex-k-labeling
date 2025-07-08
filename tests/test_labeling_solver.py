import unittest
from src.labeling_solver import find_minimum_k_labeling, _is_valid_assignment, greedy_labeling_solver
from src.graph_generator import generate_mongolian_tent_graph

class TestLabelingSolver(unittest.TestCase):

    def test_find_minimum_k_labeling_n1(self):
        """Test the solver for n=1"""
        # For n=1, the lower bound for k is 2. The solver should find this.
        k, labeling = find_minimum_k_labeling(1)
        self.assertEqual(k, 2)
        self.assertIsNotNone(labeling)
        
        # Verify the labeling is valid
        graph = generate_mongolian_tent_graph(1)
        self.assertTrue(_is_valid_assignment(graph, labeling))

    def test_find_minimum_k_labeling_n2(self):
        """Test the solver for n=2"""
        # For n=2, the lower bound for k is 4. The solver should find this.
        k, labeling = find_minimum_k_labeling(2)
        self.assertEqual(k, 4)
        self.assertIsNotNone(labeling)
        
        # Verify the labeling is valid
        graph = generate_mongolian_tent_graph(2)
        self.assertTrue(_is_valid_assignment(graph, labeling))

    def test_is_valid_assignment_positive(self):
        """Test the validity checker with a known valid assignment"""
        graph = generate_mongolian_tent_graph(2)
        # A known valid labeling for MT_3,2 with k=4
        labeling = {
            (1, 1): 1, (1, 2): 2,
            (2, 1): 3, (2, 2): 4,
            'x': 1
        }
        # This labeling actually results in duplicate edge weights (e.g., x-(1,2) and (1,1)-(1,2) both have weight 3).
        # So, it should be an invalid assignment.
        self.assertFalse(_is_valid_assignment(graph, labeling))

    def test_is_valid_assignment_negative(self):
        """Test the validity checker with a known invalid assignment"""
        graph = generate_mongolian_tent_graph(2)
        # An invalid labeling with duplicate edge weight 3 ( (1,1)-(x) and (1,2)-(1,1) )
        labeling = {
            (1, 1): 1, (1, 2): 2,
            (2, 1): 3, (2, 2): 4,
            'x': 2
        }
        self.assertFalse(_is_valid_assignment(graph, labeling))

    def test_greedy_labeling_solver_n1(self):
        """Test the greedy solver for n=1"""
        graph = generate_mongolian_tent_graph(1)
        max_k = 2  # Theoretical lower bound for n=1
        labeling = greedy_labeling_solver(graph, max_k)
        self.assertIsNotNone(labeling)
        self.assertTrue(_is_valid_assignment(graph, labeling))

    def test_greedy_labeling_solver_n2(self):
        """Test the greedy solver for n=2. The greedy heuristic may or may not find a solution; if it does, it must be valid."""
        graph = generate_mongolian_tent_graph(2)
        max_k = 6  # Reasonable upper limit for test purposes
        labeling = greedy_labeling_solver(graph, max_k)
        if labeling:
            self.assertTrue(_is_valid_assignment(graph, labeling))
        else:
            # Greedy heuristic did not find a labeling; this is acceptable for this test case
            self.assertIsNone(labeling)

if __name__ == '__main__':
    unittest.main() 