from __future__ import annotations

"""K-labeling solvers for Mongolian Tent graphs and related structures.

Provides exact backtracking solver and several greedy/heuristic approaches
(deterministic first-fit, randomized multi-attempt, and hybrid fast mode).

References:
    - ai-docs/algorithms/backtracking_algorithm.md (exact solver description)
    - ai-docs/algorithms/heuristic_algorithm.md (greedy strategies and rationale)
    - ai-docs/fixes/fix_backtracking_performance.md (optimization notes)
    - ai-docs/enhancments/enhancement01_Task_1.md (solver feature roadmap)
"""
from src.graph_generator import create_mongolian_tent_graph, generate_circulant_graph
from src.graph_properties import calculate_lower_bound, calculate_circulant_lower_bound
from src.constants import MAX_K_MULTIPLIER_DEFAULT, GREEDY_ATTEMPTS_DEFAULT
from typing import Any, Tuple, Union, Dict, List, Optional, Callable

# Animation event type imports (optional – avoid hard dependency when unused)
from importlib import import_module
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.events import StepEvent as StepEvent  # noqa: F401  (re-export for typing)
    from src.events import EventType as EventType  # noqa: F401
else:
    try:
        _events_mod = import_module("src.events")
        StepEvent = getattr(_events_mod, "StepEvent")  # type: ignore
        EventType = getattr(_events_mod, "EventType")  # type: ignore
    except Exception:  # pragma: no cover – animation module unavailable
        StepEvent = None  # type: ignore
        EventType = None  # type: ignore


try:
    from bitarray import bitarray  # type: ignore
    _BITARRAY_AVAILABLE = True
except ImportError:  # pragma: no cover – fallback when dependency not installed
    bitarray = None  # type: ignore
    _BITARRAY_AVAILABLE = False


def _init_used_weights(length: int):  # noqa: D401 – simple factory helper
    """Return a zero-initialised weight-usage mask.

    Uses *bitarray* when available for O(1) index ops on a compact
    contiguous bit-set (~8× memory saving & a noticeable speed-up in inner
    loops).  Falls back to a Python list of bools when the library is not
    installed.
    """
    if _BITARRAY_AVAILABLE and bitarray is not None:
        mask = bitarray(length)  # type: ignore[operator]
        mask.setall(False)
        return mask
    # Fallback – regular Python list
    return [False] * length

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

def _get_generic_vertex_sort_key(v: Any) -> Tuple[int, ...]:
    """Return a stable sort key for any vertex type."""
    if isinstance(v, tuple): # For Mongolian Tent (row, col)
        return (0, v[0], v[1])
    elif isinstance(v, int): # For Circulant graphs (integer IDs)
        return (1, v)
    elif v == 'x': # For Mongolian Tent apex
        return (2,)
    else: # Fallback for other types
        return (3, str(v))

def is_labeling_valid(adjacency_list: Dict[Any, List[Any]], vertex_labels: Dict[Any, int], last_vertex: Optional[Any] = None, sort_key_func: Callable[[Any], Tuple[int, ...]] = _get_vertex_sort_key) -> bool:
    """
    Check if the current labeling is valid for the graph.

    Args:
        adjacency_list: adjacency list of the graph.
        vertex_labels: mapping of vertex -> label.
        last_vertex: if provided, only validate edges incident on this vertex; otherwise, validate the entire graph.

    Returns:
        True if the labeling is valid (no duplicate edge weights), False otherwise.

    References:
        - ai-docs/algorithms/backtracking_algorithm.md (edge weight uniqueness definition)
        - ai-docs/fixes/fix_greedy_inefficiency.md (incremental validation optimizations)
    """
    if last_vertex is not None:
        if last_vertex not in vertex_labels:
            return True  # Should not happen if called correctly
        last_label = vertex_labels[last_vertex]
        existing_weights: set[int] = set()
        # Collect weights from the rest of the graph
        for source_vertex, neighbors in adjacency_list.items():
            if source_vertex == last_vertex or source_vertex not in vertex_labels:
                continue
            for target_vertex in neighbors:
                if target_vertex != last_vertex and target_vertex in vertex_labels:
                    if sort_key_func(source_vertex) < sort_key_func(target_vertex):
                        existing_weights.add(vertex_labels[source_vertex] + vertex_labels[target_vertex])
        # Check new weights from the last vertex
        for neighbor in adjacency_list[last_vertex]:
            if neighbor in vertex_labels:
                weight = last_label + vertex_labels[neighbor]
                if weight in existing_weights:
                    return False
                existing_weights.add(weight)
        return True

    # Full validation when last_vertex is not specified
    weights: set[int] = set()
    for source_vertex, neighbors in adjacency_list.items():
        if source_vertex not in vertex_labels:
            continue
        for target_vertex in neighbors:
            if target_vertex in vertex_labels and sort_key_func(source_vertex) < sort_key_func(target_vertex):
                weight = vertex_labels[source_vertex] + vertex_labels[target_vertex]
                if weight in weights:
                    return False
                weights.add(weight)
    return True

