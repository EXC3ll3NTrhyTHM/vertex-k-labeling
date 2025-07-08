# Task 1: Graph Construction

## Goal

Generate the graph structure for a Mongolian Tent graph \\( MT_{3,n} \\) for a given integer `n`. This involves creating a ladder graph \\( L_n \\) and then extending it by adding an apex vertex.

## High-Level Plan

1.  **Implement Ladder Graph \\( L_n \\) Generation**: Create a function or class that constructs a ladder graph.
2.  **Implement Mongolian Tent Graph \\( MT_{3,n} \\) Generation**: Extend the ladder graph to form the Mongolian Tent graph by adding an apex and connecting it to the top row vertices.

---

## Detailed Steps

### 1. Implement Ladder Graph \\( L_n \\)

-   [x] Define a representation for the graph (e.g., using an adjacency list with a dictionary).
-   [x] Create a function `generate_ladder_graph(n)` that takes an integer `n` as input.
-   [x] Inside the function, define the vertices. They can be represented as tuples: `(1, i)` for the top row and `(2, i)` for the bottom row, where `i` is from 1 to `n`.
-   [x] Add the horizontal edges for the top row: `((1, i), (1, i+1))` for `i` from 1 to `n-1`.
-   [x] Add the horizontal edges for the bottom row: `((2, i), (2, i+1))` for `i` from 1 to `n-1`.
-   [x] Add the vertical "rung" edges: `((1, i), (2, i))` for `i` from 1 to `n`.
-   [x] Return the constructed ladder graph.

### 2. Implement Mongolian Tent Graph \\( MT_{3,n} \\)

-   [x] Create a function `generate_mongolian_tent_graph(n)` that takes `n` as input.
-   [x] Inside this function, call `generate_ladder_graph(n)` to get the base graph.
-   [x] Define and add the apex vertex (e.g., `'x'`).
-   [x] Add edges connecting the apex vertex to all top-row vertices: `('x', (1, i))` for `i` from 1 to `n`.
-   [x] Return the final Mongolian Tent graph structure. 