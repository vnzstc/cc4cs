#include <stdint.h>
#include <values.h>
#include <8051.h>

typedef float TARGET_TYPE;
typedef long TARGET_INDEX;

TARGET_INDEX i; 
TARGET_INDEX j;

TARGET_TYPE dist[size];

/* Vertex set is used to keep track of visited nodes */
TARGET_TYPE vertex_set[size];
TARGET_TYPE vertex_set_size;

TARGET_TYPE prev[size];

/* Variable useful during get_min() function */
TARGET_TYPE min;

void resetValues()
{
	P0 = 0;
	P1 = 0;
	P2 = 0;
	P3 = 0;
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

/* Check if vertex_set is empty */

TARGET_TYPE is_empty()
{
	return (vertex_set_size == 0) ? 1 : 0;
}

void get_min()
{
	min = 2147483640;

	for(i = 0;
		i < size;
		i++)
	{
		if(dist[i] <= min && 
			vertex_set[i] != -1)
			min = i;
	}
}

void dijkstra(TARGET_INDEX size, TARGET_TYPE a[size][size])
{
	TARGET_INDEX u = 0;

	for(i = 0;
		i < size;
		i++)
	{
		/* For each vertex in the graph initializes the array that contains the estimates of the distances*/
		dist[i] = 2147483640;
		/* For each vertex in the graph set previous node in the graph as undefined*/
		prev[i] = -1;
		
		/* Add node i to vertex_set */
		vertex_set[i] = i;
		++vertex_set_size;
	}

	/* distance from source to source */
	dist[0] = 0;

	while(!is_empty())
	{
		/* node with the least distance will be selected first */
		get_min();
		u = min;

		vertex_set[u] = -1;
		--vertex_set_size;

		for(i = 0;
			i < size;
			i++)
		{
			if(dist[u] + a[u][i] <= dist[i] && 
				a[u][i] != -1)
			{
				dist[i] = dist[u] + a[u][i];
				prev[i] = u;
			}
		}
	}

}


/* Function for debugging 
void print_dist_prev()
{
	for(i = 0;
		i < size;
		i++)
	{
		printf("dist: %d, prev: %d\n", dist[i], prev[i]);
	}
}

*/

void main()
{

	make_oriented();
	dijkstra(size, a);
	resetValues();
}