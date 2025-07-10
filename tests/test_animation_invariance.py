from src.labeling_solver import find_optimal_k_labeling
from src.events import StepEvent


def test_solver_invariance_with_animation():
    """Solver results must be identical regardless of animation callback."""

    # Run without animation
    k_no_anim, lbl_no_anim = find_optimal_k_labeling(3)
    assert k_no_anim is not None and lbl_no_anim is not None, "solver failed without animation"

    # Run with dummy collector that records events but does nothing
    collected: list[StepEvent] = []

    def _collector(ev: StepEvent):
        collected.append(ev)

    k_anim, lbl_anim = find_optimal_k_labeling(3, on_step=_collector)

    # Ensure solver succeeded and matches baseline
    assert k_anim == k_no_anim, "k differs when animation enabled"
    assert lbl_anim == lbl_no_anim, "labeling differs when animation enabled"

    # Sanity check that some events were indeed collected
    assert collected, "no events were emitted during solver run" 