# --------------------
# Solver base emit helper
# --------------------

def _maybe_emit(callback: Optional[Callable[["StepEvent"], None]], event: Optional["StepEvent"]):
    """Safely invoke *callback* with *event* if both are provided.

    The indirection avoids import errors when the animation module is not
    installed or when event types are mocked.
    """

    if callback is not None and event is not None:
        try:
            callback(event)  # type: ignore[arg-type]
        except Exception:  # pragma: no cover – animation errors should not break solver
            # Fail-safe: ignore animation issues
            pass

def _backtrack_k_labeling_generic(
    adjacency_list: Dict[Any, List[Any]],
    max_k_value: int,
    vertex_labels: Dict[Any, int],
    unlabeled_vertices: List[Any],
    used_weights: List[bool],
    on_step: Optional[Callable[["StepEvent"], None]] = None,
) -> Optional[Dict[Any, int]]:
    """
    Recursively find a valid k-labeling using backtracking.

    Args:
        adjacency_list: adjacency list of the graph.
        max_k_value: maximum label value to use.
        vertex_labels: current partial mapping of vertices to labels.
        unlabeled_vertices: list of vertices remaining to label.

    Returns:
        A dict mapping vertices to labels if a complete valid labeling is found, otherwise None.

    References:
        - ai-docs/algorithms/backtracking_algorithm.md (recursive algorithm pseudocode)
        - ai-docs/fixes/fix_backtracking_performance.md (bit-array optimization)
    """
    if not unlabeled_vertices:
        # Base case: all vertices are labeled — verify full validity before accepting
        if is_labeling_valid(adjacency_list, vertex_labels, sort_key_func=_get_generic_vertex_sort_key):
            return vertex_labels
        return None

    vertex_to_label = unlabeled_vertices[0]
    remaining_vertices = unlabeled_vertices[1:]

    for label in range(1, max_k_value + 1):
        if StepEvent and EventType:
            _maybe_emit(
                on_step,
                StepEvent(EventType.VERTEX_LABELED, {"vertex": vertex_to_label, "label": label}),
            )
        vertex_labels[vertex_to_label] = label
        new_weights: List[int] = []
        conflict = False
        for neighbor in adjacency_list[vertex_to_label]:
            if neighbor in vertex_labels:
                weight = label + vertex_labels[neighbor]
                if StepEvent and EventType:
                    _maybe_emit(
                        on_step,
                        StepEvent(
                            EventType.EDGE_WEIGHT_CALCULATED,
                            {"edge": (vertex_to_label, neighbor), "weight": weight},
                        ),
                    )
                # Check against bit-array mask
                if weight < len(used_weights) and used_weights[weight]:
                    conflict = True
                    break
                new_weights.append(weight)
        if not conflict:
            # Mark new weights in bit-array mask
            for w in new_weights:
                used_weights[w] = True

            # Recurse with updated weights
            result = _backtrack_k_labeling_generic(
                adjacency_list,
                max_k_value,
                vertex_labels,
                remaining_vertices,
                used_weights,
                on_step,
            )
            if result is not None:
                return result  # Found a solution
            # Backtrack bit-array flags
            for w in new_weights:
                used_weights[w] = False
    # Backtrack if no valid label was found
    if StepEvent and EventType and vertex_to_label in vertex_labels:
        _maybe_emit(
            on_step,
            StepEvent(EventType.BACKTRACK, {"vertex": vertex_to_label}),
        )
    del vertex_labels[vertex_to_label]
    return None

