#!/usr/bin/env python3
"""
Test script for the benchmark execution system.
This script tests the benchmark runner with a small subset of graphs to verify functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.report_generator import BenchmarkRunner, BenchmarkResult

def test_mongolian_tent_benchmarks():
    """Test Mongolian Tent benchmarking with small graphs."""
    print("Testing Mongolian Tent benchmarking...")
    
    runner = BenchmarkRunner()
    
    # Override test sizes to use only small graphs for testing
    original_method = runner.run_mongolian_tent_benchmarks
    
    def test_run_mongolian_tent_benchmarks():
        from src.labeling_solver import find_optimal_k_labeling, find_feasible_k_labeling
        from src.graph_properties import calculate_lower_bound
        
        # Test with only small graphs for quick verification
        test_sizes = [3, 4]  # Small subset for testing
        results = []
        
        for n in test_sizes:
            print(f"Testing Mongolian Tent graph MT(3,{n})...")
            
            # Calculate theoretical lower bound
            lower_bound = calculate_lower_bound(n)
            print(f"  Lower bound: {lower_bound}")
            
            # Test backtracking algorithm with short timeout
            print(f"  Testing backtracking algorithm...")
            try:
                backtrack_result = runner._run_single_benchmark_with_timeout(
                    algorithm_func=find_optimal_k_labeling,
                    graph_type="mongolian_tent",
                    graph_params={"n": n},
                    algorithm_name="backtracking",
                    lower_bound=lower_bound,
                    timeout=10.0  # Short timeout for testing
                )
                results.append(backtrack_result)
                print(f"    Result: k={backtrack_result.k_value}, time={backtrack_result.execution_time:.3f}s, success={backtrack_result.success}")
            except Exception as e:
                print(f"    Error: {e}")
            
            # Test heuristic algorithm (accurate mode)
            print(f"  Testing heuristic algorithm (accurate mode)...")
            try:
                heuristic_result = runner._run_single_benchmark_with_timeout(
                    algorithm_func=find_feasible_k_labeling,
                    graph_type="mongolian_tent", 
                    graph_params={"n": n},
                    algorithm_name="heuristic_accurate",
                    lower_bound=lower_bound,
                    timeout=5.0,  # Short timeout for testing
                    algorithm_kwargs={"algorithm": "accurate", "num_attempts": 10}
                )
                results.append(heuristic_result)
                print(f"    Result: k={heuristic_result.k_value}, time={heuristic_result.execution_time:.3f}s, success={heuristic_result.success}")
            except Exception as e:
                print(f"    Error: {e}")
        
        return results
    
    # Run the test
    results = test_run_mongolian_tent_benchmarks()
    
    # Test table generation
    if results:
        print("\nTesting table generation...")
        mt_table, _ = runner.generate_results_tables(results)
        print("Generated Mongolian Tent table:")
        print(mt_table)
    
    return results

def test_circulant_benchmarks():
    """Test Circulant benchmarking with small graphs."""
    print("\nTesting Circulant benchmarking...")
    
    runner = BenchmarkRunner()
    
    # Test with only small graphs for quick verification
    test_params = [(6, 2)]  # Small subset for testing
    results = []
    
    for n, r in test_params:
        print(f"Testing Circulant graph C({n},{r})...")
        
        from src.graph_properties import calculate_circulant_lower_bound
        lower_bound = calculate_circulant_lower_bound(n, r)
        print(f"  Lower bound: {lower_bound}")
        
        # Test heuristic algorithm only (faster for testing)
        print(f"  Testing heuristic algorithm (accurate mode)...")
        try:
            from src.labeling_solver import find_feasible_k_labeling
            heuristic_result = runner._run_single_benchmark_with_timeout(
                algorithm_func=find_feasible_k_labeling,
                graph_type="circulant",
                graph_params={"n": n, "r": r},
                algorithm_name="heuristic_accurate",
                lower_bound=lower_bound,
                timeout=5.0,  # Short timeout for testing
                algorithm_kwargs={"algorithm": "accurate", "num_attempts": 10}
            )
            results.append(heuristic_result)
            print(f"    Result: k={heuristic_result.k_value}, time={heuristic_result.execution_time:.3f}s, success={heuristic_result.success}")
        except Exception as e:
            print(f"    Error: {e}")
    
    # Test table generation
    if results:
        print("\nTesting table generation...")
        _, circulant_table = runner.generate_results_tables(results)
        print("Generated Circulant table:")
        print(circulant_table)
    
    return results

def main():
    """Main test function."""
    print("Testing Benchmark Execution System")
    print("=" * 50)
    
    try:
        # Test Mongolian Tent benchmarks
        mt_results = test_mongolian_tent_benchmarks()
        
        # Test Circulant benchmarks  
        circulant_results = test_circulant_benchmarks()
        
        # Test combined table generation
        all_results = mt_results + circulant_results
        if all_results:
            print("\nTesting combined table generation...")
            runner = BenchmarkRunner()
            mt_table, circulant_table = runner.generate_results_tables(all_results)
            
            print("\nFinal Combined Results:")
            print("Mongolian Tent Results:")
            print(mt_table)
            print("\nCirculant Results:")
            print(circulant_table)
        
        print("\n" + "=" * 50)
        print("Benchmark system test completed successfully!")
        
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())