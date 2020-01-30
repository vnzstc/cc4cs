#include <stdint.h>
#include <values.h>

typedef int16_t TARGET_TYPE;
typedef int16_t TARGET_INDEX;

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

void main()
{
	insertionsort(size, a);
}