# Task: Calculate the Lower Bound for Edge Irregularity Strength

Your task is to implement a function that calculates the theoretical lower bound for the edge irregularity strength ($es$) of a circulant graph ($C_{n,r}$). The calculation must be based on the formula provided in the research paper "Irregularity Strength of Circulant Graphs Using Algorithmic Approach."

---

## Formula

[cite_start]The formula for the theoretical lower bound is given in Theorem 3 of the paper[cite: 155].

$$ \max\left\{\left\lceil\frac{nr+2}{4}\right\rceil, r\right\} $$

### Variable Definitions

* **n**: An integer representing the number of vertices in the graph (the order).
* **r**: An integer representing the degree of the graph (it is an *r*-regular graph).

---

## Example Calculation

Let's test the formula with an example from the paper's data. [cite_start]For a circulant graph with **n = 12** and **r = 7** (this corresponds to the r = n-5 case in Table 2)[cite: 171].

1.  **Substitute variables**:
    `max{⌈(12 * 7 + 2) / 4⌉, 7}`

2.  **Calculate the fraction**:
    `max{⌈(84 + 2) / 4⌉, 7}` = `max{⌈86 / 4⌉, 7}` = `max{⌈21.5⌉, 7}`

3.  **Apply the ceiling function**:
    `max{22, 7}`

4.  **Find the maximum value**:
    `22`

The theoretical lower bound for $C_{12,7}$ is **22**.

---

## Your Task

Create a function `calculate_circulant_lower_bound(n, r)` that performs this calculation.

### **Inputs:**

* `n` (integer): The order of the circulant graph.
* `r` (integer): The degree of the circulant graph.

### **Output:**

* An integer representing the calculated lower bound.

### **Implementation Steps:**

1.  Calculate the value of the expression `(n * r + 2) / 4`.
2.  Use a math library to apply the ceiling function to the result from step 1.
3.  Compare the result from step 2 with the value of `r`.
4.  Return the greater of the two values.