# Performance Enhancement for Graph Data Structures

## 1. Objective

This document details a series of performance-oriented refactors for the graph data structures used in the k-labeling project. The goal is to significantly improve the speed and reduce the memory consumption of the graph solvers, especially for larger graphs (e.g., n > 30), by transitioning from dictionary-based structures to more efficient array-based (list) structures.

## 2. Analysis of Current State

The existing implementation, as described in `graph_data_structure.md`, uses Python dictionaries for core data structures to accommodate non-integer vertex identifiers (e.g., `(1, 1)` for Ladder Graphs).

-   `adjacency_list`: `collections.defaultdict(list)` mapping a vertex ID to a list of neighbor IDs.
-   `vertex_labels`: `dict` mapping a vertex ID to its integer label.

**Primary Bottleneck:** The use of dictionaries, while flexible, introduces significant performance overhead compared to native lists:

-   **Slower Access:** Dictionary lookups require key hashing, which is slower than direct `O(1)` integer indexing into a list.
-   **Higher Memory Usage:** Dictionaries have a larger memory footprint than lists.
-   **Poor Cache Locality:** The labels and graph structure are in separate memory locations. Accessing a neighbor's label requires at least two separate lookups, which can lead to cache misses.

## 3. Proposed Enhancements

The core enhancement is to map all vertex identifiers to a contiguous integer range `[0, n-1]`, which enables the use of high-performance lists for all core data.

### Enhancement 1: Implement Integer Vertex Mapping (Foundational Change)

**Concept:**
Introduce a mapping layer that translates arbitrary vertex identifiers (like tuples or strings) into unique integers from 0 to n-1. This mapping will be created once when a graph is generated and used throughout the solving process.

**Rationale:**
This is the foundational change that enables all other performance improvements. By ensuring all vertex IDs are integers in a contiguous range, we can replace slow, memory-heavy dictionaries with fast, lightweight lists.

**Implementation Guide:**

1.  Locate the graph generation functions in `src/graph_generator.py`.
2.  Modify each generator function (e.g., `generate_ladder_graph`, `create_mongolian_tent_graph`, `generate_circulant_graph`) to perform the following:
    -   As vertices are created, build two mapping dictionaries:
        -   `node_to_int`: Maps the original vertex ID to its new integer ID.
        -   `int_to_node`: Maps the new integer ID back to the original ID (for final output).
    -   The function should now return a tuple containing the adjacency list, the `node_to_int` map, and the `int_to_node` map.

**Affected Code Locations:**

-   **Primary Target:** `src/graph_generator.py`. All graph generation functions must be updated.
-   **Consumers:** Any script that calls these generator functions will need to be updated to handle the new return signature.

**Example: Before vs. After in `generate_ladder_graph`**

**Before:**

```python
# Returns a dictionary-based adjacency list
def generate_ladder_graph(n):
    adj = defaultdict(list)
    # ... logic using tuple keys like (1, 1) ...
    return adj
```

**After:**

```python
# Returns an integer-based adj list and the mappings
def generate_ladder_graph(n):
    adj_dict = defaultdict(list)
    # ... existing logic to build adj_dict ...

    # --- New Mapping Logic ---
    nodes = sorted(adj_dict.keys()) # Ensure consistent ordering
    node_to_int = {node: i for i, node in enumerate(nodes)}
    int_to_node = {i: node for i, node in enumerate(nodes)}

    # --- New List-based Adjacency List ---
    num_vertices = len(nodes)
    adj_list = [[] for _ in range(num_vertices)]
    for node, neighbors in adj_dict.items():
        node_int = node_to_int[node]
        for neighbor in neighbors:
            adj_list[node_int].append(node_to_int[neighbor])

    return adj_list, node_to_int, int_to_node
```

### Enhancement 2: Convert Core Data Structures to Lists

**Concept:**
With the integer mapping in place, replace the dictionary-based `adjacency_list` and `vertex_labels` with simple Python lists.

**Rationale:**
This directly addresses the performance bottlenecks. List indexing is `O(1)` and significantly faster than dictionary lookups. Memory usage will be reduced, and data locality will be improved, leading to better cache performance.

**Implementation Guide:**

-   This change affects all solver algorithms (BranchAndBoundSolver, greedy, backtracking, etc.).
-   The solvers should now expect the graph and labels in list format.
-   Update all data access patterns.

**Affected Code Locations:**

-   All solver implementation files.
-   Any utility function that interacts with the graph structure or labels.

**Example: Before vs. After in a Solver**

**Before (Dictionary-based):**

```python
# adj and vertex_labels are dictionaries
neighbor_id = adj[current_vertex_id][0]
neighbor_label = vertex_labels[neighbor_id]
```

**After (List-based):**

```python
# adj and vertex_labels are lists, IDs are integers
neighbor_int_id = adj[current_vertex_int_id][0]
neighbor_label = vertex_labels[neighbor_int_id]
```

### Enhancement 3: Implement Hybrid Edge Weight Tracking

**Concept:**
Combine the speed of a boolean array (bitmask) with the memory flexibility of a `set` for tracking used edge weights.

**Rationale:**
The existing bitmask approach is fast but can cause extreme memory allocation if a single large weight is encountered. A `set` is flexible but slower. A hybrid approach offers the best of both worlds.

**Implementation Guide:**

1.  In the solver classes, define a constant for the size of the fast-access bitmask, e.g., `FAST_WEIGHT_LIMIT = 4 * num_vertices`.
2.  Initialize both a boolean list and a set:
    -   `used_weights_fast = [False] * FAST_WEIGHT_LIMIT`
    -   `used_weights_slow = set()`
3.  Create helper methods to encapsulate the logic for checking and adding weights.

**Affected Code Locations:**

-   The `__init__` method and the core recursive/iterative loops of all solver classes.

**Example: Before vs. After in a Solver**

**Before (Bitmask only):**

```python
# In solver loop
if used_weights[new_weight]:
    # Conflict found
used_weights[new_weight] = True
```

**After (Hybrid):**

```python
# Can be encapsulated in a helper class/methods
def is_weight_used(weight):
    if weight < FAST_WEIGHT_LIMIT:
        return used_weights_fast[weight]
    else:
        return weight in used_weights_slow

def add_weight(weight):
    if weight < FAST_WEIGHT_LIMIT:
        used_weights_fast[weight] = True
    else:
        used_weights_slow.add(weight)

# In solver loop
if is_weight_used(new_weight):
    # Conflict found
add_weight(new_weight)
```

## 4. Summary of Data Structure Changes

| Data Structure  | Before (dict-based)             | After (list-based)                                  |
| --------------- | ------------------------------- | --------------------------------------------------- |
| Adjacency List  | `defaultdict(list)`             | `list[list[int]]`                                   |
| Vertex Labels   | `dict`                          | `list[int]`                                         |
| Edge Weights    | `set` OR `list[bool]` (Bitmask) | Hybrid: `list[bool]` (for common) + `set` (for outliers) |

By implementing these changes, the solvers will be fundamentally more performant and capable of handling much larger graph instances efficiently.
