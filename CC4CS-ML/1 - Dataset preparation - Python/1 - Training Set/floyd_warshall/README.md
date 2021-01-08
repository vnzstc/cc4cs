## Floyd-Warshall's algorithm - brief description of the implementation 

Floyd-Warshall's algorithm is an algorithm for finding shortest paths in a weighted graph with positive
or negative edge weights (but with no negative cycles).
The graph is rappresented with an adjacency matrix. 
At each iteration it compares every path between a pair of nodes and checks for a minimum cost path. The minimum cost is stored in
the matrix that rapresent the graph.
At the end of execution, the output is the adjacency matrix that contains minimum cost paths between every pair of nodes.

### Test and Implementation Details:


*******************
TARGET_INDEX:<b>uint8_t</b>
TARGET_TYPE:<b>uint8_t</b>

- 2 + (size * size)}array_a
- size <= 10 ---> 2 + (100) + 2 ---> TOT: 104

<b>uint8_t size:</b> [1, 10];100 <br>
<b>uint8_t a[size][size]:</b> [0, 255]


*******************
TARGET_INDEX:<b>uint8_t</b>
TARGET_TYPE:<b>uint16_t</b>

- 8 + (size * size * 2)}array_a
- size <= 7 ---> 8 + (98) ---> TOT: 106

<b>int size:</b> [1, 7];100 <br>
<b>int a[size][size]:</b> [0, 65535]

*******************
TARGET_INDEX:<b>uint8_t</b>
TARGET_TYPE:<b>uint32_t</b>

- 8 + (size * size * 4)}array_a
- size <= 5 ---> 8 + (100) ---> TOT: 118

<b>uint8_t size:</b> [1, 5];100 <br>
<b>uint32_t a[size][size]:</b> [0, 4294967295]

*******************
TARGET_INDEX:<b>uint8_t</b>
TARGET_TYPE:<b>float</b>

- 8 + (size * size * 4)}array_a
- size <= 5 ---> 8 + (100) ---> TOT: 118

<b>uint8_t size:</b> [1, 5];100 <br>
<b>float a[size][size]:</b> [0.0, 4294967295.0]