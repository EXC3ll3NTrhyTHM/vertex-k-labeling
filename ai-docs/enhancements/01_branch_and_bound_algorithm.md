# Algorithm Guide: Finding es(MT(3,n)) with Branch & Bound

This document provides a step-by-step guide to implement an efficient Branch & Bound algorithm to find the exact **edge irregularity strength (`es`)** for the **Mongolian Tent Graph `MT(3,n)`**.

---

## 1. Context & Goal

-   **Problem:** Find the smallest integer `k` such that we can label the vertices of `MT(3,n)` with numbers from `{1, 2, ..., k}` and have all edge weights be unique. An edge's weight is the sum of the labels of its two endpoints.
-   **Graph:** `MT(3,n)` consists of a `3 x n` ladder graph where an additional apex vertex `z` is connected to all `n` vertices in the top row.
-   **Lower Bound:** The theoretical minimum `k` we are trying to achieve is `es(MT(3,n)) >= 3n - 1`. Our algorithm will start its search from this value.
-   **Algorithm:** We will use a **Branch & Bound** search. This is an optimized backtracking algorithm that intelligently prunes branches of the search tree that cannot lead to a valid solution, making it much more efficient.

---

## 2. Step-by-Step Implementation Plan

### ☐ Step 1: Graph Representation

First, you need a way to represent the `MT(3,n)` graph in your code. An adjacency list is efficient for this purpose.

-   [ ] **Define Vertices:**
    -   Create `3n + 1` vertices. A good mapping is:
        -   Vertices `0` to `3n-1`: The ladder vertices `v_i,j`. A possible mapping is `vertex_index = (i-1)*n + (j-1)` for `i` in `{1,2,3}` and `j` in `{1,...,n}`.
        -   Vertex `3n`: The apex vertex `z`.
-   [ ] **Define Edges:**
    -   Based on the vertex mapping, create the list of edges `E`. An edge can be represented as a pair of vertex indices, e.g., `(u, v)`.
    -   **Horizontal Edges:** `3 * (n-1)` edges.
    -   **Vertical Edges:** `2 * n` edges.
    -   **Apex Edges:** `n` edges connecting vertex `3n` (`z`) to the top row vertices (`v_3,j`).
-   [ ] **Create Adjacency List:**
    -   Construct an adjacency list `adj` where `adj[u]` contains a list of all vertices `v` adjacent to `u`. This will be used to quickly find neighbors when calculating edge weights.

### ☐ Step 2: The Main Controller

The main part of your program will test potential values of `k` in an increasing order, starting from the known lower bound. The first `k` for which a valid labeling is found is the optimal `es(MT(3,n))`.

-   [ ] **Calculate Lower Bound:**
    -   Set `k_min = 3n - 1`.
-   [ ] **Iterative Search for `k`:**
    -   Start a loop: `for k from k_min upwards...`
    -   Inside the loop, you will attempt to find a valid labeling where the maximum label used is `k`.
    -   Create the necessary data structures for the search:
        -   `labels`: An array of size `3n + 1` to store the label of each vertex, initialized to 0.
        -   `used_edge_weights`: A hash set to store the weights of edges that have already been formed. This allows for O(1) checking of duplicate weights.
    -   Call the recursive Branch & Bound solver function (defined in Step 4).
    -   `solution_found = solve(initial_state)`
    -   If `solution_found` is `true`:
        -   The current `k` is the `es(MT(3,n))`.
        -   Print `k` as the result and terminate the program.

### ☐ Step 3: Vertex Ordering for Efficiency

The order in which you assign labels to vertices dramatically impacts performance. A good heuristic is to label high-degree vertices first, as this constrains the search space more quickly.

-   [ ] **Define a Static Vertex Order:**
    -   Create a predefined list or array `vertex_order` that specifies the sequence for labeling.
    -   **Recommended Order:**
        1.  **Apex Vertex (`z`):** This vertex is part of `n` edges. Label it first.
        2.  **Top Row Vertices (`v_3,j`):** These have the next highest degrees.
        3.  **Middle Row Vertices (`v_2,j`):**
        4.  **Bottom Row Vertices (`v_1,j`):**
    -   The recursive solver will follow this `vertex_order` list instead of a naive `0, 1, 2, ...` sequence.

### ☐ Step 4: The Recursive Branch & Bound Solver