class BranchAndBoundSolver:
    def __init__(self, n: int, on_step: Optional[Callable[["StepEvent"], None]] = None):
        self.n = n
        self.adjacency_list = create_mongolian_tent_graph(n)
        self.on_step = on_step
        self.vertex_order = self._create_smart_vertex_order(n)

    def _create_smart_vertex_order(self, n: int) -> List[Any]:
        # Apex vertex 'x'
        vertex_order = ['x']

        # Top row vertices (v_3,j)
        for j in range(1, n + 1):
            vertex_order.append((3, j))

        # Middle row vertices (v_2,j)
        for j in range(1, n + 1):
            vertex_order.append((2, j))

        # Bottom row vertices (v_1,j)
        for j in range(1, n + 1):
            vertex_order.append((1, j))
        return vertex_order

    def _is_assignment_valid(self, current_v: Any, labels: Dict[Any, int], used_edge_weights: set[int]) -> Tuple[bool, set[int]]:
        newly_formed_weights = set()
        current_label = labels[current_v]

        for neighbor in self.adjacency_list[current_v]:
            if neighbor in labels:  # If neighbor is already labeled
                weight = current_label + labels[neighbor]
                if weight in used_edge_weights or weight in newly_formed_weights:
                    return False, set()  # Conflict found
                newly_formed_weights.add(weight)
        return True, newly_formed_weights

    def _solve_recursive(self, v_idx: int, k: int, labels: Dict[Any, int], used_weights: set[int]) -> Optional[Dict[Any, int]]:
        if v_idx == len(self.vertex_order):
            return labels  # All vertices labeled, solution found

        current_v = self.vertex_order[v_idx]

        for label in range(1, k + 1):
            labels[current_v] = label
            is_valid, newly_formed_weights = self._is_assignment_valid(current_v, labels, used_weights)

            if is_valid:
                # Add newly formed weights to the set for the recursive call
                updated_used_weights = used_weights.union(newly_formed_weights)
                result = self._solve_recursive(v_idx + 1, k, labels, updated_used_weights)
                if result is not None:
                    return result  # Solution found

            # Backtrack: remove the current label and newly formed weights
            del labels[current_v]
            # No need to remove from used_weights as we pass a new set to recursive calls

        return None

    def find_es(self) -> Tuple[Optional[int], Optional[Dict[Any, int]]]:
        k_min = calculate_lower_bound(self.n)
        k = k_min

        while True:
            print(f"Attempting to find a valid labeling for k = {k} using Branch & Bound...")
            labels: Dict[Any, int] = {}
            used_edge_weights: set[int] = set()
            
            solution = self._solve_recursive(0, k, labels, used_edge_weights)
            
            if solution is not None:
                print(f"Found a valid labeling for k = {k} using Branch & Bound.")
                return k, solution
            k += 1

def find_optimal_k_labeling_circulant(
    n: int,
    r: int,
    *,
    on_step: Optional[Callable[["StepEvent"], None]] = None,
    on_event: Optional[Callable[["StepEvent"], None]] = None,
) -> Tuple[Optional[int], Optional[Dict[Any, int]]]:
    """
    Find the optimal (minimum) k and a valid labeling for a Circulant graph.
    """
    if n <= 0:
        return None, None

    adjacency_list = generate_circulant_graph(n, r)
    if not adjacency_list: # Handle invalid circulant graph parameters
        print(f"Invalid parameters for circulant graph: n={n}, r={r}")
        return None, None

    vertices = sorted(adjacency_list.keys(), key=_get_generic_vertex_sort_key, reverse=True) # Sort for consistent behavior
    
    # Determine a reasonable lower bound for circulant graphs.
    # This might need to be refined based on graph properties.
    # For now, a simple lower bound could be based on max degree or a small constant.
    # For circulant graphs, the degree is (n-1) for K_n, or (n-6) for the modified one.
    # A simple lower bound could be max_degree + 1, or 1 if no edges.
    k = calculate_circulant_lower_bound(n, r) # Use the theoretical lower bound

    while True:
        print(f"Attempting to find a valid labeling for k = {k} for Circulant graph C({n}, {r})...")
        used_weights = _init_used_weights(2 * k + 1)
        callback = on_event if on_event is not None else on_step
        labeling = _backtrack_k_labeling_generic(adjacency_list, k, {}, vertices, used_weights, callback)
        if labeling is not None and is_labeling_valid(adjacency_list, labeling, sort_key_func=_get_generic_vertex_sort_key):
            print(f"Found a valid labeling for k = {k} for Circulant graph C({n}, {r}).")
            return k, labeling
        k += 1

