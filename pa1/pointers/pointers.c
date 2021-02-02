#include <stdio.h>
#include <stdlib.h>

void swap_pass_by_values ( int a, int b );
void swap_pass_by_references ( int* a_pointer, int* b_pointer );
int * modify_array (int size, int param[]);
int factorial(int n);

int global_variable = 0;

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

  printf ("\n\nLESSON 7: PASSING-BY-VALUE\n");
  int a = 211;
  int b = 422;
  printf ("before swap_pass_by_values:   a = %d\n", a);
  printf ("before swap_pass_by_values:   b = %d\n", b);
  printf ("outside swap_pass_by_values: &a = %ld\n", (long int) &a);
  printf ("outside swap_pass_by_values: &b = %ld\n", (long int) &b);
  swap_pass_by_values (a,b);
  printf ("after swap_pass_by_values:    a = %d\n", a);
  printf ("after swap_pass_by_values:    b = %d\n", b);

  printf ("\n\nLESSON 8: PASSING-BY-REFERENCE\n");
  printf ("before swap_pass_by_references:   a = %d\n", a);
  printf ("before swap_pass_by_references:   b = %d\n", b);
  printf ("outside swap_pass_by_references: &a = %ld\n", (long int) &a);
  printf ("outside swap_pass_by_references: &b = %ld\n", (long int) &b);
  swap_pass_by_references ( &a, &b );
  printf ("after swap_pass_by_references:    a = %d\n", a);
  printf ("after swap_pass_by_references:    b = %d\n", b);

  printf ("\n\nLESSON 9: PASSING AN ARRAY LEADS TO PASSING-BY-REFERENCE\n");
  int* returned_array = modify_array(array_size, array);
  for (int i=0; i<array_size; i++) {
    printf("returned_array[%d] = %d\n", i, returned_array[i]);
  }
  for (int i=0; i<array_size; i++) {
    printf("array[%d]    = %d\n", i, array[i]);
  }

  printf ("\n\nLESSON 10: C MEMORY MODEL; STACK AND HEAP; RECURSION EXAMPLE\n");
  printf ("global_variable = %d\n", global_variable);
  printf ("Address of global_variable = %ld\n", (long int) &global_variable);
  int n = 3;
  printf ("%d! = %d\n", n, factorial(n));

  free(array);
  return 0;
}

void swap_pass_by_values ( int a, int b ) {
  printf ("inside swap_pass_by_values:  &a = %ld\n", (long int) &a);
  printf ("inside swap_pass_by_values:  &b = %ld\n", (long int) &b);
  int temp = b;
  b = a;
  a = temp;
}

void swap_pass_by_references ( int* a_pointer, int* b_pointer ) {
  printf ("inside swap_pass_by_references:  &a = %ld\n", (long int) a_pointer);
  printf ("inside swap_pass_by_references:  &b = %ld\n", (long int) b_pointer);
  int temp = *b_pointer;
  *b_pointer = *a_pointer;
  *a_pointer = temp;
}

int* modify_array (int size, int param[]) {
  for (int i=0; i<size; i++) {
    param[i] = 211 + i;
  }
  return param;
}

int factorial(int n) {
  printf ("In factorial(%d), the parameter was stored at: %ld\n", n, (unsigned long) &n);
  if (n==1) return 1;
  else {
    int recurse = factorial(n-1);
    printf ("In factorial(%d), the returned value from call to factorial(%d) was stored at: %ld\n", n, n-1, (unsigned long) &recurse);
    return n*recurse;
  }
}
