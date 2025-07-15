# Enhancement Proposal: Vertex K-Labeling for Circulant Graphs

## 1. Introduction

This document outlines the necessary changes to extend the existing vertex k-labeling functionality to support circulant graphs. The goal is to enable the calculation of k-labelings for circulant graphs and to visualize these labelings, including both vertex labels and edge weights, using the existing visualization tools.

## 2. Current Limitations

The current k-labeling solvers (`find_optimal_k_labeling`, `greedy_k_labeling`, `_first_fit_greedy_k_labeling`) in `src/labeling_solver.py` are tightly coupled to the `create_mongolian_tent_graph` function and the specific vertex naming conventions (e.g., `('x')`, `(row, col)`) of Mongolian Tent graphs. This prevents their direct application to other graph types, such as circulant graphs, which use integer vertex IDs.

## 3. Proposed Changes

To address these limitations, the following modifications are proposed:

### 3.1. Generalize K-Labeling Solvers (`src/labeling_solver.py`)

The core logic of the k-labeling algorithms (backtracking and greedy) needs to be generalized to operate on any arbitrary graph represented by an adjacency list. This involves:

*   **Creating a new solver function for Circulant Graphs**: Introduce a new function, e.g., `find_k_labeling_circulant(n: int, r: int, algorithm: str = "optimal") -> Tuple[Optional[int], Optional[Dict[Any, int]]]`, which will:
    *   Call `graph_generator.generate_circulant_graph(n, r)` to obtain the circulant graph.
    *   Adapt the existing `_backtrack_k_labeling` and `greedy_k_labeling` functions (or create new, generalized versions) to accept a generic adjacency list and a list of vertices.
    *   The `_get_vertex_sort_key` function will need to be updated or a new one created to handle integer vertex IDs for circulant graphs.
    *   The `is_labeling_valid` function is already generic enough to handle any vertex type, so no changes are needed there.
*   **Refactor `_backtrack_k_labeling` and `greedy_k_labeling`**: These functions should be modified to accept a `graph` (adjacency list) and `vertices` (list of vertex IDs) as direct arguments, rather than implicitly relying on `create_mongolian_tent_graph`. This will make them reusable for different graph types.

### 3.2. Visualization Enhancements (`src/visualization/static.py`)

The `visualize_k_labeling` function already supports displaying vertex labels and edge weights. However, for circulant graphs, the layout needs to be adjusted:

*   **Layout for Circulant Graphs**: When visualizing circulant graphs, the `shaped` parameter in `visualize_k_labeling` should be set to `False` to utilize a circular layout (e.g., using the `neato` or `circo` engine in Graphviz) which is more appropriate for circulant graphs than the "tent" shape.
*   **Vertex ID Formatting**: Ensure `format_vertex_id` correctly handles integer vertex IDs for circulant graphs. It already uses `str(v)`, which should be sufficient.

## 4. Implementation Details

### 4.1. `src/labeling_solver.py`

```python
# In labeling_solver.py

# ... (existing imports and functions) ...

from src.graph_generator import generate_circulant_graph # New import

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

def _backtrack_k_labeling_generic(
    adjacency_list: Dict[Any, List[Any]],
    max_k_value: int,
    vertex_labels: Dict[Any, int],
    unlabeled_vertices: List[Any],
    used_weights: List[bool],
    on_step: Optional[Callable[["StepEvent"], None]] = None,
) -> Optional[Dict[Any, int]]:
    """
    Generalized recursive backtracking solver.
    (This will replace or be called by the existing _backtrack_k_labeling)
    """
    # ... (existing logic, but using _get_generic_vertex_sort_key for sorting if needed) ...
    if not unlabeled_vertices:
        if is_labeling_valid(adjacency_list, vertex_labels, sort_key_func=_get_generic_vertex_sort_key):
            return vertex_labels
        return None

    vertex_to_label = unlabeled_vertices[0]
    remaining_vertices = unlabeled_vertices[1:]

    for label in range(1, max_k_value + 1):
        # ... (rest of the logic, ensuring it's generic) ...
        vertex_labels[vertex_to_label] = label
        new_weights: List[int] = []
        conflict = False
        for neighbor in adjacency_list[vertex_to_label]:
            if neighbor in vertex_labels:
                weight = label + vertex_labels[neighbor]
                if weight < len(used_weights) and used_weights[weight]:
                    conflict = True
                    break
                new_weights.append(weight)
        if not conflict:
            for w in new_weights:
                used_weights[w] = True

            result = _backtrack_k_labeling_generic(
                adjacency_list,
                max_k_value,
                vertex_labels,
                remaining_vertices,
                used_weights,
                on_step,
            )
            if result is not None:
                return result
            for w in new_weights:
                used_weights[w] = False
    del vertex_labels[vertex_to_label]
    return None


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
    max_degree = max((len(adj) for adj in adjacency_list.values()), default=0)
    k = max_degree + 1 if max_degree > 0 else 1 # A very basic lower bound

    while True:
        print(f"Attempting to find a valid labeling for k = {k} for Circulant graph C({n}, {r})...")
        used_weights = _init_used_weights(2 * k + 1)
        callback = on_event if on_event is not None else on_step
        labeling = _backtrack_k_labeling_generic(adjacency_list, k, {}, vertices, used_weights, callback)
        if labeling is not None and is_labeling_valid(adjacency_list, labeling, sort_key_func=_get_generic_vertex_sort_key):
            print(f"Found a valid labeling for k = {k} for Circulant graph C({n}, {r}).")
            return k, labeling
        k += 1

# Modify is_labeling_valid to accept a sort_key_func
def is_labeling_valid(adjacency_list: Dict[Any, List[Any]], vertex_labels: Dict[Any, int], last_vertex: Optional[Any] = None, sort_key_func: Callable[[Any], Tuple[int, ...]] = _get_vertex_sort_key) -> bool:
    """
    Check if the current labeling is valid for the graph.
    (Existing logic, but use sort_key_func for vertex comparisons)
    """
    if last_vertex is not None:
        # ... (existing logic, replace _get_vertex_sort_key with sort_key_func) ...
        if last_vertex not in vertex_labels:
            return True
        last_label = vertex_labels[last_vertex]
        existing_weights: set[int] = set()
        for source_vertex, neighbors in adjacency_list.items():
            if source_vertex == last_vertex or source_vertex not in vertex_labels:
                continue
            for target_vertex in neighbors:
                if target_vertex != last_vertex and target_vertex in vertex_labels:
                    if sort_key_func(source_vertex) < sort_key_func(target_vertex):
                        existing_weights.add(vertex_labels[source_vertex] + vertex_labels[target_vertex])
        for neighbor in adjacency_list[last_vertex]:
            if neighbor in vertex_labels:
                weight = last_label + vertex_labels[neighbor]
                if weight in existing_weights:
                    return False
                existing_weights.add(weight)
        return True

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

```

