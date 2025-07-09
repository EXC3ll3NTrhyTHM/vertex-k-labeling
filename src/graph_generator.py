import collections
from typing import Dict, List, Any


def generate_ladder_graph(n):
    """
    Generates a ladder graph L_n with n rungs.

    The graph is represented by an adjacency list (dictionary).
    Vertices are represented as tuples: (1, i) for the top row
    and (2, i) for the bottom row, where i is from 1 to n.

    References:
        - ai-docs/initial-design/task_1.md  (ladder graph generation requirements)
        - ai-docs/initial-design/master_plan.md  (overall project architecture)
    """
    if n <= 0:
        return collections.defaultdict(list)

    graph = collections.defaultdict(list)

    # Add horizontal edges for the three rows
    for i in range(1, n):
        for row in (1, 2, 3):
            graph[(row, i)].append((row, i + 1))
            graph[(row, i + 1)].append((row, i))

    # Add vertical rungs between rows 1↔2 and 2↔3
    for i in range(1, n + 1):
        graph[(1, i)].append((2, i))
        graph[(2, i)].append((1, i))
        graph[(2, i)].append((3, i))
        graph[(3, i)].append((2, i))

    return graph


def create_mongolian_tent_graph(tent_size: int) -> Dict[Any, List[Any]]:
    """
    Generate a Mongolian Tent graph MT_{3,n} for a given integer tent_size.

    Args:
        tent_size (int): number of columns in the tent graph.

    Returns:
        adjacency list of the Mongolian Tent graph.

    References:
        - ai-docs/initial-design/task_1.md  (Mongolian Tent graph construction)
        - ai-docs/initial-design/master_plan.md  (design overview of MT graphs)
    """
    if tent_size <= 0:
        return collections.defaultdict(list)

    graph = generate_ladder_graph(tent_size)
    apex_vertex = 'x'

    # Add the apex vertex and connect it to the top row vertices
    graph[apex_vertex] = []
    for i in range(1, tent_size + 1):
        top_vertex = (1, i)
        graph[apex_vertex].append(top_vertex)
        graph[top_vertex].append(apex_vertex)

    return graph


def generate_circulant_graph(n: int, r: int) -> Dict[int, List[int]]:
    """
    Generate a circulant graph by removing edges from the complete circulant K_n to reduce each vertex's degree by 5.

    Only valid for even n ≥ 6. It removes generators s=1,2,n/2 in that order.
    Final degree = (n-1) - 5 = n - 6.

    Args:
        n (int): number of vertices (5 ≤ n ≤ 50).
        r (int): ignored.

    Returns:
        adjacency list mapping vertex id to list of neighbor ids; empty for invalid inputs.

    References:
        - ai-docs/algorithms/circulant_graph_generation_algorithm.md  (circulant graph generation logic)
        - ai-docs/enhancments/enhancement03_circulant_graph.md  (improvements and edge-removal strategy)
    """
    # Validate n even and sufficient size
    if not (6 <= n <= 50 and n % 2 == 0):
        return collections.defaultdict(list)
    graph = collections.defaultdict(list)
    half = n // 2
    # Step 1: build complete circulant K_n adjacency
    for s in range(1, half + 1):
        for i in range(n):
            j = (i + s) % n
            graph[i].append(j)
            graph[j].append(i)
    # Step 2: remove closest neighbor edges first
    for s in (1, 2, half):
        for i in range(n):
            j = (i + s) % n
            # remove edge i<->j if exists
            if j in graph[i]:
                graph[i].remove(j)
            if i in graph[j]:
                graph[j].remove(i)
    return graph 