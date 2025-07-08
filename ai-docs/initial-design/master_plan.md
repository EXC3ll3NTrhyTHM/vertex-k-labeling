# Vertex k-labeling Master Plan for Mongolian Tent Graphs

## **Objective**

Implement an algorithm to compute the **edge irregularity strength (es(G))** for Mongolian Tent Graph \( MT_{3,n} \) using vertex k-labeling such that:

✅ All edge weights are unique  
✅ Minimum k is determined

---

## **Overall Inputs**

- Positive integer n (3 ≤ n ≤ 50)

## **Overall Outputs**

- Minimum k (edge irregularity strength es(G))  
- Valid vertex labeling (φ) for MT_{3,n} satisfying problem constraints

---

## **Definitions**

### **Edge Weight Computation Formula**

For any edge xy in G:

\[
w_\phi(xy) = \phi(x) + \phi(y)
\]

where:

- φ(x) is the label assigned to vertex x  
- All edge weights must be **distinct**

---

### **Graph Definitions for Implementation**

#### **Ladder Graph \( L_n \)**

- **Vertices**:  
  - {(1, i), (2, i), (3, i)} for i = 1 to n  
  - (1, i) = top row vertex in column i  
  - (2, i) = *middle* row vertex in column i  
  - (3, i) = bottom row vertex in column i

- **Edges**:  
  - Horizontal top row: ((1, i), (1, i+1)) for i = 1 to n-1  
  - Horizontal middle row: ((2, i), (2, i+1)) for i = 1 to n-1  
  - Horizontal bottom row: ((3, i), (3, i+1)) for i = 1 to n-1  
  - Vertical rungs:  
    - ((1, i), (2, i)) for i = 1 to n  
    - ((2, i), (3, i)) for i = 1 to n

---

#### **Mongolian Tent Graph \( MT_{3,n} \)**

- Construct from ladder graph \( L_n \)
- Add apex vertex **x**
- Connect apex vertex x to **every top row vertex (1, i)** for i = 1 to n

---

### **Theoretical Lower Bound**

\[
es(G) \ge \max \left\{ \frac{|E(G)| + 1}{2}, \Delta(G) \right\}
\]

where:

- |E(G)| is the total number of edges  
- Δ(G) is the maximum vertex degree in G

---

## **Worked Example: MT_{3,3}**

### **Graph Construction**

- **Vertices**:  
  - Top row: (1,1), (1,2), (1,3)  
  - Middle row: (2,1), (2,2), (2,3)
  - Bottom row: (3,1), (3,2), (3,3)  
  - Apex: x

- **Edges**:  
  - Horizontal top: (1,1)-(1,2), (1,2)-(1,3)  
  - Horizontal middle: (2,1)-(2,2), (2,2)-(2,3)  
  - Horizontal bottom: (3,1)-(3,2), (3,2)-(3,3)  
  - Vertical rungs (top→middle): (1,1)-(2,1), (1,2)-(2,2), (1,3)-(2,3)  
  - Vertical rungs (middle→bottom): (2,1)-(3,1), (2,2)-(3,2), (2,3)-(3,3)  
  - Apex connections: x-(1,1), x-(1,2), x-(1,3)

- **Total edges |E(G)|** = 15  
- **Maximum degree Δ(G)** = 4

### **Lower bound calculation**

\[
\frac{|E(G)| + 1}{2} = \frac{15 + 1}{2} = 8
\]

\[
\Delta(G) = 4
\]

Hence, **lower bound k ≥ max{8,4} = 8**.

---

### **Sample Valid Labeling for k=5**

*(Note: This is illustrative; actual implementation should verify uniqueness)*

- φ(x) = 5  
- φ(1,1) = 1  
- φ(1,2) = 2  
- φ(1,3) = 3  
- φ(2,1) = 2  
- φ(2,2) = 3  
- φ(2,3) = 4

**Sample edge weights:**

- x-(1,1): 5+1=6  
- x-(1,2): 5+2=7  
- x-(1,3): 5+3=8  
- (1,1)-(1,2): 1+2=3  
- (1,2)-(1,3): 2+3=5  
- (2,1)-(2,2): 2+3=5  
- (2,2)-(2,3): 3+4=7  
- (1,1)-(2,1): 1+2=3  
- (1,2)-(2,2): 2+3=5  
- (1,3)-(2,3): 3+4=7

⚠ **Note**: Duplicate weights observed → this sample fails. Your algorithm must find an assignment with **no duplicate edge weights** and k minimized. This demonstrates why backtracking validation is required.

---

## **TASKS**

### **Task 1. Graph Construction**

**Description**: Generate the graph structure required for labeling.

- **Inputs**: n
- **Outputs**:
  - Ladder graph \( L_n \)
  - Mongolian Tent graph \( MT_{3,n} \) with apex vertex connected to top-row vertices

**Subtasks**:

1.1 Implement function to generate ladder graph \( L_n \)  
1.2 Extend ladder to build Mongolian Tent graph \( MT_{3,n} \)

---

### **Task 2. Calculate Theoretical Lower Bound**

**Description**: Compute the lower bound for k based on graph properties.

- **Inputs**: MT_{3,n}
- **Outputs**:
  - Number of edges |E(G)|
  - Maximum degree Δ(G)
  - Theoretical lower bound k

**Subtasks**:

2.1 Calculate |E(G)|  
2.2 Calculate Δ(G)  
2.3 Determine lower bound for k

---

### **Task 3. Labeling Algorithm Implementation**

**Description**: Find valid labeling using backtracking to satisfy edge weight uniqueness and minimize k.

- **Inputs**: MT_{3,n}, lower bound k
- **Outputs**:
  - Minimum k
  - Valid labeling array φ

**Subtasks**:

3.1 Design backtracking algorithm:

- Start with k = lower bound
- For each vertex:
  - Assign label from {1,...,k}
  - Calculate all current edge weights
  - Check for duplicate edge weights
  - Backtrack on conflict

3.2 If valid labeling found:
- Record current k
- Attempt with k-1 to minimize further

---

### **Task 4. Optimization & Heuristics**

**Description**: Implement performance improvements.

- **Inputs**: Labeling algorithm
- **Outputs**: Faster execution time, reduced search space

**Subtasks**:

4.1 Prioritize labeling high-degree vertices first  
4.2 Implement pruning on duplicate detection  
4.3 Implement greedy heuristic to find initial feasible upper bound k

---

### **Task 5. Testing & Verification**

**Description**: Validate implementation correctness.

- **Inputs**: Algorithm implementation
- **Outputs**:
  - Test results for MT_{3,3}
  - Verification of unique edge weights
  - Confirmation of minimized k

---

### **Task 6. Documentation & Reporting**

**Description**: Generate final deliverables.

- **Inputs**: Completed implementation and test results
- **Outputs**:
  - Problem summary
  - Algorithm design explanation
  - Code documentation
  - Test results and screenshots
  - Final report or notebook

---

# **End of Master Plan**
