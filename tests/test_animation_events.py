from src.labeling_solver import find_feasible_k_labeling
from src.events import EventType, StepEvent


def test_event_emission_count_small_graph():
    """Ensure the solver emits the expected number of VERTEX_LABELED events.

    For a small graph we expect exactly one *VERTEX_LABELED* event per vertex
    present in the final solution.  The solver additionally emits a
    *SOLUTION_FOUND* event containing the complete ``labels`` mapping – this is
    used below to derive the expected vertex count in a backend-agnostic way
    (we do not depend on knowledge of Mongolian Tent graph order).
    """
    events: list[StepEvent] = []

    def _collector(ev: StepEvent):
        events.append(ev)

    # Use a tiny graph (n=3) and the fast heuristic for speed inside CI.
    k, labeling = find_feasible_k_labeling(3, algorithm="fast", on_step=_collector)

    # Basic sanity guard – solver should succeed.
    assert k is not None and labeling, "solver failed on n=3 with animation enabled"

    labeled_events = [e for e in events if e.type is EventType.VERTEX_LABELED]
    solution_events = [e for e in events if e.type is EventType.SOLUTION_FOUND]

    # Exactly one solution event must be emitted.
    assert len(solution_events) == 1, "expected a single SOLUTION_FOUND event"

    expected_vertex_count = len(
        solution_events[0].data["labels"]
    )  # robust to graph size

    assert len(labeled_events) == expected_vertex_count, (
        f"number of VERTEX_LABELED events does not match vertices in final "
        f"solution ({len(labeled_events)} vs {expected_vertex_count})"
    ) 