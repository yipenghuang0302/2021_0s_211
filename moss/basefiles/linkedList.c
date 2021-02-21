#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int value;
    struct Node* next;
} Node;

Node* insertNode(Node* head, int val);
void insertNode2(Node** head, int val);
void printList(struct Node* head);
int freeList(Node* head);

Node* insertNode(Node* head, int val) {
    // create a link
    Node* newNode = malloc(sizeof(Node));
    newNode->value = val;

    // point it current head
    newNode->next = head;
    
    // point head to new first node
    head = newNode;

    return head;
}

// allows us to modify the Node* head pointer value
void insertNode2(Node** head, int val) {
    // create a link
    Node* newNode = (Node*) malloc(sizeof(Node));
    newNode->value = val;

    // point it to current head
    newNode->next = *head; // points to the pointer of head (deferenced)

    // point first to new first node
    *head = newNode;
}

void printList(Node* head) {
    struct Node* ptr = head;
    struct Node* prev = NULL;
    while (ptr != NULL) {
        if (ptr == head || ptr->value != prev->value) {
            printf("%d\t", ptr->value);
        }
        prev = ptr;
        ptr = ptr->next;
    }
    printf("\n");
}

int freeList(Node* head) {
    Node* tempNode = head;
    while (head != NULL) {
        tempNode = head;
        head = head->next;
        free(tempNode);
    }

    return EXIT_SUCCESS;
}

int main(int argc, char const *argv[])
{
    FILE* fp;
    fp = fopen(argv[1], "r");
    if (fp == NULL) {
        printf("file error\n");
        return EXIT_FAILURE;
    }

    // create head
    Node* head = NULL;
    head = (Node*) malloc(sizeof(Node));
    head->value = 0; // Syntactic sugar for (*head).value = 100;
    head->next = NULL;

    // scan values and insert them into the linked list
    int buff;
    while (fscanf(fp, "%d", &buff) == 1) {
        // insert new node method 2
        insertNode2(&head, buff);

        // insert new node method 1
        // head = insertNode(head, buff);
    }
    
    printList(head);
    freeList(head);

    return EXIT_SUCCESS;
}
