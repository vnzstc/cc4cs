#include <stdint.h>
#include <8051.h>
#include <values.h>

typedef int8_t TARGET_TYPE;
typedef int8_t TARGET_INDEX;

void prototype(int8_t n, int8_t arr[n]);

TARGET_INDEX i = 0;
TARGET_INDEX j = 0;


void resetValues()
{
	P0 = 0;
	P1 = 0;
	P2 = 0;
	P3 = 0;
}

void insertion_sort()
{
   TARGET_TYPE key = 0;

   for (i = 1; 
   		i < n;
   		i++)
   {
       key = arr[i];
       j = i-1;
 
       while (j >= 0 &&
       		  arr[j] > key)
       {
           arr[j+1] = arr[j];
           j = j-1;
       }
       arr[j+1] = key;
   }
}

void main()
{
	insertion_sort();
	resetValues();
}
