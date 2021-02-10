#include <stdlib.h>
#include <stdio.h>

int main () {

    unsigned char n = 2;
    unsigned char  m = 3;

    unsigned char ** p;
    p = calloc( n, sizeof(unsigned char) );

    for (int i = 0; i < n; i++)
        p[i] = calloc( m, sizeof(unsigned char) );

    for (int i = 0; i <= n; i++)
        for (int j = 0; j <= m; j++) {
            p[i][j] = 10*i+j;
            printf("p[%d][%d] = %d\n", i, j, p[i][j]);
        }

}
