# Task: Integrate Theoretical Lower Bound into Circulant Graph Solver

## 1. Introduction

This document outlines the task of integrating the newly defined `calculate_circulant_lower_bound(n, r)` function into the `find_optimal_k_labeling_circulant` solver. This integration will replace the current basic lower bound estimation with a more accurate theoretical lower bound, potentially improving the efficiency of the solver by starting the search for `k` from a more informed value.

## 2. Current State

In `src/labeling_solver.py`, the `find_optimal_k_labeling_circulant` function currently calculates a basic lower bound for `k` using `max_degree + 1`:

```python
    max_degree = max((len(adj) for adj in adjacency_list.values()), default=0)
    k = max_degree + 1 if max_degree > 0 else 1 # A very basic lower bound
```

## 3. Proposed Change

Replace the existing basic lower bound calculation within `find_optimal_k_labeling_circulant` with a call to the `calculate_circulant_lower_bound(n, r)` function.

## 4. Implementation Steps

1.  **Implement `calculate_circulant_lower_bound(n, r)`**: Ensure the function described in `ai-docs/enhancements/14_calculate_theoretical_lower_bound_for_circulant_graphs.md` is implemented in `src/graph_properties.py` (or a suitable location if decided otherwise).

2.  **Import the function**: In `src/labeling_solver.py`, import `calculate_circulant_lower_bound`.

3.  **Modify `find_optimal_k_labeling_circulant`**: Locate the `find_optimal_k_labeling_circulant` function in `src/labeling_solver.py` and change the line that calculates `k` to use the new function:

    ```python
    # Old line to be replaced:
    # max_degree = max((len(adj) for adj in adjacency_list.values()), default=0)
    # k = max_degree + 1 if max_degree > 0 else 1 # A very basic lower bound

    # New line:
    k = calculate_circulant_lower_bound(n, r) # Use the theoretical lower bound
    ```

4.  **Update `main.py` (if necessary)**: Ensure that `main.py` passes the `r` parameter to `find_optimal_k_labeling_circulant` if it's not already doing so, as `calculate_circulant_lower_bound` requires both `n` and `r`.

## 5. Verification

1.  **Run `test_circulant_labeling.py`**: Execute the `test_circulant_labeling.py` script to ensure that the circulant graph labeling still functions correctly and produces valid results. Observe if the initial `k` value printed by the solver changes to reflect the theoretical lower bound.

2.  **Manual Inspection**: For specific `n` and `r` values (e.g., `n=12, r=7` as per the example in the formula document), manually verify that the `k` value reported by the solver matches the theoretical lower bound calculated by the formula.

3.  **Performance Observation**: While not a strict verification, observe if there's any noticeable change in the solver's performance (e.g., faster convergence to the optimal `k`) due to starting from a more accurate lower bound.