### Test and Implementation Details:
void prototype(int8_t size, int8_t a[size][size]);<br>

*******************
TARGET_INDEX:<b>int8_t</b>
TARGET_TYPE:<b>int8_t</b>

- 4 + (size * 1)} dist + (size * 1)} vertex_set + (size * 1)} prev + (size * size)}graph
- size <= 9 ----> 4 + 9 + 9 + 9 + 81 ---> 111

<b>int8_t size</b> [2,9];100

The graph doesn't admit negative costs on edges<br>
<b>int8_t a[size][size]</b>[-128, 127]<br>

*******************
TARGET_INDEX:<b>int8</b>
TARGET_TYPE:<b>int</b>

- 8 + (size * 2)} dist + (size * 2)} vertex_set + (size * 2)} prev + (size * size * 2)}graph
- size <= 5 --> 8 + 10 + 10 + 10 + 50 ---> 88

<b>int  size</b> [2,5];100
The graph doesn't admit negative costs on edges<br>
<b>int a[size][size]</b>[-32768, 32767] <br>

*******************
TARGET_INDEX:<b>int8_t</b>
TARGET_TYPE:<b>long</b>

<b>int8_t  size</b> [2,3];100
The graph doesn't admit negative costs on edges<br>
<b>long a[size][size]</b>[-2147483648, 2147483647]<br>


*******************
TARGET_INDEX:<b>int8_t</b>
TARGET_TYPE:<b>float</b>

<b>int8_t  size</b> [2,3];100
The graph doesn't admit negative costs on edges<br>
<b>float a[size][size]</b>[-2147483648.0, 2147483647.0]<br>