from src.graph_generator import generate_mongolian_tent_graph
from src.graph_properties import calculate_lower_bound

def _is_valid_assignment(graph, labeling, last_vertex=None):
    """
    Checks if the assignment for the last labeled vertex is valid.
    If last_vertex is None, it checks the entire graph.
    """
    if last_vertex is not None:
        # Check only the edges connected to the last labeled vertex
        if last_vertex not in labeling:
            return True # Should not happen if called correctly
        
        last_label = labeling[last_vertex]
        weights = set()

        # Collect weights from the rest of the graph
        for u, neighbors in graph.items():
            if u == last_vertex or u not in labeling:
                continue
            for v in neighbors:
                if v != last_vertex and v in labeling:
                    # Ensure consistent edge checking to avoid duplicates
                    if str(u) < str(v):
                        weights.add(labeling[u] + labeling[v])
        
        # Check new weights from the last vertex
        for neighbor in graph[last_vertex]:
            if neighbor in labeling:
                weight = last_label + labeling[neighbor]
                if weight in weights:
                    return False
                weights.add(weight)
        return True

    # Original full check if last_vertex is not specified
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
    # REMOVED: This section was causing the backtracking solver to start from a potentially suboptimal k.
    # greedy_k = k
    # greedy_labeling = None
    # while greedy_labeling is None and greedy_k <= 2 * k: # Limit greedy search to avoid infinite loops for unlabelable graphs
    #     greedy_labeling = greedy_labeling_solver(graph, greedy_k)
    #     if greedy_labeling is None:
    #         greedy_k += 1
    
    # if greedy_labeling is not None:
    #     print(f"Greedy labeling found for k = {greedy_k}. Starting backtracking from this k.")
    #     k = greedy_k # Start backtracking from this potentially higher k
    # else:
    #     print("No greedy labeling found within reasonable bounds. Starting backtracking from lower bound.")

    while True:
        print(f"Attempting to find a valid labeling for k = {k}...")
        labeling = backtracking_solver(graph, k, {}, vertices)
        if labeling is not None:
            print(f"Found a valid labeling for k = {k}")
            return k, labeling
        k += 1 

def greedy_labeling_solver(graph, max_k):
    """
    Attempts to find a valid labeling using a randomized greedy approach.
    It shuffles the order of vertices and labels to explore different search paths.
    """
    # Create a copy of the vertices list to shuffle
    vertices = list(graph.keys())
    # Introduce randomness in vertex processing order
    import random
    random.shuffle(vertices)
    
    labeling = {}
    
    for vertex in vertices:
        # Introduce randomness in label selection order
        labels = list(range(1, max_k + 1))
        random.shuffle(labels)
        
        found_label = False
        for label in labels:
            labeling[vertex] = label
            if _is_valid_assignment(graph, labeling, last_vertex=vertex):
                found_label = True
                break # Found a valid label
        
        if not found_label:
            # If no label can be assigned to this vertex, this path has failed
            return None
            
    return labeling

def find_heuristic_labeling(n: int, max_k_multiplier=20, num_attempts=100):
    """
    Finds a feasible, but not necessarily minimal, k-labeling for large n
    by running a randomized greedy solver multiple times.

    Args:
        n: The size parameter for the Mongolian Tent graph.
        max_k_multiplier: The search for k will stop if it exceeds this multiple of the lower bound.
        num_attempts: The number of times to run the randomized solver for each k.

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
            print(f"Attempting randomized greedy solve for k={k} ({num_attempts} attempts)...")

        for _ in range(num_attempts):
            labeling = greedy_labeling_solver(graph, k)
            if labeling:
                print(f"Heuristic search found a valid labeling with k={k} for n={n}.")
                return k, labeling

        k += 1

    print(f"Heuristic search failed to find a solution for n={n} within the k limit (k>{max_k}).")
    return None, None 