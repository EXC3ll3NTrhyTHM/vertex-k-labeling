# Enhancement: Parallel Heuristic Search & Performance Profiling

## Context
The project now contains two heuristic modes (accurate & fast) and an exact back-tracking solver.  As *n* grows, runtime becomes the key bottleneck.  Two complementary improvements can unlock substantial speed-ups and lay the groundwork for future research:

1. **Parallelism (Road-map item 1-C)** – run multiple independent heuristic passes concurrently, exploiting all CPU cores.
2. **Profiling & Hot-loop Optimisation (Road-map item 2-A)** – measure where the time goes, then accelerate the verified hotspots (Python-level refactor, JIT, or C/Cython).

---

## 1-C  Parallel Heuristic Search

### Problem it solves
* The current heuristic explores candidate labelings sequentially.  On modern multi-core machines this under-utilises available CPU resources.
* Randomised passes are **embarrassingly parallel**: each attempt is independent and terminates as soon as any attempt finds a feasible labeling.

### High-level approach
1. **Executor selection**  
   Use Python’s `concurrent.futures.ProcessPoolExecutor` (preferred—true parallelism) with a fall-back to `ThreadPoolExecutor` when `fork` is unavailable (e.g., Windows without `spawn` overhead concerns).
2. **Task definition**  
   Wrap `greedy_k_labeling` (accurate) and `_first_fit_greedy_k_labeling` (fast) into a function that tries one candidate `k` and returns `(k, labeling | None)`.
3. **Dynamic termination**  
   • Submit *N* tasks (N ≈ `os.cpu_count()`) per `k`.  
   • Use `as_completed` / `wait FIRST_COMPLETED` to cancel the rest as soon as a solution is returned.
4. **Adaptive scheduling**  
   If no task succeeds, increment `k` and resubmit; otherwise return the first winner.
5. **Command-line toggle**  
   Extend `main.py` with `--parallel` flag (default `auto`) to enable or disable.

### Expected benefits
* ≈ linear speed-up with core count for randomised heuristics (accurate mode).  
  E.g., 8-core laptop ⇒ ~8× fewer wall-clock seconds per *k*.
* Clean separation of concerns—no change to heuristics’ logic, only orchestration layer.

---

## 2-A  Profiling & Hot-loop Optimisation

### Problem it solves
* We suspect the inner edge-weight validation dominates runtime, but lack hard data.
* Blind optimisation risks effort without gain; profiling pin-points hotspots and guides targeted improvements.

### High-level approach
1. **Instrumentation**  
   • Add a `scripts/profile.py` helper with `cProfile` / `profile` module wrappers.  
   • Save `.prof` files; view with `snakeviz` or `pyinstrument` for flame graphs.
2. **Benchmark scenarios**  
   Profile both heuristic modes for representative sizes: n = 5, 20, 50.
3. **Analysis**  
   Identify top-5 cumulative time functions (likely `is_labeling_valid`, adjacency traversals, random shuffles).
4. **Optimisation candidates**  
   • **Algorithmic** – memoise computed edge-weights per partial labeling.  
   • **Data-structure** – replace Python `set` with `bitarray` or `numpy` boolean mask.  
   • **Low-level** – prototype `numba` JIT compile of validation, or port it to Cython for ~15× speed-up.
5. **Regression guard**  
   Extend `tests/test_performance.py` with new baselines and fail when runtime regresses > 20 %.

### Expected benefits
* Quantitative visibility into runtime.  
* After first round of optimisations, expect 3–10× speed-up for core validation loop.
* Profiling artifacts become living documentation for future contributors.

---

## Deliverables
1. `src/parallel_executor.py` – utility launching parallel heuristic attempts.
2. CLI flag `--parallel {auto,on,off}` integrated into `main.py`.
3. `scripts/profile.py` – one-command profiler; README snippet.
4. Updated unit tests and performance benchmarks.
5. Design doc (this file) kept up-to-date.

---

## Timeline (suggested)
| Week | Goal |
|------|------|
| 1 | Prototype parallel executor, baseline profile results |
| 2 | Integrate CLI flag, write initial unit tests |
| 3 | Analyse profiles, implement first optimisation (e.g., numba) |
| 4 | Harden cancellation logic, document metrics, update README |


---

*Prepared by : AI assistant – 2025-07-08* 