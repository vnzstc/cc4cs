## Test and Implementation Details:
void prototype(int8_t size, int8_t a[size][size], int8_t goal);

*******************
TARGET_INDEX:<b>int8_t</b>
TARGET_TYPE:<b>int8_t</b>

- 7 + (size * 1)} come_from +  (size * 1)} frontier + (size*size*1)}a
- size <= 9 ---> 7 + 9 + 9 + 81 ---> TOT: 106

<b>int8_t size</b> [2,9];50<br>

The graph doesn't admit negative costs on edges<br>
<b>int8_t a[size][size]</b>[-128, 127]<br>

Goal Destination<br>
<b>int8_t goal</b> [0; size-1] :> [0, 8];2

*******************
TARGET_INDEX:<b>int8_t</b>
TARGET_TYPE:<b>int</b>


- 14 + (size * 2)} come_from +  (size * 2)} frontier + (size*size*2)}a
- size <= 6 ---> 14 + 12 + 12 + 72 ---> TOT: 110

<b>int size</b> [2,6];50<br>

The graph doesn't admit negative costs on edges<br>
<b>int a[size][size]</b>[-32768, 32767]<br>

Goal Destination<br>
<b>int goal</b> [0; size-1] :> [0, 5];2

*******************
TARGET_INDEX:<b>int8_t</b>
TARGET_TYPE:<b>long</b>

<b>long size</b> [2,3];50<br>

The graph doesn't admit negative costs on edges<br>
<b>long a[size][size]</b> [-2147483648, 2147483647]<br>

Goal Destination<br>
<b>long goal</b> [0; size-1] :> [0, 2];2

Warnings!

*******************
TARGET_INDEX:<b>int8_t</b>
TARGET_TYPE:<b>float</b>

<b>int8_t size</b> [2,3];50<br>

The graph doesn't admit negative costs on edges<br>
<b>float a[size][size]</b> [-2147483648.0, 2147483647.0]<br>

Goal Destination<br>
<b>int8_t goal</b> [0; size-1] :> [0, 2];2

