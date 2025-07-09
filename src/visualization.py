"""Graph visualization utilities for Mongolian Tent graphs.

Requires the `graphviz` Python package and Graphviz binaries installed on the system.

References:
    - ai-docs/enhancments/enhancment01_add_visualization.md (initial visualization feature design)
    - ai-docs/initial-design/task_4.md (task detailing visualization requirements)
    - ai-docs/fixes/fix_backtracking_performance.md (context on visualization of performance results)
"""
from pathlib import Path
from typing import Dict, Any, Tuple

try:
    from graphviz import Graph  # type: ignore
except ImportError as e:  # pragma: no cover
    raise ImportError("Graphviz python package is required. Install via `pip install graphviz`." ) from e

from src.labeling_solver import is_labeling_valid  # for optional validation

__all__ = ["visualize_k_labeling"]


def format_vertex_id(v: Any) -> str:
    """Return a stable string representation for vertex IDs usable in DOT."""
    return str(v).replace(" ", "")


def visualize_k_labeling(
    graph: Dict[Any, list],
    labeling: Dict[Any, int],
    output: str = "graph.png",
    validate: bool = False,
    *,
    shaped: bool = True,
    heuristic_k: int | None = None,
    lower_bound_k: int | None = None,
    gap: int | str | None = None,
    time_taken: float | None = None,
    solver_name: str | None = None,
) -> Path:
    """Render the labeled graph to an image using Graphviz.

    Args:
        graph: adjacency list of the graph.
        labeling: mapping of vertex -> label (k value).
        output: path to output file (.png, .svg, etc.). Format inferred from extension.
        validate: if True, assert that the labeling has no duplicate edge weights.
        shaped: if True, use top-to-bottom flow and create clusters for top and bottom rows.
        heuristic_k: the heuristic k value.
        lower_bound_k: the lower bound k value.
        gap: the gap between heuristic k and lower bound k.
        time_taken: the time taken to find k.
        solver_name: the name of the solver used (e.g., "Heuristic" or "Backtracking").

    Returns:
        Path to the generated file.

    References:
        - ai-docs/enhancments/enhancment01_add_visualization.md (visualization algorithm details)
        - ai-docs/refactor/refactoring_task.md (notes on modularization of visualization utilities)
    """
    if validate:
        assert is_labeling_valid(graph, labeling), "Labeling is not valid (duplicate edge weights)."

    fmt = Path(output).suffix.lstrip(".") or "png"
    dest_path = Path(output)
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    # Use an undirected Graph to remove arrowheads in the rendered output.
    # Use 'dot' engine for shaped (Mongolian Tent) layouts and 'circo' for circulant radial layouts
    engine = "dot" if shaped else "neato"
    dot = Graph(format=fmt, engine=engine)
    if shaped:
        dot.attr(rankdir="TB")

    # Add a global label for the graph with the k values
    label_text = []
    if solver_name is not None:
        label_text.append(f"Solver: {solver_name}")
    if heuristic_k is not None:
        label_text.append(f"Heuristic K: {heuristic_k}")
    if lower_bound_k is not None:
        label_text.append(f"Lower Bound K: {lower_bound_k}")
    if gap is not None:
        label_text.append(f"Gap: {gap}")
    if time_taken is not None:
        label_text.append(f"Time Taken: {time_taken:.2f} seconds")

    if label_text:
        dot.attr(label="\n".join(label_text), labelloc="t", labeljust="l")

    dot.attr("node", shape="circle", style="filled", color="#D5E8D4")

    if shaped:
        # Create horizontal clusters for each ladder row (row index = first element in tuple vertex)
        # Supports arbitrary number of rows; for the Mongolian Tent graph we expect 3.
        # Sub-graphs must match the parent graph type, so we also use Graph here.
        from graphviz import Graph as _G

        # Group vertices by their row index.
        row_to_vertices = {}
        for v in labeling:
            if isinstance(v, tuple):
                row_to_vertices.setdefault(v[0], []).append(v)

        for row_idx in sorted(row_to_vertices):
            vertices = sorted(row_to_vertices[row_idx], key=lambda x: x[1])
            cluster = _G(name=f"row_{row_idx}")
            cluster.attr(rank="same", style="invis")
            for v in vertices:
                cluster.node(format_vertex_id(v), label=f"{labeling[v]}")
            # Add invisible edges between consecutive vertices to enforce ordering within the rank.
            for i in range(len(vertices) - 1):
                cluster.edge(format_vertex_id(vertices[i]), format_vertex_id(vertices[i+1]), style="invis")
            dot.subgraph(cluster)

        # Apex vertex (top of the tent)
        if 'x' in labeling:
            apex_node = format_vertex_id('x')
            dot.node(apex_node, label=f"{labeling['x']}")
            # Force apex to top rank explicitly.
            dot.subgraph(_G(name='apex', body=[apex_node], graph_attr={'rank': 'min'}))
    else:
        # For circulant graphs (shaped=False), explicitly order nodes in a circle.
        # Assumes nodes are integers 0 to n-1.
        import math
        node_ids = sorted([v for v in graph.keys() if isinstance(v, int)])
        n_nodes = len(node_ids)
        radius = 2.0  # arbitrary radius
        for idx, v in enumerate(node_ids):
            angle = 2 * math.pi * idx / n_nodes
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            # pos attribute with ! to fix position
            dot.node(format_vertex_id(v), label=str(v), pos=f"{x},{y}!")

    # Add edges with weights
    added = set()
    for u, neighbors in graph.items():
        for v in neighbors:
            # Avoid duplicate edges
            if (v, u) in added:
                continue
            added.add((u, v))
            if u in labeling and v in labeling:
                weight = labeling[u] + labeling[v]
                dot.edge(format_vertex_id(u), format_vertex_id(v), label=str(weight))
            else:
                # fallback no label
                dot.edge(format_vertex_id(u), format_vertex_id(v))

    # Write file
    rendered_path = Path(dot.render(filename=dest_path.stem, directory=dest_path.parent, cleanup=True))
    return rendered_path


if __name__ == "__main__":  # pragma: no cover
    import argparse
    from src.graph_generator import create_mongolian_tent_graph
    from src.labeling_solver import find_optimal_k_labeling

    parser = argparse.ArgumentParser(description="Visualize Mongolian Tent graph labeling.")
    parser.add_argument("n", type=int, help="Value of n for MT_{3,n}")
    parser.add_argument("--file", default="graph.png", help="Output image file (extension decides format)")
    args = parser.parse_args()

    k, labeling = find_optimal_k_labeling(args.n)
    graph = create_mongolian_tent_graph(args.n)
    if labeling is None:
        raise RuntimeError("Failed to find a valid labeling to visualize.")
    out = visualize_k_labeling(graph, labeling, output=args.file)
    print(f"Graph rendered to {out.resolve()}") 