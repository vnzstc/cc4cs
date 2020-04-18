#include <stdint.h>
#include <8051.h>
#include <values.h>

typedef float TARGET_TYPE;
typedef long TARGET_INDEX;

int8_t current, i, j, tail, head = 0;
TARGET_TYPE visited[size];

void resetValues()
{
	P0 = 0;
	P1 = 0;
	P2 = 0;
	P3 = 0;
}

void enqueue(TARGET_TYPE par)
{
	if((tail-head) != size-1)
	{
		visited[tail] = par;
		tail = (tail+1) % size;
	}
}

TARGET_TYPE dequeue()
{
	TARGET_TYPE element = 0;

	if(head != tail)
	{	
		element = visited[head];
		head = (head+1) % size;
	}

	return element;
}

void clean_input(TARGET_INDEX size, TARGET_TYPE a[size][size], TARGET_TYPE visited[size])
{
	head, tail = 0;
	visited[size];

	for(i = 0; i < size; i++) 
	{
		visited[i] = 0;
		for(j = 0; j < size; j++)
		{
			if(i == j)
				a[i][i] = -1;

			if(a[i][j] < 0)
				a[i][j] *= -1;	
		}
	}
}

void dfs(TARGET_INDEX size, TARGET_TYPE a[size][size])
{	

	visited[head] = 0;
	++tail;

	while(tail > 0)
	{
		current = visited[head];
		--tail;

		if(a[current][current] != -2)
		{
			a[current][current] = -2;

			for(i = 0;
				i < size;
				i++)
			{
				if(a[i][i] != -2 &&
					a[current][i] > 0)	
				{
					visited[tail++] = i;
					head = tail-1;
				}
			}
			
		}
	}
}
void main()
{
	clean_input(size, a, visited);
	dfs(size, a);
	resetValues();
}