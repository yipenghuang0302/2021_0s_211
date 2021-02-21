#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

int main(int argc, char* argv[])
{

    // PROCESSING VECTOR A

    FILE* vector_a_fp = fopen(argv[1], "r");
    if (!vector_a_fp) {
        perror("fopen failed");
        return EXIT_FAILURE;
    }

    // First way to read a single integer
    unsigned int length_l;
    fscanf(vector_a_fp, "%d", &length_l);

    // Declaring vector_a as a variable-length array
    double vector_a[length_l];
    for ( unsigned int i=0; i<length_l; i++ ) {
        // First way to read a single floating point
        fscanf(vector_a_fp, "%lf", &vector_a[i]);
    }
    fclose(vector_a_fp);

    // PROCESSING VECTOR B

    FILE* vector_b_fp = fopen(argv[2], "r");
    if (!vector_b_fp) {
        perror("fopen failed");
        return EXIT_FAILURE;
    }

    // Second way to read a single integer
    char buff[256];
    fscanf(vector_b_fp, "%s", buff);
    unsigned int length_m = atoi(buff);

    // Assert that the two vectors must be the same length
    assert ( length_l == length_m );

    // Declaring vector_b as a pointer which we malloc
    double* vector_b = malloc( length_m * sizeof(double*) );
    for ( unsigned int i=0; i<length_m; i++ ) {
        // Second way to read a single floating point
        fscanf(vector_b_fp, "%s", buff);
        *(vector_b+i) = atof(buff);
    }
    fclose(vector_b_fp);

    // DOT PRODUCT CALCULATION

    double sum = 0.0;
    for ( unsigned int i=0; i<length_l; i++ ) {
        // Performing the dot product calculation
        // Notice we can access elements of vectors a and b with either
        // array notation or pointer arithmetic
        sum += *(vector_a+i) * vector_b[i];
    }
    printf("%f\n",sum);

    free( vector_b );

    return 0;

}
