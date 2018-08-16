#include <stdint.h>
#include <values.h>

typedef uint8_t TARGET_TYPE;
typedef uint8_t TARGET_INDEX;

void prototype(uint8_t n, uint8_t m);

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
        r = m % n; 
        m = n;
        n = r;
    }

    return m;
}


void main()
{
    gcd();
}