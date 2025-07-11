# Enhancement 01: Add Graphviz-Based Visualization

## Objective

Provide a clear, visual representation of Mongolian Tent graphs **with their computed vertex labels and edge weights**.  By integrating [Graphviz](https://graphviz.org/) we can:

* Quickly validate that all edge weights are unique.
* Spot patterns or anomalies in the labeling.
* Improve presentations and documentation with illustrative diagrams.

## High-Level Overview

- [ ] **Dependencies**
  - [x] System-level: Ensure Graphviz binaries are installed (e.g., `brew install graphviz`, `apt-get install graphviz`, or Windows installer).
  - [x] Python: Add `graphviz` package to the project (`pip install graphviz`).

- [x] **New Module – `src/visualization.py`**
  - [x] Implement `visualize_labeling(graph: dict, labeling: dict, output: str = "graph.png") -> None`.
  - [x] Node labels show vertex id and its assigned `k` label.
  - [x] Edge labels show the computed weight (sum of labels).
  - [x] Render and export as PNG or SVG via `graphviz.Digraph.render()`.

- [x] **Usage Example** *(update docs / code snippets)*
  - [x] Add example invocation in `main.py` or separate script demonstrating visualization.

- [x] **Optional CLI Helper**
  - [x] Provide a CLI entry-point (`python -m src.visualization --n 5 --file out.svg`).

- [x] **Tests / CI**
  - [x] Unit test: Call `visualize_labeling` with a tiny graph and assert the output file is created.
  - [x] Skip visualization test automatically if Graphviz binaries are not available (`unittest.skipUnless`).

---

*Once implemented, run `visualization.py` for quick visual checks or include images in documentation & reports.* 