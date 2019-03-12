#include <stdint.h>
#include <values.h>


typedef int16_t TARGET_TYPE;
typedef int8_t TARGET_INDEX;

TARGET_INDEX i; 
TARGET_INDEX j;

TARGET_TYPE edge_counter()
{
	TARGET_TYPE total_edges = 0;

	for(i = 0;
		i < size;
		i++)
	{
		for(j = 0;
			j < size;
			j++)
		{
			if(a[i][j] != -1)
				++total_edges;
		}
	}

	return total_edges;
}

void bellman_ford(TARGET_INDEX size, TARGET_TYPE a[size][size])
{

	TARGET_TYPE dist[size];
	TARGET_TYPE total_edges = edge_counter();

	for(i = 0;
		i < size;
		i++)
	{
		dist[i] = 127;
	}

	dist[0] = 0;

	for(i = 0;
		i < size;
		i++)
	{
		for(j = 0; 
			j < total_edges; 
			j++)
		{
			if(dist[j] + a[j][i] <= dist[i] && 
				a[j][i] != -1)
			{
				dist[i] = dist[j] + a[j][i];
			}
		}	
	}

}

void make_oriented()
{
	for(i = 0; 
		i < size; 
		i++)
	{
		a[i][i] = -1;

		/* Makes the last node the goal node */
		a[size-1][i] = -1;

		for(j = 0; 
			j < size; 
			j++)
		{
			if(a[i][j] < 0
				&& i != j
				&& a[i][j] != -1 )
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
	bellman_ford(size, a);
}