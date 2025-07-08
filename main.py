from src.graph_generator import generate_mongolian_tent_graph
from src.graph_properties import calculate_lower_bound
from src.labeling_solver import find_heuristic_labeling
import json

def main():
    """
    Main function to find a feasible k-labeling for a Mongolian Tent graph.
    """
    n = 30
    print(f"Finding a heuristic k-labeling for Mongolian Tent graph with n = {n}")

    graph = generate_mongolian_tent_graph(n)
    
    # Use the heuristic solver to find a feasible labeling quickly
    k, labeling = find_heuristic_labeling(n)

    if labeling:
        print(f"\nHeuristic k found: {k}")
        
        # Convert tuple keys to strings for JSON serialization
        serializable_labeling = {str(k_v): v for k_v, v in labeling.items()}
        print("Valid labeling found:")
        print(json.dumps(serializable_labeling, indent=4, sort_keys=True))

        # --- Visualization Example ---
        try:
            from src.visualization import visualize_labeling
            visualize_labeling(graph, labeling, output=f"graphs/mt3_{n}_heuristic.png")
            print(f"Visualization saved to graphs/mt3_{n}_heuristic.png")
        except ImportError:
            print("Graphviz not installed; skipping visualization.")
    else:
        print(f"Could not find a valid labeling for n = {n}")

if __name__ == "__main__":
    main()
