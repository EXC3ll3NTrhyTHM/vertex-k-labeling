# Accurate Heuristic k-Labeling Algorithm

*July 15, 2025*

---

## 1. Overview

The accurate heuristic k-labeling algorithm is a sophisticated method for finding a valid k-labeling for a graph. It improves upon simpler greedy approaches by incorporating intelligent search strategies to increase the probability of finding a solution, especially for difficult graphs or tight k-values.

The algorithm combines three key techniques:

1.  **Conflict-Guided Vertex Ordering:** Prioritizes labeling the most difficult vertices first.
2.  **Conflict-Minimizing Label Selection:** Chooses labels that are least likely to cause future conflicts.
3.  **Limited Backjumping:** Implements a non-chronological backtracking strategy to escape dead ends efficiently.

---

## 2. Algorithm Steps

The algorithm proceeds in a series of attempts. For each attempt, it performs the following steps:

### Step 1: Vertex Ordering

Instead of a random or static ordering, the vertices are sorted dynamically based on their labeling history. The primary sorting key is the **failure count** of each vertex, in descending order. The failure count is the number of times the algorithm has failed to find a valid label for that vertex in previous attempts. The secondary sorting key is the vertex degree, also in descending order, which acts as a tie-breaker.

This ordering ensures that the algorithm focuses on the most contentious parts of the graph first.

### Step 2: Iterative Labeling

The algorithm iterates through the sorted vertices, assigning a label to each one. For each vertex, it performs the following:

#### a. Label Selection

Instead of choosing a random or the first available label, the algorithm selects the label that is least likely to cause conflicts with future label assignments. This is done by calculating a **conflict score** for each possible label from 1 to k.

The conflict score for a label is the number of available labels for unassigned neighboring vertices that would be eliminated if that label were assigned to the current vertex. The algorithm chooses the label with the lowest conflict score.

#### b. Assignment and Conflict Resolution

If a valid label with a finite conflict score is found, it is assigned to the current vertex, and the algorithm proceeds to the next vertex.

If no valid label can be found for the current vertex, the algorithm performs a **limited backjump**. It identifies the most recently labeled vertex in the current vertex's conflict set and jumps back to it, undoing all label assignments made in between. The algorithm then tries a different label for the jumped-to vertex.

A limit is placed on the number of backjumps allowed in a single attempt to prevent infinite loops.

### Step 3: Verification and Termination

If the algorithm successfully assigns a label to every vertex in the graph, it verifies that the resulting labeling is valid (i.e., all edge weights are unique). If the labeling is valid, the algorithm terminates and returns the solution.

If the algorithm fails to find a valid labeling after a predetermined number of attempts, it terminates and reports failure.
