#include <stdlib.h>
#include <stdio.h>

int main(int argc, char* argv[]) {

  FILE* fp = fopen(argv[1], "r");
  if (!fp) {
    perror("fopen failed");
    return EXIT_FAILURE;
  }

  fclose(fp);

}
