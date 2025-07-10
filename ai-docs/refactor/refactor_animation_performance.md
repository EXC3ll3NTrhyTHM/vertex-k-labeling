# Refactoring Plan: Decouple Animation Rendering from Solver Execution

## 1. Background
The current `AnimationController` integrates real-time rendering directly into the solver loop via repeated calls to Matplotlib/NetworkX, which adds significant overhead (graph redraws, layout calculations, frame capture) on every step event. In high‐step or large‐*n* scenarios, this can dominate runtime and invalidate performance targets.

## 2. Objectives
- **Zero‐overhead** event emission inside the solver: collecting events should be as cheap as a simple list append.
- **Offline** frame generation: rendering can occur after the solver completes, in a separate pass or process.
- **Flexible playback**: support live, record (GIF/MP4), and post-mortem replay modes with minimal code duplication.
- **Maintain testability**: existing animation tests should pass without change, verifying output correctness.

## 3. Proposed Solution
1. **Event Buffering in Solver**
   - Introduce an `EventRecorder` callback that only appends `StepEvent` instances to a list. Replace current `AnimationController` callbacks during solve.
   - Example API: `events: List[StepEvent] = []; recorder = EventRecorder(events)`.

2. **Offline Replay Renderer**
   - Create a separate `ReplayController` that takes a buffered event list and drives the existing drawing logic (or a specialized lighter renderer).
   - Internally, reuse most of `AnimationController._render_frame()`, but without touching solver performance.

3. **Lazy Layout Caching**
   - Compute graph layout (`self._pos`) once and cache it. Both live and replay renderers reuse this layout without recomputing on each frame.

4. **Batching and Rate‐Limiting**
   - During replay, down-sample events to one frame per 1/fps seconds or one frame per *k* events. This reduces number of render calls and final file size.

5. **Asynchronous Frame Writing**
   - Use `imageio.get_writer(..., mode='I')` with a background thread or process to encode frames as they are produced, lowering peak memory.

6. **Integration Hook**
   - Extend CLI: `--animate record` runs solver with `EventRecorder` then invokes `ReplayController.save(path, fps)`.
   - Preserve `--animate live` functionality by instantiating the existing `AnimationController` only in live mode.

## 4. Detailed Steps
1. Refactor solver signatures:
   - Add optional `on_event: Callable[[StepEvent], None]`.
2. Implement `EventRecorder`:
   ```python
   class EventRecorder:
       def __init__(self, buffer): self.buffer = buffer
       def __call__(self, ev): self.buffer.append(ev)
   ```
3. Extract render logic into base class or helper:
   - Move `draw` and `layout` code out of `AnimationController` into `BaseRenderer`.
4. Create `ReplayController(BaseRenderer)`:
   - Accept `events: List[StepEvent]` and an optional `mode` (`record` vs. `live`).
   - Drive frames by iterating through events and calling `self.update(ev)`.
5. Update `main.py`:
   - In record mode, use `EventRecorder` buffer + `ReplayController.save(...)` after solving.
6. Remove rendering from solver callback in record mode.

## 5. Impact and Testing
- **Performance**: Measuring overhead drops to near-zero during solving; full render cost isolated in a replay phase.
- **Backward Compatibility**: CLI flags unchanged; live animation unchanged.
- **Tests**: Adjust `test_animation_events.py` and GIF tests to use `ReplayController` for recording tests.

## 6. Migration Plan
1. Merge refactoring on a feature branch.
2. Update docs and example notebooks to use new API.
3. Benchmark before/after to validate <10% overhead target.
4. Deprecate old direct‐rendering path in solver in a future release. 