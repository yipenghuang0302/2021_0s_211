#include <stdlib.h>
#include <stdio.h>

int main () {

    int* pointer0 = malloc(sizeof(int));
    int* pointer1 = pointer0;

    *pointer0 = 100;
    printf("*pointer1 = %d\n", *pointer0);

    *pointer0 = 10;
    printf("*pointer1 = %d\n", *pointer0);

    free(pointer0);

    *pointer1 = 1;
    printf("*pointer1 = %d\n", *pointer0);

}
