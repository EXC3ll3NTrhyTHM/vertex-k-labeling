# Heuristic Algorithms for Mongolian Tent Graph k-Labeling

*Last updated: 2025-07-08*

---

## 1. Motivation

Finding the minimum *k* for which a 
k-labeling exists is NP-hard.  Exact backtracking works only for very small *n*.
We therefore rely on **heuristic search** that sacrifices provable optimality for
speed while still returning a feasible labeling in practice.

The project currently offers two heuristic modes:

| Mode | CLI value | Key idea | Speed | Typical *k* quality |
|------|-----------|----------|-------|---------------------|
| Accurate (default) | `accurate` | Many randomised greedy passes | Medium | Best |
| Fast | `fast` | Deterministic first-fit + a few random passes | Very High | Good-enough |

Both modes share the same high-level structure but differ in how many
candidate labelings they explore per *k*.

---

## 2. Common Framework

1. **Lower-bound start** – Compute the theoretical lower bound `LB(n)`
   (see `calculate_lower_bound`) and start the search at *k = LB*.
2. **Iterate over k** – For each *k* until an upper limit `LB × max_k_multiplier`:
   1. Generate one or more candidate labelings with a greedy assignment
      procedure (Section 3).
   2. Validate each candidate on the fly (`is_labeling_valid`).
   3. If a candidate succeeds (all edge weights unique) → DONE.
   4. Otherwise increment *k* and repeat.
3. **Fail-fast cap** – If no solution is found before the upper limit, return
   `(None, None)`.

The two modes differ only in *how many* greedy attempts they make per
*k* and *how* the vertex ordering & label choices are produced.

---

## 3. Greedy Labeling Core

Given a fixed *k*, we assign labels one vertex at a time:

1. **Vertex ordering** – Process vertices in a specific order.
   * Accurate mode: *randomly shuffled* order → promotes diversity.
   * Fast mode: *descending degree* order (deterministic) → minimises early
     conflicts.
2. **Label selection** – For the current vertex `v` try label values
   `1 … k` in random or ascending order (see below).
3. After placing a label, **partial validation** runs only against edges
   adjacent to `v` (much cheaper than global check).
4. If no label is valid, backtrack to the previous vertex (rare due to greedy
   nature) or abort the attempt.

### Accurate Mode Details
* **Attempts per k** – default `num_attempts = 100` (configurable).
* **Two layers of randomness**
  1. Shuffle vertex order.
  2. Shuffle the list of candidate labels for each vertex.
* **Effect** – High probability of discovering a low *k* but runtime grows
  with both *num_attempts* and *n*.

### Fast Mode Details
* **Pass 1 — First-fit deterministic**
  * Order: descending degree.
  * Labels: ascending 1 … k.
  * Extremely fast; may fail for tight *k*.
* **Pass 2 — Limited random attempts**
  * Number of passes = `max(2, min(10, ⌈n / 2⌉))`.
  * Each pass uses the same greedy algorithm as Accurate mode but only **one**
    shuffled attempt.
  * Balances extra accuracy against time: small *n* gets 2 passes, large *n*
    capped at 10.

---

## 4. Complexity Analysis

Let `E` be number of edges (≈ `9n` for MT₍₃,ₙ₎) and `A` the number of greedy
attempts per *k*.

*Greedy attempt cost* ≈ `O(E × k)` because each label trial checks ≤ degree
edges.

| Mode | Attempts `A` | Worst-case time (per k) |
|------|--------------|-------------------------|
| Accurate | 100 | 100 × O(E k) |
| Fast | ≤ 11 | 11 × O(E k) |

In practice Fast mode is an order of magnitude quicker than Accurate mode.

---

## 5. Adjustable Parameters

| Parameter | Location | Default | Purpose |
|-----------|----------|---------|---------|
| `num_attempts` | `find_feasible_k_labeling()` | 100 | Accurate mode passes per k |
| `max_k_multiplier` | same | 20 | Upper bound stop-condition |
| `algorithm` | same | "accurate" | Choose heuristic mode |

Tuning tips:
* Decrease `num_attempts` to trade quality for speed in Accurate mode.
* Increase `max_k_multiplier` if the heuristic reports failure for large *n*.

---

## 6. Strengths & Limitations

### Strengths
* Finds feasible labelings for `n ≤ 200` in seconds (Fast) or minutes
  (Accurate) on a modern laptop.
* Simple code; easy to parallelise because attempts are independent.
* Parameterised for flexible trade-offs.

### Limitations
* No optimality guarantee – may return *k* > minimum, especially in Fast mode.
* Performance still degrades when degree grows quadratically with *n*.
* Heavy reliance on random shuffling; reproducibility requires fixed RNG seed.

---

## 7. Future Work
* **Parallelism** – Implement ProcessPool (see enhancement 1-C).
* **Meta-heuristics** – Tabu search or genetic algorithm seeded by greedy
  solutions.
* **GPU / JIT** – Offload edge-weight validation to Numba or CUDA for further
  speed-ups.

---

*Prepared by AI assistant – 2025-07-08* 