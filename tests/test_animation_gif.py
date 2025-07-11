from pathlib import Path

# Ensure all animation dependencies are installed; missing libs will cause test failure

import matplotlib  # type: ignore
matplotlib.use("Agg")  # non-interactive backend for testing

from src.graph_generator import create_mongolian_tent_graph
from src.labeling_solver import greedy_k_labeling, is_labeling_valid
from src.visualization.recorder import EventRecorder
from src.visualization.replay import ReplayController


def test_gif_record_mode(tmp_path):
    """Verify that AnimationController records frames and writes a non-empty GIF."""
    graph = create_mongolian_tent_graph(3)
    # Record events during greedy solve using EventRecorder
    events = []
    recorder = EventRecorder(events)
    labeling = greedy_k_labeling(
        graph,
        k_upper_bound=5,
        attempts=1,
        on_event=recorder,
    )
    assert labeling and is_labeling_valid(graph, labeling), "solver failed to produce labeling"

    # Replay events and save to temporary location
    replayer = ReplayController(graph, events, fps=5)
    gif_path: Path = replayer.save(tmp_path / "test_anim.gif")
    assert gif_path.exists(), "GIF file was not created"
    assert gif_path.stat().st_size > 0, "GIF file is empty" 