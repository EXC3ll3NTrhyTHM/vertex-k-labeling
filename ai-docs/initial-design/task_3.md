# Task 3: Labeling Algorithm Implementation

## Goal

Implement a backtracking algorithm to find a valid vertex k-labeling for a given Mongolian Tent Graph \\( MT_{3,n} \\). The objective is to find the minimum integer `k` for which a labeling `φ: V -> {1, 2, ..., k}` exists, such that all edge weights are unique.

## High-Level Plan

1.  **Implement Backtracking Solver**: Create the core recursive function that attempts to find a valid labeling for a given `k`.
2.  **Implement Main Search Function**: Create a wrapper function that starts with the theoretical lower bound for `k` and iteratively calls the solver, incrementing `k` until the first valid labeling is found. This first solution will be the minimum `k`.

---

## Detailed Steps

### 1. Implement Backtracking Solver

-   [x] Create a new file `src/labeling_solver.py`.
-   [x] Define a recursive function `backtracking_solver(graph, k, labeling, vertices_to_label)`.
-   [x] **Base Case**: If `vertices_to_label` is empty, a valid solution has been found. Return the completed `labeling`.
-   [x] **Recursive Step**:
    -   [x] Select the next vertex to label from `vertices_to_label`.
    -   [x] Iterate through possible labels from `1` to `k`.
    -   [x] For each label, create a temporary assignment.
    -   [x] Check if this assignment creates any duplicate edge weights with already labeled vertices.
    -   [x] If it's a valid partial assignment, recursively call `backtracking_solver` with the updated labeling and remaining vertices.
    -   [x] If the recursive call returns a valid solution, propagate it up.
-   [x] If the loop finishes without finding a valid label, it means a dead end has been reached. Return `None` to backtrack.

### 2. Implement Main Search Function

-   [x] In `src/labeling_solver.py`, create a main function `find_minimum_k_labeling(n)`.
-   [x] Inside this function, generate the \\( MT_{3,n} \\) graph.
-   [x] Calculate the theoretical lower bound for `k` using the function from Task 2.
-   [x] Start a loop, with `k` initialized to the lower bound.
-   [x] Inside the loop:
    -   [x] Call the `backtracking_solver` with the graph and the current `k`.
    -   [x] If the solver returns a valid labeling, this `k` is the minimum. Return the `k` and the labeling.
    -   [x] If the solver returns `None`, increment `k` and continue the loop. 