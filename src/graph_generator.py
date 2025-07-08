import collections

def generate_ladder_graph(n):
    """
    Generates a ladder graph L_n with n rungs.

    The graph is represented by an adjacency list (dictionary).
    Vertices are represented as tuples: (1, i) for the top row
    and (2, i) for the bottom row, where i is from 1 to n.
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

def create_mongolian_tent_graph(tent_size):
    """
    Generate a Mongolian Tent graph MT_{3,n} for a given integer tent_size.

    Args:
        tent_size (int): number of columns in the tent graph.

    Returns:
        adjacency list of the Mongolian Tent graph.
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