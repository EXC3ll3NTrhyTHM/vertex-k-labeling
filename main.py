from src.graph_generator import generate_mongolian_tent_graph
from src.graph_properties import calculate_lower_bound
from src.labeling_solver import find_minimum_k_labeling, greedy_labeling_solver
import json

def main():
    """
    Main function to find the minimum k-labeling for a Mongolian Tent graph.
    """
    n = 30  # Using a small n due to the complexity of the solver
    print(f"Finding minimum k-labeling for Mongolian Tent graph with n = {n}")

    graph = generate_mongolian_tent_graph(n)
    max_k = calculate_lower_bound(n)

    # Use the greedy heuristic to find an initial upper bound for k
    initial_labeling = greedy_labeling_solver(graph, max_k)
    if initial_labeling:
        initial_k = max(initial_labeling.values())
        print(f"Initial k found by greedy heuristic: {initial_k}")
    else:
        initial_k = max_k
        print("Greedy heuristic did not find a valid labeling. Using lower bound as initial k.")

    # Use the initial k as an upper bound for the backtracking solver
    min_k, labeling = find_minimum_k_labeling(n)

    if labeling:
        print(f"\nMinimum k found: {min_k}")
        
        # Convert tuple keys to strings for JSON serialization
        serializable_labeling = {str(k): v for k, v in labeling.items()}
        print("Valid labeling:")
        print(json.dumps(serializable_labeling, indent=4, sort_keys=True))
    else:
        print(f"Could not find a valid labeling for n = {n}")

if __name__ == "__main__":
    main()
