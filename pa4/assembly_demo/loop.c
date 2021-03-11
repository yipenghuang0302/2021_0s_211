#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>

unsigned long count_bits_for (
    unsigned long number
) {
    unsigned long tally = 0;
    for (int shift=0; shift<8*sizeof(unsigned long); shift++) {
        tally += 0b1 & number>>shift;
    }
    return tally;
}

unsigned long count_bits_while (
    unsigned long number
) {
    unsigned long tally = 0;
    int shift=0;
    while (shift<8*sizeof(unsigned long)) {
        tally += 0b1 & number>>shift;
        shift++;
    }
    return tally;
}

unsigned long count_bits_while_goto (
    unsigned long number
) {
    unsigned long tally = 0;
    int shift=0;
    if (!(shift<8*sizeof(unsigned long))) {
        goto DONE;
    }
LOOP:
        tally += 0b1 & number>>shift;
        shift++;
    if ((shift<8*sizeof(unsigned long))) {
        goto LOOP;
    }
DONE:
    return tally;
}

unsigned long count_bits_do_while (
    unsigned long number
) {
    unsigned long tally = 0;
    int shift=0;
    do {
        tally += 0b1 & number>>shift;
        shift++;
    } while (shift<8*sizeof(unsigned long));
    return tally;
}

unsigned long count_bits_do_while_goto (
    unsigned long number
) {
    unsigned long tally = 0;
    int shift=0;
LOOP:
        tally += 0b1 & number>>shift;
        shift++;
    if ((shift<8*sizeof(unsigned long))) {
        goto LOOP;
    }
    return tally;
}

int main () {
    return EXIT_SUCCESS;
}
