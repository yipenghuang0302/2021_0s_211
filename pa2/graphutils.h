#include <stdbool.h>
#include <stddef.h>
#include <float.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>

typedef size_t graphNode_t;

typedef struct AdjacencyListNode AdjacencyListNode;
struct AdjacencyListNode {
    graphNode_t graphNode; // the destination graph node
    double weight; // a weight, if weighted graph, otherwise will be 1.0
    AdjacencyListNode* next; // pointer to next linked list node
};

bool almostEqual (double a, double b)
{
    return fabs(a - b) <= DBL_EPSILON;
}

// READ INPUT FILE TO CREATE GRAPH ADJACENCY LIST
// Reads adjacency matrices for both undirected and directed graphs.
// Reads adjacency matrices for both unweighted and weighted graphs.
// Returns the number of nodes in the graph; returns 0 if reading failed.
size_t adjMatrixToList (
    const char* filename, // path to input file containing adjacency matrix
    AdjacencyListNode** adjacencyList
) {

    FILE* fp = fopen(filename, "r");
    if (!fp) {
        perror("fopen failed");
        return 0;
    }

    // first, read the graphNodeCount
    size_t graphNodeCount;
    fscanf(fp, "%ld", &graphNodeCount);

    // next, allocate the linked list heads
    *adjacencyList = calloc( graphNodeCount, sizeof(AdjacencyListNode) );

    // finally, read the adjacency matrix and allocate linked list nodes
    for (size_t adjMatrixRow=0; adjMatrixRow<graphNodeCount; adjMatrixRow++) {

        (*adjacencyList)[adjMatrixRow].graphNode = adjMatrixRow; // A note indicating source graph node
        (*adjacencyList)[adjMatrixRow].next = NULL;

        for (size_t adjMatrixCol=0; adjMatrixCol<graphNodeCount; adjMatrixCol++) {

            double weight;
            fscanf(fp, "%lf", &weight);

            if ( !almostEqual(weight,0.0) ) { // if not almost zero, indicating an edge exists

                AdjacencyListNode* newTop = calloc(1,sizeof(AdjacencyListNode));
                newTop->graphNode = adjMatrixCol;
                newTop->weight = weight;
                newTop->next = (*adjacencyList)[adjMatrixRow].next;

                (*adjacencyList)[adjMatrixRow].next = newTop;

            }
        }
    }
    fclose(fp);

    return graphNodeCount;
}

// TRAVERSE AND FREE THE LINKED LISTS, AND FREE THE ADJACENCY LIST
void freeAdjList (
    size_t graphNodeCount,
    AdjacencyListNode* adjacencyList
) {
    // example of how to traverse the graph adjacency list
    for (size_t source=0; source<graphNodeCount; source++) {

        AdjacencyListNode* dest = adjacencyList[source].next;

        // list iterator
        while (dest) {
            AdjacencyListNode* temp = dest;
            dest = dest->next; // iterator moves to next
            free(temp);
        }

    }
    free(adjacencyList);
}
