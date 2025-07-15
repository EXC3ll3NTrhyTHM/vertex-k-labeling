from src.graph_generator import create_mongolian_tent_graph
import math
from typing import Dict, List, Any, Tuple
import collections

def calculate_circulant_lower_bound(n: int, r: int) -> int:
    """
    Calculates the theoretical lower bound for the edge irregularity strength (es) of a circulant graph (Cn,r).
    Formula: max{ceil((nr+2)/4), r}
    """
    if n <= 0 or r <= 0:
        return 0

    # Calculate the first part of the formula: ceil((n * r + 2) / 4)
    part1 = math.ceil((n * r + 2) / 4)

    # Return the maximum of part1 and r
    return max(part1, r)


"""
Graph property calculations for Mongolian Tent and related graphs.

Provides metrics such as edge count, maximum degree, theoretical lower bounds,
regularity checks, and diameter estimates.

References:
    - ai-docs/algorithms/heuristic_algorithm.md (lower bound derivation)
    - ai-docs/fixes/fix_greedy_inefficiency.md (context on degree metrics improvements)
    - ai-docs/enhancments/enhancement02_shape_graph.md (diameter computation motivation)
"""
def calculate_graph_metrics(adjacency_list: Dict[Any, List[Any]]) -> Tuple[int, int]:
    """
    Calculate the number of edges and the maximum degree of a graph.

    Args:
        adjacency_list (dict): The graph represented as an adjacency list.

    Returns:
        tuple: A tuple containing the number of edges and the maximum degree.

    References:
        - ai-docs/algorithms/backtracking_algorithm.md (edge enumeration requirements)
        - ai-docs/fixes/fix_greedy_inefficiency.md (performance considerations)
    """
    if not adjacency_list:
        return 0, 0

    edge_count = sum(len(neighbors) for neighbors in adjacency_list.values()) // 2
    max_degree = max(len(neighbors) for neighbors in adjacency_list.values()) if adjacency_list else 0
    
    return edge_count, max_degree

def calculate_lower_bound(tent_size: int) -> int:
    """
    Calculates the theoretical lower bound for k for a Mongolian Tent Graph.

    Args:
        tent_size (int): The size parameter for the Mongolian Tent Graph.

    Returns:
        int: The theoretical lower bound for k.

    References:
        - ai-docs/algorithms/heuristic_algorithm.md (lower-bound formula)
        - ai-docs/fixes/fix_incorrect_ladder_levels.md (boundary corrections)
    """
    if tent_size <= 0:
        return 0
    
    graph = create_mongolian_tent_graph(tent_size)
    edge_count, max_degree = calculate_graph_metrics(graph)
    
    # Lower bound formula: k >= max(ceil((|E(G)| + 1) / 2), delta(G))
    lower_bound_k = max(math.ceil((edge_count + 1) / 2), max_degree)
    
    return lower_bound_k 
   
def is_regular(adjacency_list: Dict[Any, List[Any]], r: int) -> bool:
    """
    Check if the graph is r-regular: every vertex has degree exactly r.

    References:
        - ai-docs/enhancments/enhancement_CP-SAT_solver.md (regularity constraints)
    """
    if not adjacency_list:
        return False
    return all(len(neighbors) == r for neighbors in adjacency_list.values())

def compute_diameter(adjacency_list: Dict[Any, List[Any]]) -> int:
    """
    Compute the diameter of the graph (longest shortest-path between any two vertices).

    References:
        - ai-docs/enhancments/enhancement02_shape_graph.md (use cases for diameter)
    """
    if not adjacency_list:
        return 0
    diameter = 0
    for source in adjacency_list:
        visited = {source}
        queue = collections.deque([(source, 0)])
        while queue:
            node, dist = queue.popleft()
            diameter = max(diameter, dist)
            for neighbor in adjacency_list[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
    return diameter 