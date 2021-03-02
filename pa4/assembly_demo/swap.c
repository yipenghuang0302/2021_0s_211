#include <stdlib.h>
#include <stdio.h>

void swap_uc ( unsigned char*a, unsigned char*b ) {
  unsigned char temp = *b;
  *b = *a;
  *a = temp;
}

void swap_sc ( signed char*a, signed char*b ) {
  signed char temp = *b;
  *b = *a;
  *a = temp;
}

void swap_c ( char*a, char*b ) {
  char temp = *b;
  *b = *a;
  *a = temp;
}

void swap_s ( short*a, short*b ) {
  short temp = *b;
  *b = *a;
  *a = temp;
}

void swap_i ( int*a, int*b ) {
  int temp = *b;
  *b = *a;
  *a = temp;
}

void swap_l ( long*a, long*b ) {
  long temp = *b;
  *b = *a;
  *a = temp;
}

int main () {
  char a = 0;
  char b = 1;
  swap_c(&a,&b);
  printf("a=%d,b=%d\n",a,b);
  return EXIT_SUCCESS;
}
