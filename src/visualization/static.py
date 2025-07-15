"""Graph visualization utilities for Mongolian Tent graphs.

Requires the `graphviz` Python package and Graphviz binaries installed on the system.

References:
    - ai-docs/enhancments/enhancment01_add_visualization.md (initial visualization feature design)
    - ai-docs/initial-design/task_4.md (task detailing visualization requirements)
    - ai-docs/fixes/fix_backtracking_performance.md (context on visualization of performance results)
"""
from pathlib import Path
from typing import Dict, Any, Tuple, Optional

try:
    from graphviz import Graph  # type: ignore
except ImportError as e:
    raise ImportError("Graphviz python package is required. Install via `pip install graphviz`.") from e

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
    if validate:
        from src.labeling_solver import _get_generic_vertex_sort_key
        assert is_labeling_valid(graph, labeling, sort_key_func=_get_generic_vertex_sort_key), "Labeling is not valid (duplicate edge weights)."

    fmt = Path(output).suffix.lstrip(".") or "png"
    dest_path = Path(output)
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    # Use an undirected Graph to remove arrowheads in the rendered output.
    # Use 'dot' engine for shaped (Mongolian Tent) layouts and 'circo' for circulant radial layouts
    engine = "dot" if shaped else "neato"
    dot = Graph(format=fmt, engine=engine)  # type: ignore
    if shaped:
        dot.attr(rankdir="TB")
    else: # For circulant graphs, set up a circular layout
        dot.attr(overlap="false", splines="true", sep="0.5", K="0.6") # Adjust these for better layout

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
        from graphviz import Graph as _G

        # Group vertices by their row index.
        row_to_vertices: Dict[int, list] = {}
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
                cluster.edge(
                    format_vertex_id(vertices[i]),
                    format_vertex_id(vertices[i+1]),
                    style="invis",
                )
            dot.subgraph(cluster)

        # Apex vertex (top of the tent)
        if 'x' in labeling:
            apex_node = format_vertex_id('x')
            dot.node(apex_node, label=f"{labeling['x']}")
            dot.subgraph(_G(name='apex', body=[apex_node], graph_attr={'rank': 'min'}))
    else:
        import math

        node_ids = sorted([v for v in graph.keys() if isinstance(v, int)])
        n_nodes = len(node_ids)
        radius = 2.0  # arbitrary radius
        for idx, v in enumerate(node_ids):
            angle = 2 * math.pi * idx / n_nodes
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            # pos attribute with ! to fix position
            dot.node(format_vertex_id(v), label=f"{labeling.get(v, '')}", pos=f"{x},{y}!")

    # Add edges with weights
    added: set[tuple] = set()
    for u, neighbors in graph.items():
        for v in neighbors:
            if (v, u) in added:
                continue
            added.add((u, v))
            if u in labeling and v in labeling:
                weight = labeling[u] + labeling[v]
                dot.edge(format_vertex_id(u), format_vertex_id(v), label=str(weight))
            else:
                dot.edge(format_vertex_id(u), format_vertex_id(v))

    rendered_path = Path(dot.render(filename=dest_path.stem, directory=dest_path.parent, cleanup=True))
    return rendered_path


def draw_state(
    graph: Dict[Any, list],
    labels: Dict[Any, int],
    *,
    highlight: Any | None = None,
    ax: Optional[Any] = None,
    pos: Dict[Any, Tuple[float, float]] | None = None,
    node_size: int = 300,
) -> Any:
    """Draw the current labeling state using Matplotlib/NetworkX."""
    import networkx as nx
    import matplotlib.pyplot as _plt  # type: ignore

    if ax is None:
        _fig, ax = _plt.subplots()  # type: ignore
        ax.set_axis_off()  # type: ignore

    G = nx.Graph()
    for u, nbrs in graph.items():
        for v in nbrs:
            G.add_edge(u, v)

    if pos is None:
        pos = nx.spring_layout(G, seed=42)

    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#cccccc")

    labeled_nodes = list(labels.keys())
    unlabeled_nodes = [v for v in G.nodes if v not in labeled_nodes]

    nx.draw_networkx_nodes(G, pos, nodelist=unlabeled_nodes, node_color="#eeeeee", ax=ax, node_size=node_size)
    nx.draw_networkx_nodes(G, pos, nodelist=labeled_nodes, node_color="#7fc97f", ax=ax, node_size=node_size)

    if highlight is not None:
        nx.draw_networkx_nodes(G, pos, nodelist=[highlight], node_color="#fc8d62", ax=ax, node_size=node_size * 1.2)

    lbl_map = {v: str(labels[v]) for v in labeled_nodes}
    nx.draw_networkx_labels(G, pos, labels=lbl_map, ax=ax, font_size=8)

    return ax


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