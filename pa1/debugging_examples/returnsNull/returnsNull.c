#include <stdlib.h>
#include <stdio.h>

int* returnsNull () {
  int val = 100;
  return &val;
}

int main () {

  int* pointer = returnsNull();
  printf("pointer = %p\n", pointer);
  printf("*pointer = %d\n", *pointer);

}
