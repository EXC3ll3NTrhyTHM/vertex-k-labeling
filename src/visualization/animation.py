from __future__ import annotations

from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from .base_renderer import BaseRenderer

try:
    import imageio.v2 as imageio  # modern imageio api
except ImportError:  # pragma: no cover – imageio is optional until record mode used
    imageio = None  # type: ignore

from src.events import StepEvent, EventType

__all__ = ["AnimationController"]


class AnimationController(BaseRenderer):
    """Consume solver *StepEvent*s and produce a live or recorded animation.

    Parameters
    ----------
    graph:
        Adjacency list of the graph being solved.
    mode:
        "off" (default), "live", or "record". In *live* mode frames are drawn to
        screen interactively. In *record* mode, frames are collected and later
        saved to a GIF/MP4 via :meth:`save`.
    fps:
        Desired frames per second when recording.
    figsize:
        Size of the Matplotlib figure.
    """

    def __init__(
        self,
        graph: Dict[Any, List[Any]],
        *,
        mode: str = "live",
        fps: int = 30,
        figsize: Tuple[int, int] = (6, 6),
    ) -> None:
        # Initialize base renderer (caches layout, sets up figure/axes)
        super().__init__(graph, mode=mode, fps=fps, figsize=figsize)
        # If recording, capture initial frame
        if self.mode == "record":
            self._render_frame()

    # ---------------------
    # Public API
    # ---------------------

    def update(self, event: StepEvent):  # noqa: D401 – simple updater
        """Callback to be passed to solver; handles one *StepEvent*."""
        if self.mode == "off":
            return  # noop

        # Update labels and set highlight on change/backtrack
        if event.type == EventType.VERTEX_LABELED:
            vertex = event.data["vertex"]
            self.labels[vertex] = event.data["label"]
            self.highlighted_vertex = vertex
        elif event.type == EventType.BACKTRACK:
            vertex = event.data["vertex"]
            self.labels.pop(vertex, None)
            self.highlighted_vertex = vertex

        self._render_frame()

    def save(self, path: str | Path) -> Path:
        """Save recorded frames to *path* (GIF/MP4 depending on extension)."""
        if self.mode != "record":
            raise RuntimeError("save() is only valid in 'record' mode")
        if not self.frames:
            raise RuntimeError("no frames have been recorded")

        dest = Path(path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        fmt = dest.suffix.lower()

        if fmt in {".gif", ".mp4"}:
            if imageio is None:
                raise ImportError("imageio is required for saving animations. Install via 'pip install imageio'.")
            imageio.mimsave(dest, self.frames, fps=self.fps)
        else:
            raise ValueError("Unsupported animation format. Use .gif or .mp4")
        return dest

    # ---------------------
    # Internal helpers
    # ---------------------

    def _setup_plot(self) -> None:
        # Use precomputed layout and axes from BaseRenderer
        # Draw static edges once
        import networkx as nx  # type: ignore

        nx.draw_networkx_edges(nx.Graph(self.graph), self._pos, ax=self._ax, edge_color="#cccccc")
        self._nodes = None  # will be scatter collection
        self._labels_text = {}

    def _render_frame(self) -> None:
        import networkx as nx

        if self._fig is None:
            # Lazy setup for record mode (avoid display)
            self._setup_plot()

        self._ax.clear()  # type: ignore[attr-defined]
        self._ax.set_axis_off()  # type: ignore[attr-defined]

        # Draw current state
        G = nx.Graph()
        for u, neighbors in self.graph.items():
            for v in neighbors:
                G.add_edge(u, v)
        # Draw edges
        nx.draw_networkx_edges(G, self._pos, ax=self._ax, edge_color="#cccccc")
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

        # Node colors based on labeled/unlabeled
        labeled_nodes = list(self.labels.keys())
        unlabeled_nodes = [v for v in self.graph.keys() if v not in labeled_nodes]
        nx.draw_networkx_nodes(G, self._pos, nodelist=unlabeled_nodes, ax=self._ax, node_color="#eeeeee")
        # Draw labeled nodes, separating highlighted vertex
        if self.highlighted_vertex in labeled_nodes:
            other_nodes = [v for v in labeled_nodes if v != self.highlighted_vertex]
            if other_nodes:
                nx.draw_networkx_nodes(
                    G,
                    self._pos,
                    nodelist=other_nodes,
                    ax=self._ax,
                    node_color="#7fc97f",
                )
            # Highlight most recently changed vertex in yellow
            nx.draw_networkx_nodes(
                G,
                self._pos,
                nodelist=[self.highlighted_vertex],
                ax=self._ax,
                node_color="#ffff00",
            )
        else:
            nx.draw_networkx_nodes(G, self._pos, nodelist=labeled_nodes, ax=self._ax, node_color="#7fc97f")

        # Draw labels
        lbl_mapping = {v: str(self.labels[v]) for v in labeled_nodes}
        nx.draw_networkx_labels(G, self._pos, labels=lbl_mapping, ax=self._ax, font_size=8)

        self._fig.canvas.draw()  # type: ignore[attr-defined]

        if self.mode == "live":
            plt.pause(0.001)
        elif self.mode == "record":
            # Save current frame as numpy array
            import numpy as np

            # Attempt to grab RGB buffer; fallback to RGBA buffer if needed
            try:
                buf = self._fig.canvas.tostring_rgb()  # type: ignore[attr-defined]
                w, h = self._fig.canvas.get_width_height()  # type: ignore[attr-defined]
                frame = np.frombuffer(buf, dtype=np.uint8).reshape((h, w, 3))
            except Exception:
                # Fallback to print_to_buffer for backends without tostring_rgb
                buf, (w, h) = self._fig.canvas.print_to_buffer()  # type: ignore[attr-defined]
                arr = np.frombuffer(buf, dtype=np.uint8).reshape((h, w, 4))
                frame = arr[..., :3]
            self.frames.append(frame)

    # Context manager for cleaner usage (optional)
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.mode == "live":
            plt.close(self._fig) 