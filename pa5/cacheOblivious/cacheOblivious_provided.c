#include <stddef.h>
#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

/* Markers used to bound trace regions of interest */
volatile char MARKER_START, MARKER_END;

// Cache oblivious matrix transpose
// https://en.wikipedia.org/wiki/Cache-oblivious_algorithm
void recursiveMatTrans (
    size_t global_n, // overall size of matrix needed to find index for given row and col
    size_t n, // size of submatrix in this recursive call
    int* A, size_t offset_row_A, size_t offset_col_A,
    int* B, size_t offset_row_B, size_t offset_col_B
) {

    if (n<=32) { // base case
        for ( size_t i=0; i<n; i++ ) {
            for ( size_t j=0; j<n; j++ ) {
                B[ (offset_row_B+j)*global_n + offset_col_B+i ] = A[ (offset_row_A+i)*global_n + offset_col_A+j ];
            }
        }
    } else { // recursive case
        recursiveMatTrans ( global_n, n>>1, A, offset_row_A,        offset_col_A,        B, offset_row_B,        offset_col_B        );
        /* ... */
        /* ... */
        /* ... */
    }
}

int main(int argc, char* argv[])
{

    /* Record marker addresses */
    FILE* marker_fp = fopen(".marker","w");
    assert(marker_fp);
    fprintf(marker_fp, "%llx\n%llx",
        (unsigned long long int) &MARKER_START,
        (unsigned long long int) &MARKER_END );
    fclose(marker_fp);

    if (argc!=2) {
        printf("Usage: ./matTrans <matrix_a_file>\n");
        exit(EXIT_FAILURE);
    }

    FILE* matrix_a_fp = fopen(argv[1], "r");
    if (!matrix_a_fp) {
        perror("fopen failed");
        return EXIT_FAILURE;
    }
    size_t n;
    fscanf(matrix_a_fp, "%ld\n", &n);
    int* a = calloc( n*n, sizeof(int) );
    for ( size_t i=0; i<n; i++ ) {
        for ( size_t j=0; j<n; j++ )
            fscanf(matrix_a_fp, "%d ", &a[i*n+j]);
        fscanf(matrix_a_fp, "\n");
    }
    fclose(matrix_a_fp);

    int* b = calloc( n*n, sizeof(int) );
    MARKER_START = 211;
    recursiveMatTrans ( n, n, a, 0, 0, b, 0, 0 );
    MARKER_END = 211;

    for ( size_t i=0; i<n; i++ ) {
        for ( size_t j=0; j<n; j++ ) {
            printf( "%d ", b[i*n+j] );
        }
        printf( "\n" );
    }

    free(b);
    free(a);
    exit(EXIT_SUCCESS);

}
