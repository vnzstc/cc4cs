#include <stdint.h>
#include <8051.h>
#include <values.h>

typedef float TARGET_TYPE;
typedef int8_t TARGET_INDEX;

void prototype(int8_t size, float a[size][size]);

TARGET_TYPE array[size];

TARGET_INDEX tail = 0;
TARGET_INDEX head = 0;

TARGET_INDEX current = 0;
TARGET_INDEX i = 0;

/*
 * My implementation of bfs, dfs takes in input a graph represented as a square adjacency matrix,
 * where the connections between nodes are represented with a 1 otherwise we will find a -1
 * if two nodes aren't connected.
 */


void resetValues()
{
	P0 = 0;
	P1 = 0;
	P2 = 0;
	P3 = 0;
}

/* Print for debug

void print_queue()
{
	for(i = 0;
		i < size;
		i++)
	{
		printf("%d ", array[i]);
	}
}

*/


void enqueue(TARGET_TYPE par)
{
	if((tail-head) != size-1)
	{
		array[tail] = par;
		tail = (tail+1) % size;
	}
}


TARGET_TYPE dequeue()
{
	TARGET_TYPE element = 0;

	if(head != tail)
	{	
		element = array[head];
		head = (head+1) % size;
	}

	return element;
}

void clean_input()
{
	head = 0;
	tail = 0;

	for(i = 0;
		i < size; 
		i++)
	{
		a[i][i] = -1;
		array[i] = 0; 
	}
}

void breath_first_search()
{
	/* 
	 * We store a -2 in a[node][node] position to indicate that a node has been already 
	 * visited
	 */
	a[0][0] = -2;
	enqueue(0);

	while(head != tail)
	{
		current = dequeue();

		for(i  = 0; 
			i < size;
			i++)
		{	
			if(a[i][i] != -2 &&
			   a[current][i] > 0)	
			{
				enqueue(i);
				a[i][i] =  -2;
			}
		}
	}
}

void depth_first_search()
{	

	array[head] = 0;
	++tail;

	while(tail > 0)
	{
		current = array[head];
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
					array[tail++] = i;
					head = tail-1;
				}
			}
			
		}
	}
}


void main()
{

	breath_first_search();
	//print_queue();
	/* clean_input(): 
	 * restores the input to the initial condition in preparation of depth first search 
	 */
	clean_input();
	depth_first_search();
	resetValues();
}