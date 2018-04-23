#include <8051.h>
#include <values.h>

void resetValues()
{
	P0 = 0;
	P1 = 0;
	P2 = 0;
	P3 = 0;
}

void prova(int k)
{
	int cont = 0;
	int i = 0; 

	for(; i < k; i++)
	{
		cont++;
	}
}

void main()
{
	prova(k);
	resetValues();
}
