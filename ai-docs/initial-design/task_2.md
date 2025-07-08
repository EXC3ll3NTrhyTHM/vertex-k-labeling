# Task 2: Calculate Theoretical Lower Bound

## Goal

Compute the theoretical lower bound for `k` for a given Mongolian Tent Graph \\( MT_{3,n} \\). This value provides the minimum possible value for the edge irregularity strength, which helps to narrow the search space for the labeling algorithm.

## High-Level Plan

1.  **Calculate Graph Properties**: Determine the number of edges `|E(G)|` and the maximum degree `Δ(G)` of the input graph.
2.  **Compute Lower Bound**: Use the calculated properties to compute the theoretical lower bound for `k` using the formula \\( k \ge \max\left\{ \lceil \frac{|E(G)| + 1}{2} \rceil, \Delta(G) \right\} \\).

---

## Detailed Steps

### 1. Calculate Graph Properties

-   [x] Create a function `get_graph_properties(graph)` that takes a graph (adjacency list) as input.
-   [x] **Calculate Edge Count |E(G)|**: Inside the function, sum the lengths of all adjacency lists and divide by 2 to get the total number of edges.
-   [x] **Calculate Maximum Degree Δ(G)|**: Find the maximum length of any adjacency list in the graph.
-   [x] Return both the edge count and the maximum degree.

### 2. Implement Lower Bound Calculation

-   [x] Create a function `calculate_lower_bound(n)` that takes `n` as input.
-   [x] Inside this function, generate the \\( MT_{3,n} \\) graph using the function from Task 1.
-   [x] Call `get_graph_properties()` to get `|E(G)|` and `Δ(G)`.
-   [x] Calculate the value from the formula: `ceil((|E(G)| + 1) / 2)`.
-   [x] The lower bound for `k` is the maximum of this value and `Δ(G)`.
-   [x] Return the final lower bound value. 