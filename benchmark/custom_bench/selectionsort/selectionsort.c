#include <stdint.h>
#include <8051.h>
#include <values.h>

typedef float TARGET_TYPE;
typedef int8_t TARGET_INDEX;

void prototype(int8_t n, float arr[n]);

TARGET_INDEX i = 0;
TARGET_INDEX j = 0;


void resetValues()
{
	P0 = 0;
	P1 = 0;
	P2 = 0;
	P3 = 0;
}


void swap(TARGET_INDEX index_1, TARGET_INDEX index_2)
{
  TARGET_TYPE b = arr[index_1];
  arr[index_1] = arr[index_2];
  arr[index_2] = b;
}

void selection_sort()
{
  TARGET_INDEX min_idx = 0;

  for (i = 0; 
       i < n-1;
       i++)
  {

    min_idx = i;

    for (j = i+1;
         j < n;
         j++)
      if (arr[j] < arr[min_idx])
        min_idx = j;

      swap(min_idx, i);
    }
}

void main()
{
	selection_sort();
  resetValues();
}
