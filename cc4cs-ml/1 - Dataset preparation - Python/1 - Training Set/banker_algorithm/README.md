## Test and Implementation Details:
void prototype(int n_process, int n_resources, int8_t available[n_resources], int8_t allocated[n_process][n_resources], int8_t max[n_process][n_resources]);

*******************
TARGET_INDEX:<b>uint8_t</b>
TARGET_TYPE:<b>uint8_t</b>

- 4 + (n_resources * 1)}available + (n_resources * n_process * 1)} allocated + (n_resources * n_process * 1)} max +
n_process}process + (n_process * n_resources)}need

- n_resources <= 5 , n_process <= 5 -----> 4 + 5 + 25 + 25 + 5 + 25

<b>uint8_t n_resources</b> [1, 5]; 10<br>
<b>uint8_t n_process</b> [1, 5]; 10<br>

<b>uint8_t available[n_resources]</b> [0, 255]</br>
<b>uint8_t allocated[n_process][n_resources]</b> [0, 255]</br>
<b>uint8_t max[n_process][n_resources]</b> [0, 255]</br>

*******************
TARGET_INDEX:<b>uint8_t</b>
TARGET_TYPE:<b>uint16_t</b>

- 8 + (n_resources * 2)}available + (n_resources * n_process * 2)} allocated + (n_resources * n_process * 2)} max +
n_process * 2}process + (n_process * n_resources * 2)}need

- n_resources <= 3 , n_process <= 3 -----> 8 + 6 + 18 + 18 + 6 + 18 
---> TOT: 74

<b>uint16_t n_resources</b> [1, 3]; 10<br>
<b>uint16_t n_process</b> [1, 3]; 10<br>

<b>uint16_t available[n_resources]</b> [0, 65535]</br>
<b>uint16_t allocated[n_process][n_resources]</b> [0, 65535]</br>
<b>uint16_t max[n_process][n_resources]</b> [0, 65535]</br>

*******************
TARGET_INDEX:<b>uint8_t</b>
TARGET_TYPE:<b>uint32_t</b>

- 24 + (n_resources * 4)}available + (n_resources * n_process * 4)} allocated + (n_resources * n_process * 4)} max +
n_process * 4}process + (n_process * n_resources * 4)}need

- n_resources <= 2, n_process <= 2 -----> TOT: 88

<b>uint32_t n_resources</b> [1, 2]; 10<br>
<b>uint32_t n_process</b> [1, 2]; 10<br>

<b>uint32_t available[n_resources]</b> [0, 4294967295]</br>
<b>uint32_t allocated[n_process][n_resources]</b> [0, 4294967295]</br>
<b>uint32_t max[n_process][n_resources]</b> [0, 4294967295]</br>

*******************
TARGET_INDEX:<b>uint8_t</b>
TARGET_TYPE:<b>float</b>

- 8 + (n_resources * 4)}available + (n_resources * n_process * 4)} allocated + (n_resources * n_process * 4)} max +
n_process * 4}process + (n_process * n_resources * 4)}need

- n_resources <= 2  , n_process <= 2 

<b>uint8_t n_resources</b> [1, 2]; 10<br>
<b>uint8_t n_process</b> [1, 2]; 10<br>

<b>float available[n_resources]</b> [0, 4294967295]</br>
<b>float allocated[n_process][n_resources]</b> [0, 4294967295]</br>
<b>float max[n_process][n_resources]</b> [0, 4294967295]</br>
