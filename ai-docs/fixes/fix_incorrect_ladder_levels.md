# Enhancement 03: Fix Incorrect Ladder Levels (3 Rows Required)

## Goal

Refactor code, tests, and documentation to support **three-row ladders** in Mongolian Tent graphs (rows 1, 2, & 3) instead of the previously-assumed two rows.

## High-Level Overview

1. **Graph Generator Update** – `generate_ladder_graph` & `generate_mongolian_tent_graph` must create 
   three horizontal rows plus two sets of vertical rungs.
2. **Property Calculations** – Edge-count and degree logic in `graph_properties.py` must reflect the new structure.
3. **Solver Impact** – Labeling algorithms remain row-agnostic, but tests relying on hard-coded counts/labels need updates.
4. **Documentation** – All docs/examples must reference three rows.
5. **Visualization** – `visualization.py` already supports arbitrary rows; ensure top/middle/bottom ranks.

## Detailed Steps

- [x] **Generator Refactor**
  - [x] Modify `generate_ladder_graph(n)` to create vertices `(1,i)`, `(2,i)`, `(3,i)`.
  - [x] Add horizontal edges for rows 1-3.
  - [x] Add vertical rungs `(1,i)-(2,i)` and `(2,i)-(3,i)`.
  - [x] Update `generate_mongolian_tent_graph` to attach apex to row-1 only.

- [x] **Property Functions**
  - [x] Re-compute edge count formula (now `|E| = 6n − 3`).
  - [x] Ensure `get_graph_properties` returns correct max-degree (should become Δ = 4).

- [x] **Unit Tests**
  - [x] Update `tests/test_graph_generator.py` expected counts.
  - [x] Adjust lower-bound calculations in `tests/test_graph_properties.py`.
  - [x] Revise any hard-coded label examples.

- [ ] **Solver & Heuristics**
  - [ ] Verify algorithms work unchanged; update doctstrings where they mention rows.

- [ ] **Documentation**
  - [ ] Ensure `master_plan.md`, worked example, and other docs reflect 3 rows.
  - [ ] Remove outdated two-row sample labeling.

- [ ] **Visualization**
  - [ ] Test shaped layout for n = 3 now showing three horizontal ranks.

*Tick each box upon completion to track progress for this bug fix.* 