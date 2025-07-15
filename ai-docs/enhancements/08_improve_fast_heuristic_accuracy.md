# Task: Improve Fast Heuristic Accuracy (without sacrificing performance)

## Objective
Enhance the accuracy of the `fast` heuristic algorithm in `src/labeling_solver.py` to find valid k-labelings with lower `k` values more frequently, while strictly maintaining its current performance characteristics (i.e., avoiding significant increases in runtime).

## Background
The `fast` heuristic currently employs a two-stage approach:
1.  A deterministic `_first_fit_greedy_k_labeling` pass, which prioritizes speed.
2.  A limited number of randomized `greedy_k_labeling` passes (with `attempts=1`), aiming for slight accuracy improvement.

The primary challenge is to improve the quality of the solutions found by these passes without introducing computationally expensive operations.

## Proposed Improvements

### 1. Optimize `_first_fit_greedy_k_labeling` (Deterministic Pass)

This is the fastest component, so any improvements here must be extremely lightweight.

*   **1.1 Smarter Vertex Ordering (Lightweight)**
    *   **Current:** Vertices are sorted by descending degree.
    *   **Consider:** Explore alternative static vertex orderings that might lead to better label assignments. This could involve:
        *   Ordering by degree *and* some measure of "centrality" or "constraint" (e.g., number of unlabeled neighbors).
        *   A fixed, pre-calculated order for specific `n` values if patterns emerge.
    *   **Constraint:** The sorting key calculation must be very fast (e.g., O(V log V) or O(V) if pre-calculated).

*   **1.2 Smarter Label Selection (First-Fit Refinement)**
    *   **Current:** Assigns the smallest valid label (1, 2, 3...).
    *   **Consider:** Instead of strictly first-fit, explore a "least constraining value" approach. This would involve:
        *   For each potential label, quickly estimate how many future conflicts it might create for *unlabeled* neighbors.
        *   Choose the label that minimizes these potential future conflicts.
    *   **Constraint:** This estimation must be extremely fast, perhaps by only considering direct neighbors or a very shallow look-ahead. Avoid full constraint propagation.

### 2. Enhance `greedy_k_labeling` (Randomized Passes - Single Attempt)

The randomized passes currently use `attempts=1`, meaning each pass is a single random permutation. Improving the quality of *each single pass* is key.

*   **2.1 Intelligent Randomization (Vertex Order)**
    *   **Current:** `random.shuffle(vertices)`
    *   **Consider:** Instead of a completely random shuffle, introduce a "biased" randomization. For example:
        *   Randomly select from a small pool of "most constrained" or "highest degree" unlabeled vertices first.
        *   Use a randomized version of the vertex ordering strategy from 1.1.
    *   **Constraint:** The biasing logic must be very fast and not significantly slow down the shuffling or selection process.

*   **2.2 Intelligent Randomization (Label Selection)**
    *   **Current:** `random.shuffle(labels)` then first-fit from shuffled labels.
    *   **Consider:** Similar to 1.2, but applied to the randomized label selection. Instead of a pure random shuffle, prioritize labels that are "less constraining" or "more central" in the remaining label pool.
    *   **Constraint:** Again, this must be a very quick estimation.

### 3. Iterative Refinement (Post-Assignment)

This is a more advanced concept and might impact performance, so it needs careful consideration.

*   **3.1 Local Search (Very Limited)**
    *   **Concept:** After a greedy assignment, if a solution is found, attempt a very small number of local swaps or re-assignments to try and reduce `k` or improve the "quality" of the labeling (e.g., by making it more robust to small changes).
    *   **Constraint:** This would only be applied *after* a valid labeling is found, and the number of iterations/swaps must be extremely small (e.g., 1-2 swaps) to avoid performance degradation. This might be better suited for a separate "refinement" algorithm rather than part of the "fast" heuristic itself.

## Implementation Notes
*   **Profiling:** Before and after each change, rigorously profile the `fast` heuristic to ensure performance is not degraded.
*   **Test Cases:** Focus on test cases where the `fast` heuristic currently yields suboptimal `k` values compared to the optimal or `accurate` heuristic.
*   **Parameter Tuning:** Any new parameters introduced (e.g., for biasing randomization) should be carefully tuned.

## Definition of Done
*   The `fast` heuristic consistently finds valid k-labelings with `k` values closer to the optimal/accurate heuristic for a given set of `n` values.
*   The average runtime of the `fast` heuristic remains within a small percentage (e.g., <10%) of its current average runtime across a representative set of `n` values.
*   All changes are well-documented and adhere to existing code style.
