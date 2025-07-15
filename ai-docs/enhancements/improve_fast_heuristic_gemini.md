# Improving Accuracy for the Fast Heuristic Algorithm

*July 11, 2025*

---

## 1. Motivation for Improvement

The current "Fast Heuristic" algorithm is designed for speed, using a deterministic pass followed by a few random attempts. While fast, its accuracy is limited because the deterministic part is rigid, and the random passes are shallow.

We can significantly improve its ability to find tighter `k` values by injecting more intelligence into both phases. The goal is to make "smarter" choices without resorting to the high number of attempts used by the "Accurate" mode. These enhancements focus on learning from conflicts and making more informed local decisions.

---

## 2. Step 1: Enhance the Deterministic First-Fit Pass

The current deterministic pass sorts vertices by descending degree. We can improve this by adding a more sophisticated tie-breaking rule and a better label selection strategy.

-   [ ] **Implement Tie-Breaking with Neighbor Degrees:**
    -   When sorting vertices, the primary key remains the vertex degree (descending).
    -   Add a secondary sorting key: the **sum of the degrees of each vertex's neighbors**.
    -   When two vertices have the same degree, this tie-breaker will prioritize the one connected to a more constrained neighborhood. This often resolves critical conflicts earlier.

-   [ ] **Adopt Least-Constraining Label Selection:**
    -   Instead of choosing the smallest available label (1, 2, 3...), select the label that is least likely to cause future conflicts.
    -   **How-to:** For the current vertex, iterate through all valid candidate labels. For each label, calculate a "conflict score" representing how many labeling options it would eliminate for its *unassigned neighbors*. Choose the label with the **lowest** score.
    -   This simple change makes the greedy choice much more robust and forward-thinking.

---

## 3. Step 2: Make Randomized Passes More Strategic

The current randomized passes use a fully shuffled vertex order and label selection. We can get better results with a semi-random, "guided" approach that learns from the initial deterministic failure.

-   [ ] **Identify and Prioritize Conflict Vertices:**
    -   During the initial deterministic pass, if it fails, **record the vertex (`v_fail`) where no valid label could be found**. This vertex is the immediate source of the failure.
    -   In the subsequent randomized passes, modify the vertex ordering. Instead of a full shuffle, create a priority group.
    -   Place `v_fail` and its immediate neighbors at the **front** of the labeling order. The rest of the vertices can be shuffled randomly behind them.
    -   This "guided" approach focuses the limited random attempts on resolving the specific bottleneck that caused the first pass to fail.

-   [ ] **Use a "Perturbation" Strategy:**
    -   Instead of a fully random shuffle, start with the successful descending-degree order from the deterministic pass.
    -   Slightly "perturb" this order by swapping a small number of random pairs of vertices.
    -   This maintains the generally good structure of the degree-based ordering while introducing just enough variation to escape local minima where the purely deterministic approach gets stuck.

---

## 4. Step 3: Implement a Lightweight Restart Mechanism

If both the deterministic and limited random passes fail for a given `k`, the current algorithm simply increments `k`. A better approach is to use information from the failure to make the next try for `k` more effective.

-   [ ] **Introduce a Failure-Tracking System:**
    -   Create a simple, persistent data structure (e.g., a dictionary or hash map) to count how many times each vertex has been the `v_fail` (the vertex that couldn't be labeled).
    -   This count should **not** reset between attempts for the same `k`.

-   [ ] **Use Failure Counts to Guide the Next Attempt:**
    -   If the first set of passes for `k` fails, before incrementing to `k+1`, perform one final "expert" pass for `k`.
    -   In this pass, order the vertices primarily by their **failure count** in descending order.
    -   This ensures that the most historically problematic vertices across all attempts are dealt with first, giving the algorithm a highly targeted "last chance" to find a solution at the current `k`.