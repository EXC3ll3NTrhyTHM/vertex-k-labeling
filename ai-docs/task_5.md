# Task 5: Testing & Verification

## Goal

Ensure the correctness, robustness, and performance of the vertex k-labeling implementation for Mongolian Tent graphs. All algorithms must:

- Produce **unique edge weights** for every tested graph instance.
- Return the **minimum possible k** (edge irregularity strength).
- Pass performance thresholds on reasonable graph sizes (baseline: MT_{3,5}).

---

## High-Level Overview

1. **Unit Tests** – Cover individual components (graph generators, lower-bound calculator, validation helpers).
2. **Integration Tests** – Validate end-to-end k-labeling search (backtracking + heuristics) on multiple n values.
3. **Greedy Heuristic Tests** – Confirm the heuristic either finds a valid labeling or cleanly indicates failure without corrupting state.
4. **Performance Benchmarks** – Measure runtime for representative graphs; flag regressions.
5. **Edge & Error Handling Tests** – Verify graceful handling of invalid input (e.g., n ≤ 0).

---

## Detailed Steps

### 1. Unit Tests

- [x] **Graph Construction** – Assert correct vertex/edge counts for `generate_ladder_graph` and `generate_mongolian_tent_graph` across n = 1…5.
- [x] **Lower Bound Calculator** – Validate `calculate_lower_bound` against manual calculations for sample graphs.
- [x] **Validity Checker** – Ensure `_is_valid_assignment` correctly flags duplicate and unique edge-weight scenarios.

### 2. Integration Tests

- [x] **Backtracking Solver** – Confirm `find_minimum_k_labeling` returns the theoretical lower bound for n = 1, 2, 3.
- [x] **Upper-Bound Respect** – Verify solver never exceeds initial greedy upper bound when provided.

### 3. Greedy Heuristic Tests

- [x] **Successful Cases** – Expect non-`None` labeling for small graphs where heuristic is effective (e.g., n = 1).
- [x] **Graceful Failures** – Ensure function returns `None` without side-effects for cases like n = 2 where greedy may fail.

### 4. Performance Benchmarks

- [x] **Baseline Timing** – Record runtime of full solver on MT_{3,3} and MT_{3,5} (target: <10 s on dev machine).
- [x] **Regression Guard** – Add benchmark test with threshold; fail if runtime exceeds 2× baseline.

### 5. Edge & Error Handling

- [x] **Invalid Input** – Confirm functions raise `ValueError` or return empty graph for n ≤ 0.
- [x] **Large n Smoke Test** – Run solver (with relaxed timeout) on MT_{3,8} to ensure no crashes.

---

*Mark each checkbox when the corresponding task is completed to track progress.* 