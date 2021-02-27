#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>

#define EXP_SZ 8
#define FRAC_SZ 23

int main(int argc, char *argv[]) {

    FILE* fp = fopen(argv[1], "r");
    if (!fp) {
        perror("fopen failed");
        return EXIT_FAILURE;
    }

    // SETUP

    // first, read the binary number representation of float point number
    char buff;
    unsigned int binary = 0;
    for (int i=EXP_SZ+FRAC_SZ; 0<=i; i--) { // read MSB first as that is what comes first in the file
        fscanf(fp, "%c", &buff);
        binary += buff=='1' ? 1<<i : 0;
    }

    bool sign = 1&binary>>31;

    // E
    unsigned short exp = ((1<<EXP_SZ)-1) & binary>>FRAC_SZ;
    unsigned short bias = (1<<(EXP_SZ-1))-1;
    signed short e = exp - bias;

    // M
    unsigned int frac = ((1<<FRAC_SZ)-1) & binary;
    frac += 1<<FRAC_SZ;
    double m = (double)frac / (double)(1<<FRAC_SZ);

    // https://www.tutorialspoint.com/c_standard_library/c_function_ldexp.htm
    double number = ldexp ( m, e );
    number = sign ? -number : number;
    printf("%e\n", number);

    return EXIT_SUCCESS;

}
