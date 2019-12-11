#include <stdint.h>
#include <values.h>

typedef float TARGET_TYPE;
typedef long TARGET_INDEX;

TARGET_TYPE dist[size];
TARGET_INDEX i, j = 0;

void bellmanford(TARGET_INDEX size, TARGET_TYPE a[size][size])
{
	TARGET_INDEX up = 0;
	TARGET_TYPE total_edges = 0;

	for(i = 0; i < size; i++)
	{
		for(j = 0; j < size; j++)
		{
			if(a[i][j] != -1)
				++total_edges;
		}
	}

	// Calculates the maximum value for the current datatype
	up = 1;
	for(i = 0; i < (8*sizeof(TARGET_TYPE)) - 1; i++)
		up *= 2;
	up -= 1;

	// Initializes the dist array 
	for(i = 0; i < size; i++)
		dist[i] = up;

	// Sets the source equal to zero
	dist[0] = 0;
	
	for(i = 0; i < size; i++)
	{
		for(j = 0; j < total_edges; j++)
		{
			if(dist[j] + a[j][i] <= dist[i] && a[j][i] != -1)
				dist[i] = dist[j] + a[j][i];
		}	
	}

}

void make_oriented()
{
	for(i = 0; i < size; i++)
	{
		a[i][i] = -1;

		// Makes the last node the goal node 
		a[size-1][i] = -1;

		for(j = 0; j < size; j++)
		{
			if(a[i][j] < 0 && i != j && a[i][j] != -1)
			{
				a[i][j] *= -1;
				a[j][i] = -1;
			}
			else
			{

				if(a[j][i] >= 0)
					a[i][j] = -1;
			}
		}
	}

}

void main()
{

	make_oriented();
	bellmanford(size, a);
}