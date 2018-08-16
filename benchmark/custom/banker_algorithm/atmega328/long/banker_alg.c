#include <stdint.h>
#include <8051.h>
#include <values.h>

typedef uint32_t TARGET_TYPE;
typedef uint8_t TARGET_INDEX;

void prototype(uint8_t n_process, uint8_t n_resources, uint32_t available[n_resources], uint32_t allocated[n_process][n_resources], uint32_t max[n_process][n_resources]);


TARGET_TYPE need[n_process][n_resources];

TARGET_TYPE size = n_process;

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
	for(i = 0; 
		i < n_process;
		i++)
	{
		for(j = 0;
			j < n_resources;
			j++)
		{
			need[i][j] = max[i][j] - allocated[i][j];
		}
	}

}

TARGET_TYPE banker_algorithm()
{	
	for(i = 0; 
		i < n_process;
		i++)
	{
		
		for(j = 0; 
			j < n_resources;
			j++)
		{

			available[j] -= need[i][j];
			allocated[i][j] += need[i][j];
			
			found = 0;
			if( need[i][j] <= available[j] /*&&*/ 
				/*need[i][j] >= 0 */ )
			{
				available[j]  += allocated[i][j];
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
	banker_algorithm();
	resetValues();
}
