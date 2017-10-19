/* MDH WCET BENCHMARK SUITE. */

/* Changes:
 * JG 2005/12/08: Prototypes added, and changed exit to return in main.
 */


#include <stdint.h>
#include <8051.h>
#include <values.h>


typedef uint8_t TARGET_TYPE;
typedef uint8_t TARGET_INDEX;


#define SWAP(a,b) temp=(a);(a)=(b);(b)=temp;

void prototype(uint8_t x, uint8_t y);

void resetValues()
{
  P0 = 0;
  P1 = 0;
  P2 = 0;
  P3 = 0;
}

TARGET_INDEX divides(TARGET_TYPE n, TARGET_TYPE m)
{
  return (m % n == 0);
}

TARGET_INDEX even(TARGET_TYPE n)
{
  return (divides (2, n));
}

TARGET_INDEX prime(TARGET_TYPE n)
{
  TARGET_TYPE i;

  if (even(n))
      return (n == 2);

  for (i = 3; 
       i * i <= n;
       i += 2) { 

      if (divides (i, n)) /* ai: loop here min 0 max 357 end; */
          return 0; 
  }

  return (n > 1);
}

void main ()
{
  TARGET_INDEX res = 0;
  TARGET_TYPE temp = 0;
 
  SWAP(x, y);
  res = (!(prime(x) && prime(y)));
  resetValues();
}