def find_optimal_k_labeling_circulant(
    n: int,
    r: int,
    *,
    on_step: Optional[Callable[["StepEvent"], None]] = None,
    on_event: Optional[Callable[["StepEvent"], None]] = None,
) -> Tuple[Optional[int], Optional[Dict[Any, int]]]:
    """
    Find the optimal (minimum) k and a valid labeling for a Circulant graph.
    """
    if n <= 0:
        return None, None

    adjacency_list = generate_circulant_graph(n, r)
    if not adjacency_list: # Handle invalid circulant graph parameters
        print(f"Invalid parameters for circulant graph: n={n}, r={r}")
        return None, None

    vertices = sorted(adjacency_list.keys(), key=_get_generic_vertex_sort_key, reverse=True) # Sort for consistent behavior
    
    # Determine a reasonable lower bound for circulant graphs.
    # This might need to be refined based on graph properties.
    # For now, a simple lower bound could be based on max degree or a small constant.
    # For circulant graphs, the degree is (n-1) for K_n, or (n-6) for the modified one.
    # A simple lower bound could be max_degree + 1, or 1 if no edges.
    k = calculate_circulant_lower_bound(n, r) # Use the theoretical lower bound

    while True:
        print(f"Attempting to find a valid labeling for k = {k} for Circulant graph C({n}, {r})...")
        used_weights = _init_used_weights(2 * k + 1)
        callback = on_event if on_event is not None else on_step
        labeling = _backtrack_k_labeling_generic(adjacency_list, k, {}, vertices, used_weights, callback)
        if labeling is not None and is_labeling_valid(adjacency_list, labeling, sort_key_func=_get_generic_vertex_sort_key):
            print(f"Found a valid labeling for k = {k} for Circulant graph C({n}, {r}).")
            return k, labeling
        k += 1

def find_optimal_k_labeling(
    graph_type: str,
    graph_params: Dict[str, Any],
    *,
    on_step: Optional[Callable[["StepEvent"], None]] = None,
    on_event: Optional[Callable[["StepEvent"], None]] = None,
) -> Tuple[Optional[int], Optional[Dict[Any, int]]]:
    """
    Find the optimal (minimum) k and a valid labeling for a given graph.

    Args:
        graph_type: The type of graph to generate ("mongolian_tent" or "circulant").
        graph_params: A dictionary of parameters specific to the graph type (e.g., {"n": 5} for Mongolian Tent, {"n": 5, "r": 2} for Circulant).

    Returns:
        A tuple (k, labeling) where k is the minimum label value for which a valid labeling exists and labeling is the mapping.

    References:
        - ai-docs/initial-design/task_2.md (exact solver deliverable)
        - ai-docs/fixes/large_n_solution.md (scaling guidance for large n)
    """
    adjacency_list = {}
    lower_bound = 0
    graph_description = ""

    if graph_type == "mongolian_tent":
        tent_size = graph_params.get("n")
        if tent_size is None or tent_size <= 0:
            return None, None
        adjacency_list = create_mongolian_tent_graph(tent_size)
        lower_bound = calculate_lower_bound(tent_size)
        graph_description = f"Mongolian Tent graph (n={tent_size})"
    elif graph_type == "circulant":
        n = graph_params.get("n")
        r = graph_params.get("r")
        if n is None or r is None or n <= 0 or r <= 0:
            return None, None
        adjacency_list = generate_circulant_graph(n, r)
        if not adjacency_list: # Handle invalid circulant graph parameters
            print(f"Invalid parameters for circulant graph: n={n}, r={r}")
            return None, None
        lower_bound = calculate_circulant_lower_bound(n, r)
        graph_description = f"Circulant graph C({n}, {r})"
    else:
        raise ValueError(f"Unsupported graph type: {graph_type}")

    # Sort vertices for consistent behavior in backtracking
    if graph_type == "circulant":
        vertices = sorted(adjacency_list.keys()) # Circulant graphs often benefit from natural vertex order
    else:
        vertices = sorted(adjacency_list.keys(), key=lambda v: len(adjacency_list[v]), reverse=True)

    k = lower_bound

    while True:
        print(f"Attempting to find a valid labeling for k = {k} for {graph_description}...")
        # Start backtracking with a bit-array mask for possible edge weights (0..2*k)
        used_weights = _init_used_weights(2 * k + 1)
        callback = on_event if on_event is not None else on_step
        labeling = _backtrack_k_labeling_generic(adjacency_list, k, {}, vertices, used_weights, callback)
        if labeling is not None and is_labeling_valid(adjacency_list, labeling, sort_key_func=_get_generic_vertex_sort_key):
            print(f"Found a valid labeling for k = {k} for {graph_description}.")
            return k, labeling
        k += 1

