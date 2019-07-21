#include <stdint.h>
#include <values.h>

/*
 * This function exchanges two elements of the input array 
 * The variables index_1 and index_2 indicate the position of elements to exchange.
 */

#define TARGET_INDEX int8_t
#define TARGET_TYPE int8_t

void swap(TARGET_INDEX index_1, TARGET_INDEX index_2)
{
	TARGET_TYPE b = a[index_1];
	a[index_1] = a[index_2];
	a[index_2] = b;
}

/*
 * This is the main function of the program. For each element, it is checked if the element in position i+1 
 * is less than the current one. In the positive case, it swaps the elements.
 * The process is executed many times as the number of nodes. 
 * This function returns the sorted array.
 */

void bubble_sort(TARGET_INDEX dim, TARGET_TYPE a[dim])
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
				swap(i, i+1);
				is_sorted = 0;
				currentSwap = i;
			}
		}

		if(is_sorted) break;
		lastSwap = currentSwap;
	}
}

void main()
{
	bubble_sort(dim, a);
}
