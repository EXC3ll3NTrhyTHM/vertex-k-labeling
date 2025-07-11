# Enhancement 04 – Task List: Animated Visualization for the Labeling Solver

> Track progress by ticking the checkboxes (\[x\]) as you complete each item.

---

## Goal

Deliver an animated visualization feature that illustrates every labeling step, supports live and recorded modes, and integrates seamlessly with existing solver APIs without affecting performance when disabled.

## High-Level Overview

1. **Instrumentation** – Emit structured *step events* from the solver.
2. **Animation Controller** – Consume events, update state, render frames.
3. **Rendering** – Reuse Matplotlib for live display; use `imageio` for GIF/MP4 export.
4. **CLI & API** – Offer `--animate` flag and optional callback parameter.
5. **Quality Assurance** – Unit tests validating functionality and performance.
6. **Documentation** – Examples, GIFs, and README updates.

---

## Detailed Checklist

### 1. Event System
- [x] Design `StepEvent` dataclass in `src/events.py` (type, payload, timestamp)
- [x] Add `on_step` callback parameter to `LabelingSolver` constructor
- [x] Insert `_emit()` calls at key points in heuristic solver
- [x] Insert `_emit()` calls at key points in backtracking solver

### 2. Animation Controller (`src/visualization/animation.py`)
- [x] Implement `__init__(graph, mode, fps)` with internal state copy
- [x] Implement `update(event)` to mutate state & (optionally) render
- [x] Implement frame storage for **record** mode
- [x] Implement `save(path)` using `imageio` to compile GIF/MP4

### 3. Visualization Helpers
- [x] Extend `visualization.py` with `draw_state(graph, labels, highlight=None)`
- [x] Ensure consistent styling with existing static images

### 4. CLI & Configuration
- [x] Add `--animate {off,live,record}` flag in `main.py` (default `off`)
- [x] Wire flag to instantiate `AnimationController` and pass its `update` callback

### 5. Tests
- [ ] Unit test: Event emission count matches expected steps for small graph
- [ ] Unit test: GIF file created and non-empty in record mode
- [ ] Integration test: Solver results identical with animation enabled/disabled

### 6. Documentation & Examples
- [ ] Update `README.md` usage section with animation examples
- [ ] Add animated GIF demo under `graphs/`
- [ ] Create Jupyter notebook showcasing live animation

### 7. Performance Validation
- [ ] Benchmark runtime overhead for *n* = 100 (target <10%)
- [ ] Verify memory footprint stays below 500 MB in record mode for *n* = 200

---

## Completion Criteria

- [ ] All checklist items above are ticked.
- [ ] CI passes with animation feature toggled on & off.
- [ ] Acceptance criteria in the [Enhancement document](./enhancement04_animation_label_solver.md#acceptance-criteria) are satisfied. 