def greedy_k_labeling(
    adjacency_list: Dict[Any, List[Any]],
    k_upper_bound: int,
    attempts: int = GREEDY_ATTEMPTS_DEFAULT,
    *,
    on_step: Optional[Callable[["StepEvent"], None]] = None,
    on_event: Optional[Callable[["StepEvent"], None]] = None,
    failure_counts: Optional[Dict[Any, int]] = None,
    backjumps_allowed: int = 3,
    graph_type: str = "mongolian_tent", # Added graph_type parameter
) -> Optional[Dict[Any, int]]:
    """A more robust greedy solver that makes multiple randomized attempts.

    References:
        - ai-docs/algorithms/heuristic_algorithm.md (multi-attempt heuristic)
        - ai-docs/fixes/fix_greedy_inefficiency.md (shuffle and attempt count tuning)
    """
    import random

    # Pre-calculate degrees for sorting if using failure counts
    degrees = {}
    if failure_counts is not None:
        degrees = {v: len(neighbors) for v, neighbors in adjacency_list.items()}

    for _ in range(attempts):
        if graph_type == "circulant":
            vertices = sorted(adjacency_list.keys()) # Circulant graphs often benefit from natural vertex order
        else: # Default for mongolian_tent and other graphs
            vertices = list(adjacency_list.keys())
            if failure_counts is not None:
                # Sort by failure count (desc), then degree (desc) as a tie-breaker
                vertices.sort(key=lambda v: (failure_counts.get(v, 0), degrees.get(v, 0)), reverse=True)
            else:
                random.shuffle(vertices)

        vertex_labels: dict = {}
        used_weights = [False] * (2 * k_upper_bound + 1)
        vertex_index = 0
        backjumps = 0

        while vertex_index < len(vertices):
            vertex = vertices[vertex_index]
            
            # Find the best label using conflict minimization
            best_label = -1
            min_conflict_score = float('inf')
            conflict_set = set()

            possible_labels = list(range(1, k_upper_bound + 1))
            random.shuffle(possible_labels)

            for label in possible_labels:
                is_valid_label = True
                current_conflict_set = set()
                for neighbor in adjacency_list[vertex]:
                    if neighbor in vertex_labels:
                        weight = label + vertex_labels[neighbor]
                        if used_weights[weight]:
                            is_valid_label = False
                            current_conflict_set.add(neighbor)
                
                if is_valid_label:
                    conflict_score = _calculate_conflict_score(
                        label, vertex, adjacency_list, vertex_labels, used_weights, k_upper_bound
                    )
                    if conflict_score < min_conflict_score:
                        min_conflict_score = conflict_score
                        best_label = label
                else:
                    conflict_set.update(current_conflict_set)

            if best_label != -1:
                vertex_labels[vertex] = best_label
                for neighbor in adjacency_list[vertex]:
                    if neighbor in vertex_labels:
                        weight = best_label + vertex_labels[neighbor]
                        used_weights[weight] = True
                vertex_index += 1
            else:
                # Backjump logic
                if backjumps < backjumps_allowed and conflict_set:
                    # Find the most recently labeled vertex in the conflict set
                    jump_target_index = -1
                    for i in range(vertex_index - 1, -1, -1):
                        if vertices[i] in conflict_set:
                            jump_target_index = i
                            break
                    
                    if jump_target_index != -1:
                        # Unlabel vertices from current back to jump target
                        for i in range(jump_target_index + 1, vertex_index + 1):
                            v_to_unlabel = vertices[i]
                            if v_to_unlabel in vertex_labels:
                                # Un-mark weights
                                for neighbor in adjacency_list[v_to_unlabel]:
                                    if neighbor in vertex_labels and neighbor != v_to_unlabel:
                                        weight = vertex_labels[v_to_unlabel] + vertex_labels[neighbor]
                                        used_weights[weight] = False
                                del vertex_labels[v_to_unlabel]
                        
                        vertex_index = jump_target_index
                        backjumps += 1
                        continue

                # If backjump fails or not allowed, fail the attempt
                if failure_counts is not None:
                    failure_counts[vertex] += 1
                break  # End this attempt

        if len(vertex_labels) == len(vertices):
            if is_labeling_valid(adjacency_list, vertex_labels, sort_key_func=_get_generic_vertex_sort_key):
                return vertex_labels

    return None

