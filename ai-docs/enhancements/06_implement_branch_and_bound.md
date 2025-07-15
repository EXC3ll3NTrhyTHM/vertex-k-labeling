# Task: Implement Branch & Bound Algorithm for es(MT(3,n))

This document outlines the tasks required to implement the Branch & Bound algorithm for finding the exact edge irregularity strength (`es`) for the Mongolian Tent Graph `MT(3,n)`, as detailed in `ai-docs/enhancements/branch_and_bound_algorithm.md`.

---

## 1. Core Implementation: Branch & Bound Solver

The primary logic for the Branch & Bound algorithm will reside in `src/labeling_solver.py`.

-   [x] **Create a new solver class or function:**
    -   Consider creating a new class, e.g., `BranchAndBoundSolver`, or a dedicated function within `labeling_solver.py` to encapsulate the Branch & Bound logic.
    -   This solver will take `n` as input and return `es(MT(3,n))` and the corresponding labeling.

-   [x] **Implement `find_es(n)` (Main Controller):**
    -   This function will iterate `k` from `3n-1` upwards.
    -   It will initialize `labels` and `used_edge_weights` for each `k`.
    -   It will call the recursive `solve_recursive` function.

-   [x] **Implement `solve_recursive(v_idx, k, vertex_order, labels, used_weights, adj)`:**
    -   This is the core recursive function.
    -   Handle the base case (all vertices labeled).
    -   Implement the branching logic (loop through possible labels).
    -   Integrate the pruning rules (validity check).
    -   Manage state (labels, used_weights) for backtracking.

-   [x] **Implement `is_assignment_valid(current_v, labels, used_edge_weights, adj)` (Pruning Rule):**
    -   This helper function will check for duplicate edge weights.
    -   It will identify newly formed edges and calculate their weights.
    -   It will return `true` if valid, `false` otherwise.

---

## 2. Graph Representation and Utilities

Ensure the `MT(3,n)` graph can be correctly generated and its properties accessed.

-   [x] **Extend `src/graph_generator.py`:**
    -   Add or modify a function, e.g., `create_mt3n_graph(n)`, to accurately represent `MT(3,n)`.
    -   This function should return the graph structure, including an adjacency list.
    -   Ensure correct definition of vertices (ladder and apex) and edges (horizontal, vertical, apex).

-   [x] **Implement `create_smart_vertex_order(n)`:**
    -   This function should generate the optimized vertex labeling order (apex, then top row, middle, bottom).
    -   Consider placing this in `src/graph_properties.py` or as a static method within the new solver class.

---

## 3. Integration and Testing

After implementing the core logic, integrate it into the main application flow and ensure robust testing.

-   [x] **Integrate into `main.py`:**
    -   Modify `main.py` to allow calling the new Branch & Bound solver.
    -   Provide options for users to select this solver.

-   [x] **Create new test cases in `tests/`:**
    -   Add a new test file, e.g., `tests/test_branch_and_bound_solver.py`.
    -   Write unit tests for `create_mt3n_graph` and `create_smart_vertex_order`.
    -   Write integration tests for the `BranchAndBoundSolver` to verify its correctness for small `n` values where `es(MT(3,n))` is known.
    -   Test edge cases and performance characteristics.

-   [x] **Performance Profiling (Optional but Recommended):**
    -   Once implemented, consider profiling the Branch & Bound solver to identify bottlenecks and further optimization opportunities.

---

## 4. Documentation Update

-   [x] **Update `README.md`:**
    -   Add a section describing the new Branch & Bound solver and how to use it.
    -   Mention its purpose (finding exact `es` for `MT(3,n)`).

---
