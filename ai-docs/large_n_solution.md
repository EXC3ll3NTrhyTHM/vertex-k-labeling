# Addressing Large 'n' in Mongolian Tent Graph K-Labeling

## The Problem: Computational Infeasibility for Exact Solutions

As the size parameter 'n' for the Mongolian Tent Graph \(MT_{3,n}\) increases, finding the **minimum k-labeling** using our current backtracking algorithm becomes computationally infeasible. This is due to the exponential growth of the search space.

- **Exponential Complexity**: The backtracking algorithm explores a vast number of possible label assignments. For even moderately larger 'n' values (e.g., n=8), the number of combinations becomes astronomical, making a complete search impractical.
- **Heuristic Failure**: Furthermore, the increased complexity of the three-row graph structure rendered simple, deterministic greedy heuristics ineffective. These methods consistently got stuck in local optima ("greedy traps") and failed to find valid solutions.

| n   | Vertices | Edges | Lower Bound (k) |
|-----|----------|-------|-----------------|
| 3   | 10       | 15    | 6               |
| 5   | 16       | 25    | 14              |
| 8   | 25       | 40    | 27              |
| 30  | 91       | 150   | 149             |

## The Solution: Randomized Heuristic for Feasible Solutions

Since finding the absolute minimum 'k' is impractical and simple heuristics fail, we shift our goal to finding a **feasible 'k'** (a valid labeling) within a reasonable timeframe. The successful approach utilizes a **randomized greedy algorithm**. By introducing randomness into the search process, the solver can explore a much wider variety of potential solutions and escape the local optima that plagued deterministic methods.

### High-Level Overview of the Randomized Heuristic

1.  **Randomized Greedy Solver**: The core `greedy_labeling_solver` was rewritten to be non-deterministic:
    *   It shuffles the order of vertices before processing them.
    *   For each vertex, it shuffles the list of possible labels before attempting to assign one.
    *   This randomization allows the solver to try vastly different paths on each run.

2.  **Iterative, Multi-Attempt Search**: The `find_heuristic_labeling` function orchestrates the search:
    *   It starts with `k` at the theoretical lower bound.
    *   For each value of `k`, it runs the `greedy_labeling_solver` multiple times (e.g., 100 attempts).
    *   If any attempt for a given `k` succeeds, that labeling is returned.
    *   If all attempts for a `k` fail, `k` is incremented, and the process repeats.

3.  **Reasonable Upper Limit**: To prevent indefinite execution, the iterative search still has a safety limit, ensuring `k` does not exceed a specified multiple of the lower bound.

This randomized heuristic approach sacrifices guaranteed optimality for practical solvability, allowing us to obtain valid k-labelings for much larger and more complex Mongolian Tent graphs. 