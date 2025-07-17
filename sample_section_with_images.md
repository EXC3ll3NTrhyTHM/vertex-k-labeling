# Sample Report Section with Images

## 2. Background & Literature Review

### 2.1. Graph Theory Fundamentals

A graph $G = (V, E)$ consists of a finite set of vertices $V$ and a set of edges $E \subseteq V \times V$. In this study, we consider undirected graphs where edges are unordered pairs of vertices. The degree of a vertex $v$, denoted $\deg(v)$, is the number of edges incident to $v$. The maximum degree of a graph is $\Delta(G) = \max_{v \in V} \deg(v)$.

Graphs are represented using adjacency lists, where each vertex maintains a list of its neighboring vertices. This representation is memory-efficient for sparse graphs and provides $O(\deg(v))$ access time for vertex neighbors, making it well-suited for the graph classes studied in this work.

### 2.2. Vertex k-Labeling

The vertex k-labeling problem, also known as the edge irregularity strength problem, seeks to assign labels from $\{1, 2, \ldots, k\}$ to vertices such that all edge weights are distinct. The edge weight of an edge $\{u, v\}$ is defined as $w(u, v) = f(u) + f(v)$ where $f$ is the labeling function.

This problem has applications in network design where unique edge identifiers are required, and in coding theory for constructing error-correcting codes. The minimum $k$ for which a valid labeling exists is the edge irregularity strength $es(G)$, which provides a measure of the graph's structural complexity.

### 2.3. Graph Classes

#### 2.3.1. Circulant Graphs

A circulant graph $C_n(S)$ is defined on $n$ vertices $\{0, 1, \ldots, n-1\}$ where vertex $i$ is adjacent to vertex $(i + s) \bmod n$ for each $s \in S$. The set $S$ is called the generator set and determines the graph's structure.

**Example**: $C_6(\{1, 2\})$ has vertices $\{0, 1, 2, 3, 4, 5\}$ where vertex 0 connects to vertices 1, 2, 4, and 5.

Circulant graphs exhibit high symmetry and regularity properties, making them important in algebraic graph theory and network topology design.

![Example of a Circulant graph structure showing the regular connectivity pattern](graphs\circulant_6_2.png)

*Figure: Example of a Circulant graph structure showing the regular connectivity pattern*

#### 2.3.2. Mongolian Tent Graphs

A Mongolian Tent graph $MT(3,n)$ consists of three horizontal paths of length $n$ connected by vertical edges, with an additional apex vertex connected to all vertices in the top row. The structure resembles a tent with three levels and $n$ columns.

**Example**: $MT(3,2)$ has 7 vertices: apex vertex $x$, top row $(1,1), (1,2)$, middle row $(2,1), (2,2)$, and bottom row $(3,1), (3,2)$.

These graphs combine path-like and star-like structural elements, providing an interesting test case for labeling algorithms.

![Example of a Mongolian Tent graph structure showing the three-level tent configuration](graphs\mt3_3.png)

*Figure: Example of a Mongolian Tent graph structure showing the three-level tent configuration*

### 2.4. Algorithmic Strategies

#### 2.4.1. Backtracking

Backtracking is an exhaustive search algorithm that builds solutions incrementally and abandons partial solutions (backtracks) as soon as it determines they cannot lead to a valid complete solution. The algorithm maintains the invariant that all partial assignments satisfy the problem constraints, using constraint propagation to prune the search space early.

For the k-labeling problem, backtracking assigns labels to vertices one by one, checking edge weight uniqueness at each step and backtracking when conflicts arise.

#### 2.4.2. Heuristics

Heuristic algorithms are strategies designed to find good approximate solutions to computationally hard problems in reasonable time, often by making locally optimal choices at each step. While heuristics do not guarantee optimal solutions, they can provide practical solutions for larger problem instances where exact algorithms become intractable.

The greedy heuristic approach for k-labeling prioritizes vertices by degree and uses randomized multi-attempt search to improve solution quality while maintaining polynomial time complexity.

## 7. Appendix

### 7.1. Algorithm Visualization Gallery

This section presents a comprehensive collection of algorithm execution results and graph visualizations generated during the experimental evaluation.

#### 7.1.1. Backtracking Algorithm Results

The following images demonstrate the backtracking algorithm's performance on various graph instances, showing both successful solutions and the systematic search process.

#### Backtracking Algorithm Solutions

![Mongolian Tent MT(3,10) solved with backtracking algorithm](graphs\mt3_10_backtracking.png)

*Figure: Mongolian Tent MT(3,10) solved with backtracking algorithm*

![Mongolian Tent MT(3,14) solved with backtracking algorithm](graphs\mt3_14_backtracking.png)

*Figure: Mongolian Tent MT(3,14) solved with backtracking algorithm*

![Mongolian Tent MT(3,3) solved with backtracking algorithm](graphs\mt3_3_backtracking.png)

*Figure: Mongolian Tent MT(3,3) solved with backtracking algorithm*

![Mongolian Tent MT(3,4) solved with backtracking algorithm](graphs\mt3_4_backtracking.png)

*Figure: Mongolian Tent MT(3,4) solved with backtracking algorithm*


#### 7.1.2. Heuristic Algorithm Results

These visualizations showcase the heuristic algorithm's performance across different modes (accurate, intelligent, fast) and demonstrate the trade-offs between solution quality and computational efficiency.

#### Heuristic Algorithm Solutions

![Mongolian Tent MT(3,100) solved with fast heuristic algorithm](graphs\mt3_100_heuristic_fast.png)

*Figure: Mongolian Tent MT(3,100) solved with fast heuristic algorithm*

![Mongolian Tent MT(3,10) solved with accurate heuristic algorithm](graphs\mt3_10_heuristic_accurate.png)

*Figure: Mongolian Tent MT(3,10) solved with accurate heuristic algorithm*

![Mongolian Tent MT(3,10) solved with fast heuristic algorithm](graphs\mt3_10_heuristic_fast.png)

*Figure: Mongolian Tent MT(3,10) solved with fast heuristic algorithm*

![Mongolian Tent MT(3,10) solved with intelligent heuristic algorit