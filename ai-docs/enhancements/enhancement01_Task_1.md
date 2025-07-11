# Enhancement 01: Task 1 - Implement Heuristic Solver Function

## Goal

To implement the `find_heuristic_labeling` function in `src/labeling_solver.py`, enabling the finding of feasible (though not necessarily minimal) k-labelings for large Mongolian Tent graphs (e.g., n=30 or n=50) within practical timeframes.

## High-Level Overview

This task involved creating a new function that leverages the faster, existing `greedy_labeling_solver`. The `find_heuristic_labeling` function iteratively attempts to find a valid labeling by incrementally increasing the allowed `k` value until a solution is found or a predefined upper limit for `k` is reached. This approach prioritizes speed and feasibility over guaranteed optimality.

## Detailed Steps

- [x] Define the `find_heuristic_labeling` function signature in `src/labeling_solver.py` with parameters for `n` and an optional `max_k_multiplier` (to set an upper bound for `k`).
- [x] Implement initial error handling for `n <= 0`, returning `None, None`.
- [x] Inside the function, generate the Mongolian Tent graph for the given `n` and calculate its theoretical lower bound for `k` (`lower_bound`).
- [x] Initialize the current `k` to the `lower_bound` and set `max_k` (e.g., `lower_bound * max_k_multiplier`).
- [x] Implement a `while` loop that continues as long as the current `k` is less than or equal to `max_k`.
- [x] Within the loop, call the `greedy_labeling_solver` with the generated `graph` and the current `k`.
- [x] Add logic to check the result from `greedy_labeling_solver`:
    - If a `labeling` is found (not `None`), return the current `k` and the `labeling`.
    - If no `labeling` is found, increment `k` by 1 and continue the loop.
- [x] Include print statements for progress feedback, showing the current `n` and `k` values during the iterative search.
- [x] If the loop completes without finding a solution (i.e., `k` exceeds `max_k`), return `None, None` to indicate failure.
 