from src.graph_generator import generate_circulant_graph
from src.labeling_solver import find_optimal_k_labeling_circulant
from src.visualization.static import visualize_k_labeling
import os

def main():
    # Define parameters for your circulant graph
    n = 8  # Number of vertices (must be even and >= 6)
    r = 3  # Parameter for circulant graph (ignored in current generate_circulant_graph, but kept for context)

    print(f"Generating Circulant graph C({n}, {r})...")
    graph = generate_circulant_graph(n, r)

    if not graph:
        print(f"Failed to generate circulant graph with n={n}, r={r}. Please check parameters.")
        return

    print("Finding optimal k-labeling...")
    k, labeling = find_optimal_k_labeling_circulant(n, r)

    if labeling is None:
        print("Failed to find a valid k-labeling.")
        return

    print(f"Optimal k found: {k}")
    print("Labeling:", labeling)

    output_dir = "graphs"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"circulant_{n}_{r}_k_labeled.png")

    print(f"Visualizing labeled graph to {output_file}...")
    # Use shaped=False for circulant graphs to get a circular layout
    visualize_k_labeling(graph, labeling, output=output_file, shaped=False, solver_name="Optimal Circulant Solver", heuristic_k=k)

    print(f"Successfully generated and visualized labeled circulant graph to {output_file}")

if __name__ == "__main__":
    main()