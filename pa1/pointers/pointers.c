#include <stdio.h>
#include <stdlib.h>

int * modify_array (int size, int param[]);

int main() {

  printf ("\n\nLESSON 1: WHAT ARE POINTERS?\n");
  unsigned int number = 500;
  unsigned int* pointer = &number;
  printf ("number          = %d\n", number);
  printf ("pointer         = %p\n", pointer);
  printf ("sizeof(pointer) = %ld\n", sizeof(pointer));
  printf ("pointer         = %ld\n", (long int) pointer);

  printf ("\n\nLESSON 2: DEREFERENCING POINTERS WITH *\n");
  unsigned int deref_pointer = *pointer;
  printf ("deref_pointer   = %d\n", deref_pointer);

  printf ("\n\nLESSON 3: THE INTEGER DATATYPE USES FOUR BYTES\n");
  printf ("sizeof(int)     = %ld bytes\n", sizeof(int));
  printf ("pointer         = %ld\n", (long int) pointer);
  // notice how the + operator has an overloaded functionality for pointers
  printf ("pointer+1       = %ld\n", (long int) (pointer+1));

  printf ("\n\nLESSON 4: PRINTING EACH BYTE OF AN INTEGER\n");
  // 500 = 256 + 244
  // 500 = 256 + 128 + 64 + 32 + 16 + 4
  // 500 = 0b1_11110100
  unsigned char* char_pointer = (unsigned char*) pointer;
  printf ("byte at %ld = %d\n", (long int) char_pointer+0, *(char_pointer+0));
  printf ("byte at %ld = %d\n", (long int) char_pointer+1, *(char_pointer+1));
  printf ("byte at %ld = %d\n", (long int) char_pointer+2, *(char_pointer+2));
  printf ("byte at %ld = %d\n", (long int) char_pointer+3, *(char_pointer+3));

  printf ("\n\nLESSON 5: POINTERS ARE JUST VARIABLES THAT LIVE IN MEMORY TOO\n");
  unsigned int** pointer_to_pointer = &pointer;
  printf ("  pointer_to_pointer = %ld\n", (long int) pointer_to_pointer);
  printf ("**pointer_to_pointer = %d\n", **pointer_to_pointer);

  printf ("\n\nLESSON 6: ARRAYS\n");
  int array_size = 3;
  int* array = malloc(array_size*sizeof(int));
  for (int i=0; i<array_size; i++) {
    printf("array+%d = %ld\n", i, (long int) (array+i));
  }
  for (int i=0; i<array_size; i++) {
    array[i] = 211 * i;
    printf("array[%d] = %d\n", i, array[i]);
  }
  for (int i=0; i<array_size; i++) {
    printf("*(array+%d) = %d\n", i, *(array+i));
  }




  printf ("\n\nLESSON 7: PASSING BY VALUE\n");
  int* returned_array = modify_array(array_size, array);
  for (int i=0; i<array_size; i++) {
    printf("returned_array[%d] = %d\n", i, returned_array[i]);
  }
  for (int i=0; i<array_size; i++) {
    printf("array[%d]    = %d\n", i, array[i]);
  }

  free(array);
  return 0;
}

int* modify_array (int size, int param[]) {
  for (int i=0; i<size; i++) {
    param[i] = 211 + i;
  }
  return param;
}
