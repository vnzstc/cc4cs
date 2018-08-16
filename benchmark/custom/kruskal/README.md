## Test and Implementation Details:

void prototype(int8 size, int8 a[size][size]);

*******************
TARGET_INDEX:<b>int8</b>
TARGET_TYPE:<b>int8</b>

- 8 + (size * 1)} union_find + (size* size * 1) <br>
- size <= 10 ---> 8 + 10 + 100 ---> TOT: 118 <br>

<b>int8_t size</b> [2, 10];100 <br>
<b>int8_t a[size][size]</b> [-128, 127]


Warnings: 

../../kruskal.c:53: warning 94: comparison is always true due to limited range of data type
../../kruskal.c:80: warning 94: comparison is always true due to limited range of data type
../../kruskal.c:113: warning 94: comparison is always true due to limited range of data type
../../kruskal.c:183: warning 94: comparison is always true due to limited range of data type

Resolution:

Added cast when I assign integer costants.


*******************
TARGET_INDEX:<b>int8_t</b>
TARGET_TYPE:<b>int</b>

- 16 + (size * 2)} union_find + (size* size * 2)}a <br>
- size <= 6 ---> 16 + 12 + 72 ---> TOT: 100 <br>

<b>int size</b> [2,6];100 <br>
<b>int a[size][size]</b> [-32768, 32767] 

No Warnings! 

*******************
TARGET_INDEX:<b>int8</b>
TARGET_TYPE:<b>long</b>

- 22 + (size * 4)} union_find + (size* size * 4)}a <br>
- size <= 4 ---> 22 + 16 + 64 ---> TOT: 106 <br>

<b>long size</b> [2,4];100 <br>
<b>long a[size][size]</b> [-2147483648, 2147483647]



Warnings: 

../../includes/values_358/values.h:5: warning: this decimal constant is unsigned only in ISO C90
../../includes/values_358/values.h:5: warning: this decimal constant is unsigned only in ISO C90
../../includes/values_358/values.h:6: warning: this decimal constant is unsigned only in ISO C90
../../includes/values_358/values.h:6: warning: this decimal constant is unsigned only in ISO C90
../../includes/values_358/values.h:7: warning: this decimal constant is unsigned only in ISO C90
../../includes/values_358/values.h:7: warning: this decimal constant is unsigned only in ISO C90
../../kruskal.c: In function 'find_min':
../../kruskal.c:69: warning: this decimal constant is unsigned only in ISO C90

Resolution:

We can ignore this warning


*******************
TARGET_INDEX:<b>int8</b>
TARGET_TYPE:<b>float</b>

- 22 + (size * 4)} union_find + (size* size * 4)}a <br>
- size <= 4 ---> 22 + 16 + 64 ---> TOT: 106 <br>

<b>int8 size</b> [2,3];100 <br>
<b>float a[size][size]</b> [-2147483648.0, 2147483647.0]


Warnings:

../../kruskal.c: In function 'find_min':
../../kruskal.c:69: warning: this decimal constant is unsigned only in ISO C90
