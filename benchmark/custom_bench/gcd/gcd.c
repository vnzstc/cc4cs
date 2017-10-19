#include <stdint.h>
#include <8051.h>
#include <values.h>

typedef int8_t TARGET_TYPE;
typedef int8_t TARGET_INDEX;

void prototype(int8_t n, int8_t m);

void resetValues()
{
    P0 = 0;
    P1 = 0;
    P2 = 0;
    P3 = 0;
}

TARGET_TYPE modulo(TARGET_TYPE x, TARGET_TYPE y)
{
    TARGET_TYPE result = x; 
      
    while (result >= y)
        result -= y;

    return result;
}

TARGET_TYPE gcd()
{

    TARGET_TYPE r = 0;

    if(m == 0 && n == 0)
        return -1;

    if(m < 0) 
        m = -m;
    if(n < 0)
        n = -n;


    while(n) 
    {
        r = modulo(m,n);
        m = n;
        n = r;
    }

    return m;
}


void main()
{
    gcd();
    resetValues();
}