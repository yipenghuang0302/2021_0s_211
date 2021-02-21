#include <stdio.h>
#include <stdlib.h>

int editArray(int* numbers, int index, int newNum);

int main(int argc, char const *argv[])
{
    // open file
    FILE *fp;
    fp = fopen(argv[1], "r");

    if (fp == NULL) {
        printf("file error\n");
        return 0;
    }

    // read first number
    int numCount;
    fscanf(fp, "%d", &numCount);

    printf("numCount: %d\n", numCount);

    // declare without malloc
    // int numbers[numCount];

    // malloc numbers array
    int* numbers = (int*) malloc(numCount * sizeof(int));

    // initialize all values to 0
    for (int i = 0; i < numCount; i++) {
        numbers[i] = 0;
    }
    
    // read numbers from file and enter them into the array
    for (int i = 0; i < numCount; i++) {
        fscanf(fp, "%d", &(numbers[i]));
        printf("%d\t", numbers[i]);
    }
    printf("\n");

    // call function to edit malloced numbers array from another function
    editArray(numbers, 3, 42);
    printf("numbers[3]: %d\n", numbers[3]);

    for (int i = 0; i < numCount; i++) {
        printf("%d\t", numbers[i]);
    }
    printf("\n");

    // free dynamically allocated array
    free(numbers);
    
    return EXIT_SUCCESS;
}

int editArray(int* numbers, int index, int newNum) {
    numbers[index] = newNum;

    return EXIT_SUCCESS;
}
