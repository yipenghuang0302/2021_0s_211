#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <math.h>

// Include a header file that has the function prototypes
#include "isPrime.h"

int main(int argc, char* argv[]) {
  int number = atoi(argv[1]);
  int isPrime = is_prime(number);
  printf(isPrime ? "yes\n" : "no\n");
}

bool is_not_prime(int n){
  return !is_prime(n);
}

bool is_prime(int n){

  if (n<2)
    return false;

  for (int i=2; i<=sqrt(n); i++)
    if ((n%i)==0)
      return false;

  return true;
}
