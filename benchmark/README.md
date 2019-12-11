## Framework Benchmark
This directory contains all the functions that can be used to calculate CC4CS. In the README.md file of each directory, it is specified the equation used to calculate the occupied memory. The result of this equation is used to estimate a number that works as upperbound for the ranges included in the parameters.json 

The chosen 8051's instruction set simulator (ISS) needs to set its I/O ports to 0 to stop its execution. The following equation does not comprise, the memory occupied, to store the values of the variables representing the ports.

#### Files 
Each directory contains: 
&nbsp;&nbsp;&nbsp;&nbsp; frst.c - It is the file that when the Leon3 or the Atmega328p is chosen as microprocessor  
&nbsp;&nbsp;&nbsp;&nbsp; scnd.c - It is the file that is executed when the 8051 is chosen as microprocessor  
&nbsp;&nbsp;&nbsp;&nbsp; parameters.c - It is file that contains the possible values assumed by the parameters of the function