# Task: Refactor Graph Data Structures for Performance

This document outlines the actionable steps required to refactor the project's core data structures. The primary goal is to significantly improve speed and reduce memory consumption for larger graphs by transitioning from dictionary-based structures to more efficient list-based ones [cite: ai-docs/enhancements/19_data_structure_refactoring.md#1-objective].

## Implement Integer Vertex Mapping

- [ ] In `src/graph_generator.py`, modify graph generation functions to create and return `node_to_int` and `int_to_node` mappings alongside the adjacency list [cite: ai-docs/enhancements/19_data_structure_refactoring.md#enhancement-1-implement-integer-vertex-mapping-foundational-change].
- [ ] Ensure the new integer-based adjacency list is created using the `node_to_int` mapping before being returned [cite: ai-docs/enhancements/19_data_structure_refactoring.md#enhancement-1-implement-integer-vertex-mapping-foundational-change].
- [ ] Update any scripts that call the generator functions to handle the new return signature (adjacency list, `node_to_int`, `int_to_node`) [cite: ai-docs/enhancements/19_data_structure_refactoring.md#enhancement-1-implement-integer-vertex-mapping-foundational-change].

## Convert Core Data Structures to Lists

- [ ] Refactor all solver algorithms (e.g., BranchAndBoundSolver, greedy, backtracking) to expect the graph's `adjacency_list` as a `list[list[int]]` [cite: ai-docs/enhancements/19_data_structure_refactoring.md#enhancement-2-convert-core-data-structures-to-lists].
- [ ] Update all solvers to expect `vertex_labels` as a `list[int]` instead of a dictionary [cite: ai-docs/enhancements/19_data_structure_refactoring.md#enhancement-2-convert-core-data-structures-to-lists].
- [ ] Replace all dictionary-based lookups (e.g., `vertex_labels[vertex_id]`) with direct list indexing (e.g., `vertex_labels[vertex_int_id]`) in all solvers and utility functions [cite: ai-docs/enhancements/19_data_structure_refactoring.md#enhancement-2-convert-core-data-structures-to-lists].

## Implement Hybrid Edge Weight Tracking

- [ ] In the solver classes, define a constant `FAST_WEIGHT_LIMIT` (e.g., `4 * num_vertices`) to set the boundary for the fast-access bitmask [cite: ai-docs/enhancements/19_data_structure_refactoring.md#enhancement-3-implement-hybrid-edge-weight-tracking].
- [ ] Initialize two data structures for tracking edge weights: a boolean list (`used_weights_fast`) for weights under the limit and a set (`used_weights_slow`) for weights exceeding it [cite: ai-docs/enhancements/19_data_structure_refactoring.md#enhancement-3-implement-hybrid-edge-weight-tracking].
- [ ] Implement helper methods in the solvers to abstract the logic for checking (`is_weight_used`) and adding (`add_weight`) weights using the hybrid approach [cite: ai-docs/enhancements/19_data_structure_refactoring.md#enhancement-3-implement-hybrid-edge-weight-tracking].
