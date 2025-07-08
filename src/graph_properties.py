from src.graph_generator import generate_mongolian_tent_graph
import math

def get_graph_properties(graph):
    """
    Calculates the number of edges and the maximum degree of a graph.

    Args:
        graph (dict): The graph represented as an adjacency list.

    Returns:
        tuple: A tuple containing the number of edges and the maximum degree.
    """
    if not graph:
        return 0, 0

    edge_count = sum(len(v) for v in graph.values()) // 2
    max_degree = max(len(v) for v in graph.values()) if graph else 0
    
    return edge_count, max_degree

def calculate_lower_bound(n):
    """
    Calculates the theoretical lower bound for k for a Mongolian Tent Graph.

    Args:
        n (int): The parameter n for the Mongolian Tent Graph.

    Returns:
        int: The theoretical lower bound for k.
    """
    if n <= 0:
        return 0
    
    graph = generate_mongolian_tent_graph(n)
    edge_count, max_degree = get_graph_properties(graph)
    
    # Lower bound formula: k >= max(ceil((|E(G)| + 1) / 2), delta(G))
    lower_bound_k = max(math.ceil((edge_count + 1) / 2), max_degree)
    
    return lower_bound_k 