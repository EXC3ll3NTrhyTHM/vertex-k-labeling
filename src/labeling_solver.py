from src.graph_generator import create_mongolian_tent_graph
from src.graph_properties import calculate_lower_bound
from typing import Any, Tuple, Union

def _get_vertex_sort_key(v: Union[Tuple[int, int], str]) -> Tuple[int, str, str]:
    if isinstance(v, tuple):
        # (type_discriminator, row_as_str_padded, col_as_str_padded)
        # Use zfill to ensure consistent lexicographical sorting for numbers
        return (0, str(v[0]).zfill(3), str(v[1]).zfill(3)) # Assuming max 3 digits for row/col
    elif v == 'x':
        # (type_discriminator, padded_placeholder_str, padded_placeholder_str)
        return (1, '000', '000') # Consistent padding for 'x', and matching length of other string parts
    else:
        # Fallback for any other unexpected vertex types, sorted by string
        # (type_discriminator, string_representation_padded, empty_string_padding)
        # Ensure the third element is also a string of consistent length
        return (2, str(v).zfill(10), '000') # Make all tuples (int, str, str)

def is_labeling_valid(graph, labeling, last_vertex=None):
    """
    Check if the current labeling is valid for the graph.

    Args:
        graph: adjacency list of the graph.
        labeling: mapping of vertex -> label.
        last_vertex: if provided, only validate edges incident on this vertex; otherwise, validate the entire graph.

    Returns:
        True if the labeling is valid (no duplicate edge weights), False otherwise.
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
                    # Ensure consistent edge checking to avoid duplicates based on canonical vertex order
                    if _get_vertex_sort_key(u) < _get_vertex_sort_key(v):
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
                # To avoid double counting, only consider edges where u < v based on canonical vertex order
                if _get_vertex_sort_key(u) < _get_vertex_sort_key(v):
                    weight = labeling[u] + labeling[v]
                    if weight in weights:
                        return False
                    weights.add(weight)
    return True

def _backtrack_k_labeling(graph, k, labeling, vertices_to_label):
    """
    Recursively find a valid k-labeling using backtracking.

    Args:
        graph: adjacency list of the graph.
        k: maximum label value to use.
        labeling: current partial mapping of vertices to labels.
        vertices_to_label: list of vertices remaining to label.

    Returns:
        A dict mapping vertices to labels if a complete valid labeling is found, otherwise None.
    """
    if not vertices_to_label:
        return labeling # Base case: all vertices are labeled

    vertex_to_label = vertices_to_label[0]
    remaining_vertices = vertices_to_label[1:]

    for label in range(1, k + 1):
        labeling[vertex_to_label] = label
        
        # After assigning a label, check if the partial labeling is valid
        if is_labeling_valid(graph, labeling):
            result = _backtrack_k_labeling(graph, k, labeling, remaining_vertices)
            if result is not None:
                return result # Found a solution

    # Backtrack if no valid label was found
    del labeling[vertex_to_label]
    return None

def find_optimal_k_labeling(n):
    """
    Find the optimal (minimum) k and a valid labeling for the Mongolian Tent graph MT_3,n.

    Args:
        n: size parameter for the Mongolian Tent graph.

    Returns:
        A tuple (k, labeling) where k is the minimum label value for which a valid labeling exists and labeling is the mapping.
    """
    if n <= 0:
        return None, None

    graph = create_mongolian_tent_graph(n)
    
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
        labeling = _backtrack_k_labeling(graph, k, {}, vertices)
        if labeling is not None:
            print(f"Found a valid labeling for k = {k}")
            return k, labeling
        k += 1 

def greedy_k_labeling(graph, max_k):
    """
    Attempt to find a valid k-labeling using a randomized greedy approach for a given k.

    Args:
        graph: adjacency list of the graph.
        max_k: maximum label value to try.

    Returns:
        A dict mapping vertices to labels if a valid labeling is found, otherwise None.
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
            if is_labeling_valid(graph, labeling, last_vertex=vertex):
                found_label = True
                break # Found a valid label
        
        if not found_label:
            # If no label can be assigned to this vertex, this path has failed
            return None
            
    return labeling

def find_feasible_k_labeling(n: int, max_k_multiplier=20, num_attempts=100):
    """
    Find a feasible k-labeling for the Mongolian Tent graph using a heuristic search.

    Args:
        n: the size parameter for the Mongolian Tent graph.
        max_k_multiplier: multiplier to set an upper bound on k based on the lower bound.
        num_attempts: number of randomized greedy attempts per k value.

    Returns:
        A tuple (k, labeling) with a valid labeling found, or (None, None) if none is found within bounds.
    """
    if n <= 0:
        return None, None

    if max_k_multiplier < 1:
        raise ValueError("max_k_multiplier must be at least 1")

    graph = create_mongolian_tent_graph(n)
    lower_bound = calculate_lower_bound(n)
    k = lower_bound
    max_k = lower_bound * max_k_multiplier  # safety upper limit

    print(f"\n[Heuristic Search] Starting search for n={n} from k={lower_bound} (limit: k={max_k})...")

    while k <= max_k:
        # Provide periodic feedback
        if k == lower_bound or k % 10 == 0:
            print(f"Attempting randomized greedy solve for k={k} ({num_attempts} attempts)...")

        for _ in range(num_attempts):
            labeling = greedy_k_labeling(graph, k)
            if labeling:
                print(f"Heuristic search found a valid labeling with k={k} for n={n}.")
                return k, labeling

        k += 1

    print(f"Heuristic search failed to find a solution for n={n} within the k limit (k>{max_k}).")
    return None, None 