This is the core of the algorithm. It will try to assign labels to vertices one by one, checking for violations and backtracking when necessary.

-   [ ] **Define the Recursive Function Signature:**
    -   `solve(vertex_order_idx, labels, used_edge_weights)`
    -   `vertex_order_idx`: The index in your `vertex_order` list, indicating which vertex to label now.
    -   `labels`: The current state of vertex labels.
    -   `used_edge_weights`: The set of edge weights seen so far in this path.
-   [ ] **Base Case (Success):**
    -   If `vertex_order_idx` is equal to the total number of vertices (`3n + 1`), it means all vertices have been successfully labeled without conflicts.
    -   Return `true`.
-   [ ] **Recursive Step (Branching):**
    -   Get the current vertex to be labeled: `current_v = vertex_order[vertex_order_idx]`.
    -   Loop through all possible labels for this vertex: `for label from 1 to k...`
        -   Assign the label: `labels[current_v] = label`.
        -   **Pruning Rule Check (Step 5):** Check if this assignment is valid.
        -   If it is valid:
            -   Recursively call the solver for the next vertex: `if solve(vertex_order_idx + 1, labels, new_used_edge_weights)`.
            -   If the recursive call returns `true`, it means a solution was found down this path. Immediately return `true` up the call stack.
-   [ ] **Backtracking:**
    -   If the `for` loop finishes without finding a valid label that leads to a solution, it means this path is a dead end.
    -   Before returning, you must "un-set" any state changes made within this function call so that previous calls can explore other options. (Note: Passing copies or managing state carefully can handle this automatically).
    -   Return `false`.

### ☐ Step 5: Pruning Rules (The "Bound")

This is the most critical step for making the algorithm efficient. Pruning happens *before* a recursive call. After assigning a label to `current_v`, you must check its validity.

-   [ ] **Implement the Validity Check:**
    -   This check should be a separate function: `is_assignment_valid(current_v, labels, used_edge_weights)`
    -   **Identify Newly Formed Edges:** Find all neighbors of `current_v` that have already been assigned a label (i.e., they appeared earlier in the `vertex_order` list).
    -   **Calculate New Edge Weights:** For each such neighbor `neighbor_v`, calculate the weight: `w = labels[current_v] + labels[neighbor_v]`.
    -   **Feasibility Pruning:**
        -   The minimum possible edge weight is `1+1=2` and the maximum is `k+k=2k`.
        -   Check if the calculated weight `w` is already in the `used_edge_weights` set.
        -   If `w` is a duplicate, this assignment is invalid. The branch is pruned. Return `false` from the validity check.
    -   If all new edge weights are unique, the assignment is valid.
    -   **Update State:** Add all the newly calculated weights to a temporary set. If the validity check passes, this temporary set is merged with `used_edge_weights` before the next recursive call.

---

## 3. Pseudocode Summary

```
function find_es(n):
    graph = create_mt3n_graph(n)
    vertex_order = create_smart_vertex_order(n) // z, then v3,j, etc.
    k = 3 * n - 1

    while True:
        labels = array of size (3n+1) initialized to 0
        used_edge_weights = new HashSet()

        if solve_recursive(0, k, vertex_order, labels, used_edge_weights, graph.adj):
            return k // Solution found!

        k = k + 1 // Try the next possible value for k

function solve_recursive(v_idx, k, vertex_order, labels, used_weights, adj):
    // Base Case: All vertices are labeled
    if v_idx == len(labels):
        return true

    current_v = vertex_order[v_idx]

    // Branching: Try all possible labels for the current vertex
    for label from 1 to k:
        labels[current_v] = label
        
        // Pruning: Check for immediate conflicts
        newly_formed_weights = new HashSet()
        is_valid = true
        for neighbor in adj[current_v]:
            if labels[neighbor] != 0: // If neighbor is already labeled
                weight = labels[current_v] + labels[neighbor]
                if used_weights.contains(weight) or newly_formed_weights.contains(weight):
                    is_valid = false
                    break
                newly_formed_weights.add(weight)
        
        if is_valid:
            // Recurse to the next vertex
            if solve_recursive(v_idx + 1, k, vertex_order, labels, used_weights.union(newly_formed_weights), adj):
                return true

    // Backtrack: No valid label found for current_v in this path
    labels[current_v] = 0 // Reset label
    return false

```