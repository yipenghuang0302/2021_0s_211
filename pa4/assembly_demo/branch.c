#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>

unsigned long absdiff_ternary (
    unsigned long x,
    unsigned long y
) {
    return x<y ? y-x : x-y;
}

unsigned long absdiff_if_else (
    unsigned long x,
    unsigned long y
) {
    if (x<y) return y-x;
    else return x-y;
}

unsigned long absdiff_goto (
    unsigned long x,
    unsigned long y
) {
    if (!(x<y)) goto Else;
    return y-x;
Else:
    return x-y;
}

int main () {
    return EXIT_SUCCESS;
}
