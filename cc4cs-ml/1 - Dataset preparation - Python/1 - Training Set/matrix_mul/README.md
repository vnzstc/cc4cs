### Test and Implementation Details:

void prototype(int row_num_a, int column_num_a, int a[row_num_a][column_num_a],int row_num_b, int column_num_b, int b[row_num_b][column_num_b])

*******************
TARGET_INDEX:<b>int8_t</b>
TARGET_TYPE:<b>int8_t</b>


- 4 + (rowA * colA) + (rowB * colB) + (rowA * colB ) + (2 Overlay)
- rowA, colA, rowB, colB <= 6;

In worst case we have rowA = 6, colA = 6, rowB = 6, colB = 6 ---> 4 + (36) + (36) + (36) + 2 ---> TOT: 114

<b>int8_t row_num_a:</b>	[1,6];3<br>
<b>int8_t column_num_a:</b> [1,6];3<br>
<b>int8_t a[row_num_a][column_num_a]:</b> [-127,128]<br>
<b>int8_t row_num_b:</b> [1,6];3<br>
<b>int8_t column_num_b:</b> [1,6];3<br>
<b>int8_t b[row_num_b][column_num_b]:</b> [-127,128]<br>

*******************
TARGET_INDEX:<b>int8_t</b>
TARGET_TYPE:<b>int</b>

- 11 + (rowA * colA * 2) + (rowB * colB * 2 ) + (rowA * colB * 2 ) + (2 Overlay)
- rowA, colA, rowB, colB <= 4;

In worst case we have rowA = 4, colA = 4, rowB = 4, colB = 4 ---> 13 + (32) + (32) + (32) ---> TOT: 109

<b>int row_num_a:</b>	 [1,4];3<br>
<b>int column_num_a:</b> [1,4];3<br>
<b>int a[row_num_a][column_num_a]:</b> [-32768,32767]<br>
<b>int row_num_b:</b> [1,4];3<br>
<b>int column_num_b:</b> [1,4];3<br>
<b>int b[row_num_b][column_num_b]:</b> [-32768,32767]<br>

*******************
TARGET_INDEX:<b>int8_t</b>
TARGET_TYPE:<b>long</b>

- 17 + (rowA * colA * 4) + (rowB * colB * 4) + (rowA * colB * 4) + (4 Overlay)
- rowA, colA, rowB, colB <= 2;

In worst case we have rowA = 2, colA = 2, rowB = 2, colB = 2 ---> 21 + (16) + (16) + (16) ---> TOT: 69

<b>long row_num_a:</b>	 [1,2];3<br>
<b>long column_num_a:</b> [1,2];3<br>
<b>long a[row_num_a][column_num_a]:</b>[-2147483648, 2147483647] <br>
<b>long row_num_b:</b> [1,2];3<br>
<b>long column_num_b:</b> [1,2];3<br>
<b>long b[row_num_b][column_num_b]:</b>[-2147483648, 2147483647] <br>

*******************
TARGET_INDEX:<b>int8_t</b>
TARGET_TYPE:<b>float</b>

- 22 + (rowA * colA * 4) + (rowB * colB * 4) + (rowA * colB * 4) + (1 Overlay)
- rowA, colA, rowB, colB <= 2;

In worst case we have rowA = 2, colA = 2, rowB = 2, colB = 2 ---> 23 + (16) + (16) + (16) ---> TOT: 72

<b>int8_t row_num_a:</b>    [1,2];3<br>
<b>int8_t column_num_a:</b> [1,2];3<br>
<b>float a[row_num_a][column_num_a]:</b>[-2147483648.5, 2147483647.5]<br>
<b>int8_t row_num_b:</b> [1,2];3<br>
<b>int8_t column_num_b:</b> [1,2];3<br>
<b>float b[row_num_b][column_num_b]:</b>[-2147483648.5, 2147483647.5]<br>