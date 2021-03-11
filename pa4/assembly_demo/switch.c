#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>

char balanced_switch (
    char open
) {
  switch(open) {
      case '<' :
          return ( '>' );
      case '(' :
          return ( ')' );
      case '[' :
          return ( ']' );
      case '{' :
          return ( '}' );
      case '>' :
      case ')' :
      case ']' :
      case '}' :
          return ( 0 );
          break;
      default :
          return ( -1 );
  }
}

int main () {
    return EXIT_SUCCESS;
}
