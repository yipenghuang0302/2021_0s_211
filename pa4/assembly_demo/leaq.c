#include <stdlib.h>
#include <stdio.h>

long * leaq ( long * ptr, long index ) {
  return &ptr[index+1];
}

long mulAdd ( long base, long index ) {
  return base+index*8+8;
}

int main () {

  long d[2];
  long * ptr = leaq(d,0);
  printf("ptr=%p\n",ptr);

  return EXIT_SUCCESS;
}
