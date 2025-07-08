from src.graph_generator import create_mongolian_tent_graph
from src.graph_properties import calculate_lower_bound, calculate_graph_metrics
from src.labeling_solver import find_feasible_k_labeling, find_optimal_k_labeling
import json
import time
import argparse
from src.constants import DEFAULT_TENT_SIZE, DEFAULT_SOLVER_TYPE

def main():
    """
    Main function to find a feasible k-labeling for a Mongolian Tent graph.
    """
    parser = argparse.ArgumentParser(description="Find and visualize k-labeling for Mongolian Tent graphs.")
    parser.add_argument("--n", type=int, default=DEFAULT_TENT_SIZE, help=f"Value of n for MT_{{3,n}} (default: {DEFAULT_TENT_SIZE})")
    parser.add_argument("--solver", type=str, default=DEFAULT_SOLVER_TYPE, choices=["heuristic", "backtracking"], help=f"Solver to use: 'heuristic' or 'backtracking' (default: {DEFAULT_SOLVER_TYPE})")
    args = parser.parse_args()

    n = args.n
    solver_type = args.solver

    print(f"Finding a {solver_type} k-labeling for Mongolian Tent graph with n = {n}")

    graph = create_mongolian_tent_graph(n)
    
    start_time = time.time()
    if solver_type == "heuristic":
        k, labeling = find_feasible_k_labeling(n)
        lower_bound = calculate_lower_bound(n)
        if isinstance(k, int) and isinstance(lower_bound, int):
            gap = k - lower_bound
        else:
            gap = 'N/A'
        solver_name = "Heuristic"
    elif solver_type == "backtracking":
        k, labeling = find_optimal_k_labeling(n)
        lower_bound = k # For backtracking, the found k is the lower bound
        gap = 0 # For backtracking, the gap is 0 as it finds the minimum
        solver_name = "Backtracking"
    else:
        print("Invalid solver type. Please choose 'heuristic' or 'backtracking'.")
        return
    end_time = time.time()
    time_taken = end_time - start_time

    if labeling:
        print(f"\n{solver_name} k found: {k}")
        print(f"Theoretical lower bound for k: {lower_bound}")
        print(f"Gap to lower bound: {gap}")
        print(f"Time taken to find k: {time_taken:.2f} seconds")

        # --- Visualization Example ---
        try:
            from src.visualization import visualize_k_labeling
            visualize_k_labeling(graph, labeling, output=f"graphs/mt3_{n}_{solver_type}.png", heuristic_k=k, lower_bound_k=lower_bound, gap=gap, time_taken=time_taken, solver_name=solver_name)
            print(f"Visualization saved to graphs/mt3_{n}_{solver_type}.png")
        except ImportError:
            print("Graphviz not installed; skipping visualization.")
    else:
        print(f"Could not find a valid labeling for n = {n}")

if __name__ == "__main__":
    main()
