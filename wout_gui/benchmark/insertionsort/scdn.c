#include <stdint.h>
#include <8051.h>
#include <values.h>

typedef float TARGET_TYPE;
typedef long TARGET_INDEX;

void insertionsort(TARGET_INDEX size, TARGET_TYPE a[size])
{
    TARGET_INDEX i, j = 0;
    TARGET_TYPE key = 0;

    for (i = 1; i < size; i++)
    {

        key = a[i];
        j = i-1;

        while (j >= 0 && a[j] > key)
        {
            a[j+1] = a[j];
            j = j-1;
        }

        a[j+1] = key;
    }
}

void reset_values()
{
  P0 = 0;
  P1 = 0;
  P2 = 0;
  P3 = 0;
}

void main()
{
	insertionsort(size, a);
	reset_values();
}
