# Fast Heuristic Algorithm for K-Labeling

## Overview

The "Fast Heuristic" algorithm, implemented in `src/labeling_solver.py` within the `find_feasible_k_labeling` function (when `algorithm="fast"` is specified), is designed to quickly find a feasible k-labeling for Mongolian Tent graphs. It prioritizes speed over finding the absolute optimal `k` value, making it suitable for scenarios where a quick, reasonably good solution is preferred.

This heuristic combines a deterministic first-fit approach with a limited number of randomized greedy attempts.

## Algorithm Breakdown

The `fast` heuristic operates in an iterative manner, incrementing the maximum allowed label value `k` (starting from the calculated lower bound) until a valid labeling is found or an upper bound for `k` is reached. For each `k` value, it performs the following steps:

### 1. Deterministic First-Fit Pass (`_first_fit_greedy_k_labeling`)

This is the primary and fastest component of the `fast` heuristic. It attempts to find a valid labeling using a deterministic greedy strategy:

*   **Vertex Ordering:** Vertices of the graph are sorted in descending order of their degree. This strategy aims to label the most constrained vertices (those with more connections) first, as they are more likely to cause conflicts if labeled late.
*   **Label Assignment:** For each vertex in the sorted order, the algorithm attempts to assign the smallest possible label (starting from 1) that does not create a conflict with already labeled neighbors. A conflict occurs if the sum of the current vertex's label and a neighbor's label results in an edge weight that has already been used by another edge in the graph.
*   **Conflict Checking:** An efficient bit-array (or a list of booleans as a fallback) is used to keep track of used edge weights, allowing for O(1) lookup for conflict detection.
*   **Outcome:** If a valid labeling is found in this pass, it is immediately returned as the solution for the current `k`. If no valid label can be assigned to a vertex, this pass fails for the current `k`.

### 2. Limited Randomized Passes (`greedy_k_labeling` with `attempts=1`)

If the deterministic first-fit pass fails to find a solution for the current `k`, the algorithm proceeds to a limited number of randomized attempts. This step aims to introduce some variability to potentially find a solution that the deterministic approach missed, without significantly impacting performance.

*   **Number of Passes:** The number of randomized passes is dynamically determined based on the `tent_size` (`n`), capped between 2 and 10 passes (e.g., `max(2, min(10, tent_size // 2))`). This ensures that for smaller graphs, only a few random attempts are made, while for larger graphs, a slightly higher (but still limited) number of attempts are performed.
*   **Randomized Vertex Order:** In each randomized pass, the vertices are shuffled into a random order before labeling.
*   **Randomized Label Selection:** For each vertex, the available labels (from 1 to `k`) are also shuffled, and the first valid label from this shuffled list is assigned.
*   **Conflict Checking:** Similar to the deterministic pass, an efficient mechanism (bit-array/boolean list) is used for conflict detection.
*   **Outcome:** If any of these randomized passes successfully finds a valid labeling for the current `k`, it is returned as the solution. If all randomized passes fail, the algorithm increments `k` and repeats the entire process.

## Performance vs. Accuracy Trade-off

The "Fast Heuristic" explicitly trades off potential optimality for speed. The deterministic first-fit pass is extremely fast but may not always find the lowest possible `k`. The subsequent limited randomized passes offer a chance to improve accuracy without incurring the high computational cost of a full multi-attempt randomized heuristic (which would typically run many more attempts per `k` value).

## References

*   `src/labeling_solver.py` (implementation details)
*   `ai-docs/enhancements/improve_fast_heuristic_accuracy.md` (notes on future improvements)
