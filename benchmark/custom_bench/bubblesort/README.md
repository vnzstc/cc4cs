## BubbleSort Sorting Algorithm: brief description of the implementation.

 Starting from the beginning of the list, compare every adjacent pair, 
 swap their position if they are not in the right order (the latter one is smaller than the former one). 
 After each iteration, one less element (the last one) is needed to be compared 
 until there are no more elements left to be compared.
 
 We have 2 main procedures: bubble_sort(), swap().
 
 <b>Swap:</b> Simply exchanges position of two elements in the array.<br>
 <b>Bubble_Sort:</b> Iterates through the array, n*n times,  and call swap function when a[i]>a[i+1]
 
### Test and Implementation Details:
void prototype(int dim, int a[dim]);<br>

*******************
TARGET_INDEX:<b>int8_t</b>
TARGET_TYPE:<b>int8_t</b>

- 2 + size}array_a 
- size <= 116 ----> 2 + 116 -----> TOT: 118

<b> int8_t size:</b> [1, 116]; 100 <br>
<b> int8_t a[size]:</b> [-128, 127] 

*******************
TARGET_INDEX:<b>int8_t</b>
TARGET_TYPE:<b>int</b>

- 10 + (size * 2)}array_a 
- size <= 54 ----> 10 + 108 -----> TOT: 118

<b> int size:</b> [1, 54]; 100 <br>
<b> int a[size]:</b> [-32768, 32767]

*******************
TARGET_INDEX:<b>int8_t</b>
TARGET_TYPE:<b>long</b>

- 26 + (size * 4)}array_a 
- size <= 23 ----> 26 + 92 -----> TOT: 118

<b> long size:</b> [1, 23]; 100 <br>
<b> long a[size]:</b> [-2147483648,2147483647]

*******************
TARGET_INDEX:<b>int8_t</b>
TARGET_TYPE:<b>float</b>

- 21 + (size * 4)}array_a 
- size <= 24 ----> 21 + 96 -----> TOT: 117

<b> int8_t size:</b> [1, 23]; 100 <br>
<b> float a[size]:</b> [-2147483648.0,2147483647.0]
