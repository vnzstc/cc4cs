/* MDH WCET BENCHMARK SUITE. */

#include <stdint.h>
#include <values.h>

typedef float TARGET_TYPE;
typedef uint8_t TARGET_INDEX;

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

  prime(n);
}

