#include <stdint.h>
#include <8051.h>
#include <values.h>

/*
 * This function exchanges two elements in the array given in input. 
 * The variables index_1 and index_2 indicate the position of elements that will be exchanged.
 */
typedef int8_t TARGET_TYPE;
typedef int8_t TARGET_INDEX;

void prototype(int8_t dim, int8_t a[dim]);

void swap(TARGET_INDEX index_1, TARGET_INDEX index_2)
{
	TARGET_TYPE b = a[index_1];
	a[index_1] = a[index_2];
	a[index_2] = b;
}

/*
 * This is the main function of the program. For each element checks if the element in i+1 position is less than the
 * current element. In the positive case, swaps the elements.
 * the process is executed many times as the number of nodes. 
 * This function returns the sorted array.
 */

void bubble_sort()
{
	TARGET_INDEX i;
	TARGET_TYPE j;
	TARGET_TYPE is_sorted;
	TARGET_TYPE currentSwap; 
	TARGET_TYPE lastSwap = dim-1;

	for(j = 0;
		j < dim;
		j++)
	{
		is_sorted = (TARGET_TYPE) 1;
		currentSwap = -1;
		for(i = 0;
			i < lastSwap;
			i++)
		{
			if(a[i] > a[i+1])
			{
				swap(i,i+1);
				is_sorted = 0;
				currentSwap = i;
			}
		}

		if(is_sorted) break;
		lastSwap = currentSwap;
	}
}

void resetValues()
{
	P0 = 0;
	P1 = 0;
	P2 = 0;
	P3 = 0;
}

void main()
{
	bubble_sort();
	resetValues();
}
