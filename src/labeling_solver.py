from src.graph_generator import generate_mongolian_tent_graph
from src.graph_properties import calculate_lower_bound

def _is_valid_assignment(graph, labeling):
    """
    Checks if the current partial labeling has any duplicate edge weights.
    """
    weights = set()
    for u, neighbors in graph.items():
        if u not in labeling:
            continue
        for v in neighbors:
            if v in labeling:
                # To avoid double counting, only consider edges where u < v
                # This requires a consistent way to compare vertices, so we convert to string
                if str(u) < str(v):
                    weight = labeling[u] + labeling[v]
                    if weight in weights:
                        return False
                    weights.add(weight)
    return True

def backtracking_solver(graph, k, labeling, vertices_to_label):
    """
    Recursively finds a valid k-labeling using backtracking.
    """
    if not vertices_to_label:
        return labeling # Base case: all vertices are labeled

    vertex_to_label = vertices_to_label[0]
    remaining_vertices = vertices_to_label[1:]

    for label in range(1, k + 1):
        labeling[vertex_to_label] = label
        
        # After assigning a label, check if the partial labeling is valid
        if _is_valid_assignment(graph, labeling):
            result = backtracking_solver(graph, k, labeling, remaining_vertices)
            if result is not None:
                return result # Found a solution

    # Backtrack if no valid label was found
    del labeling[vertex_to_label]
    return None

def find_minimum_k_labeling(n):
    """
    Finds the minimum k and a valid labeling for the Mongolian Tent Graph MT_3,n.
    """
    if n <= 0:
        return None, None

    graph = generate_mongolian_tent_graph(n)
    
    # Sort vertices by degree (descending) as a heuristic to prune the search space
    vertices = sorted(graph.keys(), key=lambda v: len(graph[v]), reverse=True)
    
    k = calculate_lower_bound(n)
    
    # Attempt to find a greedy labeling to set an initial upper bound for k
    # We start with the current k (lower bound) and try to find a greedy solution.
    # If found, this provides an upper limit for k, potentially reducing search space.
    greedy_k = k
    greedy_labeling = None
    while greedy_labeling is None and greedy_k <= 2 * k: # Limit greedy search to avoid infinite loops for unlabelable graphs
        greedy_labeling = greedy_labeling_solver(graph, greedy_k)
        if greedy_labeling is None:
            greedy_k += 1
    
    if greedy_labeling is not None:
        print(f"Greedy labeling found for k = {greedy_k}. Starting backtracking from this k.")
        k = greedy_k # Start backtracking from this potentially higher k
    else:
        print("No greedy labeling found within reasonable bounds. Starting backtracking from lower bound.")

    while True:
        print(f"Attempting to find a valid labeling for k = {k}...")
        labeling = backtracking_solver(graph, k, {}, vertices)
        if labeling is not None:
            print(f"Found a valid labeling for k = {k}")
            return k, labeling
        k += 1 

def greedy_labeling_solver(graph, max_k):
    """
    Attempts to find a valid labeling greedily for a given max_k.
    Returns a labeling if found, otherwise None.
    """
    labeling = {}
    vertices = sorted(graph.keys(), key=lambda v: len(graph[v]), reverse=True)
    
    for vertex in vertices:
        found_label = False
        for label in range(1, max_k + 1):
            labeling[vertex] = label
            if _is_valid_assignment(graph, labeling):
                found_label = True
                break
        if not found_label:
            return None # Cannot find a valid label for this vertex, backtrack
            
    return labeling 

def find_heuristic_labeling(n: int, max_k_multiplier=5):
    """
    Finds a feasible, but not necessarily minimal, k-labeling for large n.

    This function uses the greedy solver iteratively. It starts with the theoretical
    lower bound for k and increases it until the greedy algorithm finds a valid
    solution or a reasonable upper limit is reached.

    Args:
        n: The size parameter for the Mongolian Tent graph.
        max_k_multiplier: The search will stop if k exceeds this multiple of the lower bound.

    Returns:
        A tuple (k, labeling) if a solution is found, otherwise (None, None).
    """
    if n <= 0:
        return None, None

    if max_k_multiplier < 1:
        raise ValueError("max_k_multiplier must be at least 1")

    graph = generate_mongolian_tent_graph(n)
    lower_bound = calculate_lower_bound(n)
    k = lower_bound
    max_k = lower_bound * max_k_multiplier  # safety upper limit

    print(f"\n[Heuristic Search] Starting search for n={n} from k={lower_bound} (limit: k={max_k})...")

    while k <= max_k:
        # Provide periodic feedback
        if k == lower_bound or k % 10 == 0:
            print(f"Attempting greedy solve for k={k}...")

        labeling = greedy_labeling_solver(graph, k)
        if labeling:
            print(f"Heuristic search found a valid labeling with k={k} for n={n}.")
            return k, labeling

        k += 1

    print(f"Heuristic search failed to find a solution for n={n} within the k limit (k>{max_k}).")
    return None, None 