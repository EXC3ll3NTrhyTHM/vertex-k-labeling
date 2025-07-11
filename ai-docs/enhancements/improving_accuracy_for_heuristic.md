# Improving Accuracy for the Heuristic k-Labeling Algorithm

*July 11, 2025*

---

## 1. Motivation for Improvement

Your current heuristic algorithm finds feasible k-labelings by using multiple randomized greedy passes. While effective, its accuracy relies heavily on chance—hoping that one of the random attempts successfully finds a valid labeling.

To improve **accuracy** and find solutions for tighter, more difficult values of *k*, we can integrate more sophisticated techniques. These methods move beyond pure randomness to guide the search intelligently, increasing the probability of finding a solution where simple greedy attempts fail.

The following steps outline three key enhancements:
1.  **Conflict-Guided Vertex Ordering:** Prioritize labeling the "hardest" vertices first.
2.  **Conflict-Minimizing Label Selection:** Choose labels that are least likely to cause future conflicts.
3.  **Limited Backjumping:** Implement a smarter, non-chronological backtracking strategy.

---

## 2. Step 1: Implement Conflict-Guided Vertex Ordering

Instead of relying on random shuffling or a static descending-degree order, this technique dynamically re-orders vertices based on how difficult they are to label. This is a powerful enhancement over the existing `Accurate` mode's random shuffling.

-   [ ] **Track Labeling Failures:**
    -   Create a data structure, such as a dictionary or a hash map called `failure_counts`, to store the number of times a labeling attempt has failed for each vertex.
    -   When a greedy pass fails because no valid label can be found for a vertex `v`, increment `failure_counts[v]`.

-   [ ] **Modify the Vertex Ordering Strategy:**
    -   Before starting a new greedy attempt (i.e., for each of the `num_attempts` in your `Accurate` mode), sort the vertices to be labeled.
    -   The primary sorting key should be the `failure_counts` in descending order. Vertices that have caused failures most often will be chosen first.
    -   The secondary sorting key should be the vertex degree, also in descending order. This acts as a tie-breaker, falling back to your `Fast` mode's logic.
    -   This ensures your algorithm focuses its effort on resolving the most contentious parts of the graph first.

---

## 3. Step 2: Adopt Conflict-Minimizing Label Selection

The current algorithm selects labels randomly or in ascending order. A more intelligent approach is to evaluate each potential label based on how many future options it eliminates. This is known as the **Minimum-Remaining-Values (MRV)** or **Least-Constraining-Value (LCV)** heuristic.

-   [ ] **Calculate Label "Cost":**
    -   When selecting a label for the current vertex `v`, don't just pick the first valid one. Instead, iterate through all possible labels from `1...k`.
    -   For each valid candidate label `L`, calculate a "conflict score." This score is the number of currently *unassigned* neighboring vertices whose pool of available labels would be reduced if `v` were assigned label `L`.
    -   A simple way to do this: For each unassigned neighbor `u`, check how many of its potential labels `1...k` would create a conflicting edge weight with the new edge `(v,u)`. Sum these counts to get the total conflict score for label `L`.

-   [ ] **Choose the Best Label:**
    -   Select the label with the **lowest** conflict score. This is the "least constraining value" because it preserves the maximum number of options for neighboring vertices.
    -   If there's a tie, you can use a random choice or the lowest numerical label as a tie-breaker.

-   [ ] **Integrate into the Greedy Core:**
    -   Replace the random or ascending label selection logic in your `Greedy Labeling Core` with this conflict-minimizing approach. This change will significantly reduce the chances of running into a dead end.

---

## 4. Step 3: Introduce Limited Backjumping (Advanced)

Standard backtracking goes back one step when it gets stuck. **Conflict-Directed Backjumping** is a smarter technique where the algorithm jumps back directly to the vertex that caused the conflict, which may be several steps back. This avoids wasting time exploring irrelevant parts of the search tree.

-   [ ] **Track Conflict Sources:**
    -   When trying to label a vertex `v`, maintain a "conflict set" for it. This set contains the previously labeled vertices `u` that prevent any label from being assigned to `v`.
    -   For example, if you cannot label `v` because all potential labels create weight conflicts with edges `(v, u1)` and `(v, u2)`, then the conflict set for `v` is `{u1, u2}`.

-   [ ] **Implement the "Jump":**
    -   If no label can be assigned to `v`, don't just backtrack to the immediately preceding vertex in the ordering.
    -   Instead, identify the most recently labeled vertex in `v`'s conflict set. Let this be `u_conflict`.
    -   Jump directly back to `u_conflict`, erasing the label assignments for all vertices that came after `u_conflict` in the ordering. The search then continues by trying a different label for `u_conflict`.

-   [ ] **Control the Scope (Limitation):**
    -   Full backjumping can be complex. A simpler, "limited" version can still provide significant benefits.
    -   **Suggestion:** Only allow a small number of backjumps (e.g., 1-3) per greedy pass. If it fails after that, terminate the attempt and start a new randomized pass, updating the failure counts as in Step 1. This prevents getting stuck in a complex series of jumps while still allowing the algorithm to escape simple dead ends.