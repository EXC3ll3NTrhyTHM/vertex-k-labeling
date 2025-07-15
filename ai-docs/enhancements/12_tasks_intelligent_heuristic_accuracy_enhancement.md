# Task: Complete Intelligent Heuristic Accuracy Enhancement

## Development Roadmap

### Phase 1: Advanced Vertex Ordering & Adaptive Label Selection
- [x] **Task 1.1: Refine Dynamic Scoring for Vertex Selection**
    - [x] Modify the vertex selection logic in `src/labeling_solver.py` to incorporate a dynamic scoring mechanism. This score should consider:
        - [x] Vertex degree.
        - [x] Number of already-labeled neighbors.
        - [x] Potential conflicts based on current partial labeling.
    - [x] Prioritize vertices with higher scores.
- [x] **Task 1.2: Implement Adaptive Conflict Thresholds for Label Selection**
    - [x] Update the label selection function in `src/labeling_solver.py` to include adaptive conflict thresholds.
    - [x] Allow for dynamic adjustment of acceptable conflict levels based on the stage of the labeling process (e.g., stricter early on, more lenient later).
- [ ] **Task 1.3: Integrate Refined Strategies into Greedy Pass**
    - [ ] Integrate the updated vertex ordering and adaptive label selection into the main greedy pass for the `intelligent` mode in `src/labeling_solver.py`.

### Phase 2: Multi-Strategy Local Search & Comprehensive Testing
- [ ] **Task 2.1: Develop Multi-Strategy Local Search Repair Mechanism**
    - [ ] Refactor the local search repair mechanism in `src/labeling_solver.py` to support multiple repair strategies (e.g., iterative minimum conflict re-labeling, tabu search, simulated annealing-like perturbations).
    - [ ] Implement a switching mechanism to trigger alternative strategies if the primary one gets stuck.
- [ ] **Task 2.2: Update and Add Comprehensive Tests**
    - [ ] Update existing unit and integration tests in `tests/test_heuristic_solver.py` to cover the enhanced `intelligent` mode.
    - [ ] Add new test cases to specifically validate the accuracy and performance improvements, including edge cases and benchmarks against previous versions and other heuristics.
