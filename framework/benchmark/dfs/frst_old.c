#include <stdint.h>
#include <values.h>

typedef int8_t TARGET_TYPE;
typedef int8_t TARGET_INDEX;

TARGET_INDEX current, i, tail, head = 0;
TARGET_TYPE visited[size];

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

void clean_input()
{
	head, tail = 0;

	for(i = 0; i < size; i++){
		visited[i] = 0;
		a[i][i] = -1;
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
	clean_input();
	dfs(size, a);
}