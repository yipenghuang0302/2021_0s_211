#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>

struct bstNode {
    int val;
    struct bstNode* l_child;
    struct bstNode* r_child;
};

int main(int argc, char* argv[])
{
    FILE* fp = fopen(argv[1], "r");
    if (!fp) {
        perror("fopen failed");
        return EXIT_FAILURE;
    }

    struct bstNode* root = NULL;

    char buff[256];
    while ( fscanf(fp, "%s", buff)!=EOF ) {
    }

    fclose(fp);
    return 0;
}
