# Enhancement 02: Shape Graphviz Output to Mongolian Tent Layout

## Goal

Adjust `visualize_labeling` so the rendered image clearly resembles the Mongolian Tent structure:
* Apex vertex `x` at the top.
* Top-row vertices `(1,i)` aligned horizontally beneath the apex, ordered left→right.
* Bottom-row vertices `(2,i)` aligned horizontally beneath the top row, ordered left→right.
* All edges labeled with their weights, preserving readability.

## High-Level Overview

The plan is to leverage Graphviz ranking and invisible edges:
1. Use `rankdir=TB` for a top-to-bottom flow.
2. Place nodes into two `subgraph` clusters (`rank="same"`) for top and bottom rows.
3. Insert invisible edges inside each rank to enforce ordering.
4. Keep the apex node outside clusters so it floats to the highest rank.
5. Handle edge creation carefully to avoid duplicates and to label apex edges cleanly.

## Detailed Steps

- [x] **Refactor Function** – Modify `src/visualization.py` to:
  - [x] Add `rankdir='TB'` to the main graph attributes.
  - [x] Create `top_row` and `bottom_row` subgraphs (rank='same', style='invis').
  - [x] Add top/bottom vertices to their respective clusters sorted by column index.
  - [x] Insert invisible edges between consecutive vertices in each cluster to lock ordering.
  - [x] Ensure apex vertex `x` is added separately and connects only to top-row vertices.

- [x] **Edge Generation** – Update edge loop to:
  - [x] Skip duplicates by maintaining a `set` of added pairs.
  - [x] Label each edge with weight; special-case apex connections if needed.

- [x] **Parameter Switch** – Add optional `shaped: bool = True` parameter to `visualize_labeling` to toggle the enhanced layout (default True).

- [ ] **Unit Test** – Write a test that:
  - [ ] Calls `visualize_labeling` with `shaped=True` for `n=3`.
  - [ ] Confirms output image is created without raising errors (skip if Graphviz unavailable).

- [ ] **Documentation Update** – Add usage snippet in `Add_Visualization.md` illustrating the shaped layout.

*Mark each checkbox after completing the corresponding implementation task.* 