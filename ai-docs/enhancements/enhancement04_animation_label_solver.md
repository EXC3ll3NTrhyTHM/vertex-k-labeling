# Enhancement 04: Animated Visualization for the Labeling Solver

## Motivation

While static graphs and final labeling screenshots help validate correctness, they do not reveal **how** the solver reaches its solution. An animated visualization will:

1. Provide an intuitive, step-by-step illustration of the solver’s decision-making process.
2. Help developers debug heuristics and backtracking by visually spotting sub-optimal or redundant moves.
3. Serve as an engaging educational tool for presentations and documentation.

## Goals & Non-Goals

| Area | Goals | Non-Goals |
|------|-------|-----------|
| **Visualization** | Show each labeling step, highlight updated vertices/edges, display current objective value | 3-D renderings, complex camera controls |
| **Performance** | Handle graphs up to *n* = 200 in real-time (>30 fps) | Deep performance profiling/optimizations outside visualization scope |
| **Integration** | Minimal API changes to existing `labeling_solver` public interface | Refactor of solver algorithms |
| **Export** | Optionally save animation as GIF/MP4 | Advanced video editing features |

## High-Level Design

```
┌──────────────┐   step events   ┌──────────────────────┐   frames   ┌──────────────┐
│ labeling_…   │───────────────►│ AnimationController  │───────────►│ Matplotlib / │
│  Solver      │                │ (new module)         │            │  Pillow      │
└──────────────┘                └──────────────────────┘            └──────────────┘
```

1. **Instrumentation Hooks**:  
   Add a light-weight callback mechanism inside `labeling_solver.SolverBase` that emits *step events* (vertex labeled, edge weight calculated, backtrack, etc.).

2. **AnimationController** (new module in `src/visualization/animation.py`):  
   • Receives step events and updates an internal representation of the graph.  
   • Decides whether to render immediately (live mode) or store frames (record mode).

3. **Rendering Backend**:  
   Use **Matplotlib** for immediate cross-platform rendering (already a dependency) and **Pillow** to compile frames into GIF/MP4 via `imageio`.

## API Changes

```python
# src/labeling_solver.py
class LabelingSolver:
    def __init__(self, ..., on_step: Callable[[StepEvent], None] | None = None):
        self._on_step = on_step

    def _emit(self, event: StepEvent):
        if self._on_step:
            self._on_step(event)
```

```python
solver = LabelingSolver(...)
anim   = AnimationController(graph, mode="record", fps=30)
solver.solve(on_step=anim.update)
anim.save("solver_run.gif")
```

No breaking change: callers that ignore `on_step` behave exactly as before.

## Implementation Steps

1. **Define `StepEvent` dataclass** (`src/events.py`)
2. **Embed `_emit()` calls** in heuristic & backtracking loops (≈10 touch-points).
3. **Create `AnimationController`** with two public methods:  
   • `update(event)` – called by solver.  
   • `save(path)` – compile frames if in record mode.
4. **Extend `visualization.py`** with helper to draw current graph state (reuse existing styling).
5. **CLI Flag**: `--animate [live|record]` in `main.py` default *off*.
6. **Unit Tests**:  
   • Verify that enabling animation does not alter solver results.  
   • Check that GIF file is generated and non-empty.
7. **Documentation & Examples**:  
   • Add animated GIFs to `README.md`.  
   • Provide sample notebook.

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Performance overhead on large graphs | Emit events only when animation enabled. Use shallow copies, avoid full graph redraw if unchanged. |
| Memory consumption when recording | Stream frames to disk using a temporary directory. |
| Dependency bloat | Reuse existing Matplotlib; add lightweight `imageio` (≈1 MB). |

## Acceptance Criteria

- Running `python main.py --n 20 --heuristic --animate record` produces a GIF <10 MB in ≤2× solver runtime.
- Live mode shows smooth updates at ≥30 fps on *n* ≤100.
- Unit tests pass on CI with animation enabled/disabled.

## Timeline (1 FTE)

| Week | Deliverable |
|------|-------------|
| 1 | Event API draft & instrumentation hooks |
| 2 | AnimationController prototype & live mode |
| 3 | Record mode, GIF export, CLI integration |
| 4 | Docs, tests, polish, PR review |

## References

- Matplotlib animation docs: https://matplotlib.org/stable/api/animation_api.html
- ImageIO for GIF: https://imageio.readthedocs.io/
- Prior art: NetworkX drawing with dynamic updates 