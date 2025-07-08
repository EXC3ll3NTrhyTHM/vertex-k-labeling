"""Graph visualization utilities for Mongolian Tent graphs.

Requires the `graphviz` Python package and Graphviz binaries installed on the system.
"""
from pathlib import Path
from typing import Dict, Any, Tuple

try:
    from graphviz import Digraph  # type: ignore
except ImportError as e:  # pragma: no cover
    raise ImportError("Graphviz python package is required. Install via `pip install graphviz`." ) from e

from src.labeling_solver import _is_valid_assignment  # for optional validation

__all__ = ["visualize_labeling"]


def _vertex_id(v: Any) -> str:
    """Return a stable string representation for vertex IDs usable in DOT."""
    return str(v).replace(" ", "")


def visualize_labeling(
    graph: Dict[Any, list],
    labeling: Dict[Any, int],
    output: str = "graph.png",
    validate: bool = False,
) -> Path:
    """Render the labeled graph to an image using Graphviz.

    Args:
        graph: adjacency list of the graph.
        labeling: mapping of vertex -> label (k value).
        output: path to output file (.png, .svg, etc.). Format inferred from extension.
        validate: if True, assert that the labeling has no duplicate edge weights.

    Returns:
        Path to the generated file.
    """
    if validate:
        assert _is_valid_assignment(graph, labeling), "Labeling is not valid (duplicate edge weights)."

    fmt = Path(output).suffix.lstrip(".") or "png"
    dest_path = Path(output)

    dot = Digraph(format=fmt)
    dot.attr("node", shape="circle", style="filled", color="#D5E8D4")

    # Add nodes
    for v, lbl in labeling.items():
        dot.node(_vertex_id(v), label=f"{v}\n{lbl}")

    # Add edges with weights
    added = set()
    for u, nbrs in graph.items():
        for v in nbrs:
            # Avoid duplicate edges
            if (v, u) in added:
                continue
            added.add((u, v))
            if u in labeling and v in labeling:
                weight = labeling[u] + labeling[v]
                dot.edge(_vertex_id(u), _vertex_id(v), label=str(weight))
            else:
                # fallback no label
                dot.edge(_vertex_id(u), _vertex_id(v))

    # Write file
    rendered_path = Path(dot.render(filename=dest_path.stem, directory=dest_path.parent, cleanup=True))
    return rendered_path


if __name__ == "__main__":  # pragma: no cover
    import argparse
    from src.graph_generator import generate_mongolian_tent_graph
    from src.labeling_solver import find_minimum_k_labeling

    parser = argparse.ArgumentParser(description="Visualize Mongolian Tent graph labeling.")
    parser.add_argument("n", type=int, help="Value of n for MT_{3,n}")
    parser.add_argument("--file", default="graph.png", help="Output image file (extension decides format)")
    args = parser.parse_args()

    k, labeling = find_minimum_k_labeling(args.n)
    graph = generate_mongolian_tent_graph(args.n)
    out = visualize_labeling(graph, labeling, output=args.file)
    print(f"Graph rendered to {out.resolve()}") 