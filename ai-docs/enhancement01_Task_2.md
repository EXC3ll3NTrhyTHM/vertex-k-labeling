# Enhancement 01: Task 2 – Implement Iterative Greedy Search

## Goal

Augment the heuristic solver to perform an **iterative greedy search** that repeatedly invokes `greedy_labeling_solver`, starting from the theoretical lower bound for `k` and incrementing until a valid labeling is found or an upper safety limit is reached.

## High-Level Overview

The iterative greedy search is the core loop inside `find_heuristic_labeling`. It systematically tries increasing `k` values:
1. Begin with `k = lower_bound` (computed from graph properties).
2. Call `greedy_labeling_solver(graph, k)` to attempt a fast labeling.
3. If a labeling is returned, exit and report that `k`.
4. If no labeling is found, increment `k` by 1 and repeat.
5. Stop when `k` exceeds `max_k` (a multiple of the lower bound) to avoid infinite runtimes.

## Detailed Steps

- [x] Import or receive the already-generated `graph`, `lower_bound`, and `max_k_multiplier` inside `find_heuristic_labeling`.
- [x] Initialize `k` to `lower_bound` and calculate `max_k = lower_bound * max_k_multiplier`.
- [x] Enter a `while k <= max_k` loop.
- [x] Inside the loop, call `greedy_labeling_solver(graph, k)`.
- [x] If a non-`None` labeling is returned, print a success message and `return k, labeling`.
- [x] If no labeling is found, increment `k` by 1 and continue the loop.
- [x] Provide periodic progress feedback (e.g., every 10 increments of `k`).
- [x] After the loop, print a failure message and `return None, None` if the search exhausted all `k` values without success. 