#include <stdio.h>
#include <stdlib.h>

int factorial(int num) {
    int result = 1;

    for (int i = 1; i <= num; i++) {
		result = result * i;
    }

    return result;
}

int main(int argc, char const *argv[])
{
	int num, result;
    
    num = atoi(argv[1]);
    result = factorial(num);

	printf("The factorial of %d is %d\n", num, result);

    return EXIT_SUCCESS;
}
