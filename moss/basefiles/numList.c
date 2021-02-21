#include <stdlib.h>
#include <stdio.h>

int main(int argc, char* argv[]) {

  FILE* fp = fopen(argv[1], "r");
  if (!fp) {
    perror("fopen failed");
    return EXIT_FAILURE;
  }

  char buf[256];

  char* result = fgets(buf, 256, fp);
  printf("First fgets %s\n", result);

  result = fgets(buf, 256, fp);
  printf("Second fgets %s\n", result);

  result = fgets(buf, 256, fp);
  printf("Third fgets %s\n", result);

  fclose(fp);

}
