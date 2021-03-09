#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>

short equal_sl ( long x, long y ) {
    return x==y;
}

short below_ul ( unsigned long x, unsigned long y ) {
    return x<y;
}

short nae_ul ( unsigned long x, unsigned long y ) {
    return !(x>=y);
}

short negative ( long x ) {
    return x<0;
}

short lt_sl ( long x, long y ) {
    return x<y;
}

int main () {
    return EXIT_SUCCESS;
}
