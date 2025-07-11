# Task List: Decouple Animation Rendering from Solver Execution

> Track progress by ticking the checkboxes ([x]) as you complete each item.

---

## 1. Event Buffering in Solver
- [x] Add optional `on_event: Callable[[StepEvent], None]` parameter to all solver entry points (`find_optimal_k_labeling`, `find_feasible_k_labeling`, `find_feasible_k_labeling`, etc.)
- [x] Implement `EventRecorder` class that collects `StepEvent` instances into a list
- [x] Replace record-mode direct use of `AnimationController` with `EventRecorder` in solver CLI path

## 2. Extract Rendering Logic into Base Class
- [x] Define `BaseRenderer` (or helper module) encapsulating:
  - `__init__(graph, mode, fps, figsize)` setup
  - `_setup_plot()`: one-time layout and figure initialization
  - `_render_frame()`: draw edges, nodes, labels, highlights
- [x] Refactor `AnimationController` to inherit from `BaseRenderer` and implement live update/update+record logic

## 3. Implement Offline Replay Renderer
- [x] Create `ReplayController(BaseRenderer)` that:
  - Accepts a buffered `List[StepEvent]`
  - Iterates events and calls `update(ev)` to produce frames
- [x] Add `ReplayController.save(path: str, fps: int, sample_rate: Optional[int] = None)` method to write GIF/MP4

## 4. Lazy Layout Caching
- [x] Ensure layout (`self._pos`) is computed once and stored in `c` during initialization
- [x] Update live and replay paths to reuse cached layout without recalculation

## 5. Batching and Rate-Limiting Frames
- [x] Implement event-to-frame down-sampling: e.g., 1 frame per N events or per time window (1/fps)
- [x] Expose `sample_rate` or `max_frames` parameter in `ReplayController.save()`

## 6. Asynchronous Frame Writing (Optional)
- [x] Integrate `imageio.get_writer(..., mode='I')` for streaming frames to disk
- [x] Offload encoding to a background thread/process to reduce peak memory usage

## 7. CLI Integration
- [x] Update `main.py`:
  - In record mode: use `EventRecorder` during solve, then instantiate `ReplayController` to generate frames
  - In live mode: instantiate `AnimationController` for real-time display
- [x] Document new behavior and flags in `README.md`

## 8. Test Updates
- [x] Adjust `test_animation_events.py` to verify events are collected by `EventRecorder`
- [x] Modify GIF tests to use `ReplayController.save()` instead of `AnimationController`
- [x] Ensure live-mode tests still pass unmodified

---

*Completion Criteria:* All above checkboxes ticked, CI passes with zero rendering overhead during solve, and recorded animations are identical to original behavior. 