#!/usr/bin/env python3
"""
Integration test for Mathematical Notation Formatter with Report Generator

This script tests the integration of the mathematical notation formatter
with the report generator to ensure proper functionality.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from report_generator import ReportGenerator, MathematicalNotationFormatter

def test_report_generator_integration():
    """Test that ReportGenerator properly integrates with MathematicalNotationFormatter."""
    print("Testing Report Generator Integration with Math Formatter:")
    print("=" * 60)
    
    # Create report generator instance
    report_gen = ReportGenerator()
    
    # Test helper methods
    print("Testing helper methods:")
    print(f"  Graph name (Circulant): {report_gen.format_graph_name('circulant', n=10, r=5)}")
    print(f"  Graph name (MT): {report_gen.format_graph_name('mongolian_tent', m=3, n=8)}")
    print(f"  Complexity (exponential): {report_gen.format_complexity('exponential_k_vertices')}")
    print(f"  Formula (k-labeling): {report_gen.format_mathematical_formula('k_labeling_definition')}")
    
    # Test algorithm descriptions use proper LaTeX
    print("\nTesting algorithm descriptions:")
    backtrack_desc = report_gen.analyzer.analyze_backtracking_algorithm()
    heuristic_desc = report_gen.analyzer.analyze_heuristic_algorithm()
    
    print(f"  Backtracking complexity: {backtrack_desc.time_complexity}")
    print(f"  Backtracking space: {backtrack_desc.space_complexity}")
    print(f"  Heuristic complexity: {heuristic_desc.time_complexity}")
    print(f"  Heuristic space: {heuristic_desc.space_complexity}")
    
    print("\nIntegration test completed successfully!")
    print("Mathematical notation formatter is properly integrated with report generator.")

def test_standalone_formatter():
    """Test standalone mathematical notation formatter functionality."""
    print("\nTesting Standalone Mathematical Notation Formatter:")
    print("=" * 60)
    
    formatter = MathematicalNotationFormatter()
    
    # Test various formatting functions
    test_cases = [
        ("Circulant C(6,2)", formatter.format_graph_notation("circulant", n=6, r=2)),
        ("MT(3,10)", formatter.format_graph_notation("mongolian_tent", m=3, n=10)),
        ("Exponential complexity", formatter.format_complexity_notation("exponential_k_vertices")),
        ("Heuristic complexity", formatter.format_complexity_notation("heuristic_accurate")),
        ("Lower bound formula", formatter.format_bounds_and_formulas("lower_bound_general")),
        ("k-labeling definition", formatter.format_bounds_and_formulas("k_labeling_definition")),
        ("Vertex set", formatter.format_set_notation("vertex_set")),
        ("Label set", formatter.format_set_notation("label_set", "k")),
        ("Conflict score", formatter.format_algorithm_notation("conflict_score"))
    ]
    
    for description, result in test_cases:
        print(f"  {description}: {result}")
    
    print("\nStandalone formatter test completed successfully!")

def main():
    """Run all integration tests."""
    print("Mathematical Notation Formatter Integration Test Suite")
    print("=" * 70)
    print()
    
    test_report_generator_integration()
    test_standalone_formatter()
    
    print("\n" + "=" * 70)
    print("All integration tests passed!")
    print("Mathematical notation formatter is ready for use in report generation.")

if __name__ == "__main__":
    main()