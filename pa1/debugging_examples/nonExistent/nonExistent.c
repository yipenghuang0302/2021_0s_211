#include <stdlib.h>
#include <stdio.h>

int main () {

  int **x = malloc(sizeof(int*));

  **x = 8;

  printf("x = %p\n", x);
  printf("*x = %p\n", *x);
  printf("**x = %d\n", **x);
  fflush(stdout);

}
