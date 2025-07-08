# Enhancement 01: Task 3 – Safety Limit for Iterative Greedy Search

## Goal

Ensure the iterative greedy search in `find_heuristic_labeling` **cannot run indefinitely** by enforcing a configurable safety limit on `k`. The search must stop once `k` exceeds a multiple of the theoretical lower bound, preventing excessive runtimes on very large graphs.

## High-Level Overview

The heuristic already accepts a `max_k_multiplier` parameter, but we want to formalize, document, and test this behavior so that:
1. The default multiplier (currently 5) is applied if the caller doesn't provide one.
2. Callers can pass a custom multiplier to tighten or loosen the search cap.
3. The function emits a clear message and returns `(None, None)` when the limit is reached without success.
4. Unit tests verify that the safety limit triggers as expected.

## Detailed Steps

- [x] **Parameter Check** – Guarantee `max_k_multiplier` is ≥ 1; raise `ValueError` if not.
- [x] **Default Handling** – Confirm the default multiplier of 5 is used when none is supplied.
- [x] **Limit Calculation** – Compute `max_k = lower_bound * max_k_multiplier` inside the solver.
- [x] **Loop Guard** – Ensure the `while` loop condition is `k <= max_k`.
- [x] **Failure Path** – After the loop, print a descriptive message and return `(None, None)`.
- [x] **Logging** – Provide periodic progress updates including current `k` and limit.
- [x] **Unit Test – Trigger** – Add a test that runs the heuristic with a deliberately tiny multiplier (e.g., 1) on a graph that cannot be solved at `k = lower_bound`, asserting it returns `(None, None)` quickly.
- [x] **Unit Test – Success Under Higher Limit** – Verify that with a higher multiplier (e.g., 10) the solver can find a labeling for the same graph. 