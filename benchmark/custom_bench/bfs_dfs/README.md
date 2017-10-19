### Test and Implementation Details:
void prototype(int size, int a[size][size])

*******************
TARGET_INDEX:<b>int8_t</b>
TARGET_TYPE:<b>int8_t</b>

- 4 + (size * size * 1)}array_a + (size * 1)}array_array + 2 <br>
- size <= 10 ---> 4 + (100) + (10) + 2 ---> TOT: 116

<b>int8_t size:</b> [2, 10]; 100<br>
<b>int8_t a[size][size]:</b> [-128, 127]

*******************
TARGET_INDEX:<b>int8_t</b>
TARGET_TYPE:<b>int</b>

- 8 + (size * size * 2)}array_a + (size * 2)}array_array + 2 (Overlay) <br>

- size <= 6 ---> 8 + (36 * 2) + (12) + 2 ---> TOT: 94

<b>int size:</b> [2, 6]; 100<br>
<b>int a[size][size]:</b> [-32768, 32767]

*******************
TARGET_INDEX:<b>int8_t</b>
TARGET_TYPE:<b>long</b>

- 8 + (size * size * 4)}array_a + (size * 4)}array_array + 2 (Overlay) <br>
- size <= 4 ---> 8 + (64) + (16) ---> TOT: 88

<b>long size:</b> [2, 4]; 100<br>
<b>long a[size][size]:</b> [-2147483648, 2147483647]  

*******************
TARGET_INDEX:<b>int8_t</b>
TARGET_TYPE:<b>float</b>

- 8 + (size * size * 4)}array_a + (size * 4)}array_array + 2 (Overlay) <br>
- size <= 4 ---> 8 + (64) + (16) ---> TOT: 88

<b>int8_t size:</b> [2, 4]; 100<br>
<b>float a[size][size]:</b> [-2147483648.0, 2147483647.0]  


