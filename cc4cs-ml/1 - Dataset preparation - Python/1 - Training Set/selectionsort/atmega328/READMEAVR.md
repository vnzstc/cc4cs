### Test and Implementation Details:
void prototype(int size, int a[size]);<br>
*******************
TARGET_INDEX:<b>int8_t</b>
TARGET_TYPE:<b>int8_t</b>

- 8 + size}a + (size * 2)}stack

<b> int8_t size:</b>&nbsp;&nbsp;[2, 100]; 100 <br>
<b> int8_t a[size]:</b> [-128, 127]


*******************
TARGET_INDEX:<b>int8_t</b>
TARGET_TYPE:<b>int</b>

<b> int8_t size:</b>&nbsp;&nbsp;[2, 100]; 100 <br>
<b> int a[size]:</b> [-32766,32767]

*******************
TARGET_INDEX:<b>int8_t</b>
TARGET_TYPE:<b>long</b>

<b> int8_t size:</b>&nbsp;&nbsp;[2, 100]; 100 <br>
<b> long a[size]:</b> [-2147483648, 2147483647]


*******************

TARGET_INDEX:<b>int8_t</b>
TARGET_TYPE:<b>float</b>

<b> int8_t size:</b>&nbsp;&nbsp;[2, 100]; 100 <br>
<b> float a[size]:</b> [-2147483648.0, 2147483647.0]
