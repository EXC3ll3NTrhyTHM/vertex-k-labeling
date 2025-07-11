import unittest
from src.labeling_solver import BranchAndBoundSolver
from src.graph_generator import create_mongolian_tent_graph
from src.graph_properties import calculate_lower_bound

class TestBranchAndBoundSolver(unittest.TestCase):

    def test_create_smart_vertex_order(self):
        solver = BranchAndBoundSolver(3)
        expected_order_n3 = ['x', (3, 1), (3, 2), (3, 3), (2, 1), (2, 2), (2, 3), (1, 1), (1, 2), (1, 3)]
        self.assertEqual(solver.vertex_order, expected_order_n3)

        solver = BranchAndBoundSolver(1)
        expected_order_n1 = ['x', (3, 1), (2, 1), (1, 1)]
        self.assertEqual(solver.vertex_order, expected_order_n1)

    def test_find_es_n1(self):
        solver = BranchAndBoundSolver(1)
        k, labeling = solver.find_es()
        self.assertIsNotNone(k)
        self.assertIsNotNone(labeling)
        self.assertEqual(k, calculate_lower_bound(1)) # For n=1, es(MT(3,1)) is 2

    def test_find_es_n2(self):
        solver = BranchAndBoundSolver(2)
        k, labeling = solver.find_es()
        self.assertIsNotNone(k)
        self.assertIsNotNone(labeling)
        # For n=2, es(MT(3,2)) is 6 (based on 3n formula)
        self.assertEqual(k, 6)

    def test_find_es_n3(self):
        solver = BranchAndBoundSolver(3)
        k, labeling = solver.find_es()
        self.assertIsNotNone(k)
        self.assertIsNotNone(labeling)
        # For n=3, es(MT(3,3)) is 9 (based on 3n formula)
        self.assertEqual(k, 8)

    def test_is_assignment_valid_mt31(self):
        solver = BranchAndBoundSolver(1) # MT(3,1) graph
        
        # Test case 1: Labeling apex 'x' with 1
        labels = {'x': 1}
        used_weights = set()
        is_valid, new_weights = solver._is_assignment_valid('x', labels, used_weights)
        self.assertTrue(is_valid)
        self.assertEqual(new_weights, set()) # No edges formed yet

        # Test case 2: Labeling (3,1) with 2, after 'x' is labeled 1
        labels = {'x': 1, (3,1): 2}
        used_weights = set() # used_weights should be empty for this call, as it's passed from parent recursive call
        is_valid, new_weights = solver._is_assignment_valid((3,1), labels, used_weights)
        self.assertTrue(is_valid)
        self.assertEqual(new_weights, {3}) # Edge ('x', (3,1)) has weight 1+2=3

        # Test case 3: Labeling (2,1) with 3, after 'x':1, (3,1):2. Edge ('x', (3,1)) weight 3 is now in used_weights
        labels = {'x': 1, (3,1): 2, (2,1): 3}
        used_weights = {3} # Edge ('x', (3,1)) weight is already formed
        is_valid, new_weights = solver._is_assignment_valid((2,1), labels, used_weights)
        self.assertTrue(is_valid)
        self.assertEqual(new_weights, {5}) # Edge ((3,1), (2,1)) has weight 2+3=5

        # Test case 4: Labeling (1,1) with 4, after 'x':1, (3,1):2, (2,1):3. Edges ('x', (3,1)):3, ((3,1), (2,1)):5 are in used_weights
        labels = {'x': 1, (3,1): 2, (2,1): 3, (1,1): 4}
        used_weights = {3, 5}
        is_valid, new_weights = solver._is_assignment_valid((1,1), labels, used_weights)
        self.assertTrue(is_valid)
        self.assertEqual(new_weights, {7}) # Edge ((2,1), (1,1)) has weight 3+4=7

        # Test conflict: Label (2,1) with 1 (instead of 3). Edge ((3,1), (2,1)) weight 2+1=3. Conflict with existing 3.
        labels_conflict = {'x': 1, (3,1): 2}
        used_weights_conflict = {3} # From ('x', (3,1))
        labels_conflict[(2,1)] = 1
        is_valid, new_weights = solver._is_assignment_valid((2,1), labels_conflict, used_weights_conflict)
        self.assertFalse(is_valid)
        self.assertEqual(new_weights, set())

    def test_adjacency_list_mt31(self):
        solver = BranchAndBoundSolver(1)
        adj = solver.adjacency_list
        print(f"Adjacency list for MT(3,1): {adj}")
        # Expected connections for MT(3,1)
        self.assertIn((3,1), adj['x'])
        self.assertIn('x', adj[(3,1)])
        self.assertIn((2,1), adj[(3,1)])
        self.assertIn((3,1), adj[(2,1)])
        self.assertIn((1,1), adj[(2,1)])
        self.assertIn((2,1), adj[(1,1)])

if __name__ == '__main__':
    unittest.main()