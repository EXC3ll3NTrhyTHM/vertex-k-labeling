from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional

import matplotlib.pyplot as plt
import networkx as nx

class BaseRenderer(ABC):
    """Base class providing graph layout and frame rendering capabilities."""

    def __init__(
        self,
        graph: Dict[Any, List[Any]],
        *,
        mode: str = "live",
        fps: int = 30,
        figsize: Tuple[int, int] = (6, 6),
    ) -> None:
        if mode not in {"off", "live", "record"}:
            raise ValueError("mode must be 'off', 'live', or 'record'")
        self.graph = graph
        self.mode = mode
        self.fps = fps
        self.figsize = figsize

        # Internal state
        self.labels: Dict[Any, int] = {}
        self.highlighted_vertex: Any | None = None
        self.frames: List[Any] = []

        # Precompute layout once
        G = nx.Graph()
        for u, neighbors in self.graph.items():
            for v in neighbors:
                G.add_edge(u, v)
        self.pos = nx.spring_layout(G, seed=42)
        # Alias for backward compatibility
        self._pos = self.pos

        # Setup figure/axes for live or record modes
        if self.mode in {"live", "record"}:
            self._fig, self._ax = plt.subplots(figsize=self.figsize)
            self._ax.set_axis_off()
            # Draw static edges once for both live and record modes
            self._draw_static()

    @abstractmethod
    def update(self, event: Any) -> None:
        """Handle a StepEvent (or equivalent) to update internal state and render frame."""
        ...

    def _draw_static(self) -> None:
        """Draw static graph elements (edges) once and cache the artist."""
        # Cache static edges as a LineCollection
        static_graph = nx.Graph()
        for u, neighbors in self.graph.items():
            for v in neighbors:
                static_graph.add_edge(u, v)
        self._static_edges = nx.draw_networkx_edges(
            static_graph,
            self.pos,
            ax=self._ax,
            edge_color="#cccccc",
        )  # type: ignore

    def _render_frame(self) -> None:
        """Render current graph state, overlay dynamic elements, then capture frame if in record mode."""
        import networkx as nx  # type: ignore
        # Remove previous dynamic overlays (all but the first static edges collection)
        # Preserve static edges drawn by _draw_static (first collection)
        collections = list(self._ax.collections)
        for coll in collections[1:]:
            coll.remove()
        # Remove dynamic text elements (labels)
        for txt in list(self._ax.texts):
            txt.remove()

        # Dynamic overlays; static edges already drawn once by _draw_static
        G = nx.Graph()
        for u, neighbors in self.graph.items():
            for v in neighbors:
                G.add_edge(u, v)

        # Draw edge weight labels for labeled edges
        edge_labels: Dict[tuple, str] = {}
        for u, v in G.edges():
            if u in self.labels and v in self.labels:
                edge_labels[(u, v)] = str(self.labels[u] + self.labels[v])
        if edge_labels:
            nx.draw_networkx_edge_labels(
                G,
                self._pos,
                edge_labels=edge_labels,
                ax=self._ax,
                font_size=6,
            )

        # Draw nodes
        labeled_nodes = list(self.labels.keys())
        unlabeled_nodes = [v for v in self.graph.keys() if v not in labeled_nodes]
        nx.draw_networkx_nodes(
            nx.Graph(self.graph),
            self.pos,
            nodelist=unlabeled_nodes,
            ax=self._ax,
            node_color="#eeeeee",
        )
        # Highlight and draw labeled nodes
        if self.highlighted_vertex in labeled_nodes:
            other_nodes = [v for v in labeled_nodes if v != self.highlighted_vertex]
            if other_nodes:
                nx.draw_networkx_nodes(
                    nx.Graph(self.graph),
                    self.pos,
                    nodelist=other_nodes,
                    ax=self._ax,
                    node_color="#7fc97f",
                )
            nx.draw_networkx_nodes(
                nx.Graph(self.graph),
                self.pos,
                nodelist=[self.highlighted_vertex],
                ax=self._ax,
                node_color="#ffff00",
            )
        else:
            nx.draw_networkx_nodes(
                nx.Graph(self.graph),
                self.pos,
                nodelist=labeled_nodes,
                ax=self._ax,
                node_color="#7fc97f",
            )

        # Draw labels on nodes
        lbl_mapping = {v: str(self.labels[v]) for v in labeled_nodes}
        nx.draw_networkx_labels(
            nx.Graph(self.graph),
            self.pos,
            labels=lbl_mapping,
            ax=self._ax,
            font_size=8,
        )

        # Overlay blue highlights on edges incident to the highlighted vertex
        if self.highlighted_vertex is not None:
            incident_edges = [
                (u, v) for u, vs in self.graph.items() for v in vs
                if self.highlighted_vertex in (u, v)
            ]
            if incident_edges:
                nx.draw_networkx_edges(
                    nx.Graph(self.graph),
                    self.pos,
                    edgelist=incident_edges,
                    ax=self._ax,
                    edge_color="#0000ff",
                )

        # Render draw
        self._fig.canvas.draw()  # type: ignore[attr-defined]

        # Capture frame if in record mode
        if self.mode == "record":
            import numpy as np  # type: ignore
            try:
                buf = self._fig.canvas.tostring_rgb()  # type: ignore[attr-defined]
                w, h = self._fig.canvas.get_width_height()  # type: ignore[attr-defined]
                frame = np.frombuffer(buf, dtype=np.uint8).reshape((h, w, 3))
            except Exception:
                buf, (w, h) = self._fig.canvas.print_to_buffer()  # type: ignore[attr-defined]
                arr = np.frombuffer(buf, dtype=np.uint8).reshape((h, w, 4))
                frame = arr[..., :3]
            self.frames.append(frame)

    def save(self, path: str) -> Path:
        """Optional helper for batch frame saving (to be implemented by subclass)."""
        raise NotImplementedError

__all__ = ["BaseRenderer"] 