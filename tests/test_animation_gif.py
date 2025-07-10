from pathlib import Path

# Ensure all animation dependencies are installed; missing libs will cause test failure

from src.graph_generator import create_mongolian_tent_graph

import matplotlib  # type: ignore

matplotlib.use("Agg")  # non-interactive backend for testing
from src.visualization.animation import AnimationController
from src.labeling_solver import greedy_k_labeling, is_labeling_valid


def test_gif_record_mode(tmp_path):
    """Verify that AnimationController records frames and writes a non-empty GIF."""
    graph = create_mongolian_tent_graph(3)
    controller = AnimationController(graph, mode="record", fps=5)

    # Run a quick greedy solve emitting events to the controller.
    labeling = greedy_k_labeling(graph, k_upper_bound=5, attempts=1, on_step=controller.update)
    assert labeling and is_labeling_valid(graph, labeling), "solver failed to produce labeling"

    # Save to temporary location
    gif_path: Path = controller.save(tmp_path / "test_anim.gif")
    assert gif_path.exists(), "GIF file was not created"
    assert gif_path.stat().st_size > 0, "GIF file is empty" 