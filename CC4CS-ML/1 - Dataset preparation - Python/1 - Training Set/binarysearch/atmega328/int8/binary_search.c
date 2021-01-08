#include <stdint.h>
#include <values.h>

typedef int8_t TARGET_TYPE;
typedef int8_t TARGET_INDEX;

void prototype(int8_t size, int8_t arr[size], int8_t goal);

TARGET_TYPE divide(TARGET_TYPE nu, TARGET_TYPE de) 
{

    TARGET_TYPE temp = 1;
    TARGET_TYPE quotient = 0;

    while (de <= nu) 
    {
        de <<= 1;
        temp <<= 1;
    }

    //printf("%d %d\n",de,temp,nu);
    while (temp > 1) {
        de >>= 1;
        temp >>= 1;

        if (nu >= de)
		{
            nu -= de;
            //printf("%d %d\n",quotient,temp);
            quotient += temp;
        }
    }

    return quotient;
}

TARGET_TYPE binary_search()
{
	TARGET_TYPE l = 0;
	TARGET_TYPE r = size-1;

	while (l <= r)
	{
		TARGET_INDEX m = l + (r-l)/2;
		// TARGET_INDEX m = l + divide((r-l),2);

		if (arr[m] == goal) 
			return m;  

		if (arr[m] < goal) 
			l = m + 1; 
		else
			r = m - 1; 
	}

	return -1; 
}

void main()
{
	binary_search();
}
