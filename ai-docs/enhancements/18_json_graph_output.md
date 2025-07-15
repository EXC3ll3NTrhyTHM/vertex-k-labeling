# Enhancement: JSON Output for Graph Representation

## Problem Description

Currently, the application primarily outputs visual representations (PNGs) of the k-labeled graphs. While useful for quick inspection, these static images are not suitable for external data processing, advanced visualization tools, or integration with other systems. There is a need for a structured, machine-readable representation of the generated graphs, including their vertices, edges, and associated labels/weights.

## Proposed Solution

Implement an option to output the graph structure (vertices and edges) and their k-labeling results in JSON format. This JSON output will be available for both Mongolian Tent graphs and Circulant graphs, controlled by a new command-line argument.

### New Command-Line Argument

A new argument, `--output-json`, will be added to `main.py`. When this flag is present, the application will generate a JSON file containing the graph data instead of, or in addition to, the standard visualization.

Example usage:
```bash
python main.py --graph-type circulant --n 10 --solver heuristic --output-json
python main.py --graph-type mongolian_tent --n 5 --solver backtracking --output-json
```

### JSON Structure

The JSON output will contain two main arrays: `vertices` and `edges`.

**For unlabeled graphs (before solving):**
```json
{
  "graph_type": "mongolian_tent" | "circulant",
  "n": <int>,
  "r": <int> (only for circulant),
  "vertices": [
    {"id": <int>, "label": "v<id>"}
    // ... more vertices
  ],
  "edges": [
    {"source": <int>, "target": <int>}
    // ... more edges
  ]
}
```

**For k-labeled graphs (after solving):**
```json
{
  "graph_type": "mongolian_tent" | "circulant",
  "n": <int>,
  "r": <int> (only for circulant),
  "k_value": <int>,
  "lower_bound": <int>,
  "gap": <int> | "N/A",
  "time_taken_seconds": <float>,
  "solver_name": "<solver_name>",
  "vertices": [
    {"id": <int>, "label": "v<id>", "k_label": <int>}
    // ... more vertices with their k-labels
  ],
  "edges": [
    {"source": <int>, "target": <int>, "weight": <int>}
    // ... more edges with their calculated weights
  ]
}
```

### File Naming Convention

The JSON file will be saved in the `graphs/` directory with a descriptive name, e.g., `graphs/circulant_10_5_k_labeled.json` or `graphs/mt3_5_heuristic.json`, mirroring the existing PNG naming conventions.

## Implementation Details

1.  **Modify `main.py`:**
    *   Add `--output-json` as a boolean argument to `ArgumentParser`.
    *   After a `k` and `labeling` are found (and before visualization), check if `--output-json` is true.
    *   If true, construct the JSON data structure:
        *   Iterate through the graph's nodes to populate the `vertices` array, including their `k_label` if available.
        *   Iterate through the graph's edges to populate the `edges` array, calculating and including their `weight` (sum of k-labels of incident vertices) if a labeling exists.
        *   Include metadata like `graph_type`, `n`, `r` (if circulant), `k_value`, `lower_bound`, `gap`, `time_taken_seconds`, and `solver_name`.
    *   Use the `json` module to dump the dictionary to a file.

2.  **Helper Function (Optional but Recommended):**
    *   Consider creating a utility function (e.g., in `src/graph_properties.py` or a new `src/graph_serializer.py`) that takes a graph object and a labeling (if available) and returns the structured dictionary suitable for JSON serialization. This promotes code reusability and separation of concerns.

3.  **Edge Weight Calculation:**
    *   Ensure the edge weights are correctly calculated as the sum of the k-labels of their incident vertices, as per the k-labeling definition.

## Benefits

*   **Interoperability:** Enables easy integration with external visualization tools (e.g., D3.js, Gephi), data analysis platforms (e.g., Pandas, R), and other applications.
*   **Flexibility:** Users can process and analyze graph data programmatically without relying on image parsing.
*   **Debugging and Testing:** Provides a clear, structured representation of the graph state and labeling results, aiding in debugging and automated testing.
*   **API Readiness:** Lays the groundwork for potential future API endpoints that return graph data.
