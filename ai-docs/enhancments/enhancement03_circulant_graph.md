# Enhancement 03: Circulant Graph Generation (C_{n,r})

## Context
Circulant graphs are a family of r-regular graphs on n vertices where each vertex i is connected to vertices (i ± j) mod n for a set of generators j=1…⌊r/2⌋ (and the opposite vertex when r is odd). Supporting circulant graphs expands our library beyond complete and shape-based graphs, enabling tailored experiments on structured graph families (Problem-2 of the project).

## Goals
- Implement a generator for circulant graphs in `src/graph_generator.py`.
- Integrate a new `circulant` graph type in the CLI (`main.py`) with a customizable degree parameter `r` (default r = n - 5).
- Extend `src/graph_properties.py` to verify circulant-specific invariants (regularity, diameter).
- Add visualization support for circulant layouts in `src/visualization.py` (radial placement).
- Write comprehensive unit tests for generation, properties, and visualization.
- Update documentation (`README.md`) with usage examples for circulant graphs.

## Detailed Steps
- [ ] **Generator Function** – Add `generate_circulant_graph(n: int, r: int) -> Graph` to `src/graph_generator.py`:
  - Validate inputs: 5 ≤ n ≤ 50, 1 ≤ r < n.
  - Compute edge set: for j in 1…⌊r/2⌋, connect each i to (i±j)%n; if r odd and n even, include opposite vertex once.
- [ ] **Constants Update** – In `src/constants.py`, define `DEFAULT_CIRCULANT_OFFSET = 5` and register `GRAPH_TYPES['circulant']` with default r = n - DEFAULT_CIRCULANT_OFFSET.
- [ ] **CLI Integration** – Modify `main.py`:
  - Add `--graph-type {complete,shape,circulant}` argument.
  - Accept `--r` when `circulant` is selected, falling back to `n - DEFAULT_CIRCULANT_OFFSET`.
- [ ] **Graph Properties** – In `src/graph_properties.py`, add:
  - `is_regular(graph, r)` validation for circulants.
  - `compute_diameter(graph)` check against known circulant diameters.
- [ ] **Visualization** – In `src/visualization.py`:
  - Implement `radial_layout_circulant(graph)` placing nodes evenly on a circle.
  - Extend `visualize_graph` to handle `graph_type='circulant'` and optionally label generators.
- [ ] **Testing** – Create tests in `tests/`:
  - `test_graph_generator_circulant.py`: small n examples (e.g., C_{9,2}, C_{12,3}), edge counts, error on invalid params.
  - `test_graph_properties_circulant.py`: verify regularity and diameter.
  - `test_visualization_circulant.py`: generate image without errors (skip if missing Graphviz).
- [ ] **Documentation** – Update `README.md`:
  - Add `circulant` to supported graph types.
  - Include code snippet demonstrating generation and visualization of a circulant graph.

## Deliverables
1. `src/graph_generator.py`: new generator function.
2. `src/constants.py`: default constants and graph type registration.
3. `main.py`: CLI flags and logic.
4. `src/graph_properties.py`: circulant-specific checks.
5. `src/visualization.py`: radial layout for circulants.
6. New unit tests in `tests/`.
7. Updated `README.md` with usage examples.
8. This enhancement document.

## Timeline (Suggested)
| Week | Task |
|------|------|
| 1    | Implement generator, constants, and CLI support |
| 2    | Extend graph properties and write corresponding tests |
| 3    | Add visualization code and tests |
| 4    | Update documentation, finalize integration, and review |

*Prepared by: AI assistant – 2025-07-09* 