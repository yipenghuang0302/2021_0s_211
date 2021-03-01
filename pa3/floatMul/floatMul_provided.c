#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <math.h>

#define EXP_SZ 8
#define FRAC_SZ 23

int main(int argc, char *argv[]) {

    // float value = *(float *) &binary; // you are not allowed to do this.
    // unsigned int binary = *(unsigned int*) &value; // you are not allowed to do this.

    FILE* fp = fopen(argv[1], "r");
    if (!fp) {
        perror("fopen failed");
        return EXIT_FAILURE;
    }

    // SETUP

    // first, read the binary number representation of multiplier
    /* ... */

    // notice that you are reading two different lines; caution with reading
    /* ... */

    // first, read the binary number representation of multiplcand
    /* ... */

    float product = *(float *) &multiplier * *(float *) &multiplicand; // you are not allowed to print from this.
    unsigned int ref_bits = *(unsigned int *) &product; // you are not allowed to print from this. But you can use it to validate your solution.

    // SIGN
    /* ... */
    printf("%d_",sign);
    assert (sign == (1&ref_bits>>(EXP_SZ+FRAC_SZ)));

    // EXP
    // get the exp field of the multiplier and multiplicand
    /* ... */
    // add the two exp together
    /* ... */
    // subtract bias
    /* ... */

    // FRAC
    // get the frac field of the multiplier and multiplicand
    /* ... */
    // assuming that the input numbers are normalized floating point numbers, add back the implied leading 1 in the mantissa
    /* ... */
    // multiply the mantissas
    /* ... */

    // overflow and normalize
    /* ... */

    // rounding
    /* ... */

    // move decimal point
    /* ... */

    // PRINTING
    // print exp
    for ( int bit_index=EXP_SZ-1; 0<=bit_index; bit_index-- ) {
        bool trial_bit = 1&exp>>bit_index;
        printf("%d",trial_bit);
        assert (trial_bit == (1&ref_bits>>(bit_index+FRAC_SZ)));
    }
    printf("_");

    // print frac
    for ( int bit_index=FRAC_SZ-1; 0<=bit_index; bit_index-- ) {
        bool trial_bit = 1&frac>>bit_index;
        printf("%d",trial_bit);
        assert (trial_bit == (1&ref_bits>>(bit_index)));
    }

    return(EXIT_SUCCESS);

}
