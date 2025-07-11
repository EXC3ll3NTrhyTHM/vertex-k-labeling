<context>
# Overview
This document outlines the plan to enhance the accuracy of the "intelligent" heuristic algorithm for k-labeling, specifically targeting improvements within `src/labeling_solver.py`. The current intelligent heuristic, while an improvement over purely random approaches, can still be optimized to find lower `k` values more consistently and efficiently, especially for larger and more complex graphs. This enhancement focuses on refining the core strategies of vertex ordering, label selection, and local search to achieve superior accuracy and performance.

# Core Features
1.  **Refined Vertex Ordering (Advanced Degree-Biased Randomization)**
    - **What:** Further refine the prioritization of vertices by incorporating not just degree, but also connectivity to already-labeled vertices and potential for creating conflicts.
    - **Why:** A more nuanced ordering can guide the search more effectively, reducing the likelihood of early dead-ends and leading to better `k` values.
    - **How:** Implement a dynamic scoring mechanism for unlabeled vertices that considers their degree, the number of their neighbors that are already labeled, and the number of potential conflicts they might introduce based on current partial labeling. Vertices with higher scores (indicating higher constraint or potential impact) will be prioritized.

2.  **Adaptive Conflict-Directed Label Selection (Dynamic Conflict Thresholds)**
    - **What:** Enhance the minimum conflict heuristic by dynamically adjusting the acceptable conflict threshold based on the current state of the labeling process.
    - **Why:** Early in the search, a stricter conflict avoidance might be beneficial, while later, a more lenient approach might help escape local minima.
    - **How:** Introduce a mechanism where the conflict score evaluation for label selection can adapt. For instance, in the initial phase, strictly choose zero-conflict labels if available. As the labeling progresses or if no zero-conflict labels are found, allow for a minimal number of conflicts, potentially using a weighted sum of conflicts.

3.  **Multi-Strategy Local Search Repair Mechanism**
    - **What:** Instead of a single local search strategy, implement a multi-pronged approach that can switch between different repair heuristics (e.g., tabu search, simulated annealing-like perturbations) if the primary local search gets stuck.
    - **Why:** A single local search might get trapped in local minima. Multiple strategies increase the chances of escaping these and finding a globally better solution.
    - **How:** If the initial local search (e.g., iterative minimum conflict re-labeling) fails to resolve all conflicts within a certain number of iterations, trigger an alternative repair strategy. This could involve temporarily allowing "bad" moves to escape local optima or introducing small, random perturbations to the labeling to explore new solution spaces.

# User Experience
- **CLI Interaction:** The existing `--algorithm intelligent` flag will continue to be used. The improvements will be transparent to the user, resulting in better outcomes without changes to the command-line interface.
- **Expected Outcome:** Users will observe that the `intelligent` mode consistently finds lower `k` values and/or completes the labeling process faster for a wider range of graph sizes and complexities compared to its previous iteration. The output format and visualization will remain unchanged.
</context>
<PRD>
# Technical Architecture
- **File to Modify:** `src/labeling_solver.py` will be the primary location for the changes.
- **New Logic:**
    - The existing vertex ordering function will be updated to incorporate the advanced dynamic scoring mechanism.
    - The label selection function will be modified to include adaptive conflict thresholds.
    - The local search repair mechanism will be refactored to support multiple repair strategies and a switching mechanism.
- **Testing:** Existing test cases in `tests/test_heuristic_solver.py` will be updated, and new test cases will be added to specifically validate the enhanced `intelligent` mode's accuracy and performance improvements. Benchmarking against previous versions and other heuristics will be crucial.

# Development Roadmap
1.  **Phase 1: Advanced Vertex Ordering & Adaptive Label Selection**
    - Refine the dynamic scoring for vertex selection in `src/labeling_solver.py`.
    - Implement adaptive conflict thresholds within the label selection logic.
    - Integrate these refined strategies into the main greedy pass for the `intelligent` mode.

2.  **Phase 2: Multi-Strategy Local Search & Comprehensive Testing**
    - Develop and integrate the multi-strategy local search repair mechanism.
    - Update and add comprehensive unit and integration tests to `tests/test_heuristic_solver.py` to cover the new logic, including edge cases, performance benchmarks, and comparisons against previous versions.

# Logical Dependency Chain
1.  Refinement of vertex ordering is foundational as it influences the initial greedy pass.
2.  Adaptive label selection builds upon the conflict-directed approach and is integrated into the greedy pass.
3.  The multi-strategy local search is a post-processing step that depends on the outcome of the greedy pass.
4.  Testing should be developed in parallel with the features but can only be finalized once all implementation is complete and integrated.

# Risks and Mitigations
- **Risk 1: Over-optimization leading to diminishing returns:** Excessive complexity in heuristics might not yield proportional improvements in `k` values or performance.
  - **Mitigation:** Implement changes incrementally and rigorously benchmark each iteration. Define clear performance and accuracy targets. If a new strategy doesn't meet targets, re-evaluate its inclusion.
- **Risk 2: Increased computational time for advanced heuristics:** The more sophisticated scoring and multi-strategy approaches could introduce significant overhead.
  - **Mitigation:** Profile all new components extensively. Prioritize strategies that offer the best accuracy-to-performance ratio. Explore approximations or pre-computation where feasible.
- **Risk 3: Difficulty in tuning multiple heuristic parameters:** The introduction of dynamic thresholds and multiple repair strategies might make the algorithm harder to tune for optimal performance across different graph types.
  - **Mitigation:** Design parameters to be robust and self-adjusting where possible. Provide clear documentation and default values. Consider automated parameter tuning if necessary for future enhancements.

# Appendix
- This PRD builds upon the initial "intelligent" heuristic design and aims to further enhance its accuracy and robustness.
