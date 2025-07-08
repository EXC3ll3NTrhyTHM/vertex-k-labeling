# Addressing Large 'n' in Mongolian Tent Graph K-Labeling

## The Problem: Computational Infeasibility for Exact Solutions

As the size parameter 'n' for the Mongolian Tent Graph \(MT_{3,n}\) increases, finding the **minimum k-labeling** using our current backtracking algorithm becomes computationally infeasible. This is due to the exponential growth of the search space.

- **Exponential Complexity**: The backtracking algorithm explores a vast number of possible label assignments. For even moderately larger 'n' values (e.g., n=8), the number of combinations becomes astronomical, making a complete search impractical, potentially taking years or centuries.

- **Observation from Small 'n'**: Even a small increase from n=3 to n=5 resulted in a significant increase in runtime, indicating the rapid escalation of computational demand.

| n   | Vertices | Edges | Lower Bound (k) | Rough Search Space (k^V) |
|-----|----------|-------|-----------------|--------------------------|
| 3   | 7        | 10    | 6               | ~ \( 6^7 \)              |
| 5   | 11       | 18    | 10              | ~ \( 10^{11} \)          |
| 8   | 17       | 30    | 16              | ~ \( 16^{17} \)          |
| 30  | 61       | 118   | 60              | ~ \( 60^{61} \)          |

## The Solution: Heuristic Approach for Feasible Solutions

Since finding the absolute minimum 'k' is impractical for large 'n', we shift our goal to finding a **feasible 'k'** (a valid labeling) within a reasonable timeframe. This is achieved using an iterative greedy heuristic.

### High-Level Overview of the Heuristic Solution

1.  **New Heuristic Solver Function**: A new function, `find_heuristic_labeling`, has been implemented in `src/labeling_solver.py` specifically for handling large 'n' values.

2.  **Iterative Greedy Search**: This function leverages the existing `greedy_labeling_solver`:
    *   It starts by setting `k` to the theoretical lower bound.
    *   It then iteratively calls `greedy_labeling_solver` with the current `k`.
    *   If `greedy_labeling_solver` finds a valid labeling, that `k` and labeling are returned.*   If it fails (returns `None`), `k` is incremented, and the process repeats.

3.  **Reasonable Upper Limit**: To prevent indefinite execution, the iterative search has a safety limit, ensuring `k` does not exceed a specified multiple of the lower bound (e.g., 5 times the lower bound).

This heuristic approach sacrifices guaranteed optimality for practical solvability, allowing us to obtain valid k-labelings for much larger Mongolian Tent graphs. 