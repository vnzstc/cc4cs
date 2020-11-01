#include <stdint.h>
#include <8051.h>
#include <values.h> 

typedef int16_t TARGET_INDEX;
typedef int16_t TARGET_TYPE;

#ifndef ARRAYS
#define STACK
TARGET_TYPE stack[size];
#define VISITED
int8_t visited[size];
#endif

TARGET_INDEX top = -1;

void reset_values()
{
	P0 = 0;
	P1 = 0;
	P2 = 0;
	P3 = 0;
}

void create_adjacency_matrix()
{
    TARGET_INDEX i, j = 0;

    for(i = 0; i < size; i++)
    {
        for(j = 0; j < size; j++)
		{
			if(a[i][j] > 0)
				a[i][j] = 1;
			else
				a[i][j] = 0;			
		}
    }    
}

TARGET_TYPE pop()
{
	return stack[top--];
}

void push(TARGET_INDEX vertex)
{
	stack[++top] = vertex;
}

void dfs(TARGET_INDEX size, TARGET_TYPE a[size][size])
{
	TARGET_INDEX i = 0;
	// Mark the first node as visited
	visited[0] = 1;
	// Put the first element in the stack
	push(0);

	// stack is not empty
	while(top != -1)
	{
		TARGET_TYPE next = pop();

		for(i = 0; i < size; i++)
		{
			TARGET_TYPE neighbor = a[next][i];

			if(neighbor == 1 && (!visited[i]))
			{
				// put next in the stack;
				push(i);
				// mark next as visited;
				visited[i] = 1;
			}
		}
	}
}

void main()
{
	// initialize the visited array
	TARGET_INDEX i = 0;
	for(i = 0; i < size; i++)
		visited[i] = 0;

	create_adjacency_matrix();
	dfs(size, a);	
	reset_values();
}
