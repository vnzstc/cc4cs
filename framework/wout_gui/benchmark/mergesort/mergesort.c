#include <stdint.h>
#include <values.h>
#include <8051.h>

typedef long TARGET_TYPE;
typedef int8_t TARGET_INDEX;

void prototype(long size, long a[size]);

TARGET_INDEX h = 0;

void resetValues()
{
	P0 = 0;
	P1 = 0;
	P2 = 0;
	P3 = 0;
}


void merge(TARGET_INDEX i1, TARGET_TYPE f1, TARGET_TYPE f2)
{
	TARGET_TYPE x[size];
	TARGET_INDEX i2 = f1 + 1;
	TARGET_INDEX i = 0;
	TARGET_TYPE start = i1;

	while(i1 <= f1 &&
		  i2 <= f2)
	{
		if(a[i1] <= a[i2])
			x[i++] = a[i1++];
		else
			x[i++] = a[i2++];
	}


	if(i1 <= f1)
	{
		for(h = i1;
			h <= f1;
			h++)
			x[i++] = a[h];
	}
	else{

		for(h = i2;
			h <= f2;
			h++)
			x[i++] = a[h];
	}

	for(h = start, i = 0;
		h <= f2;
		h++)
		a[h] = x[i++];
}


TARGET_TYPE min(TARGET_TYPE c, TARGET_TYPE b)
{
	return c < b ? c : b;
}

void mergesort()
{
	TARGET_TYPE m = 0;
	TARGET_TYPE x = 0;

	for(m = 1; 
		m <= size-1;
		m *= 2)
	{
		for(x = 0; 
			x < size-1;
			x += (2*m))
		{
			merge(x, x+m-1, min(x + 2*m - 1, size-1));

 		}
	}

}


void main()
{
	mergesort();
	resetValues();
}