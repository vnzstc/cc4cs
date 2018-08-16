### Test and Implementation Details:
void prototype(int size, int a[size]);<br>

*******************
TARGET_INDEX:<b>int8_t</b>
TARGET_TYPE:<b>int8_t</b>

- 1 + (3 + size * 1}x Overlay)+ size}a 
- size <= 57 ----> 4 + (57 * 2) -----> TOT: 118

<b>int8_t size:</b> [1, 57]; 100<br>
<b>int8_t a[size]:</b> [-128, 127]

*******************
TARGET_INDEX:<b>int8_t</b>
TARGET_TYPE:<b>int</b>

- 4 + (11 + size * 2}x Overlay) + (size * 2) }a
- size <= 25 ----> 15 + (25 * 2) + (25 * 2) -----> TOT: 115

<b>int size:</b> [1, 25]; 100<br>
<b>int a[size]:</b> [-32768, 32767]

*******************
TARGET_INDEX:<b>int8_t</b>
TARGET_TYPE:<b>long</b>

- 43 + size * 4}a 
- size <= 11 ----> 43 + 72 -----> TOT: 115

<b>int8_t size:</b> [1, 11]; 100<br>
<b>long a[size]:</b> [-2147483648, 2147483647]


*******************
TARGET_INDEX:<b>int8_t</b>
TARGET_TYPE:<b>float</b>

- 41 + (size * 4) }x+ (size * 4}a 
- size <= 9 ----> 41 + (6 * 4 * 2) -----> TOT: 89

<b>int8_t size:</b> [1, 6]; 100<br>
<b>float a[size]:</b> [-2147483648.0, 2147483647.0]
