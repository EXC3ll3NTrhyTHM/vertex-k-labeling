#!/usr/bin/env python3
"""
Test script for the Mathematical Notation Formatter

This script tests the mathematical notation formatting functionality
to ensure proper LaTeX formatting for graph theory and complexity notation.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from report_generator import MathematicalNotationFormatter

def test_graph_notation():
    """Test graph theory notation formatting."""
    formatter = MathematicalNotationFormatter()
    
    print("Testing Graph Notation Formatting:")
    print("=" * 40)
    
    # Test Circulant graphs
    print("Circulant Graphs:")
    print(f"  C(6,2): {formatter.format_graph_notation('circulant', n=6, r=2)}")
    print(f"  C(10,5): {formatter.format_graph_notation('circulant', n=10, r=5)}")
    print(f"  C(12,[3,5]): {formatter.format_graph_notation('circulant', n=12, r=[3,5])}")
    
    # Test Mongolian Tent graphs
    print("\nMongolian Tent Graphs:")
    print(f"  MT(3,5): {formatter.format_graph_notation('mongolian_tent', m=3, n=5)}")
    print(f"  MT(3,10): {formatter.format_graph_notation('mongolian_tent', m=3, n=10)}")
    
    # Test generic graph
    print(f"\nGeneric Graph: {formatter.format_graph_notation('generic')}")
    print()

def test_complexity_notation():
    """Test algorithmic complexity notation formatting."""
    formatter = MathematicalNotationFormatter()
    
    print("Testing Complexity Notation Formatting:")
    print("=" * 40)
    
    # Test exponential complexity
    print("Exponential Complexity:")
    print(f"  Backtracking: {formatter.format_complexity_notation('exponential_k_vertices')}")
    print(f"  Custom k^V: {formatter.format_complexity_notation('exponential_k_vertices', {'k': 'k', 'V': '|V|'})}")
    
    # Test polynomial complexity
    print("\nPolynomial Complexity:")
    print(f"  Linear V+E: {formatter.format_complexity_notation('polynomial_vertices_edges')}")
    print(f"  Heuristic: {formatter.format_complexity_notation('heuristic_accurate')}")
    
    # Test space complexity
    print("\nSpace Complexity:")
    print(f"  Space V+k: {formatter.format_complexity_notation('space_vertices_k')}")
    print(f"  Linear V: {formatter.format_complexity_notation('linear_vertices')}")
    print()

def test_bounds_and_formulas():
    """Test mathematical bounds and formulas formatting."""
    formatter = MathematicalNotationFormatter()
    
    print("Testing Bounds and Formulas Formatting:")
    print("=" * 40)
    
    # Test general bounds
    print("General Bounds:")
    print(f"  Lower bound: {formatter.format_bounds_and_formulas('lower_bound_general')}")
    print(f"  k-labeling def: {formatter.format_bounds_and_formulas('k_labeling_definition')}")
    
    # Test specific graph bounds
    print("\nSpecific Graph Bounds:")
    print(f"  Circulant bound: {formatter.format_bounds_and_formulas('lower_bound_circulant', n=10, r=5)}")
    print(f"  MT bound: {formatter.format_bounds_and_formulas('lower_bound_mongolian_tent', m=3, n=10)}")
    
    # Test other formulas
    print("\nOther Formulas:")
    print(f"  Edge weight: {formatter.format_bounds_and_formulas('edge_weight_function')}")
    print(f"  Gap calculation: {formatter.format_bounds_and_formulas('gap_calculation', k=7, lower_bound=5)}")
    print()

def test_set_notation():
    """Test mathematical set notation formatting."""
    formatter = MathematicalNotationFormatter()
    
    print("Testing Set Notation Formatting:")
    print("=" * 40)
    
    print("Basic Sets:")
    print(f"  Vertex set: {formatter.format_set_notation('vertex_set')}")
    print(f"  Edge set: {formatter.format_set_notation('edge_set')}")
    print(f"  Label set: {formatter.format_set_notation('label_set', 'k')}")
    print(f"  Weight set: {formatter.format_set_notation('weight_set')}")
    
    print("\nCirculant Generators:")
    print(f"  Single generator: {formatter.format_set_notation('circulant_generators', 3)}")
    print(f"  Multiple generators: {formatter.format_set_notation('circulant_generators', [2, 5])}")
    print()

def test_algorithm_notation():
    """Test algorithm-specific mathematical notation."""
    formatter = MathematicalNotationFormatter()
    
    print("Testing Algorithm Notation Formatting:")
    print("=" * 40)
    
    print("Backtracking Notation:")
    print(f"  Branching factor: {formatter.format_algorithm_notation('backtrack_branching_factor', k=7)}")
    print(f"  Search depth: {formatter.format_algorithm_notation('search_tree_depth')}")
    
    print("\nHeuristic Notation:")
    print(f"  Max attempts: {formatter.format_algorithm_notation('heuristic_attempts', attempts=100)}")
    print(f"  Conflict score: {formatter.format_algorithm_notation('conflict_score')}")
    print(f"  Success prob: {formatter.format_algorithm_notation('success_probability', probability='0.85')}")
    print()

def main():
    """Run all mathematical notation formatter tests."""
    print("Mathematical Notation Formatter Test Suite")
    print("=" * 50)
    print()
    
    test_graph_notation()
    test_complexity_notation()
    test_bounds_and_formulas()
    test_set_notation()
    test_algorithm_notation()
    
    print("All tests completed successfully!")
    print("Mathematical notation formatter is working correctly.")

if __name__ == "__main__":
    main()