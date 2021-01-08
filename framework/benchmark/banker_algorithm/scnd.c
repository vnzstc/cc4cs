#include <stdint.h>
#include <8051.h>
#include <values.h>

typedef unsigned long TARGET_TYPE;
typedef unsigned long TARGET_INDEX;

#ifndef NEED
#define NEED
TARGET_TYPE need[n_process][n_resources];
#endif

TARGET_INDEX i = 0;
TARGET_INDEX j = 0;

TARGET_TYPE found = 0;

void resetValues()
{
	P0 = 0;
	P1 = 0;
	P2 = 0;
	P3 = 0;
}

void create_needs()
{
	for(i = 0; i < n_process; i++)
	{
		for(j = 0; j < n_resources; j++)
			need[i][j] = max[i][j] - allocated[i][j];
	}

}

TARGET_TYPE banker_algorithm(TARGET_INDEX n_process, TARGET_INDEX n_resources, TARGET_TYPE available[n_resources], TARGET_TYPE allocated[n_process][n_resources], TARGET_TYPE max[n_process][n_resources])
{	
	for(i = 0; i < n_process; i++)
	{
		
		for(j = 0; j < n_resources; j++)
		{

			available[j] -= need[i][j];
			allocated[i][j] += need[i][j];
			
			found = 0;

			if(need[i][j] <= available[j] /*&&*/ 
				/*need[i][j] >= 0 */ )
			{
				available[j] += allocated[i][j];
				found = 1;
			}

			if(found == 0)
				return -1;
		}

	}

	return 1;
}


void main()
{

	create_needs();
	banker_algorithm(n_process, n_resources, available, allocated,max);
	resetValues();
}
