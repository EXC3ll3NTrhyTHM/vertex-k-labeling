from src.graph_generator import create_mongolian_tent_graph
import math

def calculate_graph_metrics(adjacency_list):
    """
    Calculate the number of edges and the maximum degree of a graph.

    Args:
        adjacency_list (dict): The graph represented as an adjacency list.

    Returns:
        tuple: A tuple containing the number of edges and the maximum degree.
    """
    if not adjacency_list:
        return 0, 0

    edge_count = sum(len(neighbors) for neighbors in adjacency_list.values()) // 2
    max_degree = max(len(neighbors) for neighbors in adjacency_list.values()) if adjacency_list else 0
    
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
    
    graph = create_mongolian_tent_graph(n)
    edge_count, max_degree = calculate_graph_metrics(graph)
    
    # Lower bound formula: k >= max(ceil((|E(G)| + 1) / 2), delta(G))
    lower_bound_k = max(math.ceil((edge_count + 1) / 2), max_degree)
    
    return lower_bound_k 