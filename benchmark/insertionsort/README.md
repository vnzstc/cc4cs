## Insertion Sort 
This README explains the execution flow of the algorithm and how much memory it occupies.

#### Files 
&nbsp;&nbsp;&nbsp;&nbsp; frst.c - It is the file that when the Leon3 or the Atmega328p is chosen as microprocessor  
&nbsp;&nbsp;&nbsp;&nbsp; scnd.c - It is the file that is executed when the 8051 is chosen as microprocessor  
&nbsp;&nbsp;&nbsp;&nbsp; parameters.c - It is file that contains the possible values assumed by the parameters of the function

#### Variables
&nbsp;&nbsp;&nbsp;&nbsp; TARGET_INDEX:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; i, j, size;  
&nbsp;&nbsp;&nbsp;&nbsp;TARGET_TYPE:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; key, a[size];

#### Occupied Memory
&nbsp;&nbsp;&nbsp;&nbsp; **#b** = number of bytes used by a given data type (e.g. int8_t, int16_t)  
&nbsp;&nbsp;&nbsp;&nbsp; **#index** = number of variables used as an index  
&nbsp;&nbsp;&nbsp;&nbsp; **size** = actual size of the arrays  

&nbsp;&nbsp;&nbsp;&nbsp; **Eq**: Total Memory > (#index * #b) + #b + (size * #b)