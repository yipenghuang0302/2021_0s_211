#include <stdlib.h>
#include <stdio.h>

void immediate ( long * ptr ) {
  *ptr = 0xFFFFFFFFFFFFFFFF;
}

void displacement_c ( char * ptr ) {
  ptr[1] = 0xFF;
}
void displacement_s ( short * ptr ) {
  ptr[1] = 0xFFFF;
}
void displacement_i ( int * ptr ) {
  ptr[1] = 0xFFFFFFFF;
}
void displacement_l ( long * ptr ) {
  ptr[1] = 0xFFFFFFFFFFFFFFFF;
}

void index_c ( char * ptr, long index ) {
  ptr[index] = 0xFF;
}
void index_s ( short * ptr, long index ) {
  ptr[index] = 0xFFFF;
}
void index_i ( int * ptr, long index ) {
  ptr[index] = 0xFFFFFFFF;
}
void index_l ( long * ptr, long index ) {
  ptr[index] = 0xFFFFFFFFFFFFFFFF;
}

void displacement_and_index ( long * ptr, long index ) {
  ptr[index+1] = 0xFFFFFFFFFFFFFFFF;
}

int main () {

  long a;
  immediate(&a);
  printf("a=%lx\n",a);

  long b[2];
  displacement_l(b);
  printf("b[1]=%lx\n",b[1]);

  long c[2];
  index_l(c,1);
  printf("c[1]=%lx\n",c[1]);

  long d[2];
  displacement_and_index(d,0);
  printf("d[1]=%lx\n",d[1]);

  return EXIT_SUCCESS;
}
