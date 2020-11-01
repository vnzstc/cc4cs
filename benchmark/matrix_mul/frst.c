#include <stdint.h>
#include <values.h>

typedef float TARGET_TYPE;
typedef long TARGET_INDEX;

#ifndef RES
#define RES
TARGET_TYPE res[rows_a][columns_b];
#endif

void matrix_mul(TARGET_INDEX rows_a, TARGET_INDEX columns_a, TARGET_TYPE a[rows_a][columns_a], 
				TARGET_INDEX rows_b, TARGET_INDEX columns_b, TARGET_TYPE b[rows_b][columns_b])
{
	TARGET_INDEX i, j, k, tot = 0; 

	/* 
	 * If the number of columns of A is different from the b's rows number then 
	 * the multiplication can't be done 
	 */

	if(columns_a != rows_b)
		return;

	/* Iterates through the rows of A */
	for(i = 0; i < rows_a; i++)
	{
		/* Iterates through the columns of B */
		for(k = 0; k < columns_b; k++)
		{
			/* 
			 * Iterates through the columns of A. We need of the "tot" variable to remember 
			 * the value of an element in res array
			 */

			for(tot = 0, j = 0; j < columns_a; j++)
				tot += (a[i][j] * b[j][k]);

			res[i][k] = tot;
		}
	}
}

void main()
{
	matrix_mul(rows_a, columns_a, a, rows_b, columns_b, b);
}
