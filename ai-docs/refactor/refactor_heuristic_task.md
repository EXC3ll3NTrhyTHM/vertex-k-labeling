# Goal: Refactor the Accurate Heuristic Algorithm

**Objective**: To replace the current purely random heuristic algorithm with a more intelligent, guided search strategy to improve accuracy (find lower *k* values), enhance performance for larger graphs, and ensure more consistent results.

---

## High-Level Overview

The project involves three main phases:
1.  **Implement a Smarter Greedy Pass**: We will replace the random vertex and label selection with more informed choices. This involves creating a new `intelligent` algorithm mode that uses degree-biased vertex ordering and a conflict-minimizing strategy for choosing labels.
2.  **Add a Local Search Repair Mechanism**: Instead of discarding nearly-valid solutions, we will implement a local search phase to iteratively repair the few remaining conflicts.
3.  **Testing and Validation**: We will add a comprehensive suite of tests to validate the new algorithm's correctness and benchmark its performance against the old `accurate` mode.

---

## Detailed Steps

### Phase 1: Core Logic Implementation

- [x] **1.1: Create New Algorithm Mode**: In `src/labeling_solver.py`, add a new `intelligent` option to the `find_feasible_k_labeling` function signature and its internal logic to handle the new code path.
- [x] **1.2: Implement Degree-Biased Vertex Ordering**: Create a helper function that takes the graph's vertices and returns a list of vertices ordered by degree quantiles. The selection from within each quantile should be random.
- [x] **1.3: Implement Minimum Conflict Label Selection**: Create a helper function that, for a given vertex, calculates a conflict score for each possible label (`1...k`) and returns the label with the lowest score.
- [x] **1.4: Integrate into a New Greedy Pass**: Assemble the new ordering and label selection logic into a single, cohesive greedy pass for the `intelligent` mode.

### Phase 2: Local Search and Repair

- [x] **2.1: Implement Conflict Identification**: After the initial greedy pass, create a function that identifies and returns a list of all vertices involved in edge weight conflicts.
- [x] **2.2: Implement the Local Search Loop**: If conflicts are found, implement a loop that runs for a fixed number of iterations. In each iteration, it should pick a conflicted vertex and attempt to repair it using the minimum conflict label selection logic from step 1.3.
- [x] **2.3: Integrate into `intelligent` mode**: The local search should be triggered only if the main greedy pass for the `intelligent` mode fails to find a perfect solution.

### Phase 3: Testing and Validation

- [x] **3.1: Create New Test File/Cases**: In `tests/test_heuristic_solver.py`, add new test cases specifically for the `intelligent` algorithm.
- [x] **3.2: Test Correctness**: Add tests to verify that the `intelligent` mode produces valid k-labelings for known small graphs.
- [x] **3.3: Test Components**: Add unit tests for the new helper functions: degree-biased ordering and minimum conflict selection.
- [x] **3.4: Benchmark Performance**: Add a test that runs on a larger benchmark graph and asserts that the `intelligent` mode finds a `k` value that is less than or equal to the one found by the `accurate` mode in a reasonable amount of time.

---

*This task file will be updated as steps are completed.*