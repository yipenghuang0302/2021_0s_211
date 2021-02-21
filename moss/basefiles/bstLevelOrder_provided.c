#include <stdlib.h>
#include <stdio.h>

// A program to perform a LEVEL ORDER (BREADTH-FIRST) TRAVERSAL of a binary search tree

// BINARY SEARCH TREE

typedef struct BSTNode BSTNode;
struct BSTNode {
    int key;
    BSTNode* l_child; // nodes with smaller key will be in left subtree
    BSTNode* r_child; // nodes with larger key will be in right subtree
};

// Add new data to the BST using recursion
BSTNode* insert ( BSTNode* root, int key ) {

    // If the BSTNode doesn't yet exist
    if (root==NULL) {
        root = malloc(sizeof(BSTNode));
        root->l_child = NULL;
        root->r_child = NULL;
        root->key = key;
    }

    // If the BSTNode already exists, then insert key in correct subtree
    // ...
    return root;
}

// Delete the BST using recursion
void delete ( BSTNode* root ) {
    // ...
}


// LINKED LIST IMPLEMENTATION OF QUEUE

// queue needed for level order traversal
typedef struct QueueNode QueueNode;
struct QueueNode {
    BSTNode* data;
    QueueNode* next; // pointer to next node in linked list
};
typedef struct Queue {
    QueueNode* front; // front (head) of the queue
    QueueNode* back; // back (tail) of the queue
} Queue;

// Append a new QueueNode to the back of the Queue
Queue enqueue ( Queue queue, BSTNode* data ) {

    QueueNode* queueNode = malloc(sizeof(QueueNode));
    queueNode->data = data;
    queueNode->next = NULL; // At back of the queue, there is no next node.

    if (queue.back==NULL) { // If the Queue is currently empty
        // ...
    } else {
        // ...
    }

    return queue;
}

// Remove a QueueNode from the front of the Queue
BSTNode* dequeue ( Queue* queue ) {

    if (queue->front==NULL) { // If the Queue is currently empty
        return NULL;
    } else {

        // The QueueNode at front of the queue to be removed
        QueueNode* temp = queue->front;

        if (queue->back==temp) { // If the Queue will become empty
            queue->back = NULL;
        }
        queue->front = temp->next;

        BSTNode* bstNode = temp->data;
        free(temp);
        return bstNode;
    }
}



int main ( int argc, char* argv[] ) {

    // READ INPUT FILE TO CREATE BINARY SEARCH TREE
    FILE* fp = fopen(argv[1], "r");
    if (!fp) {
        perror("fopen failed");
        return EXIT_FAILURE;
    }
    BSTNode* root = NULL;
    int key;
    while ( fscanf(fp, "%d", &key)!=EOF ) {
        root = insert (root, key);
    }
    fclose(fp);

    // USE A QUEUE TO PERFORM LEVEL ORDER TRAVERSAL
    Queue queue = { .front=NULL, .back=NULL };
    // ...

    delete(root);
    return EXIT_SUCCESS;
}
