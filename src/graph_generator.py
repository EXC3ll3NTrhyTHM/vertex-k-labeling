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

    # Add horizontal edges for the top and bottom rows
    for i in range(1, n):
        graph[(1, i)].append((1, i + 1))
        graph[(1, i + 1)].append((1, i))
        graph[(2, i)].append((2, i + 1))
        graph[(2, i + 1)].append((2, i))

    # Add vertical "rung" edges
    for i in range(1, n + 1):
        graph[(1, i)].append((2, i))
        graph[(2, i)].append((1, i))

    return graph

def generate_mongolian_tent_graph(n):
    """
    Generates a Mongolian Tent graph MT_{3,n} for a given integer n.
    """
    if n <= 0:
        return collections.defaultdict(list)

    graph = generate_ladder_graph(n)
    apex_vertex = 'x'

    # Add the apex vertex and connect it to the top row vertices
    graph[apex_vertex] = []
    for i in range(1, n + 1):
        top_vertex = (1, i)
        graph[apex_vertex].append(top_vertex)
        graph[top_vertex].append(apex_vertex)

    return graph 