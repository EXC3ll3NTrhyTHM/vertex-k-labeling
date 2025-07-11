# Edge Irregular K-Labeling for Mongolian Tent Graph

## Overview

This algorithm labels the vertices of a Mongolian tent graph such that **all edge weights are unique**, where edge weight is defined as the sum of its two endpoint labels.

## Input

- Graph `G = (V, E)`:  
  - `V`: Set of vertices  
  - `E`: Set of edges
- `n`: Number of vertices

## Output

- `V_labels`: Array of vertex labels with minimal `k` such that edge weights are unique.
- `k`: Maximum label used.

## Algorithm

1. **Initialize**
   - Start with `V_labels` as an empty array or zeros of size `n`.
   - Set `available_labels` to the set `{1, 2, ..., n}` or an expanding pool if needed.

2. **Recursive Backtracking Label Assignment**
   - Define a recursive function `assign_label(node_index)`:
     1. If `node_index == n`, return `True` (all nodes labeled).
     2. For each label `l` in `available_labels`:
        - Assign `V_labels[node_index] = l`.
        - Compute all edge weights involving this node:
          - For each neighbor `j` of `node_index` already labeled:
            - Compute `weight = l + V_labels[j]`.
        - Check **global edge weight uniqueness**:
          - If duplicate weight found:
            - Continue to next label.
        - Else:
          - Recurse with `assign_label(node_index + 1)`.
          - If recursion succeeds, return `True`.
        - Unassign `V_labels[node_index]` (backtrack).

3. **Start**
   - Call `assign_label(0)` to begin labeling from the first node.

4. **Return**
   - `V_labels` containing the valid labeling.
   - `k = max(V_labels)`.

## Notes

- **Order of labeling** matters. Try starting with the apex node to reduce branching complexity.
- Maintain a **global set of used edge weights** to efficiently check uniqueness.
- Use **heuristics** to select the next node (e.g. highest degree node first) for faster convergence.

## Complexity

- Worst case is exponential (backtracking over all label permutations), but practical performance is acceptable for graphs of size ≤ 100 with pruning.

## Extensions

- If minimal `k` is desired, implement a **binary search on k**:
  - Set lower bound to max degree, upper bound to n.
  - Check feasibility for each mid-point until minimal k found.

---

Prepared for integration with your coding agent to implement edge irregular k-labeling for Mongolian tent graphs efficiently.

---

Let me know if you need a Python starter script for this algorithm implementation.

