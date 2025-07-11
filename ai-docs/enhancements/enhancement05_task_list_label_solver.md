# Enhancement 05 – Task List: Edge‐Irregular K‐Labeling Solver

> Track progress by ticking the checkboxes ([x]) as you complete each item.

---

## 1. New Module & API
- [x] Create new file `src/edge_irregular_solver.py`
- [x] Define public function `k_labeling_backtracking(graph: Dict[Any, List[Any]], k_limit: Optional[int] = None) -> Optional[Dict[Any, int]]`
- [x] Document API: inputs (adjacency list, optional k upper bound), outputs (label mapping or None)

## 2. Core Backtracking Algorithm
- [x] Implement `assign_label(node_idx: int, ordering: List[Any], labels: Dict[Any,int], used_weights: Set[int]) -> bool`:
  - Base case: all nodes labeled → return True
  - For each label `l` in 1..k_limit:
    - Check new edge weights vs `used_weights` for neighbors already labeled
    - On conflict, continue; else update `labels`, extend `used_weights`, recurse
    - On recurse success → return True, else undo (backtrack)
- [x] Determine search ordering:
  - Default: descending vertex degree
  - Special: place apex node first (if present)

## 3. K‐Limit Management
- [x] Compute initial lower bound: `max_degree = max(len(neighbors) for neighbors in graph.values())`
- [x] If `k_limit` is `None`:
  - Start at `lower_bound`, increment until backtracking succeeds
- [ ] (Optional) Implement binary search on k between lower_bound and `n`

## 4. Validation & Utilities
- [x] Reuse or import `is_labeling_valid` for full‐graph checks (optional sanity guard)
- [x] Write helper to compute `used_weights` set incrementally

## 5. Command‐Line Integration
- [x] In `main.py`, register new solver option, e.g. `--solver backtracking` or `--solver edge-irregular`
- [x] Hook `k_labeling_backtracking` into CLI dispatch
- [x] Add flags for `--k-limit` and printing progress

## 6. Unit Testing
- [ ] Create `tests/test_edge_irregular_solver.py`
- [ ] Test on small graphs (n=3,4): verify full labeling returned and `k = max(label)` is minimal
- [ ] Edge‐case tests: empty graph, single node, disconnected parts
- [ ] Performance test: ensure n=10 solves within reasonable time (<1s) with default settings

## 7. Documentation
- [ ] Update `ai-docs/algorithms/mongolian_tent_klabeling.md` to reference new module & function signatures
- [ ] Add usage example in `README.md` under “Rendering” or “Solvers” section
- [ ] Provide code snippet demonstrating backtracking API

## 8. Completion Criteria
- [ ] All checklist items ticked
- [ ] CI passes with new solver enabled & existing tests unaffected
- [ ] Verified minimal `k` found for sample graphs matches known results 