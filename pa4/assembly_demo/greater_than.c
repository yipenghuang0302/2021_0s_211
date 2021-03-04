#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>

bool gt_uc ( unsigned char x, unsigned char y ) {
    return x > y;
}
bool gt_sc ( signed char x, signed char y ) {
    return x > y;
}

bool gt_us ( unsigned short x, unsigned short y ) {
    return x > y;
}
bool gt_ss ( signed short x, signed short y ) {
    return x > y;
}

bool gt_ui ( unsigned int x, unsigned int y ) {
    return x > y;
}
bool gt_si ( signed int x, signed int y ) {
    return x > y;
}

bool gt_ul ( unsigned long x, unsigned long y ) {
    return x > y;
}
bool gt_sl ( signed long x, signed long y ) {
    return x > y;
}

int main () {
    return EXIT_SUCCESS;
}
