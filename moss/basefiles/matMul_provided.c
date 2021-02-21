#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>

int main(int argc, char* argv[])
{

    FILE* matrix_a_fp = fopen(argv[1], "r");
    if (!matrix_a_fp) {
        perror("fopen failed");
        return EXIT_FAILURE;
    }

    char buff[256];

    fscanf(matrix_a_fp, "%s", buff);
    char length_l = atoi(buff);
    int** matrix_a = malloc( length_l * sizeof(int*) );

    fscanf(matrix_a_fp, "%s", buff);
    char length_m = atoi(buff);
    for ( unsigned char i=0; i<length_l; i++ ) {
        matrix_a[i] = malloc( length_m * sizeof(int) );
    }

    fclose(matrix_a_fp);

    for ( unsigned char i=0; i<length_l; i++ ) {
        free( matrix_a[i] );
    }
    free( matrix_a );

    return 0;

}
