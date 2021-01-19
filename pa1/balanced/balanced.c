#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>

// Struct to hold the expected close brace character and a pointer to the next element.
struct element {
    char close;
    struct element* next;
};

int main(int argc, char* argv[])
{

    FILE* fp = fopen(argv[1], "r");
    if (!fp) {
        perror("fopen failed");
        return EXIT_FAILURE;
    }

    bool balanced = true;

    char buff;
    while ( fscanf(fp, "%c", &buff)==1 ) {
    }

    printf ( balanced ? "yes" : "no" );
    fclose(fp);
    return 0;
}
