#include <stdint.h>
#include <8051.h>
#include <values.h>

typedef int8_t TARGET_TYPE;
typedef int8_t TARGET_INDEX;

void test(TARGET_TYPE a, TARGET_INDEX b, TARGET_TYPE c[b], TARGET_INDEX f, TARGET_TYPE e[b][f])
{
	TARGET_TYPE d = 0;
	d = a + b;
}

void resetValues()
{
	P0 = 0;
	P1 = 0;
	P2 = 0;
	P3 = 0;
}

void main()
{
	test(a, b, c, f, e);
	resetValues();
}