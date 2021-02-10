#include <stdlib.h>
#include <stdio.h>

struct stack {
    char data;
    struct stack* next;
};

void push ( char value, struct stack s ) { // bug in signature

    struct stack *bracket = malloc(sizeof(struct stack));
    bracket->data = value;
    bracket->next = &s;

    s = *bracket;

    return;
}

char pop ( struct stack **s ) {

    struct stack *temp = *s;
    char data = temp->data;

    *s = (*s)->next;
    free (temp);

    return data;
}

int main () {
    struct stack s;
    push( 'S', s );
    push( 'C', s );
    // printf ("s = %p\n", s);
    struct stack* pointer = &s;
    printf ("pop: %c\n", pop(&pointer));
    printf ("pop: %c\n", pop(&pointer));
}