# --------------------
# Fast deterministic greedy heuristic (single pass, no random shuffling)
# --------------------


def _first_fit_greedy_k_labeling(
    adjacency_list: Dict[Any, List[Any]],
    k_upper_bound: int,
    *,
    on_step: Optional[Callable[["StepEvent"], None]] = None,
    graph_type: str = "mongolian_tent", # Added graph_type parameter
) -> Optional[Dict[Any, int]]:
    """A single-pass deterministic greedy solver.

    Vertices are processed in descending degree order and assigned the
    smallest label that maintains edge weight uniqueness.

    This trades potentially higher k values for much faster runtimes
    compared to the randomized multi-attempt heuristic.

    References:
        - ai-docs/enhancments/enhancement01_Task_2.md (fast heuristic concept)
    """

    if graph_type == "circulant":
        vertices = sorted(adjacency_list.keys()) # Circulant graphs often benefit from natural vertex order
    else:
        # Order vertices by degree (high -> low) to maximize early pruning.
        vertices = sorted(adjacency_list.keys(), key=lambda v: len(adjacency_list[v]), reverse=True)

    vertex_labels: Dict[Any, int] = {}
    # Initialize used_weights bit-array for incremental conflict checks
    used_weights = [False] * (2 * k_upper_bound + 1)
    for vertex in vertices:
        assigned = False
        for label in range(1, k_upper_bound + 1):
            temp_weights: List[int] = []
            conflict = False
            for neighbor in adjacency_list[vertex]:
                if neighbor in vertex_labels:
                    weight = label + vertex_labels[neighbor]
                    if StepEvent and EventType:
                        _maybe_emit(
                            on_step,
                            StepEvent(
                                EventType.EDGE_WEIGHT_CALCULATED,
                                {"edge": (vertex, neighbor), "weight": weight},
                            ),
                        )
                    if used_weights[weight]:
                        conflict = True
                        break
                    temp_weights.append(weight)
            if not conflict:
                vertex_labels[vertex] = label
                if StepEvent and EventType:
                    _maybe_emit(
                        on_step,
                        StepEvent(EventType.VERTEX_LABELED, {"vertex": vertex, "label": label}),
                    )
                for w in temp_weights:
                    used_weights[w] = True
                assigned = True
                break
        if not assigned:
            return None
    return vertex_labels

