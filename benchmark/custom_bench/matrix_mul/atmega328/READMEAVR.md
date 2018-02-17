### Test and Implementation Details:

void prototype(int row_num_a, int column_num_a, int a[row_num_a][column_num_a],int row_num_b, int column_num_b, int b[row_num_b][column_num_b])

*******************
TARGET_INDEX:<b>int8_t</b>
TARGET_TYPE:<b>int8_t</b>

<b>int8_t row_num_a:</b>	[1,6];3<br>
<b>int8_t column_num_a:</b> [1,6];3<br>
<b>int8_t a[row_num_a][column_num_a]:</b> [-127,128]<br>
<b>int8_t row_num_b:</b> [1,6];3<br>
<b>int8_t column_num_b:</b> [1,6];3<br>
<b>int8_t b[row_num_b][column_num_b]:</b> [-127,128]<br>

*******************
TARGET_INDEX:<b>int8_t</b>
TARGET_TYPE:<b>int</b>

<b>int row_num_a:</b>	 [1,4];3<br>
<b>int column_num_a:</b> [1,4];3<br>
<b>int a[row_num_a][column_num_a]:</b> [-32768,32767]<br>
<b>int row_num_b:</b> [1,4];3<br>
<b>int column_num_b:</b> [1,4];3<br>
<b>int b[row_num_b][column_num_b]:</b> [-32768,32767]<br>

*******************
TARGET_INDEX:<b>int8_t</b>
TARGET_TYPE:<b>long</b>

<b>long row_num_a:</b>	 [1,2];3<br>
<b>long column_num_a:</b> [1,2];3<br>
<b>long a[row_num_a][column_num_a]:</b>[-2147483648, 2147483647] <br>
<b>long row_num_b:</b> [1,2];3<br>
<b>long column_num_b:</b> [1,2];3<br>
<b>long b[row_num_b][column_num_b]:</b>[-2147483648, 2147483647] <br>

*******************
TARGET_INDEX:<b>int8_t</b>
TARGET_TYPE:<b>float</b>

<b>int8_t row_num_a:</b>    [1,2];3<br>
<b>int8_t column_num_a:</b> [1,2];3<br>
<b>float a[row_num_a][column_num_a]:</b>[-2147483648.5, 2147483647.5]<br>
<b>int8_t row_num_b:</b> [1,2];3<br>
<b>int8_t column_num_b:</b> [1,2];3<br>
<b>float b[row_num_b][column_num_b]:</b>[-2147483648.5, 2147483647.5]<br>