### 4.2. `src/visualization/static.py`

```python
# In visualization/static.py

# ... (existing imports and functions) ...

def visualize_k_labeling(
    graph: Dict[Any, list],
    labeling: Dict[Any, int],
    output: str = "graph.png",
    validate: bool = False,
    *,
    shaped: bool = True, # This parameter will be used to control layout
    heuristic_k: int | None = None,
    lower_bound_k: int | None = None,
    gap: int | str | None = None,
    time_taken: float | None = None,
    solver_name: str | None = None,
) -> Path:
    # ... (existing validation and path setup) ...

    # Use 'dot' for shaped (Mongolian Tent) layouts and 'neato' or 'circo' for circulant radial layouts
    engine = "dot" if shaped else "neato" # Changed to neato for circulant
    dot = Graph(format=fmt, engine=engine)  # type: ignore
    if shaped:
        dot.attr(rankdir="TB")
    else: # For circulant graphs, set up a circular layout
        dot.attr(overlap="false", splines="true", sep="0.5", K="0.6") # Adjust these for better layout

    # ... (existing global label for graph) ...

    dot.attr("node", shape="circle", style="filled", color="#D5E8D4")

    if shaped:
        # ... (existing shaped graph rendering logic) ...
        # This part handles the specific layout for Mongolian Tent graphs
        pass
    else:
        # New logic for circulant graph layout (circular)
        import math

        node_ids = sorted([v for v in graph.keys() if isinstance(v, int)]) # Assuming integer vertex IDs for circulant
        n_nodes = len(node_ids)
        radius = 2.0  # arbitrary radius, adjust as needed
        for idx, v in enumerate(node_ids):
            angle = 2 * math.pi * idx / n_nodes
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            # pos attribute with ! to fix position
            dot.node(format_vertex_id(v), label=f"{labeling.get(v, '')}", pos=f"{x},{y}!") # Use labeling.get(v, '') for label
            # Add vertex labels
            dot.node(format_vertex_id(v), label=f"{labeling.get(v, '')}")


    # Add edges with weights (this part is already generic and should work)
    added: set[tuple] = set()
    for u, neighbors in graph.items():
        for v in neighbors:
            if (v, u) in added:
                continue
            added.add((u, v))
            if u in labeling and v in labeling:
                weight = labeling[u] + labeling[v]
                dot.edge(format_vertex_id(u), format_vertex_id(v), label=str(weight))
            else:
                dot.edge(format_vertex_id(u), format_vertex_id(v))

    # ... (rest of the function) ...
    rendered_path = Path(dot.render(filename=dest_path.stem, directory=dest_path.parent, cleanup=True))
    return rendered_path

```

## 5. Testing

*   **Unit Tests**: Add new unit tests for `find_k_labeling_circulant` to verify its correctness for various circulant graph parameters.
*   **Integration Tests**: Create integration tests that generate a circulant graph, find its k-labeling, and then visualize it, asserting that the output image is created and contains the expected elements (vertex labels, edge weights).

## 6. Future Considerations

*   **Heuristic Solvers for Circulant Graphs**: Extend the `greedy_k_labeling` and `_first_fit_greedy_k_labeling` to also accept generic adjacency lists, allowing for heuristic solutions for circulant graphs.
*   **Performance Optimization**: For larger circulant graphs, investigate performance optimizations for the k-labeling algorithms.
*   **Lower Bound Calculation**: Research and implement more accurate lower bound calculations for k-labeling of circulant graphs to improve solver efficiency.