def find_feasible_k_labeling(
    graph_type: str,
    graph_params: Dict[str, Any],
    max_k_multiplier: int = MAX_K_MULTIPLIER_DEFAULT,
    num_attempts: int = GREEDY_ATTEMPTS_DEFAULT,
    *,
    algorithm: str = "accurate",
    on_step: Optional[Callable[["StepEvent"], None]] = None,
    on_event: Optional[Callable[["StepEvent"], None]] = None,
) -> Tuple[Optional[int], Optional[Dict[Any, int]]]:
    """
    Find a feasible k-labeling for a given graph using a heuristic search.

    Args:
        graph_type: The type of graph to generate ("mongolian_tent" or "circulant").
        graph_params: A dictionary of parameters specific to the graph type (e.g., {"n": 5} for Mongolian Tent, {"n": 5, "r": 2} for Circulant).
        max_k_multiplier: multiplier to set an upper bound on k based on the lower bound.
        num_attempts: number of randomized greedy attempts per k value.

    Returns:
        A tuple (k, labeling) with a valid labeling found, or (None, None) if none is found within bounds.

    References:
        - ai-docs/algorithms/heuristic_algorithm.md (search strategy)
        - ai-docs/enhancments/enhancement01_Task_3.md (fast vs accurate modes)
    """
    adjacency_list = {}
    lower_bound = 0
    graph_description = ""

    if graph_type == "mongolian_tent":
        tent_size = graph_params.get("n")
        if tent_size is None or tent_size <= 0:
            return None, None
        adjacency_list = create_mongolian_tent_graph(tent_size)
        lower_bound = calculate_lower_bound(tent_size)
        graph_description = f"Mongolian Tent graph (n={tent_size})"
    elif graph_type == "circulant":
        n = graph_params.get("n")
        r = graph_params.get("r")
        if n is None or r is None or n <= 0 or r <= 0:
            return None, None
        adjacency_list = generate_circulant_graph(n, r)
        if not adjacency_list: # Handle invalid circulant graph parameters
            print(f"Invalid parameters for circulant graph: n={n}, r={r}")
            return None, None
        lower_bound = calculate_circulant_lower_bound(n, r)
        graph_description = f"Circulant graph C({n}, {r})"
    else:
        raise ValueError(f"Unsupported graph type: {graph_type}")

    if max_k_multiplier < 1:
        raise ValueError("max_k_multiplier must be at least 1")

    k = lower_bound
    k_upper_bound = lower_bound * max_k_multiplier  # safety upper limit

    # Initialize failure counts for conflict-guided vertex ordering in 'accurate' mode
    failure_counts = {v: 0 for v in adjacency_list}

    print(
        f"\n[Heuristic Search] Starting search for {graph_description} from k={lower_bound} (limit: k={k_upper_bound}) using '{algorithm}' heuristic..."
    )


    while k <= k_upper_bound:
        if algorithm == "fast":
            if k == lower_bound or k % 10 == 0:
                print(f"Attempting fast greedy solve for k={k} (multi-pass)...")

            # 1) Deterministic first-fit pass (very quick)
            callback = on_event if on_event is not None else on_step
            labeling = _first_fit_greedy_k_labeling(adjacency_list, k, on_step=callback, graph_type=graph_type)
            if labeling and is_labeling_valid(adjacency_list, labeling, sort_key_func=_get_generic_vertex_sort_key):
                print(f"Fast heuristic found a valid labeling with k={k} for {graph_description} on deterministic pass.")
                return k, labeling

            # 2) Limited randomized passes correlated to n to improve accuracy without large slowdown.
            passes = max(2, min(10, tent_size // 2))  # e.g., n=5 ⇒ 2 passes, n=20 ⇒ 10 passes cap.
            for _ in range(passes):
                callback = on_event if on_event is not None else on_step
                labeling = greedy_k_labeling(
                    adjacency_list,
                    k,
                    attempts=1,
                    on_event=callback,
                    graph_type=graph_type,
                )
                if labeling and is_labeling_valid(adjacency_list, labeling, sort_key_func=_get_generic_vertex_sort_key):
                    print(
                        f"Fast heuristic found a valid labeling with k={k} for {graph_description} after randomized pass."
                    )
                    return k, labeling
        else:  # accurate / default multi-attempt heuristic
            if k == lower_bound or k % 10 == 0:
                print(f"Attempting randomized greedy solve for k={k} ({num_attempts} attempts)...")
            callback = on_event if on_event is not None else on_step
            labeling = greedy_k_labeling(
                adjacency_list,
                k,
                attempts=num_attempts,
                on_event=callback,
                failure_counts=failure_counts,
                graph_type=graph_type,
            )
            if labeling and is_labeling_valid(adjacency_list, labeling, sort_key_func=_get_generic_vertex_sort_key):
                print(f"Heuristic search found a valid labeling with k={k} for {graph_description}.")
                return k, labeling
        k += 1
    print(
        f"Heuristic search failed to find a solution for {graph_description} within the k limit (k>{k_upper_bound})."
    )
    return None, None

def _calculate_conflict_score(
    label: int,
    vertex: Any,
    adjacency_list: Dict[Any, List[Any]],
    vertex_labels: Dict[Any, int],
    used_weights: List[bool],
    k_upper_bound: int,
) -> int:
    """
    Calculates the conflict score for a potential label.
    The score is the sum of how many label choices are eliminated for all unassigned neighbors.
    A lower score is better.
    """
    conflict_score = 0
    # For each unassigned neighbor, count how many of its potential labels would become invalid.
    for neighbor in adjacency_list[vertex]:
        if neighbor not in vertex_labels:  # Unassigned neighbor
            # For this neighbor, iterate through all its possible labels
            for neighbor_label in range(1, k_upper_bound + 1):
                weight = label + neighbor_label
                # If this weight is already used somewhere in the graph,
                # then this `neighbor_label` is not a valid choice for `neighbor` anymore.
                if weight < len(used_weights) and used_weights[weight]:
                    conflict_score += 1
    return conflict_score