from typing import Any, Dict, List, Optional, Set
from src.labeling_solver import is_labeling_valid


def compute_used_weights(graph: Dict[Any, List[Any]], labels: Dict[Any, int]) -> Set[int]:
    """Compute the set of edge weights (sum of labels) for all labeled edges in the graph."""
    weights: Set[int] = set()
    for u, neighbors in graph.items():
        if u in labels:
            for v in neighbors:
                if v in labels:
                    weights.add(labels[u] + labels[v])
    return weights


def k_labeling_backtracking(graph: Dict[Any, List[Any]], k_limit: Optional[int] = None) -> Optional[Dict[Any, int]]:
    """
    Compute an edge-irregular k-labeling of the given graph using backtracking.

    Args:
        graph: adjacency list mapping nodes to list of neighbor nodes.
        k_limit: optional upper bound on k. If None, the function will search from lower bound up to n.

    Returns:
        A dict mapping nodes to labels if valid labeling is found; otherwise, None.
    """
    # Determine search ordering: sort nodes by descending degree
    ordering = sorted(graph.keys(), key=lambda n: len(graph[n]), reverse=True)

    def assign_label(node_idx: int, labels: Dict[Any, int], used_weights: Set[int], limit: int) -> bool:
        if node_idx == len(ordering):
            return True
        node = ordering[node_idx]
        for label_val in range(1, limit + 1):
            conflict = False
            new_weights: Set[int] = set()
            for neighbor in graph[node]:
                if neighbor in labels:
                    weight = label_val + labels[neighbor]
                    # Check against existing and new weights to avoid duplicates
                    if weight in used_weights or weight in new_weights:
                        conflict = True
                        break
                    new_weights.add(weight)
            if conflict:
                continue
            labels[node] = label_val
            used_weights.update(new_weights)
            if assign_label(node_idx + 1, labels, used_weights, limit):
                return True
            # Backtrack: remove label and weights
            del labels[node]
            used_weights.difference_update(new_weights)
        return False

    # K-limit management
    lower_bound = max((len(neighbors) for neighbors in graph.values()), default=0)
    # search upper bound
    max_k = len(graph) if k_limit is None else k_limit
    for limit in range(lower_bound, max_k + 1):
        label_map: Dict[Any, int] = {}
        used_set: Set[int] = set()
        if assign_label(0, label_map, used_set, limit):
            # Sanity check full-graph labeling
            if not is_labeling_valid(graph, label_map):
                continue
            return label_map
    return None 