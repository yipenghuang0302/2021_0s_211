#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>

typedef struct element {
    int val;
    element* next;
} element;

void freeStack(element* first_node) {
    element* ptr = first_node;

    while (first_node != NULL) {
        ptr = first_node;
        first_node = first_node->next;
        free(ptr);
    }
}