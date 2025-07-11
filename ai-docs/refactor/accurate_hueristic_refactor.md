# Refactoring the Accurate Heuristic Algorithm

*Last updated: 2025-07-11*

---

## 1. Motivation

The current "accurate" heuristic algorithm relies on a brute-force randomization strategy: it runs many independent, randomly-ordered greedy passes for each value of *k*. While this approach is simple and parallelizable, its effectiveness is purely a matter of chance. For larger or more complex graphs, this can lead to:

1.  **Sub-optimal *k***: The algorithm may fail to find a valid labeling for a lower *k* that actually exists, settling for a higher, easier-to-find value.
2.  **Wasted Computation**: Many of the random attempts may explore the same unpromising parts of the search space, offering no new information.
3.  **Scaling Issues**: The number of attempts required to find a solution grows significantly with the graph size *n*, making it impractical for very large graphs.

This document proposes a refactoring of the accurate heuristic to incorporate more intelligent search strategies, aiming to improve accuracy and efficiency.

---

## 2. Proposed Enhancements

The core idea is to move from a purely random search to a more informed, guided search. We can achieve this by introducing techniques that learn from the search process and make smarter decisions.

### 2.1. Smarter Vertex Ordering

Instead of a purely random shuffle, we can use a more strategic ordering that prioritizes "difficult" vertices first.

**Proposal: Degree-Biased Random Ordering**

1.  **Primary Sort**: Order vertices by descending degree. This is the strategy used in the "fast" mode and is effective because it tackles the most constrained vertices first.
2.  **Introduce Randomness**: Instead of a strict sort, group vertices into quantiles based on their degree. For example, the top 10% of highest-degree vertices form one group, the next 10% another, and so on.
3.  **Final Order**: The final processing order is determined by picking a random vertex from the highest-degree group, then a random vertex from the second-highest group, and so on. Within each group, the selection is random.

**Benefit**: This maintains the principle of handling high-degree vertices early while still introducing diversity into the search, helping to avoid the pitfalls of a single deterministic order.

### 2.2. Conflict-Directed Label Selection

The current algorithm tries labels `1...k` in a shuffled order. A smarter approach is to choose the label that is least likely to cause future conflicts.

**Proposal: Minimum Conflict Heuristic**

For a given vertex `v`, iterate through all possible labels `1...k`. For each potential label, calculate a "conflict score". This score is the number of newly created duplicate edge weights among the already-labeled neighbors of `v`.

The label chosen is the one with the **minimum conflict score**. Ties can be broken randomly.

**Benefit**: This is a greedy, "best-first" approach that actively tries to steer the search away from invalid states, increasing the probability of finding a valid labeling in a single pass.

### 2.3. Limited Backtracking / Local Search

The current algorithm gives up on an entire attempt if it gets stuck. A more resilient strategy would be to try and "repair" a partial solution.

**Proposal: Local Search Repair**

If the greedy algorithm completes but the labeling is invalid (i.e., there are still conflicting edges), don't discard it immediately. Instead, initiate a local search phase:

1.  **Identify Conflicts**: Identify all vertices involved in an edge weight conflict.
2.  **Iterative Repair**: For a fixed number of iterations (e.g., `10 * n`):
    *   Pick a random vertex `v` from the conflict set.
    *   Re-label `v` using the **Minimum Conflict Heuristic** described in section 2.2.
    *   Update the conflict set.
3.  **Termination**: If the conflict set becomes empty, a valid solution has been found. If the iteration limit is reached, the attempt fails.

**Benefit**: This gives the algorithm a second chance to fix a "nearly good" solution, which is often more efficient than starting over from scratch.

---

## 3. Implementation Plan

1.  **Create a new algorithm mode**: Introduce a new option, e.g., `intelligent` or `accurate-v2`, to the `labeling_solver.py`. This will allow for A/B testing against the existing `accurate` mode.
2.  **Refactor `labeling_solver.py`**:
    *   Implement the **Degree-Biased Random Ordering** logic for vertex selection.
    *   Create a new function for the **Minimum Conflict Heuristic** for label selection.
    *   Add the **Local Search Repair** loop that runs after an initial greedy pass is complete.
3.  **Update Tests**: Create new test cases in `tests/test_heuristic_solver.py` to validate the behavior and performance of the new `intelligent` mode, especially for graphs where the old `accurate` mode is known to be inefficient.

---

## 4. Expected Outcome

*   **Improved Accuracy**: The new heuristic should find lower values of *k* than the purely random approach, given a similar amount of computation time.
*   **Better Scaling**: The algorithm should be more capable of finding solutions for larger graphs (*n* > 200) where the current random search becomes prohibitively slow.
*   **More Consistent Performance**: The results should be less sensitive to the initial random seed, leading to more predictable behavior.
