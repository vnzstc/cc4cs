#include <stdint.h>
#include <8051.h>
#include <values.h>

typedef uint32_t TARGET_TYPE;
typedef uint8_t TARGET_INDEX;

void prototype(uint32_t n, uint32_t a[n][n]);

/*
 * The graph is rapresented with an adjacency map that contains the 
 * costs of edges between nodes 
 */

void resetValues()
{
	P0 = 0;
	P1 = 0;
	P2 = 0;
	P3 = 0;
}

void floyd_warshall()
{
  TARGET_INDEX i;
  TARGET_INDEX j;
  TARGET_INDEX h;

  /* 
   * The algorithm checks each path between nodes i and j that going through h node
   * if a minimum cost path is found updates the entry in b table
   */

  for(h = 0;
    h < n;
    h++)
  {
    for(i = 0;
      i < n;
      i++)
    {
      for(j = 0;
        j < n;
        j++)
      {
        if(a[i][h] + a[h][j] < a[i][j])
          a[i][j] = a[i][h] + a[h][j];
      }
    }
  }

}

void main()
{
  floyd_warshall();
  resetValues();
}
