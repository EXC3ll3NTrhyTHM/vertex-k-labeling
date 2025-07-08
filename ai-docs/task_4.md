# Task 4: Optimization & Heuristics

## Goal

Implement performance improvements and heuristics for the labeling algorithm to achieve faster execution times and a reduced search space, especially for larger graphs.

## High-Level Plan

1.  **Prioritize Vertex Labeling**: Implement a strategy to label high-degree vertices first.
2.  **Optimize Duplicate Detection**: Refine the duplicate edge weight detection to prune invalid branches earlier in the backtracking process.
3.  **Implement Greedy Heuristic (Optional)**: Develop a greedy approach to find an initial feasible upper bound for `k`, which can potentially speed up the search for the minimum `k`.

---

## Detailed Steps

### 1. Prioritize Vertex Labeling

-   [x] Modify the `find_minimum_k_labeling` function in `src/labeling_solver.py` to sort vertices by their degree in descending order before initiating the backtracking process.
    -   [x] This has already been implemented in `find_minimum_k_labeling` from Task 3.

### 2. Optimize Duplicate Detection

-   [x] Review the `_is_valid_assignment` function in `src/labeling_solver.py`.
-   [x] Consider optimizing the set operations for faster duplicate checks.
    -   [x] Current implementation already uses a `set` for `weights`, which is efficient.
    -   [x] No further changes are immediately required based on the current implementation.

### 3. Implement Greedy Heuristic (Optional)

-   [x] Design a greedy algorithm that attempts to find *any* valid labeling for a potentially higher `k` value, to establish an upper bound.
-   [x] This can be a separate function that the main search function can optionally call before starting the iterative search from the lower bound.
-   [x] Decide if this is necessary based on performance during testing for larger `n` values. 