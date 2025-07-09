# Fix: Inefficient Greedy Validity Checking

## Issue
In the heuristic solvers `greedy_k_labeling` and `_first_fit_greedy_k_labeling`, each attempted label assignment invoked `is_labeling_valid(..., last_vertex=vertex)`. Despite the `last_vertex` parameter aiming for incremental checks, its implementation reconstructed the set of existing edge weights from scratch on every call. This resulted in an O(V+E) scan per label trial within the innermost loop, creating a severe performance bottleneck for larger graphs.

## Root Cause
- **Redundant Full-Graph Scans**: Each label trial rebuilt the entire set of used edge weights by iterating over almost the whole adjacency list.
- **High Overhead in Inner Loop**: These scans ran inside nested loops over vertices and labels, multiplying their cost by O(V×K) label attempts.

## Fix Implemented
1. **Single Initialization of Bit-Array**: Initialize a boolean array `used_weights` of size `(2 * k_upper_bound + 1)` once per solver invocation to track which edge-weight sums are already used.
2. **Inline Conflict Detection**:
   - For each vertex and candidate label, iterate only over its neighbors.
   - Check against `used_weights[weight]` to detect conflicts in O(deg(vertex)) time.
   - Collect new weights in a temporary list without rescanning the entire graph.
3. **Incremental Updates**:
   - On successful label assignment, mark each new weight as used by setting `used_weights[weight] = True`.
   - No need to backtrack `used_weights` on failure in greedy solvers, as they do not recursively undo assignments.

## Summary of Changes
- Removed calls to `is_labeling_valid` in both solvers.
- Added and maintained a shared `used_weights` bit-array.
- Reduced per-trial complexity from O(V+E) to O(deg(vertex)).

## Code Snippet
```python
# Initialization once per attempt:
used_weights = [False] * (2 * k_upper_bound + 1)

# Label assignment loop example:
for vertex in vertices:
    for label in range(1, k_upper_bound + 1):
        temp_weights = []
        conflict = False
        for neighbor in adjacency_list[vertex]:
            if neighbor in vertex_labels:
                weight = label + vertex_labels[neighbor]
                if used_weights[weight]:
                    conflict = True
                    break
                temp_weights.append(weight)
        if not conflict:
            vertex_labels[vertex] = label
            for w in temp_weights:
                used_weights[w] = True
            break
```

## Performance Impact
By eliminating redundant full-graph scans and checking only local neighbors, the greedy solvers now run in O(V×deg_max×K) instead of O(V×(V+E)×K), yielding significant speedups on larger Mongolian Tent graphs. 