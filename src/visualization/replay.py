from pathlib import Path
from typing import List, Optional

import imageio.v2 as imageio  # type: ignore
import numpy as np

from .base_renderer import BaseRenderer
from src.events import StepEvent, EventType
from threading import Thread  # add for async writing
from queue import Queue  # add for frame queue

__all__ = ["ReplayController"]

class ReplayController(BaseRenderer):
    """Consume a list of StepEvent objects to produce a recorded animation."""

    def __init__(
        self,
        graph,
        events: List[StepEvent],
        *,
        fps: int = 30,
        figsize: tuple[int, int] = (6, 6),
        sample_rate: Optional[int] = None,
    ) -> None:
        # Initialize base renderer in record mode
        super().__init__(graph, mode="record", fps=fps, figsize=figsize)
        self.events = events
        self.sample_rate = sample_rate

    def update(self, event: StepEvent) -> None:
        # Update labels and highlight
        if event.type == EventType.VERTEX_LABELED:
            vertex = event.data["vertex"]
            self.labels[vertex] = event.data["label"]
            self.highlighted_vertex = vertex
        elif event.type == EventType.BACKTRACK:
            vertex = event.data["vertex"]
            self.labels.pop(vertex, None)
            self.highlighted_vertex = vertex
        # Render frame after state update
        self._render_frame()

    def save(
        self,
        path: str | Path,
        sample_rate: Optional[int] = None,
    ) -> Path:
        """Stream-replay events to write frames on-the-fly to GIF/MP4."""
        # Allow overriding sample_rate at call time
        sr = sample_rate if sample_rate is not None else self.sample_rate
        dest = Path(path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        fmt = dest.suffix.lower()
        if imageio is None:
            raise ImportError(
                "imageio is required for saving animations. Install via 'pip install imageio'."
            )
        if fmt not in {".gif", ".mp4"}:
            raise ValueError("Unsupported animation format. Use .gif or .mp4")

        # Asynchronously write frames to reduce memory and blocking
        frame_queue: Queue = Queue()

        def _writer():
            with imageio.get_writer(dest, fps=self.fps, mode="I") as writer:
                while True:
                    frame = frame_queue.get()
                    if frame is None:
                        break
                    writer.append_data(frame)  # type: ignore[attr-defined]

        writer_thread = Thread(target=_writer, daemon=True)
        writer_thread.start()

        # Generate frames and feed to writer thread
        for idx, ev in enumerate(self.events):
            if sr is None or idx % sr == 0:
                self.update(ev)
                frame_queue.put(self.frames[-1])

        # Signal completion and wait for writer
        frame_queue.put(None)
        writer_thread.join()
        return dest 