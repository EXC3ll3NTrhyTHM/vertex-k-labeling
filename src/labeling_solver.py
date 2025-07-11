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
from src.graph_generator import create_mongolian_tent_graph
from src.graph_properties import calculate_lower_bound
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

def is_labeling_valid(adjacency_list: Dict[Any, List[Any]], vertex_labels: Dict[Any, int], last_vertex: Optional[Any] = None) -> bool:
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
                    if _get_vertex_sort_key(source_vertex) < _get_vertex_sort_key(target_vertex):
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
            if target_vertex in vertex_labels and _get_vertex_sort_key(source_vertex) < _get_vertex_sort_key(target_vertex):
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

def _backtrack_k_labeling(
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
        if is_labeling_valid(adjacency_list, vertex_labels):
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
            result = _backtrack_k_labeling(
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

def find_optimal_k_labeling(
    tent_size: int,
    *,
    on_step: Optional[Callable[["StepEvent"], None]] = None,
    on_event: Optional[Callable[["StepEvent"], None]] = None,
) -> Tuple[Optional[int], Optional[Dict[Any, int]]]:
    """
    Find the optimal (minimum) k and a valid labeling for the Mongolian Tent graph MT_3,n.

    Args:
        tent_size: size parameter for the Mongolian Tent graph.

    Returns:
        A tuple (k, labeling) where k is the minimum label value for which a valid labeling exists and labeling is the mapping.

    References:
        - ai-docs/initial-design/task_2.md (exact solver deliverable)
        - ai-docs/fixes/large_n_solution.md (scaling guidance for large n)
    """
    if tent_size <= 0:
        return None, None

    adjacency_list = create_mongolian_tent_graph(tent_size)
    # Sort vertices by degree (descending) to prune the search space
    vertices = sorted(adjacency_list.keys(), key=lambda v: len(adjacency_list[v]), reverse=True)
    k = calculate_lower_bound(tent_size)

    while True:
        print(f"Attempting to find a valid labeling for k = {k}...")
        # Start backtracking with a bit-array mask for possible edge weights (0..2*k)
        used_weights = _init_used_weights(2 * k + 1)
        callback = on_event if on_event is not None else on_step
        labeling = _backtrack_k_labeling(adjacency_list, k, {}, vertices, used_weights, callback)
        if labeling is not None and is_labeling_valid(adjacency_list, labeling):
            print(f"Found a valid labeling for k = {k}")
            return k, labeling
        k += 1

def greedy_k_labeling(
    adjacency_list: Dict[Any, List[Any]],
    k_upper_bound: int,
    attempts: int = GREEDY_ATTEMPTS_DEFAULT,
    *,
    on_step: Optional[Callable[["StepEvent"], None]] = None,
    on_event: Optional[Callable[["StepEvent"], None]] = None,
) -> Optional[Dict[Any, int]]:
    """A more robust greedy solver that makes multiple randomized attempts.

    References:
        - ai-docs/algorithms/heuristic_algorithm.md (multi-attempt heuristic)
        - ai-docs/fixes/fix_greedy_inefficiency.md (shuffle and attempt count tuning)
    """
    import random
    for _ in range(attempts):
        vertices = list(adjacency_list.keys())
        random.shuffle(vertices)
        vertex_labels: dict = {}
        # Initialize used_weights bit-array for incremental conflict checks
        used_weights = [False] * (2 * k_upper_bound + 1)
        success = True
        for vertex in vertices:
            labels = list(range(1, k_upper_bound + 1))
            random.shuffle(labels)
            assigned = False
            for label in labels:
                temp_weights: List[int] = []
                conflict = False
                for neighbor in adjacency_list[vertex]:
                    if neighbor in vertex_labels:
                        weight = label + vertex_labels[neighbor]
                        if StepEvent and EventType:
                            _maybe_emit(
                                on_event,
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
                            on_event,
                            StepEvent(EventType.VERTEX_LABELED, {"vertex": vertex, "label": label}),
                        )
                    for w in temp_weights:
                        used_weights[w] = True
                    assigned = True
                    break
            if not assigned:
                success = False
                break
        if success:
            # Verify the final labeling is truly valid (no duplicate edge weights)
            if is_labeling_valid(adjacency_list, vertex_labels):
                if StepEvent and EventType:
                    _maybe_emit(on_event, StepEvent(EventType.SOLUTION_FOUND, {"labels": vertex_labels}))
                return vertex_labels
            # Otherwise, discard and continue attempts
    return None

# --------------------
# Fast deterministic greedy heuristic (single pass, no random shuffling)
# --------------------


def _first_fit_greedy_k_labeling(
    adjacency_list: Dict[Any, List[Any]],
    k_upper_bound: int,
    *,
    on_step: Optional[Callable[["StepEvent"], None]] = None,
) -> Optional[Dict[Any, int]]:
    """A single-pass deterministic greedy solver.

    Vertices are processed in descending degree order and assigned the
    smallest label that maintains edge weight uniqueness.

    This trades potentially higher k values for much faster runtimes
    compared to the randomized multi-attempt heuristic.

    References:
        - ai-docs/enhancments/enhancement01_Task_2.md (fast heuristic concept)
    """

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
    tent_size: int,
    max_k_multiplier: int = MAX_K_MULTIPLIER_DEFAULT,
    num_attempts: int = GREEDY_ATTEMPTS_DEFAULT,
    *,
    algorithm: str = "accurate",
    on_step: Optional[Callable[["StepEvent"], None]] = None,
    on_event: Optional[Callable[["StepEvent"], None]] = None,
) -> Tuple[Optional[int], Optional[Dict[Any, int]]]:
    """
    Find a feasible k-labeling for the Mongolian Tent graph using a heuristic search.

    Args:
        tent_size: the size parameter for the Mongolian Tent graph.
        max_k_multiplier: multiplier to set an upper bound on k based on the lower bound.
        num_attempts: number of randomized greedy attempts per k value.

    Returns:
        A tuple (k, labeling) with a valid labeling found, or (None, None) if none is found within bounds.

    References:
        - ai-docs/algorithms/heuristic_algorithm.md (search strategy)
        - ai-docs/enhancments/enhancement01_Task_3.md (fast vs accurate modes)
    """
    if tent_size <= 0:
        return None, None
    if max_k_multiplier < 1:
        raise ValueError("max_k_multiplier must be at least 1")

    adjacency_list = create_mongolian_tent_graph(tent_size)
    lower_bound = calculate_lower_bound(tent_size)
    k = lower_bound
    k_upper_bound = lower_bound * max_k_multiplier  # safety upper limit

    print(
        f"\n[Heuristic Search] Starting search for n={tent_size} from k={lower_bound} (limit: k={k_upper_bound}) using '{algorithm}' heuristic..."
    )

    while k <= k_upper_bound:
        if algorithm == "fast":
            if k == lower_bound or k % 10 == 0:
                print(f"Attempting fast greedy solve for k={k} (multi-pass)...")

            # 1) Deterministic first-fit pass (very quick)
            callback = on_event if on_event is not None else on_step
            labeling = _first_fit_greedy_k_labeling(adjacency_list, k, on_step=callback)
            if labeling and is_labeling_valid(adjacency_list, labeling):
                print(f"Fast heuristic found a valid labeling with k={k} for n={tent_size} on deterministic pass.")
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
                )
                if labeling and is_labeling_valid(adjacency_list, labeling):
                    print(
                        f"Fast heuristic found a valid labeling with k={k} for n={tent_size} after randomized pass."
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
            )
            if labeling and is_labeling_valid(adjacency_list, labeling):
                print(f"Heuristic search found a valid labeling with k={k} for n={tent_size}.")
                return k, labeling
        k += 1
    print(
        f"Heuristic search failed to find a solution for n={tent_size} within the k limit (k>{k_upper_bound})."
    )
    return None, None 