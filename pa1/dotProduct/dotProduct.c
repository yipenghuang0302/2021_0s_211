#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

int main(int argc, char* argv[])
{

    char buff[256];

    FILE* vector_a_fp = fopen(argv[1], "r");
    if (!vector_a_fp) {
        perror("fopen failed");
        return EXIT_FAILURE;
    }
    fscanf(vector_a_fp, "%s", buff);
    unsigned short length_l = atoi(buff);
    double* vector_a = malloc( length_l * sizeof(double) );
    for ( unsigned short i=0; i<length_l; i++ ) {
        fscanf(vector_a_fp, "%s", buff);
        vector_a[i] = atof(buff);
    }
    fclose(vector_a_fp);

    FILE* vector_b_fp = fopen(argv[2], "r");
    if (!vector_b_fp) {
        perror("fopen failed");
        return EXIT_FAILURE;
    }
    fscanf(vector_b_fp, "%s", buff);
    assert ( length_l == atoi(buff) );
    double* vector_b = malloc( length_l * sizeof(double*) );
    for ( unsigned short i=0; i<length_l; i++ ) {
        fscanf(vector_b_fp, "%s", buff);
        *(vector_b+i) = atof(buff);
    }
    fclose(vector_b_fp);

    double sum = 0.0;
    for ( unsigned short i=0; i<length_l; i++ ) {
        sum += *(vector_a+i) * vector_b[i];
    }
    printf("%f\n",sum);

    free( vector_a );
    free( vector_b );

    return 0;

}
