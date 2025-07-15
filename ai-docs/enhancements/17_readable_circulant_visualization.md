# Enhancement: Improved Readability for Circulant Graph Visualizations

## Problem Description

Current PNG visualizations of circulant graphs often suffer from significant readability issues, particularly when the number of vertices (`n`) or the offset (`r`) increases. The primary problems are:
1.  **Overlapping Edges:** Edges frequently overlap, making it difficult to distinguish individual connections and their associated weights.
2.  **Unreadable Labels:** Due to overlapping edges and potentially small font sizes, the labels (vertex labels, edge weights) become illegible, making it impossible to determine the weight associated with each edge.

This hinders the analysis and understanding of the k-labeling results for circulant graphs.

## Proposed Solutions

### Solution for PNG Files (Static Image Improvement)

To improve the readability of static PNG visualizations, the following approaches can be considered:

1.  **Optimized Graph Layout Algorithms:**
    *   **Graphviz Layouts:** Experiment with different Graphviz layout engines beyond the default (often `dot`). `neato` or `fdp` might produce more spread-out layouts, or even `circo` for a circular arrangement that might inherently reduce some overlaps for circulant graphs.
    *   **Custom Circular Layout:** Implement a custom layout algorithm that places vertices in a perfect circle and then draws edges. For circulant graphs, this is a natural representation. The challenge then becomes how to draw edges (especially chords) without excessive overlap.
        *   **Arc-based Edges:** Instead of straight lines, draw edges as arcs. This can help differentiate edges, especially those that would otherwise overlap heavily. The curvature can be adjusted based on the "distance" between connected vertices.
        *   **Edge Bundling (Advanced):** For very dense graphs, consider algorithms that bundle edges together, reducing visual clutter while still conveying connectivity. This is more complex to implement.

2.  **Adjusting Visualization Parameters:**
    *   **Increased Spacing:** Increase the spacing between nodes and the overall canvas size to give more room for edges and labels.
    *   **Label Placement:** Implement smarter label placement algorithms to ensure labels do not overlap with edges or other labels. Graphviz has some capabilities here, but fine-tuning might be needed.
    *   **Font Sizes:** Dynamically adjust font sizes for labels based on the graph size to maintain readability.
    *   **Edge Thickness/Coloring:** Use varying edge thicknesses or color gradients to highlight certain properties (e.g., higher weights thicker/brighter) or to group edges, which can indirectly help readability.

3.  **Selective Information Display:**
    *   For very large graphs, it might be impractical to display all edge weights. Consider options like:
        *   Displaying only a subset of edge weights (e.g., only the k-labeling values, or only for a few representative edges).
        *   Providing a legend or a separate table for edge weights.

### Solution Not Involving PNGs (Interactive and Data-Driven Approaches)

For a more robust and interactive solution that overcomes the limitations of static images:

1.  **Interactive Web-Based Visualization (HTML/SVG/Canvas):**
    *   **Libraries:** Utilize JavaScript libraries like D3.js, Plotly.js, or vis.js to render the graph in a web browser.
    *   **Features:**
        *   **Zoom and Pan:** Allow users to zoom in and pan around the graph to inspect details.
        *   **Hover Information:** Display edge weights and vertex labels on hover. This is the most effective way to show detailed information without cluttering the initial view.
        *   **Click/Select:** Enable selection of nodes/edges to highlight paths or display properties.
        *   **Dynamic Layouts:** Some libraries offer force-directed layouts that can be adjusted in real-time, or allow for custom layouts (like a circular layout for circulant graphs).
    *   **Implementation:** The Python backend would generate the graph data (e.g., as JSON) and a simple HTML/JavaScript frontend would consume this data and render the interactive visualization.

2.  **Structured Data Output:**
    *   Provide the k-labeling results in a structured, machine-readable format (e.g., JSON, CSV). This allows users to process and visualize the data using their preferred tools (e.g., spreadsheet software, data analysis environments, or other graph visualization tools).
    *   Example JSON structure:
        ```json
        {
          "vertices": [
            {"id": 0, "label": "v0", "k_label": 5},
            {"id": 1, "label": "v1", "k_label": 3}
          ],
          "edges": [
            {"source": 0, "target": 1, "weight": 8},
            {"source": 0, "target": 2, "weight": 7}
          ]
        }
        ```

3.  **Dedicated Graph Visualization Software Integration:**
    *   Export the graph data into a format compatible with dedicated graph visualization software (e.g., Gephi, Cytoscape). These tools are designed for complex graph analysis and visualization and offer advanced layout and filtering options.

## Implementation Steps (High-Level)

1.  **Research and Select Tools:** Evaluate Graphviz layout options, and explore interactive JS libraries (D3.js, Plotly.js, vis.js) or Python visualization libraries (NetworkX + Matplotlib/Bokeh/Plotly).
2.  **Modify `visualization.py`:**
    *   For PNGs: Add parameters to `visualize_k_labeling` to control Graphviz layout engine, node/edge spacing, and label font sizes.
    *   For interactive: Add a new function (e.g., `generate_interactive_visualization`) that outputs HTML/JSON.
3.  **Update `main.py`:** Add command-line arguments to select the visualization output type (e.g., `--output-format png` or `--output-format html`).
4.  **Develop Interactive Frontend (if applicable):** Create a basic HTML/JS template to load and display the graph data.
5.  **Testing:** Thoroughly test the new visualization options with various circulant graph parameters to ensure readability improvements.
